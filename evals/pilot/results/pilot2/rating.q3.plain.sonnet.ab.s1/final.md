**Design 2 (Candidate B) is better.**

The two designs behave identically today. They differ in what happens when the rules change, and the board minutes say a change is coming.

**What the sources require**
- **Dashboard and letters must agree (treasurer).** Both designs do this by having `dashboard` and `reminders_due` share one predicate, `is_overdue`.
- **The reminder timing is about to change (board minutes).** From January, the friendly reminder goes out after 3 days for a six-month trial, then probably reverts or is adjusted depending on the July report.
- **The late fee is fixed by contract (clause 4.3).** The fee may only be added once rent is unpaid seven days after it is due. A board trial of earlier reminders doesn't change the tenancy agreement.

**Candidate A** uses a single `OVERDUE_AFTER` for the dashboard, the reminder and the fee. This keeps the dashboard and letters in sync, but it also ties the fee to the same threshold. To run the 3-day trial, the developer would change `OVERDUE_AFTER` to 3 days. That would silently start charging £15 late fees at 3 days, which breaches the tenancy agreement. The alternative is to split the function during the trial, under time pressure. The comment citing clause 4.3 would also be wrong, because the constant would then drive the reminder as well as the fee.

**Candidate B** separates the two concepts:
- `REMINDER_AFTER` drives `is_overdue`, which both the dashboard and the reminders use. They stay in sync by construction, and the trial is a one-line change that moves both together, so the treasurer's requirement still holds.
- `LATE_FEE_AFTER` is tied to clause 4.3 and is unaffected by the trial.

The two `7`s look like duplication, but they are different facts with different sources and different reasons to change. B keeps them separate, while A merges them only because they happen to be equal today.

One minor point: B's `late_fee_applies` has no docstring, and its body repeats the shape of `is_overdue`. That is a small cost next to A's risk of overcharging tenants.

WINNER: 2