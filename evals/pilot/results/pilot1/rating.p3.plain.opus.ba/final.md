**Design 1 is better.**

The deciding constraint is #4. The two exports have different owners (the regional board versus the cooperative office) and change on different schedules, and a change to one must never affect the other. They share some code today, but that is coincidence. It is not a shared rule.

**Design 1 (separate `board_rows` / `statement_rows`)**
- Each function belongs to one owner. When the board issues a circular, you edit `board_rows` and nothing else. The statement code is never touched, so it cannot regress.
- The duplicated parts (the sort key and the first four columns) look shared but aren't. If the board later wants sorting by member id, or the office wants weight in kg, each change stays local.
- Each function is called from exactly one place (constraint #5), so a separate entry point per caller costs nothing extra.
- Each function reads straight through with no branching. It is easy to check against its spec, and its docstring names the authority that defines its format.

**Design 2 (`export_rows(deliveries, for_board)`)**
- The boolean flag argument joins two unrelated specs into one function. Every line runs for both exports. Any edit made for the board, such as changing the date format, reordering columns, or adding a column, is mixed in with statement logic, and a mistake can silently change the member statement. That breaks constraint #4.
- The column layout is spread across conditionals. Neither export's format can be read in one place.
- The shared parts will drift apart over time, and each divergence adds another `if for_board` branch. The function only gets harder to change safely.
- Its small reduction in duplication saves almost nothing, because the duplicated code is a sort key and a few columns.

Merging these would only make sense if both exports were bound by a single rule, for example a legal requirement that both use the same ordering. Then the shared piece could be factored into a named helper. Nothing in the constraints describes such a rule.

WINNER: 1