**Design 1 (Candidate B) is better.**

The two designs behave identically today, since every threshold is 7 days. They differ in what happens when the rules change, and the board minutes say one of them will change in January.

- **The reminder trigger and the late fee are separate rules.** The reminder timing is a co-op policy choice, and the board has agreed to trial 3 days for six months. The late-fee timing is a contractual term (clause 4.3, 7 days) and can't be changed by a board trial. They only coincide at the moment.

- **Design 2 ties them together.** It uses one `OVERDUE_AFTER` constant for the dashboard, the reminders and the fees. To run the trial, someone would have to change that constant to 3 days. That would silently start charging £15 fees at 3 days, which breaches the tenancy agreement. The alternative is to untangle the code under time pressure. Its comment cites clause 4.3 as the justification for the reminder timing, which is the wrong source, and that makes the trap more likely.

- **Design 1 keeps the treasurer's requirement.** The dashboard and the reminders both use `is_overdue`, so "behind" on the dashboard is exactly what triggers a letter. This addresses the auditor's finding. Changing `REMINDER_AFTER` to 3 days moves both together and leaves the fee rule alone.

- **Design 1 documents its source.** `LATE_FEE_AFTER` carries the clause 4.3 reference, so a future reader can see that it is contractual and shouldn't be changed with the trial.

Design 1 has two constants with the same value, which looks like duplication. But they encode different facts that happen to be equal today, so the duplication is deliberate and correct. Sharing `is_overdue` between the dashboard and the reminders is the coupling the treasurer asked for, and keeping the fee rule separate is the decoupling the contract requires.

WINNER: 1