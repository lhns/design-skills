# Candidate A is the better design

**Deciding reason:** the June audit reruns last year's reports and checks them line by line against the PDFs already sent. That requires the mapping as it stood in the past. Candidate B overwrites the mapping, so it can't reproduce those reports. Candidate A can.

## Constraints

- **C1.** The report gives totals per reporting line, built from tagged expenses (FIN-31).
- **C2.** Codes move between lines over time. VOL-TRAVEL and VOL-SUBS go from "Volunteer expenses" to "Programme delivery" from 1 April.
- **C3.** Each June, the auditor reruns two of the previous year's quarterly reports from the system. They must match the PDFs sent to the trust line by line.
- **C4.** Expenses are never deleted. Corrections are new rows. Volume is small and there is one editor.

## How Candidate B breaks

1. Rhea follows her own plan and edits `MAPPING["VOL-TRAVEL"]` to "Programme delivery" in April.
2. In June, the auditor reruns Q3 of the previous year.
3. Every VOL-TRAVEL and VOL-SUBS expense from that quarter now lands in "Programme delivery".
4. The report has no "Volunteer expenses" row, and "Programme delivery" is higher than on the PDF. The tick-off fails on two lines.

B's comment says the app has "one answer for where a code belongs". That is exactly the wrong invariant here, because where a code belongs depends on the date.

B also rests on Rhea's "not that I know of" answer about history. But that answer is contradicted by her own audit comment. The rule is that only constraints eliminate options, and C3 is a constraint. B drops history to be simpler, which is false elegance.

## Testing Candidate A

- **C2:** A 1 April row for each VOL code makes `line_for` pick the new line for expenses on or after that date, and the old line before it. The trust changes lines by grant year, and dating each mapping row from its start date models that directly.
- **C3:** Rows are never edited or removed. So rerunning any past quarter gives the same mapping, and with C4 the same expenses, so it reproduces the sent report.
- **C1:** An unmapped code raises a clear error rather than silently disappearing.

**Concept count:** A adds exactly one concept, the `valid from` date on each row, and C3 forces it. There are no flags or exception branches. The edit Rhea makes stays the same in shape: she adds a row instead of changing one.

## Minor points about A (not deciding)

- **Same-date ties.** If two rows for one code share a start date, `max(starts)` breaks the tie on the line name. It would be better to reject such duplicates when the mapping is loaded.
- **Late corrections.** A correction row dated inside an already-reported quarter would change a rerun. Both designs share this problem, and it isn't about the mapping.

## Ledger

- **Forced:** a date-effective, append-only mapping (C2 + C3).
- **Designer choice:** effective dates are keyed on the expense's `spent_on` date, not the report period. These give the same result here because quarters sit inside grant years.
- **Deletion rejected:** removing mapping history (Candidate B). It breaks C3.

WINNER: 1