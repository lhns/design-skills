# Design 1 (Candidate B) is better

The key question is which rules change together and which only look alike today.

**Three rules, two sources of truth**

| Concern | Source | Will it change? |
|---|---|---|
| Who appears on the dashboard | Treasurer: must match exactly who gets a letter | Moves with the reminder rule |
| When the reminder letter goes out | Co-op policy; board trial moves it to 3 days from January | Yes, soon |
| When the late fee may be charged | Tenancy agreement, clause 4.3: 7 days | Only if every tenancy is amended |

Right now all three thresholds are 7 days. That is coincidence, not a shared rule.

**Design 2 merges them into one constant.** `OVERDUE_AFTER` drives the dashboard, the reminders and the late fee, and its comment cites clause 4.3 for all three. In January someone will run the board's trial by changing it to `days=3`. The dashboard and letters will move correctly, but the co-op will also start charging £15 fees on day 3. That breaches the tenancy agreement, which allows the charge only after seven days. Worse, nothing in the code warns them, because the comment says the constant *is* the contractual rule. This is DRY applied to incidental similarity. The wrong abstraction makes the cheap change dangerous.

**Design 1 keeps the knowledge in the right places:**
- `is_overdue` is the single definition behind both `dashboard` and `reminders_due`. That meets the treasurer's requirement by construction: the auditor's finding cannot happen again.
- `late_fee_applies` has its own constant, tied to clause 4.3 by the comment. The January trial is a one-line edit to `REMINDER_AFTER` and cannot affect the fee rule.

**Small suggestions for Design 1 (not blocking):**
- Add a comment on `REMINDER_AFTER` noting that it is co-op policy, not contractual, and that the board is trialling 3 days from January. Also note that it intentionally also drives the dashboard. This makes the asymmetry with `LATE_FEE_AFTER` deliberate rather than looking like duplication someone might "clean up".
- `is_overdue` is a slightly vague name now that "overdue" has two meanings. A name like `is_in_arrears` or `needs_reminder` would make clear it is the dashboard/reminder rule.
- A test that sets the reminder threshold below 7 days and asserts no fee before day 7 would protect the contractual rule from future refactoring.

WINNER: 1