---
name: clean-code
description: Guides writing and reviewing clean, maintainable code and designs. Use when writing new code, refactoring, reviewing a change, or weighing design trade-offs.
---

# Clean Code

Code is read far more often than it is written. Optimize for the next person who has to understand and change it, and that person is often you in six months. These guidelines are defaults, not laws. Apply them with judgment and follow the conventions of the codebase you are working in.

## Naming

- Choose names that reveal intent. A reader should know what a variable holds or what a function does without reading its body.
- Use nouns for types and values, verbs for functions. Booleans read well as questions: `isReady`, `hasAccess`.
- Avoid vague words such as `data`, `info`, `manager`, `handler`, or `util` unless the context truly makes them specific.
- Be consistent. Use one word per concept across the codebase: do not mix `fetch`, `get`, and `retrieve` for the same idea.
- Match name length to scope. A loop index can be `i`; a module-level constant deserves a descriptive name.
- If you struggle to name something, it may be doing too much. Treat naming difficulty as a design signal.

## Functions

- Keep functions small and focused on one thing. If you can describe a function only with "and", consider splitting it.
- Aim for a single level of abstraction per function. High-level orchestration should not be mixed with low-level detail.
- Prefer few parameters. Three or more related arguments often indicate a missing concept that deserves its own type.
- Avoid boolean flag parameters that switch behavior; write two functions instead.
- Prefer pure functions where practical: same input, same output, no hidden side effects. Isolate side effects at the edges.
- Separate commands (which change state) from queries (which return values) so callers can predict what a call does.

## Readable control flow

- Use guard clauses and early returns to handle edge cases first, keeping the main path unindented.
- Limit nesting. More than two or three levels deep is a cue to extract a function or invert a condition.
- Prefer positive conditions and extract complex boolean expressions into well-named variables or functions.
- Replace magic numbers and strings with named constants.
- Prefer clear loops or standard collection operations over clever one-liners. Cleverness is a cost paid by every later reader.

## Core principles

**KISS.** Choose the simplest solution that solves the actual problem. Complexity must earn its place.

**YAGNI.** Do not build for requirements you imagine might arrive. Speculative generality adds code to maintain and often guesses wrong. Make the current need work, and keep the design easy to extend when real needs appear.

**DRY.** Every piece of knowledge should have a single authoritative home. Duplication of business rules is dangerous because copies drift apart. But duplication of incidental similarity is cheaper than the wrong abstraction. Wait until you see the same idea three times, and confirm the copies change for the same reasons, before extracting.

**Separation of concerns.** Divide a program so that each part addresses one concern: parsing, business rules, persistence, presentation. Changes to one concern should rarely ripple into the others.

**Composition over inheritance.** Prefer assembling behavior from small parts to deep class hierarchies, which are rigid and hard to reason about.

## SOLID

- **Single responsibility.** A module should have one reason to change. Group things that change together and separate things that change for different reasons.
- **Open/closed.** Design so new behavior can be added by extension rather than by editing tested code, but only along axes of change you have actually observed.
- **Liskov substitution.** Subtypes must honor the contract of their base type. If callers need to check which subtype they hold, the hierarchy is wrong.
- **Interface segregation.** Prefer small, focused interfaces. Clients should not depend on methods they do not use.
- **Dependency inversion.** High-level policy should depend on abstractions, not on concrete low-level details. Pass dependencies in rather than constructing them internally.

Treat SOLID as a set of heuristics for managing change, not a checklist to satisfy. Applying every principle everywhere produces needless indirection.

## Error handling

- Fail fast and loudly. Validate inputs at the boundary and reject bad data early, rather than letting it corrupt state deeper in the system.
- Never swallow errors silently. Either handle an error meaningfully or let it propagate.
- Use the error mechanism idiomatic to your language consistently, whether exceptions, result types, or error values.
- Make error messages actionable: say what went wrong, with what input, and ideally what to do next.
- Distinguish expected failures (invalid input, missing file) from programming errors (broken invariants), and handle them differently.
- Clean up resources reliably, using the language's construct for scoped cleanup.
- Avoid returning null or sentinel values where a clearer type, such as an optional or an empty collection, communicates absence.

## Design trade-offs

Every design choice trades something for something else: simplicity against flexibility, performance against clarity, consistency against local convenience. Make the trade-off explicit.

- Prefer reversible decisions. Spend design effort in proportion to how costly a choice is to change later.
- Do not optimize prematurely. Measure first, then optimize the bottleneck, and note the reason when you give up clarity for speed.
- Duplication is sometimes better than coupling. A little copying can keep two modules independent.
- Refactor continuously in small steps while tests are green, rather than saving up large rewrites. Leave code a little better than you found it.
- Avoid abstractions that are used once. Introduce one when a second real use appears.

## Code review checklist

When reviewing, read the description and tests first, then the implementation. Ask:

1. **Correctness.** Does it do what was intended? Are edge cases, error paths, and concurrency concerns handled?
2. **Clarity.** Can I understand it without the author explaining? Are names precise and the flow easy to follow?
3. **Size.** Is the change focused? Large mixed changes hide bugs; suggest splitting them.
4. **Design.** Does it fit the existing structure? Are responsibilities in the right place? Is anything over-engineered or duplicated?
5. **Tests.** Are new behaviors and failure modes covered? Would the tests fail if the code were wrong?
6. **Safety.** Are inputs validated and secrets and permissions treated carefully?
7. **Performance.** Are there obvious costs, such as queries in loops or unbounded growth?
8. **Leftovers.** Any debug code, dead code, stale comments, or unrelated edits?

Give feedback on the code, not the person. Distinguish blocking problems from optional suggestions, explain the reasoning, and prefer questions when you are unsure. As an author, keep changes small, explain your intent, and treat review comments as help rather than criticism.


## Putting it together

When writing, get it working, make it clear, then make it simple, and only then consider making it fast. When reviewing, look for the smallest change that would most improve clarity or safety. In both cases, remember the goal: software that is easy to understand, easy to change, and hard to break.
