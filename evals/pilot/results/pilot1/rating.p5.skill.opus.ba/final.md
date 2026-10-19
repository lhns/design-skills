# Design 1 (Candidate B) is better

The deciding constraint is C4. The chart was set by hand and is corrected one row at a time, so it is an irregular domain, and the right representation for an irregular domain is the table itself.

## Trying to break each design

**Design 1.**
- **C1 (chart matches exactly):** the chart is stored once, in `UK_TO_EU`. The inverse is derived from it. The 11 EU values are distinct, so the inverse loses nothing.
- **C2 (unknown size raises `ValueError`):** every lookup miss raises `ValueError`, in both directions.
- **C3 (sizes arrive as numbers):** in Python, `6 == 6.0` and their hashes are equal, so `6`, `6.0` and `6.5` all find their keys. All the sizes are halves, which floats represent exactly, so lookups are reliable.
- **C4 (rows change one at a time):** a correction is a one-cell edit, and the reverse direction follows automatically.
- **One gap:** if a future edit gave two UK sizes the same EU value, the comprehension would silently drop one of them. A one-line `assert len(EU_TO_UK) == len(UK_TO_EU)` closes that gap.

**Design 2.**
- **C1:** I worked through all 11 rows by hand and they currently come out right. For example, UK 6 gives 39.37, which rounds to 39.5, and the −0.5 adjustment brings it to 39.
- **C1 and C4 together:** correctness depends on a geometric model that the factory doesn't use, plus two exception tables.
- **The adjustment tables state one fact twice.** UK 6 ↔ EU 39 appears as `UK_TO_EU_ADJUST[6]` and again as `EU_TO_UK_ADJUST[39]`.
- **The two tables are already asymmetric.** Getting 7.5 ↔ 41 right in reverse depends on rounding happening to work out, not on an entry.
- **A C4 change breaks it easily.** Suppose the factory moves UK 6.5 to EU 39.5. You now have to:
  - work out the departure from the geometric value;
  - add a forward entry;
  - work out whether the reverse rounding needs its own entry.

  Forgetting the reverse entry gives you a reverse lookup that raises `ValueError` on a valid size, which breaks C1. Every complaint fix becomes a small piece of numerical analysis.
- **Rounding is fragile.** Values such as `40.005` sit right next to the rounding boundaries, so a tweak to a constant could flip a row.

## Counting concepts

| | Design 1 | Design 2 |
| --- | --- | --- |
| Concepts | 1 table and its derived inverse | 3 physical constants, a size list, a rounding rule, a length function, 2 adjustment tables |
| Facts stated twice | 0 | 2 (each adjustment pair; the size list repeats the chart's keys) |
| Exception clauses | 0 | 3 adjustment entries, plus the round-trip check in `eu_to_uk` |
| Unforced numbers | 0 | `UK_ZERO_OFFSET` and the step sizes. They are real standards, but no constraint asks for them. |

The barleycorn model looks principled, but it removes no cases. The chart departs from the model, so the cases come back as adjustment tables, and they have to be maintained in both directions.

**Deciding reason:** the chart is authoritative and corrected row by row (C1, C4), so a single table that states each fact once and derives the inverse is the only representation in which a fitting fix is a one-cell edit that cannot desynchronise the two directions.

WINNER: 1