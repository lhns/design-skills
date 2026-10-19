**Candidate B is the better design.**

**Candidate A** keeps a materialized table, `free_slot`, which is a cache of derived data. It is rebuilt nightly, and only booking and cancelling update it during the day. Nothing updates it when Mo changes `opening_hours` or adds a `court_block`, and Mo does exactly that, often at short notice. Until the next nightly rebuild, the website keeps offering slots that are no longer valid. That is how people end up at a locked hall with bookings made that same morning, which the manager explicitly doesn't want repeated. A blocked court is a safety issue as well. Further problems:

- `book` trusts `free_slot` as the authority. It will accept a booking on a closed or blocked slot.
- `cancel` re-inserts the slot without checking whether it is still open or unblocked. It also breaks if the slot was removed or the row is missing.
- Rebuilding must also reconcile with existing bookings, and there are two sources of truth to drift apart.
- The performance gain it buys isn't needed. There are about 40 bookings a day, four courts, and one day queried at a time.

**Candidate B** computes availability on read from the authoritative tables: opening hours, blocks, and bookings. A change by Mo takes effect on the next page load, with no invalidation logic. Its cost is three small queries per day view, plus a loop over at most about 12 hours × 4 courts. That is trivial at this scale, even on Monday mornings with a small database. `book` re-checks against the current data inside a transaction, and the unique index on `(court, starts_at)` is the final guard against double booking. `cancel` is a single delete, with nothing to keep in sync.

B has minor weaknesses:

- The block query uses `date()` comparisons, which is fine.
- The `COURTS` constant is hardcoded.
- The booking race is covered by the unique index, though the resulting integrity error should be translated into `SlotUnavailable`.
- Existing bookings made before a closure or block are not cancelled automatically. Neither design handles this, so it needs a separate process (notifying members).

These are small compared with A's stale-data defect, which directly causes the failure the manager wants to avoid. B's simplicity and correctness outweigh A's unnecessary optimisation.

WINNER: 2