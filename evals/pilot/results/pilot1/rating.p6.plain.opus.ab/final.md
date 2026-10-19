**Design 1 is better.** Both are correct for today's bands, but only Design 1 survives the yearly band revisions (constraint 6) without rewriting logic.

**Correctness**
- **Design 1:** For each calendar day from the day before entry through the exit day, it intersects each band with `[entry, exit)` and charges the overlapping minutes.
  - Starting one day early catches a night band that began the evening before entry.
  - Multi-day stays and repeated midnight crossings are handled.
  - When `exit <= entry`, every overlap is zero or negative, so it returns 0 without a special case.
  - Durations are whole minutes, so `// 60` is exact.
  - Looping over at most 8 days is trivially cheap.
- **Design 2:** It also prices correctly. It splits the stay into a first partial day, some whole days and a last partial day. A five-way case analysis covers 06:00 and 22:00, and the whole-day price is a closed-form constant.

**Maintainability (constraint 6)**
- **Design 1:** The bands are data. Splitting the day band, moving 22:00 to 23:00, or adding a third band just means editing `BANDS`. The algorithm does not change because it never assumes how many bands there are or where they fall. The only invariant is that the bands tile the day, and the comment states it.
- **Design 2:** The band structure is spread across code:
  - the `six`/`ten` anchors;
  - five branches that assume exactly one day band between two night segments;
  - the constant `16 * 60 * DAY_RATE + 8 * 60 * NIGHT_RATE`.
  
  Splitting a band would mean rewriting `_same_day_price`'s branches and recomputing the full-day constant by hand. That is easy to get subtly wrong, and the council will force it about once a year.

**Readability:** Design 1 has a single rule: overlap × rate, summed. Design 2 makes the reader check five branches and their boundary conditions (`<` vs `<=`) to trust it.

WINNER: 1