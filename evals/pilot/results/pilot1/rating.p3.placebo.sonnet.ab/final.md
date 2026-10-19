**Candidate B (two separate functions) is the better design.**

**Why A is weaker**

- `for_board` is a boolean flag that switches behavior. Nearly every line branches on it, so the function is really two exports interleaved. The shared part is only the sort key and the loop skeleton.
- It violates constraint 4. The board and the cooperative office change the formats for different reasons and on different schedules. Both changes would edit the same function. A tweak to the statement's date format, for example, sits one ternary away from the board's, and a slip in an edit can alter the other export. The only protection is careful editing.
- `running` is computed in the loop for both modes, even though only the statement uses it. Mixed concerns in one loop body make the code harder to follow, and each new column or rule adds another `if for_board` branch.
- The call sites (`export_rows(ds, True)`) are cryptic, and constraint 5 means there is no reuse to justify the shared entry point.

**Why B is better**

- Each function has a single reason to change: the board's circular for `board_rows`, the office's requests for `statement_rows`. Changes cannot leak from one export to the other, which is exactly what constraint 4 demands.
- Each function reads top to bottom with no branching on mode. The docstrings state the column spec and name the owner of the format.
- The names say what they produce, and call sites are self-explanatory.

**The duplication in B**

The duplicated `sorted(..., key=(date, ticket))` is real, but it is small and incidental. Each export is called from one place, so there is no second consumer to benefit from sharing. Duplication is cheaper than coupling here. If the sort order is ever considered a single business rule that must stay in sync, a tiny `in_delivery_order(deliveries)` helper would be a reasonable extraction. It would not need a mode flag, and it is not required now. Even with this minor repetition, B better respects the stated independence requirement.

WINNER: 2