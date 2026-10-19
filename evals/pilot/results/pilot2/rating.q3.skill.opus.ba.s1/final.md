# Design 1 (Candidate B) is better

## Constraints

- **C1 (clause 4.3):** a late fee may be added only once rent is still unpaid 7 days after its due date, at most once per month.
- **C2 (treasurer's email):** whoever is "behind" on the dashboard is exactly whoever triggers a reminder letter.
- **C3 (board minutes):** from January the reminder goes out sooner, after 3 days, as a six-month trial that may be reversed.

## What the constraints force

- **The fee threshold and the reminder threshold are separate facts.** C1 fixes the fee at 7 days. C3 moves the reminder to 3 days. Today both happen to be 7, but they change for different reasons: a contract versus a board trial. Merging them would merge two different facts, not remove a duplicate.
- **The dashboard and the reminder share one predicate.** This is C2. Both designs do it through `is_overdue`.

## Trying to break each design

- **Design 2 (Candidate A)** has one concept, `OVERDUE_AFTER`, that carries both the fee threshold and the letter threshold. In January someone sets it to 3 days for the trial. On the 4th, every unpaid household is charged £15. Clause 4.3 does not allow that. To avoid it, the developer has to split the constant and the predicate. That is the split Design 1 already has, but now made under pressure. Its comment ties the reminder and the dashboard to clause 4.3, which the board has already decided to change. Design 2 also passes C2 today, but it is one edit away from breaking C1.
- **Design 1 (Candidate B):**
  - Setting `REMINDER_AFTER = 3 days` moves the dashboard and the letters together, so C2 holds.
  - The fee stays at 7 days, so C1 holds.
  - Ending the trial means reverting one value.
  - I found no input or edit that breaks C1, C2 or C3.

## Concept count

Design 1 has one more constant and one more predicate. Both are forced by C3 together with C1, so the extra concepts are justified.

One small gap in Design 1: `REMINDER_AFTER` has no comment naming its source. It should cite the board decision and the January trial, as `LATE_FEE_AFTER` cites clause 4.3. That is a documentation fix, not a structural one.

**Deciding reason:** the board has already decided that letters will go out earlier than fees can be charged, and only Design 1 keeps those as separate facts, so the trial cannot trigger unlawful late fees.

WINNER: 1