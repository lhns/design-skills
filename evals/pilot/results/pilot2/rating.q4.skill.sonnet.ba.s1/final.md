**Constraints**
- C1 (Odile): the refund rule is full refund if withdrawing at least 10 days before the first session, otherwise nothing. The deadline day itself gets the full refund.
- C2 (Odile, complaints log): the email is the learner's copy of the terms, so the email and the refund logic must never disagree. The spring-term incident cost 23 refunds when they did.
- C3 (Odile): the board changes the terms occasionally, twice in four years.
- C4 (Gwen): the office team edits the template without a developer, and placeholders are fine.
- C5 (inferred): the refund calculation must be correct for whole-day dates.

**Core fact.** The cutoff is one fact: "10 days before the first session". Design 1 states it twice, as `FULL_REFUND_DAYS = 10` in code and as the word "ten" in the template prose. A board change then needs a code edit and a template edit kept in sync. That is the exact failure from spring: the code moved from 7 to 10 while the emails still said "one week". Nothing in Design 1 prevents it from recurring, and the template is owned by a different person from the code.

Design 2 states the fact once. The email's wording is derived from the same value the refund uses, as the deadline date. When the board changes the constant, the code and every new email change together.

**Trying to break each design**
- Design 1: the board changes the cutoff to 14 days, a developer updates the constant, and Gwen's template still says "ten days". The email and the refund now disagree, so C2 fails. Nothing detects this.
- Design 2: I can't find an input that makes the email and refund disagree, because both call `full_refund_deadline`. The boundary is right too: `today <= deadline` gives a full refund on the deadline day, which is what Odile specified. Design 1's `>= 10` is equivalent, so C1 and C5 hold in both.
- Gwen's workflow (C4) holds in both. Design 2 adds a `$refund_deadline` placeholder that she can move around freely, and she doesn't need to touch Python.

**Side benefit.** An absolute date ("on or before Friday 12 June") is also clearer to a learner than counting days. It removes the ambiguity of whether "ten days before" includes the session day.

**Costs and caveats**
- Design 2 adds one function, `full_refund_deadline`. That function names the single shared fact, so it earns its place under C2. It also uses `timedelta` instead of a bare integer, which is fine.
- Design 2 does not fix the case where an already-sent email says the old terms after a change, because that email is a historical document. This is a separate problem that neither design addresses, and the answer would be to store the terms or deadline with the enrolment. Within scope, Design 2 still removes the main source of drift.
- A small remaining risk in both designs: Gwen could delete the placeholder and hard-code a date or number. That is a template discipline problem, not a design flaw.

**Deciding reason:** Design 2 keeps C2 by deriving the email's deadline and the refund decision from one definition, while Design 1 states the cutoff twice, in code and in prose, which is exactly how the 23 refunds happened.

**Ledger**
- Constraints: C1 refund rule and boundary, C2 email and refund agree, C3 terms change, C4 template editable without Python, C5 whole-day correctness.
- Forced decisions: one definition of the deadline, used by both the email and the refund.
- Designer choices: expressing the cutoff as a `timedelta`, and showing an absolute date in the email.
- Deletions: the duplicated "ten days" fact in the template prose.

WINNER: 2