"""The report: a readable one on stdout, and the same facts as JSON for a machine.

The text report states its own boundary in full, at the top, every time. That is not decoration:
the failures this tool is meant to avoid are implied claims, and the cheapest way to avoid them
is to say what was and was not observed before showing any numbers.

Nothing here ranks, scores or judges a site. There is no aggregate grade, and there is
deliberately no such thing anywhere in the package.
"""

from __future__ import annotations

import json
from typing import Any

from .facts import ERROR, SiteReport
from .urls import relative_path

BOUNDARY = (
    "sitewalk reports what is observable in the output the server returns. It reads HTML and "
    "does not execute JavaScript, so it cannot see anything a browser would render after load; "
    "a short visible-text length is not evidence that a page is empty. It does not predict "
    "whether an agent will find, trust or recommend a site, and it measures no ranking, "
    "citation or traffic."
)


def _flag(fact) -> str:
    flags = []
    if fact.looks_script_rendered:
        flags.append("script-shell?")
    if fact.note:
        flags.append("note")
    if fact.truncated:
        flags.append("truncated")
    return ",".join(flags) or "-"


def to_dict(report: SiteReport) -> dict[str, Any]:
    """The machine-readable shape. Keys are stable; new keys are added, never renamed."""
    return {
        "tool": "sitewalk",
        "report_version": report.report_version,
        "facts_version": report.facts_version,
        "source": {
            "kind": report.source_kind,
            "target": report.target,
            "origin": report.origin,
        },
        # Which client made the requests, so a site owner reading this can find it in their logs.
        "user_agent": report.user_agent or None,
        "started_at": report.started_at,
        "finished_at": report.finished_at,
        "claim_boundary": BOUNDARY,
        "not_measured": [
            "ranking",
            "citations",
            "traffic",
            "whether an agent will find, trust or recommend the site",
            "anything rendered by JavaScript after load",
        ],
        "limits": report.limits,
        "status_counts": report.status_counts,
        "json_ld_type_counts": report.json_ld_type_counts,
        "sitemap": {
            "urls_named": len(report.sitemap_named),
            "urls": list(report.sitemap_named),
            "never_reached": list(report.sitemap_unreached),
        },
        "surfaces": {
            name: {
                "url": surface.url,
                "exists": surface.exists,
                "status": surface.status,
                "content_type": surface.content_type,
                "bytes": surface.bytes,
                "error": surface.error,
            }
            for name, surface in sorted(report.surfaces.items())
        },
        "pages": [
            {
                "url": fact.url,
                "path": relative_path(fact.url),
                "status": fact.status,
                "content_type": fact.content_type,
                "title": fact.title,
                "meta_description": fact.description,
                "canonical": fact.canonical,
                "json_ld_types": list(fact.json_ld_types),
                "json_ld_blocks": fact.json_ld_blocks,
                "json_ld_malformed": fact.json_ld_malformed,
                "visible_text_chars": fact.visible_text_chars,
                "internal_links": fact.internal_links,
                "external_links": fact.external_links,
                "in_sitemap": fact.in_sitemap,
                "looks_script_rendered": fact.looks_script_rendered,
                # The heuristic's own inputs, so a reader can check the label rather than
                # trust it. See the script_rendered finding for what it does and does not mean.
                "script_shell_evidence": {
                    "script_bytes": fact.script_bytes,
                    "script_blocks": fact.script_blocks,
                    "app_root_element": fact.app_root,
                },
                "truncated": fact.truncated,
                "redirect_to": fact.redirect_to,
                "error": fact.error,
                "note": fact.note,
            }
            for fact in report.pages
        ],
        "findings": [
            {
                "kind": finding.kind,
                "severity": finding.severity,
                "message": finding.message,
                "subject": finding.subject,
            }
            for finding in report.findings
        ],
        "finding_counts": {
            "error": len(report.errors),
            "info": len(report.infos),
        },
        "plan": report.plan,
        "notes": report.notes,
    }


def to_json(report: SiteReport, indent: int | None = 2) -> str:
    return json.dumps(to_dict(report), indent=indent, sort_keys=False, ensure_ascii=False)


def _rule(title: str) -> str:
    return f"\n== {title} " + "=" * max(0, 72 - len(title))


def to_text(report: SiteReport) -> str:
    lines: list[str] = []
    lines.append(f"sitewalk {report.report_version} — structural map")
    lines.append(f"source: {report.source_kind} {report.source}")
    if report.user_agent:
        lines.append(f"user agent: {report.user_agent}")
    lines.append(f"target: {report.target}")
    lines.append(f"read: {report.started_at} to {report.finished_at}")
    limits = report.limits or {}
    lines.append(
        "bounded by: "
        f"{limits.get('pages_read', len(report.pages))} pages read, "
        f"{limits.get('requests_made', 0)} requests, "
        f"{limits.get('link_checks_made', 0)} link checks"
        + (", page cap reached" if limits.get("page_cap_reached") else "")
    )
    lines.append("")
    lines.append("claim boundary: " + BOUNDARY)
    lines.append(
        "not measured here: ranking, citations, traffic, whether any agent will recommend the "
        "site."
    )

    lines.append(_rule("Pages"))
    lines.append(
        f"{'path':<28} {'st':>3} {'ctype':<16} {'title':<24} {'desc':>4} {'canon':<12} "
        f"{'json-ld':<22} {'text':>6} {'in':>3} {'out':>3} {'sm':>2} flags"
    )
    lines.append(
        "  title: '-' absent, '0' present but empty. desc: meta description length, '-' absent."
    )
    for fact in report.pages:
        paths = relative_path(fact.url)
        title = "-" if fact.title is None else (fact.title or "0")
        desc = "-" if fact.description is None else str(len(fact.description))
        canonical = "-"
        if fact.canonical:
            canonical = "self" if fact.canonical == fact.url else (
                "other-host" if fact.canonical_host and fact.canonical_host not in report.origin else "other-url"
            )
        json_ld = ",".join(fact.json_ld_types) or "-"
        lines.append(
            f"{paths[:28]:<28} {fact.status:>3} {(fact.content_type or '-')[:16]:<16} "
            f"{title[:24]:<24} {desc:>4} {canonical:<12} {json_ld[:22]:<22} "
            f"{fact.visible_text_chars:>6} {fact.internal_links:>3} {fact.external_links:>3} "
            f"{'y' if fact.in_sitemap else '-':>2} {_flag(fact)}"
        )
        if fact.error:
            lines.append(f"{'':<28} error: {fact.error}")
        if fact.note:
            lines.append(f"{'':<28} note: {fact.note}")

    lines.append(_rule("Status distribution"))
    for status, count in sorted(report.status_counts.items()):
        lines.append(f"  {status:<12} {count}")

    lines.append(_rule("Surfaces"))
    for name, surface in sorted(report.surfaces.items()):
        state = "present" if surface.exists else "missing"
        detail = f"status {surface.status}" if surface.status else (surface.error or "no response")
        lines.append(f"  {name:<12} {state:<8} {detail}")

    if report.json_ld_type_counts:
        lines.append(_rule("JSON-LD types across the site"))
        for type_name, count in report.json_ld_type_counts.items():
            lines.append(f"  {type_name:<32} {count}")

    sitemap_named = sum(1 for fact in report.pages if fact.in_sitemap)
    lines.append(_rule("Sitemap coverage"))
    lines.append(f"  URLs the sitemap names:                 {len(report.sitemap_named)}")
    lines.append(f"  pages reached that the sitemap names:   {sitemap_named}")
    lines.append(f"  pages reached that it does not name:    {len(report.pages) - sitemap_named}")
    lines.append(f"  sitemap URLs never reached:             {len(report.sitemap_unreached)}")

    errors = report.errors
    infos = report.infos
    lines.append(_rule(f"Findings ({len(errors)} error, {len(infos)} note)"))
    if not errors and not infos:
        lines.append("  none")
    for label, group in (("ERROR", errors), ("NOTE", infos)):
        for finding in group:
            lines.append(f"  [{label}] {finding.kind}: {finding.message}")

    if report.plan:
        lines.append(_rule("Plan"))
        plan = report.plan
        lines.append(f"  {plan.get('path') or '(no path)'} — plan_version {plan.get('plan_version')}")
        lines.append(f"  result: {'met' if plan.get('passed') else 'not met'}")

    if report.notes:
        lines.append(_rule("Notes"))
        for note in report.notes:
            lines.append(f"  - {note}")

    lines.append(_rule("Exit"))
    if report.errors:
        lines.append(
            f"  {len(report.errors)} error-severity finding(s). Under --strict the exit status is 1."
        )
    else:
        lines.append("  no error-severity findings.")
    return "\n".join(lines)


def summary_line(report: SiteReport) -> str:
    """One line for a CI log: what was read, what was found, and what gated."""
    return (
        f"sitewalk: {len(report.pages)} page(s), "
        f"{len(report.errors)} error(s), {len(report.infos)} note(s) — "
        + ("FAIL" if report.errors else "ok")
    )


def exit_code(report: SiteReport, strict: bool) -> int:
    """0 normally; 1 under ``--strict`` when an error-severity finding exists."""
    if strict and report.errors:
        return 1
    return 0


__all__ = ["BOUNDARY", "to_dict", "to_json", "to_text", "summary_line", "exit_code", "ERROR"]
