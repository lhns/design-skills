**Candidate B is the better design.**

The three behaviours are not governed by the same rule, even though today they share the number seven.

- **Late fee (7 days):** This comes from clause 4.3 of the tenancy agreement. It is a contractual term that can't change without amending every tenancy.
- **Reminder letter (7 days today):** This is a co-op policy choice. The September board minutes already schedule a change: from January, a six-month trial sends it after three days, then probably a revert or a permanent change after the July report.
- **Dashboard:** The treasurer wants it to match the reminders exactly, so it should follow the reminder rule, not the fee rule.

**Candidate A** uses a single `OVERDUE_AFTER` for all three. When the trial starts, the developer has to change that one constant, and the damage is easy to miss:

- Set it to 3 days and the nightly job starts charging 15.00 fees on day 3. That breaches the tenancy agreement and charges tenants money they don't owe.
- Leave it at 7 and the trial doesn't happen.
- Either way, the developer must first untangle the shared constant under time pressure, and the comment on it ("clause 4.3") would be wrong for the reminder.

**Candidate B** gives the two reasons for change separate homes:

- `REMINDER_AFTER` is a policy knob, and the trial is a one-line change.
- `LATE_FEE_AFTER` is tied to the contract, and its comment cites clause 4.3.
- The dashboard and the reminders share `is_overdue`, so the treasurer's requirement that they agree is enforced by construction. A household can't appear on the dashboard without being sent a letter.
- The fee can't drift with the trial, because it has its own predicate.

This isn't speculative generality. The change is documented in the board minutes and has a date. It is also the case where the usual DRY warning applies: two pieces of code that look the same today but change for different reasons should not be merged. The identical `7` values are a coincidence, not shared knowledge.

B has small flaws:

- `late_fee_applies` repeats the `not paid and today >= due + …` shape.
- `is_overdue` is a slightly generic name for what is really "reminder-overdue".
- `late_fee_applies` lacks a docstring.

These are cosmetic. A cleaner version might name the first predicate `is_behind` and parameterise a shared helper by threshold. They don't outweigh A's coupling of a contractual rule to a policy that is about to change.

WINNER: 2