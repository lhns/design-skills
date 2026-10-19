# Design 2 (Candidate A) is the better design

**Constraints:**
- C1–C6 are the routing rules, in priority order.
- C7: subject matching ignores case.
- C8: the rules change a few times a year, only by the owning engineers, through code review and deploy.

**Both designs route correctly.** I tried to break each one against every rule:
- **Refund, amount 600:** Design 1 sends it to `billing-escalations` and Design 2 does too.
- **Refund, amount `None` or 400:** Design 1's `gt` guards against `None`, the ticket falls through to the merged `billing` rule, and lands in `billing`. Design 2 also sends it to `billing`.
- **"LOGIN" by phone:** both lowercase the subject and send it to `security`.
- **Enterprise ticket in German with a refund:** both send it to `enterprise-desk`, so priority holds in both.

I found no ticket that breaks either design. Correctness doesn't decide this, so the deciding test is: which constraint forces each concept?

**Design 1's extra concepts:**
- a YAML rule format
- an operator vocabulary (`eq`, `ne`, `gt`, `contains_any`)
- an interpreter (`_matches`)
- reflective field lookup (`getattr`)
- a file loaded at import time

**A rules file outside the code is only worth having if non-engineers edit rules, or rules change without a deploy. C8 rules out both.** Rules change rarely, and only through the same code review and deploy as the Python. So no constraint forces the DSL, and it is an extension point with a single user.

The DSL also adds new ways to fail that Design 2 doesn't have:
- `open("routing.yaml")` is relative to the current working directory, so the service breaks if it is started from another directory.
- A misspelled field or operator in the YAML (`customer_teir`, `contians_any`) raises `AttributeError` or `KeyError` only when a ticket reaches that rule. Review and type checking of the Python don't catch it.
- The rule list has no guaranteed final catch-all. If someone deletes the `when: {}` entry, `next()` raises `StopIteration` at runtime.
- Rule C2 is split across two YAML entries. Its "else `billing`" half is merged into C3's keyword list. A reader can no longer see one entry per rule, and if a later edit reorders or splits the entries, refund tickets can be misrouted without any error.

**Design 2:**
- It has one function with six branches, one per rule, in priority order.
- Each `if` maps to exactly one rule, including C2's nested split.
- C7 is handled once, by `subject = t.subject.lower()`.
- Changing a rule is a one-line diff in reviewed, deployed code, which is exactly the process C8 describes.

**Ledger:**
- **Forced:** first-match priority order (C1–C6) and a single place where case is normalized (C7).
- **Deletions:** the YAML file, the operator table, the interpreter and the import-time file load. No constraint breaks without them, because C8 makes code the rule-editing medium.
- **Counts:** Design 1 has about five more concepts, a runtime-only failure path and one rule split across two entries. Design 2 has none of these.

**Deciding reason:** both route every ticket correctly, but Design 1 adds a rule language and interpreter that only matter if people outside code review edit the rules, which C8 rules out, and that language brings failure modes of its own.

WINNER: 2