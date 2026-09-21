# Agent instructions

## Read first, in this order

1. **[CONTEXT.md](CONTEXT.md)** — what this is, why it exists, what success and stopping look
   like. One page. Do not skip it.
2. **[RECORD.md](RECORD.md)** — the project's Perspicuity record: current position, the
   inherited basis, the plan, the unit table, the review.
3. **[docs/RECORDS.md](docs/RECORDS.md)** — how decision records are named, when one is
   required, and what the checker enforces.
4. **[docs/ACTORS.md](docs/ACTORS.md)** — who acts in the records, and the rule that you are
   named rather than called "the agent".
5. **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** — the settled technical decisions and the
   alternatives that were rejected.

## Your first task

**Before any feature work: name yourself, own the process documents, and file the first record.**

### 1. Name yourself

You are the coordinator of this project. Choose a name for yourself before you write anything
into a record — one or two syllables, a persona rather than a job. Not `Primary`, not
`Coordinator` or `Assistant`, not a model or vendor name, not a living person's name.

That name is how the published corpus will refer to you, and it persists across every session
you work in. The model behind it can change; the name does not. Two or three candidates is
enough. Record it in [docs/ACTORS.md](docs/ACTORS.md) under the roster.

You own the naming of the workers you delegate to as well. Name each one when you make its
assignment, and put the name in the grant and in the return.

### 2. Own the process documents

Read the files above, then review and revise `AGENTS.md`, `CONTEXT.md` and `docs/RECORDS.md` so
that a worker arriving with no context could follow the process without asking a question.

This is a real deliverable, not a warm-up. You are the first person to read these documents
with fresh eyes, and you are the only one who will ever read them in this state. Expect to find:

- rules that are stated but not enforced anywhere, and could be;
- a convention that reads clearly to its author and ambiguously to you;
- something important about how work should be done here that is missing entirely.

The standing constraints in this file are the ones most likely to be wrong: they were written
before anyone knew what this project would need. Check them against `CONTEXT.md` and change
them if they do not hold.

### 3. File the record

File the result as the first sub-record in the corpus —
`docs/records/YYYY-MM-DD-process-record-conventions.md`, following
[docs/RECORDS.md](docs/RECORDS.md) exactly, including the naming rule, the id rule (the project
code, a hyphen, then the file name without its extension), the parent link to `RECORD.md`, and
the `## Current position` block with Work scope and Next.

That record is both the review and the worked example: the first thing in the corpus
demonstrates the convention it establishes. It is a real record, not a formality — carry the
alternatives you considered, the reason you chose what you chose, and what you left open.

Then report back with the record's path, what you changed and why, and anything you could not
settle. Leave feature work until that is accepted.

## What Perspicuity is

This project is built under **Perspicuity**, a method for doing work with AI agents so that the
reasoning survives the conversation. It is not a reporting requirement bolted on at the end.
It is how the work is done.

**One evolving record per intention.** Not a document per meeting or per task. A record starts
when a question does and keeps accumulating: what was asked, what was decided, what was done,
what happened. It is amended by revision, never rewritten into agreement with hindsight.

**Three stages, which overlap and repeat:**

| Stage | What happens |
| --- | --- |
| **Frame and Decide** | Establish the actual problem, the outcomes that matter and who owns them, the material conditions, credible alternatives, and their consequences. Then select — or record the question as pending with its owner. |
| **Act** | Turn the choice into assessable work: units, inputs, owners, timing, and acceptance criteria registered *before* implementation. Record actual evidence after. |
| **Review** | Assess against the criteria registered earlier, keeping delivery acceptance separate from evidence of later benefit. A thing shipping is not a thing working. |

**Four rules that do the real work:**

1. **Register before dependent work.** Save the basis before comparing alternatives; save the
   choice before acting on it; save the review criteria before the outcome is known. A record
   written afterwards records what you decided, not what you knew.
2. **Separate the recommendation from the selection.** A worker prepares the basis and
   recommends. The decider selects. Do not record a choice you were not authorised to make.
3. **Keep givens, uncertainties and assumptions apart.** A given has a source and a date. An
   assumption is an unverified claim, and it says what would challenge it. Collapsing these is
   how a corpus becomes confidently wrong.
4. **Delivery is not benefit.** "The check shipped" and "a supplier paid" are different
   findings. Keep them distinct in every review.

**Scale the method to the stakes.** A reversible implementation detail gets a sentence in the
action account. A choice that changes a published claim, a dependency, what we fetch or store,
or a precedent later work follows, gets its own record. The admission test is in
[docs/RECORDS.md](docs/RECORDS.md#when-a-record-is-required).

The full skill is installed at `/home/david/.codex/skills/perspicuity/SKILL.md`. Read it once,
properly, before you file your first record.

## The corpus rule

> Every consequential choice in this repository exists as a Perspicuity record **before** the
> work that depends on it. If a choice is not in a record, it has not been made.

The corpus is the point of this project, not a by-product. It is written to be read by
strangers and it is intended for publication. A record that restates its parent is noise. A
record whose reason cannot be reconstructed is a defect.

## Naming records

The project record is [`RECORD.md`](RECORD.md). Sub-decisions go in `docs/records/`:

```
docs/records/2026-09-19-crawler-policy-stance.md   ->   id: sw-2026-09-19-crawler-policy-stance
```

- File: `YYYY-MM-DD-<slug>.md`, where the date is when the choice was made and the slug is 2–5
  lowercase hyphenated words naming **the decision**, not the activity.
- Id: the project code, a hyphen, then the file name without its extension. Mechanical, so the
  two cannot disagree.
- Title: a short intention phrase — `Set the crawler policy stance`, not `Crawler policy`.
- Subject prefix when one fits: `rubric-`, `market-`, `tech-`, `process-`, `data-`.
- Every sub-record names `RECORD.md` as its parent, and the parent's decision index lists it.
- Ids are stable. Never rename one; supersede it with a new revision.

The project code is in `CONTEXT.md`. Full rules, the skeleton to copy, and the
publication-hygiene list are in [docs/RECORDS.md](docs/RECORDS.md). `make records` checks the
mechanical parts.

## Standing constraints

<!-- Replace this section during Project Setup. It is the short list of rules that must not be
     broken without a recorded choice: the things that are true of this product, not of every
     product. Check them against CONTEXT.md before you rely on them.

     A real example, from the agent eligibility check:

     - Standard library only for the runtime. A new dependency needs a recorded choice.
     - The core report is deterministic. No model may decide or alter a pass/fail result.
     - The claim boundary holds: never state or imply that the report predicts whether an agent
       will find, trust or recommend a supplier.
     - Only the submitted domain is fetched. Nothing else is crawled.
     - Reports are private by default. Publication is the subject's action.
     - No accounts, cookies or tracking, and no paid API in the core.
     - Credentials and personal data never enter a record, a commit or the repository.
-->

- **Credentials and personal data never enter a record, a commit or the repository.**
- <fill in the rest during Project Setup>

## Authority

The principal is the decider. They retain **spending, outbound messages, external agreements and
the release word for publication**. Everything else within the project record's scope is
delegated, including reversible implementation details.

Work outside that grant needs a new recorded choice, not a judgement call. If you cannot tell
whether something is inside it, it is outside it — ask, or record it as pending and continue
with the parts that are not blocked.

## Definition of done

- `make ci` exits 0.
- `make records` is clean.
- The change is in a record if it meets the admission test, and the record names its evidence.
- You have said what you did **not** establish. An honest "unobserved" beats an implied claim.
