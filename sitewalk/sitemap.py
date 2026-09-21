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


@dataclass(frozen=True)
class Rule:
    """One ``Disallow`` rule, with the line it came from.

    ``pattern`` is the path prefix as matched. ``source_line`` is the line **exactly as it appears
    in ``robots.txt``** — leading whitespace, internal spacing and any trailing comment intact, and
    without its newline, because ``splitlines`` removes it and a quote carrying a terminator is not
    something a reader can select in a file.

    The source line is carried because the report quotes it: a reader takes the string out of the
    report, searches the file, and finds it. It is **not** the parser's ``line`` variable, which is
    ``raw.split("#", 1)[0].strip()``; on a line with a trailing comment the two differ, and quoting
    the stripped form silently drops the comment.
    """

    pattern: str
    source_line: str


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


def parse_robots(text: str) -> tuple[list[str], list[Rule]]:
    """Read ``robots.txt`` and return ``(sitemaps, disallow_rules)``.

    ``Disallow`` lines are honoured for the catch-all group and for our own name. The rules are
    matched as path prefixes, which is what the convention means in practice; ``Crawl-delay`` is
    ignored because it is not in the convention and ``--delay`` is explicit.
    """
    sitemaps: list[str] = []
    disallowed: list[Rule] = []
    applies = False
    for source_line in (text or "").splitlines():
        line = source_line.split("#", 1)[0].strip()
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
            if value and all(rule.pattern != value for rule in disallowed):
                disallowed.append(Rule(pattern=value, source_line=source_line))
    return sitemaps, disallowed


def is_disallowed(path: str, rules: Iterable[Rule]) -> Rule | None:
    """The rule that disallows this path, or None.

    Returns the rule rather than a bool so the report can quote the line that caused the skip. A
    caller that only needs the answer can test it for truth.
    """
    for rule in rules:
        if rule.pattern == "/" or path.startswith(rule.pattern):
            return rule
    return None
