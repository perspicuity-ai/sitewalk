"""``--plan site.json``: check a built site against the plan it claims to follow.

The plan format is owned by the ``siteplan`` project, which is authoritative; this module is the
consumer side and links there rather than restating the format. Two things are **enforced**,
because they are the two the site is meant to be built from and this tool can observe both:

* ``required_surfaces`` — the machine-readable files the site must publish;
* ``identity.schema_types`` — the Schema.org entity types the home page must carry in JSON-LD.

Everything else in the file is read, reported as *not checked* with the reason, and otherwise
ignored. A key this tool does not understand is ignored rather than fatal, because the format is
expected to grow and a consumer that fails on growth forces lockstep releases between two
deliberately independent projects.

A plan that cannot be read at all is an error with a non-zero exit: a gate that cannot read its
own plan must not report a pass.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .facts import SiteReport
from .urls import relative_path

#: Keys the format defines at the top level, and whether this consumer enforces them.
KNOWN_KEYS: dict[str, str] = {
    "plan_version": "read and reported; a version this consumer does not know is a note",
    "site": "read and reported",
    "kind": "read and reported",
    "required_surfaces": "enforced against the surfaces found",
    "identity": "enforced: identity.schema_types against the home page's JSON-LD",
    "offering": "not checked: offering.fields names Schema.org properties this tool does not extract",
    "url_rules": "not checked: url shape is observable but is not what this gate was asked to hold",
    "crawler_stance": "not checked: robots.txt is read and obeyed, but a stance is not observable from pages",
    "pages": "not checked: every page the crawl found is already reported",
}

#: The plan version this consumer was written against.
SUPPORTED_PLAN_VERSION = 1


@dataclass
class PlanCheck:
    """The outcome of checking a site against a plan."""

    path: str
    version: Any = None
    site: str | None = None
    kind: str | None = None
    problems: list[str] = field(default_factory=list)
    unmet_surfaces: list[str] = field(default_factory=list)
    missing_schema_types: list[str] = field(default_factory=list)
    home_json_ld_types: list[str] = field(default_factory=list)
    planned: bool = False
    notes: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.planned and not self.problems and not self.unmet_surfaces and not self.missing_schema_types


def load_plan(path: str | Path) -> dict[str, Any]:
    """Read a plan file. Raises ``ValueError`` with a readable message when it cannot be used."""
    plan_path = Path(path)
    try:
        text = plan_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"could not read the plan file {plan_path}: {exc}") from exc
    try:
        data = json.loads(text)
    except ValueError as exc:
        raise ValueError(f"the plan file {plan_path} is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"the plan file {plan_path} must contain a JSON object")
    return data


def _as_list(value: Any, allow_single_string: bool = False) -> list[str] | None:
    """Return a list of non-empty strings, or None when the value is not one.

    ``allow_single_string`` is off by default and turned on only where a bare string is
    unambiguous. Leniency about this belongs in the producer, which knows what it meant when it
    wrote the file; a consumer that quietly coerces a malformed value into a plausible one
    reports a plan as met when the plan was never well formed. That is the same class of error as
    reporting a check that was never performed.
    """
    if isinstance(value, str):
        if not allow_single_string:
            return None
        return [value] if value else []
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            if isinstance(item, str):
                if item:
                    out.append(item)
            elif item is not None:
                return None
        return out
    return None


def check_plan(report: SiteReport, plan: dict[str, Any], path: str = "") -> PlanCheck:
    """Compare a crawled site against a plan, enforcing the two observable keys."""
    check = PlanCheck(path=str(path), planned=True)
    check.version = plan.get("plan_version")
    site = plan.get("site")
    check.site = site if isinstance(site, str) else None
    kind = plan.get("kind")
    check.kind = kind if isinstance(kind, str) else None

    if check.version is None:
        # Not a failure. siteplan has not confirmed the key is required, and a consumer that
        # rejects a plan for missing a version rejects plans it could have checked.
        check.notes.append(
            "the plan names no plan_version; it was read anyway and the keys this consumer "
            "knows were checked"
        )
    elif check.version != SUPPORTED_PLAN_VERSION:
        # Any version is accepted, by the principal's decision of 2026-09-21 (RECORD.md, Q3): a
        # consumer that rejects an unfamiliar version or key breaks the producer every time the
        # format grows. What it must do instead is say what it did and did not enforce.
        check.notes.append(
            f"the plan declares plan_version {check.version!r} and this consumer was written "
            f"against version {SUPPORTED_PLAN_VERSION}. The plan was read, not rejected: the "
            "keys this consumer knows were checked and anything it does not recognise was "
            "ignored, so a met result here does not mean the whole plan was verified"
        )

    required = plan.get("required_surfaces")
    if required is not None:
        # A single surface name as a bare string is accepted here: the meaning is unambiguous,
        # and "is a list" is the kind of strictness that costs a producer a release for nothing.
        names = _as_list(required, allow_single_string=True)
        if names is None:
            check.problems.append("required_surfaces is not a list of strings")
        else:
            for name in names:
                surface = report.surfaces.get(name)
                if surface is None or not surface.exists:
                    check.unmet_surfaces.append(name)

    identity = plan.get("identity")
    if identity is not None:
        if not isinstance(identity, dict):
            check.problems.append("identity is not an object")
        else:
            wanted = identity.get("schema_types")
            if wanted is not None:
                types = _as_list(wanted)
                if types is None:
                    check.problems.append("identity.schema_types is not a list of strings")
                else:
                    home = next(
                        (f for f in report.pages if relative_path(f.url) == "/" and f.is_html), None
                    )
                    if home is None:
                        check.problems.append(
                            "the plan requires identity schema types but no home page was read"
                        )
                    else:
                        check.home_json_ld_types = list(home.json_ld_types)
                        for wanted_type in types:
                            if wanted_type not in home.json_ld_types:
                                check.missing_schema_types.append(wanted_type)
            if "fields" in identity:
                check.notes.append(
                    "identity.fields is not checked: this tool reads @type values, not the "
                    "properties of a JSON-LD entity"
                )

    for key in plan:
        if key not in KNOWN_KEYS:
            check.notes.append(f"the plan key {key!r} is not one this consumer knows; it was ignored")
    for key, why in KNOWN_KEYS.items():
        if key in plan and key in ("offering", "url_rules", "crawler_stance", "pages"):
            check.notes.append(f"{key} — {why}")
    return check


def apply_to_report(check: PlanCheck, report: SiteReport) -> None:
    """Add a plan's unmet requirements to a report's findings, so ``--strict`` can gate on them."""
    from .facts import ERROR, Finding

    report.plan = {
        "path": check.path,
        "plan_version": check.version,
        "site": check.site,
        "kind": check.kind,
        "passed": check.passed,
        "required_surfaces_met": not check.unmet_surfaces,
        "identity_schema_types_met": not check.missing_schema_types,
        "home_json_ld_types": check.home_json_ld_types,
        "notes": check.notes,
    }
    for name in check.unmet_surfaces:
        report.findings.append(
            Finding(
                kind="plan_surface_missing",
                severity=ERROR,
                message=f"the plan requires {name}, which the site does not publish",
                subject=name,
            )
        )
    for wanted_type in check.missing_schema_types:
        report.findings.append(
            Finding(
                kind="plan_identity_missing",
                severity=ERROR,
                message=(
                    f"the plan requires the home page to carry the JSON-LD type {wanted_type!r}; "
                    f"the home page carries {check.home_json_ld_types or 'none'}"
                ),
                subject=wanted_type,
            )
        )
    for problem in check.problems:
        report.findings.append(
            Finding(
                kind="plan_unreadable_key",
                severity=ERROR,
                message=f"the plan could not be applied: {problem}",
                subject=check.path,
            )
        )
    for note in check.notes:
        report.notes.append(f"plan: {note}")
