**Design 1 (the lookup table) is the better design.**

**Why the table wins**

- **The chart is authoritative data, not a formula.** The factory set it by hand, and it is the source of truth. Design 1 states it once, in the same shape as the published chart, so anyone can check it against the source by eye.
- **Correctness is easy to see.** Both directions match the chart by construction. `EU_TO_UK` is derived from `UK_TO_EU`, so the two directions cannot drift apart. Unknown sizes raise `ValueError` automatically, because they are not keys.
- **It fits how the chart changes.** Rows are adjusted individually, by moving one EU value by half a size. In Design 1 that is a one-number edit in one place. The reverse direction updates itself.
- **Numeric input works.** In Python, `6 == 6.0` and they hash equally, so `6`, `6.0` and `6.5` all look up correctly.
- **It is simple.** About 15 lines with no arithmetic and nothing to misread.

**Why Design 2 loses**

- **It models the wrong thing.** It reconstructs the chart from a geometric formula (barleycorns and Paris points), then patches the places where the factory disagrees with it. The chart is the truth. The formula is only an approximation of it, and it forces the maintainer to understand both.
- **Adjustments become awkward.** A one-row change means working out the formula's output for that size and writing a correction. The corrections for the two directions are separate dictionaries (`UK_TO_EU_ADJUST` and `EU_TO_UK_ADJUST`), and they must be kept consistent by hand. A single fitting adjustment can require edits in both, and forgetting one gives silently wrong results. The current `{39: +0.5}` entry exists only to undo the effect of the `6: -0.5` entry on the reverse path.
- **The reverse path is fragile.** It guesses a UK size by rounding, patches it, and then validates by round-tripping through `uk_to_eu`. This is hard to reason about. For example, `eu_to_uk` does floating-point arithmetic on arbitrary input before validating, and the correctness of the whole scheme depends on rounding behaving as hoped.
- **Floating-point arithmetic adds risk** where exact lookups would have none.
- **It is over-engineered.** It adds constants, helper functions and correction tables to compute 11 values that could simply be listed. This is speculative generality: there is no requirement to support sizes beyond the chart.

**A minor note on Design 1**

Its keys are floats, which is fine here because the values (`3.5`, `37.5` and so on) are exactly representable in binary. If the chart ever gained a non-half-size value, that would be worth revisiting. Adding a test that round-trips every row would also be cheap insurance. Neither is a reason to prefer Design 2.

WINNER: 1