# Design 1 (Candidate A) is better

**Constraints**
- C1–C6: the six routing rules. The first one that applies wins.
- C7: subject matching ignores case.
- C8: the rules change a few times a year, only by the owning engineers, through code review and deploy.

## Does each design keep the rules?

I traced both designs against C1–C7 and could not find an input that breaks either one.

- **Refund amounts:** in B, a refund with `amount=None` or an amount of 500 or less falls through to the `billing` row.
- **Missing amounts:** B's `gt` guards against `None`.
- **Phone logins:** B's `security` row comes before `self-service`, so a phone login reaches `security`.
- **Fallback:** the empty `when` on `general` catches everything else, so `next()` cannot run out of rules.

Correctness does not decide this comparison. Concept count and failure modes do.

## What Candidate B adds, and whether any constraint forces it

B adds a YAML rule format, an operator table (`eq`, `ne`, `gt`, `contains_any`), an interpreter (`_matches`, `route`), and a file load when the module is imported. These parts are only worth having if someone other than the engineers edits the rules, or if rules change without a deploy. C8 rules out both cases. B is an extension point with no user beyond the code itself.

## Costs that come with B's extra layer

- **Facts stated twice.** C2 is split across two rows, so `refund` appears twice. C4 is split the same way, so `password, login` appears twice. Changing a keyword now means editing two rows, and missing one causes a silent misroute. A states each rule once, one block per constraint.
- **A new way to break at runtime.** `open("routing.yaml")` uses a path relative to the current working directory. If the service starts from another directory, it crashes on import. A typo in a field name or operator, such as `channle` or `contains`, also passes review and only fails as an `AttributeError` or `KeyError` when a ticket arrives. In A, the same typo is ordinary Python that linters and tests catch.
- **The flexibility isn't real.** Any rule change outside the four operators, such as word-boundary matching, OR across fields, or a new comparison, still requires editing Python. Engineers then have to change two languages instead of one.

## Candidate A

A is one function. The constraint order maps directly onto the order of the `if` statements. Each nested branch, the amount check and the channel check, sits under the rule that requires it. The only unforced detail is that `subject.lower()` runs before the enterprise check, which is harmless.

## Ledger

- **Forced:** the rules are evaluated in priority order, first match wins, with case-insensitive subject matching. Both designs do this.
- **Designer choice in B, not forced by any constraint:** a data-driven rule format plus an interpreter.
- **Deletions when choosing A:** the YAML format, the operator table, the interpreter, the file I/O, and the two duplicated keyword lists.

**Deciding reason:** both designs route correctly, but no constraint calls for B's rule engine, and it adds concepts, duplicated keywords and runtime failure modes on top of a function the owning engineers already change through code review.

WINNER: 1