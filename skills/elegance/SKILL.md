---
name: elegance
description: Design systems and write code that is elegant, meaning few independent concepts that are each forced by a requirement, and judge designs by that standard. Use for architecture, system and API design, data models, design docs and implementation plans, redesigns and structural refactors, and whenever you compare or rate designs or code for simplicity or quality, even if the user never says "elegant". Not for bug fixes, single-function edits or style review, where no design choice is at stake.
---

# Elegance

A design is elegant when a few independent concepts satisfy every constraint. **The law: every concept names the constraint that forces it. Everything else is derived or deleted.**

Scale the method to the decision. For a small change, the constraints fit in one sentence and the code itself shows the reasoning. Constraint ids, forks and a ledger are for designs, plans and redesigns.

## Terms
- **Constraint:** something the design must satisfy. It comes from the user's own statements or from reality: an external API, data volume, law, money, physics. Requirements the context plainly implies count too, such as "never charge twice" in a payment flow; mark those *inferred*.
- **Designer choice:** anything else you decide, including defaults, preferences and conclusions you draw from constraints. A designer choice stays provisional. It can never remove an option, and it doesn't become a constraint when a user accepts your proposal; only the user's own statements do that.
- **Concept:** a part of the design with exactly one purpose, such as a type, service, state, rule, flag or config option.
- **Independent:** each concept can be explained by one scenario that names no other concept.

## Designing
1. **List the constraints,** with short ids (C1, C2, …) when the design is big enough to need them.
2. **Derive what they force.** Where only one option survives, state it as forced. Where several survive, you have a fork:
   - give the options, what each one forces, and your recommendation;
   - put the fork whose answer settles the most first;
   - if nobody can answer now, don't stop: take your recommendation, label it a designer choice, and list the fork.
3. **Only constraints eliminate options.** Simplicity, familiarity and taste only rank what remains. A design made simpler by dropping or weakening a constraint is false elegance, the worst result here. If a constraint makes the design ugly, keep the constraint and say so.
4. **One problem per fork.** Decide each problem at its own fork. Before you delete or shrink a concept, list every problem it solves, including ones no listed constraint names. Then check each problem on its own: a concept can become unnecessary for one problem while still carrying another.
5. **Find the shared concept.** Look for the one concept that most constraints are cases of, and express variation as independent axes of it rather than as new kinds. When exception clauses pile up in your first design, you are polishing a local optimum: sketch two or three candidates that differ in their core representation, not in details, and rank them by these tests. If no single concept fits without exception clauses, the domain is irregular: use a table, and name the constraint that makes it so. Two cases are not a pattern.
6. **Reuse before inventing,** from the system and from the field. Express a new need with an existing concept if you can. Before designing a new mechanism, look for a known structure (state machine, event log, lattice, relational model, a fold) whose laws already cover your cases. A real fit deletes cases you would otherwise write; check that its guarantees are the ones your constraints need. Name the invariant the design keeps; a change that breaks it is wrong.
7. **Keep the core ignorant of optional concepts.** Put optional behavior at the edge (caller, wrapper, config), so the core never depends on it. Don't add an extension point with a single user, and no new service just to do this.
8. **Make limits conditions:** "stop when an attempt makes no progress", not "retry 3 times". Where reality forces a bound but not its value, such as a timeout or a memory cap, keep one named value and state its reason.
9. **Subtract before adding.** Ask of every concept which constraint breaks without it; if none does, delete it. Compare the counts of concepts, exception clauses ("except", "only if", "unless"), special-case branches, facts stated in two places, and unforced numbers:
   - between alternatives, for a new design;
   - before and after, for a change.

   Counts only go down, unless a named constraint forces a rise.
10. **Re-derive instead of patching.** For a redesign:
    1. Collect the old design's special cases as candidate constraints, and confirm each one.
    2. Derive the design from the constraints without looking at the old one.
    3. Diff the two. Keep what is forced, and list the rest as candidates for deletion.

    When a single constraint changes, re-derive only the concepts it touches. When the clean shape isn't visible yet, a rough working version is a legitimate first step: the special cases it forced you to handle are clues to real constraints. Then re-derive from those, or subtract, and delete what nothing forces.

When there is a fork, a designer choice or a deletion to show, end with a short ledger: the constraints, the forced decisions, the designer choices, and the deletions.

## In code
Code is the design at small scale, under the same law: types, states, functions, parameters and branches are concepts. Branches and duplicates are the two signs of a representation that doesn't fit: a special case it can't absorb, and a fact it makes you state twice. Change the representation so both disappear: a sentinel node, an empty collection instead of null, a table instead of a chain of ifs. Merge only what is the same fact; similar code that changes for different reasons is not duplication.

Low complexity is a sign of elegance when every constraint still holds and you count across the whole system: a case moved into a caller, config, regex or dependency still counts. Line counts and complexity scores are diagnostics; golfing lowers them without deleting a case.

## Reviewing and comparing
1. **Try to break it.** For each design and each constraint, name a concrete input or event that would break it, or show that none can. A design that fails a constraint loses to one that keeps it, however short it is.
2. **Check how options were removed.** For each option a proposal rejects, was it ruled out by a constraint, or only by a value such as simplicity?
3. **Check each concept.** Which constraint breaks without it? Is it a new kind, or a reuse? Does it add an exception clause? Is every number a condition or a reasoned bound?
4. **Weigh what's left.** Prefer fewer independent concepts, fewer exceptions, an invariant that holds, and small blast radius: if one constraint changes, how many concepts change? Lines, table rows and complexity scores are not concepts. A longer design wins when its extra parts trace to constraints the shorter one drops or handles with exceptions.

State the deciding reason in one sentence.

## Check your own tendencies
| If you notice yourself… | Do this instead |
| --- | --- |
| filling a gap with a plausible default | label it a designer choice |
| making a hard constraint softer so the design gets simpler | restate the constraint and show where it is met |
| adding a flag, option, interface, layer or concept no constraint names | delete it, or reuse an existing one |
| picking a number such as `max_retries = 3` | turn it into a condition, or give a reasoned bound |
| naming a pattern or theory | show which cases it deletes, or drop it |
| asking a bare question | give the options, what each forces, and a recommendation |
