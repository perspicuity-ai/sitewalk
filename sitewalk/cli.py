"""``python3 -m sitewalk`` — the command line.

Two sources, one analysis. ``--dir`` reads a built directory and performs **no network access at
all**; ``--url`` crawls a live site through the address guard. ``--plan`` checks the result
against a ``siteplan`` file. ``--strict`` turns findings into a non-zero exit so CI can gate.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import fetch, findings, guard, plan as plan_module, report as report_module
from .crawl import crawl
from .errors import GuardError, PlanError
from .sources import FileSource, LiveSource
from .urls import SURFACE_PATHS, origin_of

PROGRAM = "sitewalk"
VERSION = fetch.VERSION

DESCRIPTION = """\
Map the structure of a site that is already built.

Give it a directory of built files and it reads them without touching the network, which is what
makes it usable as a deploy gate; or give it a URL and it crawls the site, staying inside the
submitted origin and refusing any address that is not publicly routable.

It reports what is observable in the output the server returns. It does not execute JavaScript,
and it says so rather than implying a page is empty. It does not predict whether an agent will
find, trust or recommend a site, and it measures no ranking, citation or traffic."""

EPILOG = """\
exit status:
  0   the run completed
  1   under --strict, at least one error-severity finding was reported
  2   the run could not be made: a bad argument, an unreadable directory, or a plan file that
      could not be read. A gate that cannot read its own plan must not report a pass.

examples:
  python3 -m sitewalk --dir build/ --strict
  python3 -m sitewalk --dir build/ --json > sitewalk.json
  python3 -m sitewalk --url https://example.com --max-pages 20
  python3 -m sitewalk --url https://example.com --plan site.json --strict
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=PROGRAM,
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--url",
        metavar="URL",
        help="crawl a live site, starting at this URL and staying inside its origin",
    )
    source.add_argument(
        "--dir",
        metavar="PATH",
        dest="directory",
        help="read an already-built directory. No network access is performed at all",
    )
    parser.add_argument("--plan", metavar="FILE", help="check the site against a siteplan file")
    parser.add_argument(
        "--json",
        action="store_true",
        help="write the machine-readable report to stdout instead of the text report",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit 1 when an error-severity finding exists, so CI can gate on it",
    )
    parser.add_argument("--max-pages", type=int, default=50, metavar="N", help="crawl bound (default 50)")
    parser.add_argument(
        "--timeout", type=float, default=10.0, metavar="SECONDS", help="per-request timeout (default 10)"
    )
    parser.add_argument(
        "--max-body",
        type=int,
        default=2 * 1024 * 1024,
        metavar="BYTES",
        help="body size cap in bytes; a longer body is truncated and reported (default 2097152)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.2,
        metavar="SECONDS",
        help="polite delay between requests to the site (default 0.2)",
    )
    parser.add_argument(
        "--user-agent", default=fetch.USER_AGENT, metavar="STRING", help="the User-Agent to send"
    )
    parser.add_argument("--version", action="version", version=f"{PROGRAM} {VERSION}")
    return parser


def build_live_source(origin: str, **options) -> LiveSource:
    """The one place the live source is constructed.

    It exists so the live path can be exercised with no network: a test replaces
    ``sitewalk.fetch.fetch`` and ``sitewalk.guard.default_resolver`` and calls the command line,
    and the source picks those up because it is built here rather than by a dataclass default.
    """
    return LiveSource(origin=origin, **options)


def _validate(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    if args.max_pages < 1:
        parser.error("--max-pages must be at least 1")
    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")
    if args.max_body < 1:
        parser.error("--max-body must be at least 1 byte")
    if args.delay < 0:
        parser.error("--delay cannot be negative")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    _validate(args, parser)

    if args.directory:
        root = Path(args.directory)
        if not root.is_dir():
            print(f"{PROGRAM}: {root} is not a directory", file=sys.stderr)
            return 2
        source = FileSource(root)
        target = source.origin
        if args.timeout != 10.0 or args.delay != 0.2 or args.user_agent != fetch.USER_AGENT:
            print(
                f"{PROGRAM}: note: --timeout, --delay and --user-agent do not apply to --dir; "
                "no network request is made",
                file=sys.stderr,
            )
    else:
        try:
            scheme, host, port, _path = guard.parse_target(args.url)
        except GuardError as exc:
            print(f"{PROGRAM}: {exc}", file=sys.stderr)
            return 2
        origin = origin_of(args.url)
        if not origin:
            print(f"{PROGRAM}: {args.url!r} has no usable origin", file=sys.stderr)
            return 2
        source = build_live_source(
            origin,
            user_agent=args.user_agent,
            timeout=args.timeout,
            delay=args.delay,
            max_body=args.max_body,
        )
        target = origin

    try:
        result = crawl(source, target, max_pages=args.max_pages)
    except GuardError as exc:
        print(f"{PROGRAM}: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"{PROGRAM}: could not read the source: {exc}", file=sys.stderr)
        return 2

    report = findings.analyse(result)

    if args.plan:
        try:
            plan_data = plan_module.load_plan(args.plan)
        except ValueError as exc:
            print(f"{PROGRAM}: {exc}", file=sys.stderr)
            return 2
        check = plan_module.check_plan(report, plan_data, path=args.plan)
        plan_module.apply_to_report(check, report)

    if args.json:
        print(report_module.to_json(report))
    else:
        print(report_module.to_text(report))
        print(report_module.summary_line(report), file=sys.stderr)

    return report_module.exit_code(report, args.strict)


if __name__ == "__main__":  # pragma: no cover - exercised through __main__.py
    sys.exit(main())
