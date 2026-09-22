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

from .facts import CONDITIONAL, ERROR, NOT_CHECKED, Finding, SiteReport
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

#: The surfaces this consumer can actually check.
CHECKED_SURFACES = ("robots.txt", "sitemap.xml", "llms.txt", "rss.xml", "json-ld")

#: The format's closed vocabulary for ``required_surfaces``. A name in here that this consumer
#: cannot check is a gap here, reported as unverified. A name *outside* it is not a surface of this
#: format at all, so there is nothing to check and nothing to be unverified about: it is reported
#: unmet, because the site is not publishing the thing the name denotes.
KNOWN_SURFACES = ("json-ld", "llms.txt", "robots.txt", "rss.xml", "sitemap.xml")


@dataclass
class PlanCheck:
    """The outcome of checking a site against a plan."""

    path: str
    version: Any = None
    site: str | None = None
    kind: str | None = None
    problems: list[str] = field(default_factory=list)
    unmet_surfaces: list[str] = field(default_factory=list)
    unverified_surfaces: list[str] = field(default_factory=list)
    conditions: list[str] = field(default_factory=list)
    #: Which of the enforced keys the plan actually carried, so a sub-check that never ran is
    #: reported as "not run" rather than as met or failed.
    enforced: list[str] = field(default_factory=list)
    missing_schema_types: list[str] = field(default_factory=list)
    home_json_ld_types: list[str] = field(default_factory=list)
    planned: bool = False
    notes: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        """Met outright. A conditional verdict is not a pass, and not a failure either."""
        return (
            self.planned
            and not self.problems
            and not self.unmet_surfaces
            and not self.unverified_surfaces
            and not self.missing_schema_types
            and not self.conditions
        )

    @property
    def verdict(self) -> str:
        """``met``, ``met with conditions``, or ``not met``."""
        if self.problems or self.unmet_surfaces or self.missing_schema_types:
            return "not met"
        if self.conditions or self.unverified_surfaces:
            return "met with conditions"
        return "met"


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Build an object, refusing a repeated key.

    ``json.loads`` collapses duplicates silently, so two consumers using different parsers can read
    **different plans from the same bytes** with no fault on either side — the silent divergence
    this project exists to remove. The format leaves duplicates to the parser and so cannot warn
    about them; ``object_pairs_hook`` can, so this consumer detects and refuses them rather than
    picking one. Nested objects get the same treatment: the hook is called for every object.
    """
    seen: set[str] = set()
    for key, _value in pairs:
        if key in seen:
            raise ValueError(f"duplicate key {key!r} in the same JSON object")
        seen.add(key)
    return dict(pairs)


def load_plan(path: str | Path) -> dict[str, Any]:
    """Read a plan file. Raises ``ValueError`` with a readable message when it cannot be used."""
    plan_path = Path(path)
    try:
        text = plan_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"could not read the plan file {plan_path}: {exc}") from exc
    try:
        data = json.loads(text, object_pairs_hook=_reject_duplicate_keys)
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

    # Rule 4 of the format: keys grow, versions announce. An unknown key is additive growth a
    # consumer may carry and name; an unknown version means a key's meaning may have moved, so the
    # verdict cannot be clean. Four cases, three verdicts, and the two failures share a gate while
    # saying different things about the file.
    version = check.version
    if isinstance(version, bool) or not isinstance(version, int):
        # Absent, or present and not an integer. A definite fault: the plan is invalid against
        # every version, and with no readable version the semantics of no key are known.
        check.problems.append(
            f"plan_version is required and must be the integer {SUPPORTED_PLAN_VERSION}; "
            f"this plan has {version!r}, so the file is malformed and none of its keys can be "
            "trusted"
        )
        check.conditions.append("the plan declares no usable plan_version")
    elif version < SUPPORTED_PLAN_VERSION:
        # Fully specified by its own version, so it reads normally and cleanly.
        check.notes.append(
            f"the plan declares the older plan_version {version}; an older plan is fully "
            "specified by its own version, so it was read normally"
        )
    elif version > SUPPORTED_PLAN_VERSION:
        check.conditions.append(
            f"the plan declares plan_version {version} and this consumer implements "
            f"{SUPPORTED_PLAN_VERSION}, so a key's meaning may have moved: the result is "
            "conditional and a --strict run will refuse to certify it"
        )

    required = plan.get("required_surfaces")
    if required is not None:
        check.enforced.append("required_surfaces")
        # A single surface name as a bare string is accepted here: the meaning is unambiguous,
        # and "is a list" is the kind of strictness that costs a producer a release for nothing.
        names = _as_list(required, allow_single_string=True)
        if names is None:
            check.problems.append("required_surfaces is not a list of strings")
        else:
            for name in names:
                if name not in CHECKED_SURFACES and name in KNOWN_SURFACES:
                    # A surface of this format that this consumer cannot check: a gap here, not a
                    # finding about the site. The vocabulary is closed and describes what a plan
                    # may require, so reporting it absent would assert something the code never
                    # established.
                    check.unverified_surfaces.append(name)
                    continue
                if name not in KNOWN_SURFACES:
                    # Not a surface of this format. There is no check to be missing and nothing to
                    # be unverified about; the site simply does not publish what the name denotes.
                    check.unmet_surfaces.append(name)
                    continue
                surface = report.surfaces.get(name)
                if surface is None or surface.state == NOT_CHECKED:
                    # Not looked at. Unverified, never absent: absent means a fetch was attempted
                    # and failed, and this is the case where nothing was attempted at all.
                    #
                    # `NOT_CHECKED` reaches this branch when a surface is in the format's
                    # vocabulary but not in `CHECKED_SURFACES` — which is no surface today, so the
                    # state is currently unreachable from normal runs. It is kept deliberately: it
                    # is what makes a future unchecked surface *unverified* rather than *absent*.
                    # A dead-code audit that removes it restores the exact overclaim this module
                    # was fixed to stop making. See the constant in `facts.py` for what would make
                    # it reachable, and `tests/test_plan.py::ANotCheckedSurfaceIsStillHandled`,
                    # which fails if this handling goes.
                    check.unverified_surfaces.append(name)
                elif not surface.exists:
                    check.unmet_surfaces.append(name)

    identity = plan.get("identity")
    if identity is not None:
        check.enforced.append("identity")
        if not isinstance(identity, dict):
            check.problems.append("identity is not an object")
        else:
            wanted = identity.get("schema_types")
            if wanted is not None:
                check.enforced.append("identity.schema_types")
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


def _sub_check(
    *, ran: bool, unmet: list[str], unverified: list[str], faults: list[str]
) -> bool | None:
    """``True`` met, ``False`` not met, ``None`` when the check did not run.

    Three outcomes, because two would force one of two lies: a plan that never mentions the key
    cannot be reported as passing the check, and must not be reported as failing it either.
    """
    if not ran or faults:
        return None
    if unmet:
        return False
    if unverified:
        return None
    return True


def apply_to_report(check: PlanCheck, report: SiteReport) -> None:
    """Add a plan's verdict to a report's findings, so ``--strict`` can gate on them."""
    report.plan = {
        "path": check.path,
        "plan_version": check.version,
        "site": check.site,
        "kind": check.kind,
        "passed": check.passed,
        "verdict": check.verdict,
        "conditions": list(check.conditions),
        # A sub-check reports met / not met / **None when it did not run**. `None` is not `false`:
        # claiming `true` for a check that could not run is the overclaim this project keeps
        # finding, and claiming `false` would be a finding about a site that was never examined.
        "required_surfaces_met": _sub_check(
            ran="required_surfaces" in check.enforced,
            unmet=check.unmet_surfaces,
            unverified=check.unverified_surfaces,
            faults=check.problems,
        ),
        "required_surfaces_unverified": list(check.unverified_surfaces),
        "identity_schema_types_met": _sub_check(
            ran="identity.schema_types" in check.enforced,
            unmet=check.missing_schema_types,
            unverified=[],
            faults=check.problems,
        ),
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
    for name in check.unverified_surfaces:
        report.findings.append(
            Finding(
                kind="plan_surface_unverified",
                severity=CONDITIONAL,
                message=(
                    f"the plan requires {name}, which this tool has no check for; it is reported "
                    "unverified rather than absent, and a --strict run will not certify a plan "
                    "containing it"
                ),
                subject=name,
            )
        )
    for condition in check.conditions:
        report.findings.append(
            Finding(
                kind="plan_verdict_conditional",
                severity=CONDITIONAL,
                message=condition,
                subject=check.path,
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
                kind="plan_invalid",
                severity=ERROR,
                message=f"the plan could not be applied: {problem}",
                subject=check.path,
            )
        )
    for note in check.notes:
        report.notes.append(f"plan: {note}")
