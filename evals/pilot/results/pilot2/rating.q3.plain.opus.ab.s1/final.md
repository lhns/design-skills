**Design 2 is better.** The two designs behave identically today, since both thresholds are 7 days. The difference is which rules they tie together, and the co-op's records say these are two separate rules.

**Two policies, two owners**

- **Late fee:** fixed by the tenancy agreement (clause 4.3). It may only be charged once rent is still unpaid 7 days after the due date. Changing this means changing every tenancy.
- **"Behind" (dashboard and reminder letter):** set by the co-op. The treasurer wants the dashboard and the letters to agree exactly. The board has already agreed to trial a 3-day reminder.

**Why Design 1 is risky**

Design 1 has a single `OVERDUE_AFTER`, documented as clause 4.3, driving all three functions. When the trial starts, the developer will change it to 3 days. That silently starts posting £15 fees on day 3, which breaches the tenancy agreement for all ~140 homes. Undoing that means refunds and an awkward conversation with the auditor, which is the kind of embarrassment the treasurer wanted to avoid.

The alternative fix is to leave the constant alone and give the reminder its own threshold. But then the dashboard and the letters no longer agree, which repeats last year's audit finding. Design 1 has no correct one-line change for the trial.

**Why Design 2 fits**

- The dashboard and reminders share `is_overdue`/`REMINDER_AFTER`, so they can never drift apart. This meets the treasurer's requirement.
- Fees use `late_fee_applies`/`LATE_FEE_AFTER`, cited to clause 4.3, so a change to reminder timing cannot affect fees.
- The trial is a one-constant edit, and so is reverting it in July if the board decides against it.

The shared 7 days is a coincidence between two policies, not one rule, and Design 2 models it that way.

**Small improvement for Design 2**

`REMINDER_AFTER` should have its own comment saying it is co-op policy (the board trial, and the treasurer's rule that dashboard and letters match), not a contractual term. Otherwise a future maintainer may "tidy" the two constants back into one.

WINNER: 2