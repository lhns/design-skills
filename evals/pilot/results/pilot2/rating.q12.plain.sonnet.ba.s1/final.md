**Design 2 (Candidate A) is the better design.**

**The real requirement is to match the published times.** Ruth says the trustees fixed the closing times in 2019 and printed them on the leaflet, the season-ticket cards and the gate boards. The website and ticket machine must agree with those. Mismatches have already caused a queue of unhappy season-ticket holders. The 2011 policy is where those numbers originally came from, but the published table is now the source of truth.

**Design 1 only approximates the policy.** It derives closing times from a sunset formula, a sinusoidal approximation at 52°N, plus DST rules and rounding. That is a different thing from the printed table.
- Agreement with Ruth's list for 2026 and 2027 only shows the approximation currently lands on the right half-hour. Several months likely sit close to a rounding boundary, so a small change in the leap-year offset, the DST dates or the formula could shift a month by 30 minutes in some later year. The website would then silently disagree with the painted boards, which is the failure Ruth described.
- It is also more complex and harder to audit. Nobody can check it against the leaflet by eye.
- Real sunset times would not give the trustees' numbers anyway. Even a more precise formula would only be faithful to the policy, not to the boards.

**Design 2 encodes the actual published values directly.**
- It is trivially verifiable against the leaflet, and it is deterministic for every year.
- It is simple, with no maths or DST logic to get wrong.
- If the trustees change the times, the table is updated deliberately, along with the boards and leaflets. That is the right process because the physical signage has to change at the same time.

A small improvement would be a test that asserts the table equals Ruth's list. Even without that, Design 2 is the safer and clearer choice.

WINNER: 2