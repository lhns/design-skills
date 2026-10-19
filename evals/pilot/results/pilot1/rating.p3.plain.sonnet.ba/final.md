**Design 1 is better.**

The key constraint is #4: the two exports change for different reasons and on different schedules (the board's yearly circular vs. the office's ad hoc member requests), and a change to one must never alter the other. That is the textbook case for separate functions, because the two exports have different reasons to change.

**Design 1 (separate functions)**
- Each function is owned by one stakeholder. Editing the statement's date format, adding a column, or changing the running total cannot touch the board report's code path, so the isolation requirement is met structurally rather than by careful editing.
- Each function reads top to bottom with no branching on a mode flag. The docstrings document who defines the format.
- The duplicated pieces are small: the sort key and the loop skeleton. That duplication is incidental, not a shared business rule. The two exports share a sort order today, but constraint 3 doesn't say the board and the office must stay in lockstep. If the board's circular demanded a different order, the functions could diverge independently, which is exactly what you want. Extracting a shared helper would couple them again for little gain.

**Design 2 (one function with a `for_board` flag)**
- Every difference is a conditional on `for_board`, so the function is really two exports interleaved. Any change to either format means editing a function that also produces the other, so a mistake can silently alter the other output. That directly violates constraint 4.
- There are subtle coupling hazards: `running` is computed only on the statement path, and the `continue` for rejected loads sits before the running total update. The ordering is correct today, but someone adding a column or filter for one export can easily break the other.
- Constraint 5 (each export called from exactly one place) means there's no call-site reuse that a unified function would benefit from. A flag parameter buys nothing here and costs clarity. Boolean flag arguments also make call sites less readable (`export_rows(ds, True)`).
- The "reduces duplication" benefit is illusory: it merges code that only coincidentally looks similar.

Design 1 is more cohesive per function, has lower coupling between exports, and makes the expected changes local and safe. Design 2 trades that for a few saved lines.

WINNER: 1