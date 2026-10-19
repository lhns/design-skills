**Constraints**
- C1 (manager): ~40 bookings/day, small DB, so load is tiny. Read performance is not a constraint.
- C2 (Mo): opening hours and court blocks change at short notice, even the afternoon before, and a block must take effect immediately.
- C3 (manager, inferred as a requirement): nobody should book or see a slot that is closed or blocked. Locked-hall incidents must not recur.
- C4 (schema): `booking` is unique on `(court, starts_at)`, so double booking is already prevented.
- C5: bookings come from both the website and the desk.

**Candidate A** keeps `free_slot` as a materialized copy of facts that already exist in `opening_hours`, `court_block` and `booking`. That copy is rebuilt nightly. The admin page edits hours and blocks, but nothing in the code updates `free_slot` when they change.

Breaking input: Mo closes the hall for tomorrow's exam at 3pm. `free_slot` still lists tomorrow's slots until the night job runs. Worse, a block made at 9am today stays bookable all day, and `book` succeeds because the stale row is deleted. That is exactly the "booked online that same morning, locked hall" incident. A also has a second issue: `cancel` re-inserts a slot without checking whether it has since been blocked or closed, so it can resurrect a closed slot. The performance reason for the table is also not a constraint (C1). A violates C3 and C2, and it states the same fact twice (availability in the tables and again in `free_slot`).

**Candidate B** derives availability on demand from the three source tables, so there is one source of truth. Admin changes take effect on the next read (C2, C3). `book` rechecks inside the transaction against current hours and blocks, and the unique index backs it up against races (C4). `cancel` is a plain delete with nothing to keep in sync. The cost is a few small queries per request, which at 40 bookings/day and a small DB is negligible (C1). Even the Monday-morning peak is modest for three tiny queries.

Weaknesses in B:
- There is a small race: a block inserted between the check and the insert in `book` could slip through. This window is milliseconds, and A has it too (worse, since A has no check at all).
- `COURTS` is hardcoded, which matches "four courts" but duplicates the fact. It is minor.
- Blocks are not rechecked against `booking`, so existing bookings on a newly blocked court are not surfaced. Neither design handles that.

**Deciding reason:** B keeps a single source of truth, so a last-minute hours change or court block is honored immediately and the locked-hall incident cannot recur. A's cache buys speed that no constraint requires, and it breaks C3.

**Ledger**
- Constraints: C1–C5 above.
- Forced: derive availability from the source tables (C2, C3); rely on the unique index for double booking (C4).
- Designer choices: none that affect the verdict. The hardcoded `COURTS` is the only one, and it's minor.
- Deletions: `free_slot`, the nightly job and the cache-sync logic in `book` and `cancel`.

WINNER: 2