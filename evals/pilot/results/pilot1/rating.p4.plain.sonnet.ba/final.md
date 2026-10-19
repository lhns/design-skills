**Design 2 is better.**

The rules are only changed by the engineers who own the service, through code review and deploy. Nobody else will edit them, so the main benefit of a data-driven rule engine, letting non-engineers change behavior without a deploy, doesn't apply here. Design 1 pays for that flexibility anyway:

- **Indirection:** to understand routing you have to read the YAML, the operator table, and the interpreter, and mentally combine them. In Design 2 the priority order reads top to bottom in one function.
- **Duplication and fragility:** Design 1 splits rule 2 and rule 4 into separate entries and repeats keyword lists (`refund` appears twice, `password`/`login` twice). Correctness depends on the order of the entries and on the `billing` rule listing `refund` again as a fallback. Design 2 expresses the nested logic (refund, then amount) directly.
- **Error handling:** a typo in a field name, operator, or queue in the YAML fails only at runtime (`getattr`/`KeyError`), and the `next(...)` without a default raises `StopIteration` if no rule matches. Design 2 uses plain code that linters, type checkers, and tests can check.
- **Hidden bugs:** `contains_any` assumes the field is a string, and `gt` works only because of its special None check. The YAML file is loaded at import time from a relative path, so it depends on the working directory. Design 2 has none of these.
- **Change cost:** the rules change a few times a year, and each change goes through review and deploy regardless. Editing a few lines of Python is as easy as editing YAML, and the diff is easier to review. If a new kind of condition is needed (for example, a time-of-day check), Design 1 requires extending the interpreter as well, so it is no longer config-only.

Design 2 is shorter, explicit, and type-checkable, and it matches how the rules are actually maintained. If non-engineers needed to edit the rules, or the rule set grew large, Design 1 would make sense, but neither is the case here.

WINNER: 2