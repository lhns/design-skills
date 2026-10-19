**Design 2 (Candidate A) is the better design**, because Design 1 cannot reproduce past reports, and the audit depends on that.

**Why Design 1 fails**

Jonas asked whether old versions of the mapping were needed, and Rhea said no because reports are never resubmitted. Her later comment contradicts that. Every June the auditor reruns two of the previous year's quarterly reports from the system and checks them line by line against the PDFs sent to the trust.

With Design 1's single mutable `MAPPING`:

- On 1 April Rhea moves VOL-TRAVEL and VOL-SUBS to "Programme delivery".
- In June the auditor reruns, for example, Q3 of the previous year.
- The report has no "Volunteer expenses" row, and "Programme delivery" is larger than on the submitted PDF.
- The audit tick-off fails, even though nothing was wrong with the original report.

The comment "the app has one answer for where a code belongs" is the flaw. Where a code belongs depends on *when* the money was spent. Since expenses are never deleted, the inputs are stable, and the mapping is the only thing that changes over time.

**Why Design 2 works**

- **Effective-dated, append-only mapping.** Each expense maps by its own `spent_on` date, so a report for an old quarter always gives the same result. That is what the audit needs.
- **Fits the known change.** The 1 April fold is just two new rows dated `2025-04-01` (or whichever year applies). No old row is edited.
- **Not speculative.** Jonas's YAGNI concern was reasonable, but this history has a real user (the auditor) and a change already scheduled. It is also cheap: one extra column and a lookup function, not a versioning system.
- **Clear failure.** `line_for` raises a `KeyError` naming the code and date when no mapping applies, such as a code used before its start date. Design 1 would give a bare `KeyError: 'X'`.

**Minor points on Design 2 (not blocking)**

- If two rows for the same code have the same `valid from` date, `max(starts)` silently picks the alphabetically later line. A check at load time that `(code, valid_from)` is unique would catch Rhea's typos.
- `line_for` scans the whole list for each expense. At a few thousand expenses a year that cost doesn't matter, so the simple version is the right choice.
- "Rows are never edited or removed" is only a comment. A test that pins the totals of a past report would catch it if someone broke that rule.

Design 1 is simpler, but it is simple because it ignores the requirement that past reports stay reproducible.

WINNER: 2