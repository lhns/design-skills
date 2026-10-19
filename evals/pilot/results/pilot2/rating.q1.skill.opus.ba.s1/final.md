**Design 1 (Candidate B) is better.** It keeps the terms' promise that "your balance ends up as if you had not bought them." Design 2 breaks that promise whenever cents are involved.

**Constraints**
- **C1:** You earn `int(euros) × rate` per purchase, at the rate on the purchase day.
- **C2:** After a return, the balance equals what it would be had the returned items not been bought.
- **C3:** An order can receive several partial refunds.
- **C4:** Total refunds never exceed what was paid.
- **C5:** Balances may go negative.

**Trying to break Design 2 against C2**

Take an order of 21.20 at rate 1. It earns 21 points. The customer returns two books at 10.60 each.

- **First refund (10.60):**
  - The kept amount is 10.60, which should earn 10 points, so the balance should be 10.
  - Design 2 takes back `int(10.60) = 10` points, leaving 11. That is one point too many.
- **Second refund (10.60):**
  - The order is now fully refunded, so the balance should be 0.
  - Design 2 takes back 10 more, leaving 1. The customer keeps a point for a purchase they fully returned.

The cause is that truncation does not distribute over sums: `int(a) + int(b) ≠ int(a + b)`. Design 2 floors each refund on its own. The scheme floors the whole purchase. So Design 2 is wrong under C1, C2 and C3 together. Several refunds per order are the normal case here, so this is not an edge case.

**Design 1 against the same case**

Design 1 does not compute points for the refund amount. It computes the points for what the customer keeps after the refund, minus the points for what they kept before it.

- The adjustments telescope. After any sequence of refunds, the balance change sums to `points_for(paid − refunded) − points_for(paid)`.
- That is exactly C2's invariant: the balance equals the points for the amount actually kept.
- In the example, the refunds take back 11 and then 10 points, ending at 0.

**Counting concepts**

Design 1 adds `points_for` and `_add`. Both remove duplication rather than add cases:
- `points_for` is the single place where the earning rule is stated. Purchase and refund both use it, so they cannot drift apart. In Design 2 the rule is written twice, and the two copies already disagree in behaviour.
- `_add` handles the balance update in one place, which also means a refund for an unseen customer cannot raise a `KeyError`.

Neither design has extra exception clauses. Both validate C4 identically, and both allow negative balances (C5).

**Deciding reason:** Design 1 states the earning rule once and derives refunds as a difference of kept amounts, so C2 holds for any sequence of partial refunds. Design 2's per-refund truncation leaves customers with points they should not have.

WINNER: 1