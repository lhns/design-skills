**Design 1 is better. It keeps the constraint that the balance ends up as if the refunded items had not been bought, and Design 2 breaks it.**

**Constraints**
- C1: Points are `floor(euros) × rate` on a single purchase, so rounding happens once, on the whole order.
- C2: After a refund, the balance must be as if the returned items had not been bought.
- C3: One order can get several partial refunds, and the rate is the one on the purchase day. Both designs store that rate on the order.
- C4: Balances may go negative.
- C5: The refund must be positive and at most what is left on the order.

**Breaking Design 2 (C1, C2):** it deducts `floor(amount) × rate`, so it rounds each refund separately instead of rounding the order once.
- Order paid 37.40 at rate 1 earns 37 points. Refunding a 12.50 book takes back 12, leaving 25. Had the book never been bought, the order would be 24.90, which earns 24 points. The balance is off by one.
- Order paid 1.00 and refunded as 0.50 + 0.50. Each refund takes back `floor(0.50) = 0` points. The order is fully refunded but the customer keeps 1 point, which contradicts C2.
- The error depends on how the refunds are split, so the same total refunded can give different balances.
- It also does `self.balances[order.customer] -= ...` without a default. If the customer has no entry, for example after a restart or on a fresh `Points` object, this raises `KeyError`.

**Why Design 1 holds (C1, C2, C3):** it takes back `points_for(kept_before) − points_for(kept_after)`. These differences telescope across any sequence of refunds, so the total taken back is `points_for(paid) − points_for(paid − total_refunded)`.
- The balance depends only on what remains of the order, not on the order or size of the refunds.
- A fully refunded order nets exactly zero.
- The rate is applied at the purchase-day value, as required.
- A single `points_for` holds the earning rule, so `purchase` and `refund` cannot disagree about it. Design 2 states the rule in two places and the copies diverge.
- `_add` handles a missing balance, and it works naturally with negative balances (C4).

Both designs make the same validity check (C5). Design 1's extra concepts, `points_for` and `_add`, are each forced: the first by C1 and C2, the second by the missing-key case.

**Ledger**
- Constraints: C1–C5 above.
- Forced: compute refund points as the difference of the points on the remaining amount, so the earning rule is stated once.
- Designer choices: none added.
- Deletions: Design 1 removes the duplicated earning rule and the `KeyError` case. Design 2's apparent simplicity comes from dropping C2.

WINNER: 1