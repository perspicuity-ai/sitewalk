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
        check = check_plan(report_for(), {"required_surfaces": ["robots.txt", "sitemap.xml"]})
        self.assertEqual(check.unmet_surfaces, [])
        self.assertTrue(check.passed)

    def test_a_missing_surface_is_reported_as_unmet(self):
        check = check_plan(report_for(), {"required_surfaces": ["robots.txt", "security.txt"]})
        self.assertEqual(check.unmet_surfaces, ["security.txt"])
        self.assertFalse(check.passed)

    def test_a_surface_that_is_a_string_rather_than_a_list_is_accepted(self):
        check = check_plan(report_for(), {"required_surfaces": "robots.txt"})
        self.assertEqual(check.unmet_surfaces, [])

    def test_a_surface_list_that_is_the_wrong_type_is_a_problem(self):
        check = check_plan(report_for(), {"required_surfaces": {"robots.txt": True}})
        self.assertTrue(check.problems)

    def test_an_unmet_surface_becomes_an_error_that_gates(self):
        report = report_for()
        apply_to_report(check_plan(report, {"required_surfaces": ["security.txt"]}), report)
        self.assertIn("plan_surface_missing", [f.kind for f in report.errors])


class IdentityChecks(unittest.TestCase):
    def test_a_required_schema_type_the_home_page_carries_is_met(self):
        check = check_plan(report_for(), {"identity": {"schema_types": ["Organization"]}})
        self.assertEqual(check.missing_schema_types, [])
        self.assertTrue(check.passed)

    def test_a_required_schema_type_the_home_page_lacks_is_reported(self):
        check = check_plan(report_for(), {"identity": {"schema_types": ["LocalBusiness", "Restaurant"]}})
        self.assertEqual(check.missing_schema_types, ["Restaurant"])

    def test_the_types_the_home_page_carries_are_reported_even_when_they_are_enough(self):
        check = check_plan(report_for(), {"identity": {"schema_types": ["Organization"]}})
        self.assertIn("Organization", check.home_json_ld_types)
        self.assertIn("WebSite", check.home_json_ld_types)

    def test_fields_are_read_but_not_checked_and_that_is_said(self):
        check = check_plan(
            report_for(), {"identity": {"schema_types": ["Organization"], "fields": ["address"]}}
        )
        self.assertTrue(any("identity.fields is not checked" in note for note in check.notes))
        self.assertFalse(check.problems)

    def test_a_missing_schema_type_becomes_an_error_that_gates(self):
        report = report_for()
        apply_to_report(check_plan(report, {"identity": {"schema_types": ["Restaurant"]}}), report)
        self.assertIn("plan_identity_missing", [f.kind for f in report.errors])
        message = [f.message for f in report.errors if f.kind == "plan_identity_missing"][0]
        self.assertIn("Organization", message)


class Leniency(unittest.TestCase):
    def test_an_unknown_key_is_ignored_with_a_note(self):
        check = check_plan(report_for(), {"required_surfaces": ["robots.txt"], "future_key": {"a": 1}})
        self.assertTrue(any("future_key" in note for note in check.notes))
        self.assertTrue(check.passed)

    def test_the_keys_that_are_not_checked_are_named_with_a_reason(self):
        check = check_plan(report_for(), FULL_PLAN)
        notes = " ".join(check.notes)
        for key in ("offering", "url_rules", "crawler_stance", "pages"):
            with self.subTest(key=key):
                self.assertIn(key, notes)

    def test_a_partial_plan_is_usable(self):
        check = check_plan(report_for(), {})
        self.assertTrue(check.passed)
        self.assertTrue(any("plan_version" in note for note in check.notes))

    def test_a_plan_version_this_consumer_does_not_know_is_a_note_not_a_failure(self):
        check = check_plan(report_for(), {"plan_version": 99, "required_surfaces": ["robots.txt"]})
        self.assertTrue(check.passed)
        self.assertTrue(any("plan_version" in note for note in check.notes))

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
        check = check_plan(report, {"identity": {"schema_types": ["Organization"]}})
        self.assertTrue(check.problems)


if __name__ == "__main__":
    unittest.main()
