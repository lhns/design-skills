**Design 2 is better.** Its state is a pure function of the set of scans, so it does not depend on the order they arrive in.

**Constraints**
- C1: scans arrive late and out of order, by up to an hour or a whole shift. Each scan carries a usable timestamp.
- C2: a refused pallet is received again under the same barcode, so a pallet can have several lives.
- C3: scans are never edited or deleted, and volume is small.
- C4 (inferred): the stock screen must be right whatever the arrival order.

**The shared concept.** Tickets #41, #47 and #49 are the same fact: the latest scan taken wins, however late it arrives. Design 2 states that once. It keeps a log sorted by time taken and reads the last entry.
- #41: the late move sorts before `shipped`, so the pallet stays shipped.
- #47: the late receive sorts before the moves, so the pallet stays in its freezer location.
- #49: the moves are ordered by time taken, so the later one wins.
- A refused return is a `received` scan after `shipped`. It becomes the latest scan and gives DOCK, with no special rule.

**Breaking Design 1.** It has three rules (`shipped` blocks moves, receives don't override a location, moves must be newer than `moved_at`). Each rule is a patch for one ticket, and the state depends on arrival order.
- Refused pallet, with the bay handheld uploading late. The return `received` arrives before the older `shipped`. The receive is ignored because a location is known, then `shipped` sets the location to None. The pallet is physically on the dock but shows as gone.
- Refused pallet, with a first-life move arriving late. After the re-receive, `shipped` is False and `moved_at` is stale. A freezer move from before the shipment passes the guards and puts the pallet back in the freezer. Rule #41 only holds while the pallet is currently shipped, so it cannot cover this.
- It also stores two facts about the same thing (`shipped` and `location=None`), plus `moved_at`, which has no meaning across lives.

**Breaking Design 2.** The only real weak spot is two scans with identical timestamps, where `insort` falls back to arrival order. That is a rare tie, and it could be fixed by adding a tie-break key. Clock skew between handhelds affects both designs. Memory growth is irrelevant at a few thousand scans a day, and an append-only log fits the rule that scans are never edited.

**Ledger**
- Constraints: C1 to C4 above.
- Forced: order the scans by the time they were taken, and take the latest.
- Deletions from Design 1: the `shipped` flag, `moved_at`, and the three ticket-specific guards.
- Concept count: Design 1 has three state fields and three exception rules. Design 2 has one log and one rule.

The deciding reason: only Design 2 gives the right answer for every arrival order, including refused returns, and it does so with one rule instead of three order-dependent patches.

WINNER: 2