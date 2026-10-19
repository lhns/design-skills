**Design 1 (Candidate B) is better.**

**The deciding factor is the window being booked.** Today is 19 October 2026, and the booking page asks for the next twelve months, up to October 2027. That reaches into the 2027-28 school year (the October 2027 half-term). The council's proposed 2027-28 dates are still out for consultation, and the final dates come in December. So the two designs differ on exactly the dates nobody knows yet:

- **Candidate A** guesses those dates from a pattern, and parents can book them now. If the consultation moves the October 2027 half-term, as the council did with February 2026-27, families will have paid for days when the club can't open. There would be no hall and no play workers, because the teaching assistants are back in school. Nadia's one firm rule is "never in term time", and A can break it silently.
- **Candidate B** offers nothing beyond the confirmed tables. Its failure mode is safe: some days aren't bookable until December. Fixing that is a six-line data edit copied from the council's table.

**Design reasons that support the same choice:**

- **Source of truth.** The council publishes a table, not a rule. B mirrors that table directly. A turns two years of observations into an algorithm (Easter computation, "Monday on or after 19 Dec", and so on), then patches it with `COUNCIL_CHANGES` wherever reality differs. A third of its known holidays are already exceptions. The real data goes in as overrides to a guessed model, so every new year means checking the prediction against the table anyway.
- **Simplicity and reviewability.** A volunteer can check B against the council's page line by line. A needs someone to understand the Easter algorithm and the half-term heuristics to confirm a date is right.
- **Hidden fragility in A.** A will answer for any year at all, for example 2031, with confidence it hasn't earned. It also recomputes the whole holiday list for every day in the range. That costs little, but it's needless work.

**Suggested improvement to B.** At present B treats "not yet published" and "term time" the same way: both return no days. It should expose the last covered date, for example `max(b for _, b in HOLIDAYS)`. Then the booking page can say "dates from September 2027 open once the council confirms them in December" instead of looking like the club is closed. It would also help to sort or validate `HOLIDAYS` so that typos such as overlapping or reversed ranges fail loudly.

WINNER: 1