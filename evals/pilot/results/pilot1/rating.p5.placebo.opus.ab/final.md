**Design 2 is better.**

**The chart is the specification, and B stores it as data.** Constraint 1 says the factory chart is authoritative. B's `UK_TO_EU` dict is that chart, row for row, so anyone can check it against the factory sheet by eye. A derives the values from barleycorn and Paris-point geometry, then patches the cases where the factory differs. To confirm A matches the chart, you have to compute all eleven rows by hand, with floating-point rounding involved.

**Constraint 4 decides it.** Rows change one at a time after fitting complaints. That has happened twice in three years.
- **In B**, an adjustment is a one-number edit in one place. The inverse map is derived automatically, so the two directions cannot drift apart.
- **In A**, the same edit means working out what the geometric formula yields, writing the difference into `UK_TO_EU_ADJUST`, and then checking whether `EU_TO_UK_ADJUST` also needs an entry. Whether it does depends on how the reverse formula happens to round. The two adjustment tables hold the same knowledge, so A breaks DRY, and they are exactly the copies that drift. A's round-trip check in `eu_to_uk` catches some mistakes, but only at runtime, and only as a `ValueError` for a size that should be valid.

**The model in A is false for this problem.** The comment "where the factory's grading departs from the geometric conversion" admits the chart is not geometric. The constants (`BARLEYCORN_CM`, `UK_ZERO_OFFSET`, `PARIS_POINT_CM`) suggest a general rule that the business does not follow. That is speculative generality: complexity that buys nothing for one last and eleven sizes, and that misleads the next maintainer.

**Both designs meet constraints 2 and 3, but B does it more simply.** In Python, `6 == 6.0` and the two hash the same, so dict lookup accepts `6`, `6.0` and `6.5` alike. B rejects anything off the chart with a clear `ValueError` in both directions, using plain lookup. A relies on `in` against a list plus float arithmetic and `_nearest_half` rounding, which is harder to reason about at the boundaries.

**Possible improvement to B:** add a check at import time that the EU values are unique, for example `assert len(EU_TO_UK) == len(UK_TO_EU)`. A future hand edit could give two UK sizes the same EU value, and then the inverse map would silently drop one of them. Add a table-driven test that lists the chart once.

WINNER: 2