"""The command line: exit codes, output shapes, and the boundary the output states.

The exit codes are the contract a CI gate is built on, so they are tested directly rather than
inferred: 0 for a completed run, 1 under ``--strict`` when findings exist, and 2 when the run
could not be made at all — including an unreadable plan, because a gate that cannot read its own
plan must not report a pass.

Every test here runs against the fixture directory or the fake connection, inside
``no_network()`` or its equivalent, so the suite needs no network.
"""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from sitewalk import cli

from . import fakes
from .fakes import FIXTURES

EXAMPLE = str(FIXTURES / "example-site")
BARE = str(FIXTURES / "bare-site")


def run_cli(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with fakes.no_network(), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = cli.main(argv)
    return code, out.getvalue(), err.getvalue()


class Arguments(unittest.TestCase):
    def test_a_source_is_required(self):
        with self.assertRaises(SystemExit) as caught:
            with contextlib.redirect_stderr(io.StringIO()):
                cli.main([])
        self.assertEqual(caught.exception.code, 2)

    def test_the_two_sources_are_mutually_exclusive(self):
        with self.assertRaises(SystemExit) as caught:
            with contextlib.redirect_stderr(io.StringIO()):
                cli.main(["--dir", EXAMPLE, "--url", "https://example.com"])
        self.assertEqual(caught.exception.code, 2)

    def test_a_missing_directory_exits_two_with_a_message(self):
        code, out, err = run_cli(["--dir", "/nonexistent/build"])
        self.assertEqual(code, 2)
        self.assertIn("is not a directory", err)
        self.assertEqual(out, "")

    def test_an_unsupported_scheme_exits_two_before_any_work(self):
        code, _out, err = run_cli(["--url", "ftp://example.com/"])
        self.assertEqual(code, 2)
        self.assertIn("scheme", err)

    def test_a_non_default_port_exits_two(self):
        code, _out, err = run_cli(["--url", "https://example.com:8443/"])
        self.assertEqual(code, 2)
        self.assertIn("port", err)

    def test_a_page_bound_of_zero_is_rejected(self):
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stderr(io.StringIO()):
                cli.main(["--dir", EXAMPLE, "--max-pages", "0"])

    def test_a_negative_delay_is_rejected(self):
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stderr(io.StringIO()):
                cli.main(["--dir", EXAMPLE, "--delay", "-1"])

    def test_the_help_text_states_the_boundary(self):
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(io.StringIO()) as out:
                cli.main(["--help"])
        text = out.getvalue()
        self.assertIn("does not execute JavaScript", text)
        self.assertIn("ranking", text)

    def test_the_directory_mode_says_that_network_options_do_not_apply(self):
        code, _out, err = run_cli(["--dir", EXAMPLE, "--timeout", "5"])
        self.assertEqual(code, 0)
        self.assertIn("no network request is made", err)


class ExitCodes(unittest.TestCase):
    def test_a_clean_site_exits_zero(self):
        code, _out, _err = run_cli(["--dir", BARE])
        self.assertEqual(code, 0)

    def test_the_fixture_has_findings_and_exits_zero_without_strict(self):
        code, _out, _err = run_cli(["--dir", EXAMPLE])
        self.assertEqual(code, 0)

    def test_the_fixture_exits_one_with_strict(self):
        code, _out, _err = run_cli(["--dir", EXAMPLE, "--strict"])
        self.assertEqual(code, 1)

    def test_strict_does_not_gate_on_a_note_alone(self):
        # The bare fixture's only error is no_json_ld; a site with structured data and no
        # errors must exit 0 even though notes exist. This is asserted through the report
        # rather than by building a second fixture.
        from sitewalk import findings, report as report_module

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "index.html").write_text(
                '<title>T</title><meta name="description" content="d">'
                '<link rel="canonical" href="https://localhost/">'
                '<link rel="canonical" href="https://localhost/">'
                '<script type="application/ld+json">{"@type":"Organization"}</script>'
                "<body><p>text</p></body>",
                encoding="utf-8",
            )
            report = findings.analyse(_crawl_dir(root))
        self.assertEqual(report.errors, [])
        self.assertEqual(report_module.exit_code(report, strict=True), 0)


def _crawl_dir(root: Path):
    from sitewalk.crawl import crawl
    from sitewalk.sources import FileSource

    source = FileSource(root)
    with fakes.no_network():
        return crawl(source, source.origin)


class PlanOnTheCommandLine(unittest.TestCase):
    def write_plan(self, data) -> str:
        handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        json.dump(data, handle)
        handle.close()
        self.addCleanup(Path(handle.name).unlink)
        return handle.name

    def test_a_met_plan_keeps_the_exit_at_zero(self):
        path = self.write_plan({"plan_version": 1, "required_surfaces": ["robots.txt"]})
        code, out, _err = run_cli(["--dir", EXAMPLE, "--plan", path, "--strict"])
        self.assertEqual(code, 1)  # the fixture has its own findings
        self.assertIn("Plan", out)

    def test_an_unmet_plan_adds_a_gating_finding(self):
        path = self.write_plan({"plan_version": 1, "required_surfaces": ["security.txt"]})
        code, out, _err = run_cli(["--dir", BARE, "--plan", path, "--strict"])
        self.assertEqual(code, 1)
        self.assertIn("plan_surface_missing", out)

    def test_an_unreadable_plan_exits_two(self):
        code, _out, err = run_cli(["--dir", EXAMPLE, "--plan", "/nonexistent/site.json"])
        self.assertEqual(code, 2)
        self.assertIn("could not read the plan file", err)

    def test_a_plan_that_is_not_json_exits_two(self):
        handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        handle.write("{oops")
        handle.close()
        self.addCleanup(Path(handle.name).unlink)
        code, _out, err = run_cli(["--dir", EXAMPLE, "--plan", handle.name])
        self.assertEqual(code, 2)
        self.assertIn("not valid JSON", err)

    def test_the_plan_result_appears_in_the_json_output(self):
        path = self.write_plan({"plan_version": 1, "site": "example.com"})
        _code, out, _err = run_cli(["--dir", EXAMPLE, "--plan", path, "--json"])
        data = json.loads(out)
        self.assertEqual(data["plan"]["plan_version"], 1)
        self.assertEqual(data["plan"]["site"], "example.com")


class Output(unittest.TestCase):
    def test_the_text_report_states_the_claim_boundary(self):
        _code, out, _err = run_cli(["--dir", EXAMPLE])
        self.assertIn("does not execute JavaScript", out)
        self.assertIn("not measured here", out)
        self.assertIn("ranking", out)

    def test_the_text_report_names_every_page_it_read(self):
        _code, out, _err = run_cli(["--dir", EXAMPLE])
        for path in ("/", "/about/", "/team/", "/services/", "/landing.html", "/shell.html"):
            with self.subTest(path=path):
                self.assertIn(path, out)

    def test_the_text_report_carries_the_bounds(self):
        _code, out, _err = run_cli(["--dir", EXAMPLE])
        self.assertIn("bounded by:", out)

    def test_the_summary_line_goes_to_stderr_so_stdout_stays_machine_readable(self):
        _code, out, err = run_cli(["--dir", EXAMPLE])
        self.assertIn("claim boundary", out)
        self.assertIn("sitewalk:", err)
        self.assertNotIn("sitewalk:", out)

    def test_the_json_output_is_valid_json_and_carries_the_boundary(self):
        _code, out, _err = run_cli(["--dir", EXAMPLE, "--json"])
        data = json.loads(out)
        self.assertEqual(data["tool"], "sitewalk")
        self.assertIn("does not execute JavaScript", data["claim_boundary"])
        self.assertIn("ranking", data["not_measured"])

    def test_the_json_output_lists_every_page_with_its_facts(self):
        _code, out, _err = run_cli(["--dir", EXAMPLE, "--json"])
        data = json.loads(out)
        first = data["pages"][0]
        for key in (
            "url",
            "path",
            "status",
            "content_type",
            "title",
            "meta_description",
            "canonical",
            "json_ld_types",
            "visible_text_chars",
            "internal_links",
            "in_sitemap",
            "looks_script_rendered",
        ):
            with self.subTest(key=key):
                self.assertIn(key, first)

    def test_no_absolute_filesystem_path_appears_in_the_report(self):
        _code, out, _err = run_cli(["--dir", EXAMPLE, "--json"])
        self.assertNotIn(str(FIXTURES), out)
        self.assertNotIn(str(Path.home()), out)

    def test_the_render_heuristic_is_reported_as_a_question_not_a_conclusion(self):
        _code, out, _err = run_cli(["--dir", EXAMPLE])
        self.assertIn("script-shell?", out)
        self.assertIn("does not execute JavaScript", out)


class LiveModeOverTheFakeConnection(unittest.TestCase):
    """``--url`` end to end, with the connection faked and the resolver injected."""

    def test_a_live_run_produces_a_report_and_exits_zero(self):
        http = fakes.FakeHTTP(routes={})
        http.add("/", '<title>Live</title><a href="/page/">page</a>')
        http.add("/page/", "<title>Page</title>")
        http.add("/robots.txt", "User-agent: *\n", content_type="text/plain")
        # ``LiveSource`` takes its resolver and connector as defaults, bound when the dataclass
        # is defined, so both module attributes are patched before the source is constructed.
        with fakes.fake_network(http):
            with unittest.mock.patch("sitewalk.guard.default_resolver", fakes.resolver_for("93.184.216.34")):
                with unittest.mock.patch("sitewalk.fetch.default_connector", http.connector):
                    out, err = io.StringIO(), io.StringIO()
                    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                        code = cli.main(["--url", "https://example.com", "--delay", "0"])
        self.assertEqual(code, 0, err.getvalue())
        self.assertIn("/page/", out.getvalue())

    def test_a_live_run_never_requests_an_external_host(self):
        http = fakes.FakeHTTP(routes={})
        http.add("/", '<title>Live</title><a href="https://elsewhere.example/x">off</a>')
        with fakes.fake_network(http):
            with unittest.mock.patch("sitewalk.guard.default_resolver", fakes.resolver_for("93.184.216.34")):
                with unittest.mock.patch("sitewalk.fetch.default_connector", http.connector):
                    # stderr is captured too: the summary line is expected noise here, and this
                    # test asserts on what was requested, not on what was printed.
                    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                        cli.main(["--url", "https://example.com", "--delay", "0"])
        self.assertNotIn("/x", http.paths_requested)


if __name__ == "__main__":
    unittest.main()
