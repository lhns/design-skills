# Candidate A (Design 1) is the better design

## The central issue: one rule, one home

The complaints log describes a specific failure. The board changed the cutoff, the code (or the desk) followed the new rule, and the email still showed the old one. The email counts as the learner's copy of the terms, so the stale wording cost 23 refunds.

**Candidate B repeats that failure.** The cutoff lives in two places:

- `FULL_REFUND_DAYS = 10` in Python
- "at least ten days before your first session" typed into Gwen's template

When the board next changes the terms, someone must update both. They are owned by different people: developers own the constant and Gwen owns the text. Nothing links the two copies, and no test fails if they disagree. This is the DRY case where duplication is truly dangerous: a business rule copied across a team boundary.

**Candidate A fixes this.** `FULL_REFUND_BEFORE` drives both:

- `refund_on_withdrawal`, through `full_refund_deadline`
- the email, through the `$refund_deadline` placeholder

When the policy changes, a developer edits one constant, and every email after that states the new deadline. The email cannot contradict the code that decides refunds.

## It also suits the people involved

- **Gwen** keeps full control of the wording. She has one more placeholder, `$refund_deadline`, which she can move around as she asked. She never edits Python.
- **Learners** get a concrete date, such as "Monday 12 January", instead of "ten days before". This is clearer and leaves less room to argue at the desk.
- **The deadline-day rule** ("a withdrawal on the deadline day itself still gets the full refund") is spelled out in A. A named function returns the "last day on which a withdrawal still gets the full fee back", and the code compares with `today <= deadline`. The template's "on or before" matches it exactly. In B, the reader has to work out that `.days >= 10` gives the same boundary.

## Correctness

Both versions compute the same boundary. With plain dates, `today <= first_session - 10 days` is equivalent to `(first_session - today).days >= 10`. So B is not wrong today. It is fragile, because its correctness depends on two separately maintained copies staying in sync.

## Minor points that apply to both

- The template is read at import time. A missing file fails at startup, which is fine (fail fast), but Gwen's edits only take effect after a restart.
- `Template.substitute` raises an error if Gwen deletes or misspells a placeholder. This is the right behaviour. A test that renders the real template file would catch the problem before deployment.
- A's template still states the shape of the policy ("full refund… after that no refund") in prose. If the board ever brought in partial refunds, the template would need rewording anyway. That is a real change of terms, not a number drifting out of sync, so it is acceptable under YAGNI.

WINNER: 1