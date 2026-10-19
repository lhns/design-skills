# Candidate B is the better design

**Constraints**
- **C1.** Scans arrive late and out of order: freezer batches, loading-bay handhelds, the dock PC uploading at the end of the shift.
- **C2.** Each scan carries the time it was taken, and handheld clocks are synced. Taken-time is therefore a trustworthy order, even when arrival order is not.
- **C3.** A refused pallet comes back the same day and is received again under the same barcode. One pallet can go through received → moved → shipped more than once.
- **C4.** Volumes are small, and scans are never edited or deleted.

**What these force.** Arrival order means nothing (C1), and taken-time is reliable (C2). So a pallet's location must be a function of its scans ordered by `at`: the latest scan taken wins. The three tickets are all one symptom: the old system applied scans in arrival order. Ordering by time removes all three without any special rule. C4 makes keeping every scan per pallet cheap.

**Trying to break A.** Here is one refused pallet on one day, with taken time first and upload time in brackets:
1. received 08:00 [dock PC, 18:00]
2. moved F2 09:00 [09:30]
3. shipped 10:00 [loading-bay handheld, 17:00]
4. received again 14:00 [dock PC, 18:00]
5. moved F3 15:00 [15:30]

The truth is that the pallet is in **F3**.

Here is what A does, in arrival order:
- At 09:30 the F2 move applies.
- At 15:30 the F3 move applies.
- At 17:00 the late `shipped` arrives. It sets `shipped=True` and `location=None`.
- At 18:00 the receives arrive. They set `shipped=False`, and because location is `None`, they set `location="DOCK"`.

The stock screen now shows the pallet at **DOCK**. It is actually in F3.

The variants fail too:
- If the 14:00 receive is the last thing to arrive, A shows DOCK.
- If the receive arrives before the late `shipped`, A shows the pallet as gone.
- A pre-shipment move that arrives late, after a re-receive, passes both guards. It is newer than `moved_at` and `shipped` is now `False`, so it puts the pallet back in an old bay.

All three of A's rules were written assuming one lifecycle per pallet. They apply arrival-order patches, so C3 together with C1 breaks them. A also never compares `received` or `shipped` against time, so a late ship or a late receive always overrides newer information.

**Trying to break B.** The scans are kept sorted by `at`, so the result does not depend on arrival order (C1). It also holds across any number of return trips (C3), because "latest taken scan" means the same thing in every cycle. The only unresolved case is two scans of the same pallet with identical timestamps. `insort` then keeps them in arrival order. That is a negligible edge case, and a sequence number would resolve it if it ever matters.

**Concept count**
- **A:** a mutable state record and a `shipped` flag. It has three exception clauses ("only if no location", "ignored once shipped", "ignored if older"), and each one cites a ticket.
- **B:** one ordered log per pallet and one rule (the latest taken scan says where the pallet is). It has no exceptions.

B has fewer concepts and also satisfies a constraint that A fails.

**Ledger**
- **Forced:** order by taken time, not arrival time (C1, C2). Location is the latest scan (C3).
- **Designer choice in B:** keep the full scan list rather than only the latest scan per pallet. Justified by C4, and it also gives an audit trail.
- **Deleted:** the `shipped` flag, `moved_at`, and the ticket rules #41, #47 and #49.

**Deciding reason:** A patches arrival-order symptoms and gives the wrong location for a refused pallet whose scans arrive late, while B derives the location from taken-time order, which the operations manager says is reliable.

WINNER: 2