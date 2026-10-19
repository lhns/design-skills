**Design 1 is better.** The two 7-day values are different facts that happen to be equal today, and only Design 1 keeps them apart.

**Constraints**
- C1 (contract, clause 4.3): a late fee may be added only when rent is still unpaid 7 days after the due date, once per month.
- C2 (treasurer): the dashboard's definition of "behind" must be exactly the reminder letter's trigger.
- C3 (board, September item 6): from January, for six months, the reminder goes out after 3 days. This is a trial, and it ends or is revised after the July report.

**What they force**
- C1 and C3 give two thresholds with different sources and different lifetimes. One is a contractual term. The other is a policy under trial. They are equal now (7 days) but will diverge in January and may change again in July.
- C2 forces the dashboard and reminders to share one definition. Both designs do this through `is_overdue`.
- Fee, dashboard and reminder are therefore two concepts, not one: "the reminder/dashboard threshold" and "the fee threshold".

**Trying to break each design**
- Design 2: in January, set `OVERDUE_AFTER` to 3 days.
  - The dashboard and letters move to 3 days, which satisfies C2 and C3.
  - `late_fees_due` also moves to 3 days, so fees are charged before the contract allows them. That breaks C1 and exposes the co-op to charging tenants unlawfully.
  - The fix is to split the concept at that point, under time pressure, and the comment citing clause 4.3 would then sit on the wrong constant.
  - Design 2 is shorter only because it states one fact where reality has two.
- Design 1: set `REMINDER_AFTER` to 3 days.
  - The dashboard and letters change together, so C2 holds.
  - The fee stays at 7 days, so C1 holds.
  - One constant changes, and the trial ends by reverting that same constant.

**Counting**
- Design 1 has two constants and one extra predicate. Design 2 has one constant.
- Design 1's extra parts trace to C1 and C3. Design 2 saves them only by dropping a constraint, which is false elegance.
- Design 1 is not duplication, because the two values change for different reasons.
- Weakness in Design 1: `REMINDER_AFTER` has no comment giving its reason. It should say it is a policy value, under trial from January per the board minutes, and independent of clause 4.3.

**Ledger**
- Constraints: C1 contract fee threshold; C2 dashboard equals letter trigger; C3 reminder threshold changes in January.
- Forced: separate fee threshold; shared dashboard/reminder predicate.
- Designer choices: none beyond naming.
- Deletions: none. Design 2's single constant is rejected because it breaks C1 under C3.

WINNER: 1