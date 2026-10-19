**Constraints**
- C1: Points are earned per whole euro of one purchase (floor of the order total × rate). Stated in the terms.
- C2: After returns, the balance ends up as if the returned items had not been bought. Stated in the terms.
- C3: The purchase-day rate applies, not the return-day rate. Stated by the manager. Both designs store the rate on the order.
- C4: Several partial refunds can hit one order. Stated by the manager.
- C5: Balances may go negative. Both designs allow it.
- C6: Refunds must be positive and at most what is left on the order. Stated by the developer. Both designs check this.

**Try to break A**

Take an order paid at 19.99 with rate 1. The purchase earns int(19.99) = 19 points.
- Refund 10.50 and then 9.49. A takes back int(10.50) + int(9.49) = 10 + 9 = 19. That is correct here, but only by luck.
- Refund 0.50 and then 19.49. The total refunded is 19.99, so everything is returned. A takes back 0 + 19 = 19. This one is also fine.
- Refund 9.99 twice on a 19.98 order. The purchase earns 19. A takes back 9 + 9 = 18, which leaves 1 point from an order that was fully returned. This breaks C2.
- Refund 0.99 on a 1.98 order, then 0.99 again. The purchase earns 1. A takes back 0 + 0 = 0, so the order is fully returned and the customer keeps 1 point.

The cause is that flooring each refund separately differs from flooring the total. A cannot meet C2 under C4, and the error grows with repeated refunds. A single small refund of 0.50 on a 3.00 order also takes back 0 points, which is arguably right, but A has no way to show that it is consistent with the other cases.

**Try to break B**

B computes the points on the kept amount before and after each refund, so the total taken back is always points_for(paid) − points_for(kept_now). Each refund telescopes into the next one.
- After a full return, kept is 0, so the balance change over the order's life is exactly zero (C2).
- After any sequence of partial refunds, the net points equal int(kept) × rate. This is the points the remaining items would have earned on their own. The result is independent of how the refunds were split or ordered (C4).
- The rate comes from the order (C3).
- Order 19.99 refunded 0.50: kept goes from 19.99 to 19.49, so 19 → 19 and nothing is taken back. This is consistent with the floor rule.
- Negative balances work, because `_add` has no floor (C5).
- I found no input that breaks B.

One remaining question is whether the "kept" model is the right reading of "as if you had not bought them". The terms say the balance ends up as if the items had not been bought. That is a statement about the end state. B satisfies it exactly for full returns and, for partial returns, gives the floor of what remains. That is the natural reading. If the shop meant to take back per-book points instead, we would need item-level data, which the module does not receive.

**Concept count**
- A has one formula written in two places: `int(x) * rate` in `purchase` and in `refund`. B states it once, in `points_for`, so a change to the earning rule changes one place.
- B adds `_add`, which removes the duplicated dictionary update. It also adds two local variables. These carry the invariant and are forced by C2 and C4.
- A is shorter, but it is shorter because it drops C2 for partial refunds.

**Deciding reason:** B keeps the invariant that the balance depends only on what remains of the order, so C2 holds under any sequence of partial refunds (C4), while A floors each refund separately and leaves stray points behind.

**Ledger**
- Constraints: C1–C6 above, all stated.
- Forced decisions: compute the refund's points as the difference between points on the kept amount before and after. The earning rule appears once.
- Designer choices: `_add` helper (convenience only, not forced by any constraint).
- Deletions: the duplicated earning formula and the per-refund flooring.

WINNER: 2