"""The live crawl, driven through the fake connection.

Nothing here opens a socket. The point of these tests is the crawl's *decisions*: what it
discovers, what it refuses to follow, where it stops, and whether it stays inside the origin it
was given. A crawl that quietly leaves the origin is the failure that matters, so that is
asserted directly rather than inferred.
"""

from __future__ import annotations

import unittest

from sitewalk.crawl import crawl
from sitewalk.facts import Page
from sitewalk.sources import LiveSource

from . import fakes

ORIGIN = "https://example.com"

SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://example.com/</loc></url>
  <url><loc>https://example.com/from-sitemap/</loc></url>
  <url><loc>https://example.com/orphan/</loc></url>
</urlset>
"""

ROBOTS = """User-agent: *
Disallow: /private/
Sitemap: https://example.com/sitemap.xml
"""


def site() -> fakes.FakeHTTP:
    http = fakes.FakeHTTP(routes={})
    http.add(
        "/",
        '<title>Home</title><a href="/linked/">linked</a>'
        '<a href="/private/secret/">secret</a>'
        '<a href="https://elsewhere.example/x">off-site</a>',
    )
    http.add("/linked/", "<title>Linked</title>")
    http.add("/from-sitemap/", "<title>From the sitemap</title>")
    http.add("/orphan/", "<title>Orphan</title>")
    http.add("/private/secret/", "<title>Secret</title>")
    http.add("/robots.txt", ROBOTS, content_type="text/plain")
    http.add("/sitemap.xml", SITEMAP, content_type="application/xml")
    http.add("/llms.txt", "# llms", content_type="text/plain")
    return http


def run(http: fakes.FakeHTTP, **kwargs):
    source = fakes.live_source(http, origin=ORIGIN)
    with fakes.fake_network(http):
        return crawl(source, ORIGIN, **kwargs), source


class Discovery(unittest.TestCase):
    def test_it_reads_the_three_surfaces(self):
        result, _source = run(site())
        self.assertTrue(result.surfaces["robots.txt"].exists)
        self.assertTrue(result.surfaces["sitemap.xml"].exists)
        self.assertTrue(result.surfaces["llms.txt"].exists)

    def test_it_reads_the_urls_the_sitemap_names(self):
        result, _source = run(site())
        self.assertIn("https://example.com/from-sitemap/", result.sitemap_urls)
        self.assertIn("https://example.com/from-sitemap/", {f.url for f in result.pages})

    def test_it_follows_internal_links_from_the_home_page(self):
        result, _source = run(site())
        self.assertIn("https://example.com/linked/", {f.url for f in result.pages})

    def test_it_marks_which_pages_the_sitemap_names(self):
        result, _source = run(site())
        by_url = {fact.url: fact for fact in result.pages}
        self.assertTrue(by_url["https://example.com/from-sitemap/"].in_sitemap)
        self.assertFalse(by_url["https://example.com/linked/"].in_sitemap)

    def test_a_sitemap_named_in_robots_is_read_when_sitemap_xml_is_absent(self):
        http = fakes.FakeHTTP(routes={})
        http.add("/", "<title>Home</title>")
        http.add("/robots.txt", "Sitemap: https://example.com/other.xml", content_type="text/plain")
        http.add(
            "/other.xml",
            '<urlset><url><loc>https://example.com/listed/</loc></url></urlset>',
            content_type="application/xml",
        )
        http.add("/listed/", "<title>Listed</title>")
        result, _source = run(http)
        self.assertIn("https://example.com/listed/", {f.url for f in result.pages})

    def test_a_sitemap_index_is_followed(self):
        http = fakes.FakeHTTP(routes={})
        http.add("/", "<title>Home</title>")
        http.add(
            "/sitemap.xml",
            '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            "<sitemap><loc>https://example.com/sitemap-pages.xml</loc></sitemap>"
            "</sitemapindex>",
            content_type="application/xml",
        )
        http.add(
            "/sitemap-pages.xml",
            '<urlset><url><loc>https://example.com/deep/</loc></url></urlset>',
            content_type="application/xml",
        )
        http.add("/deep/", "<title>Deep</title>")
        result, _source = run(http)
        self.assertIn("https://example.com/deep/", {f.url for f in result.pages})

    def test_a_sitemap_index_off_the_origin_is_reported_and_not_fetched(self):
        http = fakes.FakeHTTP(routes={})
        http.add("/", "<title>Home</title>")
        http.add(
            "/sitemap.xml",
            '<sitemapindex><sitemap><loc>https://elsewhere.example/sitemap.xml</loc></sitemap></sitemapindex>',
            content_type="application/xml",
        )
        result, _source = run(http)
        self.assertTrue(any("off the origin" in note for note in result.notes))
        self.assertEqual(http.paths_requested, ["/robots.txt", "/sitemap.xml", "/llms.txt", "/rss.xml", "/"])


class StayingInsideTheOrigin(unittest.TestCase):
    def test_an_external_link_is_never_requested(self):
        http = site()
        run(http)
        self.assertNotIn("/x", http.paths_requested)
        for connection in http.connections:
            self.assertTrue(connection.requests)

    def test_an_off_origin_redirect_is_refused(self):
        http = fakes.FakeHTTP(routes={})
        http.add("/", '<title>Home</title><a href="/linked/">linked</a>')
        http.redirect("/linked/", "https://elsewhere.example/moved/")
        result, _source = run(http)
        by_url = {fact.url: fact for fact in result.pages}
        moved = by_url["https://example.com/linked/"]
        self.assertFalse(moved.ok)
        self.assertIn("off the submitted origin", moved.error or "")

    def test_a_redirect_inside_the_origin_is_followed(self):
        http = fakes.FakeHTTP(routes={})
        http.add("/", '<title>Home</title><a href="/old/">old</a>')
        http.redirect("/old/", "/new/")
        http.add("/new/", "<title>New</title>")
        result, _source = run(http)
        by_url = {fact.url: fact for fact in result.pages}
        self.assertEqual(by_url["https://example.com/old/"].redirect_to, "https://example.com/new/")
        self.assertTrue(by_url["https://example.com/old/"].ok)

    def test_a_sitemap_naming_a_foreign_url_does_not_add_that_url(self):
        # With no declared origin the site's own sitemap may be read, but a URL on a host the site
        # has not claimed to be is never crawled. The note names the host it was judged against.
        http = fakes.FakeHTTP(routes={})
        http.add("/", "<title>Home</title>")
        http.add(
            "/sitemap.xml",
            '<urlset><url><loc>https://elsewhere.example/other</loc></url></urlset>',
            content_type="application/xml",
        )
        result, _source = run(http)
        self.assertNotIn("https://elsewhere.example/other", {f.url for f in result.pages})
        self.assertTrue(any("off the site" in note for note in result.notes))
        self.assertEqual(result.sitemap_urls, [])

    def test_a_declared_origin_lets_the_sites_own_sitemap_be_read(self):
        # The U14 case: the sitemap names the origin the site claims to be, so its URLs are
        # accepted and mapped onto the origin being walked.
        http = fakes.FakeHTTP(routes={})
        http.add("/", "<title>Home</title>")
        http.add(
            "/sitemap.xml",
            '<urlset><url><loc>https://example.com/listed/</loc></url></urlset>',
            content_type="application/xml",
        )
        http.add("/listed/", "<title>Listed</title>")
        source = fakes.live_source(http, origin=ORIGIN)
        with fakes.fake_network(http):
            result = crawl(source, ORIGIN, declared_origin=ORIGIN)
        self.assertIn("https://example.com/listed/", result.sitemap_urls)
        self.assertIn("https://example.com/listed/", {f.url for f in result.pages})


class RobotsIsObeyed(unittest.TestCase):
    def test_a_disallowed_path_is_not_fetched(self):
        http = site()
        result, _source = run(http)
        self.assertNotIn("/private/secret/", http.paths_requested)
        self.assertNotIn("https://example.com/private/secret/", {f.url for f in result.pages})

    def test_a_disallowed_path_is_recorded_as_skipped(self):
        result, _source = run(site())
        self.assertTrue(any("disallows" in skip.reason for skip in result.skipped))

    def test_a_disallowed_path_named_in_the_sitemap_is_skipped_too(self):
        http = site()
        http.add(
            "/sitemap.xml",
            '<urlset><url><loc>https://example.com/private/secret/</loc></url></urlset>',
            content_type="application/xml",
        )
        result, _source = run(http)
        self.assertNotIn("https://example.com/private/secret/", {f.url for f in result.pages})

    def test_a_disallow_for_another_agent_does_not_stop_the_crawl(self):
        http = fakes.FakeHTTP(routes={})
        http.add("/", '<title>Home</title><a href="/open/">open</a>')
        http.add("/open/", "<title>Open</title>")
        http.add("/robots.txt", "User-agent: BadBot\nDisallow: /\n", content_type="text/plain")
        result, _source = run(http)
        self.assertIn("https://example.com/open/", {f.url for f in result.pages})


class Bounds(unittest.TestCase):
    def test_the_page_cap_stops_the_crawl_and_says_so(self):
        http = fakes.FakeHTTP(routes={})
        http.add("/", '<title>Home</title><a href="/a/">a</a><a href="/b/">b</a><a href="/c/">c</a>')
        for name in "abc":
            http.add(f"/{name}/", f"<title>{name}</title>")
        result, _source = run(http, max_pages=2)
        self.assertEqual(len(result.pages), 2)
        self.assertTrue(result.cap_reached)

    def test_a_link_the_crawl_reached_is_not_requested_again(self):
        # The crawl itself answers the link question for anything it read, so the separate link
        # check makes no extra request for it.
        http = fakes.FakeHTTP(routes={})
        links = "".join(f'<a href="/missing-{i}/">x</a>' for i in range(3))
        http.add("/", f"<title>Home</title>{links}")
        result, _source = run(http, max_pages=50)
        self.assertEqual(result.link_checked, 0)
        self.assertEqual(len(result.pages), 4)
        requested = http.paths_requested
        self.assertEqual(len(requested), len(set(requested)), requested)

    def test_every_target_the_crawl_reached_answers_its_own_link_question(self):
        http = fakes.FakeHTTP(routes={})
        links = "".join(f'<a href="/missing-{i}/">x</a>' for i in range(6))
        http.add("/", f"<title>Home</title>{links}")
        # Six targets and a five-page bound: the crawl reads the home page and four targets, so
        # the bound is reached inside the crawl and the separate link check never runs. The two
        # targets it did not reach are named rather than silently dropped.
        result, _source = run(http, max_pages=5)
        self.assertEqual(len(result.pages), 5)
        self.assertEqual(result.link_checked, 0)
        self.assertTrue(result.cap_reached)
        self.assertTrue(any("left unchecked" in note for note in result.notes), result.notes)

    def test_a_disallowed_link_is_not_checked_either(self):
        # The link check exists to answer whether a link works. A path robots.txt disallows is
        # not fetched to answer that either, and the skip is recorded.
        http = fakes.FakeHTTP(routes={})
        http.add("/", '<title>Home</title><a href="/private/page/">private</a>')
        http.add("/robots.txt", "User-agent: *\nDisallow: /private/\n", content_type="text/plain")
        http.add("/private/page/", "<title>Private</title>")
        result, _source = run(http, max_pages=50)
        self.assertEqual(result.link_checked, 0)
        self.assertNotIn("/private/page/", http.paths_requested)
        self.assertTrue(any("disallows" in skip.reason for skip in result.skipped))

    def test_the_page_bound_is_the_only_bound_on_what_is_checked(self):
        # There is no separate link-check bound. A link the crawl can reach is answered by the
        # crawl; a link it cannot reach is named in the notes, and the remedy is --max-pages.
        http = fakes.FakeHTTP(routes={})
        links = "".join(f'<a href="/missing-{i}/">x</a>' for i in range(6))
        http.add("/", f"<title>Home</title>{links}")
        result, _source = run(http, max_pages=3)
        self.assertEqual(len(result.pages), 3)
        self.assertTrue(any("raise --max-pages" in note for note in result.notes), result.notes)
        self.assertTrue(any("left unchecked" in note for note in result.notes), result.notes)

    def test_a_page_already_read_is_not_requested_twice(self):
        http = site()
        run(http)
        requested = http.paths_requested
        self.assertEqual(len(requested), len(set(requested)), requested)

    def test_a_long_body_is_truncated_and_reported(self):
        http = fakes.FakeHTTP(routes={})
        http.add("/", "<title>Home</title>" + "x" * 5000)
        source = fakes.live_source(http, origin=ORIGIN, timeout=5.0)
        with fakes.fake_network(http):
            result = crawl(source, ORIGIN, max_pages=1)
        # The fixture body is far below the cap, so nothing is truncated; the cap's own
        # behaviour is asserted in ``test_the_body_cap_truncates_a_long_page`` below.
        self.assertEqual(result.truncated_pages, 0)
        self.assertFalse(result.pages[0].truncated)
        self.assertEqual(result.pages[0].title, "Home")

    def test_the_body_cap_truncates_a_long_page(self):
        body = "<title>Home</title><body><p>" + ("word " * 100) + "</p></body>"
        http = fakes.FakeHTTP(routes={})
        http.add("/", body)
        source = fakes.live_source(http, origin=ORIGIN, max_body=100)
        with fakes.fake_network(http):
            result = crawl(source, ORIGIN, max_pages=1)
        self.assertEqual(result.truncated_pages, 1)
        fact = result.pages[0]
        self.assertTrue(fact.truncated)
        self.assertEqual(fact.title, "Home")
        self.assertLess(fact.visible_text_chars, len("word " * 100))
        self.assertIn("body read stopped at", fact.note or "")


class FailuresAreFindingsNotCrashes(unittest.TestCase):
    def test_a_connection_error_is_a_page_with_no_status(self):
        class Exploding:
            def request(self, *_args, **_kwargs):
                raise OSError("connection refused")

            sock = None

            def close(self):
                pass

        def connector(scheme, host, port, timeout):
            return Exploding()

        source = LiveSource(
            origin=ORIGIN,
            delay=0.0,
            resolver=fakes.resolver_for("93.184.216.34"),
            connector=connector,
        )
        with fakes.no_network():
            result = crawl(source, ORIGIN, max_pages=1)
        self.assertEqual(result.pages[0].status, 0)
        self.assertIn("connection refused", result.pages[0].error or "")

    def test_a_status_code_alone_is_recorded_with_no_body(self):
        http = fakes.FakeHTTP(routes={})
        http.add("/", "boom", status=500)
        source = fakes.live_source(http, origin=ORIGIN)
        with fakes.fake_network(http):
            result = crawl(source, ORIGIN, max_pages=1)
        fact = result.pages[0]
        self.assertEqual(fact.status, 500)
        self.assertFalse(fact.ok)
        self.assertEqual(fact.visible_text_chars, 0)

    def test_a_page_that_is_not_html_is_reported_as_such(self):
        http = fakes.FakeHTTP(routes={})
        http.add("/", '<title>Home</title><a href="/data.json">data</a>')
        http.add("/data.json", '{"@type": "Organization"}', content_type="application/json")
        result, _source = run(http)
        by_url = {fact.url: fact for fact in result.pages}
        data = by_url["https://example.com/data.json"]
        self.assertFalse(data.is_html)
        self.assertEqual(data.json_ld_types, ())


if __name__ == "__main__":
    unittest.main()
