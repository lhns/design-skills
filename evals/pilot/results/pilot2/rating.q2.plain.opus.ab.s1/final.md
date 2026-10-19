# Design 1 (Candidate A) is the better design

The deciding fact is in Rhea's last comment, not in the ticket. Jonas asked whether old versions of the mapping matter, and Rhea said no, because reports are never resubmitted. But each June the auditor **re-runs two of the previous year's quarterly reports from the system** and checks them line by line against the PDFs sent to the trust. So the system has to reproduce an old report exactly, using the mapping that applied then.

## The timeline that breaks Candidate B

- Today is October 2026. The trust folds "Volunteer expenses" into "Programme delivery" from **1 April 2027**.
- In April 2027, Rhea edits `MAPPING` so that VOL-TRAVEL and VOL-SUBS point to "Programme delivery".
- In **June 2027**, the auditor picks two quarters from April 2026 to March 2027. Those reports were sent with a "Volunteer expenses" row.
- With Candidate B, the re-run has no "Volunteer expenses" row, and "Programme delivery" is too high by the same amount. Every affected line fails the tick-off.
- The grand total still matches, so the report looks plausible. But the audit check is per line, so it fails anyway. The only fix would be someone keeping the old dict by hand, which is the spreadsheet workaround the ticket is trying to remove.

## Why Candidate A handles it

- The mapping is effective-dated and append-only. Each expense is classified by the mapping that applied on its `spent_on` date.
- After Rhea adds `("VOL-TRAVEL", "Programme delivery", date(2027, 4, 1))`, a re-run of Q3 2026 still gives "Volunteer expenses", and Q1 of 2027/28 gives "Programme delivery". Both match what was actually sent.
- This is not history that nobody uses. The auditor uses it every year.
- The extra cost is small:
  - Rhea adds a row instead of editing one, a few times a year.
  - `line_for` scans a short list. At a few thousand expenses a year, that cost doesn't matter.
- Missing codes are also handled better. A gives a clear `KeyError` that names the code and the date. B gives a bare `KeyError: 'X'`.

## Small notes on A, none of which change the verdict

- If two rows ever share a code and a start date, `max(starts)` would quietly pick the line that sorts last alphabetically. A one-time check for duplicate `(code, start)` pairs would prevent that.
- The scheme only works if old rows are never edited. The comment says so, but a test or a load-time check would enforce it better than a comment.
- Splitting by `spent_on` assumes a correction belongs to the same reporting period as the original expense. That assumption is the same in both designs.

Candidate B's comment says the app should have "one answer for where a code belongs". That is the wrong rule here. Where a code belongs depends on the date, and the audit depends on getting the date right.

WINNER: 1