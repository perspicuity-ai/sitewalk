"""Site-wide findings: what the collected facts mean about the site as a whole.

Every finding here is derived from something the tool read, and each one names its subject so a
reader can go and look. Nothing here predicts ranking, citations, traffic or whether any agent
will recommend the site; these are observations about the output a server returned.

Severities follow D10: an ``error`` is something that is wrong with the site as built and gates
under ``--strict``; an ``info`` is a note about a choice the site made, and does not gate,
because a gate that fails on choices gets switched off.
"""

from __future__ import annotations

from collections import Counter
from typing import Iterable

from .crawl import CrawlResult
from .facts import ERROR, INFO, Finding, PageFact, SiteReport
from .pages import SCRIPT_SHELL_TEXT_CHARS
from .urls import origin_of, relative_path

REPORT_VERSION = 1
FACTS_VERSION = 1

#: Kinds that are reported as information rather than as defects. A note describes a choice the
#: site made, or an observation this tool cannot act on, and it does not gate: a gate that fails
#: on choices gets switched off. ``canonical_other_path`` is here because a canonical pointing at
#: another URL on the same host is usually a deliberate consolidation, and a build that declares
#: one per page is not defective.
_INFO_KINDS = frozenset(
    {
        "script_rendered",
        "surface_missing",
        "canonical_missing",
        "canonical_other_path",
        "missing_description",
    }
)

_MAX_NAMED = 10


def _named(items: Iterable[str]) -> str:
    """A comma-separated list, shortened so a finding stays readable in a terminal."""
    listed = list(items)
    if len(listed) <= _MAX_NAMED:
        return ", ".join(listed)
    return ", ".join(listed[:_MAX_NAMED]) + f", and {len(listed) - _MAX_NAMED} more"


def _add(report: SiteReport, kind: str, message: str, subject: str | None = None) -> None:
    severity = INFO if kind in _INFO_KINDS else ERROR
    report.findings.append(
        Finding(kind=kind, severity=severity, message=message, subject=subject)
    )


def status_counts(pages: Iterable[PageFact]) -> dict[str, int]:
    """``{"200": 4, "404": 1}`` — the distribution, as strings so JSON keys stay JSON keys."""
    counts: Counter[str] = Counter()
    for fact in pages:
        if fact.error and not fact.status:
            counts["no response"] += 1
        else:
            counts[str(fact.status)] += 1
    return dict(sorted(counts.items()))


def analyse(result: CrawlResult) -> SiteReport:
    """Turn a crawl into the report: facts, findings, and the notes that qualify them."""
    report = SiteReport(
        report_version=REPORT_VERSION,
        facts_version=FACTS_VERSION,
        source=result.source_label,
        source_kind=result.source_kind,
        target=result.target,
        origin=result.origin,
        started_at=result.started_at,
        finished_at=result.finished_at,
        pages=list(result.pages),
        surfaces=dict(result.surfaces),
        status_counts=status_counts(result.pages),
        user_agent=result.user_agent,
    )
    report.notes.extend(result.notes)

    # Only pages that answered 2xx are asked about their titles, descriptions, canonicals and
    # structured data. A page that returned 404 has none of those, and listing it six times
    # would bury the finding that actually matters — that it did not answer.
    pages = [f for f in result.pages if f.is_html and f.ok]
    unread = [f for f in result.pages if f.is_html and not f.ok]
    by_url = {fact.url: fact for fact in result.pages}
    home = next((f for f in pages if relative_path(f.url) == "/"), None)

    # -- status distribution -----------------------------------------------------------------
    failures = [f for f in result.pages if not f.ok]
    if failures:
        _add(
            report,
            "page_not_ok",
            f"{len(failures)} fetched URL(s) did not return 2xx: "
            + _named(f"{relative_path(f.url)} ({f.status or f.error})" for f in failures),
        )
    if unread:
        report.notes.append(
            f"{len(unread)} HTML URL(s) did not answer 2xx, so their title, description, "
            "canonical and structured data are unknown rather than absent: "
            + _named(relative_path(f.url) for f in unread)
        )

    # -- sitemap coverage --------------------------------------------------------------------
    reached = set(by_url)
    never_reached = [url for url in result.sitemap_urls if url not in reached]
    report.sitemap_named = list(result.sitemap_urls)
    report.sitemap_unreached = list(never_reached)
    if never_reached:
        _add(
            report,
            "sitemap_url_not_reached",
            f"{len(never_reached)} URL(s) named in the sitemap were never reached: "
            + _named(relative_path(u) for u in never_reached),
        )
    for message in result.sitemap_errors:
        _add(report, "sitemap_unreadable", message)

    # -- orphans -----------------------------------------------------------------------------
    # A page is an orphan when nothing crawled links to it. The home page is linked from
    # nowhere by definition, so it is never an orphan, and a URL that never answered is a
    # reachability problem rather than an orphan page.
    linked: set[str] = set()
    for fact in result.pages:
        linked.update(fact.internal_targets)
    orphans = [
        f.url
        for f in result.pages
        if f.in_sitemap and f.ok and f.url not in linked and (home is None or f.url != home.url)
    ]
    if orphans:
        _add(
            report,
            "orphan_page",
            f"{len(orphans)} page(s) are named in the sitemap and linked from nowhere crawled: "
            + _named(relative_path(u) for u in orphans),
        )

    # -- titles and descriptions -------------------------------------------------------------
    titled = Counter(f.title for f in pages)
    duplicates = sorted(title for title, count in titled.items() if title and count > 1)
    if duplicates:
        for title in duplicates:
            urls = [f.url for f in pages if f.title == title]
            _add(
                report,
                "duplicate_title",
                f"{len(urls)} pages share the title {title!r}: "
                + _named(relative_path(u) for u in urls),
                subject=title,
            )

    missing_titles = [f.url for f in pages if f.title is None]
    if missing_titles:
        _add(
            report,
            "missing_title",
            f"{len(missing_titles)} HTML page(s) have no <title> element: "
            + _named(relative_path(u) for u in missing_titles),
        )
    empty_titles = [f.url for f in pages if f.title == ""]
    if empty_titles:
        _add(
            report,
            "empty_title",
            f"{len(empty_titles)} page(s) have an empty <title>: "
            + _named(relative_path(u) for u in empty_titles),
        )

    described = Counter(f.description for f in pages if f.description is not None)
    duplicate_descriptions = sorted(d for d, count in described.items() if count > 1)
    for description in duplicate_descriptions:
        urls = [f.url for f in pages if f.description == description]
        _add(
            report,
            "duplicate_description",
            f"{len(urls)} pages share a meta description: {_named(relative_path(u) for u in urls)}",
            subject=description,
        )
    missing_descriptions = [f.url for f in pages if f.description is None]
    if missing_descriptions:
        _add(
            report,
            "missing_description",
            f"{len(missing_descriptions)} HTML page(s) have no meta description: "
            + _named(relative_path(u) for u in missing_descriptions),
        )

    # -- canonicals --------------------------------------------------------------------------
    own_host = (origin_of(result.origin) or "").split("://")[-1].split(":")[0]
    cross_host = [
        f.url
        for f in pages
        if f.canonical_host and f.canonical_host not in (own_host, "")
    ]
    if cross_host:
        _add(
            report,
            "canonical_other_host",
            f"{len(cross_host)} page(s) declare a canonical on another host: "
            + _named(f"{relative_path(u)} -> {by_url[u].canonical}" for u in cross_host),
        )
    no_canonical = [f.url for f in pages if f.canonical is None]
    if no_canonical:
        _add(
            report,
            "canonical_missing",
            f"{len(no_canonical)} HTML page(s) declare no canonical: "
            + _named(relative_path(u) for u in no_canonical),
        )
    self_canonical = [
        f.url
        for f in pages
        if f.canonical and f.canonical != f.url and f.url not in cross_host
    ]
    if self_canonical:
        _add(
            report,
            "canonical_other_path",
            f"{len(self_canonical)} page(s) declare a canonical at a different path on this "
            "host, which consolidates them onto that URL: "
            + _named(f"{relative_path(u)} -> {by_url[u].canonical}" for u in self_canonical),
        )

    # -- structured data ---------------------------------------------------------------------
    without_ld = [f.url for f in pages if not f.json_ld_types]
    if without_ld:
        _add(
            report,
            "no_json_ld",
            f"{len(without_ld)} HTML page(s) carry no JSON-LD @type: "
            + _named(relative_path(u) for u in without_ld),
        )
    malformed = [f for f in pages if f.json_ld_malformed]
    if malformed:
        _add(
            report,
            "malformed_json_ld",
            f"{len(malformed)} page(s) contain a JSON-LD block that does not parse: "
            + _named(relative_path(f.url) for f in malformed),
        )
    report.json_ld_type_counts = dict(
        sorted(Counter(t for f in pages for t in f.json_ld_types).items())
    )

    # -- internal links that do not answer 200 -----------------------------------------------
    broken: list[tuple[str, str, int]] = []
    for fact in pages:
        for link in fact.internal_targets:
            target = by_url.get(link)
            if target is not None and not target.ok:
                broken.append((fact.url, link, target.status))
    seen_broken: set[tuple[str, str]] = set()
    for source_url, link, status in broken:
        if (source_url, link) in seen_broken:
            continue
        seen_broken.add((source_url, link))
        _add(
            report,
            "broken_internal_link",
            f"{relative_path(source_url)} links to {relative_path(link)}, which returned {status}",
            subject=link,
        )
    unverified = [
        link
        for fact in pages
        for link in fact.internal_targets
        if link not in by_url and not link.startswith("mailto:")
    ]
    if unverified:
        _add(
            report,
            "internal_link_not_checked",
            f"{len(unverified)} internal link target(s) were not checked within the bounds: "
            + _named(relative_path(u) for u in dict.fromkeys(unverified)),
        )

    # -- surfaces ----------------------------------------------------------------------------
    for name, surface in sorted(result.surfaces.items()):
        if surface.exists:
            continue
        message = f"{name} was not found ({surface.status or surface.error or 'no response'})"
        if name == "llms.txt":
            # Non-gating by the principal's decision of 2026-09-21 (RECORD.md, Q5). The basis is
            # judgement, and it is cited so a reader can discount it: a file almost nobody
            # fetches is not a reason to fail someone's build.
            message += (
                " — reported as a note, not a defect: llms.txt is a site's own choice, and"
                " Ahrefs measured that 97% of llms.txt files received no requests across"
                " 137,000 sites (ahrefs.com/blog/llmstxt-study/). It does not gate."
            )
        _add(report, "surface_missing", message, subject=name)

    # -- the no-JavaScript boundary ----------------------------------------------------------
    shell_pages = [f for f in pages if f.looks_script_rendered]
    if shell_pages:
        _add(
            report,
            "script_rendered",
            f"{len(shell_pages)} page(s) look script-rendered: under {SCRIPT_SHELL_TEXT_CHARS} "
            "characters of visible text with substantial script. This tool does not execute "
            "JavaScript, so it cannot see what a browser would render; the visible-text length "
            "is not evidence that the page is empty. Pages: "
            + _named(relative_path(f.url) for f in shell_pages),
        )
    if result.truncated_pages:
        _add(
            report,
            "body_truncated",
            f"{result.truncated_pages} page(s) were longer than the body cap and were read in part",
        )

    if result.refused:
        report.notes.append(
            f"{len(result.refused)} request(s) were refused by the address guard: "
            + _named(result.refused)
        )
    for skip in result.skipped:
        line = f"not fetched: {relative_path(skip.url)} — {skip.reason}"
        if skip.rule:
            # Quoted verbatim, so a reader can search robots.txt for it and find it.
            line += f" (robots.txt: {skip.rule})"
        report.notes.append(line)
    report.skipped_robots = [s for s in result.skipped if s.rule]

    report.limits = {
        # Stated here as well as in the notes, so a reader who reads only the summary cannot
        # reach the end of the report without learning that something was excluded.
        "paths_skipped_robots": len(report.skipped_robots),
        "requests_made": result.requests_made,
        "pages_read": len(result.pages),
        "link_checks_made": result.link_checked,
        "page_cap_reached": result.cap_reached,
    }
    return report
