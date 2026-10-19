# Village hall bookings: design notes

Stakeholder: Gwen (bookings volunteer). Decisions about money, rules and the building belong to the hall committee; Gwen brings them to the committee.

| File | What it holds |
| --- | --- |
| [requirements.md](requirements.md) | Constraints (C1…) taken from Gwen's brief, plus requirements |
| [design.md](design.md) | The proposed design (draft, not agreed) |
| [assumptions.md](assumptions.md) | Things treated as true but not yet confirmed |
| [risks.md](risks.md) | What could go wrong, and what we'll do about it |
| [questions.md](questions.md) | Open questions, ordered by how much they change the design |
| [adr/](adr/) | Decision records (all *proposed* until Gwen/committee accept) |

## Session log

### Session 1 (2026-10-19): brief received
- Read Gwen's brief and drafted the constraints, a first design, and the assumptions and risks.
- **Urgent finding:** the clocks go back on **Sun 25 Oct 2026** and forward on **Sun 28 Mar 2027**, while Gwen is away. If the sound-limiter time switch is set and doesn't adjust itself for summer time, in spring it will cut the power at midnight instead of 23:00, which would breach the licence (R1, A3).
- Nothing has been decided yet. Every ADR is *proposed*.
- Next: Gwen answers Q1 (where amplified kit can be plugged in, and what the time switch controls). After that, take the proposed rules (ADR 0002, 0003) to the committee.
