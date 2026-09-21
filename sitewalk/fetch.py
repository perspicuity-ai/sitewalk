"""HTTP fetching, and the only module in this package that opens a socket.

Every request passes the guard first, and the peer address is checked again after connecting.
Redirects are followed one hop at a time, each hop validated from scratch, so a public host
cannot bounce this crawl to ``169.254.169.254``.

Nothing here executes JavaScript, sends a cookie, or reads a credential. The client identifies
itself in the ``User-Agent`` because a site owner reading their logs is entitled to know who
came.
"""

from __future__ import annotations

import http.client
import socket
import ssl
from typing import Callable
from urllib.parse import urljoin

from . import guard
from .errors import FetchError, GuardError
from .facts import MAX_BODY_CHARS, Page
from .pages import content_type_of
from .urls import origin_of

VERSION = "0.1.0"
PROJECT_URL = "https://github.com/perspicuity-ai/sitewalk"
USER_AGENT = f"Sitewalk/{VERSION} (+{PROJECT_URL})"

MAX_REDIRECTS = 5
MAX_EXTRA_BYTES = 64 * 1024

REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml,text/plain;q=0.9,*/*;q=0.5",
    "Accept-Encoding": "identity",
    "Connection": "close",
}

#: A connector takes ``(scheme, host, port, timeout)`` and returns an unconnected connection.
Connector = Callable[[str, str, int, float], http.client.HTTPConnection]


def default_connector(scheme: str, host: str, port: int, timeout: float):
    if scheme == "https":
        return http.client.HTTPSConnection(
            host, port, timeout=timeout, context=ssl.create_default_context()
        )
    return http.client.HTTPConnection(host, port, timeout=timeout)


def _error_page(url: str, exc: Exception) -> Page:
    return Page(url=url, status=0, error=f"{type(exc).__name__}: {exc}")


def _read_within(response, limit_bytes: int) -> tuple[bytes, bool]:
    """Read at most ``limit_bytes``, and report whether the response was longer."""
    raw = response.read(limit_bytes + 1)
    if len(raw) > limit_bytes:
        return raw[:limit_bytes], True
    return raw, False


def _answered(url: str, page: Page, final_url: str) -> Page:
    """Re-key a followed response on the URL that was asked for.

    ``page.url`` is always what the caller requested and ``redirect_to`` says where the content
    actually came from. The distinction is what stops a redirect from renaming a page in the
    report: the crawl asked about ``/old/``, and that is the page whose facts it records.
    """
    return Page(
        url=url,
        status=page.status,
        content_type=page.content_type,
        body=page.body,
        error=page.error,
        truncated=page.truncated,
        note=page.note,
        redirect_to=final_url if final_url != url else None,
    )


def fetch_once(
    url: str,
    *,
    resolver: guard.Resolver = guard.default_resolver,
    connector: Connector | None = None,
    user_agent: str = USER_AGENT,
    timeout: float = 10.0,
    max_body: int = MAX_BODY_CHARS,
    extra_body: bool = False,
) -> tuple[Page, str | None]:
    """Fetch one URL without following a redirect.

    Returns the page and, when the response was a redirect, the absolute target. A refusal from
    the guard is raised; a network failure is returned as a page with status 0, because one
    unreachable page is a finding about the site, not a reason to lose the run.
    """
    scheme, host, port, path = guard.parse_target(url)
    guard.check_host(host, port, resolver)

    connect = connector or default_connector
    connection = connect(scheme, host, port, timeout)
    try:
        connection.request("GET", path, headers={"User-Agent": user_agent, **REQUEST_HEADERS})
        # The check that closes the DNS-rebinding window: the name resolved to a public
        # address, and now the address actually connected to is confirmed to be one.
        guard.check_peer(connection, url)
        response = connection.getresponse()
        status = int(response.status)
        headers = {key.lower(): value for key, value in response.getheaders()}
        content_type = content_type_of(headers, url)
        limit = MAX_EXTRA_BYTES if extra_body else max_body
        location = headers.get("location")
        if status in (301, 302, 303, 307, 308) or (not 200 <= status < 300):
            # A redirect body is not this tool's business, and an error body is not content.
            return Page(url=url, status=status, content_type=content_type), (
                urljoin(url, location) if location else None
            )
        raw, truncated = _read_within(response, limit)
        body = raw.decode("utf-8", errors="replace")
        return (
            Page(
                url=url,
                status=status,
                content_type=content_type,
                body=body,
                truncated=truncated,
            ),
            urljoin(url, location) if location else None,
        )
    except GuardError:
        raise
    except (OSError, http.client.HTTPException, ssl.SSLError, UnicodeError) as exc:
        return _error_page(url, exc), None
    finally:
        try:
            connection.close()
        except Exception:  # pragma: no cover - a close failure must not mask the result
            pass


def fetch(
    url: str,
    *,
    resolver: guard.Resolver = guard.default_resolver,
    connector: Connector | None = None,
    user_agent: str = USER_AGENT,
    timeout: float = 10.0,
    max_body: int = MAX_BODY_CHARS,
    extra_body: bool = False,
    max_redirects: int = MAX_REDIRECTS,
    allowed_origin: str | None = None,
) -> Page:
    """Fetch a URL, following at most ``max_redirects`` hops and validating every one.

    ``allowed_origin`` keeps the crawl on the submitted site: a redirect off it is refused
    rather than followed, because following it would fetch a host the user did not submit.
    """
    current = url
    hops: list[str] = []
    for _hop in range(max_redirects + 1):
        page, target = fetch_once(
            current,
            resolver=resolver,
            connector=connector,
            user_agent=user_agent,
            timeout=timeout,
            max_body=max_body,
            extra_body=extra_body,
        )
        if target is None:
            return _answered(url, page, current)
        if len(hops) >= max_redirects:
            return Page(
                url=url,
                status=0,
                error=f"stopped after {max_redirects} redirects",
                redirect_to=target,
            )
        if allowed_origin and origin_of(target) != origin_of(allowed_origin):
            # Following it would fetch a host the user did not submit. Refused, and said so.
            return Page(
                url=url,
                status=0,
                error=f"refused a redirect off the submitted origin, to {target}",
                redirect_to=target,
            )
        hops.append(target)
        current = target
    raise FetchError(f"redirect handling failed for {url}")  # pragma: no cover
