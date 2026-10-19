**Candidate B is the better design.**

The handhelds report scans late and out of order, so the system needs to answer "what is the latest thing that physically happened to this pallet?" B answers that directly. A tries to answer it from arrival order plus a set of patches, and the patches break once a pallet is refused and received again.

**Candidate A: each ticket fix is a special case, and they interact badly**

A keeps mutable state (`location`, `moved_at`, `shipped`). Each rule comes from a ticket:
- Moves are ignored once shipped (#41).
- A receive doesn't override a known location (#47).
- A move older than the last applied move is ignored (#49).

These rules break in realistic cases:
- **A refused pallet is re-received, put away, and the dock PC uploads late.** The pallet has `shipped=True`, so the freezer's move arrives first and is discarded by the #41 rule. The late receive then sets `DOCK`. The pallet is actually in F2, and the move scan is lost for good.
- **A late original receive arrives after the shipped scan.** `received` sets `shipped = False` and `location = "DOCK"`. A pallet that left the building shows as on the dock.
- **`shipped` is a flag, not a time.** A has no way to tell a move taken before shipping from a move taken after the pallet came back, so it guesses from arrival order, which is the thing that can't be trusted.
- **A receive doesn't update `moved_at`.** Whether a move is considered stale depends on which scans happened to arrive first.

Every new arrival pattern will need another patch.

**Candidate B: time order makes the special cases unnecessary**

B stores every scan sorted by the time it was taken, and the current location is whatever the latest scan says.
- **#41:** a late move taken before the shipped scan sorts before it, so the pallet is correctly not in the building.
- **#47:** a late receive sorts before the first move, so the move wins.
- **#49:** order is fixed by timestamp, not arrival.
- **Refusal:** shipped, then received, then moved gives F2. Arrival order doesn't matter, so the late-upload case above works too.
- **Insertion order:** the result doesn't depend on the order scans arrive in, so replays and duplicates are safe. Scans are never edited or deleted, so an append-only log fits.
- **Cost:** `insort` is O(n) per pallet, and each pallet has only a handful of scans, at a few thousand scans a day.

**Minor nits in B**
- Equal timestamps are broken by arrival order, which is arbitrary but rare.
- `location_of` on an unknown pallet inserts an empty list into the `defaultdict`. Using `scans.get(pallet)` would avoid that.

These don't affect correctness. B is also shorter and easier to reason about.

WINNER: 2