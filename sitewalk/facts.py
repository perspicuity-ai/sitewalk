"""The models every other module passes around.

They are dataclasses with no behaviour so that the crawl, the plan check, the findings and the
report can each be tested against a page that was never fetched.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

#: Finding severities. Only ``error`` gates under ``--strict``; ``info`` is a note that is
#: reported and does not fail a build, because it describes a design choice of the site rather
#: than a change under test. See D10 in docs/DESIGN.md.
ERROR = "error"
INFO = "info"

#: Bodies above this many characters are not kept. Nothing downstream needs the bytes, only the
#: facts extracted from them, and a crawl should not hold a site in memory.
MAX_BODY_CHARS = 200_000


@dataclass
class Page:
    """One fetched document, from either source.

    ``body`` is ``None`` when the response had no useful body (an error status, a redirect, or a
    body over the source's cap); ``truncated`` says the cap was reached rather than the response
    being empty.
    """

    url: str
    status: int
    content_type: str = ""
    body: str | None = None
    error: str | None = None
    truncated: bool = False
    #: A note about how the body was obtained, such as a query string that is not a filename.
    note: str | None = None
    #: Where a redirect pointed, when one was followed. ``url`` stays the URL that was asked for.
    redirect_to: str | None = None

    @property
    def ok(self) -> bool:
        return 200 <= self.status < 300


@dataclass
class PageFact:
    """What one page exposes to a machine that does not execute JavaScript."""

    url: str
    status: int
    content_type: str
    title: str | None = None
    description: str | None = None
    canonical: str | None = None
    canonical_host: str | None = None
    json_ld_types: tuple[str, ...] = ()
    json_ld_blocks: int = 0
    json_ld_malformed: int = 0
    visible_text_chars: int = 0
    internal_links: int = 0
    external_links: int = 0
    internal_targets: tuple[str, ...] = ()
    in_sitemap: bool = False
    looks_script_rendered: bool = False
    script_bytes: int = 0
    script_blocks: int = 0
    app_root: bool = False
    truncated: bool = False
    error: str | None = None
    redirect_to: str | None = None
    note: str | None = None

    @property
    def is_html(self) -> bool:
        return "html" in (self.content_type or "").lower()

    @property
    def ok(self) -> bool:
        return 200 <= self.status < 300


@dataclass
class Surface:
    """An optional machine-readable file at the site root, and whether it exists."""

    name: str
    url: str
    exists: bool = False
    status: int = 0
    content_type: str = ""
    bytes: int = 0
    error: str | None = None


@dataclass
class Skip:
    """A URL that was not fetched, and why.

    ``rule`` is the ``robots.txt`` line that caused the skip when one did, carried verbatim so the
    report can quote what disallowed the path rather than only saying that something did. It is
    ``None`` for a skip with another cause.
    """

    url: str
    reason: str
    rule: str | None = None


@dataclass
class Finding:
    """One site-wide observation. ``subject`` names the page or URL it is about."""

    kind: str
    severity: str
    message: str
    subject: str | None = None


@dataclass
class SiteReport:
    """Everything one run observed, ready to be printed as text or as JSON."""

    report_version: int
    source: str
    source_kind: str
    target: str
    origin: str
    started_at: str
    finished_at: str = ""
    user_agent: str = ""
    facts_version: int = 1
    pages: list[PageFact] = field(default_factory=list)
    surfaces: dict[str, Surface] = field(default_factory=dict)
    findings: list[Finding] = field(default_factory=list)
    status_counts: dict[str, int] = field(default_factory=dict)
    json_ld_type_counts: dict[str, int] = field(default_factory=dict)
    sitemap_named: list[str] = field(default_factory=list)
    sitemap_unreached: list[str] = field(default_factory=list)
    skipped_robots: list[Skip] = field(default_factory=list)
    limits: dict[str, Any] = field(default_factory=dict)
    plan: dict[str, Any] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == ERROR]

    @property
    def infos(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == INFO]

    def errors_of(self, kind: str) -> list[Finding]:
        return [f for f in self.findings if f.kind == kind and f.severity == ERROR]
