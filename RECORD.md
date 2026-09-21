---
format: perspicuity-work/1
id: sw-project
revision: 5
skill_version: 0.5.0
updated: 2026-09-21
created_at: "2026-09-21T11:48:05-06:00"
updated_at: "2026-09-21T14:45:00-06:00"
record_status: open
work_status: active
---

# Sitewalk

The project record, and now the **Statement of Work** for `sitewalk`. It is the parent of every
record in this repository and it carries the continuing account: what is true now, the frame, the
conditions, the alternatives, the recommendation, the units, and the review.

## Current position

Mode: **`Run`**. Revision 1 declared `Run` because the principal's first message prescribed the
frame, the tool and its specification in full, leaving nothing to select. Revision 2 changed to
`Plan` on the principal's instruction, because he then wanted the basis, alternatives and units
ratified before implementation. This revision returns to `Run`: revision 2's plan has been
**ratified**, the grant is registered below, and the mode now carries that settled choice through
its units and stops at the return. Each mode change and its reason is preserved rather than
overwritten.

Principal: David. Decider: David. Moss prepares the basis and recommends; Moss did not select.

Work owner: Moss (coordinator).

Decision: `selected` — **alternative A**, ratified by David on 2026-09-21 against basis revision 2
of this record. The selection is recorded in Act under *Selection*, with the grant it authorises
and the two answers that narrowed it (Q3: accept any `plan_version` and ignore keys this consumer
does not know; Q5: a missing `llms.txt` must not gate). The product frame, the claim boundary and
the tool specification remain `inherited` from the principal (2026-09-21,
[`CONTEXT.md`](CONTEXT.md)) and are not reopened.

Work scope: **U1**, the offline gate — reconciled, verified, and where necessary cut back against
the registered facts contract. The units after it are granted but not picked up; each registers
its own pickup plan before it starts.

Work: revision 3 registers the selection, the grant and U1's pickup plan. The `Run` increment that
produced the package in the tree is accounted for in Act (*Work already in the tree*) and is not
ratified by being described: U1's reconciliation decides what survives, and this record carries
the outcome when U1 returns.

Outcome: unknown. U1 has not run. Nothing has been observed against a real built site or a real
live site.

Next: Moss — carry out U1's registered pickup plan, then register U2's pickup plan before
implementing U2.

Dependency: Nothing blocks U1. **U4 is blocked on open question Q2**: the principal has not named
which project's `build/` may be tested against, and no `build/` directory exists in this
workspace. U4 must not run until he answers.

Waiting on: David (principal), for Q2 only. U1, U2, U3 and U5 proceed without it.

Review due: 2026-10-05 — see Review. A1–A5, A8 and A9 become assessable when U1 returns; A6 and
A7 at U2 and U3; B1–B3 need a real site and remain unobserved.

Authority: David ratified the plan and **granted U1–U5** on 2026-09-21. He retains **spending,
outbound messages, external agreements and the release word for publication**. The grant's
includes, excludes and stop condition are written out in Act; nothing outside them is authorised.

| Stage | began_at | registered_at / exact basis revision | finished_at |
| --- | --- | --- | --- |
| Frame and Decide (Run, revision 1) | 2026-09-21T11:49:00-06:00 | 2026-09-21T11:52:00-06:00 — revision 1 | 2026-09-21T11:52:00-06:00 |
| Frame and Decide (Plan, revision 2) | 2026-09-21T12:14:00-06:00 | 2026-09-21T12:44:00-06:00 — revision 2 | 2026-09-21T12:44:00-06:00 |
| Selection | — | 2026-09-21T13:05:00-06:00 — revision 2, alternative A, ratified by David | 2026-09-21T13:05:00-06:00 |
| Act — U1 | 2026-09-21T13:05:00-06:00 | 2026-09-21T13:05:00-06:00 — **this revision**, U1 pickup plan | pending |
| Act — U2, U3, U5 | pending — each registers its own pickup plan at its own pickup | pending | pending |
| Act — U4 | blocked on Q2 | pending | pending |
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

`selected_at` 2026-09-21T13:05:00-06:00. Decider: **David**. Basis revision: **2** (the Statement
of Work), ratified in a direct instruction of 2026-09-21. The selection is **alternative A — full
scope, with U1 re-deriving the existing package against the registered facts contract and
deleting whatever it cannot justify.** The 2,592 lines in the tree are a proposal, not a
foundation, and a U1 that concludes most of the package should go is a successful U1.

Two of the open questions were answered in the same instruction and are now part of the basis:

- **Q3 — answered yes.** `--plan` must accept older `plan_version` values and ignore keys it does
  not understand. A consumer that rejects an unfamiliar key breaks the producer every time the
  format grows. `siteplan` is finalising the format and expects `plan_version` to be required and
  everything else optional.
- **Q5 — answered no.** A missing `llms.txt` must **not** gate. Basis: Ahrefs analysed 137,000
  sites and found 97% of `llms.txt` files received no requests at all
  ([Search Engine Journal](https://www.searchenginejournal.com/97-of-llms-txt-files-got-no-requests-ahrefs-data-shows/579478/),
  [Ahrefs](https://ahrefs.com/blog/llmstxt-study/)). The finding stays a non-gating note, and the
  reason is recorded in the output rather than only here. This is a `judgment`-basis decision:
  the study is about one crawler population at one time, and it is cited so a reader can discount
  it.
- **Q4 — answered: sub-records where the admission test is met, this record otherwise.** U1's
  outcome meets it, so U1 files one.
- **Q2 — still open, and it is the principal's.** U4 waits.
- **Q6 — answered yes.** `AGENTS.md`'s placeholder standing constraints are to be replaced with
  this project's own. That is U1 work and is inside the grant as an amendment to the process
  document, not a new choice.

**The grant.** David granted **U1–U5**. Included: the units in the order below; the power to
amend or delete unratified code that fails a registered criterion; to write and run tests; to
write `README.md`, `docs/DESIGN.md`, `scripts/check-project.sh` and the standing constraints in
`AGENTS.md`; and to commit locally in coherent commits. Excluded: any push, publish, deploy or
spend; any new dependency; any network request other than the single live run U4 requires, to a
domain the principal names; any editing of another project's repository; any contact with another
project's owner without his word. Stop condition: U1, U2, U3 and U5 delivered with this record
amended, or a material finding that changes the frame, the comparison or the selection — in which
case the unit stops and returns to David. **U4 is granted but blocked on Q2** and must not run
until he names a project and its `build/`.

### Decision index

| Record | Owner | State | Depends on |
| --- | --- | --- | --- |
| This record — frame, alternatives, selection, grant, units U1–U5 | Moss | open, active — U1 picked up | David's ratification, given 2026-09-21 |
| [`docs/records/2026-09-21-verify-before-keeping-package.md`](docs/records/2026-09-21-verify-before-keeping-package.md) — keep / amend / delete for the pre-plan package | Moss | filed at U1's return, `submitted`, awaiting acceptance | U1; Q4 placed it here |
| [`docs/DESIGN.md`](docs/DESIGN.md) — D1–D10, the technical choices and their measured thresholds | Moss | written before this plan, revised in place | U1's reconciliation decides which of D1–D10 survive |

### U1 pickup plan

Registered before U1 begins, as the skill requires: the first unit's pickup plan at planning time,
each later unit's at its own pickup.

**How U1 will be carried out.** Not by reading the code and agreeing with it. The route is
**independent re-derivation**:

1. Build the facts contract from the principal's specification and `CONTEXT.md` — the nine
   per-page facts and the site-wide findings list — as a checklist with no reference to the
   existing modules.
2. For each item, name the fixture page that must produce it and the assertion that proves it. An
   item with no fixture, or with a fixture that cannot actually produce it, fails the contract.
3. Compute what the fixtures *should* yield, by reading the fixture files directly, and compare
   that against what the tool reports. This is the audit: it tests the package against the
   fixtures rather than against its own tests.
4. For each module, decide **kept**, **amended** or **deleted**, with the reason, and record the
   counts. Dead configuration, unreachable branches and code that no criterion needs are deleted
   rather than carried.
5. Fill in `scripts/check-project.sh` with the real checks — byte-compile the package and run the
   suite — so `make ci` can fail on a real defect again.
6. Apply the three answers that bear on U1: Q5's non-gating `llms.txt` note (already true in the
   tree, now with the reason and the source in the output), Q6's standing constraints in
   `AGENTS.md`, and the `docs/records/` sub-record for the outcome.

**Acceptance criteria for U1** (from Review): A1, A2, A3, A4, A5, A8, A9. A8 now also requires
`scripts/check-project.sh` to contain real checks rather than the stub — a green check that
establishes nothing is worse than no check, and the propagated stub now fails on purpose so
`make ci` cannot pass while tests fail.

**Files U1 expects to touch:** `scripts/check-project.sh`, `sitewalk/findings.py` (the `llms.txt`
note's reason and source), `AGENTS.md` (standing constraints), `docs/records/` (the U1 record),
any module the reconciliation amends or deletes, and its tests. Anything beyond that list is
recorded as a deviation before it is done.

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

### U2 pickup plan

Registered before U2 begins. U2 is the guard and the offline testability of the live path; the
injection half was completed inside U1's grant, because U1's own criterion A8 could not be met
with a red `make ci` — that deviation is recorded in U1's sub-record and in the commit, and U2
owns the guard itself.

**How U2 will be carried out:**

1. **Re-derive the guard's rule set** from `agent-eligibility/eligibility/fetch.py` and the
   principal's specification, as a list of rules with no reference to the ported module.
2. **Adversarially test each rule through `fetch.fetch`**, not only through `guard`'s functions.
   A rule that is implemented but not reached is not a rule, and the existing suite already has
   one case of that shape: the peer check after connecting.
3. **Try to defeat it.** Hostile inputs to attempt: a public name that resolves to a private
   address among several answers; a literal metadata address; an IPv4-mapped private address; a
   redirect chain that ends off-origin; a redirect to a literal private address; a name with
   mixed public and private answers; a URL with credentials or an unusual port spelling;
   `0.0.0.0`; and a peer address that differs from the resolved one.
4. **Record anything that cannot be defended** rather than widening the rule set to cover it.
5. Register U3's pickup plan before starting U3.

**Acceptance criteria for U2:** A7 in full, plus A9 and A8 staying green.

**Files U2 expects to touch:** `sitewalk/guard.py`, `sitewalk/fetch.py`, `tests/test_guard.py`,
`tests/fakes.py`, and this record. Anything else is recorded as a deviation before it is done.

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
| A1–A5, A8, A9 (the offline gate) | The committed revision, the two independent derivations, `make ci` | Moss, at U1 delivery, 2026-09-21 | **Met, with the limits below.** Nine of nine per-page facts and twelve of twelve site-wide findings agree with computations made without importing the tool's parser; `--dir` runs inside a harness where any socket use raises; `make ci` exits 0 and exits 2 on each of three injected defects; 244 tests pass offline | Accepted by Moss as self-check only — see the next row. U1's sub-record carries the detail |
| A7 (the guard) | `tests/test_guard.py` and `tests/test_guard_adversarial.py`, injected fakes, no network | Moss, at U2 delivery, 2026-09-21 | **Met, with one defect found and fixed.** Every rule refuses what it must and names the address it refused, through `fetch.fetch` rather than through `guard` alone. The adversarial pass found that an `http`→`https` upgrade redirect — the commonest redirect on the web — was refused as off-origin, which would have reported a plain-HTTP site as unreachable; the rule is now a same-site check that allows the upgrade and refuses downgrades, other hosts, subdomains and other ports | Accepted by Moss as self-check only. The upgrade defect is the evidence that the adversarial pass was worth running, and it is also the reason an independent assessor is still wanted |
| A6 (the plan check) | CLI tests | Moss, at U3 delivery | Pending — U3 not started | Pending |
| Independent assessment of U1–U3 by an assessor who did not write them | A named assessor's return against A1–A9 | David to grant; not before delivery | **Not established for U1 or U2.** Moss wrote the package and the reconciliation, so A1–A5, A8 and A9 are a self-check. The two defects U1 found were both found by running code against injected breakage rather than by review, which is evidence that the checks work, not that the design is right | Requested in the return to the principal: name an assessor, or accept the self-check with its stated limit |
| B1–B3 (benefit) | Adopting projects' CI logs; a real run against a real site | David; trigger is U4 or a later adoption | Unobserved — needs a project and a site | Carry as U4 |

## Changes

Revision 5, 2026-09-21T14:45:00-06:00. **U2 delivered and assessed against A7.** Source: U2's
committed evidence and the adversarial suite. Reason: the skill requires each planned result to be
marked delivered, blocked or stopped before a stop. What changed: the Review table carries U2's
finding, including the defect the adversarial pass found. What is preserved: A7's text as
registered. Affects: U2, delivered; U3 and U5 remain.

Revision 4, 2026-09-21T14:10:00-06:00. **U1 delivered and assessed against A1–A5, A8 and A9.**
Source: U1's committed evidence and
[`docs/records/2026-09-21-verify-before-keeping-package.md`](docs/records/2026-09-21-verify-before-keeping-package.md).
Reason: the skill requires each planned result to be marked delivered, blocked or stopped before a
stop, with its actual evidence. What changed: the decision index now names U1's sub-record; the
Review table carries U1's findings and, explicitly, that the assessment is a self-check because
the author and the assessor are the same actor. What is preserved: revision 2's criteria text —
the criteria were not adjusted to fit the result. Affects: U1, delivered; U4 remains blocked on
Q2; U2, U3 and U5 remain to be picked up.

Revision 3, 2026-09-21T13:05:00-06:00. **David ratified the plan: alternative A is selected
and U1–U5 are granted.** Source: the principal's direct instruction of 2026-09-21, against basis
revision 2. Reason: a planning run stops at the grant request and resumes only on ratification;
the ratification arrived, so this revision records the selection, the decider, the basis
revision, the grant's includes, excludes and stop condition, and U1's pickup plan, and returns the
mode to `Run`. What changed: `Decision` moved from `pending` to `selected`; `work_status` from
`submitted` to `active`; *Selection*, the grant, the pickup plan and the decision index were
added; Q3, Q4, Q5 and Q6 were answered and Q2 confirmed still open, with U4 recorded as granted
but blocked. What is preserved: revision 2's frame, objectives, conditions, alternatives and
review criteria, and revision 1's mode and reason — the sequence is kept rather than overwritten.
Affects: U1, now picked up; U2, U3 and U5, granted and not yet picked up; U4, blocked on Q2. No
code was written for this revision; it registers the basis for the code that follows.

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
