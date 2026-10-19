**Constraints**
- C1: Members see free slots for the next 14 days on the website, and bookings are also made at the desk (stated).
- C2: Never double-book a (court, slot); the unique index enforces it (inferred).
- C3: A change to opening hours or a court block must take effect at once. Mo changes hours the afternoon before, and blocks a court immediately. The manager does not want people to turn up at a locked hall after booking online that same morning (stated).
- C4: Load is about 40 bookings a day, with a Monday-morning peak, on a small database that has never been a problem (stated). Performance is not a constraint.

**Design 2 (the precomputed `free_slot` table)**
- It makes `free_slots` fast, which solves a problem C4 says does not exist.
- It stores a second copy of facts already held in `opening_hours`, `court_block` and `booking`. That copy goes stale whenever the admin page edits hours or blocks, until the nightly job runs.
- Break it: Mo shuts the hall for an exam at 4pm. `free_slot` still lists tomorrow's slots, and `book` succeeds because it only checks `free_slot`. A member books online and finds a locked hall. That is exactly the incident the manager wants to avoid, so C3 fails.
- Closing the gap would need the admin page to update the cache too, so one fact would be maintained in several places with several writers. The cache would also need the invariant "the table equals the derivation" kept by hand.
- It also has a second weakness. `book` and `cancel` can drift from the derivation. For example, cancelling a booking inside a blocked period re-inserts a slot that should not be free.

**Design 1 (derive on every read)**
- `free_slots` computes from `opening_hours`, `court_block` and `booking` each time, so there is one source of truth. Admin edits are seen immediately (C3).
- `book` re-checks inside a transaction against the current state, so a booking cannot succeed on a slot that has just been closed or blocked.
- The unique index backs C2 against two desks racing.
- The cost is a few small queries per request, which is irrelevant at 40 bookings a day (C4).
- Weak spots: it does not cancel existing bookings when Mo closes the hall later. That is outside both designs, and Design 2 has the same gap. Also, `book` calls `free_slots` for the whole day, which is more work than needed, but it is cheap and reuses the same definition of "free", so that fact is stated once.

**Ledger**
- Constraints: C1 to C4 above. C3 is decisive.
- Forced: derive availability from the source tables at read and book time, with the unique index as the final guard against double-booking.
- Designer choices: none added.
- Deletions: Design 1 needs no cache, no nightly job and no sync logic. The `free_slot` table, the job and the cancel re-insert all go.

Design 1 wins because it is the only one that keeps C3: Design 2's cached table goes stale on Mo's same-day changes and can accept bookings for a closed hall, and its speed benefit answers a constraint that does not exist.

WINNER: 1