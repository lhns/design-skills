# Design 2 (Candidate A) is better

## Constraints

- **C1.** The report gives totals per reporting line for a quarter, straight from the app.
- **C2.** The mapping changes a few times a year. On 1 April, VOL-TRAVEL and VOL-SUBS move from "Volunteer expenses" to "Programme delivery".
- **C3.** Each June the auditor reruns two of the previous year's quarterly reports from the system. They tick the output line by line against the PDFs already sent.
- **C4.** Expenses are never deleted. Corrections are new rows. (Design 1 holds this, but it doesn't hold the mapping fixed.)

Jonas asked whether old mapping versions need to be kept, and Rhea said "not that I know of". But her own audit comment answers the question. C3 means old reports must be reproducible, and that is the constraint that forces history. History has no user in resubmission, but it has one in the audit.

## Trying to break Design 1

1. In April, Rhea edits `MAPPING` and moves the two VOL codes.
2. In June, the auditor reruns Q3 of the previous year.
3. Every VOL-TRAVEL and VOL-SUBS expense from that quarter now lands under "Programme delivery".
4. "Volunteer expenses" disappears from the output, and "Programme delivery" is inflated by the same amount.
5. Neither line matches the PDF.

This is not a hypothetical edge case. It is what will happen in the first audit after the change the ticket announces. Design 1 is shorter only because it drops C3, which is false elegance.

## Trying to break Design 2

`line_for` resolves each expense against the mapping row in force on its `spent_on` date. Adding the 1 April rows changes nothing for earlier expenses, so prior-year reruns match the PDFs and C3 holds.

The cost is small:
- one extra column (`valid from`);
- one rule: rows are append-only;
- one lookup function.

Each of these traces to C2 plus C3. The `KeyError` covers both an unknown code and a code used before its first row. That is the same failure Design 1 raises for an unknown code, so it is not a new case.

There are minor points, but neither is a flaw in the shape:
- Two rows with the same code and date would be a data-entry error. `max` would silently pick by line name, which a load-time check could catch.
- Keying on the expense date rather than the report period is a designer choice. It is equivalent here because the change falls on a grant-year boundary, which is also a quarter boundary.

## Deciding reason

Design 1 makes the auditor's June rerun of last year's reports disagree with the submitted PDFs as soon as Rhea moves the VOL codes. Design 2's effective-dated mapping keeps every past report reproducible at the cost of one column and one lookup.

WINNER: 2