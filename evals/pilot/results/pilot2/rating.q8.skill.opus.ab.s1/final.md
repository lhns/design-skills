# Badminton slots: Candidate B is the better design

## Constraints

- **C1 (manager):** about 40 bookings a day, with a Monday-morning peak. The small database has never been the bottleneck.
- **C2 (Mo):** opening hours change at short notice, sometimes only the afternoon before.
- **C3 (Mo):** a court block takes effect straight away, for safety.
- **C4 (manager):** no bookings for a hall that turns out to be closed. Last winter's two incidents were bookings made online that same morning.
- **C5 (schema):** `booking` is unique on `(court, starts_at)`, so two desks can never book the same slot.
- **C6 (inferred):** cancelling a booking must not offer a slot that is no longer bookable.

## Trying to break each design

**Candidate A** stores free slots as a second fact. "Is this slot bookable?" lives both in `opening_hours`/`court_block` and in `free_slot`, and only the nightly job reconciles the two.

- **Breaks C2 and C4.** At 15:00 Mo shortens tomorrow's hours for a parents' evening. Until the nightly rebuild, `free_slot` still lists the evening slots, and `book` happily deletes one and inserts a booking. This is exactly last winter's incident, now built into the design. An early-morning change has the same effect for that day's slots.
- **Breaks C3.** A board lifts and Mo blocks court 2. Its slots stay in `free_slot` until night, so members can book a court that is a "twisted ankle waiting to happen."
- **Breaks C6.** A booking on a court that has since been blocked, or on hours that have since closed, gets cancelled. `cancel` re-inserts its slot into `free_slot` unconditionally, so the cache now offers a slot that should never have been there.
- Bookings that already exist when the hours change are a separate problem, and neither design notifies those members. A, however, keeps creating new bad bookings all day.
- **The cache is not forced by anything.** C1 describes a load that a per-request computation over at most 4 courts × about 15 hours handles trivially. The comment's justification ("one indexed query") answers a performance constraint nobody stated. The cost is three extra concepts: the table, the nightly job, and the bookkeeping in `book`/`cancel`. Each is a place where the duplicated fact can drift.

**Candidate B** derives free slots from the source tables on every call. There is no second copy, so nothing goes stale.

- **C2, C3, C4:** a change Mo makes at 15:00 is visible to the very next `free_slots` call and to the check inside `book`.
- **C5:** a race between the check and the insert is caught by the unique index, as the comment notes.
- **C6:** `cancel` just deletes the booking. Bookability is recomputed from current hours and blocks, so a blocked slot is not resurrected.
- **C1:** the cost is a few small queries and a 60-iteration loop per day shown, which is trivial at this volume.
- **Minor issues:**
  - The interval-overlap check rejects any slot that touches a block. That is correct.
  - `COURTS` hard-codes the four courts. That is acceptable here, since the schema has no court table to read from.
  - The check-then-insert sequence relies on the unique index rather than the transaction alone for concurrency. That is the right thing to rely on.

## Ledger

| | Candidate A | Candidate B |
|---|---|---|
| Facts stated twice | bookability lives in sources and in `free_slot` | none |
| Extra concepts | `free_slot` table, nightly job, sync in book/cancel | none |
| Constraints broken | C2, C3, C4, C6 | none found |
| Constraint that forces the extra parts | none (C1 says load is not a problem) | n/a |

**Deciding reason:** A caches bookability, which turns Mo's same-day hour changes and immediate court blocks into bookable ghost slots, the exact failure the manager asked to prevent. B derives availability from the live tables at a load that the manager says the database handles easily.

WINNER: 2