**Design 2 (Candidate B) is better.** It separates two rules that change for different reasons, and it keeps the two that must agree tied together.

**There are two thresholds, not one.**

- **The late-fee threshold** is contractual. Clause 4.3 says a charge may be added only once rent is unpaid seven days after it is due. It changes only if every tenancy agreement changes.
- **The "behind" threshold** drives the dashboard and the reminder letter. The co-op sets it as policy. The treasurer's email requires the dashboard and letters to use exactly the same definition. The September board minutes say this threshold will move to three days from January as a six-month trial.

Today both are 7 days, so the two designs behave the same. That is incidental similarity, not shared knowledge.

**Why Candidate A is the riskier design**

A has one constant, `OVERDUE_AFTER`, used for the dashboard, reminders and late fees. Its comment says the value comes from clause 4.3, which tells the next developer it is the contractual figure.

When someone implements the board's trial by setting `OVERDUE_AFTER = timedelta(days=3)`, the reminders and dashboard change correctly. But late fees would also start being posted on day 3. That breaches the tenancy agreement for every household, and nothing in the code warns against it. A merges these thresholds too early: copies that change for different reasons should not share one home.

**Why Candidate B fits the requirements**

- The dashboard and `reminders_due` both use `is_overdue`, so they cannot drift apart. That satisfies the treasurer and the auditor.
- `late_fees_due` uses its own `late_fee_applies` and `LATE_FEE_AFTER`, and the clause 4.3 comment sits beside the constant it actually describes.
- The January trial is a one-line change to `REMINDER_AFTER`. Reverting it in July is just as easy, and neither touches the contractual rule.

**Small improvements to B (not blocking)**

- Add a comment on `REMINDER_AFTER` explaining that it is co-op policy, that it must match the dashboard (per the treasurer), and that the board's January trial will change it. That way nobody "tidies" the two 7-day constants back into one.
- Add tests that pin the separation. With the reminder threshold at 3 days, a charge at day 4 should appear on the dashboard and in reminders but not in late fees.

WINNER: 2