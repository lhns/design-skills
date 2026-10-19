# Design 1 (Candidate B) is the better design

## The core difference

**Candidate B** treats the pallet's location as derived from its scan history. It inserts each scan in order of when it was taken, and the location is whatever the latest-taken scan says. Arrival order doesn't matter. The ops manager confirms both preconditions: every scan carries its capture time, and handheld clocks are synced on every connect.

**Candidate A** keeps mutable state and adds a special-case rule for each ticket. Only moves are compared by time. Receives and ships are applied in arrival order, guarded by flags (`shipped`, `location is None`). That works for each ticket on its own, but not once the cases combine, and the refused-pallet flow combines them.

## Where Candidate A gives the wrong answer

These scenarios use only the delays the manager described.

1. **Refused pallet, dock PC uploads at end of shift (#47 combined with returns).**
   Shipped 12:00 → received back 15:00 (not uploaded yet) → moved to F3 at 15:30 (uploaded).
   - The move is ignored because `shipped` is still True.
   - At end of shift the receive arrives. It clears `shipped` and puts the pallet at **DOCK**.
   - The pallet is actually in F3. Candidate B shows F3.

2. **Late freezer move after a return (#41 combined with returns).**
   Move to F1 10:00 → move to F2 11:00 (freezer, delayed) → shipped 12:00 → refused, received 15:00 → *then* the 11:00 move uploads.
   - `shipped` is now False, and 11:00 is later than `moved_at`, so A shows **F2**.
   - The pallet is actually at the dock. Candidate B shows DOCK.

3. **Late shipped scan from the loading bay (bay doors block signal).**
   Shipped 12:00 (delayed) → received back 15:00 → the shipped scan uploads at 16:00.
   - A marks the pallet as gone.
   - It is actually in the building. Candidate B is correct.

The tickets show a pattern: each delayed-upload bug got a narrow patch. Candidate A writes those patches down as the design, so the next combination of delays will need another one. Candidate B fixes the root cause, which is trusting arrival order instead of capture time. #41, #47 and #49 then all follow from one rule.

## Other considerations

- **Simplicity:** B is about ten lines with a single rule. A has per-kind branches and flags whose interactions you have to trace by hand.
- **Fit to constraints:** Scans are append-only and number a few thousand a day, so keeping the full history per pallet is cheap. It also gives you an audit trail for free.
- **Minor nits in B (not blocking):**
  - `insort(..., key=...)` needs Python 3.10 or later.
  - `location_of` on a `defaultdict` creates empty entries for unknown barcodes. Use `scans.get(pallet)` instead.
  - Ties on identical timestamps resolve in arrival order. If that matters, add a secondary sort key such as a scan sequence number.
  - The design relies on clock sync. If that ever breaks, B would give wrong answers, so it's worth a monitoring check on clock drift.

WINNER: 1