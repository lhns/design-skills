**Design 1 (Candidate B) is better.** Each scan records when it was taken, and the handheld clocks are synced. So the correct location is whatever the most recent scan by time says, regardless of upload order. Candidate B does exactly that: it keeps each pallet's scans sorted by `at` and reads the latest one. Late uploads (#41, #47, #49) and refused-and-returned pallets all come out right without special cases.

**Candidate A** handles events in arrival order and patches each known ticket with its own rule. Those rules break as soon as they meet each other or the return flow.

**Late receive after shipping.** A pallet is received, moved and shipped the same day. The dock PC uploads the receive at the end of the shift (#47).
- A sets `shipped = False` and `location = "DOCK"`.
- The pallet appears to be on the dock even though it left on a lorry.

**Late shipped scan for a refused pallet.** The sequence is: shipped at 10:00, refused, received again at 14:00, moved to F2-14 at 14:30.
- The loading-bay handheld uploads the 10:00 shipped scan at 15:00.
- A sets `location = None` and `shipped = True`, so a pallet sitting in F2 shows as gone.
- Then the dock receive arrives at the end of the shift. It clears `shipped` and puts the pallet on DOCK, which is still wrong.

**The #41 rule blocks real moves.** After a ship scan has been applied, A ignores every later-arriving move until a receive turns up. For a returned pallet, the receive is typically uploaded last (end of shift). So genuine put-away moves after the return are thrown away.

**Receives and ships ignore time.** Only moves are compared by time (`moved_at`). Receive and ship scans are applied without any time check, so any late arrival of one of them can overwrite newer information.

B's costs are small at this volume. It stores every scan, which is trivial at a few thousand a day, and scans are never edited, so the stored history stays valid. The only open question is how to order two scans with identical timestamps. A secondary sort key would settle that.

WINNER: 1