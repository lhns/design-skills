**Constraints**
- C1 (stated): the report comes out of the app, per reporting line.
- C2 (stated): Rhea alone edits the mapping, a few times a year. On 1 April, VOL-TRAVEL and VOL-SUBS move to "Programme delivery".
- C3 (stated, by Rhea): no one resubmits old reports, and no one asked for mapping history.
- C4 (stated, but easy to miss): in June the auditor re-runs two of the previous year's quarterly reports from the system and ticks them line by line against the PDFs sent to the trust.
- C5 (inferred): expenses are never deleted, and corrections are new rows, so the stored data is stable and the system is meant to be reproducible.

**The deciding fork: does a past report need to be reproducible after the mapping changes?**
Rhea says "never resubmit", which answers a different question. C4 says the audit re-runs old quarters, and the output has to match the sent PDFs line by line. Jonas's question was only about history nobody uses. The audit does use it.

**Try to break each design**
- **B:** On 1 April the mapping is edited, so VOL-TRAVEL and VOL-SUBS now map to "Programme delivery". The June audit re-runs a quarter from the previous grant year. "Volunteer expenses" disappears, and its amounts move into "Programme delivery". The report no longer matches the PDF, so C4 fails. The failure is silent and also hits the reporting line the trust is dropping. B's comment says "one answer for where a code belongs", but that is wrong over time, because a code's line is a fact about a date.
- **A:** Re-running a quarter before 1 April gives the old lines, and re-running one after gives the new lines. The mapping is append-only, so the audit reproduces. Rhea's move is a two-row addition. A quarter that straddles a change is also handled, because the lookup uses each expense's own date. An unmapped code raises a `KeyError` in both designs, so neither is silent there.

**Checking how options were rejected**
Dropping history, as B does, was justified by Jonas's "I'd rather not build history nobody uses" and Rhea's "not that I know of". That is a preference, not a constraint, and C4 contradicts its premise. History is not a speculative extra here. It is one extra column in the mapping and one lookup, and a constraint forces it.

**A's cost**
A adds one concept (valid-from date) and a `max` over the matching rows. In exchange it satisfies C4, which B breaks. A caveat: A buckets by `spent_on`, so if the trust's year boundary ever differs from the date an expense was made, the date used would need revisiting. That is a minor point and does not change the ranking.

**Ledger**
- Constraints: C1, C2, C3, C4, C5.
- Forced: the mapping must depend on the expense date, because the June audit re-runs old quarters after the 1 April change.
- Designer choice: append-only rows, with a lookup that takes the latest row at or before the date.
- Deletions: none needed. B's simplification drops C4.

Deciding reason: A reproduces last year's reports after the 1 April remapping, as the audit requires, and B does not.

WINNER: 1