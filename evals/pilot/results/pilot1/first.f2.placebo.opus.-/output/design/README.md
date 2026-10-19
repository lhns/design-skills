# Mill Lane Workshop: bookings and inductions

Design record for the machine booking and induction system.
Stakeholder and decision maker: Ines (runs the workshop; available most Tuesdays and Fridays).

| File | What it holds |
| --- | --- |
| [requirements.md](requirements.md) | Constraints (C1…) taken from Ines's brief, plus inferred ones; prioritized requirements |
| [design.md](design.md) | The design doc (draft, not yet reviewed) |
| [open-questions.md](open-questions.md) | Forks waiting on Ines or the insurer, each with options and a recommendation |
| [assumptions.md](assumptions.md) | What we treat as true without proof yet |
| [risks.md](risks.md) | What could go wrong, and how we find out early |
| [adr/](adr/) | Architecture decision records (all *Proposed* so far) |

## Session log

### Session 0 — 2026-10-19 (designer only, from Ines's written brief)

**Where we are.** First draft of the constraints and a design sketch. Nothing is agreed yet; every
decision in `design.md` is a *proposal* or a *designer choice* until Ines confirms it.

**Main findings.**
- The existing fob interlocks are the natural place to enforce inductions, the table saw two-person
  rule and to measure laser hours. One rule ("power on when enough inducted people have tapped")
  covers the laser and the table saw; only the number differs.
- Because the table saw rule must be *enforced* (insurer), the interlock has to know who is inducted.
  So a digital induction register is forced, whatever happens to the paper book. The only open part is
  whether a fob-tap sign-off counts as the trainer's "signature" for the insurer.
- Ines's notes conflict in one place: "fob is the identity, full stop" (9 Oct) and "book from home
  through the website" (16 Oct). There is no fob reader at home. Proposal: sign in by emailed link,
  which has no password to forget (Q1, ADR 0003).

**Open, by owner.**
- Ines: Q1 (website sign-in), Q4 (laser fairness rule), Q5 (3D printers), Q6 (materials).
- Ines → insurer: Q2 (does a fob-tap sign-off count as a signature?), Q3 (does "two inducted people
  tap to start" count as enforced?).
- Ines → interlock and laser suppliers: A3, A4, A6 in assumptions.md.
- Designer: shortlist hosted platforms against the must-haves in ADR 0001 once Q1–Q3 are answered.

**Next.** Session with Ines (Tuesday or Friday): go through Q1–Q6, starting with Q1.
