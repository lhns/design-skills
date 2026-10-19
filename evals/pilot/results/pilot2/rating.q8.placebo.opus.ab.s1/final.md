**Design 2 (Candidate B) is the better design.** It computes free slots from the live data each time it is asked. Candidate A serves a precomputed copy that goes stale exactly when this centre needs it to be current.

### Why Candidate A fails the actual requirement

A stores derived data, the `free_slot` table, which is rebuilt only by the nightly job. During the day, only `book` and `cancel` keep it current. Mo's changes don't touch it:

- **Opening-hours changes.** When the school takes the hall "sometimes only the afternoon before", those slots stay in `free_slot` until the nightly rebuild. If Mo changes the hours on the morning of the closure, the rebuild never runs before the slot passes. Members can book online that morning and arrive at a locked hall. That is the failure the manager described from last winter.
- **Court blocks.** Mo blocks a court "straight away" because a lifted board is a safety risk. In A, the blocked court stays bookable until night.
- **`cancel` makes it worse.** It re-inserts the slot into `free_slot` without checking hours or blocks. Cancelling a booking on a court Mo has just blocked, or in hours the school has taken, puts that slot back on offer.
- **`cancel` on an unknown id** crashes with an `AttributeError` on `None` instead of failing clearly.

Fixing A would mean having the admin page also rewrite `free_slot`. That couples two modules and creates two sources of truth that will drift apart. This is the DRY problem with derived state: the rule "a slot is free if open, not blocked, and not booked" ends up living in the nightly job, in `cancel`, and in whatever the admin page does.

### Why the cache isn't worth having

The manager's numbers settle the trade-off. About 40 bookings a day, four courts, and a database that "has never been the problem". B's `free_slots` runs three small queries and loops over roughly 4 × 15 slots. Even on a busy Monday morning, that cost is trivial. A pays for an optimisation nobody needs with correctness that the users do need. This is premature optimisation in its classic form.

### Candidate B's strengths

- **One authoritative rule.** `book` validates through the same `free_slots` the website displays, so what is shown and what is accepted cannot disagree.
- **Changes take effect immediately.** A change to hours or a block applies at once, and `cancel` is a plain delete with nothing to resynchronise.
- **Race safety.** The unique `(court, starts_at)` index stops two desks from booking the same slot, and the comment says so.
- **Clear structure.** Guard clause for closed days, named constants `SLOT` and `COURTS`, and a docstring stating where the answer comes from.

### Minor points to tidy in B (not blocking)

- `book` doesn't check that `starts_at` falls within the 14-day window, or that it isn't in the past.
- A unique-violation from a concurrent booking will surface as a raw database error. Catching it and raising `SlotUnavailable` would give callers one failure type.
- `(court, starts_at) not in free_slots(...)` is a linear scan of a list. That's fine at this size, though returning a set would state the intent more clearly.
- `COURTS` is hard-coded. That's acceptable today (YAGNI), but it's worth noting if a court table ever appears.

WINNER: 2