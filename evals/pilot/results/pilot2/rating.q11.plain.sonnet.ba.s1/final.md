**Design 1 is the better design.**

**The main issue is the 2027-28 year.** Today is 19 October 2026 and the booking page asks for the next twelve months, so the window runs to October 2027. That reaches into 2027-28, and the council has only *proposed* those dates, with final dates due in December. Parents will book the whole year this month.

- **Design 1** returns nothing after 31 August 2027, so the October 2027 half-term simply isn't offered yet. That costs some lost or delayed bookings. The fix is to add the dates in December, which its comment already says to do.
- **Design 2** extrapolates a formula into 2027-28 and presents the result as fact. The manager says the council does move things, and in 2026-27 it moved both February half-term and the summer start. Design 2 had to be patched with `COUNCIL_CHANGES` to match those two years, so its "usual pattern" was fitted to the known data and isn't a rule the council follows. If the formula is wrong for October 2027, parents book and pay for days when the club can't open, because the staff are in school and the hall is in use. That means cancellations, refunds and upset families.

The two designs fail differently. Design 1 under-offers days, which is safe and easy to correct. Design 2 over-offers unconfirmed days, which does harm.

**Other points**
- Design 1 is plain data that can be checked line by line against the council's table. Design 2 needs an Easter algorithm and several date helpers to produce what a table states directly.
- The developer's check that both agree on 2025-26 and 2026-27 says nothing about Design 2's predictive power, since the exceptions were added to make them agree.
- Design 2 also recomputes the holidays for every day in the loop, which is wasteful.

**Improvement for Design 1.** It should not stay silent beyond its data. Ideally `club_days` would raise an error or flag the dates after the last confirmed holiday, so the booking page can show "dates to be confirmed" instead of an apparently closed club. The data table, not a formula, is still the right design.

WINNER: 1