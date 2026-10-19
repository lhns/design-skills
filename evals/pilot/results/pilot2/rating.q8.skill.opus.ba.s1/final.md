# Design 1 (Candidate B) is better

**Constraints**
- **C1.** Opening hours and court blocks change at short notice: "sometimes only the afternoon before", and blocks go in "straight away".
- **C2.** Never sell a slot when the hall is closed or the court is blocked. This is the manager's locked-hall complaint, and the ankle risk.
- **C3.** Two desks must not book the same slot.
- **C4.** Load is about 40 bookings a day, with a Monday-morning peak. The database "has never been the problem".

**Trying to break Design 2 (Candidate A, the `free_slot` table)**
- **Changed hours (C1, C2).** At 3pm Mo closes tomorrow afternoon for a parents' evening. `free_slot` was built by last night's job, so the website still offers those slots, and `book` accepts them because the row exists. This is the locked-hall incident again. The same happens when a board lifts and Mo blocks a court: that court stays bookable until the job runs that night.
- **Cancellations.** `cancel` puts the slot back into `free_slot` without checking hours or blocks. Cancelling a booking on a court that has since been blocked makes the blocked slot bookable again, even after the next nightly rebuild has removed it.
- **Two copies of one fact.** Free slots are stated twice: once implicitly by hours, blocks and bookings, and once in `free_slot`. Three writers (the job, `book` and `cancel`) must keep them in sync, and the admin page, which is the one writer that matters for C1, doesn't. Fixing this means making the admin page rebuild or patch the table too. That adds more concepts to serve a cache no constraint asks for.
- **What justified it.** "One indexed query" answers a performance need that C4 explicitly rules out. Computing about 4 courts × 15 hours of slots from three small queries costs nothing.

**Trying to break Design 1 (Candidate B)**
- **C1, C2.** It reads current hours, blocks and bookings every time, so a change Mo makes takes effect on the next page load and the next `book` call. `book` re-checks inside the transaction, so a slot that became blocked after the page loaded is rejected.
- **C3.** Two desks racing for one slot are stopped by the unique `(court, starts_at)` index.
- **Remaining gaps.** It doesn't enforce the 14-day window or reject past start times, but Design 2 doesn't either. Neither design warns existing bookings when hours change later, so that doesn't separate them.

**Count**
- Design 2 adds a derived table, a nightly job and synchronisation logic in `cancel`, and still fails C2.
- Design 1 has none of these. Free slots are computed on demand from what's already stored, so there is no second copy that can go stale.

**Deciding reason:** Design 2 caches free slots in a table rebuilt nightly, so same-day changes to hours or blocks are ignored and members can book a locked hall or a broken court; Design 1 computes from live data, and the load easily allows that.

WINNER: 1