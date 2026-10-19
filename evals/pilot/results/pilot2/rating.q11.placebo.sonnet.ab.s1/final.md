**Candidate B (a table of the council's published dates) is the better design.**

**The dates are published data, not a rule.** The council sets term dates after consultation, and Nadia says it moves things: the February half-term shifted for 2026-27, and next summer starts on a Wednesday. Candidate A models the pattern as formulas (Easter calculation, "Monday on or after 15 Feb") and then patches the exceptions into `COUNCIL_CHANGES`. That is a table with extra machinery around it. Its agreement with the council's tables for 2025-26 and 2026-27 only shows the formulas can reproduce known years, not that they predict unknown ones.

**A turns guesses into bookings.** Today is 19 October 2026, and the booking page looks 12 months ahead. Within days, that window will include 2027-28 holidays. The council has only *proposed* those dates, and they are under consultation until 30 November. A will generate plausible but unconfirmed dates and show them to parents as open. Parents book the whole year in October, so a wrong guess means families paying for days when the club isn't running. The play workers are council teaching assistants and the hall is the school's, so the club can't simply open on days the council moved. The cost of a wrong date is high and lands on parents and the charity.

**B only claims what is confirmed.** Every date in it comes from the council's tables. Updating it is a small, reviewable edit each December: add the table, check it against the council page.

**B's weakness:**
- Past 31 August 2027 it silently returns no club days. That is safe, since nothing gets falsely offered, but it looks identical to "closed".
- Before the page's window reaches 2027-28 holidays (late October), I'd add a guard. For example, define a `CONFIRMED_THROUGH` date and raise or return a distinct "not yet published" signal if `last` goes beyond it, so the booking page can say "dates for autumn 2027 will be released in December".
- That is a small addition, and it keeps the honest behaviour that A lacks.

**Clean-code view:**
- A has more moving parts (`easter`, three date helpers, `weeks`, an exceptions map, a per-day year calculation) to produce what B states directly. That is complexity that doesn't earn its place (KISS).
- A also splits knowledge between formulas and exceptions, so a reader must mentally combine them to know the real date.
- B has a single authoritative home for the dates, and its comment says how to maintain it.

WINNER: 2