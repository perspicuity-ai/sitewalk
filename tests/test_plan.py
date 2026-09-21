"""``--plan``: checking a built site against the plan it claims to follow.

The plan format is owned by ``siteplan``, and the consumer promise is narrow on purpose: check
``required_surfaces`` and the home page's ``identity.schema_types``, ignore keys this consumer
does not know, and never claim to have checked something it cannot observe. These tests pin that
promise, including the parts that are deliberately *not* enforced.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from sitewalk import findings
from sitewalk.crawl import CrawlResult, crawl
from sitewalk.plan import apply_to_report, check_plan, load_plan
from sitewalk.report import exit_code, to_dict
from sitewalk.sources import FileSource

from . import fakes
from .fakes import FIXTURES

EXAMPLE = FIXTURES / "example-site"

FULL_PLAN = {
    "plan_version": 1,
    "site": "example.com",
    "kind": "local-business",
    "required_surfaces": ["robots.txt", "sitemap.xml", "llms.txt"],
    "identity": {"schema_types": ["Organization"], "fields": ["name", "address"]},
    "offering": {"schema_types": ["Service"], "fields": ["name"]},
    "url_rules": {"lowercase": True, "trailing_slash": "never", "max_depth": 3},
    "crawler_stance": "open",
    "pages": [{"path": "/", "purpose": "what the business is"}],
}


def report_for(directory: Path = EXAMPLE):
    with fakes.no_network():
        source = FileSource(directory)
        result = crawl(source, source.origin)
    return findings.analyse(result)


def write_plan(data) -> str:
    handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    json.dump(data, handle)
    handle.close()
    return handle.name


class Loading(unittest.TestCase):
    def test_reads_a_plan_file(self):
        path = write_plan(FULL_PLAN)
        self.addCleanup(Path(path).unlink)
        self.assertEqual(load_plan(path)["plan_version"], 1)

    def test_a_missing_file_is_an_error_with_a_readable_message(self):
        with self.assertRaises(ValueError) as caught:
            load_plan("/nonexistent/site.json")
        self.assertIn("could not read", str(caught.exception))

    def test_invalid_json_is_an_error(self):
        handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        handle.write("{not json")
        handle.close()
        self.addCleanup(Path(handle.name).unlink)
        with self.assertRaises(ValueError) as caught:
            load_plan(handle.name)
        self.assertIn("not valid JSON", str(caught.exception))

    def test_a_json_document_that_is_not_an_object_is_an_error(self):
        handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        handle.write("[1, 2, 3]")
        handle.close()
        self.addCleanup(Path(handle.name).unlink)
        with self.assertRaises(ValueError):
            load_plan(handle.name)


class SurfaceChecks(unittest.TestCase):
    def test_a_plan_whose_surfaces_are_all_published_is_met(self):
        check = check_plan(report_for(), {"plan_version": 1, "required_surfaces": ["robots.txt", "sitemap.xml"]})
        self.assertEqual(check.unmet_surfaces, [])
        self.assertTrue(check.passed)

    def test_a_missing_surface_is_reported_as_unmet(self):
        check = check_plan(report_for(), {"plan_version": 1, "required_surfaces": ["robots.txt", "security.txt"]})
        self.assertEqual(check.unmet_surfaces, ["security.txt"])
        self.assertFalse(check.passed)

    def test_a_surface_that_is_a_string_rather_than_a_list_is_accepted(self):
        check = check_plan(report_for(), {"plan_version": 1, "required_surfaces": "robots.txt"})
        self.assertEqual(check.unmet_surfaces, [])

    def test_a_surface_list_that_is_the_wrong_type_is_a_problem(self):
        check = check_plan(report_for(), {"plan_version": 1, "required_surfaces": {"robots.txt": True}})
        self.assertTrue(check.problems)

    def test_an_unmet_surface_becomes_an_error_that_gates(self):
        report = report_for()
        apply_to_report(check_plan(report, {"plan_version": 1, "required_surfaces": ["security.txt"]}), report)
        self.assertIn("plan_surface_missing", [f.kind for f in report.errors])


class IdentityChecks(unittest.TestCase):
    def test_a_required_schema_type_the_home_page_carries_is_met(self):
        check = check_plan(report_for(), {"plan_version": 1, "identity": {"schema_types": ["Organization"]}})
        self.assertEqual(check.missing_schema_types, [])
        self.assertTrue(check.passed)

    def test_a_required_schema_type_the_home_page_lacks_is_reported(self):
        check = check_plan(report_for(), {"plan_version": 1, "identity": {"schema_types": ["LocalBusiness", "Restaurant"]}})
        self.assertEqual(check.missing_schema_types, ["Restaurant"])

    def test_the_types_the_home_page_carries_are_reported_even_when_they_are_enough(self):
        check = check_plan(report_for(), {"plan_version": 1, "identity": {"schema_types": ["Organization"]}})
        self.assertIn("Organization", check.home_json_ld_types)
        self.assertIn("WebSite", check.home_json_ld_types)

    def test_fields_are_read_but_not_checked_and_that_is_said(self):
        check = check_plan(
            report_for(), {"plan_version": 1, "identity": {"schema_types": ["Organization"], "fields": ["address"]}}
        )
        self.assertTrue(any("identity.fields is not checked" in note for note in check.notes))
        self.assertFalse(check.problems)

    def test_a_missing_schema_type_becomes_an_error_that_gates(self):
        report = report_for()
        apply_to_report(check_plan(report, {"plan_version": 1, "identity": {"schema_types": ["Restaurant"]}}), report)
        self.assertIn("plan_identity_missing", [f.kind for f in report.errors])
        message = [f.message for f in report.errors if f.kind == "plan_identity_missing"][0]
        self.assertIn("Organization", message)


class Leniency(unittest.TestCase):
    def test_an_unknown_key_is_ignored_with_a_note(self):
        check = check_plan(
            report_for(), {"plan_version": 1, "required_surfaces": ["robots.txt"], "future_key": {"a": 1}}
        )
        self.assertTrue(any("future_key" in note for note in check.notes))
        self.assertTrue(check.passed)

    def test_the_keys_that_are_not_checked_are_named_with_a_reason(self):
        check = check_plan(report_for(), FULL_PLAN)
        notes = " ".join(check.notes)
        for key in ("offering", "url_rules", "crawler_stance", "pages"):
            with self.subTest(key=key):
                self.assertIn(key, notes)

    def test_a_plan_with_only_a_version_is_valid_and_met(self):
        # The format: every key except the version marker is optional, so this plan means
        # "nothing is decided yet" and there is nothing for it to fail.
        check = check_plan(report_for(), {"plan_version": 1})
        self.assertTrue(check.passed)
        self.assertEqual(check.verdict, "met")

    def test_an_empty_plan_is_a_fault_because_a_file_must_name_its_format(self):
        # Superseded an earlier expectation that {} was usable. The frozen format requires
        # plan_version: a file that does not name its format cannot be validated safely.
        check = check_plan(report_for(), {})
        self.assertFalse(check.passed)
        self.assertEqual(check.verdict, "not met")
        self.assertTrue(any("plan_version" in problem for problem in check.problems))

    def test_a_known_version_reads_clean(self):
        check = check_plan(report_for(), {"plan_version": 1, "required_surfaces": ["robots.txt"]})
        self.assertTrue(check.passed)
        self.assertEqual(check.verdict, "met")

    def test_an_older_version_reads_normally_and_cleanly(self):
        # Fully specified by its own version, so there is nothing conditional about it.
        check = check_plan(report_for(), {"plan_version": 0, "required_surfaces": ["robots.txt"]})
        self.assertTrue(check.passed)
        self.assertEqual(check.verdict, "met")
        self.assertEqual(check.conditions, [])

    def test_an_unknown_or_newer_version_makes_the_verdict_conditional(self):
        # The format's rule 4: an unknown version means a key's meaning may have moved.
        check = check_plan(report_for(), {"plan_version": 99, "required_surfaces": ["robots.txt"]})
        self.assertFalse(check.passed)
        self.assertEqual(check.verdict, "met with conditions")
        self.assertEqual(check.problems, [], "a newer version is not a malformed file")
        self.assertTrue(check.conditions)

    def test_an_absent_version_is_a_definite_fault(self):
        # Not conditional: invalid against every version, so no key's semantics are known.
        check = check_plan(report_for(), {"required_surfaces": ["robots.txt"]})
        self.assertFalse(check.passed)
        self.assertEqual(check.verdict, "not met")
        self.assertTrue(check.problems)
        self.assertTrue(any("malformed" in problem for problem in check.problems))

    def test_a_mistyped_version_is_a_definite_fault(self):
        for value in ("1", 1.0, None, [1], True):
            with self.subTest(value=value):
                check = check_plan(report_for(), {"plan_version": value})
                self.assertTrue(check.problems, f"{value!r} was not reported as a fault")

    def test_the_two_failures_say_different_things(self):
        # Same gate, different claims about the file. Conflating them would tell a reader "this
        # might be a newer format" when the truth is "this file is malformed".
        newer = check_plan(report_for(), {"plan_version": 99})
        absent = check_plan(report_for(), {})
        newer_text = " ".join(newer.conditions)
        absent_text = " ".join(absent.problems)
        self.assertIn("may have moved", newer_text)
        self.assertNotIn("malformed", newer_text)
        self.assertIn("malformed", absent_text)

    def test_an_unknown_version_still_enforces_the_keys_it_knows(self):
        # Leniency about the version is not leniency about the checks.
        check = check_plan(
            report_for(), {"plan_version": 99, "required_surfaces": ["security.txt"]}
        )
        self.assertEqual(check.unmet_surfaces, ["security.txt"])
        self.assertEqual(check.verdict, "not met")

    def test_the_fixtures_two_version_cases_are_read_as_the_format_says(self):
        # Taken from siteplan's own conformance fixture, so the cases are the producer's rather
        # than invented here. Only these two; the other 38 test the producer's faults and a
        # consumer is explicitly permitted to tolerate them.
        import json
        from pathlib import Path

        fixture = Path("/home/david/projects/siteplan/docs/fixtures/plan-conformance.json")
        if not fixture.exists():
            self.skipTest("the siteplan conformance fixture is not present")
        cases = {c["name"]: c for c in json.loads(fixture.read_text())["cases"]}
        newer = check_plan(report_for(), cases["unknown-version"]["plan"])
        self.assertEqual(newer.verdict, "met with conditions")
        mistyped = check_plan(report_for(), cases["version-not-an-integer"]["plan"])
        self.assertEqual(mistyped.verdict, "not met")
        absent = check_plan(report_for(), cases["missing-plan-version"]["plan"])
        self.assertEqual(absent.verdict, "not met")

    def test_the_seven_valid_conformance_plans_are_read_without_a_fault(self):
        """The accept-cases: a well-formed plan is read, which is not the same as a conforming site.

        The assertion is deliberately *not* ``verdict == "met"``. A valid plan may require a
        surface this tool cannot check, or a Schema.org type the fixture site does not carry, and
        both are legitimate outcomes for a well-formed plan against a particular site. What these
        seven establish is that the consumer finds no **fault** in a valid plan — no missing
        version, no wrong type, no malformed shape. Asserting "met" here would have been the same
        overclaim the plan check itself was making.
        """
        import json
        from pathlib import Path

        fixture = Path("/home/david/projects/siteplan/docs/fixtures/plan-conformance.json")
        if not fixture.exists():
            self.skipTest("the siteplan conformance fixture is not present")
        for case in json.loads(fixture.read_text())["cases"]:
            if not case.get("valid"):
                continue
            with self.subTest(case=case["name"]):
                check = check_plan(report_for(), case["plan"])
                self.assertEqual(check.problems, [], case["name"])

    def test_the_thirty_eight_invalid_conformance_plans_are_not_treated_as_site_faults(self):
        """A consumer is permitted to tolerate what the producer rejects.

        Rule 6: the file is invalid and the producer rejects it, while the consumer may carry it
        and name what it did not check. So none of the 38 may raise a *site* finding here — they
        may only ever be read, with their faults noted. Asserting all 45 as accept-cases would have
        produced a suite failing 38 times while being wrong about the specification.
        """
        import json
        from pathlib import Path

        fixture = Path("/home/david/projects/siteplan/docs/fixtures/plan-conformance.json")
        if not fixture.exists():
            self.skipTest("the siteplan conformance fixture is not present")
        cases = [c for c in json.loads(fixture.read_text())["cases"] if not c.get("valid")]
        self.assertEqual(len(cases), 38)
        for case in cases:
            plan = case["plan"]
            if not isinstance(plan, dict):
                continue  # a non-object cannot be read as a plan at all
            with self.subTest(case=case["name"]):
                check = check_plan(report_for(), plan)
                # A fault inside a key this consumer does not enforce must not become a finding
                # about the site. The only faults it may report are its own two keys.
                # Permitted: faults on the keys this consumer enforces. Anything deeper — a
                # fault in url_rules, kind, pages, offering, or a schema type's spelling — is the
                # producer's business and must not surface as a finding about the site.
                enforced = ("plan_version", "required_surfaces", "identity")
                for problem in check.problems:
                    self.assertTrue(
                        any(key in problem for key in enforced),
                        f"{case['name']}: fault outside the enforced keys: {problem}",
                    )

    def test_an_unknown_key_never_fails_the_check(self):
        check = check_plan(
            report_for(),
            {"plan_version": 1, "required_surfaces": ["robots.txt"], "invented": [1, 2, 3]},
        )
        self.assertFalse(check.problems)
        self.assertTrue(check.passed)
        self.assertTrue(any("invented" in note for note in check.notes))

    def test_the_full_plan_from_the_siteplan_context_is_met_by_a_conforming_site(self):
        check = check_plan(report_for(), FULL_PLAN)
        self.assertEqual(check.unmet_surfaces, [])
        self.assertEqual(check.missing_schema_types, [])
        self.assertTrue(check.passed)

    def test_the_plan_result_is_recorded_on_the_report(self):
        report = report_for()
        apply_to_report(check_plan(report, FULL_PLAN, path="site.json"), report)
        self.assertTrue(report.plan["passed"])
        self.assertEqual(report.plan["path"], "site.json")
        self.assertEqual(report.plan["site"], "example.com")


class NoHomePage(unittest.TestCase):
    def test_a_plan_requiring_identity_types_with_no_home_page_is_a_problem(self):
        report = findings.analyse(CrawlResult(target="https://example.com", origin="https://example.com"))
        check = check_plan(report, {"plan_version": 1, "identity": {"schema_types": ["Organization"]}})
        self.assertTrue(check.problems)


if __name__ == "__main__":
    unittest.main()


class TheVerdictIsHonestAboutWhatItKnows(unittest.TestCase):
    """U7: the report states what is true; the gate decides what is tolerable.

    Every assertion here reads a machine-readable value — a severity, a count, an exit code — and
    not a message string, so a later change to the wording cannot make these pass while the
    behaviour changes.
    """

    def report_for_plan(self, plan):
        report = report_for()
        apply_to_report(check_plan(report, plan, path="site.json"), report)
        return report

    def test_a_known_version_produces_no_conditional_finding(self):
        report = self.report_for_plan({"plan_version": 1, "required_surfaces": ["robots.txt"]})
        self.assertEqual([f.kind for f in report.conditionals], [])
        self.assertEqual(exit_code(report, strict=True), 1)  # the fixture's own findings gate

    def test_an_older_version_produces_no_conditional_finding(self):
        report = self.report_for_plan({"plan_version": 0, "required_surfaces": ["robots.txt"]})
        self.assertEqual([f.kind for f in report.conditionals], [])

    def test_an_unknown_version_is_conditional_and_gates_under_strict(self):
        report = self.report_for_plan({"plan_version": 99})
        kinds = [f.kind for f in report.conditionals]
        self.assertIn("plan_verdict_conditional", kinds)
        self.assertEqual([f.severity for f in report.conditionals], ["conditional"])
        self.assertEqual(report.plan["verdict"], "met with conditions")
        self.assertEqual(exit_code(report, strict=True), 1)

    def test_an_absent_version_is_an_error_and_gates_under_strict(self):
        report = self.report_for_plan({})
        self.assertIn("plan_invalid", [f.kind for f in report.errors])
        self.assertEqual(report.plan["verdict"], "not met")
        self.assertEqual(exit_code(report, strict=True), 1)

    def test_a_mistyped_version_is_an_error_and_gates_under_strict(self):
        report = self.report_for_plan({"plan_version": "1"})
        self.assertIn("plan_invalid", [f.kind for f in report.errors])
        self.assertEqual(exit_code(report, strict=True), 1)

    def test_the_version_finding_reaches_the_json_with_its_severity(self):
        report = self.report_for_plan({"plan_version": 99})
        data = to_dict(report)
        severities = {f["kind"]: f["severity"] for f in data["findings"]}
        self.assertEqual(severities["plan_verdict_conditional"], "conditional")
        self.assertEqual(data["finding_counts"]["conditional"], 1)
        self.assertIn("conditional", data["severities"])
        self.assertEqual(data["plan"]["verdict"], "met with conditions")

    def test_the_gating_count_matches_the_policy_table(self):
        # The JSON tells a machine reader the verdict without its having to infer it from an exit
        # code, which is what design A exists to prevent. Run against the **bare** fixture, whose
        # own findings are nil, so the count is the plan's contribution and nothing else.
        def bare_report(plan):
            report = findings.analyse(_crawl(FIXTURES / "bare-site"))
            apply_to_report(check_plan(report, plan, path="site.json"), report)
            return report

        # Measured as the plan's own contribution, so the fixture's unrelated findings cannot
        # make the assertion pass for the wrong reason.
        baseline = to_dict(findings.analyse(_crawl(FIXTURES / "bare-site")))["finding_counts"]
        # A malformed plan contributes **two** gating findings and that is the honest shape: an
        # error saying the file is malformed, and a conditional saying that with no usable version
        # the semantics of no key are known. They are different claims and both are true.
        for plan, gating, conditional in (
            ({"plan_version": 1}, 0, 0),
            ({"plan_version": 99}, 1, 1),   # valid file, unknown specification: conditional only
            ({}, 2, 1),                     # invalid file: an error, plus the unknown-semantics note
        ):
            with self.subTest(plan=plan):
                data = to_dict(bare_report(plan))
                counts = data["finding_counts"]
                self.assertEqual(counts["gating"] - baseline["gating"], gating, plan)
                self.assertEqual(counts["conditional"] - baseline["conditional"], conditional, plan)


class EveryVocabularySurfaceHasACheck(unittest.TestCase):
    """U8's claim, and the guard against a future surface arriving in the format unchecked."""

    def test_every_vocabulary_surface_is_checked_now(self):
        from sitewalk.plan import CHECKED_SURFACES, KNOWN_SURFACES

        self.assertEqual(
            set(KNOWN_SURFACES),
            set(CHECKED_SURFACES),
            "a surface is in the format's vocabulary but this consumer does not check it, so the "
            "unverified path is reachable again and U7's fifth criterion applies to it",
        )


class AnUncheckedSurfaceIsUnverifiedNotAbsent(unittest.TestCase):
    """U7's fifth criterion, still live now that U8 added the last two checks.

    U8 implemented `rss.xml` and `json-ld`, so every surface in the format's vocabulary is now
    checked and the gap cannot be reached through a real name. The rule is not retired by that: a
    sixth surface added to the format reopens it. So the gap is injected here, deliberately, by
    taking one surface out of the checked set — which is also the test that fails if someone later
    adds a surface to the vocabulary without a check and without noticing.
    """

    def setUp(self):
        import sitewalk.plan as plan_module

        self.plan_module = plan_module
        self.original = plan_module.CHECKED_SURFACES
        self.addCleanup(setattr, plan_module, "CHECKED_SURFACES", self.original)
        plan_module.CHECKED_SURFACES = tuple(
            name for name in self.original if name != "rss.xml"
        )

    def test_a_vocabulary_surface_with_no_check_is_unverified(self):
        check = check_plan(report_for(), {"plan_version": 1, "required_surfaces": ["rss.xml"]})
        self.assertEqual(check.unverified_surfaces, ["rss.xml"])
        self.assertEqual(check.unmet_surfaces, [], "reported as absent without being looked for")
        self.assertEqual(check.verdict, "met with conditions")

    def test_the_unverified_surface_is_a_conditional_finding_that_gates_under_strict(self):
        report = report_for()
        apply_to_report(
            check_plan(report, {"plan_version": 1, "required_surfaces": ["rss.xml"]}), report
        )
        kinds = {f.kind: f.severity for f in report.conditionals}
        self.assertEqual(kinds.get("plan_surface_unverified"), "conditional")
        self.assertNotIn("plan_surface_missing", [f.kind for f in report.findings])
        self.assertEqual(exit_code(report, strict=True), 1)

    def test_the_finding_does_not_say_the_site_lacks_it(self):
        # The exact defect this replaced: "the plan requires rss.xml, which the site does not
        # publish" asserted something the code never established.
        report = report_for()
        apply_to_report(
            check_plan(report, {"plan_version": 1, "required_surfaces": ["rss.xml"]}), report
        )
        message = [f.message for f in report.findings if f.kind == "plan_surface_unverified"][0]
        self.assertIn("no check for", message)
        self.assertNotIn("does not publish", message)

    def test_a_name_outside_the_vocabulary_is_neither_checked_nor_claimed_unverified(self):
        # `security.txt` is not a surface of this format, so there is no check to be missing.
        check = check_plan(report_for(), {"plan_version": 1, "required_surfaces": ["security.txt"]})
        self.assertEqual(check.unmet_surfaces, ["security.txt"])
        self.assertEqual(check.unverified_surfaces, [])


def _crawl(directory):
    from sitewalk.crawl import crawl as run_crawl
    from sitewalk.sources import FileSource

    source = FileSource(directory)
    return run_crawl(source, source.origin)



class ASubCheckReportsWhetherItRan(unittest.TestCase):
    """U9: `required_surfaces_met: true` beside `passed: false` was an overclaim.

    A plan that never mentions a key cannot be reported as passing the check for it, and must not
    be reported as failing it either. Three outcomes, because two would force one of two lies.
    """

    def plan_block(self, plan):
        report = report_for()
        apply_to_report(check_plan(report, plan), report)
        return report.plan

    def test_a_check_that_ran_and_passed_is_true(self):
        block = self.plan_block({"plan_version": 1, "required_surfaces": ["robots.txt"]})
        self.assertIs(block["required_surfaces_met"], True)

    def test_a_check_that_ran_and_failed_is_false(self):
        block = self.plan_block({"plan_version": 1, "required_surfaces": ["security.txt"]})
        self.assertIs(block["required_surfaces_met"], False)

    def test_a_check_that_never_ran_is_neither(self):
        block = self.plan_block({"plan_version": 1, "kind": "saas"})
        self.assertIsNone(
            block["required_surfaces_met"],
            "a check that did not run must not be reported as passing",
        )
        self.assertIsNone(block["identity_schema_types_met"])

    def test_a_malformed_plan_reports_no_sub_check_as_met(self):
        # The reported defect: passed false while a sub-check claimed true.
        block = self.plan_block({"kind": "saas"})
        self.assertFalse(block["passed"])
        self.assertIsNone(block["required_surfaces_met"])
        self.assertIsNone(block["identity_schema_types_met"])

    def test_no_sub_check_claims_true_when_the_plan_did_not_pass(self):
        for plan in ({"plan_version": 99}, {}, {"plan_version": 1, "identity": "not an object"}):
            with self.subTest(plan=plan):
                block = self.plan_block(plan)
                if block["passed"]:
                    continue
                self.assertIsNot(block["required_surfaces_met"], True, plan)
                self.assertIsNot(block["identity_schema_types_met"], True, plan)


class ANotCheckedSurfaceIsStillHandled(unittest.TestCase):
    """The guard on `not_checked`, which is declared and currently unreachable.

    No live path assigns that state, because every surface in the format's vocabulary is checked.
    A dead-code audit — the one U9 ran — will find it unreached and may reasonably want to remove
    it. Removing it restores the overclaim U7 and U8 were built to stop making: a surface nothing
    looked for, reported as one the site does not publish.

    So its handling is asserted rather than trusted. This test fails if the state, or the branch
    that reads it, is deleted.
    """

    def test_the_state_is_declared(self):
        from sitewalk.facts import NOT_CHECKED

        self.assertEqual(NOT_CHECKED, "not_checked")

    def test_a_surface_in_that_state_is_handled_as_unverified(self):
        from sitewalk.facts import NOT_CHECKED, Surface

        report = report_for()
        # Injected directly rather than by making a surface unchecked, so the assertion is on the
        # branch in the plan check and not on how the state was produced.
        report.surfaces["rss.xml"] = Surface(name="rss.xml", state=NOT_CHECKED)
        check = check_plan(report, {"plan_version": 1, "required_surfaces": ["rss.xml"]})
        self.assertEqual(check.unverified_surfaces, ["rss.xml"])
        self.assertEqual(check.unmet_surfaces, [], "an unchecked surface was reported as absent")
        self.assertEqual(check.verdict, "met with conditions")

    def test_the_state_reaches_a_gating_conditional_finding(self):
        from sitewalk.facts import NOT_CHECKED, Surface

        report = report_for()
        report.surfaces["rss.xml"] = Surface(name="rss.xml", state=NOT_CHECKED)
        apply_to_report(
            check_plan(report, {"plan_version": 1, "required_surfaces": ["rss.xml"]}), report
        )
        kinds = {f.kind: f.severity for f in report.conditionals}
        self.assertEqual(kinds.get("plan_surface_unverified"), "conditional")
        self.assertEqual(exit_code(report, strict=True), 1)

    def test_the_state_is_unreachable_today_and_that_is_the_point(self):
        # Documents the unreachability rather than hiding it: every vocabulary surface is checked,
        # so the state is a safety net and not a live path. If this assertion ever fails, the
        # state has become reachable — which is also fine, and the two tests above cover it.
        from sitewalk.plan import CHECKED_SURFACES, KNOWN_SURFACES

        self.assertEqual(set(KNOWN_SURFACES), set(CHECKED_SURFACES))
