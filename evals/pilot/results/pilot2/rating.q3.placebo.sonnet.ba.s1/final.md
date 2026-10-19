**Design 1 is the better design.**

The two designs behave identically today, because both thresholds are 7 days. They differ in what happens when the reminder timing changes, and the board minutes say it will.

**Two different rules.** The late-fee threshold is a contractual term (clause 4.3) that the co-op can't change on its own. The reminder timing is an internal policy, and the board has agreed to trial 3 days from January. The two values are equal now by coincidence, and they change for different reasons.

**Design 2 merges them.** It uses one `OVERDUE_AFTER` for the dashboard, the reminders and the fees, and its comment ties all of it to clause 4.3. To run the trial, someone would change that constant to 3 days. That would also charge the 15.00 fee after 3 days, which the tenancy agreement doesn't allow. The alternative is to untangle the constant under time pressure in January. The "obvious" edit is the wrong one.

**Design 1 separates them while keeping the treasurer's requirement.**
- The dashboard and the reminders both go through `is_overdue`, so they cannot disagree about who is behind. This is the auditor's concern, and it is satisfied structurally rather than by two predicates kept in step by hand.
- `REMINDER_AFTER` is the only value the trial needs to change, and the fee rule stays at 7 days, tied to its clause.
- `late_fee_applies` has its own constant, `LATE_FEE_AFTER`, with a comment citing the clause. A reader can see why 7 days is fixed.

**On DRY.** Two constants both equal to 7 can look like duplication. They are separate pieces of knowledge, one contractual and one policy, so a shared constant would be the wrong abstraction.

**Small remaining points.** `is_overdue` could be named more precisely, for example `needs_reminder`, since "overdue" now means "overdue for dashboard and reminder purposes". That is a minor point and doesn't change the verdict.

WINNER: 1