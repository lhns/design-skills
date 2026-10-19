**Design 1 (Candidate A) is the better design.**

## Both are correct

I checked each against the constraints.

**Candidate A**
- It starts the scan one day before entry, so it catches a night band that began the evening before.
- It scans through `exit.date()`, so the band starting at 22:00 on the exit day is included.
- Each band occurrence is clipped to `[entry, exit]`. Because the bands tile the day and all times are whole minutes, every minute is counted exactly once.
- When `exit <= entry`, every overlap is negative, so the price is 0 without a special case.

**Candidate B**
- The five branches of `_same_day_price` cover every way a segment within one day can relate to 06:00 and 22:00.
- The middle days are counted correctly as `(last_midnight - first_midnight).days`.

Correctness doesn't separate them. Constraint 6 does.

## Why A wins

**1. The rules live in one place.** Constraint 6 says the bands change about once a year and may be split or moved. In A, the whole tariff is the `BANDS` table. Adding a reduced evening band from 18:00 to 22:00 is a one-line data edit, and the algorithm stays the same.

In B, the tariff knowledge is spread across:
- the `six` and `ten` locals,
- the case analysis, which assumes exactly two bands with one day band in the middle,
- the hard-coded `16 * 60 * DAY_RATE + 8 * 60 * NIGHT_RATE` full-day constant.

Splitting a band means rewriting the branching. The full-day constant can also silently drift out of sync with the boundaries. That is the DRY hazard of duplicating a business rule.

**2. Fewer paths to get wrong.** A has one uniform loop: each band occurrence overlaps the stay, and the overlap is multiplied by the rate. B has a same-day shortcut, a first-day, middle-days, last-day split, and five cases inside the per-day function. Each is a separate path to test, and its edge cases depend on band boundaries that will move.

**3. The performance difference doesn't matter.** A does about 8 days × 2 bands of work for the longest stay. B's arithmetic shortcut for full days saves almost nothing, and it costs flexibility on exactly the axis we know will change.

## Small improvements to A

- Add an explicit `if exit <= entry: return 0`. A already returns 0 in that case, but only implicitly, and constraint 5 deserves to be stated in the code.
- Add a check, ideally in a test, that `BANDS` tiles 24 hours with no gaps or overlaps. That guards the next council revision.
- Consider renaming the `exit` parameter, since it shadows a builtin.

WINNER: 1