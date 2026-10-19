# Candidate A is the better design

**The deciding reason:** Candidate A states the refund cutoff once, and both the email and the refund calculation derive from it. Candidate B states it twice, once in Python and once in Gwen's prose, which is exactly the duplicated fact behind the spring complaints.

## Constraints

- **C1.** Full refund if the learner withdraws at least N days before the first session, and nothing after. No partial refunds.
- **C2.** The board sets N and changes it from time to time. It has changed twice in four years.
- **C3.** The office team owns the email wording. Gwen edits the template, never Python, and placeholders she can move around are fine.
- **C4.** The confirmation email is the learner's copy of the terms. If the email and the computed refund disagree, the centre pays, as with the 23 spring refunds.
- **C5.** The system works in whole days, and a withdrawal on the deadline day itself still gets the full refund.

## Testing each design against them

**C1 and C5.** Both designs compute the same boundary. Candidate A refunds when `today <= first_session - 10 days`. Candidate B refunds when `(first_session - today).days >= 10`. These conditions are equivalent, and both include the deadline day. Neither design breaks here.

**C2 combined with C4.** This is where they differ.
- In Candidate B, the board changing N from 10 to 14 means a developer edits `FULL_REFUND_DAYS`. The template still says "ten days" until Gwen notices. That is the March–June scenario again: the code refunds by one rule while the email promises another, and under the trading standards advice the email wins.
- Candidate B also fails the other way round. Gwen rewording the paragraph to "two weeks" changes nothing in the code. The template is a second, unenforced copy of the policy.
- In Candidate A, the same change is a single edit, and every subsequent email shows the matching date. Gwen's file contains no number to drift.

**C3.** Both designs keep Gwen out of Python. Candidate A adds one placeholder, `$refund_deadline`, which is exactly the kind of movable placeholder she said she accepts. It also gives the learner a concrete date ("Friday 12 September") rather than arithmetic to do themselves, which is fairer to learners and easier at the desk.

## Concept count

| | Candidate A | Candidate B |
|---|---|---|
| Policy fact stated | once (`FULL_REFUND_BEFORE`) | twice (constant and template prose) |
| Derived concept | `full_refund_deadline`, used by both the email and the refund | none |
| Special cases | 0 | 0 |

Candidate A has one more function. That function is forced: it is the single place where C4's "email equals rule" invariant holds. The extra concept traces to a constraint, so it is not overhead.

## A gap neither design closes

C4 says the email is the learner's copy of the terms. Consider a learner who enrols under a 10-day rule and withdraws after the board has moved to 14 days.
- Both candidates compute that learner's refund with the *current* constant.
- That contradicts the email they were sent.

The fix fits naturally into Candidate A:
1. Compute `full_refund_deadline` once, at enrolment.
2. Store it on the enrolment record.
3. Use the stored date for both the email and `refund_on_withdrawal`.

Then the invariant becomes "a learner's refund is decided by the deadline printed in their email", which is exactly what trading standards said. Candidate B has no deadline concept to store, so it would have to grow one, and in doing so it would turn into Candidate A.

WINNER: 1