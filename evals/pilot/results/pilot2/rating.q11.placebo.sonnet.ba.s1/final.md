**Design 1 is better.** The deciding factor is what each one does with dates the council hasn't confirmed.

**Design 1 (explicit table)**
- It encodes exactly what the council has published, and the developer checked it against both confirmed years.
- Beyond the data it returns no days. Booking opens only where dates are confirmed, so the failure is safe: the club shows as closed, nobody pays for a day that doesn't run, and the fix is a short edit once the council publishes in December.
- The council changes dates by consultation, so a table matches how the real rules are made. The comment says how to extend it.
- It is plain and easy to review against the council's page.

**Design 2 (computed pattern plus exceptions)**
- It matches the two confirmed years, but only because `COUNCIL_CHANGES` patches the departures from the pattern. That list shows the pattern is not reliable.
- For 2027-28 it silently invents dates. Those dates are still under consultation until 30 November and could move, and this council has already moved February and summer.
- Parents book a year ahead in October. A wrong guess means families book and pay for days when the club, its staff (TAs who are only free in the holidays) and the school hall are not available. That is a real cost to the charity and to families, and it is hard to undo.
- Adding exceptions later means editing the pattern code and the override keys. The Easter algorithm and the week-offset helpers are also more machinery than the problem needs (YAGNI), and the logic is harder to check against the council's table.
- It also recomputes holidays for every day in the loop, which is wasteful, though minor.

**Caveat on Design 1:** it silently returns nothing for years it has no data for. Ideally it would raise or flag "dates not yet published" for dates past the last table entry, so a forgotten update is noticed. That is a small addition, and it is still a safer default than guessing.

Design 2's cleverness predicts something that is decided by people and still open, and its wrong answers cost real money and trust.

WINNER: 1