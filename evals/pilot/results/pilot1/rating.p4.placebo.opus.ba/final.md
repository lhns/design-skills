# Design 2 (Candidate A) is the better design

**Why the YAML rule engine doesn't earn its place**

The main reason to move rules into configuration is to let people edit them without touching code. Here that reason doesn't apply. Only the owning engineers change the rules, a few times a year, through code review and deploy. Changing YAML gives no faster path than changing Python. Design 1 adds a small DSL to maintain anyway: an operator table, a matcher, a schema that lives only in a comment, and a loader. That is speculative generality (YAGNI).

**Problems specific to Design 1**

- **Harder to read.** The priority rules are a short decision list, and Design 2 says exactly that. In Design 1, rule 2 becomes two YAML entries. The `billing` entry also has to repeat `refund` next to `invoice`/`receipt`, so the "refund" knowledge now lives in two places. Rule 4 is likewise split in two. A reviewer has to rebuild the original intent from the order of the entries.
- **Errors appear late and are vague.**
  - A typo in an operator (`contians_any`) raises a `KeyError` only when a ticket reaches that rule.
  - A typo in a field name raises an `AttributeError` at routing time.
  - Removing the catch-all rule causes a bare `StopIteration`.
  - Nothing validates the file at load time.
- **Hidden traps.**
  - `contains_any` lowercases the subject but not the keywords, so writing `Refund` in the YAML silently never matches.
  - `open("routing.yaml")` is relative to the current working directory, not the module.
  - The file is read as a side effect of import, which makes testing awkward.
- **Weaker tooling.** Type checkers, linters, "find usages" and stack traces all work on Python. None of them understand the YAML.

**Design 2**

- It maps one-to-one onto the specification, in priority order.
- It handles the `None` amount explicitly.
- It is trivially unit-testable, and changes show up in review as clear diffs.

Small tweaks would make it better still: rename `t` to `ticket`, and give the `500` threshold a named constant such as `REFUND_ESCALATION_THRESHOLD`. If the rules later need to be edited by non-engineers, that is the time to introduce a data-driven engine.

WINNER: 2