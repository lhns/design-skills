# Holiday club opening days: Candidate B is the better design

**Candidate B is better.** It stores the council's published table as the single source of truth. Candidate A predicts dates that nobody has confirmed.

## Constraints

- **C1:** The club is open on every weekday of the council's school holidays, bank holidays included, and never in term time. The staff and the hall both depend on this.
- **C2:** The council sets the dates. It publishes them as a table, one school year at a time, after a consultation. The dates can depart from the usual pattern, as in the February 2027 half-term and the Wednesday summer start.
- **C3:** The booking page asks for the next twelve months, and parents book a whole year at once in October.
- **Inferred:** A day must not be offered for booking unless the club will actually run on it. A family that books a day in what turns out to be term time has no childcare.

## Breaking each design

**Today is 19 October 2026.** Under C3, the booking page asks for days up to about 19 October 2027. That range includes the 2027-28 October half-term, and the council has not confirmed those dates. They are still out for consultation until 30 November.

**Candidate A** returns the week of Monday 25 October 2027 with full confidence, because its usual pattern says so.
- If the consultation moves that week, as it moved the February half-term this year, parents will already have booked a term-time week.
- That breaks C1 and the inferred constraint, in exactly the October booking window that C3 describes.
- The code has no way to tell a published date from a guessed one.

**Candidate B** returns nothing for 2027-28 until someone adds the published table in December.
- This fails safe. Some days are offered late, but no day is ever offered wrongly.
- B could be improved by letting the page say "dates for 2027-28 not yet confirmed" instead of showing a blank. That would be an addition at the edge of the system. It needs no change to the core function.

## The concepts in each design

**Candidate A** has these parts:
- a pattern of six rules
- an Easter algorithm
- two "Monday nearest" helpers
- a `COUNCIL_CHANGES` exception table
- a school-year calculation

The exception table is the council's table under another name. Every year someone still has to compare the rules with the published dates and patch any differences. So the facts are kept in two places, and the rules add risk without removing any work. None of these concepts is forced by a constraint, because C2 says the dates are published, not derived.

**Candidate B** has two parts:
- one list of published facts
- one weekday filter

Each part traces to a constraint: C2 and C1. Adding a year is one transcription from the source the developer already checks against.

## Ledger

- **Forced:** Holidays are data copied from the council's table, because of C2. Unconfirmed years must not produce bookable days, because of C1, C3 and the inferred constraint.
- **Deleted:** The pattern rules, the Easter calculation, the Monday helpers and the exception table.
- **Designer choice:** Showing "not yet confirmed" for years that are not in the table.

**Deciding reason:** A invents dates for the October 2027 half-term that the council has not yet fixed, and parents booking this month would act on them. B offers only dates the council has published, using fewer concepts.

WINNER: 2