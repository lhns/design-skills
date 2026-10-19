**Design 1 is better.**

The requirement that matters is that the website and ticket machine must match the gate boards, leaflet and season-ticket cards. Ruth says the trustees set these times in 2019 and they have not changed since. A mismatch has already caused a queue of unhappy season-ticket holders at the gate.

The 2011 policy is where those times came from. The published times are now the commitment, and the formula only explains how they were chosen.

**Candidate A** encodes the published times directly as a 12-entry table.
- It cannot drift from the boards, in any year.
- It is trivially readable and testable.
- If the trustees ever change the times, someone edits one table, and the boards and leaflet must be updated at the same time anyway.
- Last entry is derived as closing minus one hour. That is safe here because no closing time is before 01:00.

**Candidate B** re-derives the times from an approximate sunset formula, a hand-rolled DST rule and a mid-month sampling convention.
- It matches Ruth's list for 2026 and 2027 only because it was checked for those years. It is an approximation, and some mid-month values may sit close to a half-hour rounding boundary.
- In other years, small shifts in the day of year (leap years) or in where the last Sunday falls could push a month across a rounding boundary. The website would then differ from the boards, which is exactly the failure Ruth described.
- It adds complexity (trigonometry, DST logic, date arithmetic) for no benefit. The published schedule is fixed, so nothing needs computing.
- It optimises for fidelity to the policy text rather than to the real requirement, which is consistency with the printed times.

If the trustees later decide to follow the policy formula dynamically, that would be a deliberate change requiring new boards and leaflets, and the code could change then. For now, the table is the correct and safer design.

WINNER: 1