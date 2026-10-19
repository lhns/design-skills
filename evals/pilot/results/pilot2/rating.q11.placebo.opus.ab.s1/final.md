# Holiday club opening days: Candidate B is the better design

**Candidate B is better.** Both candidates give the same answers for the two confirmed school years. They differ in what they do for dates the council hasn't confirmed yet, and that case happens right now.

## The deciding case: bookings past the confirmed dates

Today is 19 October 2026. The booking page asks for the next twelve months, through about October 2027. That window includes the October 2027 half-term, which belongs to 2027-28. The council won't publish final 2027-28 dates until December, and Nadia says this is exactly when "lots of them book the whole year in one go."

- **Candidate A** works out a 2027-28 October half-term from the usual pattern (the week of 25 Oct 2027) and offers it to parents. If the consultation moves that week, the club has taken bookings for days it can't run. The play workers are teaching assistants who will be at work, and the school hall will be in use. Nadia's rule is "never in term time." Candidate A can break that rule without anyone noticing, and the code gives no sign that the answer is a guess. The council changed two holidays in 2026-27 alone, so the pattern is not reliable enough to sell bookings against.
- **Candidate B** offers no days after 31 Aug 2027 until someone adds the confirmed dates. Parents see a gap, not a wrong date. A missing week is a minor annoyance that can be fixed. A booked week in term time means refunds and upset families.

## Source of truth

The council's published table is the real authority. Candidate B simply copies that table, so checking it means comparing it line by line with the council's page.

Candidate A rebuilds the table from rules (an Easter algorithm, "Monday on or after 19 Dec", and so on) and then needs a `COUNCIL_CHANGES` list wherever the rules got it wrong. So it still needs yearly manual data entry. That data is now spread across rules and exceptions, and it is harder to check than a plain list. All that complexity buys one thing, answers for years nobody has confirmed, and that is the thing we don't want.

## Smaller points

- Candidate A recalculates `holidays()` once for every day in the range. That's cheap, but wasteful.
- In Candidate A, the special case for the summer holiday starting on a Wednesday is an override inside the rules. In Candidate B it is just another row in the list.
- The yearly maintenance is the same for both: add the new year's dates in December.

## Suggested improvement to Candidate B

Make the coverage limit visible instead of silent. Compute the last date in `HOLIDAYS`. Then either have the booking page show a message like "dates after Aug 2027 not yet confirmed by the council," or log a warning when someone asks for dates past that limit. That way nobody mistakes "data not entered yet" for "club closed." A test that fails once the table runs out within twelve months of today would also remind the developer to add the next year.

WINNER: 2