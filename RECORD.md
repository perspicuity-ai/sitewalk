---
format: perspicuity-work/1
id: sw-project
revision: 2
skill_version: 0.5.0
updated: 2026-09-21
created_at: "2026-09-21T11:48:05-06:00"
updated_at: "2026-09-21T12:44:00-06:00"
record_status: open
work_status: submitted
---

# Sitewalk

The project record, and now the **Statement of Work** for `sitewalk`. It is the parent of every
record in this repository and it carries the continuing account: what is true now, the frame, the
conditions, the alternatives, the recommendation, the units, and the review.

## Current position

Mode: **`Plan`**. The principal changed the mode in a direct instruction on 2026-09-21, after
this record had been registered and acted on in `Run`. The earlier mode is preserved here with
its reason: revision 1 declared `Run` because the principal's first message prescribed the frame,
the tool and its specification in full, leaving nothing to select. The change is recorded because
the work's purpose changed — the principal now wants the basis, the alternatives and the units
ratified **before** implementation, and a planning run stops at that boundary even though the
authority to act already exists. This revision is the statement of work and the grant request;
it selects nothing.

Principal: David. Decider: David. Moss prepares the basis and recommends; Moss does not ratify.

Work owner: Moss (coordinator).

Decision: `pending` — **David ratifies the course of action and the grant; Moss does not select.**
The product frame, the claim boundary and the tool specification are `inherited` from the
principal (2026-09-21, [`CONTEXT.md`](CONTEXT.md)) and are reproduced as inherited below, not
reopened. The choice now pending is which of the five alternatives in this revision to build,
and on what grant.

Work scope: The Statement of Work itself, and the ratification it asks for. The delivery this
record would own once ratified is the `sitewalk` package as scoped in Act below — units U1–U5,
not U0.

Work: revision 2 registers this basis **and accounts for work that was produced ahead of it**
(see *Work already in the tree* below: 15 modules, 2,592 lines of package; 9 test modules and
13 fixture files, 2,378 lines of test code; 240 tests, 238 passing, 2 failing). None of it is
committed, none of it is covered by a ratified plan, and none of it is ratified by this revision
merely by being described.

Outcome: unknown. Nothing has yet been observed against a real built site or a real live site.

Next: David — read this Statement of Work, answer the open questions that block him (the U4
domain grant is the one that gates the most), and either ratify one of the alternatives and the
grant requested in Act, or send it back with the changes he wants.

Dependency: Nothing blocks this planning increment. The whole of Act is blocked on the
ratification decision, as a planning run requires.

Waiting on: David (principal), for the ratification and for the open questions in Act.

Review due: 2026-10-05 — see Review. The delivery criteria are registered below and are not yet
assessable, because no ratified delivery exists. The benefit claims in `CONTEXT.md` are
unobserved and need a real site.

Authority: David retains **spending, outbound messages, external agreements and the release word
for publication**. Revision 1's grant covered the `Run` increment that produced the code now in
the tree; this revision supersedes that grant with the one requested in Act. Nothing outside the
requested grant is authorised, and no ratification exists until David gives it.

| Stage | began_at | registered_at / exact basis revision | finished_at |
| --- | --- | --- | --- |
| Frame and Decide (Run, revision 1) | 2026-09-21T11:49:00-06:00 | 2026-09-21T11:52:00-06:00 — revision 1 | 2026-09-21T11:52:00-06:00 |
| Frame and Decide (Plan, revision 2) | 2026-09-21T12:14:00-06:00 | 2026-09-21T12:44:00-06:00 — **this revision** | 2026-09-21T12:44:00-06:00 |
| Act | pending — waits on ratification | pending | pending |
| Review | pending | 2026-09-21T12:44:00-06:00 — revision 2, Review criteria | pending |

## Frame and Decide

### The problem

The evidence is one audit. On 2026-09-21 the `agent-eligibility` check was run against
`findmynextbite.food` and reported "no JSON, XML or API surface was linked from the home page",
while that site's sitemap lists 26 URLs and it publishes a public `/api/discovery` endpoint. The
check was not wrong; it reads one page. Nothing in this workspace can tell how a site functions
beyond its front door, and the moment that matters is before a deploy, when the question is
whether a change broke how the site presents itself to machines.

`sitewalk` answers that question from the output a server returns: a structural map of a built
site read offline from a directory, or of a live site crawled inside its own origin.

**The standing claim boundary, inherited and not reopened.** `sitewalk` reports what is
observable in the output the server returns. It does not execute JavaScript, so it cannot see
what a browser would render after load, and it says so rather than implying a page is empty. It
does not predict whether an agent will find, trust or recommend a site, and it measures no
ranking, citation or traffic.

### Objectives

| # | Objective | Source | Measure and direction | Horizon |
| --- | --- | --- | --- | --- |
| O1 | A structural map good enough to gate a deploy | David, [`CONTEXT.md`](CONTEXT.md) outcome 1, 2026-09-21 | `sitewalk --dir build/ --strict` runs with no network access and exits non-zero when error-severity findings exist. Direction: real regressions caught up, false gates down | Before the next release of any adopting project |
| O2 | A public tool others can run | David, [`CONTEXT.md`](CONTEXT.md) outcome 2, 2026-09-21 | Standard library only; documented install; test suite runs with no network and no special hardware. Direction: more projects running it | This increment for the artefact; adoption later |
| O3 | Nothing claimed beyond observation | David, [`CONTEXT.md`](CONTEXT.md) claim boundary, 2026-09-21 | Every claim in the output traceable to bytes read; the no-JavaScript limit stated in the output itself. Direction: fewer implied claims | Continuous |
| O4 | The basis, alternatives and units are reviewable before implementation | David, direct instruction, 2026-09-21 | This revision: the frame, five alternatives, a recommendation, units with estimates, and a grant request, saved before any of the work is ratified. Direction: the decider can reject or amend the plan | This session |

O3 is the principal's constraint rather than this worker's addition, and it is the objective most
easily lost while pursuing O1 and O2. O4 is the reason this revision exists and is the only
objective that this session can fully satisfy.

### Material conditions

**Givens** — established conditions, with a source and a date.

| Given | Source, date | Affects |
| --- | --- | --- |
| Mode is now `Plan`; the deliverable is a Statement of Work and the run stops at the grant request | David, direct instruction, 2026-09-21 | The whole of this revision; nothing may be implemented |
| Work exists in the tree produced under the earlier `Run` grant | `git status`, 2026-09-21 — uncommitted | The Act account and every alternative below |
| Python 3.11+, standard library only | David, [`CONTEXT.md`](CONTEXT.md); Python 3.11.3 observed in this workspace 2026-09-21 | Every unit; rules out any dependency |
| The SSRF guard is ported from [`agent-eligibility/eligibility/fetch.py`](../agent-eligibility/eligibility/fetch.py) | David, direct instruction; Apache-2.0, same organisation; file read 2026-09-21 | U2; fixes the rule set before the code |
| The plan file format is owned by `siteplan`, version 1 | [`siteplan/CONTEXT.md`](../siteplan/CONTEXT.md), read 2026-09-21 | U3; only two of its keys are observable |
| No JavaScript execution, no external APIs, no accounts, no off-origin crawling, no PII | David, [`CONTEXT.md`](CONTEXT.md), deliberate exclusions | All units; bounds what may be claimed |
| Two commits exist, neither containing package code | `git log`, 2026-09-21: `361257e` template, `6d11719` record registration | U1; the unratified work is uncommitted and therefore cleanly rejectable |
| Perspicuity 0.5.0 governs the records; `make records` is clean at revision 2 | Installed skill; `make records`, 2026-09-21 | Every revision of this record |

**Uncertainties** — what is not known, and what would resolve it.

| Uncertainty | What would resolve it | Affects |
| --- | --- | --- |
| Whether this tool is usable against a real built site, and what a real build's paths look like | Running it against a real `build/` directory from another project | O1; U1's acceptance and U4's value test |
| The false-positive rate of the gate on real sites | The same runs, with the adopting project judging the findings | O1; whether the gate survives being switched on |
| Which of the guard's refusals actually fire against real hostile input | Adversarial review by an assessor who did not write it, plus live testing | U2; the security claim |
| Whether a live run is necessary for the product's value at all | A period of offline gate use, or a project that needs the live path | Alternative E; whether U3 is worth building now |
| Whether the principal wants a sub-record per consequential choice in `docs/records/` | David's answer to open question Q4 | O4; how the corpus is organised |

**Assumptions** — provisionally treated as true, with what would challenge each.

| Assumption | Why used | What would challenge it |
| --- | --- | --- |
| A build directory's file paths correspond to the site's URLs | Implied by the deploy-gate use case | A CDN-assembled site, or a build whose paths differ from its routes |
| The existing package is salvageable rather than a rewrite | It is tested, its guard is ported from a tested implementation, and 238 of 240 tests pass | Failing its facts contract in U1's verification: a module that cannot be traced to a criterion is removed, not repaired in place |
| `is_global` differs across Python patch releases for some address ranges | Stated in the ported module's own docstring; not re-measured here | Re-checking the address exclusions against the interpreter in use |
| The principal will accept a report written to a file or stdout, and published by nobody until he says so | Publication is his retained decision | Any request to publish a report about a third party's site |

### Alternatives

Five complete courses of action. **A is what the existing work represents**; **B rejects it
entirely**; **C and D build less**; **E drops the interface between the two projects**.

| # | Course of action | What it delivers | Consequences | Evidence or judgement |
| --- | --- | --- | --- | --- |
| **A** | **Ratify the full scope, but verify before keeping.** The existing package is treated as a proposal: each module is checked against the registered facts contract, anything untraceable to a criterion is removed, and only then are U2–U5 built | O1, O2, O3, and the `--plan` interface | Fastest route to a working tool. **Risk: this is a receipt rather than a plan** — a plan that ratifies finished work judges nothing. The mitigation is that U1 has teeth: it re-derives every promised fact and finding from the fixtures, and the plan pre-commits to deleting whatever fails | Judgement, with one measurement: the code exists and 238 of 240 tests pass |
| **B** | **Discard the tree and rebuild from this plan alone** | O1, O2, O3, on a clean basis | The plan would be genuinely prior to the work, which is the strongest form of the corpus rule. Cost: 2,592 lines of package, 2,378 lines of test, and the hard-won parts — the parser flush bug, the dead link-check bound, the fixture that lied about its own title — are rediscovered at the same cost. No evidence says the rebuild would be better | Judgement |
| **C** | **Build only the offline gate.** `--dir`, discovery, facts, findings, report, `--strict`. No URL mode, no guard, no plan check | O1 only, and part of O3. Also O2 partially: a smaller tool is easier for others to run | Removes the highest-risk code and the most work, and reaches O1 soonest. Cost: the principal's specification names `--url` and `--plan`, so C delivers less than was asked for. The guard is not built and the tool cannot be pointed at a live site at all | Judgement |
| **D** | **Adopt the architecture, defer the riskiest parts.** U1–U2 now (offline gate verified; guard tested); `--plan` and `--url` deferred to a second increment | O1 now; O2 and O3 now; the deferred parts later | Reaches the deploy gate soonest while keeping the deliverable intact. Cost: a second increment means the plan format may move under `siteplan` before the consumer is built — which is an argument for deferring the *consumer*, not against it | Judgement |
| **E** | **Drop the plan-file interface.** `sitewalk` reports the site's structure; whether the site matches a brief stays `siteplan`'s business | O1 and O3, without the cross-project coupling | Removes the only interface between two deliberately independent projects, which [`CONTEXT.md`](CONTEXT.md) calls out as the one coupling it does want. Cost: no answer to "did this build follow its plan", a question a deploy gate is well placed to ask | Judgement; the `siteplan` format exists and is version 1 |

**Decisive tradeoff: A against B.** Both reach the same objectives. B satisfies the corpus rule
most cleanly, because nothing precedes the plan. A is faster and risks ratifying work nobody
judged. The preference this rests on is the principal's: he asked for a plan that **can reject
all of it**, which is a requirement about the plan's authority, not about the code's fate. A
satisfies that requirement if and only if U1 can genuinely delete modules — so U1 is written as
an independent re-derivation with a pre-commitment to remove what fails, and its estimate is
sized accordingly.

**What would warrant reconsideration:** if U1's verification finds that the facts contract is met
mainly by tests written after the code rather than by the code, A collapses into B and the honest
move is to rebuild the affected modules. If a real build directory turns out not to map onto URLs
(D1 in [`docs/DESIGN.md`](docs/DESIGN.md)), the offline source needs its own stated scope and O1
weakens for CDN-assembled sites.

### Recommendation

**Recommendation: A, with U1's verification and removal power intact — or D if the principal
wants the deploy gate sooner and is willing to see `--url` and `--plan` in a second increment.**
Moss recommends **A**; Moss does not select.

The tradeoff A accepts is that the plan arrives after the code, so its judgement of that code is
weaker than a plan written first. It is bought back by giving U1 the authority to delete.
**Build order inside A: the offline gate first.** `--dir` is O1, it is the mode the principal
said matters most, it can be verified mechanically and offline in this workspace, and it needs no
guard, no resolver and no external permission. The guard comes second because it is the
highest-risk code: it decides whether this tool may be pointed at a stranger's server at all, and
an error in it is the one failure that would matter beyond this project.

### Selection

`pending`. `selected_at` not reached. Decider: David. Basis revision: this revision (2). Moss has
recommended and requests the grant in Act; no alternative is selected and no unit may start until
David ratifies.

### Decision index

| Record | Owner | State | Depends on |
| --- | --- | --- | --- |
| This record — frame, alternatives, units U1–U5, grant request | Moss | open, submitted | David's ratification |
| [`docs/DESIGN.md`](docs/DESIGN.md) — D1–D10, the technical choices and their measured thresholds | Moss | written before this plan, not ratified as design | This revision's alternatives; its contents are inputs to U1, not decisions this plan adopts |
| `docs/records/` — subordinate decisions | — | empty; no sub-record filed | Open question Q4 |

## Act

### Work already in the tree, produced ahead of this plan

This is the account the principal asked for. It is **uncommitted**, it sits outside any ratified
plan, and this revision does not ratify it by describing it.

| What | Measure (2026-09-21) | State |
| --- | --- | --- |
| `sitewalk/` — 15 modules | 2,592 lines: pages 348, findings 328, report 244, crawl 242, sources 217, plan 210, fetch 191, guard 187, cli 182, facts 159, sitemap 114, urls 82, `__init__` 48, errors 30, `__main__` 10 | Present, uncommitted, unratified |
| `tests/` — 9 modules plus `fakes.py` | 2,378 lines, including a no-network harness that replaces `socket.socket` and `socket.getaddrinfo` with functions that raise | Present, uncommitted, unratified |
| `tests/fixtures/` — 2 sites, 13 files | A 12-page site carrying every finding the specification names, plus a bare site for the missing-surface cases | Present, uncommitted, unratified |
| `make records` | Clean, including `skill_version: 0.5.0` and the corrected checker path | True |
| `make ci` | **Exits 0, and establishes nothing**: `scripts/check-project.sh` still contains the template's stub, so no project check runs at all — the two failing tests below do not fail the build | True, and the more dangerous of the two states; U1 fixes it |
| `python3 -m unittest discover -s tests -t .` | **238 of 240 pass**; the two failures are diagnosed below | True |

**The two failures, diagnosed and deliberately not repaired** — repairing them would be
implementation. `tests/test_cli.py::LiveModeOverTheFakeConnection` patches
`sitewalk.guard.default_resolver` and `sitewalk.fetch.default_connector` at test time, but
`LiveSource` binds both as dataclass defaults when the class is defined, so the patch never
reaches the source and the test attempts a real DNS lookup. The no-network harness turns that
into a hard failure, which is the harness working as designed. It is a genuine design defect
rather than a test-only defect: **the command-line entry point cannot be exercised offline at
all**, because the live source's network dependencies are not injectable through it. U2 owns the
fix.

**What the earlier increment learned, kept because it makes the estimates honest:** a fixture
written by hand claimed `landing.html` had an empty `<title>` while the file had no `<title>` at
all, and the tool correctly reported the file. Two real defects were found by tests rather than by
reading: the parser was never flushed, so a document ending in an empty `<title>` reported no
title at all; and a second bounding flag for link checks was unreachable, because the crawl loop
already answers every link it can reach, so `--max-pages` is the only bound that binds. The
second was removed rather than kept as dead configuration.

### The grant requested

**Actor:** Moss (coordinator).

**Included:** the units U1–U5 below, in the stated order; the power to amend or delete unratified
code that fails a registered criterion; to write and run tests; to write `README.md`,
`docs/DESIGN.md` and `scripts/check-project.sh`; and to commit locally in coherent commits.

**Excluded:** any push, publish, deploy or spend; any new dependency; any network request other
than the single live run U4 requires, to the domain David names; any editing of the `siteplan`
repository; any change to another project's repository; any contact with another project's owner
without the principal's word.

**Stop condition:** U1–U4 delivered with U5's documents, and this record amended with the
evidence — or a material finding changes the frame, the comparison or the selection, in which
case the unit stops and returns to David.

**Not requested:** authority to publish anything; authority to select the alternative, which is
David's; authority to treat the existing code as ratified, which this plan's U1 must earn.

### Units

| # | Result | Inputs / dependencies | Owner, timing | Done when (acceptance criteria) | Effort estimate |
| --- | --- | --- | --- | --- | --- |
| **U0** | The unratified work already in the tree: 2,592 lines of package, 2,378 lines of test, 13 fixture files | The earlier `Run` grant (revision 1), now superseded | Moss, 2026-09-21 (already done) | **Not a unit of this plan.** Reported for accounting only. It is kept only where U1 traces it to a criterion, and deleted where it does not | — already spent, and not counted as progress against this plan |
| **U1** | The offline gate: `--dir` mode, discovery, per-page facts, site-wide findings, the text and JSON reports, `--strict`, and a real `scripts/check-project.sh` — verified against this plan rather than assumed from the tree | The fixtures; the criteria in Review; `CONTEXT.md`'s finding list. Depends on nothing outside this repository | Moss, this session if ratified, otherwise the next | Each per-page fact and each site-wide finding in A1–A3 is re-derived from a named fixture and a named test; no module remains that cannot be traced to a criterion; **the two CLI failures are resolved or the failing module is deleted**, the suite passes, and `make ci` exits 0; `make records` stays clean | 2–3 focus sessions. Uncertainty **medium**: the code exists, so this is verification and repair, but the parser bug and the fixture that lied both showed that "it exists and passes" is not evidence. If the facts contract turns out to be met mainly by post-hoc tests, this estimate doubles and alternative A collapses toward B |
| **U2** | The address guard, ported and tested, and the live source's network dependencies injectable so the command line can be exercised with no network | [`agent-eligibility/eligibility/fetch.py`](../agent-eligibility/eligibility/fetch.py), read-only; the existing guard tests. Depends on U1 for the test harness | Moss, after U1 | Schemes other than http/https, ports other than the scheme default, and any host resolving to a private, loopback, link-local, multicast, reserved, unspecified or metadata address are refused, **naming the rule**; the connected peer is re-checked after connecting; a literal address is refused without consulting a resolver; every redirect hop is re-validated; `--url` runs end to end with no network; the two CLI failures are gone and the suite passes with the network unplugged | 0.5–1 focus session. Uncertainty **low**: the rule set is fixed by a tested source, and the injection point is diagnosed |
| **U3** | `--plan site.json`: `required_surfaces` and the home page's `identity.schema_types` enforced, unknown keys ignored with a reason, an unreadable plan exiting non-zero | The `siteplan` format, read-only. Depends on U1; independent of U2 | Moss, after U2 | The example plan in `siteplan`'s `CONTEXT.md` is met by the conforming fixture and unmet by the bare one; `offering`, `url_rules`, `crawler_stance`, `pages` and `identity.fields` are named in the output as **not checked**, with the reason; a malformed or missing plan exits 2 and never 0 | 1 focus session. Uncertainty **low** for the two enforced keys, **medium** for the format staying still while `siteplan` is itself unbuilt (Q3) |
| **U4** | One documented run against a real built directory from another project, and the gate's verdict on it | A `build/` directory and its owner's permission, both named by David. Depends on U1 | Moss, with the principal | The run completes with no network access; its findings are reviewed by the project that owns the build; a real regression, if the build has one, is named; the false-positive judgement is recorded rather than assumed | 0.5 session plus the other project's time. Uncertainty **high**: no `build/` directory exists anywhere in this workspace today, so the whole unit waits on a person |
| **U5** | `README.md` (what it does, how to run it, what it does not do) and the design record | U1–U3 as built. Depends on U1 for the package, U3 for the plan section | Moss, alongside U1 and finished with U3 | A reader with no context can install and run both modes from the README alone; "what it does not do" states the no-JavaScript limit, the origin bound, the absence of any ranking, citation or recommendation claim, and that `--dir` makes no network request; `docs/DESIGN.md` carries each threshold with its rejected alternatives, or says plainly that it is judgement | 1 focus session. Uncertainty **low** |

**Order and dependency.** U1 → U2 → U3, with U5 alongside U1 and U4 startable as soon as David
names a project. U4 and U3 can run in either order once U2 is done; the requested order puts the
gate's real-world value (U4) before the interface to a project that is itself unbuilt (U3),
because U4 is what tells us whether O1 is real.

## Out of scope

| Not in this plan | Reason |
| --- | --- |
| JavaScript execution, a headless browser, or any rendered-DOM claim | [`CONTEXT.md`](CONTEXT.md)'s deliberate exclusion: it answers a different question and adds a browser engine to a deploy gate. The script-render heuristic is reported as a labelled heuristic instead |
| Crawling, fetching or checking anything outside the submitted origin | The same exclusion. A tool that follows a link off-site can be pointed at someone else's server |
| Dependencies of any kind | [`CONTEXT.md`](CONTEXT.md): standard library only, so the tool installs into someone else's CI with no build step |
| Ranking, citation, traffic, recommendation or SEO scoring | The claim boundary. There is deliberately no aggregate score anywhere in the package |
| Publishing, deploying, or adding the tool to anyone's CI as part of this plan | The release word is David's |
| `siteplan`'s producer side, or any edit to that repository | A different project, with its own owner and its own record |
| Sub-decision records in `docs/records/` for choices this plan already covers | Open question Q4. Until it is answered, this record holds them |
| The template's process documents in other repositories | A different repository. The disagreements found here are reported in this record and in the return |

## Open questions for the principal

Each blocks something specific. None of them is a reason to stop work that this grant covers.

| # | Question | Owner | What it blocks |
| --- | --- | --- | --- |
| Q1 | **Which alternative do you ratify — A (full scope, verify first) or D (gate first, `--url` and `--plan` in a second increment)?** C and E are also live if you want less built | David | Everything. No unit may start until this is answered |
| Q2 | **Which project's built directory should U4 run against, and may Moss ask its owner?** Any project with a `build/` output will do; none exists in this workspace today | David | U4, and therefore the only evidence that O1 is real rather than plausible |
| Q3 | **Must `sitewalk --plan` support an older `plan_version`, or only the current one?** `siteplan` has no code yet, so version 1 is the only version that exists and the format may move before either tool ships | David | U3's compatibility promise. The plan's default: enforce version 1, note any other, never fail on the version alone |
| Q4 | **Do you want a sub-record in `docs/records/` per consequential choice, or does this record hold them?** [`docs/RECORDS.md`](docs/RECORDS.md) allows both, and the directory is empty | David | How the corpus is organised, and whether U2's guard port gets its own record |
| Q5 | **Should a missing `llms.txt` gate, or stay a note?** Today it is a non-gating note. Making it gate is a real policy choice with a real false-positive cost on sites that never wanted one | David | U1's severity split, and how noisy the gate is on sites that did not ask for this tool |
| Q6 | **Do you want `AGENTS.md`'s standing constraints replaced with this project's?** They still hold the template's placeholder comment and a single real constraint | David | Not work in this plan: a process change outside it |

## Review criteria

Registered now, before any unit runs. Delivery acceptance is kept separate from evidence of later
benefit, because a tool shipping is not a tool working.

| Ref | Criterion | Evidence source | Owner, trigger |
| --- | --- | --- | --- |
| A1 | Every per-page fact the specification names is produced: status, content type, title, meta description, canonical, JSON-LD `@type`s, visible-text length, internal-link count, sitemap membership | A named fixture page and a named test for each of the nine facts | Moss, at U1 delivery |
| A2 | Every site-wide finding the specification names is produced: page count and status distribution, sitemap URLs never reached, orphan pages, duplicate titles, duplicate descriptions, missing titles, cross-host canonicals, pages with no JSON-LD, internal links that do not return 200, and the existence of `robots.txt`, `sitemap.xml` and `llms.txt` | The findings test, plus the fixture page that produces each one | Moss, at U1 delivery |
| A3 | The offline source and the live source produce identical facts for the same bytes, field by field | One test reading the same fixture through both sources | Moss, at U1 delivery |
| A4 | `--dir` makes no network request, and a test proves it by making any socket operation fatal | The no-network harness, applied to every offline test | Moss, at U1 delivery |
| A5 | No output claims anything about ranking, citations, traffic or recommendation, and the no-JavaScript limit and the heuristic labels are present | Text and JSON output assertions | Moss, at U1 delivery |
| A6 | Exit 0 normally; 1 under `--strict` with findings; 2 when the run cannot be made, including an unreadable plan | CLI tests | Moss, at U3 delivery |
| A7 | The guard refuses non-http(s) schemes, non-default ports, and non-public addresses including the metadata address; re-checks the connected peer; re-validates every redirect hop | `tests/test_guard.py` with injected fakes, no network | Moss, at U2 delivery; independent assessment wanted |
| A8 | `make ci` exits 0 **and the project check it runs is a real one** — a green check that establishes nothing is worse than no check, and today's `make ci` is exactly that | The command, plus `scripts/check-project.sh` containing the byte-compile and test steps rather than the template stub | Moss, at U1 delivery, and at every unit after |
| A9 | The whole suite passes with the network unplugged | `python3 -m unittest discover -s tests -t .` | Moss, at every unit |
| B1 | **Benefit, not delivery:** the gate catches a real regression in a project's release path | That project's CI log and the release it stopped | David and that project's owner; trigger is U4 or a later adoption |
| B2 | **Benefit:** at least two projects run it | Their repositories and CI configuration | David; trigger is a second adoption |
| B3 | **Benefit:** it reports more than the sitemap already says | A real run compared with the site's own sitemap | David; trigger is the first live run |

A1–A9 judge U1–U3. B1–B3 are `CONTEXT.md`'s success conditions: this plan cannot observe them,
and no unit claims to.

## Review

No finding is recorded yet, because no ratified delivery exists. The criteria above are
registered and pending.

| Criterion | Evidence source | Owner, window or trigger | Finding | Response |
| --- | --- | --- | --- | --- |
| A1–A5, A8, A9 (the offline gate) | The committed revision, the fixtures, `make ci` | Moss, at U1 delivery | Pending — U1 not started | Pending |
| A7 (the guard) | `tests/test_guard.py`, injected fakes | Moss, at U2 delivery | Pending — U2 not started | Pending |
| A6 (the plan check) | CLI tests | Moss, at U3 delivery | Pending — U3 not started | Pending |
| Independent assessment of U1–U3 by an assessor who did not write them | A named assessor's return against A1–A9 | David to grant; not before delivery | Pending — no assessor named | Pending |
| B1–B3 (benefit) | Adopting projects' CI logs; a real run against a real site | David; trigger is U4 or a later adoption | Unobserved — needs a project and a site | Carry as U4 |

## Changes

Revision 2, 2026-09-21T12:44:00-06:00. **Mode changed from `Run` to `Plan`, on the principal's
direct instruction of 2026-09-21.** Source: that instruction, plus the installed Perspicuity skill
0.5.0 (`references/record.md`, "Declare the working mode"; `references/analysis.md`). Reason: the
principal now wants the basis, the alternatives and the units ratified **before** implementation,
where revision 1 was prescribed work executed under `Run`; a planning run stops at the grant
request even when the authority to act exists. What changed: this file became a Statement of Work
— added the five alternatives with their consequences, the recommendation and the tradeoff it
accepts, the units with effort estimates, the out-of-scope list, six open questions, and the
review criteria; added the account of the work produced ahead of this plan; replaced the
requested grant; set `work_status` to `submitted` and `Decision` to `pending`. What is preserved:
the earlier mode and the reason it was declared, the inherited frame and claim boundary, the
objectives with their sources, and revision 1's registration of the run that produced the code
now in the tree. Affects: all of U1–U5. **No code was written, amended or committed in this
revision**, deliberately: a planning run stops at the boundary, and the unit table is where the
next code comes from.

Revision 1, 2026-09-21T11:52:00-06:00. Created and registered as mode `Run`. Source: the
principal's assignment of 2026-09-21 and [`CONTEXT.md`](CONTEXT.md); Perspicuity 0.5.0's record
format. Reason: the corpus rule requires the frame, the conditions, the selection and unit 1's
acceptance criteria to exist before the work that depends on them. Affects: the `Run` increment
that produced the package and tests now sitting uncommitted in the tree. No package code existed
at that revision.
