# Design 2 (Candidate A) is the better design

**Deciding reason:** both designs price correctly, but Design 2 keeps the band definition in one table that the algorithm reads. Design 1 encodes the bands in its branch structure, so the yearly revision (C6) means rewriting the code.

## Trying to break each design

| Constraint | Design 1 | Design 2 |
|---|---|---|
| C1, C2: per-minute rate by band | Correct. I checked all five branches of `_same_day_price`, including a start before 06:00 with an end after 22:00. | Correct. The bands tile the day, so their overlaps are disjoint and each minute is counted exactly once. |
| C3: up to 7 days, many midnights | Correct. It splits the stay into a first partial day, whole days and a last partial day. | Correct. The loop covers each day from `entry.date()-1` (for the night band that began the evening before entry) through `exit.date()`. That is at most about 9 days × 2 bands. |
| C4: whole minutes, naive datetimes | Correct. | Correct. The overlaps are whole minutes, so the `// 60` truncation loses nothing. |
| C5: exit ≤ entry gives 0 | Needs an explicit guard branch. | Follows with no branch: every overlap is ≤ 0, so the total stays 0. |
| C6: bands revised yearly, split or moved | **Breaks structurally.** 06:00 and 22:00 are written into `six`/`ten` and into five case branches. The full-day formula `16*60*DAY_RATE + 8*60*NIGHT_RATE` states the same band facts again, and the comments state them a third time. Splitting the night band, say into a cheaper 00:00–06:00 band, means redesigning the case analysis and keeping three copies consistent by hand. | Edit the `BANDS` table. Wrapping bands are handled by `end <= start`, and a split such as (22:00–00:00) and (00:00–06:00) works unchanged. |

## Counting concepts

- **Design 1:** two rate constants, two hard-coded boundaries, five special-case branches, a same-day/multi-day split, a midnight-alignment step, a derived full-day constant and a C5 guard. The band layout is stated in about three places.
- **Design 2:** one concept, a table of bands, plus one rule: price = Σ overlap(band occurrence, stay) × rate. It has no exception clauses, and each fact is stated once. The only odd detail, starting the loop at `entry.date()-1`, is forced by bands that wrap past midnight, and the code comments it.

## Rejected options

Design 2 does not drop Design 1's whole-day shortcut for simplicity's sake. C3 bounds a stay at 7 days, so iterating over the days costs nothing, and the shortcut serves no constraint. Its only effect is to duplicate the band facts.

## Invariant

Design 2 keeps one invariant: the bands tile the 24-hour day. While that holds, every minute of a stay falls into exactly one band occurrence. Design 1 relies on the same fact without stating it, spread across its branches.

WINNER: 2