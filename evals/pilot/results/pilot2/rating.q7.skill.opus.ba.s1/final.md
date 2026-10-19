# Candidate A (Design 2) is the better design

**Constraints**
- **C1.** The flyer rules:
  - 64.00 per ticket.
  - Early bird is 15% for bookings on or before 28 Feb.
  - Group is 10% for 6 or more tickets.
  - Member is 20%.
  - Group and member don't combine; the larger one wins.
  - Early bird combines with either.
  - Total discount is capped at 30%.
  - A 2.00 booking fee applies per order and is never discounted.
- **C2.** Amounts are Decimal. The ticket total is rounded half-up to the cent after discounts.
- **C3.** Every year, Bea, who reads only plain Python, checks the code line by line against the flyer. What runs in which order must be obvious, because that was last year's failure.
- **Not a constraint:** the residents' discount. The committee "talks about it"; it "hasn't happened yet."

**Trying to break both candidates**

Test orders:
- 6 tickets, member, early: 0.20 + 0.15 = 0.35, capped to 0.30.
- 6 tickets, non-member, late: 0.10.
- 1 ticket, booked on 28 Feb: early bird applies.
- Group and member both apply: the 0.20 survives.

Both candidates give the same results on all of these. Both round before adding the fee. Neither breaks C1 or C2, so the decision is made by C3 and by concept count.

**Concepts in B with no constraint behind them**
- **The `RULES` registry and `@rule` decorator.** This is an extension point with zero current users beyond the built-in rules. It is justified only by the residents' discount, which is not a requirement.
  - It also wouldn't absorb that discount cleanly. Bea says it will have "its own rules about what it combines with." In B, that means editing or adding pairwise resolver rules like `group_or_member`, not just "one more decorated function."
- **Step numbers 10/20/30/90.** These are unforced numbers. Correctness depends on them: `group_or_member` must run after both step-10 rules. That makes execution order implicit, which is exactly what made last year's review take an afternoon. This breaks C3.
- **`Quote` with a mutable `discounts` dict and a `fees` accumulator.** The flyer has one fixed fee. Discounts are added and then deleted, so "don't combine" is stated as a correction after the fact instead of directly.
- **A global, mutable, re-sorted `RULES` list.** It is filled at import time. Bea cannot see the program's flow from top to bottom.

**A, read against the flyer**
- Each flyer sentence maps to about one line:
  - `max(group, member)` for "you get the better one".
  - `+= early` for "combines with either".
  - `min(..., cap)` for the cap.
  - `+ BOOKING_FEE` after rounding.
- The order of execution is the order on the page. There are no exception clauses and no rule-ordering numbers.
- If the residents' discount ever arrives, re-deriving this 10-line function from its actual combination rules is cheaper and safer than designing a plugin system now around rules nobody has stated.

**Ledger**
- **Forced:**
  - Max of group and member, plus early bird, then cap (C1).
  - Round, then add the fee (C1, C2).
  - Straight-line code readable top to bottom (C3).
- **Designer choices (both candidates):** `EARLY_BIRD_UNTIL = 2027-02-28` is inclusive, reading "book by" as "on or before."
- **Deleted from B:**
  - The rule registry and decorator.
  - The step numbers.
  - `Quote`.
  - The add-then-delete conflict rule.
  - The fees accumulator.

**Deciding reason:** Both are correct, but A states the flyer's combination rules directly in reading order. B hides that order behind step numbers and a registry built for a discount that isn't a requirement, and that hidden order is exactly what Bea's yearly review needs to see.

WINNER: 2