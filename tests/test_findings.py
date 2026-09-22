"""Site-wide findings, and the severities that decide what gates.

Two things are asserted here that matter more than the messages: that every finding the product
promises is actually produced from real bytes, and that a finding is either an error that gates
under ``--strict`` or a note that does not, with a reason a reader can see. A gate that fails on
a site's design choices gets switched off, and a switched-off gate measures nothing.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from sitewalk import findings
from sitewalk.crawl import CrawlResult, crawl
from sitewalk.facts import ERROR, INFO, PageFact, Surface
from sitewalk.sources import FileSource

from .fakes import FIXTURES

EXAMPLE = FIXTURES / "example-site"


def offline_result(directory: Path = EXAMPLE, origin: str = "", **kwargs) -> CrawlResult:
    source = FileSource(directory)
    with __import__("tests.fakes", fromlist=["no_network"]).no_network():
        return crawl(source, source.origin, declared_origin=origin, **kwargs)


def fact(url: str, **kwargs) -> PageFact:
    base = {"status": 200, "content_type": "text/html"}
    base.update(kwargs)
    return PageFact(url=url, **base)


def kinds(report) -> list[str]:
    return [finding.kind for finding in report.findings]


def message_for(report, kind: str) -> str:
    matches = [finding.message for finding in report.findings if finding.kind == kind]
    return matches[0] if matches else ""


class EveryPromisedFindingIsProduced(unittest.TestCase):
    """Each case names the fixture page that produces it, so a failure says where to look."""

    @classmethod
    def setUpClass(cls):
        cls.report = findings.analyse(offline_result(origin="https://localhost"))
        cls.produced = kinds(cls.report)

    def test_page_count_and_status_distribution(self):
        self.assertEqual(self.report.status_counts, {"200": 8, "404": 3})

    def test_sitemap_urls_never_reached(self):
        self.assertIn("sitemap_url_not_reached", self.produced)
        self.assertEqual(self.report.sitemap_unreached, ["https://localhost/private/"])

    def test_orphan_pages(self):
        self.assertIn("orphan_page", self.produced)
        message = message_for(self.report, "orphan_page")
        self.assertIn("/shell.html", message)
        self.assertIn("/notes.txt", message)

    def test_duplicate_titles(self):
        self.assertIn("duplicate_title", self.produced)
        self.assertIn("Example Site", message_for(self.report, "duplicate_title"))

    def test_a_missing_title_and_an_empty_one_are_different_findings(self):
        self.assertIn("missing_title", self.produced)
        self.assertIn("empty_title", self.produced)
        self.assertIn("/landing.html", message_for(self.report, "missing_title"))
        self.assertIn("/untitled.html", message_for(self.report, "empty_title"))

    def test_duplicate_descriptions(self):
        self.assertIn("duplicate_description", self.produced)
        message = message_for(self.report, "duplicate_description")
        self.assertIn("/about/", message)
        self.assertIn("/team/", message)

    def test_canonicals_pointing_at_another_host(self):
        # Judged against a declared origin: a host can only be called foreign against an origin
        # the site claims to be, so this needs one (U14).
        self.assertIn("canonical_other_host", self.produced)
        self.assertIn("example.org", message_for(self.report, "canonical_other_host"))

    def test_pages_carrying_no_json_ld(self):
        self.assertIn("no_json_ld", self.produced)
        self.assertIn("/about/", message_for(self.report, "no_json_ld"))

    def test_internal_links_that_do_not_return_200(self):
        self.assertIn("broken_internal_link", self.produced)
        messages = [f.message for f in self.report.findings if f.kind == "broken_internal_link"]
        self.assertTrue(any("/services/missing/" in message for message in messages))
        self.assertTrue(any("/broken/" in message for message in messages))

    def test_the_existence_of_the_surfaces_the_specification_names(self):
        # The three the principal's specification names, plus the two U8 added so a plan requiring
        # any of the format's five can get a real verdict.
        self.assertEqual(
            {name: surface.exists for name, surface in self.report.surfaces.items()},
            {
                "robots.txt": True,
                "sitemap.xml": True,
                "llms.txt": True,
                "rss.xml": False,
                "json-ld": True,
            },
        )

    def test_a_missing_rss_feed_is_a_note_not_an_error(self):
        # rss.xml is not one of the surfaces the specification requires, so a site without one is
        # not defective. Only a plan that requires it makes it a finding.
        notes = [f.message for f in self.report.infos if f.kind == "surface_missing"]
        self.assertTrue(any("rss.xml" in message for message in notes), notes)
        self.assertFalse([f for f in self.report.errors if "rss.xml" in f.message])

    def test_a_missing_surface_is_a_note(self):
        report = findings.analyse(offline_result(FIXTURES / "bare-site"))
        self.assertIn("surface_missing", kinds(report))
        self.assertNotIn("surface_missing", [f.kind for f in report.errors])

    def test_a_page_that_looks_script_rendered_is_reported_as_a_note(self):
        self.assertIn("script_rendered", self.produced)
        self.assertNotIn("script_rendered", [f.kind for f in self.report.errors])
        self.assertIn("does not execute JavaScript", message_for(self.report, "script_rendered"))

    def test_a_page_with_a_title_produces_neither_title_finding(self):
        report = findings.analyse(offline_result(FIXTURES / "bare-site"))
        self.assertNotIn("missing_title", kinds(report))
        self.assertNotIn("empty_title", kinds(report))


class Severities(unittest.TestCase):
    def test_every_error_kind_gates_and_every_info_kind_does_not(self):
        report = findings.analyse(offline_result())
        for finding in report.findings:
            with self.subTest(kind=finding.kind):
                if finding.severity == ERROR:
                    self.assertNotIn(finding.kind, findings._INFO_KINDS)
                else:
                    self.assertEqual(finding.severity, INFO)

    def test_an_orphan_page_gates(self):
        report = findings.analyse(offline_result())
        self.assertIn("orphan_page", [f.kind for f in report.errors])

    def test_a_script_rendered_page_does_not_gate(self):
        report = findings.analyse(offline_result())
        self.assertIn("script_rendered", [f.kind for f in report.infos])

    def test_a_long_finding_is_shortened_rather_than_printed_whole(self):
        report = findings.analyse(offline_result())
        self.assertTrue(all(len(f.message) < 2000 for f in report.findings))

    def test_no_finding_claims_anything_about_ranking_or_recommendation(self):
        report = findings.analyse(offline_result())
        forbidden = ("rank", "citation", "traffic", "recommend", "score", "grade", "seo")
        for finding in report.findings:
            with self.subTest(kind=finding.kind):
                lowered = finding.message.lower()
                for word in forbidden:
                    self.assertNotIn(word, lowered, finding.message)


class DuplicateDetection(unittest.TestCase):
    def _report(self, facts):
        result = CrawlResult(
            target="https://example.com",
            origin="https://example.com",
            pages=list(facts),
            surfaces={},
        )
        return findings.analyse(result)

    def test_two_pages_with_the_same_title_are_reported_once(self):
        report = self._report(
            [
                fact("https://example.com/a", title="Same"),
                fact("https://example.com/b", title="Same"),
                fact("https://example.com/c", title="Other"),
            ]
        )
        duplicates = [f for f in report.findings if f.kind == "duplicate_title"]
        self.assertEqual(len(duplicates), 1)
        self.assertIn("/a", duplicates[0].message)
        self.assertIn("/b", duplicates[0].message)
        self.assertNotIn("/c", duplicates[0].message)

    def test_two_pages_with_an_empty_title_are_not_duplicates(self):
        report = self._report(
            [fact("https://example.com/a", title=""), fact("https://example.com/b", title="")]
        )
        self.assertNotIn("duplicate_title", kinds(report))
        self.assertIn("empty_title", kinds(report))

    def test_two_pages_with_no_description_are_not_duplicates(self):
        report = self._report(
            [fact("https://example.com/a", description=None), fact("https://example.com/b", description=None)]
        )
        self.assertNotIn("duplicate_description", kinds(report))
        self.assertIn("missing_description", kinds(report))

    def test_a_page_that_did_not_answer_is_not_asked_about_its_title(self):
        report = self._report(
            [
                fact("https://example.com/a", title="Same"),
                fact("https://example.com/b", status=500, title=None),
            ]
        )
        self.assertIn("page_not_ok", kinds(report))
        self.assertNotIn("missing_title", kinds(report))
        self.assertTrue(any("unknown rather than absent" in note for note in report.notes))

    def test_a_canonical_on_another_host_is_an_error_and_a_self_canonical_is_not(self):
        result = CrawlResult(
            target="https://example.com",
            origin="https://example.com",
            declared_origin="https://example.com",
            pages=[
                fact("https://example.com/a", canonical="https://elsewhere.example/a", canonical_host="elsewhere.example"),
                fact("https://example.com/b", canonical="https://example.com/b", canonical_host="example.com"),
            ],
        )
        report = findings.analyse(result)
        self.assertIn("canonical_other_host", kinds(report))
        self.assertNotIn("canonical_other_path", kinds(report))


class Orphans(unittest.TestCase):
    def _report(self, facts, sitemap):
        result = CrawlResult(
            target="https://example.com",
            origin="https://example.com",
            pages=list(facts),
            sitemap_urls=list(sitemap),
            surfaces={},
        )
        return findings.analyse(result)

    def test_the_home_page_is_never_an_orphan(self):
        home = fact("https://example.com/", in_sitemap=True)
        report = self._report([home], ["https://example.com/"])
        self.assertNotIn("orphan_page", kinds(report))

    def test_a_page_in_the_sitemap_and_linked_from_nowhere_is_an_orphan(self):
        home = fact("https://example.com/", in_sitemap=True)
        orphan = fact("https://example.com/orphan/", in_sitemap=True)
        report = self._report([home, orphan], ["https://example.com/", "https://example.com/orphan/"])
        self.assertIn("orphan_page", kinds(report))

    def test_a_page_that_is_linked_is_not_an_orphan(self):
        home = fact("https://example.com/", in_sitemap=True, internal_targets=("https://example.com/linked/",))
        linked = fact("https://example.com/linked/", in_sitemap=True)
        report = self._report([home, linked], ["https://example.com/", "https://example.com/linked/"])
        self.assertNotIn("orphan_page", kinds(report))

    def test_a_page_not_in_the_sitemap_is_not_an_orphan(self):
        home = fact("https://example.com/", in_sitemap=True)
        extra = fact("https://example.com/extra/", in_sitemap=False)
        report = self._report([home, extra], ["https://example.com/"])
        self.assertNotIn("orphan_page", kinds(report))


class LimitsAndNotesOnTheReport(unittest.TestCase):
    def test_the_report_carries_the_run_limits(self):
        report = findings.analyse(offline_result())
        self.assertIn("requests_made", report.limits)
        self.assertIn("pages_read", report.limits)
        self.assertFalse(report.limits["page_cap_reached"])

    def test_the_report_carries_the_json_ld_type_counts(self):
        report = findings.analyse(offline_result())
        self.assertEqual(report.json_ld_type_counts.get("Organization"), 2)
        self.assertEqual(report.json_ld_type_counts.get("Service"), 1)

    def test_a_guard_refusal_is_a_note_and_not_a_site_finding(self):
        class Refusing:
            kind = "url"
            label = "https://example.com"
            refusals = ("refused 10.0.0.1: it resolves to the non-public address 10.0.0.1",)

            def fetch(self, url):
                from sitewalk.facts import Page

                return Page(url=url, status=0, error="refused")

            def exists(self, url):
                return False

        result = crawl(Refusing(), "https://example.com", max_pages=1)
        report = findings.analyse(result)
        self.assertTrue(any("address guard" in note for note in report.notes))


if __name__ == "__main__":
    unittest.main()
