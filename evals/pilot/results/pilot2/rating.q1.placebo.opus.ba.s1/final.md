**Design 1 (Candidate B) is better.** It is the one that actually implements the scheme's terms.

**The requirement that decides it:** "we take back the points you earned on them, so that your balance ends up as if you had not bought them." After any sequence of refunds, the customer's points for an order must equal what they would have earned by paying only the kept amount: `int(paid - refunded) * rate`.

**Design 1** computes exactly that. On each refund it takes the difference between the points for the kept amount before and after. The adjustments telescope, so after any number of partial refunds the order has contributed `points_for(kept, rate)`. That is the stated invariant.

**Design 2** floors each refund on its own (`int(amount) * rate`). Flooring isn't additive, so the result drifts from the invariant, and it always drifts in the customer's favour:

- Paid 30.00, refund 9.99. Design 2 takes back 9 points and leaves 21. Kept is 20.01, which should earn 20. Design 1 leaves 20.
- Paid 25.50, refunded fully as 12.75 + 12.75. Design 2 takes back 12 + 12 = 24 of the 25 earned, so 1 point survives a full return. Design 1 ends at 0.
- Any refund under 1.00 takes back nothing. Repeated small refunds leak points indefinitely.

The manager said orders "can get several refunds over a few weeks", and book prices are rarely whole euros. So this isn't an edge case; it is the normal path. Points are money (100 = 1.00), so the error is a real financial leak.

**Smaller design points, also favouring Design 1:**
- The earning rule `int(amount) * rate` lives in one place, `points_for`. Purchase and refund can't disagree about how points are computed. Design 2 duplicates the rule inline.
- `_add` centralises the balance update. Design 2's `refund` uses `self.balances[order.customer] -= ...`, which would raise `KeyError` for a customer missing from `balances`. Design 1's `get(..., 0)` path is uniform.
- Both validate the refund amount correctly and use the purchase-day rate stored on the order. They are equal on those requirements.

**Minor nits on Design 1** (not blocking): `refund` mutates `order` before updating the balance, which is fine single-threaded but worth noting. A test asserting "full refund in N parts leaves balance at the pre-purchase value" would lock in the key invariant.

WINNER: 1