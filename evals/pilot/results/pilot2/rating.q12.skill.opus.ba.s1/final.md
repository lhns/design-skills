# Design 2 (Candidate A) is the better design

**Constraints**
- **C1 (Ruth):** the hours shown must match the leaflet, the season-ticket cards and the gate boards.
- **C2:** those printed times were fixed by the trustees in 2019 and have not changed since.
- **C3:** opening is 10:00 and last entry is one hour before closing.

The 2011 policy is how the trustees *derived* the table once. It is not what the website must satisfy now. The printed table is the source of truth, because a mismatch with it produces the queue of unhappy season-ticket holders.

**Trying to break each design against C1**
- **Candidate B** recomputes the printed table from a sinusoidal sunset approximation, a DST rule and a rounding step. It matches the table only because those three happen to agree with it.
  - The match was checked for 2026–27 only. Leap years shift the day-of-year by one, and the formula's error is a few minutes. Any month whose mid-month value sits near a half-hour boundary can therefore flip in some later year.
  - If the UK changes or drops summer time, B's output moves while the painted boards stay the same.
  - B has no notion of "the trustees decided", so it cannot express a trustee revision that departs from the formula.

  Each of these is a concrete event that breaks C1.
- **Candidate A** states the printed fact once, in the same shape it has on the boards. No date input can make it disagree with them. If the trustees revise the times, one row changes in the same place the boards change. That is the smallest possible blast radius.

**Counting concepts.** B adds a sunset model, magic coefficients (1071, 105, 81), a DST rule, `last_sunday`, mid-month sampling, rounding and a cap. Not one of these is forced by a current constraint, because the table already holds their result. B looks principled ("derived from policy"), but it derives from the wrong source. It also ties correctness to an approximation instead of the decree. A has two concepts (`OPENS` and `CLOSES`) plus the last-entry rule.

**Ledger**
- **Constraints:** C1, C2, C3.
- **Forced decision:** closing times come from the trustees' table, not from a calculation.
- **Deleted:** the sunset model, the DST rule, the rounding and the cap.
- **Designer choice:** cite the 2019 trustee decision in the table's comment so a future reader doesn't "fix" it back into a formula.

**Deciding reason:** A encodes exactly what the boards say, so it cannot drift from them. B only reproduces the boards by coincidence of an approximation, and that coincidence can break with the calendar or with legislation.

WINNER: 2