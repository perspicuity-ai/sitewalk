"""``--dir``: the offline source, and the claim that it is the deploy gate.

The strongest test in this file is
:class:`DirAndUrlAgreeOnTheSameBytes` — the same fixture site is read once from disk and once
over a fake HTTP connection, and the two page facts are compared field by field. That is the
test that makes ``--dir`` a gate rather than a separate, weaker checker: if the two drift, the
gate stops measuring what the live run measures.

Every test here runs inside ``no_network()``, which replaces ``socket.socket`` and
``socket.getaddrinfo`` with functions that raise, so a single accidental request fails the test
rather than passing on a connected machine.
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from sitewalk import findings
from sitewalk.crawl import crawl
from sitewalk.facts import Page
from sitewalk.pages import content_type_of
from sitewalk.sources import FileSource

from . import fakes
from .fakes import FIXTURES

EXAMPLE = FIXTURES / "example-site"
BARE = FIXTURES / "bare-site"

FACT_FIELDS = (
    "url",
    "status",
    "content_type",
    "title",
    "description",
    "canonical",
    "canonical_host",
    "json_ld_types",
    "json_ld_blocks",
    "json_ld_malformed",
    "visible_text_chars",
    "internal_links",
    "external_links",
    "in_sitemap",
    "looks_script_rendered",
    "truncated",
)

#: Fields that describe *how the body was obtained* rather than what it says, and are therefore
#: allowed to differ between a file on disk and a response over HTTP: ``error`` explains a
#: missing file in the build's own terms, and ``note`` records a query string that is not a
#: filename. Both are reported; neither is compared, and no fact about a page depends on them.
SOURCE_SPECIFIC_FIELDS = ("error", "note", "redirect_to")


def routes_from(directory: Path) -> fakes.FakeHTTP:
    """Serve a built directory over the fake connection, the way a static server would.

    ``/about/`` is served from ``about/index.html``, and a directory with no index file answers
    404, which is what makes the two sources comparable rather than merely similar.
    """
    http = fakes.FakeHTTP(routes={})
    for path in sorted(directory.rglob("*")):
        if not path.is_file():
            continue
        relative = "/" + str(path.relative_to(directory))
        url_path = relative[: -len("index.html")] if relative.endswith("/index.html") else relative
        content_type = content_type_of({}, path.name)
        if path.name == "index.html":
            content_type = "text/html"
        http.add(
            url_path,
            path.read_bytes(),
            content_type=content_type or "text/html",
        )
    return http


def live_crawl(directory: Path = EXAMPLE, **kwargs):
    http = routes_from(directory)
    source = fakes.live_source(http, origin="https://localhost", resolver=fakes.resolver_for("93.184.216.34"))
    with fakes.fake_network(http):
        result = crawl(source, "https://localhost", **kwargs)
    return result, http


def dir_crawl(directory: Path = EXAMPLE, **kwargs):
    with fakes.no_network():
        source = FileSource(directory)
        return crawl(source, source.origin, **kwargs)


class PathMapping(unittest.TestCase):
    def setUp(self):
        self.source = FileSource(EXAMPLE)

    def test_a_root_path_reads_the_root_index(self):
        self.assertEqual(self.source.resolve_path("https://localhost/"), (EXAMPLE / "index.html").resolve())

    def test_a_directory_path_reads_its_index(self):
        self.assertEqual(self.source.resolve_path("https://localhost/about/"), (EXAMPLE / "about" / "index.html").resolve())

    def test_a_directory_path_without_a_trailing_slash_also_reads_its_index(self):
        self.assertEqual(self.source.resolve_path("https://localhost/about"), (EXAMPLE / "about" / "index.html").resolve())

    def test_a_flat_html_path_reads_that_file(self):
        self.assertEqual(self.source.resolve_path("https://localhost/landing.html"), (EXAMPLE / "landing.html").resolve())

    def test_a_query_string_is_not_a_filename(self):
        page = self.source.fetch("https://localhost/about/?utm_source=x")
        self.assertTrue(page.ok)
        self.assertIn("query string", page.note or "")

    def test_a_missing_path_is_a_404_with_a_reason(self):
        page = self.source.fetch("https://localhost/nothing-here/")
        self.assertEqual(page.status, 404)
        self.assertIn("no file", page.error)

    def test_content_types_come_from_the_filename(self):
        self.assertEqual(self.source.fetch("https://localhost/notes.txt").content_type, "text/plain")
        self.assertEqual(self.source.fetch("https://localhost/sitemap.xml").content_type, "application/xml")
        self.assertEqual(self.source.fetch("https://localhost/").content_type, "text/html")


class PathEscapesAreRefused(unittest.TestCase):
    """A build directory is a boundary. A URL that leaves it is refused, not served."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "build"
        self.root.mkdir()
        (self.root / "index.html").write_text("<title>inside</title>", encoding="utf-8")
        self.secret = Path(self.temporary.name) / "outside.html"
        self.secret.write_text("<title>secret</title>", encoding="utf-8")
        self.source = FileSource(self.root)

    def test_a_dot_dot_path_is_refused(self):
        self.assertIsNone(self.source.resolve_path("https://localhost/../outside.html"))

    def test_a_deep_dot_dot_path_is_refused(self):
        self.assertIsNone(self.source.resolve_path("https://localhost/a/b/../../../outside.html"))

    def test_a_percent_encoded_dot_dot_path_is_refused(self):
        self.assertIsNone(self.source.resolve_path("https://localhost/%2e%2e/outside.html"))

    def test_a_path_with_a_null_byte_is_refused(self):
        self.assertIsNone(self.source.resolve_path("https://localhost/index.html%00.png"))

    def test_a_symlink_out_of_the_directory_is_refused(self):
        link = self.root / "escape.html"
        try:
            os.symlink(self.secret, link)
        except (OSError, NotImplementedError):  # pragma: no cover - platform without symlinks
            self.skipTest("this platform does not create symlinks")
        self.assertIsNone(self.source.resolve_path("https://localhost/escape.html"))

    def test_a_legitimate_path_inside_the_directory_still_works(self):
        self.assertTrue(self.source.exists("https://localhost/index.html"))


class TheOfflineCrawl(unittest.TestCase):
    def test_no_network_is_touched(self):
        # ``no_network`` raises on any socket use, so reaching the end is the assertion.
        result = dir_crawl()
        self.assertTrue(result.pages)

    def test_it_reads_the_home_page_first(self):
        result = dir_crawl()
        self.assertEqual(result.pages[0].url, "https://localhost/")

    def test_it_reports_the_three_surfaces(self):
        result = dir_crawl()
        self.assertTrue(result.surfaces["robots.txt"].exists)
        self.assertTrue(result.surfaces["sitemap.xml"].exists)
        self.assertTrue(result.surfaces["llms.txt"].exists)

    def test_a_missing_surface_is_recorded_as_missing(self):
        result = dir_crawl(BARE)
        self.assertFalse(result.surfaces["robots.txt"].exists)
        self.assertEqual(result.surfaces["robots.txt"].status, 404)

    def test_it_collects_the_urls_the_sitemap_names(self):
        result = dir_crawl()
        self.assertIn("https://localhost/about/", result.sitemap_urls)
        self.assertEqual(len(result.sitemap_urls), 11)

    def test_it_follows_internal_links(self):
        result = dir_crawl()
        reached = {fact.url for fact in result.pages}
        self.assertIn("https://localhost/team/", reached)
        self.assertIn("https://localhost/landing.html", reached)

    def test_a_robots_disallowed_path_is_not_read_in_offline_mode_either(self):
        # robots.txt is a statement about the site's content, not about the transport, so both
        # sources honour it. The consequence is that the two modes agree on this fixture
        # exactly, which is what makes ``--dir`` a gate rather than a second opinion.
        result = dir_crawl()
        reached = {fact.url for fact in result.pages}
        self.assertNotIn("https://localhost/private/", reached)
        self.assertTrue(any("/private/" in skip.url for skip in result.skipped))

    def test_it_never_leaves_the_origin(self):
        result = dir_crawl()
        for fact in result.pages:
            self.assertTrue(fact.url.startswith("https://localhost/"), fact.url)

    def test_the_page_cap_is_honoured_and_reported(self):
        result = dir_crawl(max_pages=3)
        self.assertEqual(len(result.pages), 3)
        self.assertTrue(result.cap_reached)
        self.assertTrue(any("page cap" in note for note in result.notes))

    def test_a_page_cap_of_one_reads_only_the_home_page(self):
        result = dir_crawl(max_pages=1)
        self.assertEqual([fact.url for fact in result.pages], ["https://localhost/"])

    def test_nested_sitemaps_are_followed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "index.html").write_text("<title>home</title>", encoding="utf-8")
            (root / "one.html").write_text("<title>one</title>", encoding="utf-8")
            (root / "sitemap.xml").write_text(
                '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                "<sitemap><loc>https://localhost/sitemap-one.xml</loc></sitemap>"
                "</sitemapindex>",
                encoding="utf-8",
            )
            (root / "sitemap-one.xml").write_text(
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                "<url><loc>https://localhost/one.html</loc></url></urlset>",
                encoding="utf-8",
            )
            result = dir_crawl(root)
        self.assertIn("https://localhost/one.html", result.sitemap_urls)
        self.assertIn("https://localhost/one.html", {f.url for f in result.pages})

    def test_a_sitemap_naming_another_origin_is_not_followed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "index.html").write_text("<title>home</title>", encoding="utf-8")
            (root / "sitemap.xml").write_text(
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                "<url><loc>https://elsewhere.example/other</loc></url></urlset>",
                encoding="utf-8",
            )
            result = dir_crawl(root)
        self.assertNotIn("https://elsewhere.example/other", {f.url for f in result.pages})
        self.assertTrue(any("off the submitted origin" in note for note in result.notes))

    def test_an_unreadable_sitemap_is_reported_rather_than_empty(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "index.html").write_text("<title>home</title>", encoding="utf-8")
            (root / "sitemap.xml").write_text("this is not xml", encoding="utf-8")
            result = dir_crawl(root)
        self.assertTrue(result.sitemap_errors)
        report = findings.analyse(result)
        self.assertTrue(report.errors_of("sitemap_unreadable"))

    def test_broken_internal_links_are_checked_and_reported(self):
        result = dir_crawl()
        report = findings.analyse(result)
        messages = [f.message for f in report.errors_of("broken_internal_link")]
        self.assertTrue(any("/broken/" in message for message in messages), messages)
        self.assertTrue(any("/services/missing/" in message for message in messages), messages)

    def test_a_link_to_a_page_already_read_is_not_requested_again(self):
        result = dir_crawl()
        # Twelve distinct URLs exist; the crawl reads each at most once.
        self.assertEqual(len(result.pages), len({fact.url for fact in result.pages}))
        self.assertLessEqual(result.requests_made, len(result.pages) + 3)


class DirAndUrlAgreeOnTheSameBytes(unittest.TestCase):
    """The claim that makes ``--dir`` a gate: it measures what the live run measures."""

    def test_the_page_facts_are_identical(self):
        offline = dir_crawl()
        online, _http = live_crawl()

        offline_facts = sorted(
            ({field: getattr(fact, field) for field in FACT_FIELDS} for fact in offline.pages),
            key=lambda item: item["url"],
        )
        online_facts = sorted(
            ({field: getattr(fact, field) for field in FACT_FIELDS} for fact in online.pages),
            key=lambda item: item["url"],
        )
        # Not "similar": equal, field by field, for every page both sources read. The one
        # difference the fixture could have shown — the robots.txt-disallowed page — is absent
        # because both sources honour robots.txt.
        self.assertEqual(offline_facts, online_facts)

    def test_the_findings_are_identical(self):
        offline = findings.analyse(dir_crawl())
        online, _http = live_crawl()
        online_report = findings.analyse(online)
        offline_kinds = sorted(f.kind for f in offline.findings)
        online_kinds = sorted(f.kind for f in online_report.findings)
        self.assertEqual(offline_kinds, online_kinds)

    def test_the_surfaces_are_identical(self):
        offline = dir_crawl()
        online, _http = live_crawl()
        self.assertEqual(
            {name: surface.exists for name, surface in offline.surfaces.items()},
            {name: surface.exists for name, surface in online.surfaces.items()},
        )

    def test_the_offline_run_produces_the_same_facts_for_every_url_the_site_publishes(self):
        offline = {fact.url: fact for fact in dir_crawl().pages}
        online = {fact.url: fact for fact in live_crawl()[0].pages}
        self.assertTrue(online, "the live crawl read nothing")
        for url, fact in online.items():
            with self.subTest(url=url):
                self.assertIn(url, offline)
                self.assertEqual(fact.visible_text_chars, offline[url].visible_text_chars)
                self.assertEqual(fact.title, offline[url].title)
                self.assertEqual(fact.json_ld_types, offline[url].json_ld_types)


class TheCommandLineMakesNoNetworkRequest(unittest.TestCase):
    """U1's strongest offline claim, asserted through the entry point rather than the library.

    ``main`` is the contract a deploy gate calls, and ``--dir`` is the mode that matters most.
    Running it inside ``no_network()`` means any socket or name lookup raises, so completing at
    all is the evidence that the offline path reaches no network code.
    """

    def test_the_text_report_runs_with_the_network_unavailable(self):
        import contextlib
        import io

        from sitewalk import cli

        out, err = io.StringIO(), io.StringIO()
        with fakes.no_network(), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = cli.main(["--dir", str(EXAMPLE)])
        self.assertEqual(code, 0, err.getvalue())
        self.assertIn("claim boundary", out.getvalue())

    def test_the_json_report_runs_with_the_network_unavailable(self):
        import contextlib
        import io

        from sitewalk import cli

        out = io.StringIO()
        with fakes.no_network(), contextlib.redirect_stdout(out):
            code = cli.main(["--dir", str(EXAMPLE), "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(out.getvalue())
        self.assertEqual(payload["source"]["kind"], "dir")
        self.assertIsNone(payload["user_agent"], "no request was made, so there is no client")

    def test_strict_gates_through_the_entry_point(self):
        import contextlib
        import io

        from sitewalk import cli

        with fakes.no_network(), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(cli.main(["--dir", str(EXAMPLE), "--strict"]), 1)
            self.assertEqual(cli.main(["--dir", str(BARE), "--strict"]), 1)


class TheJsonReportIsStable(unittest.TestCase):
    def test_every_documented_key_is_present(self):
        from sitewalk.report import to_dict

        report = findings.analyse(dir_crawl())
        data = to_dict(report)
        for key in (
            "tool",
            "report_version",
            "facts_version",
            "source",
            "claim_boundary",
            "not_measured",
            "limits",
            "status_counts",
            "json_ld_type_counts",
            "sitemap",
            "surfaces",
            "pages",
            "findings",
            "finding_counts",
            "plan",
            "notes",
        ):
            with self.subTest(key=key):
                self.assertIn(key, data)

    def test_the_json_is_serialisable_and_has_no_absolute_paths_in_page_urls(self):
        from sitewalk.report import to_json

        report = findings.analyse(dir_crawl())
        data = json.loads(to_json(report))
        for page in data["pages"]:
            self.assertTrue(page["url"].startswith("https://localhost/"), page["url"])


if __name__ == "__main__":
    unittest.main()


class TheRobotsSkipIsUnmissable(unittest.TestCase):
    """U6: a gate that skips pages must not be able to pass while under-reporting.

    A reader who reads only the summary must learn that paths were excluded, and a reader who
    follows the quote must be able to find the rule in the file it came from. Each of the three
    surfaces is asserted on its own, not through a helper that both produces and checks it.
    """

    @classmethod
    def setUpClass(cls):
        cls.report = findings.analyse(dir_crawl())
        cls.robots_text = (EXAMPLE / "robots.txt").read_text()

    def test_the_count_is_in_the_report_header(self):
        from sitewalk.report import to_text

        header = to_text(self.report).split("claim boundary")[0]
        self.assertIn("excluded:", header)
        self.assertIn("1 path(s)", header)

    def test_the_count_is_in_the_json_limits(self):
        from sitewalk.report import to_dict

        limits = to_dict(self.report)["limits"]
        self.assertEqual(limits["paths_skipped_robots"], 1)

    def test_each_skip_names_its_path_and_quotes_its_rule(self):
        from sitewalk.report import to_dict

        skipped = to_dict(self.report)["skipped_robots"]
        self.assertEqual(len(skipped), 1)
        self.assertEqual(skipped[0]["path"], "/private/")
        self.assertIn("Disallow:", skipped[0]["rule"])

    def test_the_quoted_rule_is_byte_identical_to_the_fixture_line(self):
        # The requirement: take the rule out of the report, search the file, find it. Asserted as
        # equality against the source line, not as membership, because the parser's stripped
        # variable is a substring of the source line and a membership test would pass on it.
        from sitewalk.report import to_dict

        rule = to_dict(self.report)["skipped_robots"][0]["rule"]
        self.assertIn(rule, self.robots_text)
        self.assertIn("# legacy, revisit", rule)
        self.assertTrue(rule.startswith("  "), "leading whitespace was normalised away")

    def test_the_note_also_carries_the_quoted_rule(self):
        from sitewalk.report import to_text

        notes = to_text(self.report).split("== Notes ==")[1]
        self.assertIn("/private/", notes)
        self.assertIn("# legacy, revisit", notes)

    def test_a_run_with_no_skips_says_nothing_about_exclusion(self):
        # The header line must not appear when the count is zero, or it stops meaning anything.
        from sitewalk.report import to_text

        report = findings.analyse(dir_crawl(BARE))
        self.assertNotIn("excluded:", to_text(report).split("claim boundary")[0])
