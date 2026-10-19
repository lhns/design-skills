**Constraints.** C1 board: accepted only, 4 columns, ISO date, whole kg. C2 statement: all loads, 7 columns, dd.mm.yyyy, tonnes, running total, `money`. C3 same sort. C4 the two formats change independently, so a change to one must never alter the other. C5 each export has one caller.

**Design 2 (one function with a flag).**
- The flag `for_board` is a concept that exists only to select between two formats. It appears in four branches: filter, date, weight, extra columns.
- Break it against C4: the board adds a column or changes the reject filter, and the edit sits in the same loop as the statement. The `running` variable, `row +=` and shared `row` prefix couple the two outputs. If the board adds a column in the middle, the statement's `row +=` has to be rewritten. The independence C4 asks for holds only by care, not by structure.
- C5 means there is no second caller to benefit from the shared function, so the flag buys nothing.

**Design 1 (two functions).**
- Each function states its format once, and a change to one can't touch the other. C4 holds structurally.
- The only repeated part is the sort key `(d.date, d.ticket)`. That is a real shared fact (C3), stated twice. The two exports are expected to change for different reasons, but the sort could plausibly be a shared rule. A tiny `ordered(deliveries)` helper would state it once, if the cooperative wants sorting to stay in step. As written, the duplication is minor, and it is the only cost.
- Neither function has a branch on which export it is. The only branch is the board's rejected-load filter, which is C1 itself.

**Counts.** Design 2 has one extra concept (the flag), four mode branches, and mixed state (`running` computed only in one mode). Design 1 has none of these, and one duplicated fact (the sort key), which is cheap to fix.

**Why the "shared loop" in Design 2 is false economy.** The shared part is just the iteration and the first column and the grade. That is similar code that changes for different reasons (board circular vs. member requests), not the same fact, so merging it doesn't remove a case. It adds a flag that every future change has to reason about.

**Deciding reason:** C4 requires that changes to one export never alter the other, and only Design 1 guarantees that by structure, while Design 2 couples both formats through a mode flag in a single loop and gains nothing from it given C5.

WINNER: 1