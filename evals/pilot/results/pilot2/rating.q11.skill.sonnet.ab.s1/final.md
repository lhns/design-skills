**Design 2 (B) is better.** The deciding constraints are that the club is never open in term time and that the council confirms dates only a year at a time.

**Constraints**
- C1: Open every weekday of the council's school holidays, including bank holidays. This is Nadia's own statement. Easter-based or holiday-based rules are not needed for it.
- C2: Never open in term time. Staff and the hall are unavailable then, so a wrongly offered day is a real failure.
- C3: The council sets the dates, and they move. Both 2026-27 changes were departures from the usual pattern.
- C4: Parents book up to twelve months ahead, many of them all at once in October. Whatever `club_days` says becomes a commitment to parents.
- C5 (reality): Dates are confirmed one year at a time. 2027-28 is still only proposed, with final dates due in December.

**What the data forces**
The council's table is the source of truth for the holiday dates. A's rules are an attempt to predict it. They are only as good as the council's habit of following its pattern, and C3 says that habit already broke twice, so A needs a `COUNCIL_CHANGES` table on top of the rules.

**Trying to break each design**
- **A:** Ask for dates in the 2027-28 year, for example from a window that includes the October 2027 half-term. A invents holiday dates from rules, and the proposed dates may change. If the council moves a week by consultation, A offers term-time days, breaking C2, and parents book them under C4. Nothing in the output says the dates were guessed. A also holds each fact in two places, rule and override, and has Easter arithmetic that serves nothing C1 requires.
- **B:** Ask for dates beyond the last table entry. B returns nothing, so the day is not offered. That is the safe direction for C2 and honest about C5. It does need someone to add each year when the council confirms it. The manual step is forced, because the data only exists then.

**Checking the current window**
Today is 2026-10-19, so the twelve-month window ends 2027-10-19. Everything in it is covered by confirmed data. The summer 2027 holiday ends on 31 August, and September to mid-October 2027 is term time, which both designs treat as closed. B is fully correct for what parents can book now, and its entries match the council's tables exactly. A also agrees on 2025-26 and 2026-27, so it adds no accuracy on confirmed data. Its only extra behaviour is on unconfirmed years, where it risks being wrong.

**Counts**
- A has about 8 concepts: Easter, two Monday helpers, `weeks`, the usual rules, the overrides, the school-year mapping and the lookup. It has several special cases and states each fact twice.
- B has 1 concept, a table of holidays, and no exceptions.

A's extra parts trace to no constraint. They try to cover C5 by guessing, and that guess conflicts with C2 and C4.

**Designer choices and caveats**
- A cheap improvement for B would be to make `club_days` fail loudly, or flag, when the requested range goes past the last confirmed holiday. This is optional. B's quiet "closed" is already the safe default.
- The staleness risk is real: each December the table needs the next year's dates added.

**Ledger**
- Constraints: C1–C5.
- Forced: use the council's published dates as data. Offer only confirmed days.
- Designer choice: the optional guard for the end of data.
- Deletions: Easter calculation, Monday helpers, `weeks`, the pattern rules, the overrides table and the school-year mapping.

WINNER: 2