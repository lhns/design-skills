I've written the design to `answer.md` (591 words, under the 600 limit). It replaces the layered patches with two ideas.

**1. One rule to look up who is on call, nothing stored ahead of time.** `on_call(T)` checks three things in order and takes the first match:
- **Override:** the newest override covering T.
- **Holiday:** the cover engineer if T's local date is a public holiday.
- **Rotation:** otherwise, the engineer the rotation gives for that week, after applying any swap.

Nested covers then need no special handling. Chris's override is newer than Ana's, so Chris is on call Wednesday 13:00–17:00 and Ana for the rest of her cover. The planning page cuts the requested range at the moments the answer can change (handovers, holiday midnights, override starts and ends) and looks up each piece, so it works for any range, however far ahead. Payroll adds up those pieces per engineer over the local calendar month. Paging needs three indexed lookups, with no cache or nightly job.

**2. Edits only add rows; they never change or remove them.** Each row records when it was entered and, if withdrawn, when that happened. The answer for time T uses only the rows in force at T, so no edit can change the past. That is why payroll for a past month always comes out the same, and why snapshots and the "not in the past" checks for each edit type are no longer needed. Deleting an override just marks it withdrawn from that moment.

Weeks are counted by calendar date rather than in blocks of 168 hours, so a week with a clock change is simply 167 or 169 hours long and the one-hour correction goes away.

**My design choices** (each is labelled in the file):
- A new rotation list starts with its first engineer.
- A week can be in only one swap at a time; swaps don't chain.
- Payroll pays the hours actually on call, so a clock-change day counts as 23 or 25 hours.
- An edit entered late takes effect from when it was entered: an 08:00 cover entered at 08:20 starts at 08:20.
- Correcting history is treated as a payroll adjustment and left out of this design.

**Dropped from the current system:** override splitting, "shortest wins", the holiday exception for older overrides, the schedule cache and its nightly job, payroll snapshots, and permanent deletes.