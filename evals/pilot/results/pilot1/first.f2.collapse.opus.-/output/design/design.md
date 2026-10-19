# Mill Lane workshop: bookings and inductions (design, round 1, 2026-10-19)

The current design: one suggested point in the solution space. K/X/W ids are in `kernel.yaml`
(Ines's words), F ids in `forks.yaml`. Every fork is still open, so it runs on its default and
nothing here is decided until Ines says so. Records: `vision.md`, `kernel.yaml`, `forks.yaml`, `concepts.yaml`.

## Generating idea (proposed)
**A fob tap, checked against the member's inductions.** In the building, the only thing a member
ever does with the system is tap a fob (K3, K4, K13). The tap identifies them, and a machine powers
on only if they are inducted on it (K7). Bookings, the saw's two-person rule and the laser tube
hours all come from the same taps:

| Need | What the tap does |
| --- | --- |
| Induction enforced (K7) | Machine powers on only for a fob inducted on it. |
| Saw two-person rule (K14, K15) | Saw also needs a second, different saw-inducted fob tapped within a short window (F3). |
| Booking honoured (K12) | The first tap in the slot claims the booking; if nobody claims it, it is released (F7). |
| Tube hours (K10, K11) | Interlock powered-on time adds up on the current tube (F5). |
| Fair laser use (V12) | Taps show who actually used it, and the booking rule limits holding (F6). |

## Concepts (8 forced, 8 details hanging on forks, 1 outside)
Forced:
- **Member**: one person, with a fob. The member record outlives any one fob, so a lost fob loses no inductions (K13, K7).
- **Machine**: table saw, bandsaw, lathe, laser, three printers, electronics bench (K1).
- **Induction**: member + machine + trainer + date + trainer's signature, kept six years (K7, K8, K17, K18).
- **Tap**: the one on-site event (K3, K4, K13).
- **Interlock rule**: power on only for an inducted fob (K4, K7, K15).
- **Booking**: member + machine + slot, made from home (K12, K20).
- **Tube meter**: hours on the current tube. It warns to order a spare when *remaining hours (≈1,000 − used, K10) < hours used during the supplier's lead time*. That is a condition, not a fixed number; the lead time is a fact we still need from the supplier (K11).
- **Insurer register**: sign-offs listed by trainer and date, printable at renewal (K17, K18).

Details (each depends on its fork's current default; it moves if Ines picks differently):
- Saw partner tap (F3/two-taps-at-start). One exception clause, forced by K14 and K15.
- Claim-by-tap and release (F7/release-unclaimed). The grace period is one value for Ines to set.
- One upcoming laser booking per member (F6/one-upcoming). Recommended over a 2 h/week cap: no number to tune, nothing goes unused in quiet weeks, and it targets people booking far ahead.
- Emailed sign-in link for home booking (F1/email-link). **Conflict with K13, raised with Ines.**
- Trainer signs on a tablet, book retired (F2/digital-signed). Until the insurer confirms, the default is the paper book plus a desk copy (F2/paper-plus-copy).
- Interlocks retrofitted on bandsaw, lathe and printers (F4/all-machines), so one rule holds everywhere.
- Each interlock keeps a local copy of inductions and keeps working offline (F10/cached).
- Printers are first come, first served, with live status on the website (F8). Ines is still deciding this.

Outside the system: **materials**. Sold by the sheet or spool up front, or members bring their own, with self-service payment after 18:00 (F9, W1). No meter.

Platform: a hosted makerspace platform if one passes the kernel, otherwise a custom app on managed hosting (F11, W5). Not our own server.

## Forced, not chosen
- Inductions **must** be machine-readable: the saw's interlock enforces "both inducted" (K14, K15), and paper can't tell it. So "keep only the paper book" is out (F2). What's still open is whether paper stays as the signed copy.
- The saw rule must be enforced by the machine itself. There are no staff in the woodshop in the evening and closing early is out (K16, X2).

## Scenario walk-throughs (probe)
- *Thu 19:30, woodshop, no staff.* Sam taps at the saw; it stays off and the reader shows "partner needed". Alex, also saw-inducted, taps within the window, and the saw powers on. If Alex had no saw induction, the saw stays off.
- *Laser booked 18:00-20:00 by Priya, who doesn't come.* No tap by the end of the grace period, so the slot is released and a walk-up can tap in.
- *Laser job still cutting at the end of a slot.* The interlock never cuts power mid-job, so the next booking starts late (F12).
- *Member loses a fob.* The desk attaches a new fob to the same member, and the inductions carry over.
- *Internet down on a Tuesday evening.* Interlocks decide from their local copy (F10).
- *Member leaves.* Their induction records stay for six years (K18).

## Unknowns that are facts, not decisions
- Make and model of the existing interlocks and of the laser controller (affects F5, F11).
- Supplier lead time for a laser tube (sets the tube-meter warning).
- Hours a member can get in before 10:00 (bookable window).
- Insurer's view on electronic signatures (F2) and on a two-fob start (F3).

## Ledger
- Owner constraints: K1–K21, X1–X2; values W1–W5.
- Forced: machine-readable inductions; machine-enforced saw rule; member record separate from the fob; tube meter; insurer register.
- Designer choices (provisional, on open forks): F1–F12 as above.
- Conflict for the owner: K13 ("fob is identity, full stop") vs K20 (home booking). F1 is asked.
- Deleted: none (first round).
- Counts (round 1): 16 concepts, 1 exception clause, 1 unforced number, 12 open forks, 0 facts stated twice.
