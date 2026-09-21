"""Test doubles for the network, and the guard that makes sure there is no network.

``python3 -m unittest discover -s tests -t .`` must pass with the machine unplugged. Nothing in
this file opens a socket: ``install()`` replaces ``socket.socket`` and ``socket.getaddrinfo`` for
the duration of a test, and any attempt to reach the real network raises instead of connecting.
A test that accidentally depends on the network therefore fails, loudly, rather than passing on
a machine that happens to be online.
"""

from __future__ import annotations

import socket
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from unittest import mock

from sitewalk import fetch, guard

FIXTURES = Path(__file__).parent / "fixtures"


class NetworkRefused(AssertionError):
    """Raised when a test tried to open a real socket."""


def no_sockets(*_args, **_kwargs):
    raise NetworkRefused(
        "this test tried to open a real socket; the suite must run with no network"
    )


def refuse_lookup(*_args, **_kwargs):
    raise NetworkRefused("this test tried to resolve a real name")


def address(ip: str, port: int = 443, host: str = "example.com") -> guard.Address:
    family = socket.AF_INET6 if ":" in ip else socket.AF_INET
    sockaddr = (ip, port, 0, 0) if family == socket.AF_INET6 else (ip, port)
    return guard.Address(host=host, port=port, family=family, sockaddr=sockaddr)


def resolver_for(*addresses: str):
    """A resolver that always answers with these addresses, in this order."""

    def resolve(host: str, port: int) -> list[guard.Address]:
        return [address(ip, port, host) for ip in addresses]

    return resolve


def resolver_map(mapping: dict[str, list[str]]):
    """A resolver that answers per host name, and treats an unknown name as unresolvable."""

    def resolve(host: str, port: int) -> list[guard.Address]:
        if host not in mapping:
            raise socket.gaierror(f"no fake answer for {host}")
        return [address(ip, port, host) for ip in mapping[host]]

    return resolve


@dataclass
class FakeSocket:
    """A socket that reports the peer address it was told to report."""

    peer: tuple = ("93.184.216.34", 443)

    def getpeername(self) -> tuple:
        return self.peer


class FakeResponse:
    """Enough of ``http.client.HTTPResponse`` for :func:`sitewalk.fetch.fetch_once`."""

    def __init__(self, status: int, body: bytes, headers: dict[str, str]) -> None:
        self.status = status
        self._body = body
        self._headers = list(headers.items())

    def read(self, amount: int | None = None) -> bytes:
        if amount is None:
            return self._body
        return self._body[:amount]

    def getheaders(self) -> list[tuple[str, str]]:
        return list(self._headers)


@dataclass
class FakeConnection:
    """A connection that answers from a route table and records what was asked for.

    ``sock`` is the attribute ``guard.peer_is_public`` reads, so it is named that here too.
    """

    routes: dict
    sock: FakeSocket | None = None
    requests: list[str] = field(default_factory=list)
    closed: bool = False

    def request(self, method: str, path: str, headers: dict | None = None) -> None:
        self.requests.append(path)

    def getresponse(self) -> FakeResponse:
        path = self.requests[-1]
        # An HTTP request line carries the path without a trailing slash, so ``/about`` and
        # ``/about/`` are the same request. The route table is keyed the way the crawler names
        # URLs, so the lookup strips it.
        entry = self.routes.get(path.rstrip("/") or "/")
        if entry is None:
            return FakeResponse(404, b"", {"content-type": "text/html"})
        if callable(entry):
            entry = entry()
        if isinstance(entry, FakeResponse):
            return entry
        status, body, headers = entry
        return FakeResponse(status, body, headers)

    def close(self) -> None:
        self.closed = True


@dataclass
class FakeHTTP:
    """A stand-in for a site: paths to routes, plus the connections that were opened.

    ``peer_host`` is the address the connection reports having reached. It defaults to the host
    that was asked for, which is what a real connection does; a test that needs the peer check
    to fail sets it to a non-public address.
    """

    routes: dict
    peer_host: str | None = None
    connections: list[FakeConnection] = field(default_factory=list)

    def connector(self, scheme: str, host: str, port: int, timeout: float) -> FakeConnection:
        reached = self.peer_host or "93.184.216.34"
        connection = FakeConnection(routes=self.routes, sock=FakeSocket((reached, port)))
        self.connections.append(connection)
        return connection

    def add(self, path: str, body: str | bytes, content_type: str = "text/html", status: int = 200):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.routes[path.rstrip("/") or "/"] = (status, body, {"content-type": content_type})
        return self

    def redirect(self, path: str, location: str, status: int = 301):
        self.routes[path.rstrip("/") or "/"] = (
            status,
            b"",
            {"location": location, "content-type": "text/html"},
        )
        return self

    @property
    def paths_requested(self) -> list[str]:
        return [path for connection in self.connections for path in connection.requests]


class FakeSource:
    """A minimal ``PageSource`` for the crawl tests, with no HTTP and no filesystem."""

    kind = "fake"
    label = "fake source"

    def __init__(self, pages: dict[str, tuple[int, str, str]], origin: str = "https://example.com"):
        #: url path -> (status, content_type, body)
        self.pages = pages
        self.origin = origin
        self.requested: list[str] = []

    def fetch(self, url):
        from sitewalk.facts import Page

        self.requested.append(url)
        path = url.split(self.origin, 1)[-1] or "/"
        entry = self.pages.get(path)
        if entry is None:
            return Page(url=url, status=404, content_type="text/html", error="not in the fake source")
        status, content_type, body = entry
        return Page(url=url, status=status, content_type=content_type, body=body)

    def exists(self, url: str) -> bool:
        return (url.split(self.origin, 1)[-1] or "/") in self.pages


@contextmanager
def no_network():
    """Fail any attempt to open a socket or resolve a name."""
    with mock.patch.object(socket, "socket", no_sockets), mock.patch.object(
        socket, "getaddrinfo", refuse_lookup
    ), mock.patch.object(socket, "create_connection", no_sockets):
        yield


@contextmanager
def fake_network(http: FakeHTTP, ips: list[str] | None = None):
    """Serve the fetch layer from a fake site, with no socket and no name resolution."""
    resolve = resolver_for(*(ips or ["93.184.216.34"]))
    with mock.patch.object(guard, "default_resolver", resolve), mock.patch.object(
        socket, "socket", no_sockets
    ), mock.patch.object(socket, "getaddrinfo", refuse_lookup):
        yield http


def live_source(http: FakeHTTP, ips: list[str] | None = None, **kwargs):
    """A ``LiveSource`` wired to the fake connection, with a public fake resolver."""
    from sitewalk.sources import LiveSource

    options = {
        "origin": "https://example.com",
        "delay": 0.0,
        "resolver": resolver_for(*(ips or ["93.184.216.34"])),
        "connector": http.connector,
    }
    options.update(kwargs)
    return LiveSource(**options)
