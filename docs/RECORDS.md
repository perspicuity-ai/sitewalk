# Records

The conventions for decision records in this project. They exist so the corpus stays readable
when it is merged with others and published, and so an agent can file a correct record without
asking.

The rules are enforced where they can be: `make records` runs the Perspicuity checker, and
`make ci` runs it too.

## The project code

Every project has a **short code**: two to six lowercase letters, chosen when the project is set
up, and written into `CONTEXT.md`. It prefixes every record id so that ids stay unique when the
corpora are merged.

Codes in use: `ae` for the agent eligibility check, `fmnb` for Find My Next Bite, `ps`
for this template.

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
docs/records/2026-09-19-crawler-policy-stance.md   ->   id: ae-2026-09-19-crawler-policy-stance
```

That rule is mechanical on purpose: the id and the file can never disagree, and a script could
check it.

The **project record** is the one exception. Its id is chosen at setup — conventionally
`sw-project` — and never changed.

**Ids are stable.** Never rename an id to match a later convention; supersede it with a new
revision.

**Title:** a short intention phrase, sentence case — the decision, phrased as something done
or chosen. Not a topic.

| Good | Bad | Why |
| --- | --- | --- |
| `Set the crawler policy stance` | `Crawler policy` | A topic is not a decision |
| `Choose the report URL shape` | `URLs` | Names what was chosen |
| `Refuse to audit domains we cannot verify` | `Safety notes` | States the position taken |
| `2026-09-19-validation-fixes.md` | `notes.md`, `updates.md`, `misc.md` | An activity log is not a record |

**Subject prefixes.** Start the slug with one of these when one fits. It is a convenience for
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

## When a record is required

Required when the choice:

1. changes a published claim, a check, or a claim boundary;
2. adds, removes or upgrades a dependency;
3. changes what we **fetch, store or publish** — safety and privacy both live here;
4. sets a precedent that later work will follow;
5. changes authority, ownership, or creates a review obligation;
6. selects among credible alternatives whose reason would otherwise be lost.

Not required, and better kept in the project record's action account: typo fixes, refactors
with no behavioural change, formatting, and new tests that apply an existing rule.

The test is not "was this hard?" It is "would a stranger, later, need to know why?"

## The skeleton

Copy this. Omit sections that carry nothing — a short honest record beats a padded one.

```markdown
---
format: perspicuity-work/1
id: sw-YYYY-MM-DD-<slug>
revision: 1
skill_version: 0.4.0
updated: YYYY-MM-DD
created_at: "YYYY-MM-DDTHH:MM:SS-06:00"
updated_at: "YYYY-MM-DDTHH:MM:SS-06:00"
record_status: open
work_status: not_started
# next_check: YYYY-MM-DD   only when a timed obligation exists
---

# <Intention>

## Current position

Parent: [RECORD.md](../../RECORD.md), revision N.

Principal: <name>. Decider: <who>.
Work owner: <actor>.
Decision: <pending | recommended | selected | inherited | none> — <one sentence, with the basis revision>.
Work scope: <the delivery this record owns>.
Work: <what has actually been done, with exact revisions>.
Outcome: <observed result, or explicitly unknown>.
Next: <actor / action / trigger>.
Dependency: <the missing input and its owner, when work waits>.

## Frame and Decide

<The underlying problem, the adopted frame, and any reframe with its reason.>

| Fundamental objective | Source | Measure, direction and horizon |
| --- | --- | --- |

| Material condition | Type | Basis | Affects |
| --- | --- | --- | --- |

<Register this basis before evaluating alternatives.>

### Alternatives and consequences

<Credible complete courses of action, including the current course. A compact table.>

<The decisive tradeoff, the preference it rests on, and what would warrant reconsideration.>

### Selection

<`selected_at`, decider, basis revision, the choice and the reason. Or the pending question
and its owner.>

## Act

<The plan registered before implementation, with acceptance criteria. Actual evidence after.>

## Review

| Criterion | Evidence source | Owner, window or trigger | Finding | Response |
| --- | --- | --- | --- | --- |

<Delivery acceptance stays separate from evidence of later benefit.>

## Changes

<Revision, time, change, source, reason, affected work.>
```

## Rules that the checker enforces

`make records` fails on any of these, so fix them before committing:

- A `## Current position` heading must exist, and `Work scope:`, `Next:` and (when work
  waits) `Dependency:` must appear inside it.
- `record_status` must be `open` or `closed`; `work_status` must be one of `not_started`,
  `active`, `waiting`, `submitted`, `accepted`, `stopped`.
- `revision` must be a positive integer, and `id` must carry no spaces.
- A closed record must not carry a `next_check` date, and must have `accepted` or `stopped`
  work plus a closure explanation.
- Ids must be unique across the corpus.

A clean result establishes none of this: it does not check whether the reasoning is any good,
whether the authority was real, or whether the work was done. It is a spell-checker, not a
reviewer.

## Registration order

Save the basis **before** the work that depends on it, and the choice **before** dependent
action. This is not a formality: a record written afterwards records what you decided, not
what you knew, and the difference is the whole value of the corpus.

When a later finding changes an earlier basis, do not edit the earlier revision into
agreement. Add a revision, name what changed and why, and preserve the earlier one.

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
and a date or a trigger. `next_check` in the header is the earliest such date; the dashboard
reads it, and a record with no timed obligation simply omits it.

Delivery acceptance is not benefit. "The check shipped" and "a supplier paid" are different
findings, and the corpus is only honest if they stay separate.

## Delegated work

A worker receives the parent basis, the objectives, the exact grant and the return
destination, and a **name** for the assignment. The return carries its own decision basis, or an
explicit statement that it made no new choice, plus its output revision, its checks, its
failures and anything unresolved.

The return is attributed to the worker's name, not to a model. The assessor is named too, and is
never the author. Worker completion is not acceptance.
