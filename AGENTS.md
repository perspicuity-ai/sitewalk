# Agent instructions

## Read first, in this order

1. **[CONTEXT.md](CONTEXT.md)** — what this is, why it exists, what success and stopping look
   like. One page. Do not skip it.
2. **[RECORD.md](RECORD.md)** — the project's Perspicuity record: current position, mode, the
   inherited basis, the plan, the unit table, the review.
3. **[docs/ACTORS.md](docs/ACTORS.md)** — who acts in the records, the roster, and the rule that
   you are named rather than called "the agent".
4. **[docs/RECORDS.md](docs/RECORDS.md)** — how records are named, registered and filed, when one
   is required, and exactly what the checks cover.
5. **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** — the settled technical decisions and the
   alternatives that were rejected.

The installed Perspicuity skill is the authority for the method:
`/home/david/.dsh/skills/perspicuity/SKILL.md`, with `references/record.md` and
`references/analysis.md`. Where these documents disagree with the skill, the skill wins.

## Your first task

**Before any feature work: name yourself, declare your mode, and register the record.**

### 1. Name yourself

You are the coordinator of this project. Choose a name before you write anything into a record —
one or two syllables, a persona rather than a job. Not `Primary`, not `Coordinator` or
`Assistant`, not a model or vendor name, not a living person's name.

That name is how the published corpus will refer to you, and it persists across every session you
work in. The model behind it can change; the name does not. Record it in
[docs/ACTORS.md](docs/ACTORS.md) under the roster. You own the naming of your workers too: name
each one when you make its assignment.

### 2. Declare your mode

`Plan` or `Run`, in `Current position`, before the first choice.

- **`Plan`** establishes frames, objectives, alternatives and selections, registers the work they
  authorise, and **stops at ratified decisions and registered grants**.
- **`Run`** carries a settled choice through its granted units and stops at the return.

A planning request stops at that boundary **even when the authority to act already exists**. If
the principal asks for a plan or a statement of work, do not build; produce the plan and ask for
the grant. If they ask for work that a registered grant already covers, do not re-plan it.

### 3. Own the process documents, then register the record

Review and revise `AGENTS.md`, `CONTEXT.md` and `docs/RECORDS.md` so that a worker arriving with
no context could follow them without asking a question. You are the first person to read them
with fresh eyes and the only one who ever will.

The standing constraints in this file are the most likely to be wrong: they were written before
anyone knew what this project would need. Check each against `CONTEXT.md`, keep the ones that
hold, replace the ones that do not.

If `CONTEXT.md` still contains TODOs, that is a finding, not a blocker — say so and leave it for
the principal rather than inventing the product.

Then register `RECORD.md` with the frame, the objectives and their sources, the material
conditions, the alternatives, the comparison and the selection or recommended course. Register it
**before** the work that depends on it.

## What Perspicuity is

A method for doing work with AI agents so that the reasoning survives the conversation. Not a
reporting requirement bolted on at the end — it is how the work is done.

**One evolving record per intention**, amended by revision, never rewritten into agreement with
hindsight. Three stages which overlap and repeat:

| Stage | What happens |
| --- | --- |
| **Frame and Decide** | The problem, the outcomes that matter and who owns them, the material conditions, credible alternatives, their consequences. Then select — or record the question as pending with its owner. |
| **Act** | Turn the choice into assessable work: units, inputs, owners, timing, and acceptance criteria registered *before* implementation. |
| **Review** | Assess against the criteria registered earlier, keeping delivery acceptance separate from evidence of later benefit. |

**Four rules that do the real work:**

1. **Register before dependent work.** The basis before comparing alternatives; the choice before
   acting on it; the review criteria before the outcome is known.
2. **Separate the recommendation from the selection.** A worker prepares the basis and recommends.
   The decider selects. Do not record a choice you were not authorised to make.
3. **Keep givens, uncertainties and assumptions apart**, each with its source.
4. **Delivery is not benefit.** "It shipped" and "it worked" are different findings.

## The corpus rule

> Every consequential choice in this repository exists as a Perspicuity record **before** the work
> that depends on it. If a choice is not in a record, it has not been made.

The corpus is the point of this project, not a by-product. Written to be read by strangers, and
intended for publication. A record that restates its parent is noise. A record whose reason
cannot be reconstructed is a defect.

## Naming records

```
docs/records/2026-09-19-crawler-policy-stance.md   ->   id: sw-2026-09-19-crawler-policy-stance
```

- File: `YYYY-MM-DD-<slug>.md`, the date the choice was made, the slug naming **the decision**.
- Id: the project code, a hyphen, then the file name without its extension.
- Title: an intention phrase — `Set the crawler policy stance`, not `Crawler policy`.
- Ids are stable. Never rename one; supersede it with a new revision.

The project code is in `CONTEXT.md`. Full rules in [docs/RECORDS.md](docs/RECORDS.md).

## Standing constraints

The rules that must not be broken without a recorded choice, because they are true of *this*
product rather than of every product. Replaced 2026-09-21 during U1 (the template shipped a
placeholder here); each is checked against [`CONTEXT.md`](CONTEXT.md), and the record for the
change is [`RECORD.md`](RECORD.md) revision 3.

- **Standard library only for the runtime.** Python 3.11+, no dependency, no build step. A new
  dependency needs a recorded choice, and the reason it is a constraint is that this tool has to
  install into someone else's deploy gate.
- **`--dir` performs no network access at all.** It is the deploy gate, and it must work with the
  machine unplugged. A change that makes the offline path capable of a request is a defect, not a
  tradeoff.
- **Only the submitted origin is fetched.** Nothing else is crawled, checked or resolved. A tool
  that follows a link off-site is a tool that can be pointed at someone else's server.
- **Every fetched address passes the guard in `sitewalk/guard.py`**, which refuses non-http(s)
  schemes, ports other than the scheme default, and any address that is not globally routable —
  including the cloud metadata address — and re-checks the connected peer after connecting. The
  guard is the highest-risk code here; a change to it needs a recorded choice.
- **The claim boundary holds.** Never state or imply that the report predicts whether an agent
  will find, trust or recommend a site, and never report ranking, citations or traffic.
- **Nothing is executed.** No JavaScript engine, no browser, no shelling out. A page that looks
  script-rendered is *said* to look script-rendered, with the evidence, and never called empty.
- **The report is deterministic.** No model may decide or alter a finding, a severity or an exit
  code. The same bytes produce the same report.
- **A gate must be able to fail.** `scripts/check-project.sh` runs real checks and `--strict`
  exits non-zero on a **gating** finding — severity `error` or `conditional`, per the policy table
  in `facts.GATING_SEVERITIES`. A green check that establishes nothing is worse than no check,
  because it is believed.
- **No accounts, cookies, tracking, telemetry or paid API.** The client sends no cookie and keeps
  no credential.
- **No persistence and no PII.** Nothing is written to disk, and nothing about a person is
  collected: only published pages are read, and only structural facts are recorded.
- **Credentials and personal data never enter a record, a commit or the repository.**
- **Reports are written to stdout or a file and are not published by this project.** Publication
  is the principal's retained decision.

## Authority

The principal is the decider. They retain **spending, outbound messages, external agreements and
the release word for publication**. Everything else within the project record's scope is
delegated, including reversible implementation details.

Work outside that grant needs a new recorded choice, not a judgement call. If you cannot tell
whether something is inside it, it is outside it — ask, or record it as pending and continue with
the parts that are not blocked.

## Definition of done

- **`Current position` states position; it does not restate facts a table below already holds.**
  A count, a list of delivered units or a status word in that section goes stale the moment the
  work lands, and it is the first thing a reader and the dashboard see, so it is the most likely
  place for a claim that was true when written to be believed long after it stopped being true.
  Write *"their state is in Act's unit table"*, not *"nine units delivered"*. This is a rule about
  the shape of a summary rather than about its content: the summary stays current by carrying
  pointers, and the tables stay current because each entry is amended where the work happens.
  **A count that must be stated for the record — a measurement a decision rested on, or an instance
  in *Why this rule exists* — is dated and attributed to the revision it belongs to**, as in "238 of
  240 at registration". A dated count cannot go stale, because it never claimed to be current; an
  undated one is read as current the moment it is written. This is why the rule constrains the
  shape and not the content: history is made of counts that were true when written, and the fix is a
  date rather than an omission.
- **Every new test and fixture answers one question: *which wrong implementation would this
  catch?*** If the answer is none, the fixture is decoration and the test is counted as evidence
  while being none. A test that asserts only that a function returns what it returns is not a
  check; a fixture that cannot separate a right implementation from a plausible wrong one is not a
  fixture. This rule was earned, not assumed — see *Why this rule exists* below.
- `make ci` exits 0. It runs the record check and `scripts/check-project.sh`, which byte-compiles
  the package, runs the suite with the network unavailable, exercises `python3 -m sitewalk`
  through the real entry point, and checks that the report still states its claim boundary.
- **`scripts/check-project.sh` runs real checks and can fail.** It was a template stub until U1
  (2026-09-21); a stub that exits 0 lets `make ci` pass while tests fail, which is worse than no
  check because it is believed. If you change what a check covers, prove the script still fails
  on the defect it is meant to catch — piping a command's output into `tail` makes the pipeline's
  status `tail`'s, which is always 0, and that mistake was made here once.
- `make records` is clean. A run reporting the checker missing is a **skip, not a pass**.
- The change is in a record if it meets the admission test, and the record names its evidence.
- Every actor in the change is named. No job title, no retired label, no model name.
- The record's `## Review` says what was **not** established. An honest "unobserved" beats an
  implied claim.

## Why this rule exists

Added 2026-09-21, and the count has grown since. The same class has been found **seven** times in
this project: twice in code, once in a fixture, once in a process document, twice in a record, and
once in a summary that outlived what it described. Each looked correct when it was written, and each
was found by asking the question above of work that seemed finished.

| Instance | How it could not fail |
| --- | --- |
| The script-shell thresholds | The boundary test imported the constant it was testing, so moving the threshold from 200 to 5000 kept all 243 tests green |
| `scripts/check-project.sh` | Its test step piped the suite into `tail`, so `set -e` saw `tail`'s exit status and `make ci` printed "ci passed" with two failing tests — the exact bug the stub had been replaced to prevent |
| The raw-versus-processed quote (U6, caught before writing the test) | The fixture's `Disallow:` line had no comment and no padding, so quoting the parser's processed variable instead of the source line would have passed |
| The conformance fixture (U7, caught before writing the test) | Asserting all 45 `siteplan` conformance cases as accept-cases would have failed 38 times while being wrong: those cases test the *producer's* faults, and a consumer is permitted to tolerate them |
| A record correction (U7) | Fixing one contradiction between a criterion and a severity table introduced three more — a stale rule sentence, a wrong criterion count, and a missing acceptance-criteria line. A correction is where the author is most confident and least likely to look |
| A plan sub-check (U9) | `report.plan` said `required_surfaces_met: true` beside `passed: false`, because a check that never ran reported as though it had. Found by Finch, not by the suite |
| The outage account (2026-09-22) | A cause and an observed time were joined into one claim without checking they coincided: a service restart at 05:18:16Z was blamed for an outage, while the consumer's measured runs show the site serving 50 pages at 05:28:42Z. The cause was real and the correlation was not. The fix is to say which parts are measured and which are inferred, rather than the conclusion the two suggest together |
| `Current position` (2026-09-22) | It still said four units delivered when nine were, named a freeze that had been lifted, reported 277 tests when the suite ran 331, and claimed U6 was ungranted. Everything below it was current and evidenced; the summary above described a state that ended before the work it summarised. Found by the principal, not by a test — see the rule in the definition of done, which is the fix |

**Two practices that follow from it.**

1. **Prefer asserting on what a machine reads, not on a message string.** A test that asserts a
   phrase appears will keep passing when the phrase's meaning changes; a test that asserts a state,
   a count or a severity will not.
2. **When you correct something, check for the pattern rather than trusting the edit.** The fifth
   instance above was found by grepping for the superseded wording after the fix, not by reading
   the fix and agreeing with it.
