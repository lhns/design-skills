**Design 1 (Candidate B) is better.** It keeps every constraint with one concept. Design 2 patches each ticket with its own exception, and the patches break as soon as a pallet comes back.

## Constraints

- **C1** Scans arrive late and out of order, in batches from freezers, the loading bay and the dock PC.
- **C2** Each scan carries the time it was taken, from synced clocks. So the time a scan was taken is reliable, but the order it arrives in is not.
- **C3** A refused pallet returns with the same barcode and is received and put away again. One pallet can go through received, moved and shipped more than once.
- **C4** Scans are never edited or deleted, and there are only a few thousand a day.

From C1 and C2, a pallet's location must be a function of scans ordered by the time they were taken. The order they happen to arrive in can't decide it. Tickets #41, #47 and #49 are all cases of this one fact: an older scan arrived after a newer one.

## Trying to break Design 2 (Candidate A)

Every ticket fix assumes the pallet goes through its life only once. C3 breaks that.

1. **A late original receive revives a shipped pallet.**
   - 08:00 received; 09:00 moved to F2; 11:00 shipped.
   - The dock PC uploads the 08:00 receive at the end of the shift (#47).
   - The receive sets `shipped = False`, and because `location is None` it shows DOCK.
   - The pallet is on a lorry, but the screen says it's at the dock.
2. **A late pre-shipment move lands after a return.**
   - 09:00 move to F2 applied; 11:00 shipped; 15:00 re-received.
   - Then a freezer move taken at 10:00 arrives.
   - `shipped` is now False, and 10:00 is later than `moved_at` (09:00), so the pallet shows F2. That's wrong.
3. **A late shipped scan wipes out a return.**
   - The bay handheld uploads the 11:00 shipped scan after the 15:00 receive and the 15:30 putaway.
   - The shipped scan sets `location = None`, so the pallet shows as not in the building while it sits in a bay.
4. **Only moves are compared by time.** Receives and ships are applied in arrival order, which ignores C2 for two of the three scan kinds.

Each patch carries an exception clause: "ignore unless not shipped", "only if no location", "unless older than the last move". Adding the return case would need more of them, such as a "trip" counter or timestamps on ship and receive. That is the local optimum the method warns about.

## Trying to break Design 1 (Candidate B)

- **Shared concept:** an event log ordered by the time scans were taken. The location is a fold that reads the newest entry.
- **#41, #47, #49 and all three scenarios above:** in each one, the newest-taken scan is correct, whatever order the scans arrived in. A return is simply a newer `received`, so C3 needs no extra code.
- **C4:** keeping every scan costs nothing, because scans are append-only and there are few of them. It also gives an audit trail for free.
- **Residual risks:**
  - Two scans of the same pallet with identical timestamps keep their arrival order. That is acceptable, but worth noting.
  - Both designs depend equally on the clocks staying synced (C2).
  - `insort(key=…)` needs Python 3.10 or later.

## Counts

| | Design 1 (B) | Design 2 (A) |
|---|---|---|
| State concepts | 1 (sorted scans) | 3 (`location`, `moved_at`, `shipped`) |
| Exception clauses | 0 | 3, plus more needed |
| Constraints broken | none found | C1 with C3 (three concrete scenarios) |

**Deciding reason:** Design 2 orders only moves by the time they were taken and resolves everything else by arrival order, so a returned pallet breaks it. Design 1 makes "the latest-taken scan wins" the single invariant, and every ticket and the return case follow from it without exceptions.

WINNER: 1