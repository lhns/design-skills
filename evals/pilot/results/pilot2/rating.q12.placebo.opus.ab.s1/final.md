# Design 1 (Candidate A) is better

**The requirement is to match the boards, not the policy.** Ruth is clear that the trustees set the times in 2019 and they have not changed. They are printed on the leaflet, the season-ticket cards and the gate boards, and the website must agree with those. The policy text explains where the numbers came from, but the published table is now what the code must reproduce. Candidate A stores that table directly, so it matches the boards by construction.

**Candidate B only matches by coincidence.** It recomputes the times from an approximate sunset curve, the 15th of each month, a fixed 365-day year and a summer-time rule. The developer checked 2026 and 2027, and it agrees there. But each month's result is a value rounded to the half hour, so any month whose computed close lands near a :00 or :30 boundary can flip in another year. Several things move between years:

- In a leap year, the 15th falls one day-of-year later from March onward.
- The approximation has its own error.

When that happens, the website disagrees with the gate boards. That is exactly the incident Ruth described. The failure would also be silent: nothing in B would show that it had drifted from the published times.

**Clarity and cost of change.** A reader can check A against Ruth's list at a glance. To check B, the reader has to understand a sinusoidal sunset model, the magic numbers `1071` and `105`, the `last_sunday` arithmetic and the mid-month sampling convention. Then the reader still has to run it to confirm the output. If the trustees ever revise a month, A needs a one-line edit, while B would need special cases to override the formula. B adds complexity in order to re-derive data the organisation already treats as fixed, which runs against both YAGNI and KISS.

**Minor suggestions for A (not blocking):**

- Name the last-entry rule, for example `LAST_ENTRY_BEFORE_CLOSE = timedelta(hours=1)`, or add a comment citing the policy. `closes.hour - 1` is safe only because every closing time is 15:00 or later.
- Add a test that checks `CLOSES` against Ruth's list, so an accidental edit is caught.
- Expand the comment to note that these times were fixed by the trustees in 2019 from policy section 2. Without that, a future maintainer might "improve" the table back into Candidate B.

WINNER: 1