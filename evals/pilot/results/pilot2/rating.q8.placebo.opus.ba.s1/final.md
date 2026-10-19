# Design 1 (Candidate B) is the better design

## Why

**It answers the manager's actual complaint.** Mo changes opening hours, sometimes the afternoon before, and blocks courts as soon as a board lifts. The manager's request is that nobody turns up to a locked hall again. Design 1 reads `opening_hours`, `court_block` and `booking` live on every call. An admin edit takes effect immediately on the website, and `book` rechecks the slot inside the transaction.

**Design 2 recreates the failure the manager described.** `free_slot` is rebuilt only by the nightly job. Suppose Mo closes the hall for a parents' evening at 3 pm. Until midnight:

- the website keeps offering the closed slots;
- `book` accepts them, because it checks only that a `free_slot` row exists, not the real hours or blocks;
- a freshly blocked court stays bookable, which is the twisted-ankle case.

`cancel` has the same flaw. It reinserts the slot without checking whether it is still bookable, so it can re-open time that is closed or blocked. It also crashes on an unknown `booking_id`, because `b` is `None`. Fixing all this means hooking the admin page into `free_slot` maintenance. That spreads one business rule ("what is bookable") across three writers plus a nightly job, and the copies drift.

**The cache solves a problem nobody has.** The centre takes about 40 bookings a day on 4 courts. One day's computation is roughly 4 × 15 slots plus three small indexed queries. The manager says the database "has never been the problem." Even with the Monday-morning peak, this is premature optimisation, and it costs correctness and a second source of truth.

**Design 1's concurrency is sound.** The check and the insert share a transaction, and the unique `(court, starts_at)` index is the final guard against two desks booking the same slot at once.

## Minor suggestions for Design 1 (non-blocking)

- `book` should catch the unique-violation error and raise `SlotUnavailable`, so callers see one consistent error.
- The `court_block` filter using `date(...)` won't use an index well. At this scale that doesn't matter, but an overlap test on timestamps would read more clearly.
- `free_slots` builds a full list just to test whether one slot is free. A small `is_free(court, start)` helper would read better, though it's fine as is.

WINNER: 1