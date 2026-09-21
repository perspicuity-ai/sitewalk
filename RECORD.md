---
format: perspicuity-work/1
id: sw-project
revision: 1
skill_version: 0.5.0
updated: 2026-09-21
created_at: "2026-09-21T11:48:05-06:00"
updated_at: "2026-09-21T11:52:00-06:00"
record_status: open
work_status: active
---

# Sitewalk

The project record. Parent of every record in this repository, and the continuing account: what
is true now, what was inherited, the plan, and the review.

## Current position

Mode: **`Run`**. The principal prescribed the frame, the tool and its specification in the
session that opened this record, so there is no frame for this worker to select or ratify. The
mode is declared here because the record guide requires an opening record to name it.

Principal: David. Decider: David.

Work owner: Moss (coordinator).

Decision: `inherited` — the product frame, the claim boundary and the tool specification are the
principal's, given 2026-09-21 and reproduced below under Frame and Decide. The choices Moss made
within that grant are the design decisions in [`docs/DESIGN.md`](docs/DESIGN.md), registered
before the package existed.

Work scope: `sitewalk` unit 1 — the deliverable this session owns is the first working
`sitewalk`, as one package with two sources (`--url`, `--dir`), the plan check, the report and
`--strict`, together with its no-network test suite and the project's own checks. Naming
(`docs/ACTORS.md`) and this registration are part of it because both had to exist first.

Work: revision 1 registers the basis. Named Moss and recorded the roster
([`docs/ACTORS.md`](docs/ACTORS.md)); registered the design decisions and measurements
([`docs/DESIGN.md`](docs/DESIGN.md)); registered unit 1's pickup plan and acceptance criteria
below. No package code exists at this revision, deliberately.

Outcome: unknown. Nothing has been observed yet.

Next: Moss — build unit 1 against the registered pickup plan, commit it, then observe the
acceptance run and amend this record with the evidence.

Dependency: nothing blocks unit 1. Two inputs are unresolved and named under conditions: the
`siteplan` project holds no code yet, so the plan-file format is implemented from its
[`CONTEXT.md`](../siteplan/CONTEXT.md) example; and no project in this workspace has a built
`build/` directory yet, so the offline gate will be accepted against fixtures until a real one
exists.

Review due: 2026-10-05 — see Review; the delivery is accepted against criteria registered below,
and the benefit claims in `CONTEXT.md` remain unobserved.

Authority: David, the principal, retains spending, outbound messages, external agreements and
the release word for publication. Everything inside this record's scope is delegated to Moss,
including reversible implementation details. Unit 2 is registered but not granted: it needs the
principal's word before it runs.

| Stage | began_at | registered_at / exact basis revision | finished_at |
| --- | --- | --- | --- |
| Frame and Decide | 2026-09-21T11:49:00-06:00 | 2026-09-21T11:52:00-06:00 — this revision, revision 1 | 2026-09-21T11:52:00-06:00 |
| Act | 2026-09-21T11:52:00-06:00 | 2026-09-21T11:52:00-06:00 — revision 1, unit 1 pickup plan | pending |
| Review | pending | 2026-09-21T11:52:00-06:00 — revision 1, Review criteria | pending |

## Frame and Decide

The frame is the principal's, stated in [`CONTEXT.md`](CONTEXT.md) and restated here with its
source. It is reproduced because this record is the parent a reader arrives at, and because the
tool implements it.

**The problem.** The evidence is one audit. On 2026-09-21 the `agent-eligibility` check was run
against `findmynextbite.food` and reported "no JSON, XML or API surface was linked from the home
page", while that site's sitemap lists 26 URLs and it publishes a public `/api/discovery`
endpoint. The check was not wrong; it reads one page. Nothing in this workspace can tell you how
a site functions beyond its front door. The moment that matters most is before a deploy, when the
question is whether a change broke how the site presents itself to machines, and nothing answers
it.

**The claim boundary.** `sitewalk` reports what is observable in the output the server returns.
It does not execute JavaScript, so it cannot see what a browser would render after load, and it
says so rather than implying a page is empty. It does not predict whether an agent will find,
trust or recommend a site, and it does not measure ranking, citations or traffic.

| Fundamental objective | Source | Measure, direction and horizon |
| --- | --- | --- |
| A structural map good enough to gate a deploy | David, [`CONTEXT.md`](CONTEXT.md) outcome 1, 2026-09-21 | `sitewalk --dir build/` completes with no network access and exits non-zero under `--strict` when findings exist. Direction: more real regressions caught, fewer false gates. Horizon: before the next release of any project that adopts it. |
| A public tool others can run | David, [`CONTEXT.md`](CONTEXT.md) outcome 2, 2026-09-21 | Documented install, standard library only, and a test suite that runs with no network and no special hardware. Direction: more projects running it. Horizon: this session for the artefact; adoption is later. |
| Nothing claimed beyond observation | David, [`CONTEXT.md`](CONTEXT.md) claim boundary, 2026-09-21 | Every claim in the output is traceable to bytes the tool read, and the no-JavaScript limit is stated in the output itself. Direction: fewer implied claims. Horizon: continuous. |

The third objective is the principal's constraint, not this worker's addition. It is listed
because it is the one most easily lost while implementing the first two.

| Material condition | Type | Basis | Affects |
| --- | --- | --- | --- |
| Mode `Run`; naming, record and tool are prescribed | Given | Principal's assignment, 2026-09-21 | Everything in unit 1; no frame is selected here |
| Python 3.11+, standard library only | Given | Principal's specification; Python 3.11.3 observed in this workspace 2026-09-21 | D3; rules out any parser or HTTP library |
| The address guard is ported from `agent-eligibility/eligibility/fetch.py` | Given | Principal's instruction; Apache-2.0, same organisation; the file read 2026-09-21 | D2; fixes the rule set before the code |
| The plan file format is owned by `siteplan`, version 1 | Given | [`siteplan/CONTEXT.md`](../siteplan/CONTEXT.md), read 2026-09-21: `plan_version`, `site`, `kind`, `required_surfaces`, `identity.schema_types`, `identity.fields`, `offering.schema_types`, `url_rules`, `crawler_stance`, `pages` | D9; only two of them are observable |
| No JavaScript execution | Given | [`CONTEXT.md`](CONTEXT.md), deliberate exclusion | D3, D6; forces the script-render heuristic to be reported rather than resolved |
| The corpus rule and Perspicuity 0.5.0 govern the records | Given | [`AGENTS.md`](AGENTS.md), [`docs/RECORDS.md`](docs/RECORDS.md); skill read 2026-09-21 | Registration order, the `in_review` state, the checker |
| No committed revision exists in this repository | Given | `git log` empty, 2026-09-21 | U1 must commit; the registration commit must precede the package commit |
| Whether built bytes equal served bytes is unknown | Uncertainty | No project here has a `build/` output yet | D1's equivalence claim; `--dir` is accepted against fixtures this session |
| The false-positive behaviour of the gate is unknown | Uncertainty | No site has been run through it | U1's gate criterion; a noisy gate gets disabled by the projects it should gate |
| `is_global` differs across Python patch releases for some ranges | Assumption | The port's own docstring in `agent-eligibility/fetch.py`; not re-measured here — re-checking the exclusions against the interpreter in use would challenge it | D2; the reason the address exclusions are written out rather than inferred |
| A build directory's file paths correspond to the site's URLs | Assumption | Implied by the deploy-gate use case; a build with a different URL scheme, or a site assembled by a CDN, would challenge it | `--dir` mapping, and the scope of what the offline gate can claim |
| `sitemap.xml` is small enough to read whole | Assumption | A sitemap is a bounded file by convention; a sitemap larger than `--max-body` would challenge it, and is reported as truncated | Sitemap collection |

### Reframe considered

`CONTEXT.md` sets the problem as "how a site functions beyond its front door". A broader frame —
including HTTP response headers, redirect chains, TLS, and the behaviour of the deployed site —
would catch more real regressions. It was not adopted, because the principal's specification, the
claim boundary, and the offline requirement all bound the tool to what it can read from a page's
body. It is recorded rather than silently dropped: if the gate later proves too narrow to catch
the regressions that matter, that is the reframe to return to, and it is a decision for the
principal, not for this worker.

### Alternatives and consequences

The alternatives compared here are for **how unit 1 is built**, which is the choice this record
owns. The frame, the product and the specification are the principal's and were not compared.

| # | Alternative | Consequences | Verdict |
| --- | --- | --- | --- |
| A | One pipeline over an interchangeable `PageSource`; ported address guard; `html.parser`; stdlib only; findings split by severity | The offline gate and the live check cannot disagree about the same bytes. One code path to test. Cost: a source abstraction and a page model that the simple case does not need | **Chosen** |
| B | Two paths: a fast offline checker for surfaces and links, and a separate live crawler with the full facts | Less initial code, and each path tuned to its case. Cost: the gate measures a subset, so a release passes a gate that never checked the facts the live run reports — a silent false pass, which is worse than no gate | Rejected |
| C | `--dir` reads through `file://` so the HTTP client is reused verbatim | Zero new source code. Cost: the standard library does not implement `file://` in `http.client`, so this means a fake or a third-party reader in the one module that is the security boundary | Rejected |
| D | Use `requests` and `beautifulsoup4` for parsing and fetching | Faster to write, better tolerances. Cost: a dependency in every CI that gates on the tool, and a supply-chain surface in the module that already fetches stranger-supplied URLs | Rejected |
| E | Execute JavaScript in a headless browser to see rendered pages | Answers what a rendering client sees. Cost: a browser engine as a dependency in a deploy gate, and a different question from the one the product asks | Rejected |
| F | Gate on every finding, including notes such as a missing `llms.txt` | Stricter gate. Cost: it fails on the site's design choices rather than on the change under test, and a gate that fails on choices is disabled — at which point it gates nothing | Rejected |
| G | Enforce the whole plan format (`url_rules`, `crawler_stance`, `offering`, `pages`) | Stronger plan adherence. Cost: three of those are not observable from the pages this tool reads, so the tool would report checks it did not perform, inside the one product whose constraint is that it claims nothing beyond observation | Rejected |

Decisive tradeoff: **A against B**. Both deliver the first two objectives. They differ on the
third: B makes a claim ("the build passes") that the same tool would contradict on the live site,
and the difference would be invisible in a CI log. The preference it rests on is the principal's
claim boundary — an unverified pass is the failure mode `CONTEXT.md` is written against.

What would warrant reconsideration: if a real build directory turns out to be unrepresentable as
URLs (a CDN-assembled site, or a build whose paths differ from its routes), D1's equivalence
claim fails and the offline source needs its own stated scope. If the tool's first runs on real
sites produce findings the adopters judge wrong, F's severity split is the first thing to revisit.

The detailed technical decisions — parsing, bounds, robots handling, the script-render heuristic,
plan leniency — are D1–D10 in [`docs/DESIGN.md`](docs/DESIGN.md), with their measurements and
their rejected alternatives. They are linked rather than repeated.

### Selection

`selected_at` 2026-09-21T11:52:00-06:00. Decider: David, by the specification given in this
session. Basis revision: revision 1 of this record. The selection is alternative **A**, with
D1–D10 as its technical detail, and unit 1 as the delivery. Moss made no selection outside this
grant; the design choices inside it are recorded in [`docs/DESIGN.md`](docs/DESIGN.md) with the
alternatives rejected at each point.

### Decision index

| Record | Owner | State | Depends on |
| --- | --- | --- | --- |
| This record — the project frame and unit 1 | Moss | open, active | Principal's assignment, 2026-09-21 |
| [`docs/DESIGN.md`](docs/DESIGN.md) — D1–D10, the technical choices and their measurements | Moss | registered 2026-09-21, revision 1 | This record's frame and objectives |
| `docs/records/` — subordinate decisions | — | empty | A choice meeting the admission test in [`docs/RECORDS.md`](docs/RECORDS.md#when-a-record-is-required); naming, records registration and the tool build are inside this record's scope instead |

## Act

Unit 1 proceeds under the `Run` grant below. Its pickup plan is registered here, before the
package exists, because the acceptance criteria must be saved before the outcome is known.

### The grant

**Actor:** Moss. **Scope:** build the `sitewalk` package, its tests, its fixtures, `README.md`,
`docs/DESIGN.md`, the project's own checks in `scripts/check-project.sh`, and the commit history;
amend this record with the observed evidence; correct the process documents where they
contradict the installed skill or the project.

**Excluded:** any network request beyond the live crawl the tool itself performs when a person
runs `--url`; any commit to a remote; any push, publish, deploy or spend; any new dependency; any
file outside this repository except reading the sibling projects, which is permitted and named.

**Stop condition:** unit 1 is delivered and this record carries the evidence, or a material
finding changes the frame, the comparison or the selection — in which case the unit stops and
returns to the decider.

### Unit 1 pickup plan

How it will be carried out: build `sitewalk/` as one package — address guard, HTTP source,
filesystem source, HTML fact collector, sitemap and robots reader, crawl loop, plan check,
findings, report, CLI — then the tests, then the checks, then the documents. Sources:
`agent-eligibility/eligibility/fetch.py` for the guard's rules; `siteplan/CONTEXT.md` for the
plan format. Route adaptations inside the grant are Moss's call.

| # | Result | Inputs / dependencies | Owner, timing | Done when | Actual evidence |
| --- | --- | --- | --- | --- | --- |
| U1 | `sitewalk` unit 1: package, tests, fixtures, README, DESIGN, project checks, commits | The principal's specification; `agent-eligibility/eligibility/fetch.py` (read); Python 3.11.3 | Moss, session of 2026-09-21, built in this session | Every acceptance criterion below passes on the committed revision | Pending |
| U2 | An independent run of the gate against a real built directory, by a project that is not this one | A `build/` output from another project; that project's owner | Not granted — needs the principal's word and a willing project | Registered only, pending the principal's word | Not started |

**Acceptance criteria for U1**, registered before the work:

1. `python3 -m sitewalk --dir <fixture-dir>` produces the report with no network access
   attempted, and the same analysis the live source would produce from the same bytes.
2. Every per-page fact the principal listed is in the output: status, content type, title, meta
   description, canonical, JSON-LD `@type`s, visible-text length, internal-link count, and
   sitemap membership.
3. Every site-wide finding the principal listed is produced: page count and status distribution;
   sitemap URLs never reached; orphan pages; duplicate titles; duplicate descriptions; missing
   titles; cross-host canonicals; pages with no JSON-LD; internal links that do not return 200;
   and the existence of `robots.txt`, `sitemap.xml` and `llms.txt`.
4. `--plan site.json` checks `required_surfaces` and the home page's `identity.schema_types`,
   ignores unknown keys without failing, and errors non-zero on a plan it cannot read.
5. Exit 0 normally; exit non-zero under `--strict` when error-severity findings exist.
6. The guard refuses a non-http(s) scheme, a port other than 80/443, and a host resolving to a
   private, loopback, link-local, multicast, reserved or metadata address, and re-checks the
   connected peer after connecting. Tested against injected fakes, with no network.
7. `python3 -m unittest discover -s tests -t .` passes with no network available.
8. `make ci` exits 0 and `make records` is clean.
9. The output states the no-JavaScript limit, labels the script-rendered heuristic as a
   heuristic, and never claims anything about ranking, citations, traffic or recommendation.

## Review

Criteria registered before the outcome was known. Delivery acceptance is separate from the
benefit claims in `CONTEXT.md`, which this session cannot observe.

| Criterion | Evidence source | Owner, window or trigger | Finding | Response |
| --- | --- | --- | --- | --- |
| Delivery: acceptance criteria 1–9 for U1 | The committed revision, `make ci`, the fixture run, `tests/` | Moss, at delivery, 2026-09-21 | Pending | Pending |
| The offline gate and the live source agree on the same bytes | The fixture directory, read by both sources in one test | Moss, at delivery, 2026-09-21 | Pending | Pending |
| The address guard refuses what it must, including the post-connect peer check | `tests/test_guard.py` with injected resolver and connector fakes | Moss, at delivery, 2026-09-21 | Pending | Pending |
| Independent assessment of the delivery, by a worker that did not write it | A named assessor's return against criteria 1–9 | Principal to grant; not before delivery | Pending | Pending |
| Benefit: the gate catches a real regression in a project's release path | That project's CI log, and the release it stopped or did not stop | Principal and that project's owner; trigger is U2 running | Unobserved — `CONTEXT.md` success condition | Carry as U2 |
| Benefit: at least two projects run it | Their repositories and CI configurations | Principal; trigger is a second project adopting it | Unobserved — `CONTEXT.md` success condition | Carry as U2 |
| Benefit: it reports more than the sitemap already says | A run against a real site, compared with its sitemap | Principal; trigger is the first live run by anyone | Unobserved — `CONTEXT.md` failure condition | Carry as U2 |

## Changes

Revision 1, 2026-09-21. Created and registered. Source: the principal's assignment of
2026-09-21 and [`CONTEXT.md`](CONTEXT.md); the installed Perspicuity skill 0.5.0, whose record
format this follows. Reason: the corpus rule requires the frame, the conditions, the selection
and unit 1's acceptance criteria to exist before the work that depends on them. Affects: all of
unit 1; the package had not been written when this revision was saved. No package code exists at
this revision, deliberately — the registration commit precedes it.
