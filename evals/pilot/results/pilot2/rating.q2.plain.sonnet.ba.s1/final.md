**Design 2 is the better design.**

Jonas's question was whether anyone needs old versions of the mapping. Rhea answered no, but only about resubmitting reports. Her last comment gives the real reason: each June the auditor re-runs two of the previous year's quarterly reports from the system and ticks them off line by line against the PDFs already sent to the trust.

That requires the app to reproduce a past report exactly, long after the mapping has changed.

**Design 1** reads a single mutable mapping at run time. On 1 April, Rhea will move VOL-TRAVEL and VOL-SUBS into "Programme delivery". After that, re-running any earlier quarter would:
- show no "Volunteer expenses" row, even though the sent PDF has one;
- inflate "Programme delivery" by the same amount.

The totals would no longer tick off against the PDFs, and the audit would show discrepancies that are really just the mapping having moved. Nothing in the data would explain the difference. The comment "one answer for where a code belongs" describes the flaw: that single answer is only correct for the present.

**Design 2** keeps the mapping as append-only rows with a valid-from date, and resolves each expense's line by the expense date. Quarters before 1 April 2026 keep resolving to "Volunteer expenses", and later ones resolve to "Programme delivery". Rhea just appends rows such as `("VOL-TRAVEL", "Programme delivery", date(2026, 4, 1))`, so the cost to her is small. Because expenses are never deleted and corrections are new rows, the expense data is also stable, so reruns are deterministic. The history is not speculative. It is needed for the audit and it is only a few lines of code.

Design 2 does need one note. Expenses dated before the earliest valid-from date raise a `KeyError`. That is acceptable, because it fails loudly rather than silently misreporting.

WINNER: 2