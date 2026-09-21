"""URL handling shared by every module that touches one.

There is exactly one definition of "same origin" and one definition of "the key a URL is
deduplicated by", because a crawl that disagrees with itself about either one silently
fetches the same page twice or wanders off the site.
"""

from __future__ import annotations

from urllib.parse import urldefrag, urljoin, urlsplit, urlunsplit

#: Paths that are never crawled as pages. They are read as surfaces where that is their role.
SURFACE_PATHS = ("robots.txt", "sitemap.xml", "llms.txt", "rss.xml")


def origin_of(url: str) -> str:
    """Return ``scheme://host[:port]`` with the default port omitted.

    A default port is dropped so that ``https://example.com:443/`` and ``https://example.com/``
    are one origin rather than two.
    """
    parts = urlsplit(url)
    scheme = (parts.scheme or "").lower()
    host = (parts.hostname or "").lower()
    if not host:
        return ""
    try:
        port = parts.port
    except ValueError:
        return ""
    if port is None or (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
        return f"{scheme}://{host}"
    return f"{scheme}://{host}:{port}"


def normalise(url: str, base: str = "") -> str:
    """Return the canonical form of a link target, for comparison and deduplication.

    * the fragment is dropped, because a fragment is not a request;
    * the scheme and host are lower-cased;
    * a default port is dropped;
    * an empty path becomes ``/``, so ``https://a.com`` and ``https://a.com/`` are one URL.

    The query string is preserved: ``?page=2`` is a different page from ``?page=3``.
    """
    absolute = urljoin(base, url.strip()) if base else url.strip()
    absolute, _fragment = urldefrag(absolute)
    parts = urlsplit(absolute)
    scheme = (parts.scheme or "").lower()
    host = (parts.hostname or "").lower()
    if not scheme or not host:
        return ""
    try:
        port = parts.port
    except ValueError:
        return ""
    if port is None or (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
        netloc = host
    else:
        netloc = f"{host}:{port}"
    path = parts.path or "/"
    return urlunsplit((scheme, netloc, path, parts.query, ""))


def stays_on_site(candidate: str, origin: str) -> bool:
    """True when a redirect target is the same site as the one submitted.

    Stricter than :func:`same_origin` in one direction and looser in another, both deliberately:

    * the host and port must be **identical**, so a redirect cannot move the crawl to a shared
      host or a different port;
    * the scheme must be the same **or an upgrade from http to https**, which is the single most
      common redirect on the web. Refusing it would refuse the redirect that every plain-HTTP
      site performs, and the tool would report a site as unreachable when it is merely
      redirecting to its own TLS endpoint;
    * an https-to-http downgrade is refused, because it is not part of reaching the submitted
      site and it silently drops transport security mid-crawl.
    """
    target = urlsplit(candidate)
    base = urlsplit(origin)
    if not target.hostname or not base.hostname:
        return False
    if (target.hostname or "").lower() != (base.hostname or "").lower():
        return False

    def port_of(parts):
        """The port, or the scheme's default. ``None`` means "not stated"."""
        try:
            port = parts.port
        except ValueError:
            return None
        if port is not None:
            return port
        return 443 if (parts.scheme or "").lower() == "https" else 80

    target_scheme = (target.scheme or "").lower()
    base_scheme = (base.scheme or "").lower()
    target_port = port_of(target)
    base_port = port_of(base)
    if target_port is None or base_port is None:
        return False
    if target_port != base_port:
        # An explicit port must match exactly. Without this, ``https://host/`` and
        # ``https://host:8443/`` would compare equal because both default to 443 and 8443 is
        # not a scheme default -- but 8443 is a different listener on the same name.
        explicit = target.port is not None or base.port is not None
        if explicit:
            return False
    if target_scheme == base_scheme:
        return True
    return base_scheme == "http" and target_scheme == "https"


def same_origin(candidate: str, origin: str) -> bool:
    """True when ``candidate`` is inside the submitted origin.

    An empty ``origin`` matches nothing, so a bug that loses the origin refuses the whole site
    rather than allowing the whole web.
    """
    if not origin:
        return False
    return origin_of(candidate) == origin_of(origin)


def relative_path(url: str) -> str:
    """The origin-relative path of a URL, for display and for filesystem mapping."""
    parts = urlsplit(url)
    path = parts.path or "/"
    if parts.query:
        path = f"{path}?{parts.query}"
    return path
