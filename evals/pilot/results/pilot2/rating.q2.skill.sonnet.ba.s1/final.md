**Constraints**
- C1: The report has one row per trust reporting line, built from expenses grouped by budget code (stated).
- C2: Rhea edits the mapping a few times a year, and VOL-TRAVEL and VOL-SUBS move to "Programme delivery" on 1 April (stated).
- C3: Expenses are never deleted, and corrections are posted as new rows (stated).
- C4: In June the auditor re-runs two of the previous year's quarterly reports from the system and ticks them off line by line against the PDFs already sent (stated by Rhea). The re-run must reproduce the sent numbers.
- C5 (inferred): Reports are never resubmitted, so history is not needed for resubmission. Rhea's "no reason to keep old versions" is true for that purpose, but C4 is a separate purpose that she did not connect to the question.

**Where the problem is**
Jonas asked whether history is needed, and Rhea said no. The audit comment, written as an unrelated aside, answers that question the other way. Design 1 reads the mapping at run time. After 1 April, VOL-TRAVEL and VOL-SUBS map to "Programme delivery". Re-running a previous year's quarter in the June audit would then put volunteer spend under "Programme delivery" and show nothing under "Volunteer expenses". It would not match the PDFs, so the audit tick-off fails. Design 1's comment, "one answer for where a code belongs", is the very property that breaks C4. Even if the move is applied only at the year boundary, the June audit covers the previous year's quarters. Those quarters fall before a mapping edit made on 1 April, so they would be re-run against the new mapping.

Design 2 stores a valid-from date per row and resolves the line by the expense date. Old quarters still resolve to the old lines, and the move is a new row dated 2027-04-01. The rows are append-only, so a past report cannot silently change.

**Breaking each design**
- Design 1: re-run the 2026-27 Q1 report after the 1 April move. The totals differ from the sent PDF, so C4 fails. No input rescues it, because the information is gone once the dict is edited.
- Design 2: an expense with no applicable row raises `KeyError`, which is loud and acceptable. A late correction posted for an old expense is dated by `spent_on`, so it uses the mapping in force then, which is consistent. A mid-quarter change would split a quarter by date, which is correct. I found no input that breaks a constraint.

**Cost of Design 2**
It adds one concept, the valid-from date, and a small `line_for` function. The constraint that forces it is C4. Jonas's "history nobody uses" is true for resubmission but false for audit re-runs, so the concept is forced rather than speculative. It adds no number or flag, and an edit is "append a row", which suits Rhea's few edits a year. One remaining gap is that "never edited or removed" is enforced only by convention. That fits a single-user app, and I am not adding machinery for it.

**Ledger**
- Constraints: C1–C4 stated, C5 inferred.
- Forced: a time-dependent mapping (C4), resolved by expense date.
- Designer choices: append-only rows by convention, and an error on an unmapped code.
- Deletions: none needed. Design 1 is shorter only because it drops C4.

**Deciding reason:** the audit re-runs past quarters and must match the PDFs already sent, and only Design 2 keeps old mappings so that it can.

WINNER: 2