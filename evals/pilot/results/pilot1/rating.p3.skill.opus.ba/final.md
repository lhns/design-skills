# Design 1 (separate functions) is better

The deciding reason: constraint 4 says the two exports change for different reasons, on different schedules, and a change to one must never alter the other. Design 1 gives each reason its own function. Design 2 joins them through shared lines and a flag.

**Try to break each design against C4.** Suppose the board's next circular asks for columns in the order grade, member id, date, weight.
- **Design 2:** the shared line `row = [d.member_id, date, weight, d.grade]` builds the first four columns of *both* exports. Reordering it for the board silently reorders the statement too. C4 is broken unless you add more `if for_board` branches. A board request for weight in tonnes, or a member request for ISO dates, runs into the same problem: every column is a shared fact that only looks the same.
- **Design 1:** each change touches one function. No input or format change to one export can reach the other's output.

**Check each concept.**
- **The `for_board` flag in Design 2.** No constraint forces it. C5 says each export has exactly one caller, so nothing needs to choose between them at runtime. The flag adds four special-case branches (the reject filter, date, weight, extra columns), and each future difference adds another.
- **Duplication in Design 1.** The repeated sort key `(d.date, d.ticket)` and the loop shape are similar code that changes for different reasons. The board's ordering is set by circular; the statement's is set by the office. Merging them would bind two facts that C4 requires to stay apart. So this is not duplication worth removing.

**Counts (Design 1 vs Design 2):**

| | Design 1 | Design 2 |
|---|---|---|
| Concepts | 2 functions | 1 function + 1 flag |
| Special-case branches | 1 (board skips rejected loads, which C1 forces) | 4 |
| Blast radius of one export's format change | that export only | both exports |

Design 2 is shorter, but only because it weakens C4. That is false elegance.

WINNER: 1