# Holiday club opening days: Design 1 (Candidate B) is the better design

**Constraints**
- **C1:** The club opens exactly on the weekdays of the council's holidays and never in term time. The staff and the hall are only available then.
- **C2:** The council decides those dates. It publishes them a year at a time, after consultation, and it does break its own pattern (the 2026-27 February half-term and the Wednesday summer start).
- **C3:** Parents can book up to twelve months ahead. Many book the whole year in October.
- **C4 (from the dates):** Today is 19 October 2026 and 2027-28 is unconfirmed until December. Any call made from about late October onward reaches into 2027-28. For example, a booking on 1 November 2026 covers the October 2027 half-term.

**Trying to break each design**
- **Candidate A on unconfirmed dates:** for 2027-28 it returns dates it *predicts*. Suppose the council's December decision differs from the rule, which C2 says happens most years in some way. Parents will already have booked and paid for days that turn out to be term time. Staff are working in schools on those days and the hall is in use. That breaks C1, and it happens during exactly the October rush that C3 describes. The predictions are also invisible: the function looks equally sure about a guessed day and a confirmed one.
- **Candidate A on confirmed years:** it is right only because `COUNCIL_CHANGES` patches it. Every confirmed year can still need a code change. So A keeps a table anyway and adds a generating rule underneath it. The rule was fitted to two years of data, and two cases are not a pattern. The holiday dates now live in two places, the rule and the overrides, and the overrides only make sense relative to the rule.
- **Candidate B:** I can't find an input that makes it open on a term-time day. For 2027-28 it returns nothing until someone adds the confirmed rows. That is the truthful answer: the club's opening days are not knowable yet.

**How each design rejects the other option**
- A rejects a plain table only for convenience (less to type each year). No constraint asks for that.
- B rejects prediction because of C1 and C2. The council, not an algorithm, is the source of truth.

**Concept counts**
- **A:** Easter algorithm, two Monday helpers, `weeks`, the usual rule, the override map and a school-year derivation. That is seven concepts against B's one.
- **B:** one table that mirrors the council's published table, plus a weekday filter.

The domain is irregular because a committee sets it (C2), so a table is the right representation.

**Where B could improve**
B can't tell "closed" apart from "not yet published". The booking page should show the second as "dates not confirmed yet", for instance by exposing the last confirmed date. That fix belongs at the edge. It does not justify inventing dates.

**Deciding reason:** Candidate A lets parents book term-time days the club can't staff, whenever the council departs from a pattern it has already broken twice. Candidate B can only ever offer days the council has confirmed.

WINNER: 1