---
name: design-by-collapse
description: Run a design whose owner (a stakeholder) decides across several sessions, as a recorded collapse of the solution space; also audit such design records. Use when an owner shapes a system over several sessions, or when the user asks for constraint-driven design or focused questions about what's undefined. Builds on the elegance skill; for design within one session, use elegance alone.
---

# Design by collapse

Load the **elegance** skill first: it defines the goal, the tests and the fork format. If it's unavailable, say so and keep its rule: every part of the design can say why it's there (a constraint requires it, or it's a labeled designer choice at an open fork); anything else is an accretion.

This skill keeps the whole solution space on record. The current design is one suggested point in it, and your choices hang on forks, so a new constraint moves them instead of breaking the design. **Collapsing** means fixing an open fork with an owner answer and propagating it like a constraint.

## When an owner is present
These rules override the elegance skill:
- **Only the owner collapses a fork.** You derive what is forced and you recommend; you don't close an open fork yourself. Work proceeds on each open fork's `default`. Only work that would need a different answer, or that is hard to reverse, waits.
- **Inferences are not constraints.** What elegance calls an "inferred" constraint is an **assumption** here. It goes in the fork's `assumes:` list and may rank options, but it eliminates nothing until the owner states it. Never write a conclusion into a constraint. For example, "users sign in with company accounts" must not become "so we need no password reset".

## Records
Put the records where the repo keeps design docs; the default is `docs/design/`. For the file shapes, copy `scripts/tests/clean/` in this skill's dir. `design.md` is the deliverable: the current design, written from the chosen options and citing K and F ids. For a short engagement it also holds the owner quotes, forks and open questions. Once forks stay open across sessions, add:

| File | Holds |
| --- | --- |
| `vision.md` | The owner's words, verbatim and dated: `\| V7 \| C \| "quote" (2026-03-02) \|`. Classes: C constraint, V value, X exclusion, O open, R accepted recommendation. |
| `kernel.yaml` | Constraints (K), exclusions (X), values (W), each citing vision ids in `from`, or a checkable `source` for facts of reality (an API limit, a law, a measurement). Ids never change; a change supersedes (`status: superseded`, `superseded_by`). An item answering a fork carries `answers: F<n>`. |
| `forks.yaml` | One problem per fork, every option listed. Eliminated options stay, with `eliminated_by` (K or X only) and `why`; `preferred_by` (W) only ranks. `chosen` is your suggestion; `assumes` lists what it rests on. Open forks carry `question`, `default`, `decide_by` (the event before which not deciding locks in an option) and `asked` (date and exact text). |
| `concepts.yaml` | Each concept's purpose and verdict: forced (`traces` K ids), detail (`detail_of: F<n>/<option>`), outside (belongs elsewhere), accretion (traces to nothing; a deletion candidate for the owner). `open: true` marks an enumeration that will grow. `rounds` holds counts per round; a rise names its K id. |

**ADRs** (`docs/adr/NNNN-title.md`, or the repo's convention): where the repo has them, every hard-to-reverse fork gets one, linked from the fork in `adr:`. Where it has none, propose starting them when the first hard-to-reverse fork collapses, and write them once the owner agrees. Context cites the fork and its K ids, Decision is the chosen option, Consequences is what it forces. Status follows the fork: Proposed, naming the default being built on, while it's open; Accepted once it's forced or the owner collapses it. Like kernel ids, an accepted ADR never changes: when a fork moves, write a new ADR and mark the old one Superseded, pointing to it.

A **round** is one owner turn. After every change, run `python <this skill's dir>/scripts/check.py <records dir>` and fix what it reports. If it can't run, check by hand: each fork's live options, each elimination's source, each detail's attachment.

## Each session
1. **Start.** Read the records first. Append the owner's new message verbatim to the vision, and match it to the open fork whose `asked` it answers.
2. **End.** Before you finish, the records must be current, and the question you are about to ask must be in its fork's `asked`. The next session sees only the files.

## The loop
1. **Corpus.** Collect the owner's statements verbatim and classify them. Add nothing of your own.
2. **Kernel.** Items quoting the owner verbatim are live at once. A paraphrase, or a class you assigned, stays an assumption until a specific question settles it. Show the kernel for correction alongside your first real question.
3. **Inventory** (when a design exists): every concept with a verdict.
4. **Forks.** Every problem the design must solve becomes a fork, one problem per fork (see elegance). Split a fork when its options differ on two independent axes, when its options combine freely with another fork's, or when a single option settles more than one problem. Split an owner sentence joined by "and" into separate K items. Every number in the design is either a bound cited by a K item, or a fork. Check every new option and concept against every exclusion, by meaning, not by name.
5. **Probe.** Walk concrete scenarios through the design (failures, concurrency, late or repeated events); where behavior is subtle, write a small formal model or test. Every undecided behavior becomes a fork.
6. **Ask, then propagate** (below), and return to step 4.
7. **Generating idea.** When few forks remain, propose one to three core concepts from which the kernel falls out, scored with the elegance tests, showing how each settles the remaining forks. The owner picks.
8. **Rescue.** For an accreted design, re-derive in a clean room from the kernel and the chosen idea (see elegance), then rewrite `design.md`. Recount every round.

## Asking the owner
- **One question per round,** about the fork whose answer changes the live options of the most other forks. Report forced forks; don't ask about them or ask to confirm them. Never repeat a question found in an `asked` field.
- **Plain and self-contained:** say what it decides and why it matters now, in the fork format, recommendation first; define every term the owner hasn't used. For big forks, give one worked example per option with real values, and how established systems solve it.
- **"Not sure yet" is an answer.** The fork stays open on its default. Don't ask again before its `decide_by` event, or until its options change.
- **Approval is not an answer.** The owner approving a document you wrote states nothing. An R item never eliminates. If an elimination would hinge on one, ask the specific question that settles it; that counts as a new question, not a repeat.
- **Conflicts go to the owner.** When owner items contradict each other, raise a conflict for the owner; never resolve it yourself.
- **Review before acting.** Before a large or hard-to-reverse change, get an independent review (an advisor or a fresh reviewer), then ask the owner.

## Propagating
When an answer or a new constraint arrives:
1. **Record it.** Quote it in the vision and add a K item with a new id, superseding any item it changes.
2. **Eliminate.** Add the K id to `eliminated_by` on every option it rules out, with a `why`.
3. **Move your own choices.** Where the eliminated option was your `chosen`, move the choice, re-attach its details (the check lists them as stranded), and write the superseding ADR if the fork has one.
4. **Treat owner choices as conflicts.** Where the eliminated option was one the owner picked (its fork is answered by a K item), it is a conflict: ask the owner.
5. **Recount.** Never patch the design locally to work around the change.

## Auditing a design
For each elimination, ask whether it rests on an owner statement or a fact, or only on an inference or a value; then apply step 4's tests and the check's rules (stale choices, details hanging on no fork).

## Reporting
After each round, say exactly what changed: new K items, forks decided, choices moved, concepts deleted, counts. Keep real limits apart from planned steps, and don't present what the kernel forces as a cost; it is the point of the design.

## Several agents
One coordinator owns the records and collapses forks; others propose and check. A clean-room re-derivation gets the kernel and the concept list, never the old design.
