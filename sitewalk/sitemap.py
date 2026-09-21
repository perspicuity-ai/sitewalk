"""``sitemap.xml`` reading: the URLs it names, and the sitemaps it points at.

Only a sitemap's URLs are read from it. Priorities, change frequencies and last-modified dates
are not part of this product's promises, and a sitemap that is unreadable is reported as a
finding rather than silently contributing no URLs.
"""

from __future__ import annotations

import xml.etree.ElementTree as ElementTree
from dataclasses import dataclass, field
from typing import Iterable

#: Nested sitemap indexes are followed to this depth. A site that chains deeper than this is
#: unusual enough that following it further is not worth the requests.
MAX_SITEMAP_DEPTH = 5


@dataclass
class SitemapResult:
    """What one sitemap (and the indexes under it) named."""

    urls: list[str] = field(default_factory=list)
    nested: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def _tag_name(element: ElementTree.Element) -> str:
    return element.tag.rsplit("}", 1)[-1].lower()


def parse_sitemap(text: str) -> SitemapResult:
    """Read a ``urlset`` or a ``sitemapindex``.

    Handles a document with no namespace, with the sitemaps.org namespace, and with any other
    namespace, because the namespace is decoration and the element names are the content.
    """
    result = SitemapResult()
    stripped = (text or "").strip()
    if not stripped:
        result.errors.append("the sitemap was empty")
        return result
    try:
        root = ElementTree.fromstring(stripped)
    except ElementTree.ParseError as exc:
        result.errors.append(f"the sitemap did not parse as XML: {exc}")
        return result
    kind = _tag_name(root)
    for element in root:
        name = _tag_name(element)
        if name not in ("url", "sitemap"):
            continue
        loc = None
        for child in element:
            if _tag_name(child) == "loc":
                loc = (child.text or "").strip()
                break
        if not loc:
            continue
        if name == "sitemap":
            if loc not in result.nested:
                result.nested.append(loc)
        elif name == "url":
            if loc not in result.urls:
                result.urls.append(loc)
    if kind not in ("urlset", "sitemapindex"):
        result.errors.append(f"the document root was <{kind}>, not <urlset> or <sitemapindex>")
    return result


def parse_robots(text: str) -> tuple[list[str], list[str]]:
    """Read ``robots.txt`` and return ``(sitemaps, disallowed_paths)``.

    ``Disallow`` lines are honoured for the catch-all group and for our own name. The rules are
    matched as path prefixes, which is what the convention means in practice; ``Crawl-delay`` is
    ignored because it is not in the convention and ``--delay`` is explicit.
    """
    sitemaps: list[str] = []
    disallowed: list[str] = []
    applies = False
    for raw_line in (text or "").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        field, value = line.split(":", 1)
        field = field.strip().lower()
        value = value.strip()
        if field == "sitemap":
            if value and value not in sitemaps:
                sitemaps.append(value)
        elif field == "user-agent":
            agent = value.lower()
            applies = agent in ("*", "sitewalk")
        elif field == "disallow" and applies:
            if value and value not in disallowed:
                disallowed.append(value)
    return sitemaps, disallowed


def is_disallowed(path: str, disallowed: Iterable[str]) -> bool:
    """True when a path prefix in ``robots.txt`` covers this path."""
    for rule in disallowed:
        if rule == "/":
            return True
        if path.startswith(rule):
            return True
    return False
