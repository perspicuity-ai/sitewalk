"""The address guard.

The guard is the security boundary of the package: it decides which host this tool may connect
to, for a URL a stranger supplied. These tests are written against injected resolvers and
injected connections, so they exercise the rules themselves rather than the network, and they
run with no network available at all.

A guard that is silently not applied is the failure that matters, so most of these tests assert
that a *refusal* happened rather than that an error of some kind happened, and the
post-connection test asserts the refusal names the peer address.
"""

from __future__ import annotations

import pathlib
import socket
import unittest

from sitewalk import guard
from sitewalk.errors import GuardError

from . import fakes


class SchemeAndPort(unittest.TestCase):
    def test_http_and_https_are_accepted(self):
        for url, scheme, port in (
            ("http://example.com/", "http", 80),
            ("https://example.com/", "https", 443),
            ("https://example.com:443/", "https", 443),
            ("http://example.com:80/", "http", 80),
        ):
            with self.subTest(url=url):
                got_scheme, host, got_port, path = guard.parse_target(url)
                self.assertEqual((got_scheme, host, got_port), (scheme, "example.com", port))
                self.assertEqual(path, "/")

    def test_refuses_other_schemes(self):
        for url in (
            "ftp://example.com/",
            "file:///etc/passwd",
            "javascript:alert(1)",
            "data:text/html,hi",
            "gopher://example.com/",
            "//example.com/",
            "example.com",
            "",
        ):
            with self.subTest(url=url):
                with self.assertRaises(GuardError) as caught:
                    guard.parse_target(url)
                self.assertIn("scheme", str(caught.exception))

    def test_refuses_a_port_that_is_not_the_scheme_default(self):
        for url in (
            "https://example.com:8443/",
            "http://example.com:8080/",
            "https://example.com:80/",
            "http://example.com:443/",
            "https://example.com:22/",
            "https://example.com:0/",
        ):
            with self.subTest(url=url):
                with self.assertRaises(GuardError) as caught:
                    guard.parse_target(url)
                self.assertIn("port", str(caught.exception))

    def test_refuses_a_host_with_no_name(self):
        with self.assertRaises(GuardError):
            guard.parse_target("https:///path")

    def test_lower_cases_the_host_and_keeps_the_query(self):
        _scheme, host, _port, path = guard.parse_target("https://EXAMPLE.com:443/A?b=1#frag")
        self.assertEqual(host, "example.com")
        self.assertEqual(path, "/A?b=1")

    def test_an_international_name_is_punycoded(self):
        _scheme, host, _port, _path = guard.parse_target("https://münchen.example/")
        self.assertEqual(host, "xn--mnchen-3ya.example")

    def test_credentials_in_a_url_are_not_part_of_the_target(self):
        scheme, host, port, path = guard.parse_target("https://user:secret@example.com/x")
        self.assertEqual((scheme, host, port, path), ("https", "example.com", 443, "/x"))
        self.assertNotIn("secret", host)


class AddressRules(unittest.TestCase):
    def test_public_addresses_are_public(self):
        for ip in ("93.184.216.34", "1.1.1.1", "2606:4700:4700::1111", "8.8.8.8"):
            with self.subTest(ip=ip):
                self.assertTrue(guard.is_public_address(ip))

    def test_non_public_addresses_are_not_public(self):
        cases = {
            "10.0.0.1": "private",
            "172.16.5.4": "private",
            "192.168.1.1": "private",
            "127.0.0.1": "loopback",
            "127.1.2.3": "loopback",
            "::1": "loopback",
            "169.254.169.254": "link-local, the cloud metadata address",
            "169.254.1.1": "link-local",
            "fe80::1": "link-local",
            "224.0.0.1": "multicast",
            "ff02::1": "multicast",
            "0.0.0.0": "unspecified",
            "::": "unspecified",
            "240.0.0.1": "reserved",
            "255.255.255.255": "reserved",
            "::ffff:127.0.0.1": "an IPv4-mapped loopback",
            "::ffff:169.254.169.254": "an IPv4-mapped metadata address",
        }
        for ip, reason in cases.items():
            with self.subTest(ip=ip, reason=reason):
                self.assertFalse(guard.is_public_address(ip), f"{ip} is {reason}")

    def test_a_string_that_is_not_an_address_is_not_public(self):
        for value in ("", "example.com", "999.1.1.1", "not an address"):
            with self.subTest(value=value):
                self.assertFalse(guard.is_public_address(value))


class ResolveThenRefuse(unittest.TestCase):
    def test_every_answer_must_be_public(self):
        resolver = fakes.resolver_for("93.184.216.34", "10.0.0.1")
        with self.assertRaises(GuardError) as caught:
            guard.check_host("example.com", 443, resolver)
        self.assertIn("10.0.0.1", str(caught.exception))

    def test_a_private_first_answer_is_refused(self):
        resolver = fakes.resolver_for("192.168.0.5", "93.184.216.34")
        with self.assertRaises(GuardError):
            guard.check_host("example.com", 443, resolver)

    def test_a_public_answer_is_accepted(self):
        resolver = fakes.resolver_for("93.184.216.34")
        addresses = guard.check_host("example.com", 443, resolver)
        self.assertEqual(len(addresses), 1)

    def test_a_name_that_does_not_resolve_is_refused(self):
        with self.assertRaises(GuardError) as caught:
            guard.check_host("nope.example", 443, fakes.resolver_map({}))
        self.assertIn("could not resolve", str(caught.exception))

    def test_a_resolver_that_answers_nothing_is_refused(self):
        with self.assertRaises(GuardError):
            guard.check_host("example.com", 443, lambda host, port: [])

    def test_a_literal_private_address_is_refused_without_asking_the_resolver(self):
        asked: list[str] = []

        def resolver(host, port):
            asked.append(host)
            return [fakes.address("93.184.216.34", port, host)]

        for host in ("169.254.169.254", "127.0.0.1", "10.1.1.1", "::1", "[::ffff:169.254.169.254]"):
            with self.subTest(host=host):
                with self.assertRaises(GuardError) as caught:
                    guard.check_host(host, 80, resolver)
                self.assertIn("non-public address", str(caught.exception))
        self.assertEqual(asked, [], "a literal address must not be handed to the resolver")

    def test_a_literal_public_address_is_accepted_without_asking_the_resolver(self):
        addresses = guard.check_host("93.184.216.34", 443, fakes.resolver_map({}))
        self.assertEqual(len(addresses), 1)


class PeerCheckAfterConnecting(unittest.TestCase):
    """The check that closes the DNS-rebinding window."""

    def test_a_public_peer_passes(self):
        guard.check_peer(fakes.FakeConnection(routes={}, sock=fakes.FakeSocket(("93.184.216.34", 443))), "https://example.com/")

    def test_a_private_peer_is_refused(self):
        connection = fakes.FakeConnection(routes={}, sock=fakes.FakeSocket(("127.0.0.1", 443)))
        with self.assertRaises(GuardError) as caught:
            guard.check_peer(connection, "https://example.com/")
        self.assertIn("127.0.0.1", str(caught.exception))

    def test_the_metadata_address_as_a_peer_is_refused(self):
        connection = fakes.FakeConnection(routes={}, sock=fakes.FakeSocket(("169.254.169.254", 80)))
        with self.assertRaises(GuardError):
            guard.check_peer(connection, "http://metadata/")

    def test_a_connection_with_no_socket_is_refused(self):
        with self.assertRaises(GuardError):
            guard.check_peer(fakes.FakeConnection(routes={}, sock=None), "https://example.com/")

    def test_a_peer_that_cannot_be_read_is_refused(self):
        class Unreadable:
            sock = object()

        with self.assertRaises(GuardError):
            guard.check_peer(Unreadable(), "https://example.com/")


class TheGuardIsAppliedByTheFetchLayer(unittest.TestCase):
    """A rule that is not reached is not a rule, so these go through ``fetch``."""

    def test_a_private_answer_stops_the_fetch_before_any_connection(self):
        from sitewalk import fetch

        http = fakes.FakeHTTP(routes={})
        http.add("/", "hi")
        for ip in ("127.0.0.1", "10.0.0.1", "169.254.169.254", "192.168.1.10"):
            with self.subTest(ip=ip):
                with self.assertRaises(GuardError):
                    fetch.fetch(
                        "https://example.com/",
                        resolver=fakes.resolver_for(ip),
                        connector=http.connector,
                    )
        self.assertEqual(http.connections, [], "no connection may be opened after a refusal")

    def test_a_non_public_peer_stops_the_fetch_after_connecting(self):
        from sitewalk import fetch

        http = fakes.FakeHTTP(routes={}, peer_host="10.0.0.7")
        http.add("/", "hi")
        with self.assertRaises(GuardError) as caught:
            fetch.fetch(
                "https://example.com/",
                resolver=fakes.resolver_for("93.184.216.34"),
                connector=http.connector,
            )
        self.assertIn("10.0.0.7", str(caught.exception))
        self.assertEqual(http.paths_requested, ["/"], "the request was sent before the peer check")

    def test_a_redirect_off_the_origin_is_refused_rather_than_followed(self):
        from sitewalk import fetch

        http = fakes.FakeHTTP(routes={})
        http.redirect("/", "https://169.254.169.254/latest/meta-data/")
        page = fetch.fetch(
            "https://example.com/",
            resolver=fakes.resolver_for("93.184.216.34"),
            connector=http.connector,
            allowed_origin="https://example.com",
        )
        self.assertFalse(page.ok)
        self.assertIn("off the submitted origin", page.error)
        self.assertEqual(http.paths_requested, ["/"], "the off-origin hop was fetched")

    def test_every_redirect_hop_is_resolved_and_checked_again(self):
        from sitewalk import fetch

        checked: list[tuple[str, int]] = []

        def watched_resolver(host, port):
            checked.append((host, port))
            return [fakes.address("93.184.216.34", port, host)]

        http = fakes.FakeHTTP(routes={})
        http.redirect("/", "/second")
        http.redirect("/second", "/third")
        http.add("/third", "arrived")
        page = fetch.fetch(
            "https://example.com/",
            resolver=watched_resolver,
            connector=http.connector,
            allowed_origin="https://example.com",
        )
        self.assertTrue(page.ok)
        self.assertEqual(page.body, "arrived")
        self.assertEqual([host for host, _ in checked], ["example.com", "example.com", "example.com"])
        self.assertEqual(http.paths_requested, ["/", "/second", "/third"])

    def test_a_redirect_loop_stops_at_the_bound(self):
        from sitewalk import fetch

        http = fakes.FakeHTTP(routes={})
        http.redirect("/a", "/b")
        http.redirect("/b", "/a")
        page = fetch.fetch(
            "https://example.com/a",
            resolver=fakes.resolver_for("93.184.216.34"),
            connector=http.connector,
            allowed_origin="https://example.com",
            max_redirects=3,
        )
        self.assertFalse(page.ok)
        self.assertIn("redirects", page.error)
        self.assertLessEqual(len(http.paths_requested), 5)


if __name__ == "__main__":
    unittest.main()


class TheAddressHoldsOnlyWhatIsRead(unittest.TestCase):
    """U9: U1's deletion test, applied to this unit's own work.

    `Address` carried `host`, `port` and `family`, all written and none read. The guard reads
    `sockaddr[0]` and nothing else, so the others were the same defect that deleted
    `Page.final_url` — and they were missed because U1's audit was run against the items already
    identified rather than across the package.
    """

    def test_address_carries_only_the_socket_address(self):
        from dataclasses import fields

        self.assertEqual([f.name for f in fields(guard.Address)], ["sockaddr"])

    def test_the_guard_reads_the_ip_from_the_socket_address(self):
        addresses = guard.check_host("example.com", 443, fakes.resolver_for("93.184.216.34"))
        self.assertEqual(addresses[0].sockaddr[0], "93.184.216.34")

    def test_a_private_literal_still_refuses_after_the_slimming(self):
        with self.assertRaises(GuardError):
            guard.check_host("169.254.169.254", 80, fakes.resolver_map({}))


class NoDeadErrorTypes(unittest.TestCase):
    def test_every_error_type_is_raised_or_caught_somewhere(self):
        # PlanError was defined and never referenced. A public exception type with no raiser is a
        # promise the package does not keep.
        import inspect

        from sitewalk import errors

        defined = {
            name
            for name, value in vars(errors).items()
            if inspect.isclass(value) and issubclass(value, Exception)
        }
        sources = " ".join(
            path.read_text()
            for path in (pathlib.Path(__file__).parent.parent / "sitewalk").glob("*.py")
        )
        for name in sorted(defined):
            with self.subTest(error=name):
                self.assertIn(f"{name}(", sources, f"{name} is defined and never raised")
