"""The two sources: a live site over HTTP, and an already-built directory on disk.

The local source is the one that matters most — it is the deploy gate — so it performs **no
network access at all**. It does not import ``socket``, it does not resolve a name, and it has
no URL guard because it never reaches a URL. Its targets are the submitted origin's paths mapped
onto files, and a path that escapes the directory is refused rather than served.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol
from urllib.parse import unquote, urlsplit

from . import fetch, guard
from .facts import MAX_BODY_CHARS, Page
from .pages import content_type_of
from .urls import SURFACE_PATHS, normalise, origin_of, relative_path


class PageSource(Protocol):
    """What the crawl needs from a source, and nothing more."""

    kind: str
    #: A description of what was read, for the report's first line.
    label: str

    def fetch(self, url: str) -> Page: ...

    def exists(self, url: str) -> bool: ...


@dataclass
class FileSource:
    """Read pages from a built directory. No network, by construction.

    A URL path maps to a file under ``root``: ``/`` to ``index.html``, ``/about/`` to
    ``about/index.html``, ``/about`` to ``about.html`` or ``about/index.html``. A query string
    is not part of a filename, so the query is dropped for the mapping and named in the note —
    two URLs that differ only by query map to the same file, and saying so beats pretending the
    build holds a distinction it does not.

    ``origin`` is synthetic: a build directory has no host, so one is chosen to make paths and
    relative links work. Links written as absolute URLs to the real site are therefore external
    here, and are counted but never fetched.
    """

    root: Path
    origin: str = "https://localhost"
    _resolved_root: Path = field(init=False, repr=False)

    kind = "dir"

    def __post_init__(self) -> None:
        self.root = Path(self.root)
        self._resolved_root = self.root.resolve()
        self.label = str(self.root)

    def resolve_path(self, url: str) -> Path | None:
        """Map a URL to a file inside the root, or None if it escapes or does not exist."""
        parts = urlsplit(url)
        path = unquote(parts.path or "/")
        if "\x00" in path:
            return None
        candidate = self._resolved_root / path.lstrip("/")
        for option in self._candidates(candidate, path):
            resolved = option.resolve()
            if resolved != self._resolved_root and self._resolved_root not in resolved.parents:
                # The path tried to leave the directory. Refused, not served.
                return None
            if resolved.is_file():
                return resolved
        return None

    @staticmethod
    def _candidates(candidate: Path, path: str) -> list[Path]:
        if path.endswith("/"):
            return [candidate / "index.html"]
        return [candidate, candidate / "index.html", Path(str(candidate) + ".html")]

    def exists(self, url: str) -> bool:
        return self.resolve_path(url) is not None

    def read(self, url: str) -> bytes | None:
        path = self.resolve_path(url)
        if path is None:
            return None
        return path.read_bytes()

    def fetch(self, url: str) -> Page:
        parts = urlsplit(url)
        path = self.resolve_path(url)
        if path is None:
            return Page(url=url, status=404, error="no file in the build directory")
        try:
            raw = path.read_bytes()
        except OSError as exc:
            return Page(url=url, status=0, error=f"{type(exc).__name__}: {exc}")
        truncated = len(raw) > MAX_BODY_CHARS
        body = raw[:MAX_BODY_CHARS].decode("utf-8", errors="replace")
        if path.name == "index.html":
            content_type = "text/html"
        else:
            content_type = content_type_of({}, path.name)
            if not content_type:
                content_type = "text/html" if path.suffix.lower() in ("", ".html", ".htm") else "application/octet-stream"
        note = None
        if parts.query:
            note = f"the query string {parts.query!r} is not a filename and was not applied"
        return Page(
            url=normalise(url),
            status=200,
            content_type=content_type,
            body=body,
            truncated=truncated,
            note=note,
        )


@dataclass
class LiveSource:
    """Fetch pages over HTTP, through the guard, with a polite delay between requests.

    ``fetch`` is answered from a cache when the crawl has already asked for that URL, so a page
    that is both linked and listed in the sitemap costs one request rather than two.
    """

    origin: str
    user_agent: str = fetch.USER_AGENT
    timeout: float = 10.0
    delay: float = 0.2
    #: Body cap in characters. A longer body is truncated and the page says so.
    max_body: int = MAX_BODY_CHARS
    #: How names are resolved and how connections are opened. Both default to the real ones.
    #: ``build`` below fills them from the modules as they are *now*, rather than letting a
    #: dataclass default capture them at import time — which is what made the command line
    #: impossible to exercise without a network.
    resolver: guard.Resolver | None = None
    connector: fetch.Connector | None = None
    _last_request: float = field(default=0.0, init=False, repr=False)
    _cache: dict[str, Page] = field(default_factory=dict, init=False, repr=False)
    _refused: list[str] = field(default_factory=list, init=False, repr=False)

    kind = "url"

    def __post_init__(self) -> None:
        self.label = self.origin
        if self.resolver is None:
            self.resolver = guard.default_resolver
        if self.connector is None:
            self.connector = fetch.default_connector

    def _sleep(self) -> None:
        if self.delay <= 0:
            return
        now = time.monotonic()
        wait = self.delay - (now - self._last_request)
        if self._last_request and wait > 0:
            time.sleep(wait)
        self._last_request = time.monotonic()

    def read(self, url: str) -> bytes | None:
        """Read a small side file. Same guard, same delay, no cache."""
        if url in self._cache and self._cache[url].body is not None:
            return self._cache[url].body.encode("utf-8", errors="replace")
        self._sleep()
        try:
            page = fetch.fetch(
                url,
                resolver=self.resolver,
                connector=self.connector,
                user_agent=self.user_agent,
                timeout=self.timeout,
                max_body=self.max_body,
                extra_body=True,
                allowed_origin=self.origin,
            )
        except guard.GuardError as exc:
            self._refused.append(str(exc))
            return None
        return page.body.encode("utf-8", errors="replace") if page.body is not None else None

    def exists(self, url: str) -> bool:
        page = self.fetch(url)
        return page.ok

    def fetch(self, url: str) -> Page:
        if url in self._cache:
            return self._cache[url]
        self._sleep()
        try:
            page = fetch.fetch(
                url,
                resolver=self.resolver,
                connector=self.connector,
                user_agent=self.user_agent,
                timeout=self.timeout,
                max_body=self.max_body,
                allowed_origin=self.origin,
            )
        except guard.GuardError as exc:
            # A refusal is not a site finding; it is the tool declining to make a request.
            self._refused.append(str(exc))
            page = Page(url=url, status=0, error=f"refused: {exc}")
        self._cache[url] = page
        return page

    @property
    def refusals(self) -> tuple[str, ...]:
        """Every request the guard declined, for the report."""
        return tuple(self._refused)
