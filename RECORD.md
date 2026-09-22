---
format: perspicuity-work/1
id: sw-project
revision: 26
skill_version: 0.5.0
updated: 2026-09-21
created_at: "2026-09-21T11:48:05-06:00"
updated_at: "2026-09-22T04:15:00-06:00"
record_status: open
work_status: active
---

# Sitewalk

The project record, and now the **Statement of Work** for `sitewalk`. It is the parent of every
record in this repository and it carries the continuing account: what is true now, the frame, the
conditions, the alternatives, the recommendation, the units, and the review.

## Current position

Mode: **`Run`**. The mode carries the ratified plan through its granted units and stops at the
return; it was `Plan` while the plan was being prepared, and `Run` before that, and both changes
with their reasons are in the mode history below. This section is position, not history: the
reasons a mode changed are recorded where the change was made.

Principal: David. Decider: David. Moss prepares the basis and recommends; Moss did not select.

Work owner: Moss (coordinator).

Decision: `selected` — **alternative A**, ratified by David on 2026-09-21 against basis revision 2
of this record, and recorded in Act under *Selection* with the grant it authorises. The product
frame, the claim boundary and the tool specification remain `inherited` from the principal
(2026-09-21, [`CONTEXT.md`](CONTEXT.md)) and are not reopened.

Work scope: the ratified plan and the units it authorises. **Their state is in Act's unit table and
is deliberately not restated here** — a count in this section goes stale the moment a unit lands,
and did: see the Changes entry for revision 23.

Work: the delivery's evidence is in Review and its detail in Act. `make ci` exits 0 and the suite
passes with the network unavailable; the counts and the defects found belong to the revision that
produced them, so they are recorded there rather than summarised here.

Outcome: the tool is built and green on its own fixtures. **Nothing has been observed against a
real built site or a real live site**, which is what U4 is for, and that is the honest boundary on
every claim in this record.

Next: Moss — U10 is held on the kind-awareness answer and U4 on Q2; **U4 takes precedence whenever
it unblocks**. Register U4's pickup plan when the answer arrives, and do not start it before then.
Further pending: David, to answer Q2 by naming a project whose built directory U4 may run against.

Dependency: **U4 is blocked on open question Q2** — the principal has not named which project's
`build/` may be tested against, and no `build/` directory exists in this workspace. Nothing else
blocks anything; both Finch assessments and the principal's verification have returned.

Waiting on: David (principal), for Q2 only.

Review due: 2026-10-05. A1–A9 are assessed, by Moss as self-check and by Finch independently for
U1 and for U6–U9. **B1–B3 are unobserved and need a real site**, which is U4; they are the only
criteria still pending.

Authority: David ratified the plan on 2026-09-21 and granted the units recorded in the grant under
Act, U6–U9 by later instruction and ruling. He retains **spending, outbound messages, external
agreements and the release word for publication**. The grant's includes, excludes and stop
condition are written out in Act; nothing outside them is authorised.

| Stage | began_at | registered_at / exact basis revision | finished_at |
| --- | --- | --- | --- |
| Frame and Decide (Run, revision 1) | 2026-09-21T11:49:00-06:00 | 2026-09-21T11:52:00-06:00 — revision 1 | 2026-09-21T11:52:00-06:00 |
| Frame and Decide (Plan, revision 2) | 2026-09-21T12:14:00-06:00 | 2026-09-21T12:44:00-06:00 — revision 2 | 2026-09-21T12:44:00-06:00 |
| Selection | — | 2026-09-21T13:05:00-06:00 — revision 2, alternative A, ratified by David | 2026-09-21T13:05:00-06:00 |
| Act | 2026-09-21T13:05:00-06:00 | 2026-09-21T13:05:00-06:00 — revision 3, U1 pickup plan | see the unit table in Act |
| Review | 2026-09-21T14:05:00-06:00 | 2026-09-21T12:44:00-06:00 — revision 2, Review criteria | see Review |

### Mode history

Preserved because a later reader needs to know why the mode changed, and it is history rather than
position:

- **`Run`** (revision 1). The principal's first message prescribed the frame, the tool and its
  specification in full, leaving nothing to select.
- **`Plan`** (revision 2, 2026-09-21). The principal then wanted the basis, alternatives and units
  ratified before implementation, and a planning run stops at the grant request.
- **`Run`** (revision 3 onwards). The plan was ratified, so the mode carries the settled choice
  through its units and stops at the return.

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
| `sitewalk/` — 15 modules | 2,592 lines as measured before U1; **2,658 after U1–U3**, which removed six dead items and added the same-site redirect rule, the plan-version policy and the report's heuristic evidence | Reconciled and delivered in U1–U3 |
| `tests/` — 10 test modules plus `fakes.py` | 2,378 lines as measured before U1; **2,894 after**, including the no-network harness and the adversarial guard suite | Delivered |
| `tests/fixtures/` — 2 sites, 13 files | A 12-page site carrying every finding the specification names, plus a bare site for the missing-surface cases | Present, uncommitted, unratified |
| `make records` | Clean, including `skill_version: 0.5.0` and the corrected checker path | True |
| `make ci` | **Exits 0, and establishes nothing**: `scripts/check-project.sh` still contains the template's stub, so no project check runs at all — the two failing tests below do not fail the build | True, and the more dangerous of the two states; U1 fixes it |
| `python3 -m unittest discover -s tests -t .` | 238 of 240 passed before U1; **277 pass after** | Resolved |

**The two failures, diagnosed during planning and repaired in U2** — at the time, repairing them
would have been implementation. `tests/test_cli.py::LiveModeOverTheFakeConnection` patches
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

**Proposal P1 — granted 2026-09-21, not yet applied.** Amend `AGENTS.md`'s definition of done with
the standing rule recorded above — every new test and fixture must answer "which wrong implementation
would this catch?", and a fixture that cannot separate a right implementation from a plausible
wrong one is not a fixture. The principal granted it and is propagating the same rule to the
`project-setup` template. **It is not applied yet because it is a hold, not a dispute**: `AGENTS.md`
is part of what Finch is reading, and editing a document after an assessor read it invalidates that
part of the assessment. It is applied the moment the freeze lifts, in a commit that names it as P1.

**Not requested:** authority to publish anything; authority to select the alternative, which is
David's; authority to treat the existing code as ratified, which this plan's U1 must earn.

### Units

| # | Result | Inputs / dependencies | Owner, timing | Done when (acceptance criteria) | Effort estimate |
| --- | --- | --- | --- | --- | --- |
| **U0** | The unratified work already in the tree: 2,592 lines of package, 2,378 lines of test, 13 fixture files | The earlier `Run` grant (revision 1), now superseded | Moss, 2026-09-21 (already done) | **Not a unit of this plan.** Reported for accounting only. It is kept only where U1 traces it to a criterion, and deleted where it does not | — already spent, and not counted as progress against this plan |
| **U1** (delivered) | The offline gate: `--dir` mode, discovery, per-page facts, site-wide findings, the text and JSON reports, `--strict`, and a real `scripts/check-project.sh` — verified against this plan rather than assumed from the tree | The fixtures; the criteria in Review; `CONTEXT.md`'s finding list. Depends on nothing outside this repository | Moss, this session if ratified, otherwise the next | Each per-page fact and each site-wide finding in A1–A3 is re-derived from a named fixture and a named test; no module remains that cannot be traced to a criterion; **the two CLI failures are resolved or the failing module is deleted**, the suite passes, and `make ci` exits 0; `make records` stays clean | 2–3 focus sessions. Uncertainty **medium**: the code exists, so this is verification and repair, but the parser bug and the fixture that lied both showed that "it exists and passes" is not evidence. If the facts contract turns out to be met mainly by post-hoc tests, this estimate doubles and alternative A collapses toward B |
| **U2** (delivered) | The address guard, ported and tested, and the live source's network dependencies injectable so the command line can be exercised with no network | [`agent-eligibility/eligibility/fetch.py`](../agent-eligibility/eligibility/fetch.py), read-only; the existing guard tests. Depends on U1 for the test harness | Moss, after U1 | Schemes other than http/https, ports other than the scheme default, and any host resolving to a private, loopback, link-local, multicast, reserved, unspecified or metadata address are refused, **naming the rule**; the connected peer is re-checked after connecting; a literal address is refused without consulting a resolver; every redirect hop is re-validated; `--url` runs end to end with no network; the two CLI failures are gone and the suite passes with the network unplugged | 0.5–1 focus session. Uncertainty **low**: the rule set is fixed by a tested source, and the injection point is diagnosed |
| **U3** (delivered) | `--plan site.json`: `required_surfaces` and the home page's `identity.schema_types` enforced, unknown keys ignored with a reason, an unreadable plan exiting non-zero | The `siteplan` format, read-only. Depends on U1; independent of U2 | Moss, after U2 | The example plan in `siteplan`'s `CONTEXT.md` is met by the conforming fixture and unmet by the bare one; `offering`, `url_rules`, `crawler_stance`, `pages` and `identity.fields` are named in the output as **not checked**, with the reason; a malformed or missing plan exits 2 and never 0 | 1 focus session. Uncertainty **low** for the two enforced keys, **medium** for the format staying still while `siteplan` is itself unbuilt (Q3) |
| **U4** (blocked) | One documented run against a real built directory from another project, and the gate's verdict on it | A `build/` directory and its owner's permission, both named by David. **BLOCKED on Q2 — not started** | Moss, with the principal | The run completes with no network access; its findings are reviewed by the project that owns the build; a real regression, if the build has one, is named; the false-positive judgement is recorded rather than assumed | 0.5 session plus the other project's time. Uncertainty **high**: no `build/` directory exists anywhere in this workspace today, so the whole unit waits on a person |
| **U5** (delivered) | `README.md` (what it does, how to run it, what it does not do) and the design record | U1–U3 as built. Depends on U1 for the package, U3 for the plan section | Moss, alongside U1 and finished with U3 | A reader with no context can install and run both modes from the README alone; "what it does not do" states the no-JavaScript limit, the origin bound, the absence of any ranking, citation or recommendation claim, and that `--dir` makes no network request; `docs/DESIGN.md` carries each threshold with its rejected alternatives, or says plainly that it is judgement | 1 focus session. Uncertainty **low** |
| **U6** (delivered) | **Make the robots.txt skip structural in the report.** The report must state, where a reader cannot miss it, how many paths were excluded and why | `sitewalk/crawl.py` must keep the matched rule; `sitewalk/report.py` must surface the count; `tests/` must prove each | Moss, after Finch's assessment returns and under a fresh pickup plan | Four criteria, all currently **unmet**: (1) the total count appears in the report header, not only in Notes; (2) the count appears in `limits` in the JSON as `paths_skipped_robots`; (3) each skip names the path **and quotes the matched rule** (`Disallow: /private/`), which today is discarded by `sitemap.parse_robots`; (4) a test asserts all three, so removing any of them fails the suite | 0.5 focus session. Uncertainty **low**: the skip list already exists; this is surfacing it and keeping the rule |
| **U7** (delivered) | **Make the plan verdict honest about what it knows: a version gate, and unverified surfaces that are never reported as absent.** Under the format's rule 4, keys grow but versions announce: an unknown key is additive growth a consumer may carry and name, while an unknown version means a key's meaning may have moved, so the verdict must be conditional in default mode and an error finding under `--strict` | `siteplan/docs/PLAN-FORMAT.md` at `fe8433b` (frozen format 1), read-only; the two version cases already in `siteplan/docs/fixtures/plan-conformance.json` | Moss, after U6 | Five criteria: (1) `plan_version` 1 reads clean, unqualified; (2) an older version reads normally, unqualified; (3) an unknown or newer version is met-with-a-condition in default mode and a **`conditional` finding exiting non-zero** under `--strict` (this criterion said *error* until 2026-09-22, which contradicted design A and the code); (4) an absent or mistyped `plan_version` is an error finding under `--strict` too — an unsupported verdict rather than a conditional one — with a message distinct from the unknown-version case; (5) a required surface the consumer has **no check for** is reported as *unverified*, never as absent, as a `conditional` finding: default runs disclose it and exit 0, and `--strict` refuses to certify the plan and exits non-zero. The severity is defined in the report's own documentation and reaches `finding_counts` in the JSON. Tests load the seven **valid** plans from the conformance fixture and assert each is met, and assert that an unchecked surface produces no `plan_surface_missing` finding | 1 focus session. Uncertainty **low** |
| **U8** (delivered) | **Check the two surfaces this consumer could not check: `json-ld` and `rss.xml`.** The format's vocabulary is closed at five and describes what a plan may require, not what one tool looks for, so the gap closes on this side | `siteplan/docs/PLAN-FORMAT.md` at `fe8433b`, read-only. Cost measured 2026-09-21 | Moss, after U7 | Four criteria: (1) a plan requiring `rss.xml` is met when `/rss.xml` answers 2xx and unmet when it does not; (2) a plan requiring `json-ld` is met when any crawled page carries a JSON-LD `@type`; (3) **four states are distinguishable in the JSON, without reading a message string**: fetched-and-present, fetched-and-absent, derived-and-not-fetched, and not-checked-at-all; and (4) **the disclosure stays**: a surface this consumer still cannot check is named, is state *not checked*, stays `conditional`, and still gates under `--strict`, so a sixth surface added later reopens the same gap under the same rule. The vocabulary stays at five | 0.5–1 focus session. Uncertainty **low**, and the ruling is conditional on the cost turning out as measured: the two are one request and one already-held fact. Raised from 0.5 by the four-state requirement |
| **U9** (delivered) | **Apply U1's deletion test across the whole package, and fix what it finds.** Finch found two items that fail the very test U1 used to delete six others, so the test was right and was not applied exhaustively | `sitewalk/guard.py`, `sitewalk/errors.py`, `sitewalk/plan.py`, `docs/DESIGN.md`. Independent of U6–U8 except for the plan JSON, which is U8's surface | Moss, after U8 (the `plan` JSON item touches U8's file) | Six criteria: (1) `Address.host`, `Address.port` and `Address.family` are written but read nowhere — **verified by hand, not by a name-level scan** — and are removed; (2) `PlanError` has no reference anywhere and is removed or given a documented use; (3) the deletion test is re-run exhaustively and its **result is recorded, including a nil result**; (4) `plan.identity_schema_types_met: true` while `passed: false` on a malformed plan is fixed, since that is the same overclaim shape as U8's states; (5) DESIGN D6's `app_root_markers` and D1's `read(path)` are corrected to `app_root_element` and `fetch`; (6) each fix answers P1's question with a test that fails on the wrong change | 0.5–1 focus session. Uncertainty **low** |
| **U10** (granted; **held** — needs the kind-awareness answer) | **`json-ld` means the home page, and the verdict names the page it looked at.** Today this consumer accepts JSON-LD on **any crawled page**, so a site with it only on a deep page passes; the rule Heron has written makes it home-page-only | `siteplan/docs/PLAN-FORMAT.md`, revised by Heron. Resolves **G1** | Moss, **after the principal confirms Heron's answer to the kind-awareness caveat** | Three criteria: (1) `json-ld` is met only when the **home page** carries a `@type`; (2) the finding names the page it looked at, so a reader can tell which page was checked; (3) the tests assert the change on what a machine reads, including a site whose JSON-LD is only on a deep page, which **passes today and must not after** | 0.5 focus session. **Held:** the principal has raised with Heron whether home-page-only is wrong for kinds whose structured data legitimately lives on inner pages — a content site's `Article` markup is on its articles. Either `json-ld` leaves those kinds' surface lists or the rule becomes kind-aware. Discovering that at the first content-site build is the expensive way |
| **U11** (delivered) | **The ignored-key disclosure must reach the machine-readable output.** Rule 6 makes the disclosure the *condition* of tolerating an unknown key, and a condition that lives only in prose is not one a machine consumer can rely on | Resolves **G5**. The audit below records what already reaches the JSON and what does not | Moss, now | Four criteria: (1) every key the consumer ignored appears in the machine-readable output as a finding, not only in `notes`; (2) the finding names the key; (3) a test asserts it on the JSON, not on the text report; (4) the audit of every other tolerated case is recorded, including that they already reach the JSON, so a later change that confines one of them to prose fails a test | 0.5 focus session. Uncertainty **low** |

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

### U3 pickup plan

Registered before U3 begins. U3 is `--plan`: the consumer side of the format `siteplan` owns.

**How U3 will be carried out:**

1. **Re-read the format from `siteplan`'s own document** rather than from this record, and check
   the two enforced keys against it: `required_surfaces` and `identity.schema_types`.
2. **Apply the principal's Q3 answer as a rule, and test it:** any `plan_version` is accepted;
   a version this consumer does not know produces a note saying which revision it was built
   against and that it enforced only the keys it understands; an absent `plan_version` is a note
   and not a failure, because `siteplan` has not yet confirmed it is required.
3. **Prove the leniency is real**, not just intended: add a case with an unknown key, a case with
   a future `plan_version`, and a case with keys of the wrong type, and assert what each does.
4. **Prove the enforcement is real:** a conforming fixture meets the plan; the bare fixture fails
   it; a plan file that cannot be read exits 2, never 0.
5. **Keep the "not checked" list honest** — `offering`, `url_rules`, `crawler_stance`, `pages` and
   `identity.fields` must be named in the output as not checked, with the reason, so a reader is
   never left to assume they were verified.
6. Register U5's pickup plan before starting U5.

**Acceptance criteria for U3:** A6, plus A8 and A9 staying green.

**Files U3 expects to touch:** `sitewalk/plan.py`, `tests/test_plan.py`, `tests/test_cli.py`,
`docs/DESIGN.md` (D9), and this record.

### U5 pickup plan

Registered before U5 begins. U5 is the reader-facing documentation: `README.md` and the design
record.

**How U5 will be carried out:**

1. **Write the README for a stranger with no context.** Install, both modes, the plan check, the
   options and exit codes, and — as its own section, before the usage — what the tool does not
   do. That section is the claim boundary restated for a person who will not read `CONTEXT.md`.
2. **Check every command in it by running it.** A README whose commands do not run is a README
   that teaches a stranger to distrust the tool.
3. **Check every default in it against `cli.py`**, rather than against memory. The options table
   is a claim about behaviour, and it is the kind that goes stale silently.
4. **Bring `docs/DESIGN.md` up to date with what was built**, naming each place it had drifted:
   the removed link-check bound, robots being honoured in `--dir`, and the plan-version policy.
5. **Say in the README where the reasoning lives**, so a reader who wants the why is not left with
   only the how.

**Acceptance criteria for U5:** a reader with no context can install and run both modes from the
README alone; the "what it does not do" section states the no-JavaScript limit, the origin bound,
the absence of any ranking, citation or recommendation claim, and that `--dir` makes no network
request.

**Files U5 expects to touch:** `README.md`, `docs/DESIGN.md`, and this record.

### The robots.txt stance, confirmed as a property

Decided by Moss under the grant, confirmed by David on 2026-09-21, and recorded here rather than
left implicit in `crawl.py`, because it is a property of the product and not an implementation
detail.

**The property.** `sitewalk` honours the build's own `robots.txt` in `--dir` mode as well as in
live mode. robots.txt is a statement about the **content**, not about the transport, so a tool
that reports what a machine can read must not read what the site has refused. It is also what
makes `--dir` and `--url` agree on the same bytes, which is the property that makes the offline
path a gate rather than a second opinion (criterion A3).

**It is not a flag, deliberately.** A gate whose scope depends on a switch is a gate nobody can
compare across runs, so there is no option to include disallowed paths.

**Evidence that it holds in both modes:** `tests/test_dir_mode.py::TheOfflineCrawl.test_a_robots_disallowed_path_is_not_read_in_offline_mode_either`
and `tests/test_crawl.py::RobotsIsObeyed`, which assert both that the path is not read and that the
skip is recorded. Checked by hand on the fixture: the offline report states `/private/` was not
fetched, and a live crawl over the fake connection never requests `/private/x/`.

**The risk this carries, and its state.** A gate that skips pages can pass while under-reporting,
so the skip has to be unmissable. **It is not yet.** As delivered, the skip appears once, in the
Notes block: `not fetched: /private/ — robots.txt disallows this path for our user agent`. It is
absent from the report header, absent from the JSON `limits`, and the matched rule
(`Disallow: /private/`) is discarded by `sitemap.parse_robots`, so the report says that robots
disallowed the path without saying what it disallowed it by. A reader who reads only the summary
cannot tell that anything was excluded. That gap is **U6** below, and it is the reason the property
is written here rather than assumed.

### U7 pickup plan

Registered before U7 begins, as the skill requires for each unit at its own pickup. U7 is granted
and starts after U6. Scoped on 2026-09-21 by reading the frozen specification at
`siteplan/docs/PLAN-FORMAT.md` (`fe8433b`).

#### The design, confirmed: the report states what is true, the gate decides what is tolerable

The principal confirmed **design A** on 2026-09-21 — a distinct severity in the finding model, with
`--strict` mapping severities to exit codes rather than creating findings. The general form is worth
stating because it governs three of the fixes in this record and a later reader would otherwise
repair one and reintroduce another:

> **The report states what is true. The gate decides what is tolerable.** Whether a plan's version is
> unknown is a fact about the file; whether that fact should fail a build is a policy.

Design B — creating the finding at `error` severity only when `--strict` is set — lets the policy
write the fact, so two runs of the same site against the same plan could disagree, and comparability
is the only thing that makes a report checkable at all. The same separation is already at work in
U6 (the robots skip is a fact; whether it gates is policy) and in U7's fifth criterion (an unchecked
surface is a fact; whether it fails is policy).

#### One new severity, not two

| Severity | Meaning | Gates under `--strict` |
| --- | --- | --- |
| `error` | Something is wrong with the site as built | Yes |
| `conditional` | **New.** The verdict depends on something this consumer does not know, so the result is not a clean one: an unknown or newer plan version, an absent or mistyped one, or a required surface the consumer has no check for | Yes |
| `info` | An observation or a site's own choice, with nothing left unknown | No |

Both version cases and the unverified surface take `conditional`. They could have been split —
`conditional` for the version, `unverified` for the surface — and that was rejected: the two say the
same thing about the verdict, that it is not fully supported, and two names for one meaning is how a
severity table stops being readable. The distinction the principal drew between them is in the
**message**, which must differ, not in the severity.

#### The correction: an unchecked surface gates under `--strict`

This criterion first said an unchecked surface "fails nothing". **That contradicted the severity
table above and the table wins**, corrected on the principal's direction of 2026-09-21. The reason
it was wrong is worth keeping, because it was not carelessness: the concern behind it was **not
punishing a site for a gap in the tool**, and that concern is real.

The resolution is the one already built elsewhere in this record: **disclose by default, refuse when
asked to certify.** A default run reports the unchecked surface and exits 0, so no site fails for a
gap in `sitewalk`. `--strict` is opt-in and exists to refuse results that cannot be certified, and a
gate whose job is to certify that a built site meets its plan cannot certify a plan it is unable to
check. Passing while part of the plan went unexamined would be the same overclaim this unit exists
to remove, one level up: not "the site lacks `rss.xml`" but **"the site satisfies the plan"**, when
the tool does not know.

So one fact, one severity, two policies — the same shape as the rest of this record.

#### A consequence to state rather than discover: two surfaces can never pass a strict gate

With the format's closed vocabulary at five surfaces and this consumer checking three, **any plan
whose `required_surfaces` names `rss.xml` or `json-ld` can never pass a `--strict` run.** That is a
real design consequence, not a bug, and it pushes a decision: implement those two checks, or stop
naming them in `required_surfaces`. Registered as open item **Q7** below with its owner, rather than
left for whoever first runs `--strict` against such a plan.

#### The two consequences, made explicit

1. **The severity reaches the JSON, not only the summary.** A machine reader is the one most likely
   to treat a conditional verdict as a clean one, and the JSON is the contract. `severity` already
   appears per finding; `finding_counts` gains a `conditional` key so a consumer can read the
   verdict without walking the list.
2. **The severity is named and defined in the report's own documentation**, so a consumer does not
   have to infer its meaning from the exit code — which is the thing design A exists to prevent.
   The definition goes in the text report's legend, in `README.md`, and in `docs/DESIGN.md`.

**The exit-code mapping is written as a policy table, not as a condition buried in code:**

| Findings present | Exit without `--strict` | Exit with `--strict` |
| --- | --- | --- |
| Any `error` or `conditional` | 0 | 1 |
| `info` only, or none | 0 | 0 |

#### Scope decision: one unit, not two

The principal offered a fifth criterion inside U7 or a separate U8. **It is folded into U7**, for
one reason: the version gate and the unverified-surface split are the same defect — the verdict
claiming more than the consumer knows — found in the same function and fixed in the same pass. Two
units would need two pickup plans, two reviews and two commits for one change to `check_plan`. That
is the choice, and it is recorded because the alternative was offered rather than assumed away.

#### The defect, stated precisely

`sitewalk` looks for three surfaces: `robots.txt`, `sitemap.xml`, `llms.txt`. The format's
`required_surfaces` is a closed vocabulary of five, adding `rss.xml` and `json-ld`. When a plan
requires one of those two, the enforcement path checks `report.surfaces`, finds no entry, and emits:

```
[ERROR] plan_surface_missing: the plan requires rss.xml, which the site does not publish
```

**That is a false claim about the site.** The tool never looks for `rss.xml`, so it cannot know
whether the site publishes one. "Not found" and "not checked" are different claims, and the report
makes the stronger one. This is the same class as the `sample`-style defects U1 removed and the
`Finding.detail` field that was written and never read: the output asserting something the code
never established.

**The rule for U7:** a required surface the consumer has no check for is reported as
**unverified**, the output says the tool does not check it, and it is a `conditional` finding — so a
default run discloses it and exits 0, and a `--strict` run refuses to certify the plan. The closed
vocabulary and the consumer's capabilities are then free to drift apart without the report lying
about it, and without a gate certifying a plan it could not check.

#### The version rule, with the fourth case

| Input | Verdict | Gate |
| --- | --- | --- |
| `plan_version` 1 | Met, unqualified | — |
| An **older** version | Met, unqualified: an older plan is fully specified by its own version | — |
| An **unknown or newer** version | Conditional. The plan is **valid** against a specification this consumer does not hold, so the keys it reads may mean something else | Error finding under `--strict`; in default mode the condition appears in the summary, not in Notes |
| An **absent or mistyped** version | A definite fault: the plan is **invalid** against every version, and with no readable version the consumer cannot know the semantics of any key, so a clean verdict is not conditional but unsupported | Error finding under `--strict`, with a message distinct from the unknown-version case |

The two failing cases share a gate and differ in what they say about the file. Conflating them would
tell a reader "this might be a newer format" when the truth is "this file is malformed", which is
the more actionable of the two.

#### Test-design trap, carried forward

The conformance fixture holds 45 cases: 7 valid, 38 invalid by design, testing the *producer's*
messages for faults such as `pages[0].title`. Rule 6 explicitly permits a consumer to carry and name
what the producer rejects, and this consumer is deliberately tolerant, so **the 38 must not be
asserted as failures for `sitewalk`**. Loading all 45 as accept-cases would produce a suite that
fails 38 times while being wrong about the specification. This is the fourth instance of the
"check that cannot fail" class — caught before writing the test rather than after — and it joins P1's
record when that lands.

The fixture already contains the version cases U7 needs: `unknown-version` (`plan_version: 2`) and
`version-not-an-integer` (`"1"` as a string).



**What the specification now requires, and what changes.** The format's rule 4 — *keys grow,
versions announce* — splits a treatment this consumer currently applies uniformly:

| Input | Today | Required |
| --- | --- | --- |
| Unknown key | Ignored, named in a note | Unchanged. **Naming every ignored key is the condition of the permission, not advice** |
| `plan_version` 1 | Met, unqualified | Unchanged |
| An **older** version | Met, with a note | Read normally, unqualified: an older plan is fully specified by its own version |
| An **unknown or newer** version | Met, with a note | **Conditional.** The summary carries the condition in default mode, and under `--strict` it is an error finding and exits non-zero |
| An **absent or mistyped** version | Note, non-gating | Reported as the fault in the file that it is, and not conflated with the unknown-version case |

**Two designs considered.** Either the conditional verdict is a distinct severity in the finding
model, or the version finding is created at `error` severity only when `--strict` is set. The first
keeps the report a pure function of the site and the plan, which is what makes the report
comparable between runs; the second lets the exit status decide a fact about the file. **The first
is preferred** and will be registered with its reason when U7's pickup plan is written.

**A test-design trap, recorded because U6 is about to hit the same class.** The conformance fixture
holds 45 cases, of which **38 are invalid by design** — they test the *producer's* messages for
faults such as `pages[0].title` or a mistyped `identity.schemaTypes`. A consumer is explicitly
permitted by rule 6 to carry and name what the producer rejects, and this consumer is deliberately
tolerant, so **those 38 must not be asserted as failures for `sitewalk`**. Loading all 45 as
"must pass" would be a test asserting the opposite of the specification. U7 uses the seven valid
plans as accept-cases and may use a few invalid ones only to assert that tolerance holds and is
disclosed.

**The conformance fixture already contains the two cases U7 exists for**: `unknown-version`
(`plan_version: 2`, expected producer message "expected 1, got 2") and `version-not-an-integer`
(`"1"` as a string). So U7 can test the split without inventing a fixture, which is the same
discipline U6 now follows.

**Capability note, resolved.** `--plan` implements only `required_surfaces` and
`identity.schema_types`; the fixture's `required_surfaces` values are from a closed vocabulary
(`robots.txt`, `sitemap.xml`, `llms.txt`, `rss.xml`, `json-ld`) and three of the four are not
surfaces this tool looks for. `rss.xml` on a valid case would therefore be reported unmet. That is
the existing disclosure doing its job — the output names the surfaces it did not find — and it is
recorded here rather than discovered later as a surprise.

**Acceptance criteria for U7:** the five registered in the unit table — the four version cases
and the unverified-surface rule, the last carrying its own correction — plus the severity's
presence in the JSON `finding_counts` and its definition in the report's documentation, and A8
and A9 staying green.

**Files U7 expects to touch:** `sitewalk/facts.py` (the severity), `sitewalk/plan.py`,
`sitewalk/report.py`, `sitewalk/findings.py`, `tests/test_plan.py`, `tests/test_cli.py`,
`tests/test_findings.py`, `README.md`, `docs/DESIGN.md`, and this record.

### U8 scoping: the measured cost, and one asymmetry

Registered after U7. The principal granted it by ruling on 2026-09-21, **conditional on the cost
being what it looked like**, so the cost was measured before registering rather than after:

| Surface | What it needs | Measured |
| --- | --- | --- |
| `rss.xml` | Add the name to `SURFACE_PATHS`; the existing surface loop already fetches each name, records status, content type and bytes, and `_PAGE_EXCEPTIONS` derives from the same tuple | **One request, no new code path.** Confirmed: a missing `/rss.xml` behaves exactly like the other three in both sources, and a live crawl over the fake connection fetches it in the same loop |
| `json-ld` | A fact already held: `PageFact.json_ld_types` per page, aggregated today into `report.json_ld_type_counts`, which is reported and otherwise unused | **No request at all.** Confirmed: 4 of 11 fixture pages carry JSON-LD, and the site-wide type counts are already computed |

**The asymmetry: `json-ld` is not a URL.** `robots.txt`, `sitemap.xml`, `llms.txt` and `rss.xml`
are paths; `json-ld` cannot be fetched and is established from pages already read. A `Surface`
carrying `url` and `status` cannot represent that, and a synthetic entry with two nulls **does not
read as "derived" — it reads as "we fetched it and learned nothing"**, which is a different and
worse claim. That is the `Finding.detail` lesson arriving early: a field whose absence has two
possible meanings is read as the wrong one.

**So the requirement is four distinguishable states, in the JSON and not only in prose:**

| State | Fetched | What it means | Plan verdict |
| --- | --- | --- | --- |
| `present` | yes, 2xx | The site publishes it | Met |
| `absent` | yes, non-2xx | The site does not publish it | Unmet — a real finding about the site |
| `derived` | no, and there is nothing to fetch | Established from pages already read, such as `json-ld` | Met or unmet on the derived fact |
| `not_checked` | no, because this consumer has no check | The gap. Named, `conditional`, gates under `--strict` | Neither met nor unmet: **unverified** |

**The shape is U8's to pick** — a `kind` discriminator on `Surface`, a separate derived-surface
record, or a second lookup path — and the tiebreaker is the preference for a single lookup in the
plan check. What is not optional is that a machine reader tells state 2 from 3 from 4 without
reading a message string.

**A defect the requirement exposed, present today.** The plan check currently reads:

```python
surface = report.surfaces.get(name)
if surface is None or not surface.exists:
    check.unmet_surfaces.append(name)
```

`surface is None` is the *not checked* case and `not surface.exists` is the *absent* case, and the
two are collapsed into one branch. That is why the `rss.xml` false claim was possible: an unchecked
surface took the path meant for an absent one. **The lookup itself has to change, not only the
record's shape** — an unchecked surface must never enter `unmet_surfaces`.

**Verification, as required: make the wrong change and watch it fail.** For U8 that means
deliberately collapsing two of the four states in the model and confirming the tests fail — the
assertion must be on the state a machine reads, not on a message. The same discipline caught the
script-shell thresholds and the `check-project.sh` pipe.

**What does not change.** The closed vocabulary stays at five. A surface this consumer cannot check
is still named in the output, still `conditional`, and still gates under `--strict` — implementing
two checks makes the gate able to certify more, it does not make the disclosure optional. If the
format adds a sixth surface, the same gap reopens and the same rule applies.

### U11 pickup plan

Registered before U11 begins. U11 is the disclosure rule of the format's rule 6, made structural.

**Why it is a defect and not a polish.** Rule 6 and rule 4 both make the disclosure the *condition*
of tolerating something: a consumer may carry an unknown key precisely because it names what it did
not check, "and that disclosure is the condition that makes tolerance permissible — not advice about
it". This consumer names ignored keys in `report.notes`, which is rendered in the text report and
serialised as a bare string array. A machine consumer reading `findings` cannot see them, so the
condition the format relies on is not met for the consumers most likely to act on it.

**The audit of every tolerated case, run before the fix** (2026-09-22), because the principal asked
whether the same shape appears elsewhere — the four surface states, the version conditions and the
ignored keys are all "the verdict depends on something the consumer knows or does not know":

| Tolerated case | Reaches the machine-readable output? |
| --- | --- |
| Version conditions (unknown, newer, absent, mistyped) | **Yes** — `plan_verdict_conditional` and `plan_invalid` findings, plus `plan.conditions` |
| Unverified surface | **Yes** — `plan_surface_unverified` finding, plus `plan.required_surfaces_unverified` |
| Four surface states | **Yes** — `surfaces[name].state`, with `surface_states` declaring the vocabulary |
| Robots skips | **Yes** — `skipped_robots[]` with the quoted rule, plus `limits.paths_skipped_robots` |
| Truncated bodies | **Yes** — `pages[].truncated` per page, and a note |
| Script-rendered pages | **Yes** — `pages[].looks_script_rendered` with the heuristic's own evidence, plus an `info` finding |
| Sitemap URLs never reached | **Yes** — `findings`, plus `sitemap.never_reached` |
| Surface not found | **Yes** — a `surface_missing` finding with its state |
| **Ignored plan keys** | **No.** A `notes` string only. **This is the single gap** |

**The fix.** `check_plan` already collects the ignored keys in a note; it will collect them as data
as well, and `apply_to_report` will emit them as `info` findings naming each key. Information rather
than `conditional`, because an ignored key is additive growth the format permits a consumer to carry
— it does not make the verdict unsupported the way an unknown version does.

**The guard, per the principal's point (4).** Each row of that table gets an assertion on the JSON,
so a later change that confines any tolerated case to prose fails a test. This is the shape-rule
applied to the report: the audit is not evidence unless something keeps it true.

### U9 scoping: the test U1 used, applied to everything

Finch's assessment returned two defects that **fail U1's own deletion test** — the test that removed
`Page.final_url` for being written and never read, and `_SITEMAP_NS` for having no caller. Finch's
words: *"an audit that finds exactly the things it was pointed at is not yet an audit."*

| Item | Evidence | Fix |
| --- | --- | --- |
| `Address.host`, `Address.port`, `Address.family` | Written at `guard.py:57` and `guard.py:135` and in `tests/fakes.py:40`; **no attribute read anywhere**. Checked by hand after a name-level scan gave a false negative, because `parts.port` and `target.port` in `urls.py` put `port` in the package's read set | `Address` keeps `sockaddr`, which is the only value the guard reads (`address.sockaddr[0]`), and drops the rest. `host` and `port` are the caller's own arguments echoed back, and `family` is needed only when constructing a literal address, not when holding one |
| `PlanError` | Defined in `errors.py`, zero references in the package or the tests, not exported | Removed. `FetchError` is kept and is *documented* as raised only on an unreachable path, because removing a real error type is a different decision from removing an unused name |
| `plan.identity_schema_types_met: true` with `passed: false` | Reproduced: a malformed plan sets both | The malformed case must not report a met sub-check. Same overclaim shape as U8's four states, which is why the fix lands after U8 |
| DESIGN drift | D6 names `app_root_markers` (the key is `app_root_element`); D1 describes the protocol as `read(path)` (it declares `fetch`) | Corrected. Documentation describing code that does not exist is the same defect class as a test that cannot fail |

**The re-run is the unit's real deliverable.** A name-level scan over the package and tests was
already run and gave false negatives — it put any attribute of a given name anywhere into the read
set — so U9 must run the test at the attribute and constructor-keyword level, and **record the result
even if it is nil**, because a nil result from an exhaustive test is a finding and an unrecorded scan
is not.

**P1 applies to this unit's own fixes**: each removed name needs the test that would fail if it came
back, and each corrected document claim needs the assertion or check that catches it drifting again.

**Acceptance criteria for U9:** the six in the unit table, plus A8 and A9 staying green.

**Files U9 expects to touch:** `sitewalk/guard.py`, `sitewalk/errors.py`, `sitewalk/plan.py`,
`sitewalk/facts.py`, `tests/test_guard.py`, `tests/fakes.py`, `docs/DESIGN.md`, and this record.

### What the frozen format left open, and what this consumer inferred

Registered 2026-09-22 at `siteplan`'s request, relayed by the principal. Their review closure records
a limit they cannot close from their side: **one reader's successful implementation can absorb
ambiguity in silence, and nobody has asked the implementer what it had to infer.** U7 and U8 were
built against `siteplan/docs/PLAN-FORMAT.md` at `fe8433b` with no shared code, so this is the
evidence that closure lacks. **These are document defects, not consumer choices**: `siteplan` owns the
format, and each item below is a case where a second implementer could reasonably decide differently
and produce a different verdict from the same file.

| # | What the document does not settle | What this consumer inferred, and where | Consequence for a second implementer |
| --- | --- | --- | --- |
| G1 | **`json-ld` is "Schema.org JSON-LD in the HTML of the pages it describes"** — the document never says which pages, nor whether the requirement means the home page, every crawled page, or any page. This is the only vocabulary surface that is not a URL, so it is also the only one with no fetch to define it | **Any crawled page carrying a `@type` satisfies it**, whichever page that is (`plan.py`, the derived `json-ld` surface in `crawl.py`) | A consumer requiring it on the home page, or on every page, returns a *different verdict* for the same site. Verified: a site with JSON-LD only on a deep page **passes** here |
| G2 | **"an unknown version … makes the verdict conditional … it is an error finding and exits non-zero"** never says whether reading continues, and the document does not distinguish a version below 1 from a known or older one | **Reading continues**, and a version below 1 is treated as older and read cleanly (`plan.py`) | A consumer that stops at a version it does not implement reports one fault where this reports keys as checked |
| G3 | **A malformed file with an unknown version has no prescribed exit** — rule 4 gives `conditional` for "unknown or newer" and is silent on absent or mistyped | **An error that gates.** This is **the principal's ruling**, given on 2026-09-21 in answer to this project's question whether a missing version should gate — not a shared inference and not this consumer's reading. It is recorded here as it stands: **a gap in a frozen document that a principal has already filled by decision**, and `siteplan` should know the decision exists because a second implementer has no way to reach it from the document | A consumer could reasonably call it conditional, and the two disagree about whether a strict run passes. The disagreement is between a consumer and a **ruling**, not between two readings |
| G4 | **Duplicate JSON keys are "a matter for the JSON parser"** — no consumer behaviour is defined | **Detected and refused** (corrected 2026-09-22). `json.loads`' default is last-value-wins and silent, but `object_pairs_hook` sees the pairs before they collapse, so `load_plan` raises `duplicate key 'site' in the same JSON object` and the run exits 2. Nested objects are covered by the same hook. **The first version of this row said the document "has no way for a consumer to detect it at all", which was false** and is the sentence that would have stopped someone fixing it | A consumer using a parser that keeps the first value reads a **different plan from the same bytes**. That divergence is now refused here rather than resolved silently, so the one input that triggers it is visible |
| G5 | **"A consumer may carry it and report it as *not checked*"** — "carry" is undefined, and rule 6's "naming every key it ignored is the condition of that permission" does not say *where* naming happens | **Named in the human-readable notes only**; the ignored key is not a finding and does not appear in the machine-readable `findings` array | A machine consumer of the JSON cannot see which keys were ignored without parsing prose. Verified: the note carries the key, the findings array does not |

**G1 and G4 are the two worth fixing first.** G1 changes a verdict on a normal site. G4's ambiguity
is now closed on this side — duplicates are refused rather than resolved — but the document still
leaves it to the parser, so a producer cannot warn about what it cannot check, and a consumer without
the hook still diverges silently. **G4's correction is itself the lesson**: this row first claimed
detection was impossible, which would have stopped anyone fixing it; the principal caught it. "Not
detectable" is a strong claim and needed the check that any strong claim needs.

**What was not inferred.** The four version cases, the closed-vocabulary behaviour, the
open-vocabulary Schema.org handling, the "no shared code" boundary and the nine keys all matched the
document as written, and the implementation needed no clarification from `siteplan` for any of them.
Whether the conformance fixture answered anything the prose did not: **`version-not-an-integer` and
`unknown-version` confirmed decisions already taken from rule 4**, and no case contradicted the
reading above. The fixture was used as the document says it may be, and 38 of its 45 cases were
deliberately not asserted as consumer accept-cases, because they test the producer's faults.

### U6 pickup plan

Registered before U6 begins. The principal granted U6 on 2026-09-21 and confirmed the shape below;
the tree was frozen for Finch's independent assessment, so U6 starts only after that returns and
its findings are taken on their merits.

**How U6 will be carried out, and the shape it will take.**

1. **`sitemap.Rule` carrying `(pattern, source_line)`**, and `is_disallowed(path, rules)` returning
   the matching `Rule` or `None` rather than a bool. The rule is unrecoverable at both ends today:
   `parse_robots` discards the line that produced each pattern, and `is_disallowed` discards which
   pattern matched.
2. **`source_line` is the line exactly as read from `robots.txt`** — the whole line, with any
   leading whitespace, internal spacing and trailing comment intact. Not reconstructed from the
   parsed parts, and not normalised. The value of quoting is that a reader can take the string out
   of the report, search the file, and find it; a reconstruction that is *almost* the line defeats
   the purpose while looking like it works.
   - **This is not the same as the `line` variable the parser already computes.** That variable is
     the result of `raw.split("#", 1)[0].strip()`. Quoting it happens to pass on the current
     fixture, whose `Disallow:` line has no comment and no padding, and fails on
     `Disallow: /private/   # legacy` by silently dropping the comment. The line kept must be the
     one as read.
   - The line is kept **without its newline**, because `splitlines()` removes it and a quote
     carrying a terminator would not be byte-identical to anything a reader can select in the
     file.
3. **The count in the header, and `paths_skipped_robots` in the JSON `limits`**, so a reader who
   reads only the summary cannot reach the end of the report without knowing something was
   excluded.
4. **No flag.** A gate whose scope depends on a switch is a gate nobody can compare across runs.
5. **The fixture must be able to tell the two implementations apart, and today it cannot.** The
   plan above names the raw-versus-processed distinction, and naming it does not fix it: a
   documented distinction with no fixture that exercises it is the same defect U1 already found
   when a boundary test imported the constant it was testing. So U6 changes
   `tests/fixtures/example-site/robots.txt` to carry a deliberately ugly `Disallow` line — leading
   whitespace, irregular internal spacing, and a trailing comment with a marker that appears
   nowhere else in the fixture:

   ```
     Disallow:   /private/   # legacy, revisit
   ```

   The parser reads that as the pattern `/private/`, so the existing skip tests keep their meaning.
   The report must quote the line as it stands, comment and padding included.
   - **The assertion is equality, not membership.** The naive version of this test —
     `assert processed_line in fixture_text` — cannot fail, because the processed string is a
     substring of the raw one. Both are findable in the file; only one is the line. So the test
     asserts that the report's quote **equals** the fixture line, which fails under the wrong
     implementation.
   - **Verified by making the wrong change once and watching it fail**, as `check-project.sh` was
     verified in U1, rather than by reasoning that it would.
   - The trailing-comment case is chosen deliberately over the alternative of finding a rule whose
     comment is not last in the file: robots.txt has no such ordering, so the trailing comment is
     the available separator, and it separates the two implementations on its own.

6. **Tests assert the three surfaces independently, not a helper that both produces and checks
   them** — this project has already been bitten once by a test that could not fail (the
   script-shell thresholds, U1). In particular: take a rule out of the fixture and require the
   report's quote to appear **byte-identical** in the fixture file it came from, so a
   reconstruction that is merely close fails.

**Why this shape.** Two alternatives were considered and rejected:

- **Re-deriving the rule at the call site** by rescanning `robots.txt` where the report is built.
  Smaller diff, and rejected because it would put the `applies` state machine (`User-agent: *`
  versus `sitewalk`, comments, an empty `Disallow:`) in two places. The trade is not smaller diff
  against larger diff, it is **one source of truth against two** — and a report that quotes a rule
  its own crawler did not use is worse than one that quotes nothing.
- **A positional third tuple element.** Every unpacking site changes anyway, and it makes each
  future addition another positional decision. A named object absorbs the next field without
  touching a call site.

Both reasons are recorded because a later reader would otherwise reopen a settled choice: the
first is a correctness argument that is invisible in the diff, and the second is why the small
option was not taken.

**Acceptance criteria for U6:** the four registered in the unit table, plus A8 and A9 staying
green.

**Files U6 expects to touch:** `sitewalk/sitemap.py`, `sitewalk/crawl.py`, `sitewalk/facts.py`,
`sitewalk/report.py`, `sitewalk/findings.py`, `tests/test_sitemap.py`, `tests/test_crawl.py`,
`tests/test_dir_mode.py`, and this record.



### A standing rule for tests in this project

Adopted 2026-09-21, on the principal's suggestion, because the same class of defect has now been
found twice in this repository by two different routes: **a check that cannot fail.**

| Found | How it could not fail |
| --- | --- |
| The script-shell thresholds (U1) | The boundary test imported the constant it was testing, so moving the threshold from 200 to 5000 kept all 243 tests green |
| `scripts/check-project.sh` (U1) | Its test step piped the suite into `tail`, so `set -e` saw `tail`'s exit status and `make ci` printed "ci passed" with two failing tests |
| The raw-versus-processed quote (U6, caught before implementing) | The fixture's `Disallow:` line had no comment and no padding, so the deliberately wrong implementation would have passed |

**The rule.** For every new test and every new fixture, answer one question in the test itself or
in the record: *which wrong implementation would this catch?* If the answer is none, the test is
decoration and the fixture is decoration with it. A test that asserts only that a function returns
what the function returns is not evidence, and it is worse than no test because it is counted.

**It applies to fixtures, not only to assertions.** The U6 case is the sharper one: the assertion
was reasonable and the *fixture* could not distinguish the cases, so the test would have passed
against a wrong implementation while looking correct. A fixture that cannot separate a right
implementation from a plausible wrong one is not a fixture.

**Stated where.** The same rule belongs in `AGENTS.md` under the definition of done, so a worker
who never reads this record still meets it. That is a process change to a file outside this
record's scope, so it is **not** made here: it is registered as proposal P1 under the requested
grant, to be applied when the principal authorises a change to `AGENTS.md` or when U6 runs under
the grant that already includes that file.

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
| ~~Q7~~ **resolved** | **Two required surfaces could never pass a strict gate.** The format's vocabulary is five surfaces; this consumer checked three. **Resolved by the principal's ruling of 2026-09-21: implement the two missing checks**, because `required_surfaces` is a closed vocabulary describing what a plan may legitimately require, not what one tool happens to look for. Narrowing it to three would delete a real requirement — a site with an RSS feed is a normal site — to accommodate a gap in the consumer, so the gap is the thing to close. Registered as **U8** | Ruling: David, 2026-09-21. The ruling was **conditional on the cost**, so the cost was measured before registering: see U8 | Closed. U8 carries it |

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
| U6 — the robots skip is unmissable | `tests/test_dir_mode.py::TheRobotsSkipIsUnmissable`, `tests/test_sitemap.py::TheSourceLineIsVerbatim`, and the injected wrong implementation | Moss, at U6 delivery, 2026-09-21 | **Met, and verified by breaking it.** The count is in the report header (`excluded: 1 path(s) …`), `limits.paths_skipped_robots` is in the JSON, each skip quotes its rule, and the quote is **byte-identical** to the fixture line including its leading whitespace and trailing comment. The wrong implementation — storing the parser's stripped variable — fails **five tests** and `make ci` exits 2; the fixture-integrity assertion fails with it, which is the guard against the fixture quietly losing its ability to separate the two | Accepted as a self-check. The wrong-change verification is the evidence that the tests can fail |
| U11 — the disclosure reaches the machine-readable output | `tests/test_plan.py::TheDisclosureReachesTheMachineReadableOutput`, and two injected regressions | Moss, at U11 delivery, 2026-09-22 | **Met, and verified by breaking it.** Every ignored key is now an `info` finding naming it, and appears in `plan.ignored_keys` as data. The audit of every other tolerated case is recorded in the pickup plan and **each row is asserted on the JSON**, so a later change confining one of them to prose fails a test. Confining the ignored-key disclosure to prose again fails 2 tests; removing `skipped_robots` from the JSON fails 4; `make ci` exits 2 for both | Accepted as a self-check. The finding the principal asked for — whether the same shape appears elsewhere — is a **nil result**, recorded as such in the audit table rather than left as an absence |
| U9 — the deletion test, run across the package | The attribute-level scan (result below), `tests/test_guard.py::TheAddressHoldsOnlyWhatIsRead`, `::NoDeadErrorTypes`, `tests/test_plan.py::ASubCheckReportsWhetherItRan`, and two injected wrong changes | Moss, at U9 delivery, 2026-09-21 | **Met, and the re-run returned a finding rather than nil.** `Address.host/port/family` and `PlanError` are removed. Field counts come from **`tools/field_count.py`**, committed so the number is re-derivable rather than published: `python3 tools/field_count.py --revision 9dfb88e` reports **128** (126 dataclass + 2 protocol) and `--revision 81413bd` reports **124** (124 + 0), a net of **−4**: `Address` −3, `PageSource` −2, `PlanCheck` +1. The scan's single hit, `PageSource.label`, was a **false positive** — it is read through `getattr(source, "label", "")` into the report — and the real defect was the Protocol declaring `kind` and `label`, members no source must implement. **The two counts published in earlier revisions of this row (115 → 113, "fell by two") were wrong**: they came from a counting script that missed `@dataclass(frozen=True)` and read `class X(Protocol)` as no protocol at all, and I corrected the row for exactly this defect without re-running the count. Finch's independent count differs by 5 at both revisions (123 → 119, same −4 delta); the scripts disagree on which classes count, the delta agrees, and committing this one is what makes at least one of the two reproducible. The plan's `required_surfaces_met: true` beside `passed: false` is fixed: a sub-check that did not run reports `None`, not `True`. Both wrong changes fail tests and `make ci` | Accepted as a self-check. The one hit being a declaration error rather than dead code is the honest result, and it is recorded as such rather than as a clean nil |
| U8a — `not_checked` is load-bearing and survives a dead-code audit | The comments at the constant in `sitewalk/facts.py` and at the branch in `sitewalk/plan.py`, plus `tests/test_plan.py::ANotCheckedSurfaceIsStillHandled` and the injected removal | Moss, after U8, 2026-09-21 | **Met, and verified by removing it.** The state is currently unreachable, and U9's own audit is the thing that would delete it — restoring the overclaim U7 and U8 removed. So the reason it exists, what would make it reachable (a sixth vocabulary value, or a surface leaving `CHECKED_SURFACES`), and which tripwire fires first (`EveryVocabularySurfaceHasACheck`) are stated **in the code**, at both the declaration and the branch; and its handling is enforced by a test that fails if the state or the branch goes. Removing the handling fails two tests and `make ci` exits 2 | Accepted. Prose in a record is not where a future auditor looks; a comment at the branch and a failing test are |
| U8 — the vocabulary is fully checked, and four states are distinguishable | `tests/test_dir_mode.py::TheFourSurfaceStatesAreDistinguishable`, `::ARssFeedIsCheckedLikeAnyOtherSurface`, `tests/test_plan.py::EveryVocabularySurfaceHasACheck`, and two injected wrong changes | Moss, at U8 delivery, 2026-09-21 | **Met, and verified by breaking it.** All five vocabulary surfaces are checked: `rss.xml` fetched in the existing loop (one name added) and `json-ld` derived from pages already read (no request at all). Four states are machine-readable — `present`, `absent`, `derived`, `not_checked` — with `exists` derived from the state so they cannot disagree, and the state vocabulary printed in the run. The wrong change that makes `derived` imply `exists` fails a test and `make ci`; collapsing `derived` into `absent` fails six | Accepted as a self-check. **One bug was found in this unit's own work**: `exists` returned True for every derived surface, so every site appeared to publish JSON-LD — the same overclaim class the states exist to prevent. Caught by asserting the bare fixture's derived surface is False |
| U7 — the verdict is honest about what it knows | `tests/test_plan.py::TheVerdictIsHonestAboutWhatItKnows`, `::AnUncheckedSurfaceIsUnverifiedNotAbsent`, and injected mutations | Moss, at U7 delivery, 2026-09-21; **mutation counts re-measured 2026-09-22** | **Met.** Four version cases: 1 and older read clean; newer or unknown is `met with conditions` and gates; absent or mistyped is `not met` and gates, with a message that says *malformed* rather than *may be newer*. A vocabulary surface this tool cannot check is **unverified**, never absent. The third severity is defined in the output and reaches `finding_counts` and `severities` in the JSON. **Mutation evidence, corrected.** An earlier version of this row said "restoring the original line fails three tests"; that was wrong, and Finch caught it. Re-measured at `81413bd`: **restoring the literal pre-U7 line (`surface is None or not surface.exists`) fails 0 tests** — because `rss.xml` reaches unverified by two independent routes, the branch it deletes is not the one carrying it — while **routing the vocabulary-gap branch to `unmet` fails 3**. Re-measured on the current tree they fail **5** and **3**, the count having risen with the tests added since. **A mutation count is a property of a revision and a test set, not a fact about the code**, so it is cited with both or not at all | Accepted as a self-check, with the failed first mutation kept because it is P1's rule catching its author |
| Independent assessment of U1–U3 by an assessor who did not write them | A named assessor's return against A1–A9 | David to grant; not before delivery | **Not established for U1 or U2.** Moss wrote the package and the reconciliation, so A1–A5, A8 and A9 are a self-check. The two defects U1 found were both found by running code against injected breakage rather than by review, which is evidence that the checks work, not that the design is right | Requested in the return to the principal: name an assessor, or accept the self-check with its stated limit |
| B1–B3 (benefit) | Adopting projects' CI logs; a real run against a real site | David; trigger is U4 or a later adoption | Unobserved — needs a project and a site | Carry as U4 |

## Changes

Revision 26, 2026-09-22T04:15:00-06:00. **U11 is delivered; U10 remains held.** Source: U11's
committed evidence. Reason: each planned result is marked delivered with its evidence. What changed:
ignored keys reach the machine-readable output as findings and as data; the audit of every tolerated
case is recorded with the one gap it found, and each row is asserted on the JSON; and U10's row now
says plainly that it waits on the kind-awareness answer rather than on the grant. What is preserved:
G1–G5 and every earlier revision. Affects: U10, when the caveat is settled; **U4 keeps precedence
whenever Q2 is answered**.

Revision 25, 2026-09-22T03:40:00-06:00. **U10 and U11 are registered from the format routing, and
U11's pickup plan is written.** Source: the principal's grant of 2026-09-22, both arising from this
record's own G-findings. Reason: G1 and G5 were registered as document defects; Heron has ruled on
both, and the consumer side of each is this repository's work. What changed: U10 is registered and
**held** pending the principal's confirmation of whether home-page-only is right for kinds whose
structured data lives on inner pages; U11 is registered with its pickup plan, including the audit
of every tolerated case showing that ignored keys are the single one confined to prose. What is
preserved: G1–G5 as recorded, with G4's correction. Affects: U11 now; U10 when the caveat is
settled; **U4 retains precedence whenever Q2 is answered**.

Revision 24, 2026-09-22T03:00:00-06:00. **G4 is corrected: duplicates are detectable, and are now
refused. G3 is re-attributed to the principal's ruling.** Source: the principal's correction of
2026-09-22. Reason: the row claimed the format "has no way for a consumer to detect" duplicate keys,
which is true of the default `json.loads` call and false of the parser — `object_pairs_hook` sees the
pairs before they collapse. That is the defect this record keeps finding, in the section written to
report defects, and it is the sentence that would have stopped someone fixing it. What changed: the
row is corrected and marked as corrected; `load_plan` refuses a repeated key at any depth with the
key named, and the run exits 2; a test class covers top-level and nested duplicates, the legitimate
repeat across different objects, and that every conformance case still loads; and G3 now records that
the malformed-version behaviour is a **ruling by the principal**, not a shared inference — a gap in a
frozen document that a principal has already filled by decision. What is preserved: G1, G2, G5 and
every earlier revision.

Revision 23, 2026-09-22T02:15:00-06:00. **The Current position is rewritten, the rule that keeps it
current is in `AGENTS.md`, and the format's open points are registered.** Source: the principal's
observations of 2026-09-22 and `siteplan`'s request through him. Reason: the Current position still
described four units delivered when nine were, named a lifted freeze, reported 277 tests against a
suite of 331, and claimed U6 ungranted — the defect this record keeps finding, in the section a
reader and the dashboard see first. What changed: `Current position` now states position and points
at the tables for state, with the mode changes moved into a short history; `AGENTS.md`'s definition
of done gains the rule that a summary carries pointers rather than counts, with this instance in the
table; and the five points the frozen format left open are registered as G1–G5 with what this
consumer inferred, for `siteplan` to rule on as document defects. What is preserved: every earlier
revision and every criterion. Affects: the record's own reading, and `siteplan`'s format.

Revision 22, 2026-09-22T01:30:00-06:00. **Finch's verification pass is answered: six findings,
five confirmed and fixed, one withdrawn.** Source: Finch's assessment of `81413bd` and the
`37a1097` delta, relayed by the principal on 2026-09-22. Reason: every one of the six is P1's rule
reaching a place it had not yet reached — a claim in the record, a doc, or a test that the code does
not support. What changed: (1) U9's field-count arithmetic is replaced by a **committed script**,
`tools/field_count.py`, with the reproducible counts 128 → 124 and the itemised delta, and the two
earlier counts are marked wrong with the reason; (2) the exit-code documentation is corrected in
five places, README and `--help` alike, to say that `error` **and** `conditional` gate; (4) U7's
mutation evidence now names which mutation produced which count and records that a count is a
property of a revision and a test set; (5) the byte-identity test asserts **equality** against an
independently written line instead of membership, which now catches `source_line + "\n"`;
(6) `surface_missing` no longer says "no response" about a surface that was never fetched, and U7's
criterion 3 says `conditional` where it had said *error*. Finding 3 was withdrawn by the principal
after Finch's closing message confirmed the row was right. What is preserved: every earlier
revision. Affects: U9, U7, the README and the `--help` text.

Revision 21, 2026-09-22T00:45:00-06:00. **`not_checked` is made to survive the audit that would
delete it.** Source: the principal's requirement of 2026-09-22. Reason: the state is declared and
currently unreachable, and U9 — the audit that removes what nothing reaches — is exactly what would
remove it, silently restoring the overclaim U7 and U8 were built to prevent. What changed: the
constant and the branch in `plan.py` now say why the state exists, what would make it reachable, and
which tripwire fires first; and `ANotCheckedSurfaceIsStillHandled` fails if the state or its handling
goes. What is preserved: every earlier revision. Affects: nothing in the delivery's behaviour — the
code is frozen again immediately after this change, with the reason recorded.

Revision 20, 2026-09-21T00:20:00-06:00 (2026-09-22). **The code is held for Finch's assessment of
U6–U9, and one U9 evidence sentence is corrected.** Source: the principal's hold instruction of
2026-09-21 and a self-check of this record's own claims against the code. Reason: Finch is assessing
U6–U9 against `81413bd`, so the tree is frozen there; and a self-check of the evidence sentences
found that U9's deletion-scan numbers describe the state **before** the fixes, while a reader
re-running the scan now gets 113 fields and zero hits. Stating both, and the arithmetic, means an
assessor does not read the nil result as a contradiction. What changed: the U9 evidence row now
distinguishes the pre-fix audit from the post-fix state; and the position records the hold. What is
preserved: every earlier revision. Affects: nothing in the delivery — **no code was written, amended
or committed in this revision**, and none will be until Finch returns.

Revision 19, 2026-09-21T23:55:00-06:00. **U9 is delivered, and every unit in the grant is now
delivered or blocked.** Source: U9's committed evidence. Reason: each planned result is marked
delivered with its evidence before a stop. What changed: `Address` holds only `sockaddr`, the one
field the guard reads; `PlanError` is removed; a plan sub-check that did not run reports `None`
rather than `True`; `DESIGN.md`'s `read(path)` and `app_root_markers` are corrected; and the
deletion test was re-run at attribute level with its result recorded, including that its single hit
was a Protocol-declaration error rather than dead code. What is preserved: every earlier revision.
Affects: the unit table is complete — U1–U3 and U5–U9 delivered, U4 blocked on Q2.

Revision 18, 2026-09-21T23:10:00-06:00. **U8 is delivered and Q7's ruling is discharged.** Source:
U8's committed evidence. Reason: each planned result is marked delivered with its evidence. What
changed: `rss.xml` joined the fetched surfaces and `json-ld` became a derived one, so every surface
in the format's vocabulary is checked; `Surface.state` carries the four-way discriminator with
`exists` derived from it and `established` for derived surfaces; the plan check treats a
`not_checked` surface as unverified; and the state vocabulary is reported in both formats. What is
preserved: U7's disclosure rule, which now applies to a surface added in future rather than to the
two that existed, and every earlier revision. Affects: U9 next, which is the last registered unit.

Revision 17, 2026-09-21T22:30:00-06:00. **U7 is delivered.** Source: U7's committed evidence.
Reason: each planned result is marked delivered with its actual evidence before a stop. What
changed: the `conditional` severity exists with its definition in the output and in the JSON
`severities` map; `--strict` maps severities to an exit code through `GATING_SEVERITIES` and never
creates a finding; the four plan-version cases are implemented with distinct messages for a
malformed file and an unknown specification; an unchecked surface is `unverified` rather than
absent, with the two distinct routes to unverified both kept; and version 1's `{}`-is-usable
expectation is superseded by the frozen format's requirement that a file names its version. What is
preserved: every earlier revision and the five registered criteria. Affects: U8 next, then U9.

Revision 16, 2026-09-21T21:45:00-06:00. **U6 is delivered.** Source: U6's committed evidence.
Reason: each planned result is marked delivered with its actual evidence before a stop. What
changed: `sitemap.Rule(pattern, source_line)` carries the verbatim line and `is_disallowed` returns
the matching rule; `crawl` records a `Skip` with its rule; the report states the count in the header,
in `limits.paths_skipped_robots` and in a `skipped_robots` array, and quotes each rule in the notes;
the fixture's `Disallow` line is deliberately ugly so it separates the two implementations; and the
wrong change was made once to confirm five tests and `make ci` fail under it. What is preserved:
every earlier revision and the four registered criteria. Affects: U7 next, then U8 and U9.

Revision 15, 2026-09-21T21:00:00-06:00. **The freeze is released, P1 is applied, and Finch's
findings register U9.** Source: Finch's assessment as relayed by the principal on 2026-09-21, and
P1's grant. Reason: the assessor returned, so the held work could land — the record corrections, P1,
and a unit for the defects that fail U1's own deletion test. What changed: P1 is applied to
`AGENTS.md`'s definition of done with the five instances that earned it; U9 is registered with six
criteria and its scoping; the corrections themselves are recorded in U1's sub-record at revision 2,
which quotes the false A4 sentence rather than deleting it. What is preserved: the four assessed
criteria and every earlier revision. Affects: U9 after U8, and the delivery state, which returns to
`active` now that work resumes. **No code was written in this revision.**

Revision 14, 2026-09-21T20:05:00-06:00. **U8 gains the four-state requirement, and a live defect
it exposed is recorded.** Source: the principal's requirement of 2026-09-21 that a machine reader
distinguish fetched-and-present, fetched-and-absent, derived-and-not-fetched and not-checked-at-all
without reading a message. Reason: a `Surface` with two nulls does not read as derived, it reads as
fetched-and-empty — the same ambiguity that made `Finding.detail` a claim the code never
established. What changed: U8 gains a fourth criterion and the four states with their plan verdicts;
the cost estimate rises to 0.5–1 session; and the plan check's `surface is None or not
surface.exists` is recorded as the defect that let an unchecked surface take the absent surface's
path — the mechanism behind the `rss.xml` false claim. What is preserved: the disclosure criterion,
which now reads as state 4, and the vocabulary at five. Affects: U8. **No code was written, amended
or committed in this revision.**

Revision 13, 2026-09-21T19:40:00-06:00. **Q7 is resolved by ruling and U8 registers the two
checks.** Source: the principal's ruling of 2026-09-21, conditional on the cost. Reason: Q7 was
registered with an owner who was not going to answer it, and the ruling closes it by closing the
gap on this side — the vocabulary describes what a plan may require, so `sitewalk` grows the checks
rather than `siteplan` narrowing what it may ask for. What changed: Q7 is marked resolved with the
ruling and its condition; U8 is registered with three criteria; the measured cost of both checks is
recorded, along with the asymmetry that `json-ld` is not a URL and so takes a different shape from
the other four surfaces, to be decided when U8 starts. What is preserved: the disclosure rule and the
`conditional` severity, which the ruling explicitly leaves in place. Affects: U8, which runs after
U7. **No code was written, amended or committed in this revision.**

Revision 12, 2026-09-21T19:10:00-06:00. **A contradiction in U7's criteria is corrected, and its
consequence registered as Q7.** Source: the principal's correction of 2026-09-21. Reason: the fifth
criterion said an unchecked surface "fails nothing" while the severity table registered an hour
earlier put it under `conditional`, which gates — two statements in one plan that cannot both be
true, and living with both would have left the implementer to choose. What changed: the criterion now
reads that default runs disclose and exit 0 while `--strict` refuses to certify; the reason the
earlier wording was wrong is kept, because the concern behind it — not punishing a site for a gap in
the tool — is real and is answered by that split; and the design consequence that a plan requiring
`rss.xml` or `json-ld` can never pass a strict gate is registered as Q7 with its owner, rather than
left to be discovered. What is preserved: the severity table, design A, and every earlier revision.
Affects: U7, which starts after U6, and Q7, which awaits the principal. **No code was written,
amended or committed in this revision.**

Revision 11, 2026-09-21T18:45:00-06:00. **U7's pickup plan is registered with design A and one
new severity.** Source: the principal's confirmation of design A and its two consequences,
2026-09-21. Reason: a pickup plan registers before its unit starts, and two things had to be settled
rather than left to the implementation — how many severities the split creates, and where the
severity is defined. What changed: the general rule (*the report states what is true, the gate
decides what is tolerable*) is recorded as the form of three separate fixes; `conditional` is fixed
as one severity covering both version cases and the unverified surface, with the principal's
distinction carried in the messages rather than the severity; the exit-code mapping is written as a
policy table; and the JSON and documentation consequences are acceptance criteria. What is
preserved: every earlier revision and the four prior criteria. Affects: U7, which starts after U6.
**No code was written, amended or committed in this revision.**

Revision 10, 2026-09-21T18:15:00-06:00. **U7 is granted and its scope is fixed: the verdict must
not claim more than the consumer knows.** Source: the principal's grant and his correction of the
capability note, 2026-09-21, plus an inspection that reproduced the false claim. Reason: the plan
check emits `the plan requires rss.xml, which the site does not publish` for a file this tool never
looks for — a claim about the site the code never established, and the same class as the `sample`
defects U1 removed. What changed: U7 gains a fifth criterion (an unchecked surface is reported
unverified — **that criterion's "and fails nothing" wording was wrong and is corrected in revision
12; the criterion now gates under `--strict`**); the fourth version case now gates too, as an unsupported rather than
conditional verdict, with its own message; the scope decision to fold both into U7 rather than
split a U8 is recorded with its reason. What is preserved: every earlier revision. Affects: U7,
which starts after U6. **No code was written, amended or committed in this revision.**

Revision 9, 2026-09-21T17:30:00-06:00. **A frozen interface arrived from `siteplan`, and its rule
4 registers a new unit.** Source: the principal's relay of Heron's freeze notice, and
`siteplan/docs/PLAN-FORMAT.md` read at `fe8433b`. Reason: the format is now authoritative and
frozen, and its version rule differs from this consumer's behaviour — an unknown or newer
`plan_version` must be a conditional verdict and a `--strict` failure, where this consumer currently
notes it and passes. What changed: U7 is registered with four criteria and no grant; U7's scoping,
its two candidate designs and a test-design trap around the 38 deliberately invalid conformance
cases are recorded; P1 is marked granted and its application is held with the reason. What is
preserved: A1–A9 and every earlier revision. Affects: U7 and P1. **No code was written, amended or
committed in this revision**; the tree remains frozen at `24c27b`.

Revision 8, 2026-09-21T16:45:00-06:00. **U6's grant is confirmed, its shape is registered, and
the fixture gap it depends on is recorded as work.** Source: the principal's confirmation of shape
A and its two requirements of 2026-09-21, plus an inspection of the fixture. Reason: the plan
named a raw-versus-processed distinction that the current fixture cannot detect, and a documented
distinction with no fixture exercising it is the defect U1 already found once. What changed: the
pickup plan now requires a deliberately ugly `Disallow` line with a unique comment marker, an
equality assertion rather than a membership one, and verification by making the wrong change and
watching it fail; a standing rule for tests and fixtures is recorded with its three instances; and
proposal P1 registers the `AGENTS.md` change that would apply it beyond this record. What is
preserved: the four U6 acceptance criteria and every earlier revision. Affects: U6, and P1, which
awaits the principal. **No code was written, amended or committed in this revision.** The tree
remains frozen at `24c27b` for Finch's assessment.

Revision 7, 2026-09-21T16:10:00-06:00. **The robots.txt stance is recorded as a property, and U6
registers a gap it exposed.** Source: the principal's reply of 2026-09-21 confirming the stance and
requiring the skip to be unmissable, plus an inspection of the report. Reason: a property the
product depends on belongs in the record rather than implicit in the code, and the inspection found
that the skip is reported only in the Notes block — absent from the header, absent from `limits`,
and with the matched rule discarded — so the property is stated together with the fact that it is
not yet upheld. What changed: the stance and its evidence are recorded; U6 is registered with four
unmet criteria and no grant; the position now records the code freeze pending Finch's assessment.
What is preserved: A1–A9 as registered, and every earlier revision. Affects: U6, and the assessment
it waits on. **No code was written, amended or committed in this revision, and none will be until
the assessment returns.**

Revision 6, 2026-09-21T15:20:00-06:00. **U3 and U5 delivered and assessed against A6.** Source:
U3's and U5's committed evidence. Reason: each planned result is marked delivered before a stop.
What changed: A6's finding; U3's plan-version policy (any version read, unknown keys ignored, a
known key of the wrong type rejected) and U5's documents. What is preserved: A6's text as
registered. Affects: U3 and U5 delivered. U4 remains blocked on Q2, and is the only unit left.

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
