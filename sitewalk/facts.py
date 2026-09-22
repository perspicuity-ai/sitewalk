"""The models every other module passes around.

They are dataclasses with no behaviour so that the crawl, the plan check, the findings and the
report can each be tested against a page that was never fetched.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

#: Finding severities. The report states what is true; the gate decides what is tolerable
#: (docs/DESIGN.md, D10). ``--strict`` maps these to exit codes and never creates a finding.
#:
#: * ``error`` — something is wrong with the site as built.
#: * ``conditional`` — the verdict depends on something this consumer does not know, so the result
#:   is not a clean one. An unknown or newer plan version, an absent or mistyped one, or a required
#:   surface this tool has no check for. Disclosed in every run; gates under ``--strict``.
#: * ``info`` — an observation or a site's own choice, with nothing left unknown. Never gates.
ERROR = "error"
CONDITIONAL = "conditional"
INFO = "info"

#: Which severities ``--strict`` turns into a non-zero exit. A policy table rather than a
#: condition buried in the exit path, so a reader can see the policy without reading the code.
GATING_SEVERITIES = (ERROR, CONDITIONAL)

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


#: The four states a surface can be in. They are distinct because a reader must be able to tell
#: "we looked and it is not there" from "we cannot look":
#:
#: * ``present``     — fetched, 2xx. The site publishes it.
#: * ``absent``      — fetched, non-2xx. The site does not publish it.
#: * ``derived``     — not fetched and nothing to fetch; established from pages already read, as
#:                     ``json-ld`` is. Reporting this with an empty URL and status would read as
#:                     "we fetched it and learned nothing", which is a different and worse claim.
#: * ``not_checked`` — this consumer has no check for it. A gap here, never a finding about the
#:   site.
#:
#: **``not_checked`` is load-bearing and currently unreachable. Do not delete it.** No live path
#: assigns it today, because every surface in the format's vocabulary is checked. It exists for the
#: case where one is not, so that such a surface is reported *unverified* rather than *absent* —
#: the overclaim U7 and U8 were built to remove ("the plan requires rss.xml, which the site does not
#: publish", about a file nothing ever looked for).
#:
#: What would make it reachable again: a sixth value added to the format's ``required_surfaces``
#: (see ``KNOWN_SURFACES`` in ``plan.py``), or a surface dropping out of ``CHECKED_SURFACES``.
#: Which fires first: the tripwire test ``tests/test_plan.py::
#: EveryVocabularySurfaceHasACheck.test_every_vocabulary_surface_is_checked_now`` fails the moment
#: the two sets differ, so a developer meets the gap at build time and is told what to do. This
#: state is what keeps the report honest if the gap ships anyway.
#:
#: A reader running a dead-code audit will find no live assignment here and may reasonably want to
#: remove it. That is the wrong call, and
#: ``tests/test_plan.py::ANotCheckedSurfaceIsStillHandled`` fails if the state or its handling
#: goes.
PRESENT = "present"
ABSENT = "absent"
DERIVED = "derived"
NOT_CHECKED = "not_checked"


@dataclass
class Surface:
    """A machine-readable surface a plan may require, and what this run knows about it.

    ``state`` is the discriminator a machine reads; ``exists`` is derived from it so the two can
    never disagree. ``url`` and ``status`` are meaningful only for the fetched states, and a
    ``derived`` surface carries a ``note`` saying what it was derived from.
    """

    name: str
    state: str = NOT_CHECKED
    url: str = ""
    status: int = 0
    content_type: str = ""
    bytes: int = 0
    error: str | None = None
    note: str | None = None
    #: For a ``derived`` surface only: whether the fact it is derived from was actually found.
    #: Without it, "derived" would have to mean "exists", and every site would appear to publish
    #: JSON-LD — the same overclaim the states exist to prevent.
    established: bool = False
    #: For a ``derived`` surface only: the pages the fact was found on, or the pages read when it
    #: was not. The format requires a consumer checking ``json-ld`` to name the page it found the
    #: markup on: "json-ld: met" without the page is the same class of claim as a verdict on a
    #: version the consumer does not know.
    pages: tuple[str, ...] = ()

    @property
    def exists(self) -> bool:
        if self.state == PRESENT:
            return True
        if self.state == DERIVED:
            return self.established
        return False


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
    def conditionals(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == CONDITIONAL]

    @property
    def gating(self) -> list[Finding]:
        """Every finding ``--strict`` refuses to accept: errors and conditionals."""
        return [f for f in self.findings if f.severity in GATING_SEVERITIES]

    @property
    def infos(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == INFO]

    def errors_of(self, kind: str) -> list[Finding]:
        return [f for f in self.findings if f.kind == kind and f.severity == ERROR]
