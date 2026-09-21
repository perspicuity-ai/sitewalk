# Design

What `sitewalk` is made of, and the measurements and rejected alternatives behind each choice.
Written 2026-09-21 by Moss, registered in [`RECORD.md`](../RECORD.md) revision 2 before the
package existed.

The value of this page is not the diagram. It is the record of what was rejected, so the next
person does not relitigate it, and of the numbers, so a later reader can tell which choices were
measurements and which were judgement.

## The shape

One process, one pass, two interchangeable sources:

```
--url https://example.com ─┐
                           ├─► PageSource ─► facts + site findings ─► text or JSON report
--dir build/ ──────────────┘         ▲
                                     │
                          --plan site.json (optional, checks the facts)
```

Everything downstream of `PageSource` is shared. There is no second analysis path for the local
source, and that is the central structural decision:

**D1. One pipeline over a source abstraction, not two tools.**
`--dir` is the deploy gate, so what it reports must be exactly what `--url` would have reported
about the same bytes. Two code paths would let the gate and the live check drift, and the drift
would be invisible until a release passed a gate that no longer measured the thing it was
trusted for. The source is a small protocol — `read(path) -> Page`, `exists(path) -> bool` —
with an HTTP implementation and a filesystem implementation, both exercised by the same tests
against the same fixtures.
*Rejected:* a `--dir` mode that runs only the offline-cheap subset of checks (the "does it exist"
surfaces and nothing else). It would have been a simpler gate that passed more sites than the
live check would, which is worse than no gate.
*Rejected:* reading the directory through a `file://` URL so the HTTP client is reused verbatim.
`urllib`/`http.client` do not implement `file://`, and faking it would put an unguarded fake
address into the one module whose job is to be the security boundary.

**D2. The address guard is its own module and its own decision.**
`sitewalk/guard.py` holds every rule about which addresses may be connected to, and nothing else
in the package is allowed to decide that. `sitewalk/fetch.py` is the only module that opens a
socket, and it refuses to do so before clearing the guard.

**D3. Standard library only, and no JavaScript.**
A browser engine would answer a different question ("what does a rendering client see") than the
one the product asks ("what does a non-executing client see"). It is also a dependency of
several hundred megabytes in a tool that has to run in a deploy gate. The absence is reported
rather than hidden: see D6.

## Measurements

| Measurement | Value | Where it is used |
| --- | --- | --- |
| Requests per run, worst case | `1 (robots) + 1 (sitemap) + min(links, 5) (nested sitemaps) + max-pages` | D7, bounds |
| Default delay between requests | 0.2 s | D7 |
| Default per-request timeout | 10 s | D7 |
| Default body cap | 2 MiB (truncated, and said so) | D7 |
| Default crawl bound | 50 pages | D7 |
| Bounds on what is read | `--max-pages` is the only one; there is no separate link-check bound | D7 |
| Robots skips | Counted in the header and in `limits.paths_skipped_robots`; each quotes its rule verbatim | D8 |
| Text that looks script-rendered | `visible_text < 200` chars **and** (`script_bytes ≥ 5000` **or** an empty app-root marker) | D6 |
| Python floor | 3.11 — the principal's specification; confirmed present as 3.11.3 | D3 |

The 200-character and 5000-byte thresholds are judgement, not measurement: they were chosen to be
obviously below anything a server-rendered page emits and obviously above an empty shell, and
they are reported in the output as a heuristic so a reader can discount them. The exact numbers
are recorded here so that a later change to them is visible as a change.

## Decisions

### D1. One pipeline over a source abstraction

Chosen because the offline gate is the point of the product, and a gate is only worth trusting if
it measures the same thing the live check measures. `PageSource` has two methods; the analysis,
findings, plan check and report code cannot tell which implementation they were given.

Rejected: **two analysis paths** (the gate would drift from the live check, silently).
Rejected: **`file://` through the HTTP client** (not implemented by the standard library, and it
would put a fake address in front of the security guard).

### D2. Port the `agent-eligibility` address guard rather than import it

`/home/david/projects/agent-eligibility/eligibility/fetch.py` is Apache-2.0, the same
organisation, and its failure modes are known. It is a *port*: the rules are the same, the code
is rewritten against `sitewalk`'s own types, and `tests/test_guard.py` is `sitewalk`'s own.

The rules, in the order they are applied:

1. scheme must be `http` or `https`;
2. port must be 80 or 443 (explicit, or the scheme default);
3. the hostname is resolved first, and **every** answer must be a public address;
4. the connected peer address is checked again after connecting, which closes the DNS-rebinding
   gap a resolve-only check leaves open;
5. every redirect hop is re-validated from scratch, so a public host cannot bounce the crawl to
   `169.254.169.254`.

`is_public_address` is written out rather than inferred from `is_global`, because on some Python
versions a multicast address reports as global. IPv4-mapped IPv6 addresses are unwrapped to their
IPv4 form first, so `::ffff:127.0.0.1` is refused.

Rejected: **importing the module directly**. It would couple the two projects through a Python
path, and `CONTEXT.md` states the two are deliberately independent; the one interface between
projects is the plan file.
Rejected: **a hostname blocklist**. It is bypassed by a DNS record, which is the whole reason the
check is on the resolved address.
Rejected: **a resolve-only check without the post-connect peer check**. It leaves the rebinding
window open, and the cost of closing it is one `getpeername()` call.

### D3. Python 3.11+, standard library only

Specified by the principal. It also holds because the tool has to run inside someone else's
deploy gate without a build step or a virtual environment. `tests/` and the fixtures are the only
places that may grow, and they do not introduce imports outside the standard library either.

Rejected: **`requests` + `beautifulsoup4`**. Better ergonomics, and a supply-chain and
installation cost in every CI that gates on this tool.

### D4. `html.parser`, with an explicit ignore-depth counter

`html.parser.HTMLParser` is the only HTML parser in the standard library. It is not a tree
builder, so the collector tracks what it needs directly: the current `<title>`, meta tags, link
rel, `script`/`style` suppression by depth counter, and the anchors inside `<body>`.

Facts taken per page: status, content type, `<title>`, meta description, `<link rel=canonical>`,
the JSON-LD `@type` values, visible-text length, internal link count, and whether the page was
named in the sitemap.

Rejected: **regex extraction**. It is the classic way this kind of tool becomes quietly wrong — a
`<title>` inside a comment or an attribute value, an unclosed tag, or a `>` inside an attribute
all break it, and the breakage is invisible in the report.
Rejected: **a tree builder written here**. A tag-soup-tolerant tree is a large amount of code to
own for facts this shallow, and a tree invites deeper claims than the tool should make.

### D5. JSON-LD is read from `<script type="application/ld+json">` only

Every such block is parsed with `json.loads`; a block that does not parse is recorded as a
malformed-JSON-LD finding rather than silently skipped. `@type` values are collected from the
top level, from `@graph`, and from nested objects, and are de-duplicated in first-seen order so a
report is deterministic. A block that is a list is walked element-wise. `@type` may be a string
or a list of strings, and both are accepted.

Deliberately **not** done: microdata, RDFa, OpenGraph, or `itemtype` attributes. They are
different vocabularies, and `CONTEXT.md` limits the claim to what the server returns in the
formats this tool reads.

### D6. Script-rendering is a heuristic, and it is labelled as one

The tool never executes JavaScript, so a page whose content arrives after load looks empty. It
reports `looks_script_rendered: true` with the evidence (`visible_text_chars`, `script_bytes`,
`app_root_markers`) and the report says, in words, that the tool does not execute JavaScript and
that the length is not evidence the page is empty.

Rejected: **silence**, i.e. reporting `visible_text: 0` with no qualifier. That is the failure
`CONTEXT.md` explicitly forbids: implying a page is empty.
Rejected: **a headless browser**. A dependency, a security surface, and a different question.

### D7. Bounds are explicit, defaulted, and reported

`--max-pages 50`, `--timeout 10`, `--max-body 2097152`, `--delay 0.2`. The delay is applied
between requests to the same host, including the `robots.txt` and sitemap requests. Every bound is
reported in the JSON output under `limits`, and a truncated body or a reached page cap is a
finding, not a silent stop.

**`--max-pages` is the only bound on what is read.** An earlier revision had a second flag,
`--max-link-checks 20`, and it was removed during U1 because it was unreachable: the crawl loop
already fetches every internal link target it can reach, so it answers the link question for each
of them, and the separate link-check pass only ever had work left when the page bound had already
stopped the crawl. A flag that cannot change the outcome is worse than no flag, because it reads
as a guarantee. What is left unchecked is named in the notes, with the remedy (`--max-pages`).

Rejected: **no delay**. A tool meant to be run by strangers against sites they may not own should
be the politest thing on the network.
Rejected: **concurrency**. It multiplies the load on the subject's server and makes the delay
meaningless; a 50-page crawl is not slow enough to justify it.

### D8. `robots.txt` is obeyed for live crawls

`Disallow` rules that apply to our user agent (`*` or `sitewalk`) stop a path from being fetched;
the path is recorded as skipped, and a sitemap URL that was skipped counts as never reached.
**This holds in `--dir` mode too**, which reads the build's own `robots.txt` and honours it. There
is no request to disallow when the pages come from disk, but robots.txt is a statement about the
site's content rather than about the transport, and the consequence is that the two sources agree
on the same bytes — which is what makes the offline gate a gate (D1). A site whose `robots.txt`
disallows paths that a deploy check needs to see should be checked with the policy in mind.

Rejected: **ignoring `Disallow`**. The principal's instruction is to publish a tool others run;
a tool that ignores robots.txt is a tool that gets blocked, correctly.
Rejected: **honouring `Crawl-delay`**. It is not in the robots.txt standard, and the explicit
`--delay` is easier to reason about.

### D9. The plan file is read leniently about its version, and strictly about its types

`--plan site.json` reads the `siteplan` format ([`siteplan/CONTEXT.md`](../../siteplan/CONTEXT.md)
is authoritative; this module is the consumer and links there rather than restating the format).
Two things are **enforced**, because they are the two a built site can be checked against and this
tool can observe both:

* `required_surfaces` — the machine-readable files the site must publish;
* `identity.schema_types` — the Schema.org entity types the home page must carry in JSON-LD.

Everything else is read, reported as **not checked** with the reason, and otherwise ignored:
`offering` and `identity.fields` name Schema.org properties this consumer does not extract;
`url_rules` and `pages` are about URL shape and per-page purpose, which the crawl reports but does
not judge; `crawler_stance` is not observable from pages at all.

**Leniency is about the format's growth, not about its correctness.** Decided by the principal on
2026-09-21 (RECORD.md, Q3):

| Input | Behaviour | Why |
| --- | --- | --- |
| `plan_version` older, newer or absent | Read, not rejected. The output notes which revision the consumer was built against and says a met result does not mean the whole plan was verified | A consumer that rejects an unfamiliar version breaks the producer every time the format grows. `siteplan` has not confirmed the key is required, so its absence cannot be fatal either |
| A key this consumer does not know | Ignored, with a note naming it | Same reason, and it is the case that will actually happen |
| A known key of the **wrong type** | A problem, reported and gating | Leniency about growth is not leniency about malformation. A consumer that coerces `"schema_types": "Organization"` into a one-item list reports a plan as met when the plan was never well formed |
| `required_surfaces` as a bare string | Accepted | The meaning is unambiguous, and rejecting it costs a producer a release for nothing. This is the one coercion, and it is opt-in per key |
| A file that cannot be read, or is not JSON, or is not an object | Exit 2 | A gate that cannot read its own plan must not report a pass |

The strict-type rule was found by testing rather than by reasoning: the first implementation
coerced a bare string for every list-valued key, so a malformed `identity.schema_types` passed.

Rejected: **enforcing everything the format can express.** Three of the keys are not observable
from the pages this tool reads, so enforcing them would mean reporting checks that were not
performed, inside the one product whose constraint is that it claims nothing beyond observation.
Rejected: **failing on unknown keys.** It forces lockstep releases between two deliberately
independent projects. Rejected: **coercing every list-valued key**, which is how a malformed plan
becomes a met plan.

### D10. Findings have severities, and the gate is a policy over them

**The report states what is true; the gate decides what is tolerable.** Three severities, defined
in the output so a machine reader never infers one from an exit code:

| Severity | Meaning | `--strict` |
| --- | --- | --- |
| `error` | Something is wrong with the site as built | exits 1 |
| `conditional` | The verdict depends on something this consumer does not know: an unknown or newer plan version, an absent or mistyped one, or a required surface it has no check for | exits 1 |
| `info` | An observation or a site's own choice, with nothing left unknown | no effect |

`--strict` maps severities to an exit code and **never creates a finding**. That separation is the
point: whether a plan's version is unknown is a fact about the file, and whether that fact should
fail a build is a policy. If the flag created findings, two runs of the same site against the same
plan could disagree about what is true, and comparability is the only thing that makes a report
checkable. The mapping is a table (`facts.GATING_SEVERITIES`) rather than a condition buried in the
exit path, so the policy is readable without reading the code.

Rejected: **gating on notes**. A missing `llms.txt` is a design choice of the site, not a defect
introduced by the change under test, and a gate that fails on choices gets disabled.
Rejected: **letting `--strict` create the conditional finding.** It would make the report a
function of the flag rather than of the site.

## What is deliberately absent

- **No JavaScript execution, and no headless browser.** See D3, D6.
- **No outbound requests off the submitted origin.** No external APIs, no font or asset fetching,
  no CDN, no link checking of external links. An internal link is one whose host is the origin;
  everything else is counted as external and never requested.
- **No persistence.** No database, no cache file, no state between runs. Reports are stdout.
- **No accounts, cookies or tracking.** The client sends no cookie, and no credential is stored
  or read from the environment.
- **No PII.** Only published pages are read, and only structural facts are recorded.
- **No ranking, citation, traffic or recommendation claims.** Not measured, not predicted, not
  implied.
- **No sitemap generation, no site building, no deployment.** This reports on a site; it does not
  change one.
- **No `siteplan` code dependency.** The coupling is the plan file alone.
