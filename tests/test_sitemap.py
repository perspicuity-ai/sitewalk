"""``robots.txt`` and ``sitemap.xml`` reading.

These are the two files a site publishes to describe itself to machines, and getting them wrong
is silent: an unread sitemap contributes no URLs and looks like a site with no sitemap. So the
unreadable cases are asserted as errors, not as empty results.
"""

from __future__ import annotations

import unittest

from sitewalk.sitemap import is_disallowed, parse_robots, parse_sitemap

URLSET = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://example.com/</loc><lastmod>2026-01-01</lastmod></url>
  <url><loc>https://example.com/about/</loc><priority>0.8</priority></url>
</urlset>
"""

INDEX = """<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>https://example.com/sitemap-pages.xml</loc></sitemap>
  <sitemap><loc>https://example.com/sitemap-posts.xml</loc></sitemap>
</sitemapindex>
"""


class SitemapUrls(unittest.TestCase):
    def test_reads_the_urls_from_a_urlset(self):
        result = parse_sitemap(URLSET)
        self.assertEqual(
            result.urls, ["https://example.com/", "https://example.com/about/"]
        )
        self.assertEqual(result.errors, [])

    def test_reads_a_sitemap_with_no_namespace(self):
        text = '<urlset><url><loc>https://example.com/a</loc></url></urlset>'
        self.assertEqual(parse_sitemap(text).urls, ["https://example.com/a"])

    def test_reads_a_sitemap_in_an_unexpected_namespace(self):
        text = (
            '<urlset xmlns="https://example.invalid/ns">'
            "<url><loc>https://example.com/a</loc></url></urlset>"
        )
        self.assertEqual(parse_sitemap(text).urls, ["https://example.com/a"])

    def test_reads_the_sitemaps_from_an_index(self):
        result = parse_sitemap(INDEX)
        self.assertEqual(
            result.nested,
            ["https://example.com/sitemap-pages.xml", "https://example.com/sitemap-posts.xml"],
        )
        self.assertEqual(result.urls, [])

    def test_deduplicates_urls(self):
        text = (
            "<urlset><url><loc>https://example.com/a</loc></url>"
            "<url><loc>https://example.com/a</loc></url></urlset>"
        )
        self.assertEqual(parse_sitemap(text).urls, ["https://example.com/a"])

    def test_ignores_an_entry_with_no_location(self):
        text = "<urlset><url><lastmod>2026-01-01</lastmod></url></urlset>"
        self.assertEqual(parse_sitemap(text).urls, [])

    def test_an_empty_document_is_reported(self):
        self.assertTrue(parse_sitemap("   ").errors)

    def test_a_document_that_is_not_xml_is_reported(self):
        result = parse_sitemap("<!doctype html><html><body>Not a sitemap</body></html>")
        self.assertTrue(result.errors)
        self.assertEqual(result.urls, [])

    def test_a_wrong_root_element_is_reported_but_still_read(self):
        text = "<rss><url><loc>https://example.com/a</loc></url></rss>"
        result = parse_sitemap(text)
        self.assertEqual(result.urls, ["https://example.com/a"])
        self.assertTrue(any("urlset" in message for message in result.errors))


class Robots(unittest.TestCase):
    def test_reads_sitemap_lines(self):
        text = "User-agent: *\nDisallow: /private/\nSitemap: https://example.com/sitemap.xml\n"
        sitemaps, disallowed = parse_robots(text)
        self.assertEqual(sitemaps, ["https://example.com/sitemap.xml"])
        self.assertEqual(disallowed, ["/private/"])

    def test_reads_a_sitemap_line_that_is_not_in_a_group(self):
        sitemaps, _ = parse_robots("Sitemap: https://example.com/sitemap.xml")
        self.assertEqual(sitemaps, ["https://example.com/sitemap.xml"])

    def test_ignores_comments_and_blank_lines(self):
        text = "# a comment\n\nSitemap: https://example.com/sitemap.xml # trailing\n"
        sitemaps, _ = parse_robots(text)
        self.assertEqual(sitemaps, ["https://example.com/sitemap.xml"])

    def test_a_disallow_for_another_agent_does_not_apply_to_us(self):
        text = "User-agent: BadBot\nDisallow: /\n\nUser-agent: *\nDisallow: /admin/\n"
        _sitemaps, disallowed = parse_robots(text)
        self.assertEqual(disallowed, ["/admin/"])

    def test_a_disallow_for_our_own_name_applies(self):
        text = "User-agent: sitewalk\nDisallow: /no-crawl/\n"
        _sitemaps, disallowed = parse_robots(text)
        self.assertEqual(disallowed, ["/no-crawl/"])

    def test_crawl_delay_is_not_a_sitemap_or_a_disallow(self):
        sitemaps, disallowed = parse_robots("User-agent: *\nCrawl-delay: 10\n")
        self.assertEqual((sitemaps, disallowed), ([], []))

    def test_an_empty_disallow_means_nothing_is_disallowed(self):
        _sitemaps, disallowed = parse_robots("User-agent: *\nDisallow:\n")
        self.assertEqual(disallowed, [])

    def test_headers_are_case_insensitive(self):
        sitemaps, disallowed = parse_robots("USER-AGENT: *\nDISALLOW: /x/\nSITEMAP: https://e.com/s.xml")
        self.assertEqual(sitemaps, ["https://e.com/s.xml"])
        self.assertEqual(disallowed, ["/x/"])


class DisallowMatching(unittest.TestCase):
    def test_a_prefix_match_is_disallowed(self):
        self.assertTrue(is_disallowed("/private/page/", ["/private/"]))

    def test_an_unrelated_path_is_allowed(self):
        self.assertFalse(is_disallowed("/public/", ["/private/"]))

    def test_a_root_disallow_covers_everything(self):
        self.assertTrue(is_disallowed("/anything", ["/"]))

    def test_no_rules_means_nothing_is_disallowed(self):
        self.assertFalse(is_disallowed("/anything", []))


if __name__ == "__main__":
    unittest.main()
