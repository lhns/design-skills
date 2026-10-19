**Design 2 (the lookup table) is better.**

**What the requirement actually is.** The 2011 policy describes how the times were derived. Ruth says the trustees applied it in 2019 and the results have been fixed ever since. They are printed on the leaflet and season-ticket cards and painted on the gate boards. The real requirement is that the website and ticket machine match those physical boards, and a mismatch has already caused a queue of unhappy season-ticket holders. The table is the single authoritative home for those published values.

**Design 1 re-derives the numbers and can drift from the boards.**
- It approximates sunset with a sine curve, then applies the DST rule and rounds. Any small error near a half-hour rounding boundary can flip a month's result.
- The developer only verified 2026 and 2027. Over other years, leap years shift `tm_yday`, and DST dates move relative to the day-of-year curve. That can push the mid-month value across a rounding boundary and silently change a closing time that the boards say is fixed.
- If the UK changes its clock rules, the output changes, but the boards don't.
- It is much more code, with a hand-tuned magic formula (`1071`, `105`, `81`, `365`), for something that only needs to return twelve known values. That makes it harder to read and review.
- Matching the table on two years is weak evidence that it will keep matching.

**Design 2 is simple and correct for the actual need.**
- It is a direct, readable encoding of the published times, so anyone can compare it to the leaflet in seconds.
- It is deterministic and has no dependence on year, DST, or latitude approximations.
- If the trustees ever revise the times, the change is a one-line, obvious edit to the table, made when the boards are repainted. That is the right moment to change it.
- It follows KISS and YAGNI: it does not build a sunset model for a requirement that no longer exists.

**Trade-offs.** Design 1 more faithfully encodes the policy's wording and would adapt automatically if the trust went back to recomputing times. But that is a hypothetical, and an automatic change would be harmful here, because the website would diverge from the physical signage. The table's weakness is that the policy rationale is only in a comment. I would improve that by also noting that the values derive from the 2011 policy as applied in 2019, but that is a small tweak.

WINNER: 2