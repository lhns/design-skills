---
name: design-by-collapse
description: Run a design with a stakeholder ("owner") who makes the decisions across several sessions, as a recorded collapse of the solution space. You keep the owner's words apart from your own inferences, map every open decision as a fork, let only constraints eliminate options, ask focused questions one at a time, and keep the design movable when constraints change. Use it when an owner decides a system's design over several sessions, when auditing such a design record, or when the user explicitly asks for constraint-driven design or for focused questions about what is still undefined. It builds on the elegance skill. For design inside one task or session, use the elegance skill alone.
---

# Design by collapse

Load the **elegance** skill first. It defines the goal and the tests (few independent concepts, each forced by a constraint) and the fork format: options, what each forces, and a recommendation. If it isn't available, say so and keep its law: every concept names the constraint that forces it, and everything else is derived or deleted.

This skill adds what a design needs when an owner decides over many sessions: a record that separates the owner's constraints from your choices, the whole solution space rather than a single design, and protocols for asking and for change. The current design is one suggested point in that space. Your choices stay provisional and hang on forks, so a new constraint moves them instead of breaking the design. **Collapsing** means fixing an open fork with an owner answer and propagating it like a constraint.

## When an owner is present
These rules override the elegance skill:
- **Only the owner collapses a fork.** You derive what is forced and you recommend; you don't close an open fork yourself. Work proceeds on each open fork's `default`. Only work that would need a different answer, or that is hard to reverse, waits.
- **Inferences are not constraints.** What elegance calls an "inferred" constraint is an **assumption** here. It goes in the fork's `assumes:` list and may rank options, but it eliminates nothing until the owner states it. Never write a conclusion into a constraint. For example, "users sign in with company accounts" must not become "so we need no password reset".

## Records
All records live in `design/`. `design/design.md` is always the deliverable: the current design, written from the chosen options and citing the K and F ids.

For a short engagement, `design.md` alone also holds the owner quotes, the forks and the open questions. Once forks stay open across sessions, add:

| File | Holds |
| --- | --- |
| `vision.md` | The owner's words, verbatim and dated, one row each: `\| V7 \| C \| "quote" (2026-03-02) \|`. Classes: C constraint, V value, X exclusion, O open, R accepted recommendation. |
| `kernel.yaml` | Constraints (K), exclusions (X) and values (W). Each cites its vision ids in `from`; a fact of reality, such as an API limit, a law or a measurement, cites a checkable `source` instead. Ids never change: a changed item gets a new id, and the old one gets `status: superseded` and `superseded_by`. An item that answers a fork carries `answers: F<n>`. |
| `forks.yaml` | One problem per fork, with every option listed. Eliminated options stay in, with `eliminated_by` (K or X ids only) and `why`. `preferred_by` (W ids) only ranks. `chosen` is your current suggestion, and `assumes` lists the assumptions it rests on. An open fork carries `question`, `default`, `decide_by` (the event before which not deciding would lock in an option) and `asked` (date and exact question text, once asked). |
| `concepts.yaml` | Every concept with its purpose and a verdict: forced (`traces` K ids), detail (`detail_of: F<n>/<option>`), outside (belongs in an adapter or another system), or accretion (traces to nothing, so delete it). `open: true` marks an enumeration that will grow. `rounds` holds the counts per round; a rise names the K id that forces it. |

A **round** is one owner turn. After every change, run `python <this skill's dir>/scripts/check.py design` and fix what it reports. If the script can't run, do its checks by hand: each fork's live options, each elimination's source, and each detail's attachment.

## Each session
1. **Start.** Read `design/` first. Append the owner's new message verbatim to the vision, and match it to the open fork whose `asked` it answers.
2. **End.** Before you finish, the records must be current, and the question you are about to ask must be in its fork's `asked`. The next session sees only the files.

## The loop
1. **Corpus.** Collect the owner's statements verbatim and classify them. Add nothing of your own.
2. **Kernel.** Items that quote the owner verbatim are live as soon as you write them. A paraphrase, or a class you assigned yourself, stays an assumption until a specific question settles it. Show the kernel to the owner for correction alongside your first real question. Don't spend a turn asking "is this right?".
3. **Inventory** (when a design already exists). List every concept and give it a verdict.
4. **Forks.** Every problem the design must solve becomes a fork, one problem per fork (see elegance). Split a fork when its options differ on two independent axes, or when its options combine freely with another fork's. Split an owner sentence joined by "and" into separate K items. Every number in the design is either a bound cited by a K item, or a fork. Check every new option and concept against every exclusion, by meaning, not by name.
5. **Probe.** Walk concrete scenarios through the design, including failures, concurrency, and events that arrive late or twice. Where behavior is subtle, write a small formal model or a test. Every behavior nobody has decided becomes a fork.
6. **Ask, then propagate,** following the sections below, and go back to step 4.
7. **Generating idea.** Once few forks remain open, propose one to three core concepts from which the kernel falls out. Score each with the elegance tests and show how each one settles the remaining forks. The owner picks.
8. **Rescue.** When an existing design has accreted, re-derive it in a clean room from the kernel and the chosen idea (see elegance), then rewrite `design.md`. Recount every round.

## Asking the owner
- **One question per round.** Ask about the fork whose answer changes the live options of the most other forks. Don't ask about forced forks, and don't ask the owner to confirm them; report them. Never repeat a question found in an `asked` field.
- **Make each question self-contained and plain.** Say what it decides, why it matters now, and each option with what it forces elsewhere; put your recommendation first. Define every term the owner hasn't used.
- **Back big forks with evidence:** one worked example per option, with real values, plus how established systems solve the same problem.
- **"Not sure yet" is an answer.** The fork stays open on its default. Don't ask again before its `decide_by` event, or until its options change.
- **Approval is not an answer.** The owner approving a document you wrote states nothing. An R item never eliminates. If an elimination would hinge on one, ask the specific question that settles it; that counts as a new question, not a repeat.
- **Conflicts go to the owner.** When owner items contradict each other, raise a conflict for the owner; never resolve it yourself.
- **Review before acting.** Before a large or hard-to-reverse change, get an independent review (an advisor or a fresh reviewer), then ask the owner.

## Propagating
When an answer or a new constraint arrives:
1. **Record it.** Quote it in the vision and add a K item with a new id, superseding any item it changes.
2. **Eliminate.** Add the K id to `eliminated_by` on every option it rules out, with a `why`.
3. **Move your own choices.** Where the eliminated option was your `chosen`, move the choice and re-attach its details (the check lists them as stranded).
4. **Treat owner choices as conflicts.** Where the eliminated option was one the owner picked (its fork is answered by a K item), it is a conflict: ask the owner.
5. **Recount.** Never patch the design locally to work around the change.

## Auditing a design
For each elimination, check whether it rests on an owner statement or a fact, or only on an inference or a value. Look for:
- bundled forks;
- excluded concepts returning under new names;
- numbers that nothing forces;
- choices a newer constraint has already ruled out;
- details that hang on no fork.

## Reporting
After each round, say exactly what changed: new K items, forks decided, choices moved, concepts deleted, counts. Keep limits the design really has apart from steps that are only planned. Don't present what the kernel forces as a cost; it is the point of the design.

## Several agents
One coordinator owns the records and collapses forks; other agents propose and check. A clean-room re-derivation gets the kernel and the concept list, never the old design.
