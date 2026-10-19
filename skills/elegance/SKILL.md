---
name: elegance
description: Design systems and write code as few independent concepts, each forced by a requirement, and judge designs by that standard. Use for architecture, API and data-model design, design docs and plans, redesigns and structural refactors, and when comparing or rating designs or code. Not for bug fixes, single-function edits or style review.
---

# Elegance

A design is elegant when a few independent concepts satisfy every constraint. **The law: every concept names the constraint that forces it. Everything else is derived or deleted.**

Scale the method to the decision. For a small change, the constraints fit in one sentence and the code itself shows the reasoning. Constraint ids, forks and a ledger are for designs, plans and redesigns.

## Terms
- **Constraint:** something the design must satisfy, from the user's own statements or from reality (an external API, data volume, law, money, physics). Requirements the context plainly implies count too, such as "never charge twice" in a payment flow; mark those *inferred*.
- **Designer choice:** anything else you decide, including defaults and conclusions drawn from constraints. It stays provisional, and it doesn't become a constraint when a user accepts your proposal; only the user's own statements do that.
- **Concept:** a part with exactly one purpose: a type, service, state, rule, flag or config option.
- **Independent:** each concept can be explained by one scenario that names no other concept.

## Designing
1. **List the constraints,** with short ids (C1, C2, …) when the design needs them.
2. **Derive what they force.** If one option survives, it's forced: state it. If several survive, you have a fork:
   - give the options, what each forces, and your recommendation;
   - put the fork whose answer settles the most first;
   - if nobody can answer now, take your recommendation, label it a designer choice, and list the fork.
3. **Only constraints eliminate options.** Simplicity, familiarity and taste only rank what remains. A design made simpler by dropping or weakening a constraint is false elegance, the worst result here. If a constraint makes the design ugly, keep the constraint and say so.
4. **One problem per fork.** Decide each problem at its own fork. Before you delete or shrink a concept, list every problem it solves, including ones no listed constraint names. Then check each problem on its own: a concept can become unnecessary for one problem while still carrying another.
5. **Find the shared concept** that most constraints are cases of, and express variation as independent axes of it, not as new kinds. If exception clauses pile up in your first design, you're polishing a local optimum: sketch two or three candidates that differ in core representation and rank them by these tests. If no concept fits without exceptions, the domain is irregular: use a table and name the constraint that makes it so. Two cases are not a pattern.
6. **Reuse before inventing,** from the system and from the field. Express a new need with an existing concept, or look for a known structure (state machine, event log, lattice, relational model, fold) whose laws already cover your cases. A real fit deletes cases you'd otherwise write; check that its guarantees are the ones your constraints need. Name the invariant the design keeps; a change that breaks it is wrong.
7. **Keep the core ignorant of optional concepts.** Put them at the edge (caller, wrapper, config). No extension point with a single user, and no new service just for this.
8. **Make limits conditions:** "stop when an attempt makes no progress", not "retry 3 times". Where reality forces a bound but not its value, such as a timeout or a memory cap, keep one named value and state its reason.
9. **Subtract before adding.** Ask of every concept which constraint breaks without it; if none does, delete it. Compare counts (concepts, exception clauses such as "except", "only if" or "unless", special-case branches, facts stated in two places, unforced numbers) between alternatives, or before and after a change. Counts only go down, unless a named constraint forces a rise.
10. **Re-derive instead of patching.** An old design, or a rough working version built to find the shape, is a source of candidate constraints: collect its special cases, confirm them, derive the design without looking at it, then diff and keep what is forced. When one constraint changes, re-derive only the concepts it touches.

When there's a fork, a designer choice or a deletion to show, end with a short ledger: constraints, forced decisions, designer choices, deletions.

## In code
Code is the design at small scale, under the same law. Branches and duplicates are the two signs of a representation that doesn't fit: a special case it can't absorb, and a fact it makes you state twice. Change the representation so both disappear: a sentinel node, an empty collection instead of null, a table instead of a chain of ifs. Merge only what is the same fact; similar code that changes for different reasons is not duplication.

Low complexity is a sign of elegance when every constraint still holds and you count across the whole system: a case moved into a caller, config, regex or dependency still counts. Line counts and complexity scores are diagnostics; golfing lowers them without deleting a case.

## Reviewing and comparing
1. **Try to break it.** For each design and each constraint, name a concrete input or event that would break it, or show that none can. A design that fails a constraint loses to one that keeps it, however short it is.
2. **Check how options were removed.** For each option a proposal rejects, was it ruled out by a constraint, or only by a value such as simplicity?
3. **Check each concept** with step 9's question, and check every number against step 8.
4. **Weigh what's left:** fewer independent concepts, fewer exceptions, an invariant that holds, and a small blast radius (if one constraint changes, how many concepts change?). A longer design wins when its extra parts trace to constraints the shorter one drops or handles with exceptions.

State the deciding reason in one sentence.

## Check your own tendencies
| If you notice yourself… | Instead |
| --- | --- |
| filling a gap with a default | label it a designer choice |
| softening a constraint to simplify | restate it and show where it's met |
| adding a flag, option, interface or layer no constraint names | delete it, or reuse an existing one |
| picking a number like `max_retries = 3` | make it a condition or a reasoned bound |
| naming a pattern or theory | show which cases it deletes, or drop it |
