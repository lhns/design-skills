**Design 1 is the better design.** It is the only one that meets constraint 4.

**Design 1 (per-grant tracking)**
- Each spend records `(grant, hours taken)` for every grant it drew from. A refund returns the hours to those same grants, so each hour keeps its original expiry.
- Expiry is checked per grant at refund time. Hours from grants that have expired are dropped, while hours from grants that are still live are returned. That is exactly what constraint 4 asks for.
- A spend that fails validation raises before any mutation, so it changes nothing (constraint 3).
- Spends consume the soonest-expiring grants first, and `expires > at` is used consistently for expiry.
- Its weaknesses are minor: it doesn't reject a duplicate `spend_id` (the old record is overwritten), it raises a bare `KeyError` on an unknown or already-refunded id, and `grant` doesn't validate that hours are positive. All of these are easy to fix.

**Design 2 (single expiry per spend)**
- It stores one `(hours, first expiry)` pair per spend and refunds all hours with the earliest expiry among the grants used. The code comment claims this is safe because the refund "never outlives the credit it replaces". That is true, but it is not what the spec requires.
- It violates "each hour goes back to the grant it was taken from and keeps that grant's expiry." Hours taken from a later-expiring grant come back with an earlier expiry, so the customer loses credit.
- Example: a spend takes 1 hour from a grant expiring on day 90 and 1 hour from a grant expiring on day 170. If the refund happens on day 100, Design 2 discards both hours because `first` is day 90. The correct result returns the day-170 hour.
- Even when the refund happens before any expiry, the refunded hours later expire too early, so the balance at later times is wrong.
- It also has the same missing-id and duplicate-id weaknesses, and its sort-based mutation of `self.grants` is more fragile.

Design 2 is shorter, but it gets the core refund semantics wrong. Design 1 is correct and a bit more verbose.

WINNER: 1