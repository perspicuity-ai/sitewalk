"""The address guard: every rule about which host may be connected to.

This is the security boundary of the package, and it is a *port* of the tested guard in
``agent-eligibility/eligibility/fetch.py`` (Apache-2.0, same organisation), rewritten against
this package's types. The rules are unchanged and deliberate:

* ``http`` and ``https`` only, on ports 80 and 443 only;
* the hostname is resolved **first** and every returned address must be public;
* the connected peer address is checked **again** after the connection is made, which is what
  closes the DNS-rebinding gap a resolve-only check leaves open;
* every redirect hop is validated from scratch, so a public host cannot bounce a crawl to
  ``169.254.169.254``.

Refusing on the *resolved address* rather than on the hostname string is the point: a
name-based blocklist is bypassed by a DNS record.

Nothing else in the package may decide whether an address is reachable. ``fetch.py`` is the only
module that opens a socket, and it asks this one first.
"""

from __future__ import annotations

import ipaddress
import socket
from dataclasses import dataclass
from typing import Callable
from urllib.parse import urlsplit, urlunsplit

from .errors import GuardError

ALLOWED_SCHEMES = ("http", "https")

#: The one port each scheme may use. ``http://host:443`` is refused as well as ``:8080``: the
#: specification is a port *per scheme*, not a set of two ports.
ALLOWED_PORTS = {"http": 80, "https": 443}


@dataclass(frozen=True)
class Address:
    """One answer from the resolver, in the shape ``socket.getaddrinfo`` returns."""

    host: str
    port: int
    family: int
    sockaddr: tuple


#: A resolver takes ``(host, port)`` and returns every address the name maps to.
Resolver = Callable[[str, int], list[Address]]


def default_resolver(host: str, port: int) -> list[Address]:
    """Resolve with the standard library, returning every answer rather than the first."""
    infos = socket.getaddrinfo(host, port, proto=socket.IPPROTO_TCP)
    out: list[Address] = []
    for family, _type, _proto, _canon, sockaddr in infos:
        out.append(Address(host=host, port=port, family=family, sockaddr=sockaddr))
    return out


def is_public_address(ip: str) -> bool:
    """True only for a globally routable unicast address.

    ``is_global`` alone is not sufficient: on some Python versions a multicast address reports
    as global, and this function is a security boundary, so the exclusions are written out
    rather than inferred. An IPv4-mapped IPv6 address is unwrapped to its IPv4 form first, so
    ``::ffff:127.0.0.1`` is refused rather than treated as a distinct address space.
    """
    try:
        parsed = ipaddress.ip_address(ip)
    except ValueError:
        return False
    if isinstance(parsed, ipaddress.IPv6Address) and parsed.ipv4_mapped is not None:
        parsed = parsed.ipv4_mapped
    if (
        parsed.is_private
        or parsed.is_loopback
        or parsed.is_link_local
        or parsed.is_multicast
        or parsed.is_reserved
        or parsed.is_unspecified
    ):
        return False
    return bool(parsed.is_global)


def parse_target(url: str) -> tuple[str, str, int, str]:
    """Validate a URL's scheme, host and port, and return them split.

    Raises :class:`GuardError`, naming the rule, for anything that is not ``http`` or ``https``
    on port 80 or 443.
    """
    parts = urlsplit((url or "").strip())
    scheme = (parts.scheme or "").lower()
    if scheme not in ALLOWED_SCHEMES:
        raise GuardError(f"refused scheme {scheme or '(none)'!r}: only http and https are fetched")
    if not parts.hostname:
        raise GuardError("refused a url with no host")
    try:
        port = parts.port
    except ValueError as exc:
        raise GuardError(f"refused an invalid port: {exc}") from exc
    default_port = ALLOWED_PORTS[scheme]
    if port is None:
        port = default_port
    elif port != default_port:
        raise GuardError(
            f"refused port {port}: {scheme} is fetched on port {default_port} only"
        )
    host = parts.hostname
    try:
        host = host.encode("idna").decode("ascii")
    except UnicodeError as exc:
        raise GuardError(f"refused an unusable hostname: {exc}") from exc
    # Credentials in a URL are never used and never stored; dropping them keeps them out of any
    # message this function raises and out of the report.
    path = urlunsplit(("", "", parts.path or "/", parts.query, ""))
    return scheme, host.lower(), port, path


def check_host(host: str, port: int, resolver: Resolver = default_resolver) -> list[Address]:
    """Resolve the host and refuse it if **any** answer is not globally routable.

    Refusing on any answer, rather than on the first, is deliberate: a name with one public and
    one private answer is a name that can be made to serve either.

    A literal address is refused on the string itself, without asking the resolver, so
    ``--url http://169.254.169.254/`` is refused by the rule that governs it rather than by
    whatever a resolver happens to return for a numeric host.
    """
    literal = _literal_address(host)
    if literal is not None:
        if not is_public_address(literal):
            raise GuardError(f"refused {host}: it is the non-public address {literal}")
        return [Address(host=host, port=port, family=socket.AF_INET, sockaddr=(literal, port))]
    try:
        addresses = resolver(host, port)
    except socket.gaierror as exc:
        raise GuardError(f"could not resolve {host}: {exc}") from exc
    if not addresses:
        raise GuardError(f"could not resolve {host}")
    for address in addresses:
        ip = address.sockaddr[0]
        if not is_public_address(str(ip)):
            raise GuardError(f"refused {host}: it resolves to the non-public address {ip}")
    return addresses


def _literal_address(host: str) -> str | None:
    """The host as a literal IP address, or None when it is a name."""
    candidate = (host or "").strip().strip("[]")
    try:
        return str(ipaddress.ip_address(candidate))
    except ValueError:
        return None


def peer_is_public(connection) -> tuple[bool, str]:
    """Check the address actually connected to, after connecting.

    Returns whether it is public and the address itself, so a refusal can name it. A connection
    with no socket, or one whose peer cannot be read, is not public: an unknown peer is refused
    rather than trusted.
    """
    sock = getattr(connection, "sock", None)
    if sock is None:
        return False, "(no socket)"
    try:
        peer = sock.getpeername()
    except (OSError, AttributeError):
        # A socket-like object that cannot report its peer is treated as unknown, and an
        # unknown peer is refused rather than trusted.
        return False, "(unreadable peer)"
    if not peer:
        return False, "(no peer)"
    address = str(peer[0])
    return is_public_address(address), address


def check_peer(connection, url: str) -> str:
    """Raise unless the connected peer of ``connection`` is a public address."""
    public, address = peer_is_public(connection)
    if not public:
        raise GuardError(
            f"refused {url}: the connected peer address is not public ({address})"
        )
    return address
