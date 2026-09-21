"""What one page exposes, read with ``html.parser``.

The parser is the part most likely to be quietly wrong: a regex or a naive scanner would pick up
a ``<title>`` inside a comment, mis-handle an unclosed tag, or swallow the rest of the document
after a self-closing ``<script/>``. These tests pin those cases, and they pin the script-shell
heuristic at its thresholds, because a heuristic whose boundary is not tested is a heuristic
nobody can safely change.
"""

from __future__ import annotations

import unittest

from sitewalk.facts import Page
from sitewalk.pages import (
    SCRIPT_SHELL_SCRIPT_BYTES,
    SCRIPT_SHELL_TEXT_CHARS,
    extract_json_ld_types,
    facts_from,
    looks_like_a_script_shell,
)

ORIGIN = "https://example.com/"


def page(body: str, url: str = ORIGIN, content_type: str = "text/html", status: int = 200) -> Page:
    return Page(url=url, status=status, content_type=content_type, body=body)


def facts(body: str, url: str = ORIGIN, content_type: str = "text/html"):
    return facts_from(page(body, url=url, content_type=content_type), in_sitemap=False)


class TitleAndDescription(unittest.TestCase):
    def test_reads_the_title(self):
        self.assertEqual(facts("<html><head><title>Hello</title></head></html>").title, "Hello")

    def test_collapses_whitespace_in_the_title(self):
        self.assertEqual(
            facts("<title>\n  Hello\n   there \n</title>").title, "Hello there"
        )

    def test_an_absent_title_is_none_and_an_empty_one_is_empty(self):
        self.assertIsNone(facts("<html><head></head><body>x</body></html>").title)
        self.assertEqual(facts("<html><head><title></title></head></html>").title, "")

    def test_a_title_inside_a_comment_is_not_the_title(self):
        body = "<html><head><!-- <title>Not this one</title> --><title>The real one</title></head></html>"
        self.assertEqual(facts(body).title, "The real one")

    def test_a_title_in_the_body_is_still_read(self):
        # Invalid HTML, but a browser raises it to the head; reporting None here would say the
        # page has no title, which is not what a reader would see.
        self.assertEqual(facts("<body><h1>x</h1><title>Late</title></body>").title, "Late")

    def test_reads_the_meta_description(self):
        body = '<meta name="description" content="A description.">'
        self.assertEqual(facts(body).description, "A description.")

    def test_ignores_other_meta_names(self):
        body = '<meta name="twitter:description" content="Not this."><meta name="description" content="This.">'
        self.assertEqual(facts(body).description, "This.")

    def test_an_empty_meta_description_is_empty_not_absent(self):
        body = '<meta name="description" content="">'
        self.assertEqual(facts(body).description, "")

    def test_a_meta_with_no_content_attribute_is_not_a_description(self):
        self.assertIsNone(facts('<meta name="description">').description)


class Canonical(unittest.TestCase):
    def test_reads_a_root_relative_canonical_as_an_absolute_url(self):
        body = '<link rel="canonical" href="/about/">'
        fact = facts(body, url="https://example.com/about/us/")
        self.assertEqual(fact.canonical, "https://example.com/about/")
        self.assertEqual(fact.canonical_host, "example.com")

    def test_records_a_canonical_on_another_host(self):
        body = '<link rel="canonical" href="https://elsewhere.example/page/">'
        fact = facts(body)
        self.assertEqual(fact.canonical_host, "elsewhere.example")

    def test_drops_the_fragment_from_a_canonical(self):
        body = '<link rel="canonical" href="https://example.com/page/#section">'
        self.assertEqual(facts(body).canonical, "https://example.com/page/")

    def test_an_absent_canonical_is_none(self):
        self.assertIsNone(facts("<html><head></head></html>").canonical)

    def test_the_first_canonical_wins(self):
        body = '<link rel="canonical" href="/one/"><link rel="canonical" href="/two/">'
        self.assertEqual(facts(body).canonical, "https://example.com/one/")


class JsonLd(unittest.TestCase):
    def test_reads_a_type_from_a_single_object(self):
        body = '<script type="application/ld+json">{"@type": "Organization"}</script>'
        self.assertEqual(facts(body).json_ld_types, ("Organization",))

    def test_reads_a_list_of_types(self):
        body = '<script type="application/ld+json">{"@type": ["WebSite", "LocalBusiness"]}</script>'
        self.assertEqual(facts(body).json_ld_types, ("WebSite", "LocalBusiness"))

    def test_walks_a_graph(self):
        body = (
            '<script type="application/ld+json">'
            '{"@context": "https://schema.org", "@graph": ['
            '{"@type": "Organization"}, {"@type": "Service"}]}</script>'
        )
        self.assertEqual(facts(body).json_ld_types, ("Organization", "Service"))

    def test_walks_nested_objects_and_deduplicates(self):
        body = (
            '<script type="application/ld+json">'
            '{"@type": "Product", "brand": {"@type": "Organization"}, '
            '"offers": {"@type": "Offer"}}</script>'
        )
        self.assertEqual(facts(body).json_ld_types, ("Product", "Organization", "Offer"))

    def test_reads_a_top_level_list(self):
        body = '<script type="application/ld+json">[{"@type": "A"}, {"@type": "B"}]</script>'
        self.assertEqual(facts(body).json_ld_types, ("A", "B"))

    def test_a_malformed_block_is_counted_and_does_not_stop_the_page(self):
        body = (
            '<title>Still read</title>'
            '<script type="application/ld+json">{"@type": "Broken",}</script>'
            '<script type="application/ld+json">{"@type": "Fine"}</script>'
        )
        fact = facts(body)
        self.assertEqual(fact.title, "Still read")
        self.assertEqual(fact.json_ld_types, ("Fine",))
        # Both blocks are present; one of them does not parse. The two counts answer different
        # questions, so a page with one broken block is not reported as having no JSON-LD.
        self.assertEqual(fact.json_ld_blocks, 2)
        self.assertEqual(fact.json_ld_malformed, 1)

    def test_an_empty_block_is_not_counted_as_a_block(self):
        fact = facts('<script type="application/ld+json">   </script>')
        self.assertEqual(fact.json_ld_blocks, 0)
        self.assertEqual(fact.json_ld_malformed, 0)

    def test_json_in_an_ordinary_script_is_not_structured_data(self):
        body = '<script>var data = {"@type": "NotThis"};</script>'
        self.assertEqual(facts(body).json_ld_types, ())

    def test_the_type_extractor_handles_depth(self):
        self.assertEqual(extract_json_ld_types({"@graph": [{"@type": ["A", "B"]}]}), ["A", "B"])
        self.assertEqual(extract_json_ld_types("not an object"), [])
        self.assertEqual(extract_json_ld_types({"@type": "  "}), [])


class VisibleText(unittest.TestCase):
    def test_counts_visible_text(self):
        self.assertEqual(facts("<body><p>one two</p></body>").visible_text_chars, len("one two"))

    def test_script_and_style_content_is_not_visible_text(self):
        body = "<body><script>var x = 'aaaaaaaaaa';</script><style>.a{color:red}</style>ok</body>"
        self.assertEqual(facts(body).visible_text_chars, 2)

    def test_collapses_whitespace_before_measuring(self):
        self.assertEqual(facts("<body>a\n\n   b</body>").visible_text_chars, 3)

    def test_a_self_closing_script_does_not_swallow_the_rest_of_the_document(self):
        body = '<body><script src="app.js" /><p>visible text here</p></body>'
        fact = facts(body)
        self.assertGreater(fact.visible_text_chars, 0)
        self.assertEqual(fact.script_blocks, 1)

    def test_an_unclosed_script_still_ends_at_the_document_end(self):
        fact = facts("<body><script>var x = 1;")
        self.assertEqual(fact.visible_text_chars, 0)
        self.assertEqual(fact.script_blocks, 1)

    def test_one_line_of_minified_html_is_measured(self):
        fact = facts("<div><p>Hello</p><p>world</p></div>")
        self.assertEqual(fact.visible_text_chars, len("Helloworld"))


class Links(unittest.TestCase):
    def test_counts_internal_links_by_unique_target(self):
        body = (
            '<a href="/a/">one</a><a href="/a/">again</a>'
            '<a href="/a/#frag">same page</a><a href="/b/">two</a>'
        )
        fact = facts(body)
        self.assertEqual(fact.internal_links, 2)
        self.assertEqual(fact.internal_targets, ("https://example.com/a/", "https://example.com/b/"))

    def test_resolves_relative_links_against_the_page_url(self):
        fact = facts('<a href="sibling/">x</a>', url="https://example.com/about/")
        self.assertEqual(fact.internal_targets, ("https://example.com/about/sibling/",))

    def test_an_absolute_link_to_the_same_origin_is_internal(self):
        fact = facts('<a href="https://example.com/x">x</a>')
        self.assertEqual(fact.internal_links, 1)

    def test_an_absolute_link_to_another_host_is_external_and_kept_out(self):
        fact = facts('<a href="https://elsewhere.example/x">x</a>')
        self.assertEqual(fact.internal_links, 0)
        self.assertEqual(fact.external_links, 1)
        self.assertEqual(fact.internal_targets, ())

    def test_non_navigational_links_are_neither(self):
        body = (
            '<a href="mailto:someone@example.com">m</a><a href="tel:+15550100">t</a>'
            '<a href="javascript:void(0)">j</a><a href="#top">f</a><a href="">e</a>'
        )
        fact = facts(body)
        self.assertEqual((fact.internal_links, fact.external_links), (0, 0))

    def test_a_protocol_relative_link_to_another_host_is_external(self):
        fact = facts('<a href="//elsewhere.example/x">x</a>')
        self.assertEqual((fact.internal_links, fact.external_links), (0, 1))

    def test_a_link_with_a_different_port_is_not_the_same_origin(self):
        fact = facts('<a href="https://example.com:8443/x">x</a>')
        self.assertEqual((fact.internal_links, fact.external_links), (0, 1))

    def test_a_query_string_distinguishes_two_links(self):
        fact = facts('<a href="/list?page=1">1</a><a href="/list?page=2">2</a>')
        self.assertEqual(fact.internal_links, 2)


class ScriptShellHeuristic(unittest.TestCase):
    """The heuristic's thresholds, and its behaviour at them.

    The thresholds are pinned to literal values on purpose. Asserting ``f(x) == f(x)`` against
    the imported constant would keep passing if someone moved the threshold, which is exactly
    the change a reader needs to be told about: the numbers are the gate's sensitivity, they are
    recorded in docs/DESIGN.md, and a test that cannot notice them moving is not a test.
    """

    def test_the_recorded_thresholds_are_the_ones_in_force(self):
        self.assertEqual(SCRIPT_SHELL_TEXT_CHARS, 200)
        self.assertEqual(SCRIPT_SHELL_SCRIPT_BYTES, 5000)

    def test_a_text_rich_page_is_not_a_shell(self):
        self.assertFalse(
            looks_like_a_script_shell(SCRIPT_SHELL_TEXT_CHARS + 1, 100_000, 3, True)
        )

    def test_an_empty_page_with_lots_of_script_is_a_shell(self):
        self.assertTrue(looks_like_a_script_shell(0, SCRIPT_SHELL_SCRIPT_BYTES, 1, False))

    def test_an_empty_page_with_an_app_root_and_any_script_is_a_shell(self):
        self.assertTrue(looks_like_a_script_shell(10, 20, 1, True))

    def test_a_short_page_with_an_app_root_but_no_script_is_not_a_shell(self):
        self.assertFalse(looks_like_a_script_shell(10, 0, 0, True))

    def test_a_short_page_with_a_little_script_and_no_root_is_not_a_shell(self):
        self.assertFalse(looks_like_a_script_shell(10, 100, 1, False))

    def test_the_threshold_boundary_is_inclusive(self):
        self.assertTrue(
            looks_like_a_script_shell(SCRIPT_SHELL_TEXT_CHARS - 1, SCRIPT_SHELL_SCRIPT_BYTES, 1, False)
        )
        self.assertFalse(
            looks_like_a_script_shell(SCRIPT_SHELL_TEXT_CHARS, SCRIPT_SHELL_SCRIPT_BYTES, 1, False)
        )

    def test_an_application_root_is_detected_in_a_real_document(self):
        body = '<body><div id="root"></div><script>%s</script></body>' % ("x" * 6000)
        fact = facts(body)
        self.assertTrue(fact.looks_script_rendered)
        self.assertTrue(fact.app_root)

    def test_a_normal_page_is_not_flagged(self):
        body = "<body><h1>A page</h1><p>%s</p><script>var a=1;</script></body>" % ("word " * 100)
        self.assertFalse(facts(body).looks_script_rendered)


class ContentTypes(unittest.TestCase):
    def test_a_non_html_body_is_measured_and_not_parsed(self):
        fact = facts('{"a": 1}', url="https://example.com/data.json", content_type="application/json")
        self.assertFalse(fact.is_html)
        self.assertEqual(fact.visible_text_chars, len('{"a": 1}'))
        self.assertIsNone(fact.title)
        self.assertEqual(fact.internal_links, 0)

    def test_a_json_ld_looking_body_in_a_text_file_is_not_structured_data(self):
        fact = facts('<script type="application/ld+json">{"@type":"X"}</script>', content_type="text/plain")
        self.assertEqual(fact.json_ld_types, ())

    def test_a_missing_content_type_falls_back_to_the_path(self):
        fact = facts("<html><head><title>T</title></head></html>", url="https://example.com/page.html", content_type="")
        self.assertTrue(fact.is_html)
        self.assertEqual(fact.title, "T")

    def test_an_error_page_with_no_body_still_carries_its_status(self):
        fact = facts_from(Page(url=ORIGIN, status=404, content_type="text/html", body=None), in_sitemap=False)
        self.assertEqual(fact.status, 404)
        self.assertFalse(fact.ok)
        self.assertIsNone(fact.title)
        self.assertEqual(fact.visible_text_chars, 0)


class MalformedMarkup(unittest.TestCase):
    def test_an_unclosed_comment_does_not_lose_the_facts(self):
        fact = facts("<html><head><title>T</title></head><body><!-- never closed <p>x</p></body>")
        self.assertEqual(fact.title, "T")

    def test_a_gt_inside_an_attribute_does_not_break_the_scan(self):
        fact = facts('<body><a href="/x" title="a > b">link</a><p>text</p></body>')
        self.assertEqual(fact.internal_links, 1)
        self.assertGreater(fact.visible_text_chars, 0)

    def test_a_stray_end_tag_does_not_lose_later_facts(self):
        fact = facts("</div><title>After a stray tag</title><a href='/y'>y</a>")
        self.assertEqual(fact.title, "After a stray tag")
        self.assertEqual(fact.internal_links, 1)

    def test_an_unusual_encoding_does_not_lose_the_facts(self):
        body = "<title>Caf\u00e9</title><p>\u00e9\u00e8\u00ea</p>"
        self.assertEqual(facts(body).title, "Caf\u00e9")


if __name__ == "__main__":
    unittest.main()
