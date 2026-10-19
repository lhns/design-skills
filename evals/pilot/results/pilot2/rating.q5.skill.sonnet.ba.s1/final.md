**Design 1 is better.** It keeps one fact, the time each scan was taken. Design 2 turns the three tickets into three special-case rules, and those rules break when a refused pallet's scans arrive late.

**Constraints**
- C1: scans arrive late and out of order, from freezers, loading bays and the dock PC. Each scan carries a trusted time.
- C2: a pallet can be received again after a refusal, with the same barcode, so it has several lives.
- C3: scans are never edited or deleted, and volumes are small.

**Design 1** is a log ordered by time, and the location is a function of the latest scan. This is the shared concept behind #41, #47 and #49: arrival order is irrelevant, only the time the scan was taken matters.
- **#41:** a late move sorts before the shipped scan, so the pallet is still shipped.
- **#47:** a late receive sorts before the first move, so the move is still the latest scan.
- **#49:** moves are ordered by time.
- **Refusal:** received, moved, shipped, then received again gives DOCK, and a later move gives that location. The log handles this with no extra rule.
- **Late scans from an old life:** these sort into their own place in the log and cannot disturb a later life.

It has no branches for the tickets. Memory is bounded by the number of scans, which C3 says is small and never deleted.

**Design 2** keeps a mutable summary of `location`, `moved_at` and `shipped`, with one rule per ticket. I tried to break it with these cases:
- **Late shipped scan after a refusal.** Sequence: moved, shipped, received again, moved in F3, then the first-life shipped scan arrives late from the bay. It sets `location = None`, so a pallet that is physically in F3 disappears.
- **Late move from the first life.** A move taken before the first shipment arrives after the re-receive. `shipped` has been reset to False and `scan.at` is newer than the stale `moved_at`, so it overwrites the real location.
- **Late receive after shipping.** A receive scan arrives after the shipped scan and resets `shipped = False`, even though it is older. The next late move is then accepted.
- **Hidden ordering.** Receives and shipped scans are applied in arrival order, and `moved_at` orders only moves. This is the same fact stated twice, with different rules.

Each fix was a patch for one observed symptom, and none states the real invariant. Design 2 has three state fields and several exception clauses, and it fails C1 and C2 when they combine.

**Minor caveat for Design 1:** scans with equal timestamps fall back to arrival order. This is rare and affects Design 2 equally.

**Ledger**
- **Constraints:** C1 late and out-of-order scans, C2 re-receipt after refusal, C3 immutable scans and small volume.
- **Forced:** order by scan time, and derive the location from the latest scan.
- **Deletions in Design 1:** the `shipped` flag, `moved_at`, and the three ticket-specific rules.
- **Reasoning check:** Design 2 was rejected because it fails C1 and C2 together, not because it is longer.

WINNER: 1