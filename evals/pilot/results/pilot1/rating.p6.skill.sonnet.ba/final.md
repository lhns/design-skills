**Design 2 is better.** Constraint 6 decides it: the council revises the bands about once a year, and a band may be split or moved.

**Correctness today.** Both designs satisfy constraints 1-5. Here is how I checked that, including attempts to break each one.

- **Design 2:**
  - The loop starts at the day before entry so a night band that began the previous evening is counted.
  - Bands that start after exit give a negative overlap and are skipped.
  - If exit is not after entry, no overlap is positive, so the price is 0.
  - Whole-minute inputs make the floor division exact.
  - A 7-day stay needs about 9 iterations, which is trivial.
- **Design 1:** I could not find a failing input. Its same-day branches cover every case, and the first partial day, the whole days in between and the last partial day are handled correctly.

**Cost of the yearly revision (C6).**
- **Design 1** encodes the band structure in several places:
  - the literals `6` and `22`;
  - the five-branch case analysis in `_same_day_price`, which assumes exactly one day band inside one night band;
  - the full-day constant `16*60*DAY_RATE + 8*60*NIGHT_RATE`, which states the band lengths a second time;
  - the day/night rates, which exist as named constants separate from the boundaries.

  Splitting a band, such as adding an evening peak, means rewriting the branch logic and the full-day constant. Forgetting the constant gives silently wrong prices for long stays. The count of special-case branches and duplicated facts is high, and a single constraint change touches most of the code.
- **Design 2** expresses the bands as data in one table. A split or move is a one-row edit, and the algorithm is untouched. The bands are the only place that holds boundaries and rates. The single shared concept is "overlap of the stay with each band occurrence, times its rate", and this deletes the case analysis and the full-day constant.

**Remaining caveat for Design 2.** It assumes the bands tile the day without gaps or overlaps. Nothing checks this, so a bad table would misprice silently. A one-line assertion over the table could enforce it, and it would be a small addition next to Design 1's duplicated facts.

**Deciding reason:** both are correct today, but Design 2 keeps C6 with one data table and no branches, while Design 1 hardcodes the band structure in branches and a derived constant that must all be rewritten when the bands change.

WINNER: 2