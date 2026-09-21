---
format: perspicuity-work/1
id: sw-2026-09-21-verify-before-keeping-package
revision: 1
skill_version: 0.5.0
updated: 2026-09-21
created_at: "2026-09-21T13:20:00-06:00"
updated_at: "2026-09-21T14:05:00-06:00"
record_status: open
work_status: submitted
---

# Verify the existing package before keeping any of it

## Current position

Parent: [RECORD.md](../../RECORD.md), revision 3 — alternative A, granted 2026-09-21.

Principal: David. Decider: David selected alternative A; Moss selected only inside it, as the plan
directed.

Work owner: Moss (coordinator).

Decision: `selected` — **the package is kept, but only where U1's independent re-derivation traced
it to a registered criterion; six items that no criterion needs were deleted and five
amendments were made.** Basis: the facts contract in [RECORD.md](../../RECORD.md) revision 2
criteria A1–A5, and the grant in revision 3.

Work scope: U1's reconciliation of the 2,592-line package that existed before the plan, and the
offline gate it delivers.

Work: revision 1 of this record is written **at U1's return, not at its pickup**. Timing is
stated rather than implied: the basis it applies was registered before the work, in
[RECORD.md](../../RECORD.md) revision 3 (*U1 pickup plan*, A1–A9). This record was not registered
separately at pickup, and a reader should know that the choice it describes was made under the
registered route rather than under a separate prior registration of its own.

Outcome: the package survived, with cuts. `make ci` exits 0, 244 tests pass with no network, and
every per-page fact and site-wide finding was re-derived independently and agrees.

Next: David — accept, correct or send back U1's delivery; the assessment is registered in the
parent's Review table, because acceptance belongs to the decider and not to the unit that
produced the work.
Dependency: nothing blocks this record. Its own acceptance waits on the principal, and its
independent assessment on an assessor he names.

## Frame and Decide

The problem is not "is this code good". It is: **the plan arrived after the code, so nothing has
judged whether the code implements the plan.** A plan that accepts the tree because the tree
exists is a receipt, and the principal said so explicitly when he ratified: "If U1 concludes that
most of the package goes, that is a successful U1."

So the question is what standard decides keep, amend or delete. Four candidates:

| # | Standard | Consequence | Verdict |
| --- | --- | --- | --- |
| A | The code exists and its tests pass | Cheapest. But the tests were written by the same increment that wrote the code, so a shared misreading passes both. This is the receipt failure | Rejected |
| B | Read each module and judge it | Catches design smells. But it is the same mind that wrote it judging it, against no external standard, and it produces opinions rather than evidence | Rejected |
| C | Discard everything and rebuild from the plan | Guarantees the plan is prior to the code. Cost: 2,592 lines of package and 2,378 of test, and every bug already found is rediscovered at the same price | Rejected — and it was alternative B in the parent, which the principal did not select |
| D | **Re-derive independently, then trust only what is traced** | Costs an audit. Produces evidence a stranger can check, and it can fail a module | **Chosen** |

The decisive consideration is what each standard can *detect*. A and B cannot detect a shared
misreading between code and test, which is the specific risk of a plan written after the work.
D can, because it compares the tool's output against expectations computed by different code, from
different inputs, by a different route.

### Selection

`selected_at` 2026-09-21T13:45:00-06:00. Decider: Moss, inside the grant. Basis revision:
[RECORD.md](../../RECORD.md) revision 3.

**The route chosen was D, and it was carried out as two independent derivations** — one for the
per-page facts, one for the site-wide findings — written without importing `sitewalk`'s parser,
then compared against the tool's output.

**Kept:** the architecture (one pipeline over two sources, the ported guard, `html.parser`), and
every module that a criterion traces to. No module was deleted wholesale: the audit found none
that failed to implement its criteria.

**Deleted — six items, none referenced by any criterion or by any other module:**

| Deleted | Where | Why it was dead |
| --- | --- | --- |
| `link_statuses()` | `crawl.py` | No caller. The crawl answers link questions from the pages it read; a URL-to-status map was never consumed |
| `PageFact.title_display`, `PageFact.description_display` | `facts.py` | No caller. The report formats these itself |
| `SiteReport.of_kind()` | `facts.py` | No caller. `errors_of` covers the one real use |
| `Page.final_url` | `facts.py`, `fetch.py` | Written by the fetch layer, read by nothing — the crawl reads `redirect_to`. Leaving both was two names for one idea, one of them wrong |
| `Finding.detail` | `facts.py`, `findings.py`, `report.py` | Always an empty dictionary, and no finding ever populated it. It was JSON output that claimed detail existed |
| `sources.METHOD`, `sources.surface_urls()`, `sources.default_source_dir()`, `sitemap._SITEMAP_NS`, `SitemapResult.add_urls()` | `sources.py`, `sitemap.py` | No callers. `_SITEMAP_NS` was declared and never applied, so it documented an intent the parser does not implement |

**Amended — five items:**

| Amended | Why |
| --- | --- |
| `scripts/check-project.sh` | Replaced the failing stub with real checks: byte-compile, the suite with the network unavailable, the entry point end to end, and the claim boundary in the output |
| `findings.py` — the `llms.txt` note | Carries its basis and its source. The principal decided it must not gate (Q5); the output now says why instead of only being non-gating by accident of the severity table |
| `report.py` — `script_shell_evidence` | The heuristic's own inputs (`script_bytes`, `script_blocks`, `app_root_element`) were computed and never shown. A labelled heuristic whose evidence is invisible asks to be trusted |
| `report.py` — `user_agent` | Collected and never printed. A site owner reading a report is entitled to know which client made the requests |
| `tests/test_pages.py` — threshold pinning | See the defect below |

### Two defects the audit found that reading would not have

1. **The heuristic's thresholds were silently tunable.** `test_the_threshold_boundary_is_inclusive`
   called `looks_like_a_script_shell(SCRIPT_SHELL_TEXT_CHARS - 1, ...)`, importing the constant it
   was testing. Moving `SCRIPT_SHELL_TEXT_CHARS` from 200 to 5000 kept every test green — verified
   by doing it and watching 243 tests pass. That is the gate's sensitivity, documented in
   [DESIGN.md](../DESIGN.md), changeable with no signal. Fixed by pinning both thresholds to
   literal values in a test whose failure message says they are recorded in DESIGN.md.
2. **The new check script could not fail.** Its test step was
   `python3 -m unittest ... 2>&1 | tail -n 4`, so `set -e` saw `tail`'s status — always 0 — and
   `make ci` printed "ci passed" with two failing tests. This is the exact bug the stub was
   replaced to prevent, reintroduced while replacing it. Fixed by capturing the suite to a file
   and testing its status directly.

Both were found by running the thing rather than by reading it, which is the argument for route D
over route B.

## Act

| # | Result | Done when | Actual evidence |
| --- | --- | --- | --- |
| 1 | Per-page facts re-derived independently | Each of the nine facts agrees with an independent computation from the fixture files | **0 mismatches across 12 fixture files.** Title, meta description, canonical (resolved absolute), JSON-LD `@type` lists, internal-link counts, status and content type compared exactly; visible text compared against a separate body-only measurement after the first attempt disagreed — see the note below |
| 2 | Site-wide findings re-derived independently | All twelve agree | **12 of 12 agree**: status distribution, sitemap URLs never reached, orphans, duplicate titles, duplicate descriptions, missing title, empty title, cross-host canonical, pages with no JSON-LD, both broken internal links, surfaces, and the JSON-LD type counts |
| 3 | Dead code traced and removed | Nothing left that no criterion needs | 6 items deleted, each confirmed to have no non-definition reference anywhere in the package or tests |
| 4 | Real project checks in place | `make ci` can fail on a real defect | Verified by breaking the code three ways: removing `surface_missing` from the non-gating set → `make ci` exits 2; moving `SCRIPT_SHELL_TEXT_CHARS` to 5000 → the pinned test fails; a syntax error in `urls.py` → exits 2. Restored after each, `make ci` green |
| 5 | The two failing CLI tests | Resolved | `LiveSource` now fills its resolver and connector from the modules at construction instead of capturing them as dataclass defaults at import, and `cli.build_live_source` is the single construction point. Both tests pass and the suite is whole |
| 6 | Standing constraints | `AGENTS.md` carries this project's | Twelve constraints derived from `CONTEXT.md`, replacing the template placeholder; the definition of done now describes the real checks rather than the stub |

**One audit correction, recorded because it is the method working.** The first visible-text
derivation disagreed with the tool on five pages. The audit was wrong: it counted text inside
`<head>`, including the `<title>`, which is not visible text. Corrected to measure the body only,
all nine agree. Had the audit been trusted over the tool, five pages of "text length is too short"
findings would have been invented — and had the tool been trusted without the audit, nobody would
have known the check was meaningful.

## Review

| Criterion | Evidence source | Owner, window or trigger | Finding | Response |
| --- | --- | --- | --- | --- |
| A1 — every per-page fact is produced | The two independent derivations, and `tests/test_pages.py` | Moss, at U1 delivery, 2026-09-21 | **Met.** Nine of nine facts agree with an independent computation across 12 fixture files, 0 mismatches | Accepted for the fixture. Not evidence for any site outside it — see below |
| A2 — every site-wide finding is produced | The findings derivation, and `tests/test_findings.py` | Moss, 2026-09-21 | **Met.** Twelve of twelve agree | Accepted |
| A3 — offline and live sources agree on the same bytes | `tests/test_dir_mode.py::DirAndUrlAgreeOnTheSameBytes` | Moss, 2026-09-21 | **Met.** Every field of every page is equal between the two sources reading the same fixture, not merely similar | Accepted. The fixture serves the same bytes both ways, which is the condition the criterion states |
| A4 — `--dir` makes no network request | `tests/fakes.py::no_network`, applied to every offline test and to three CLI tests | Moss, 2026-09-21 | **Met.** `python3 -m sitewalk --dir` completes inside a harness where any socket or name lookup raises | Accepted. The modules `--dir` reaches do not import `socket`; `urllib` is used only for URL parsing |
| A5 — no ranking, citation, traffic or recommendation claim; the no-JavaScript limit is stated | Output assertions in `tests/test_findings.py` and `tests/test_cli.py`, plus the check script's phrase check | Moss, 2026-09-21 | **Met.** A test asserts no finding's message contains ranking, citation, traffic, recommendation, score, grade or SEO vocabulary; the boundary is asserted in both output formats and mechanically in `check-project.sh` | Accepted |
| A8 — `make ci` exits 0 and the check it runs is real | `make ci`, and the three deliberate breakages | Moss, 2026-09-21 | **Met.** Green on the committed revision; exits 2 on each of three injected defects | Accepted |
| A9 — the suite passes with no network | `make ci` | Moss, 2026-09-21 | **Met.** 244 tests, no network, 0.17 s | Accepted |
| Independent assessment of this unit | A named assessor who did not write it | Not yet granted | **Not established.** Moss is the author of both the package and this reconciliation, so this is a self-check, not an independent assessment | Carried as a request in the return |

**What this record does not establish.** That the tool is correct on any site other than the
fixture. The fixture was written by the same increment as the code, so it encodes the same reading
of the specification; the independent derivations test the code against the fixture, not the
fixture against reality. U4 is the unit that tests that, and it is blocked on Q2. Until it runs,
"the tool implements the specification" rests on one fixture and one reading of the principal's
message.

## Changes

Revision 1, 2026-09-21T14:05:00-06:00. Created at U1's return. Source:
[RECORD.md](../../RECORD.md) revision 3 (the grant and the registered route) and revision 2
(criteria A1–A9). Reason: the principal ratified alternative A, which requires the existing
package to be re-derived and cut back; Q4 placed that decision in a sub-record because a stranger
will later need the reason the code was kept. Affects: `sitewalk/` (six deletions, five
amendments), `tests/` (the threshold pin, the CLI failures resolved, three CLI offline tests
added), `scripts/check-project.sh`, `AGENTS.md`. No code was deleted that a criterion traces to.
