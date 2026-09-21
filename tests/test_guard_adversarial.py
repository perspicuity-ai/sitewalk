"""Adversarial tests: try to defeat the address guard, through the fetch layer.

`test_guard.py` tests the guard's rules. This file attacks them. The distinction matters: a rule
that is implemented and never reached is not a rule, so every case here goes through
`fetch.fetch`, which is the function that actually opens sockets, and every case asserts that
**no connection was made** or that the refusal names the address it refused.

A refusal that does not name the offending address is treated as a failure here, because a
refusal a reader cannot diagnose is a refusal the next maintainer will weaken.

Nothing here opens a socket: `fakes.no_network()` makes every socket operation raise, and the
resolver and connector are injected.
"""

from __future__ import annotations

import unittest

from sitewalk import fetch, guard
from sitewalk.errors import GuardError

from . import fakes

PUBLIC = "93.184.216.34"
METADATA = "169.254.169.254"


class FetchAttempt:
    """Drive one fetch against a fake site and hand back what happened."""

    def __init__(self, routes=None, peer_host=None):
        self.http = fakes.FakeHTTP(routes=routes or {}, peer_host=peer_host)
        self.http.add("/", "<title>Home</title>")

    def run(self, url, ips=(PUBLIC,), **kwargs):
        """Return ``(page_or_None, error_or_None, paths_requested)``."""
        with fakes.no_network():
            try:
                page = fetch.fetch(
                    url,
                    resolver=fakes.resolver_for(*ips),
                    connector=self.http.connector,
                    **kwargs,
                )
            except GuardError as exc:
                return None, exc, self.http.paths_requested
        return page, None, self.http.paths_requested


class NamesThatPointSomewhereTheyShouldNot(unittest.TestCase):
    def test_a_name_resolving_to_the_metadata_address_is_refused(self):
        page, error, paths = FetchAttempt().run("https://example.com/", ips=(METADATA,))
        self.assertIsNone(page)
        self.assertIn(METADATA, str(error))
        self.assertEqual(paths, [], "a request was made to a refused host")

    def test_one_private_answer_among_public_ones_is_refused(self):
        page, error, paths = FetchAttempt().run(
            "https://example.com/", ips=(PUBLIC, "10.0.0.5", PUBLIC)
        )
        self.assertIsNone(page)
        self.assertIn("10.0.0.5", str(error))
        self.assertEqual(paths, [])

    def test_a_name_resolving_to_loopback_is_refused(self):
        for ip in ("127.0.0.1", "127.0.0.53", "::1"):
            with self.subTest(ip=ip):
                page, error, paths = FetchAttempt().run("https://example.com/", ips=(ip,))
                self.assertIsNone(page)
                self.assertIn(ip, str(error))
                self.assertEqual(paths, [])

    def test_a_name_resolving_into_every_private_range_is_refused(self):
        for ip in ("10.1.2.3", "172.16.0.1", "192.168.0.1", "169.254.1.1", "fe80::1",
                   "fc00::1", "224.0.0.1", "0.0.0.0", "240.0.0.1", "::"):
            with self.subTest(ip=ip):
                page, error, _paths = FetchAttempt().run("https://example.com/", ips=(ip,))
                self.assertIsNone(page, f"{ip} was accepted")

    def test_a_literal_metadata_address_is_refused_without_asking_the_resolver(self):
        asked = []

        def resolver(host, port):
            asked.append(host)
            return [fakes.address(PUBLIC, port, host)]

        with fakes.no_network():
            with self.assertRaises(GuardError) as caught:
                fetch.fetch(
                    f"http://{METADATA}/latest/meta-data/",
                    resolver=resolver,
                    connector=fakes.FakeHTTP(routes={}).connector,
                )
        self.assertIn(METADATA, str(caught.exception))
        self.assertEqual(asked, [], "a literal address was handed to the resolver")

    def test_a_literal_private_address_in_any_notation_is_refused(self):
        # Decimal and octal spellings of 127.0.0.1 and 169.254.169.254, which a naive string
        # check would miss. Python's ip_address rejects them, and so must the guard.
        for host in ("2130706433", "0177.0.0.1", "0x7f.0.0.1", "127.1", "127.0.0.1.nip.io"):
            with self.subTest(host=host):
                page, error, paths = FetchAttempt().run(
                    f"https://{host}/", ips=("127.0.0.1",)
                )
                self.assertIsNone(page, f"{host} was accepted")
                self.assertEqual(paths, [])

    def test_an_ipv4_mapped_private_address_is_refused(self):
        for ip in ("::ffff:127.0.0.1", "::ffff:169.254.169.254", "::ffff:10.0.0.1"):
            with self.subTest(ip=ip):
                page, _error, _paths = FetchAttempt().run("https://example.com/", ips=(ip,))
                self.assertIsNone(page, f"{ip} was accepted")

    def test_a_name_that_does_not_resolve_is_refused_not_attempted(self):
        page, error, paths = FetchAttempt().run("https://example.com/", ips=())
        self.assertIsNone(page)
        self.assertEqual(paths, [])


class ThePeerAfterConnecting(unittest.TestCase):
    """The rebinding window: the name resolved publicly and the socket went somewhere else."""

    def test_a_private_peer_is_refused_even_when_the_name_resolved_publicly(self):
        for peer in ("127.0.0.1", "10.0.0.9", METADATA, "192.168.1.1", "::1"):
            with self.subTest(peer=peer):
                page, error, paths = FetchAttempt(peer_host=peer).run("https://example.com/")
                self.assertIsNone(page, f"a {peer} peer was accepted")
                self.assertIn(peer, str(error))
                # The request line is sent before the peer can be inspected; what matters is
                # that no response was accepted and the refusal names the peer.
                self.assertEqual(paths, ["/"])

    def test_a_public_peer_is_accepted(self):
        page, error, _paths = FetchAttempt(peer_host=PUBLIC).run("https://example.com/")
        self.assertIsNone(error)
        self.assertEqual(page.status, 200)

    def test_a_connection_with_no_socket_is_refused(self):
        connection = fakes.FakeConnection(routes={}, sock=None)
        with self.assertRaises(GuardError):
            guard.check_peer(connection, "https://example.com/")


class Redirects(unittest.TestCase):
    def test_a_redirect_to_a_literal_private_address_is_refused(self):
        head = FetchAttempt()
        head.http.redirect("/", f"http://{METADATA}/latest/meta-data/")
        page, _error, paths = head.run("https://example.com/", allowed_origin="https://example.com")
        self.assertFalse(page.ok)
        self.assertIn("off the submitted origin", page.error)
        self.assertEqual(paths, ["/"], "the metadata address was fetched")

    def test_a_redirect_to_another_public_host_is_refused_because_the_origin_changed(self):
        head = FetchAttempt()
        head.http.redirect("/", "https://elsewhere.example/")
        page, _error, paths = head.run("https://example.com/", allowed_origin="https://example.com")
        self.assertFalse(page.ok)
        self.assertEqual(paths, ["/"])

    def test_a_redirect_to_the_https_upgrade_is_followed(self):
        # The most common redirect on the web. Refusing it would report a plain-HTTP site as
        # unreachable when it is merely sending the crawl to its own TLS endpoint. This is a
        # defect the adversarial pass found: the first implementation compared origins, so
        # http://host and https://host were different sites.
        head = FetchAttempt()
        head.http.redirect("http://example.com/", "https://example.com/")
        head.http.add("https://example.com/", "<title>Secure home</title>")
        page, error, paths = head.run(
            "http://example.com/", allowed_origin="http://example.com"
        )
        self.assertIsNone(error)
        self.assertTrue(page.ok, page.error)
        # The upgrade was actually taken: a connection was opened on 443, not only on 80.
        self.assertEqual(head.http.endpoints, [("example.com", 80), ("example.com", 443)])

    def test_a_redirect_that_downgrades_https_to_http_is_refused(self):
        head = FetchAttempt()
        head.http.redirect("https://example.com/", "http://example.com/")
        head.http.add("http://example.com/", "<title>Plain home</title>")
        page, _error, _paths = head.run(
            "https://example.com/", allowed_origin="https://example.com"
        )
        self.assertFalse(page.ok)
        self.assertIn("off the submitted origin", page.error or "")

    def test_a_redirect_to_a_subdomain_is_refused(self):
        head = FetchAttempt()
        head.http.redirect("https://example.com/", "https://evil.example.com/")
        head.http.add("https://evil.example.com/", "<title>Elsewhere</title>")
        page, _error, paths = head.run(
            "https://example.com/", allowed_origin="https://example.com"
        )
        self.assertFalse(page.ok)
        self.assertEqual(paths, ["/"], "the redirect target was fetched")

    def test_a_redirect_to_another_port_on_the_same_host_is_refused(self):
        head = FetchAttempt()
        head.http.redirect("https://example.com/", "https://example.com:8443/")
        page, _error, _paths = head.run(
            "https://example.com/", allowed_origin="https://example.com"
        )
        self.assertFalse(page.ok)
        self.assertEqual(
            head.http.endpoints,
            [("example.com", 443)],
            "a connection was opened to a port the submitted origin never named",
        )

    def test_a_redirect_chain_that_stays_public_is_followed(self):
        head = FetchAttempt()
        head.http.redirect("/", "/a")
        head.http.redirect("/a", "/b")
        head.http.add("/b", "<title>Arrived</title>")
        page, error, paths = head.run("https://example.com/", allowed_origin="https://example.com")
        self.assertIsNone(error)
        self.assertTrue(page.ok)
        self.assertEqual(paths, ["/", "/a", "/b"])

    def test_an_endless_redirect_chain_stops(self):
        head = FetchAttempt()
        head.http.redirect("/", "/loop")
        head.http.redirect("/loop", "/")
        page, error, paths = head.run(
            "https://example.com/", allowed_origin="https://example.com", max_redirects=4
        )
        self.assertIsNone(error)
        self.assertFalse(page.ok)
        self.assertLessEqual(len(paths), 6)

    def test_every_hop_is_resolved_by_the_guard(self):
        resolved = []

        def watching_resolver(host, port):
            resolved.append(host)
            return [fakes.address(PUBLIC, port, host)]

        head = FetchAttempt()
        head.http.redirect("/", "https://example.com/a")
        head.http.add("/a", "<title>A</title>")
        with fakes.no_network():
            fetch.fetch(
                "https://example.com/",
                resolver=watching_resolver,
                connector=head.http.connector,
                allowed_origin="https://example.com",
            )
        self.assertEqual(resolved, ["example.com", "example.com"])


class SchemesPortsAndCredentials(unittest.TestCase):
    def test_credentials_are_never_sent(self):
        head = FetchAttempt()
        sent = []
        original = head.http.connector

        def recording_connector(scheme, host, port, timeout):
            connection = original(scheme, host, port, timeout)
            original_request = connection.request

            def request(method, path, headers=None):
                sent.append((path, dict(headers or {})))
                return original_request(method, path, headers)

            connection.request = request
            return connection

        with fakes.no_network():
            fetch.fetch(
                "https://user:secret@example.com/",
                resolver=fakes.resolver_for(PUBLIC),
                connector=recording_connector,
            )
        self.assertTrue(sent, "nothing was requested")
        path, headers = sent[0]
        self.assertEqual(path, "/")
        joined = " ".join(f"{k}:{v}" for k, v in headers.items())
        self.assertNotIn("secret", joined)
        self.assertNotIn("Authorization", headers)
        self.assertNotIn("Cookie", headers)

    def test_only_the_expected_headers_are_sent(self):
        head = FetchAttempt()
        sent = []
        original = head.http.connector

        def recording_connector(scheme, host, port, timeout):
            connection = original(scheme, host, port, timeout)
            original_request = connection.request

            def request(method, path, headers=None):
                sent.append(dict(headers or {}))
                return original_request(method, path, headers)

            connection.request = request
            return connection

        with fakes.no_network():
            fetch.fetch(
                "https://example.com/",
                resolver=fakes.resolver_for(PUBLIC),
                connector=recording_connector,
            )
        self.assertEqual(
            set(sent[0]),
            {"User-Agent", "Accept", "Accept-Encoding", "Connection"},
        )

    def test_a_non_default_port_is_refused_before_connecting(self):
        for url in ("https://example.com:8443/", "http://example.com:8080/", "https://example.com:22/"):
            with self.subTest(url=url):
                page, error, paths = FetchAttempt().run(url)
                self.assertIsNone(page)
                self.assertIn("port", str(error))
                self.assertEqual(paths, [])

    def test_a_scheme_other_than_http_is_refused_before_connecting(self):
        for url in ("file:///etc/passwd", "ftp://example.com/x", "gopher://example.com/"):
            with self.subTest(url=url):
                page, error, paths = FetchAttempt().run(url)
                self.assertIsNone(page)
                self.assertIn("scheme", str(error))
                self.assertEqual(paths, [])


class ThePatternIsComplete(unittest.TestCase):
    """Mechanical checks that the enforcement points exist and are not duplicated."""

    def test_the_fetch_layer_calls_every_enforcement_point(self):
        import inspect

        source = inspect.getsource(fetch)
        for name in ("parse_target", "check_host", "check_peer"):
            with self.subTest(rule=name):
                self.assertIn(
                    f"guard.{name}",
                    source,
                    f"the fetch layer never calls guard.{name}, so that rule is not enforced",
                )

    def test_the_fetch_layer_is_the_only_module_that_opens_a_socket(self):
        # guard imports socket to resolve names, and is the only other module allowed to know
        # the network exists. Anything else reaching for it is a second path around the guard.
        import pathlib
        import re

        pkg = pathlib.Path(__file__).parent.parent / "sitewalk"
        offenders = []
        for path in pkg.glob("*.py"):
            text = path.read_text()
            if re.search(r"^\s*import (socket|ssl|http\.client)", text, re.M):
                offenders.append(path.name)
        self.assertEqual(
            sorted(offenders),
            ["fetch.py", "guard.py"],
            "a module other than fetch and guard can open a socket or resolve a name",
        )

    def test_no_module_other_than_sources_decides_what_is_fetched(self):
        # The crawl asks a source for a URL; it never builds a connection itself.
        import inspect

        from sitewalk import crawl

        source = inspect.getsource(crawl)
        self.assertNotIn("http.client", source)
        self.assertNotIn("socket", source)


if __name__ == "__main__":
    unittest.main()
