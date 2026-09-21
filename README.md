# sitewalk

Give it a web address or a directory of built files, and it returns a structural map of the site:
every page it can find, what each page exposes to a machine, how the pages connect, and where the
gaps are. It reports the shape of a site that is already built.

The reason it exists is the moment before a deploy, when the question is "did this change break
anything about how the site presents itself to machines". `sitewalk --dir build/` answers that
offline, so it can gate a release without touching the network.

## What it does not do

Read this before trusting a report. The limits are the product, not caveats on it.

- **It does not execute JavaScript.** It fetches HTML and reads it. Anything a browser would
  render after load is invisible to it. Where a page looks like a script shell, the report says so
  — with the evidence, and as a **heuristic** — rather than implying the page is empty. A short
  visible-text length is not evidence of an empty page.
- **It does not predict whether an agent will find, trust or recommend a site**, and it measures
  no ranking, citations or traffic. There is deliberately no aggregate score anywhere in it.
- **It fetches only the origin you submit.** It never follows a link off-site and never checks an
  external link. A tool that follows a link off-site is a tool that can be pointed at someone
  else's server.
- **It refuses addresses that are not publicly routable** — private, loopback, link-local,
  multicast, reserved and cloud-metadata ranges — and re-checks the address it actually connected
  to. This is the code that decides whether the tool may be pointed at a stranger's site.
- **`--dir` makes no network request at all**. A test enforces it by making every socket
  operation raise.
- **It writes nothing to disk and keeps nothing between runs.** Reports go to stdout.
- **It sends no cookie, uses no account, and stores no credential.**

## Install

Python 3.11 or later. That is the whole install:

```sh
git clone <this repository> && cd sitewalk
python3 -m sitewalk --help
```

There are no dependencies, and the package is standard library only. Run it from the repository
root, or put the repository root on `PYTHONPATH`.

## Use

### The deploy gate: a built directory

```sh
python3 -m sitewalk --dir build/                 # read the report
python3 -m sitewalk --dir build/ --strict; echo $?   # 1 if an error finding exists, for CI
python3 -m sitewalk --dir build/ --json > site.json
```

`--dir` reads an already-built directory with **no network access at all**. A URL path maps onto a
file: `/` reads `index.html`, `/about/` reads `about/index.html`, `/about` reads `about.html` or
`about/index.html`. A query string is not part of a filename, so it is dropped for the mapping and
the report says so rather than pretending the build holds a distinction it does not.

### A live site

```sh
python3 -m sitewalk --url https://example.com
python3 -m sitewalk --url https://example.com --max-pages 20 --delay 0.5 --strict
```

It fetches `/robots.txt` and `/sitemap.xml`, collects the URLs they name, follows internal links
from the home page, and stays inside the submitted origin.

**`robots.txt` is obeyed in both modes, and the skip is reported.** It is a statement about the
site's content rather than about the transport, so a tool that reports what a machine can read does
not read what the site has refused. There is no flag to override it: a gate whose scope depends on
a switch is a gate nobody can compare across runs. When paths are skipped, the report's header
states how many, `limits.paths_skipped_robots` carries the count in the JSON, and each skip in the
notes quotes the rule **verbatim as it appears in the file**, so you can search for it and find
it.

### Against a plan

```sh
python3 -m sitewalk --dir build/ --plan site.json --strict
```

The plan file format is owned by the [`siteplan`](https://github.com/perspicuity-ai/siteplan)
project. Two keys are checked: `required_surfaces` against the files the site publishes, and
`identity.schema_types` against the home page's JSON-LD. Every other key is named in the output as
**not checked**, with the reason.

The verdict depends on what this tool actually knows:

| Plan | Verdict | `--strict` |
| --- | --- | --- |
| `plan_version` 1, or older | `met` — an older plan is fully specified by its own version | as the findings dictate |
| A **newer or unknown** `plan_version` | `met with conditions` — the file may be valid against a specification this tool does not hold, so a key's meaning may have moved | **exits 1** |
| An **absent or mistyped** `plan_version` | `not met` — the file is malformed, and with no usable version no key can be trusted | **exits 1** |
| A required surface this tool has **no check for** | `met with conditions` — reported **unverified**, never absent | **exits 1** |
| An unknown key | ignored, **and named**, so a `met` never hides something that was not checked | not on its own |

This tool checks all five surfaces the format's vocabulary defines — `robots.txt`, `sitemap.xml`,
`llms.txt` and `rss.xml` by fetching them, and `json-ld` by reading the pages it already has. So no
plan can ask for something the gate cannot certify today. If the format adds a sixth, the gap
reopens and the rule still holds: an unverifiable surface is reported *unverified* and gates under
`--strict` rather than passing silently.

"Not found" and "not checked" are different claims and the output keeps them apart. Each surface
carries a machine-readable state, so a JSON consumer never has to infer one from a message:

| State | Meaning |
| --- | --- |
| `present` | Fetched, and the site publishes it |
| `absent` | Fetched, and the site does not publish it |
| `derived` | Not fetched — there is nothing to fetch; established from pages already read, as `json-ld` is |
| `not_checked` | This tool has no check for it |

`rss.xml` is reported like the other surfaces and is **not** an error when a site has no feed:
only a plan that requires one makes it a finding. A consumer that rejects a growing
format breaks the producer, so an unknown key is read and disclosed rather than refused. A plan
that cannot be read at all exits 2 — a gate that cannot read its own plan must not report a pass.

## What it reports

Per page: status, content type, `<title>`, meta description, canonical, the JSON-LD `@type`
values, visible-text length, internal-link count, and whether the sitemap named it.

Site-wide: page count and status distribution; sitemap URLs never reached; orphan pages (in the
sitemap, linked from nowhere); duplicate titles; duplicate descriptions; missing and empty titles;
canonicals pointing at another host; pages carrying no JSON-LD; malformed JSON-LD; internal links
that do not return 200; and whether `robots.txt`, `sitemap.xml` and `llms.txt` exist.

Findings have three severities, and they are defined in the output itself so nothing has to be
inferred from an exit code. An **error** is something wrong with the site as built. A
**conditional** finding means the verdict depends on something this tool does not know — an
unknown plan version, or a surface it has no check for. A **note** is an observation or a choice
the site made — a script-rendered page, a missing `llms.txt`, a truncated body.

**The report states what is true; the gate decides what is tolerable.** `--strict` maps severities
to an exit code and never creates a finding, so two runs of the same site against the same plan
cannot disagree about what is true. Error and conditional both gate; notes do not, because a gate
that fails on a site's design choices gets switched off, and a switched-off gate measures nothing. A missing `llms.txt`
is a note on purpose: it is the site's choice, and Ahrefs measured that 97% of `llms.txt` files
received no requests across 137,000 sites
([study](https://ahrefs.com/blog/llmstxt-study/)).

## Options

| Option | Default | Meaning |
| --- | --- | --- |
| `--dir PATH` | — | Read a built directory. No network access. One of `--dir` or `--url` is required |
| `--url URL` | — | Crawl a live site, staying inside its origin |
| `--plan FILE` | — | Check the site against a `siteplan` file |
| `--json` | off | Machine-readable report on stdout instead of the text report |
| `--strict` | off | Exit 1 when an error-severity finding exists |
| `--max-pages N` | 50 | The bound on how many pages are read. It is the only bound on what is read |
| `--timeout S` | 10 | Per-request timeout |
| `--max-body BYTES` | 2097152 | Body cap; a longer body is truncated and the report says so |
| `--delay S` | 0.2 | Delay between requests to the site |
| `--user-agent S` | `Sitewalk/<version>` | The client identification sent |
| `--version` | — | Print the version and exit |

Exit status: **0** normally, **1** under `--strict` when an error finding exists, **2** when the
run could not be made at all — a bad argument, an unreadable directory, or a plan file that could
not be read.

## Tests

```sh
python3 -m unittest discover -s tests -t .   # the suite
make ci                                      # record checks, byte-compile, the suite, smoke checks
```

The suite runs with **no network**. `tests/fakes.py` replaces `socket.socket` and
`socket.getaddrinfo` with functions that raise, so a test that accidentally reaches the network
fails rather than passing on a connected machine. `--dir` is exercised against fixture directories
and `--url` against an injected fake connection.

`make ci` also runs `make records`, which checks the project's Perspicuity records mechanically.
That check is a spell-checker, not a reviewer: a clean result establishes none of the reasoning.

## Where the reasoning lives

- [`CONTEXT.md`](CONTEXT.md) — what this is, why it exists, what success and stopping look like.
- [`RECORD.md`](RECORD.md) — the project record: frame, objectives, alternatives, selection,
  units and review. The plan this tool is built under.
- [`docs/DESIGN.md`](docs/DESIGN.md) — the technical choices, each with its measurements and the
  alternatives rejected at that point.
- [`docs/records/`](docs/records/) — the sub-decisions, each naming its parent.
- [`AGENTS.md`](AGENTS.md) — how work is done here, including the standing constraints.
