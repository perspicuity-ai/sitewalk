"""What one page exposes to a machine, read with ``html.parser`` and nothing else.

The parser here is deliberately shallow. It collects the facts the product promises and no more;
a tree builder would invite claims about structure this tool has not been asked to make, and
would be a large amount of tag-soup handling to own.

The one judgement in this module is :func:`looks_like_a_script_shell`. It is a **heuristic**, it
is labelled as one everywhere it is reported, and its thresholds are recorded in
docs/DESIGN.md. It exists so the tool can say "this may be rendered by JavaScript" instead of
printing a visible-text length of zero and implying the page is empty. It does not establish
that a page is empty, and it does not establish that a browser would see content.
"""

from __future__ import annotations

import json
from html.parser import HTMLParser
from typing import Any
from urllib.parse import urlsplit

from .facts import MAX_BODY_CHARS, Page, PageFact
from .urls import normalise, origin_of

#: Elements whose contents are not visible text and are not read for anything else.
_IGNORED = frozenset({"script", "style", "noscript", "template", "svg", "iframe"})

#: Elements that imply an application root a script would render into.
_APP_ROOT_IDS = frozenset({"root", "app", "___gatsby", "__next"})

#: Thresholds for the script-shell heuristic. Recorded in docs/DESIGN.md so a change is visible.
SCRIPT_SHELL_TEXT_CHARS = 200
SCRIPT_SHELL_SCRIPT_BYTES = 5000

#: Link schemes that are not navigations, and are therefore never counted or fetched.
_NON_NAVIGATIONAL = ("mailto:", "tel:", "javascript:", "data:", "sms:", "ftp:", "file:")


def _attr(attrs: list[tuple[str, str | None]], name: str) -> str | None:
    for key, value in attrs:
        if key.lower() == name:
            return value
    return None


def _collapse(text: str) -> str:
    return " ".join(text.split())


def extract_json_ld_types(data: Any) -> list[str]:
    """Collect every ``@type`` value in a JSON-LD document, in first-seen order.

    Handles the shapes that appear in the wild: a single object, a list of objects, and a
    ``@graph`` wrapper. ``@type`` may be a string or a list of strings, and nested objects are
    walked, because a type a page publishes inside a nested entity is still published.
    """
    found: list[str] = []

    def add(value: Any) -> None:
        if isinstance(value, str):
            text = value.strip()
            if text and text not in found:
                found.append(text)
        elif isinstance(value, list):
            for item in value:
                add(item)

    def walk(node: Any) -> None:
        if isinstance(node, list):
            for item in node:
                walk(item)
            return
        if not isinstance(node, dict):
            return
        if "@type" in node:
            add(node["@type"])
        for key, value in node.items():
            if key != "@type" and isinstance(value, (dict, list)):
                walk(value)

    walk(data)
    return found


class _HtmlCollector(HTMLParser):
    """Collect the page facts in one pass, in document order."""

    def __init__(self, page_url: str, origin: str) -> None:
        super().__init__(convert_charrefs=True)
        self.page_url = page_url
        self.origin = origin
        self.origin_host = (urlsplit(page_url).hostname or "").lower()
        self.title: str | None = None
        self.seen_title_element = False
        self.description: str | None = None
        self.canonical: str | None = None
        self.json_ld_blocks = 0
        self.json_ld_malformed = 0
        self.json_ld_types: list[str] = []
        self.internal_targets: list[str] = []
        self.external_links = 0
        self.script_bytes = 0
        self.script_blocks = 0
        self.app_root = False
        self.visible_chars = 0

        self._in_title = 0
        self._in_json_ld = 0
        self._ignored = 0
        self._text: list[str] = []
        self._title_chunks: list[str] = []
        self._ld_chunks: list[str] = []
        self._internal_seen: set[str] = set()

    # -- tag handling ------------------------------------------------------------------

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag == "title":
            self._in_title += 1
            self.seen_title_element = True
        elif tag == "meta":
            self._meta(attrs)
        elif tag == "link":
            self._link(attrs)
        elif tag == "a":
            self._anchor(attrs)
        elif tag == "script":
            self._open_script(attrs)
        elif tag in _IGNORED:
            self._ignored += 1
        if _attr(attrs, "id") in _APP_ROOT_IDS:
            self.app_root = True

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        # ``<script src=... />`` is invalid HTML but common. Opening and immediately closing it
        # keeps the ignored counter balanced, which a bare start-tag event would not.
        lowered = tag.lower()
        self.handle_starttag(lowered, attrs)
        if lowered in _IGNORED or lowered == "title":
            self.handle_endtag(lowered)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title" and self._in_title:
            self._in_title -= 1
            self._finish_title()
        elif tag == "script":
            self._close_script()
        elif tag in _IGNORED and self._ignored:
            self._ignored -= 1

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_chunks.append(data)
            return
        if self._in_json_ld:
            self._ld_chunks.append(data)
            return
        if self._ignored:
            if self.script_blocks:
                # Inline script content is the strongest signal for the shell heuristic.
                self.script_bytes += len(data)
            return
        self._text.append(data)

    def close_document(self) -> None:
        """Finish the document. Named apart from the base class's ``close`` on purpose.

        ``super().close()`` is what flushes the parser's buffer and fires the end tags for
        anything still open. Without it a document whose last element is an empty ``<title>``
        never reports that element at all, which reads as "the page declares no title" when the
        page in fact declares an empty one.
        """
        super().close()
        while self._in_json_ld:
            self._close_script()
        while self._ignored:
            self._ignored -= 1
        self._finish_title()
        self.visible_chars = len(_collapse("".join(self._text)))

    # -- helpers -----------------------------------------------------------------------

    def _meta(self, attrs: list[tuple[str, str | None]]) -> None:
        name = (_attr(attrs, "name") or _attr(attrs, "property") or "").strip().lower()
        content = _attr(attrs, "content")
        if content is None:
            return
        if name == "description" and self.description is None:
            self.description = _collapse(content)

    def _link(self, attrs: list[tuple[str, str | None]]) -> None:
        rel = (_attr(attrs, "rel") or "").strip().lower()
        href = _attr(attrs, "href")
        if "canonical" in rel.split() and href and self.canonical is None:
            self.canonical = normalise(href, self.page_url)

    def _anchor(self, attrs: list[tuple[str, str | None]]) -> None:
        href = _attr(attrs, "href")
        if not href:
            return
        stripped = href.strip()
        if not stripped or stripped.startswith("#") or stripped.lower().startswith(_NON_NAVIGATIONAL):
            return
        target = normalise(stripped, self.page_url)
        if not target:
            return
        if origin_of(target) == self.origin:
            if target not in self._internal_seen:
                self._internal_seen.add(target)
                self.internal_targets.append(target)
        else:
            self.external_links += 1

    def _open_script(self, attrs: list[tuple[str, str | None]]) -> None:
        self.script_blocks += 1
        self._ignored += 1
        script_type = (_attr(attrs, "type") or "").strip().lower()
        if script_type in ("application/ld+json", "application/json+ld"):
            self._in_json_ld += 1
            self._ld_chunks = []
        src = _attr(attrs, "src")
        if src:
            self.script_bytes += len(src)

    def _close_script(self) -> None:
        if self._in_json_ld:
            self._in_json_ld -= 1
            self._finish_json_ld()
        if self._ignored:
            self._ignored -= 1

    def _finish_json_ld(self) -> None:
        raw = "".join(self._ld_chunks).strip()
        self._ld_chunks = []
        if not raw:
            return
        self.json_ld_blocks += 1
        try:
            data = json.loads(raw)
        except (ValueError, RecursionError):
            self.json_ld_malformed += 1
            return
        for value in extract_json_ld_types(data):
            if value not in self.json_ld_types:
                self.json_ld_types.append(value)

    def _finish_title(self) -> None:
        """A title element that was never seen leaves ``None``; an empty one leaves ``""``.

        The difference matters: "the page declares no title" and "the page declares an empty
        title" are different defects, and a report that collapses them tells the reader nothing
        about which one to fix.
        """
        if not self.seen_title_element:
            return
        if self.title is None:
            self.title = _collapse("".join(self._title_chunks))
        self._title_chunks = []


def looks_like_a_script_shell(
    visible_chars: int, script_bytes: int, script_blocks: int, app_root: bool
) -> bool:
    """Heuristic: is this page an application shell that JavaScript would fill in?

    True when there is almost no visible text *and* there is either a substantial amount of
    script or an empty application-root element. It is labelled a heuristic in the report
    because it is one: it can be wrong in both directions, and this tool executes nothing to
    find out.
    """
    if visible_chars >= SCRIPT_SHELL_TEXT_CHARS:
        return False
    if script_bytes >= SCRIPT_SHELL_SCRIPT_BYTES:
        return True
    return bool(app_root and (script_blocks or script_bytes))


def content_type_of(headers: dict[str, str], url: str) -> str:
    """The content type from the response, or inferred from the path when the server omits it."""
    content_type = (headers.get("content-type") or "").split(";")[0].strip().lower()
    if content_type:
        return content_type
    path = urlsplit(url).path.lower()
    if path.endswith((".html", ".htm")) or path.endswith("/"):
        return "text/html"
    if path.endswith(".xml"):
        return "application/xml"
    if path.endswith(".json"):
        return "application/json"
    if path.endswith(".txt"):
        return "text/plain"
    return ""


def facts_from(page: Page, in_sitemap: bool, note: str | None = None) -> PageFact:
    """Extract one page's facts from an already-fetched page.

    A non-HTML body is measured for length and reported for what it is. It has no title, no
    links and no JSON-LD, and saying so is more honest than reporting empty strings as though
    the page had failed to supply them.
    """
    content_type = page.content_type or content_type_of({}, page.url)
    fact = PageFact(
        url=page.url,
        status=page.status,
        content_type=content_type,
        in_sitemap=in_sitemap,
        truncated=page.truncated,
        error=page.error,
        note=note,
    )
    body = page.body
    if body is None:
        return fact
    if content_type and "html" not in content_type.lower():
        fact.visible_text_chars = len(_collapse(body))
        return fact
    collector = _HtmlCollector(page.url, origin_of(page.url))
    try:
        collector.feed(body)
        collector.close_document()
    except Exception as exc:  # a parser crash must not lose the rest of the run
        fact.note = "; ".join(filter(None, [fact.note, f"html parsing stopped: {exc}"]))
    fact.title = collector.title
    fact.description = collector.description
    fact.canonical = collector.canonical
    fact.canonical_host = (
        (urlsplit(collector.canonical).hostname or "").lower() if collector.canonical else None
    )
    fact.json_ld_types = tuple(collector.json_ld_types)
    fact.json_ld_blocks = collector.json_ld_blocks
    fact.json_ld_malformed = collector.json_ld_malformed
    fact.script_bytes = collector.script_bytes
    fact.script_blocks = collector.script_blocks
    fact.app_root = collector.app_root
    fact.visible_text_chars = collector.visible_chars
    fact.internal_targets = tuple(collector.internal_targets)
    fact.internal_links = len(collector.internal_targets)
    fact.external_links = collector.external_links
    fact.looks_script_rendered = looks_like_a_script_shell(
        collector.visible_chars, collector.script_bytes, collector.script_blocks, collector.app_root
    )
    if page.truncated:
        fact.note = "; ".join(
            filter(None, [fact.note, f"body read stopped at {MAX_BODY_CHARS} characters"])
        )
    return fact
