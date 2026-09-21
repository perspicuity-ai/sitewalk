# Actors

Who and what acts in this project's records, so a reader of the published corpus can tell who
did what.

## The convention

**Every actor in a record is named.** Never "the agent", never "the AI", never a model name,
never a job title standing in for a person.

The reason is that the corpus is meant to be read by strangers, and it is meant to outlive the
tools. A role word such as `Primary` is internal jargon that means nothing outside the session
that coined it. A model name such as `GPT-5` or `Claude` is worse: it changes under the work, so
a record that names the model cannot say who was actually accountable across a year.

A chosen name is stable. The model behind it can change; the name does not.

| Rule | |
| --- | --- |
| **One name per actor, per project** | The coordinator's name is chosen once and persists across every session it works in. |
| **The coordinator names itself** | In its first session, before it files anything. See the first task in [AGENTS.md](../AGENTS.md). |
| **The coordinator names its workers** | A worker's name is assigned with its grant and travels with the assignment and the return. |
| **Names are identities, roles are separate** | Write `Wren (coordinator)` on first mention, then `Wren`. The role says what they did in this record; the name says who they are. |
| **An assessor is never the author** | Independence is a Perspicuity requirement, and separate names make it checkable. A record that assesses its own author's work says so. |
| **The principal is a person** | A human participant, not an agent. No agent may take their name or a living person's name. |

**Choosing a good name.** Short, memorable, one or two syllables. A persona, not a job: not
`Coordinator`, `Manager`, `Assistant`, `Primary` or `Admin`. Not a model or vendor name. Not a
real person's name. Two or three candidates is enough — pick one and use it consistently.

## Roster

Fill this in at setup. Add a row per actor, and keep the retired rows rather than deleting them:
a reader of an older record needs to be able to look up a name that no longer acts.

| Name | Kind | Role | From | Notes |
| --- | --- | --- | --- | --- |
| David | Human | Principal and decider | 2026-09-21 | Owns the objectives and the selection. Retains spending, outbound messages, external agreements and the release word. |
| Moss | Agent | Coordinator | 2026-09-21 | Named itself in its first session, 2026-09-21, before filing anything. Coordinates `sitewalk` and owns its records. |

### Why Moss

Three candidates were considered: **Moss** (slow, persistent, covers ground), **Quill** (a
writerly persona), **Flint** (a hard, sharp edge). Moss was chosen because it is one syllable, it
is a persona rather than a job, it is neither a model nor a vendor nor a living person's name,
and it does not collide with the coordinators of the sibling projects.

The name is the project's, not the session's. It does not change when the model behind it does.

## Retiring a legacy label

Corpora that predate this convention may use `Primary` or a model name for the coordinating
agent. When the coordinator is named:

1. Add a row to the roster recording the old label as **not an actor**, with what it meant.
2. Normalise the references to the chosen name.
3. Record the normalisation as a change entry with its reason, in the record whose text changed.

The facts do not change, only the label for the actor. Do not silently rewrite an inherited
record: the rename belongs to the actor it renames, recorded where a reader can find it.
