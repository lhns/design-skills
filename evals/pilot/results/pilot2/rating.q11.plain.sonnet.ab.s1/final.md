**Design 2 (Candidate B) is the better design.**

**The deciding fact is that the 2027-28 dates are only proposed.** Both candidates agree on every confirmed date for 2025-26 and 2026-27, so they differ only on what happens beyond the council's published data.

- **Candidate A** extrapolates from rules such as "Monday on or after 15 Feb" and "Easter minus 6 days". It presents those guesses as the club's opening days.
- **The council moves dates often.** Nadia says the 2026-27 February half-term shifted a week and the summer start moved to a Wednesday. A's `COUNCIL_CHANGES` dict is itself evidence that the rules have already been wrong twice.
- **A wrong guess is costly.** Parents book up to twelve months ahead, and many book the whole year at once. A date that A wrongly offers means a family pays for childcare that doesn't exist. The staff are only free in the holidays and the hall belongs to the school, so the club can't simply open on the day.
- **A's mistakes would be invisible.** The output looks authoritative, and nothing flags which dates are predictions.
- **Candidate B only reports confirmed dates.** For unpublished periods it offers nothing. That is a visible gap that can be fixed, and it can't cause a wrongly sold booking.

**B is also simpler.** It is a data table that can be checked line by line against the council's page. A adds an Easter algorithm, weekday arithmetic, and an exceptions dictionary, which is much more to get wrong and review. It buys nothing for the confirmed years, where the developer has already checked that the two agree.

**B has a weakness that should be fixed.** Today the twelve-month window runs to about October 2027, and all of it is covered by confirmed data. As the window rolls forward it will reach the proposed 2027-28 dates (the October 2027 half-term and later). B will then return nothing for them without saying so, and someone has to remember to add the final dates in December.

I'd keep B and make that gap explicit. For example, have `club_days` raise or report "dates not yet published" when the range goes past the last confirmed holiday, so the booking page can say so instead of showing an empty calendar. A reminder to add 2027-28 once the council publishes in December would also help.

WINNER: 2