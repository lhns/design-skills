**Design 1 is better.** It states the council's published dates as data. Design 2 predicts dates the council hasn't fixed yet.

**Constraints**
- C1: The club runs on weekdays in the council's school holidays, bank holidays included, and never in term time. Staff and hall are only available in the holidays.
- C2: The council publishes term dates a year at a time and moves them, as with February 2026-27 and summer 2027. Nothing guarantees a pattern.
- C3: Parents book up to 12 months ahead. Many book a whole year in October, so the function is called with ranges that reach past the confirmed data.
- C4: 2027-28 is only proposed until December, so the facts don't exist yet.
- C5 (inferred): Offering a day that turns out to be term time is worse than not yet offering a holiday day. Parents would book a day the club can't staff, whereas a missing day can be added when the council confirms it.

**Trying to break each design**
- **Design 2, C1, C4 and C5:** The booking window moves past October 2026, so it starts including 2027-28 dates the council hasn't confirmed. Design 2 generates Christmas 2027, February 2028 and the rest from rules. If the council shifts any of them, as it just did twice, parents book term-time days.
- **Design 2, C2:** Its rules are a reverse-engineered pattern, and the council has already departed from it. `COUNCIL_CHANGES` is a patch list, which means each year's facts are stated twice, once as the rule and once as the exception. Each new council move adds another exception.
- **Design 2, correctness today:** It agrees with the tables, but only because the overrides were fitted to them. That agreement says nothing about 2027-28.
- **Design 1, C1:** Every date is the council's own. For the confirmed years it is exactly right, and term time is never offered.
- **Design 1, C3:** Beyond the last table entry it returns nothing. That is wrong only in the safe direction (C5). Nothing in the code signals that data is missing, though, so a developer should keep adding years when the council confirms them. The 2027-28 dates are due in December.
- **Design 1, C2:** When the council moves something, you edit one row.

**Counts**
- Design 1 has one concept, a table of the council's holiday periods, plus the weekday filter.
- Design 2 has an Easter algorithm, three date helpers, a rule set and an exceptions table. Facts are stated twice, and none of it is forced by a constraint. Its only advantage, working beyond the data, would be false elegance here. It is the very thing C4 and C5 rule out.

**Deciding reason:** The council's dates are facts that get published and then change, so the elegant representation is the table. Design 2's rules would offer unconfirmed dates and break the "never in term time" constraint.

**Ledger**
- Constraints: C1 to C5 above.
- Forced: holiday dates come from the council's published tables, with a weekday filter.
- Designer choices: none beyond that. Optionally add a guard so that a range past the last confirmed year is flagged rather than silently empty.
- Deletions: the Easter calculation, the date helpers, the rule set and the exceptions table.

WINNER: 1