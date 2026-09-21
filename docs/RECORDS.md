# Records

The conventions for decision records in this project. They exist so the corpus stays readable
when it is merged with others and published, and so an agent can file a correct record without
asking.

The rules are enforced where they can be: `make records` runs the Perspicuity checker, and
`make ci` runs it too.

**The installed skill is the authority.** These notes summarise it; when they disagree with
`SKILL.md`, the skill wins and this file is the thing to fix. Read
`/home/david/.dsh/skills/perspicuity/SKILL.md` and its `references/record.md`.

## The project code

Every project has a **short code**: two to six lowercase letters, chosen when the project is set
up, and written into `CONTEXT.md`. It prefixes every record id so that ids stay unique when the
corpora are merged.

Codes in use: `ae` agent eligibility, `fmnb` Find My Next Bite, `ps` project setup, `sw`
sitewalk, `at` agenttrace, `sp` siteplan.

## Where records live

| Record | Path | Owns |
| --- | --- | --- |
| The project record | [`RECORD.md`](../RECORD.md) | The continuing account: current position, the inherited basis, the plan, the unit table, the review |
| Sub-decisions | `docs/records/YYYY-MM-DD-<slug>.md` | One consequential choice, its alternatives, its comparison and its review |

The project record is the **parent of every record in this repository**. A sub-decision never
replaces it; it hangs off it.

## Naming

**File name:** `docs/records/YYYY-MM-DD-<slug>.md`

- `YYYY-MM-DD` is the date the choice was made, not the date the file was tidied.
- `<slug>` is 2–5 lowercase words joined by hyphens, naming **the decision**, not the activity.

**Record id:** the project code, a hyphen, then the file name without its extension.

```
docs/records/2026-09-19-crawler-policy-stance.md   ->   id: sw-2026-09-19-crawler-policy-stance
```

The **project record** is the one exception: its id is chosen at setup — conventionally
`sw-project` — and never changed.

**Ids are stable.** Never rename one to match a later convention; supersede it with a new
revision.

**Title:** a short intention phrase, sentence case — the decision, phrased as something done or
chosen. Not a topic.

| Good | Bad | Why |
| --- | --- | --- |
| `Set the crawler policy stance` | `Crawler policy` | A topic is not a decision |
| `Choose the report URL shape` | `URLs` | Names what was chosen |
| `Refuse to audit domains we cannot verify` | `Safety notes` | States the position taken |
| `2026-09-19-validation-fixes.md` | `notes.md`, `updates.md`, `misc.md` | An activity log is not a record |

**Subject prefixes.** Start the slug with one of these when one fits. A convenience for
browsing, not a gate — if none fits, use a descriptive slug anyway.

| Prefix | Covers |
| --- | --- |
| `rubric-` | Anything that changes a published claim, a check, or a claim boundary |
| `market-` | Payer, pricing, outreach, positioning |
| `tech-` | Architecture, dependencies, storage, deployment |
| `process-` | How we work: records, review, gates, delegation |
| `data-` | Privacy, retention, what we store or fetch |

## Actors

**Name every actor. Never write "the agent", "the AI", `Primary`, or a model name.**

`Primary` is a Perspicuity role word for the coordinating agent. It reads as jargon to anyone
outside the session that coined it, and the corpus is written for strangers. A model name is
worse: it changes under the work, so a record that names the model cannot say who was
accountable across a year. A chosen name is stable across model changes.

- The **coordinator names itself** in its first session, before filing anything, and records the
  name in [ACTORS.md](ACTORS.md). It persists across every session it works in.
- The coordinator **names its workers** when it makes the assignment; the name travels with the
  grant and appears in the return.
- Write `Wren (coordinator)` on first mention, then `Wren`. The role says what the actor did in
  this record; the name says who they are.
- An **assessor is never the author**, and separate names make that checkable.
- **The principal is a person, not an agent.** No agent takes their name, or a living person's.

The roster, the rules for choosing a name and how to retire a legacy label are in
[ACTORS.md](ACTORS.md).

## Declare the working mode

State the mode in `Current position`: **`Run`** or **`Plan`**.

- **`Plan`** establishes frames, objectives, alternatives and selections, registers the work they
  authorise, and **stops at ratified decisions and registered grants**. A planning request stops
  at that boundary even when the authority to act already exists.
- **`Run`** carries a settled choice through its granted units and stops at the return.

Declare the mode before the first choice. Change it only when the work's purpose changes, and
keep the earlier mode with its reason. Neither mode supplies authority by itself.

A planning run is not a licence to build, and an execution run is not a licence to choose.

## When a record is required

Required when the choice:

1. changes a published claim, a check, or a claim boundary;
2. adds, removes or upgrades a dependency;
3. changes what we **fetch, store or publish** — safety and privacy both live here;
4. sets a precedent that later work will follow;
5. changes authority, ownership, or creates a review obligation;
6. selects among credible alternatives whose reason would otherwise be lost.

Not required, and better kept in the project record's action account: typo fixes, refactors with
no behavioural change, formatting, and new tests that apply an existing rule.

The test is not "was this hard?" It is "would a stranger, later, need to know why?"

## The skeleton

The compact template ships with the skill at `assets/record-template.md` and is reproduced in
[`RECORD.md`](../RECORD.md) in this repository. Copy that one.

## Rules the checker enforces

`make records` fails on any of these:

- A `## Current position` heading must exist, and `Work scope:`, `Next:` and (when work waits)
  `Dependency:` must appear inside it.
- `record_status` must be `open` or `closed`; `work_status` must be one of `not_started`,
  `active`, `waiting`, `submitted`, `in_review`, `accepted`, `stopped`.
- `revision` must be a positive integer, and `id` must carry no spaces.
- A closed record must not carry a `next_check` date, and must have `accepted` or `stopped` work
  plus a closure explanation.
- Ids must be unique across the corpus.

A clean result establishes none of this: it does not check whether the reasoning is any good,
whether the authority was real, or whether the work was done. It is a spell-checker, not a
reviewer.

## The grant, and the pickup plan

**Only a granted unit may be executed, and only within its stated scope.** A ratified decision
without a grant permits none of the work it selects.

At pickup, register the unit's **pickup plan** before implementing it: how it will be carried
out and what will show it is done. Register the first unit's plan at planning time; each later
unit's at its own pickup, because the later plans depend on what the earlier units find.

Adapting the route inside a grant is the actor's call. **Escalating** is different: when the work
changes the problem, the comparison or the selection, the unit returns to the decider. The
boundary is keyed to what changed, not to the actor's confidence — keyed to confidence,
everything escalates.

An adjoining improvement is a proposal, not part of the return.

## Registration order

Save the basis **before** the work that depends on it, and the choice **before** dependent
action. A record written afterwards records what you decided, not what you knew, and the
difference is the whole value of the corpus.

Where the documentation time differs from the decision time, say so rather than letting the
header imply otherwise. A reader must be able to tell which they are holding.

When a later finding changes an earlier basis, do not edit the earlier revision into agreement.
Add a revision, name what changed and why, and preserve the earlier one.

## Publication hygiene

Assume every record may be published. Never put in a record:

- credentials, tokens, API keys, or a `.env` value;
- a customer's, supplier's or correspondent's personal information;
- private commercial terms, or anything under an agreement that forbids disclosure;
- a real person's private contact details.

A record may name a public domain, a public source and a public price. It may name an internal
path. When in doubt, describe the fact and leave the identifier out.

## Review obligations

A record that promises later observation carries the question, the evidence source, the owner
and a date or a trigger. `next_check` in the header is the earliest such date.

Use `in_review` when the delivery is complete and an accepted check, decision or observation
remains. An `in_review` record needs a machine-readable `review_due` date as well as
`next_check`. Otherwise it is blocked waiting on them.

Delivery acceptance is not benefit. "The check shipped" and "a supplier paid" are different
findings, and the corpus is only honest if they stay separate.

## Close the commitment

Leave nothing stopped in an unnamed state. At every stop, account for each result in the work
scope and its pickup plans: **delivered**, **stopped** with a reason, or **blocked** with its
resolving step.

Close the record once every result is delivered, stopped or transferred to an identified owner.
This applies whether you continue or stop, so committed work does not accumulate as an open
queue.

## Delegated work

A worker receives the parent basis, the objectives, the exact grant and the return destination,
and **a name** for the assignment. The return carries its own decision basis, or an explicit
statement that it made no new choice, plus its output revision, its checks, its failures and
anything unresolved.

The return is attributed to the worker's name, not to a model. The assessor is named, and is
never the author. Worker completion is not acceptance.
