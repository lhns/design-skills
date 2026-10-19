**Design 1 (the explicit lookup table) is the better design.**

**Why the chart is data, not a formula.** The chart was set by hand and is authoritative. Rows get adjusted individually after fitting complaints. A formula only approximates it, so Design 2 has to patch the formula with exception tables. The exceptions are the real chart, with extra machinery around them.

**Design 1**
- Each row is one visible line of data. A fitting complaint means changing one number, and the diff shows exactly that.
- Both directions come from one table, so they cannot disagree. The reverse map is derived.
- Unknown sizes raise `ValueError` in both directions. Lookups of `6` and `6.0` work because `6 == 6.0` and their hashes are equal. The values are exactly representable halves, so float keys are safe.
- It is easy to audit against the published chart, and it is trivially correct.
- One caveat: a duplicate EU value would silently collapse in the reverse map. An assertion `len(EU_TO_UK) == len(UK_TO_EU)` would guard against that. This is a small addition.

**Design 2**
- It has a geometric model (barleycorns, Paris points) that the factory chart doesn't follow. Where the chart deviates, it needs adjustment dicts.
- The adjustments are asymmetric and easy to get wrong. A change to one row may need edits in `UK_TO_EU_ADJUST` and `EU_TO_UK_ADJUST`, and it is not obvious which. The round-trip check `uk_to_eu(uk) != eu` hides mistakes by turning them into errors.
- Moving an EU value by half a size means working out how it relates to the formula's output. The formula's rounding (`_nearest_half`) and the formula constants then determine whether an adjustment is needed at all.
- `eu_to_uk` computes a candidate with floating point and then validates it, which is fragile. Inputs like `39` and `39.0` work, but the logic is hard to reason about.
- Tests would have to verify all 11 rows anyway, so the formula adds nothing.

The formula looks clever but encodes a belief (the chart is derived from geometry) that the constraints say is false. With only 11 rows, a table is simpler, more maintainable, and exactly matches the authority.

WINNER: 1