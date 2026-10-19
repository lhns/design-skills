# Holiday club opening days: Candidate B (Design 1) is the better design

**What the decision turns on: dates nobody knows yet.** Both candidates agree on every date in 2025-26 and 2026-27, so they differ only where the booking window goes past the confirmed tables. The page asks for twelve months ahead. From October 2026 that reaches October 2027, which is in the 2027-28 school year. Those dates are only proposed, are out for consultation, and could change before December.

**Candidate A (Design 2) invents those dates and presents them as fact.**
- It works 2027-28 out from a "usual pattern" that has already broken twice in two years (the February half-term and the summer start).
- For any date past the tables, it confidently returns days that may turn out to be term time.
- That is the failure Nadia can't absorb. Her play workers are teaching assistants who aren't free in term time, and the hall belongs to the school. A parent who books such a day has a booking the club cannot staff.
- Every council change has to be spotted and added as an override. Forgetting one fails silently, because the formula still produces plausible dates.
- The Easter algorithm and the weekday helpers add complexity in exchange for guesses.

**Candidate B (Design 1) only states what the council has confirmed.**
- Its error runs the safe way. Past the end of the table, it shows no club days, so nobody can book a day that might not happen.
- When the council publishes in December, someone copies the table in. The comment tells them to do this, and the change is easy to check line by line against the council's page.
- The data matches its source one-to-one. There is no hidden logic that can disagree with what the council published.

**Weakness in B, and the fix.** B treats "not yet published" the same as "closed", without saying so. It would be better to:
- record the last confirmed date and signal that anything after it is unknown, so the page can show "dates not yet confirmed" instead of a blank, and
- set a December reminder to add 2027-28.

Both are small changes to B's design. A's weakness is built into its approach.

WINNER: 1