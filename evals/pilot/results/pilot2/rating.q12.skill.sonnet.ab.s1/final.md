**Design 1 is better.** Its table states the real constraint directly, while Design 2 reproduces that constraint only by coincidence.

**Constraints**
- C1 (Ruth): the website and ticket machine must show exactly the times on the leaflet, season-ticket cards and gate boards. A mismatch already caused a queue at the gate.
- C2 (Ruth): the times are fixed per month, set by the trustees in 2019 and unchanged since.
- C3 (inferred): last entry is one hour before closing.
- C4 (policy): opening is 10:00 every day.

The 2011 policy is where the numbers came from, but the trustees adopted a specific list. The list, not the sunset formula, is what is printed on the boards.

**Design 1**
- It has one concept, the monthly closing table, and it is the same fact the boards carry. C1 and C2 hold by construction.
- Last entry is derived from closing (C3), so that fact appears once. Opening is a constant (C4).
- Breaking it: if the trustees change a time, someone edits one row, and the boards have to be repainted anyway. No input can make the website disagree with the table.

**Design 2**
- It re-derives the times from an approximate sunset model. The constants 1071 and 105 are unforced, and the model also needs DST rules, a mid-month sampling choice and its own rounding.
- It matches Ruth's list only because it was checked for 2026 and 2027. A sunset value near a half-hour rounding boundary could flip in another year, and so could the last-Sunday DST dates. That would show the website different from the boards, which is exactly the failure Ruth described (C1).
- It adds a second source of truth that must keep agreeing with the first. The policy formula is not the constraint; the printed times are.
- Breaking it: a year where the approximated mid-month sunset lands on the other side of a 30-minute boundary, or a change in the DST rule.

**Counts:** Design 1 has one table and no exception clauses. Design 2 has a sunset model, a DST rule, a mid-month sampling rule, the 19:00 cap and magic constants. None of these is needed to meet C1–C4 once the times are fixed.

Design 2's only advantage is fidelity to the policy's wording. That doesn't outweigh C1, because Design 2 can drift from the boards and Design 1 cannot.

WINNER: 1