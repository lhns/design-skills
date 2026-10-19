**Constraints**
- C1: both directions match the chart exactly.
- C2: off-chart sizes raise `ValueError` in either direction.
- C3: inputs are numbers (`6`, `6.0`, `6.5`).
- C4: the chart is hand-set and rows are edited individually, each edit moving one EU value by half a size.

**Design 1** is a table plus its derived inverse. The chart is stated once, and `EU_TO_UK` is computed from it, so no fact is stated twice.
- C1 holds by construction, because the data is the chart.
- C2 holds because a missing key raises `KeyError`, which is converted to `ValueError`.
- C3 holds because `6 == 6.0` and `hash(6) == hash(6.0)`, so dictionary lookup treats them as the same key.
- C4: an edit is one number in one row, and the inverse follows automatically. The inverse also stays correct only while EU values are unique. A duplicate would silently drop a row, but a hand-set chart of one shoe has no duplicates, and the chart is authoritative.

**Design 2** derives the chart from a geometric formula (barleycorn, Paris point) and then patches the differences with two adjustment tables.
- The chart is now spread over three places: the formula, `UK_TO_EU_ADJUST` and `EU_TO_UK_ADJUST`. The adjustments are stated twice in opposite directions. For example, UK 6 → EU 39 is patched forward by `-0.5`, and EU 39 → UK 6 is patched back by `+0.5`.
- C4 breaks the design. Moving one EU value means editing `UK_TO_EU_ADJUST` and also working out the matching inverse entry in `EU_TO_UK_ADJUST`. The inverse entry depends on what the formula returns for that EU value, which is not obvious. Forgetting it breaks C1 in one direction.
- The `eu_to_uk` round-trip check (`uk_to_eu(uk) != eu`) exists only to catch the formula's wrong answers. It is an exception clause that compensates for the derivation.
- Float rounding (`2.54 / 3`, and `floor` on products) means a correct result depends on the arithmetic landing safely away from a rounding boundary. A tie is not guaranteed to resolve the same way after an edit.
- C3: `uk not in UK_SIZES` works with `6.0`. The `eu` side relies on float arithmetic.
- A break to test: edit UK 4.5 from 37.5 to 38. In Design 2 you must add a forward adjustment, add a reverse one, and also check that 38 doesn't collide with UK 5. In Design 1 you change one number, and a duplicate would be visible in the same table.

Design 2 also states a premise the constraints deny. C4 says the chart was set by hand and is not a formula. The formula is a model of it, and the two adjustments are the places where the model fails. If the chart changes again, the model will need more patches. The `UK_SIZES` list is also a second copy of the chart's keys.

**Counts**
- Concepts: Design 1 has one (the table) plus a derived inverse. Design 2 has the formula, 3 constants, the size list, 2 adjustment tables and the round-trip check.
- Facts stated twice: Design 1 has none. Design 2 has the chart's keys in `UK_SIZES` and in the formula, and each adjustment in both directions.
- Exception clauses: Design 1 has none. Design 2 has two adjustment tables and the verification guard.

**Deciding reason:** the chart is authoritative, hand-edited data, so the table is the single source of truth and the derived inverse keeps both directions consistent. Design 2 reconstructs the data through a formula that needs patches in both directions.

WINNER: 1