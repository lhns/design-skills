**Candidate B is the better design.**

**The deciding fact is correctness under last-minute changes.** Mo edits opening hours and blocks courts on the admin page, sometimes the afternoon before or immediately. The manager says people already turned up to a locked hall with same-morning online bookings, and doesn't want a repeat.

**Candidate A** keeps a materialized `free_slot` table that is rebuilt only nightly and otherwise updated only by `book` and `cancel`. Nothing in the admin page's writes touches it. So when Mo shortens the hours or blocks a court mid-day, the website keeps offering those slots until the next rebuild, and members can book them. That is exactly the reported failure. Further problems:
- `cancel` re-inserts a slot unconditionally, even if the hours have since changed or the court is now blocked, so cancellations can resurrect unbookable slots. It also fails with an unclear error if the booking id doesn't exist (`b` is None).
- Two sources of truth (the tables plus the derived one) can drift, and the nightly job papers over that rather than fixing it.
- Newly opened days or the rolling 14-day window depend on the job having run.

**Candidate B** derives availability on read from the authoritative tables (hours, blocks, bookings), so admin changes take effect immediately, for both the website and the desk. `book` re-checks inside a transaction, and the unique `(court, starts_at)` index backstops races. `cancel` is a single delete with no derived state to maintain. Weaknesses: the `COURTS` constant is hard-coded, the block query's `date()` comparisons are fine but not indexed-optimal, and `book` should translate a unique-constraint violation into `SlotUnavailable`. These are minor and easy to fix.

**Performance doesn't justify A's complexity.** About 40 bookings a day, 4 courts, and at most ~14 hours per day means B reads a handful of rows per request. The Monday-morning peak is modest for that, and the manager says the database has never been the problem. A's optimization addresses a bottleneck that doesn't exist, and it pays for it with the stale-data bug the manager explicitly wants to avoid.

By KISS and YAGNI, B is simpler and has a single source of truth. A trades correctness for speed that isn't needed.

WINNER: 2