**Candidate B (Design 2) is better.**

The two exports change for different reasons and on different schedules: the board by annual circular, the statement whenever members ask. Constraint 4 says a change to one must never alter the other's output.

**Candidate A** couples them through a `for_board` flag. Every line that differs is a branch on that flag, so the function is really two exports interleaved. This causes several problems:
- Any edit to the shared function, even one aimed at the statement, puts the board output at risk. Nothing in the structure prevents an accidental change to the board report.
- Each new statement column or board format change adds more flag conditionals, and the function grows harder to read.
- The shared pieces are small: the sort and the loop. They are not worth coupling the exports for.
- Constraint 5 says each export is called from exactly one place. That removes the usual argument for a shared, parameterized function, because there is no set of callers that benefits from one entry point. A boolean parameter that every caller passes as a constant is a sign the function should be split.

**Candidate B** gives each export its own function containing its own filter, formatting, and columns. A circular only touches `board_rows`, and a member request only touches `statement_rows`. The only duplication is the sort key `(d.date, d.ticket)` and the loop skeleton, which is one line and trivial. If someone later changed the sort in one, that would be a deliberate and visible edit, and constraint 4 explicitly permits the exports to diverge. Each function is also short, readable top to bottom, and documents its own format.

The duplication in B is incidental, while A's coupling is a real maintenance risk. B respects the stated requirement that the exports evolve independently.

WINNER: 2