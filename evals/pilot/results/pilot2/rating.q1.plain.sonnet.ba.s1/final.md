**Design 1 is better.** Its refunds always leave the balance at exactly what the remaining purchase would have earned, which is what the terms promise ("your balance ends up as if you had not bought them").

**Why Design 2 fails**

Design 2 takes back `int(amount) * rate` on each refund separately. Because points are earned on whole euros, flooring each refund on its own doesn't add up to the same result as flooring the total, and the shop manager said an order can get several refunds over a few weeks.

- Order of 10.00 at rate 1 earns 10 points. Two refunds of 0.50 take back 0 points each. The whole 1.00 is refunded, yet the customer keeps all 10 points, and the same happens for any run of sub-euro refunds.
- Two refunds of 1.50 take back 1 + 1 = 2 points. The remaining 7.00 earns only 7, so 3 points should have been taken back, and the customer keeps 1 too many.
- Refunding a 9.99 book out of a larger order works, but small refunds can leak points, and a fully refunded order may not return to zero.

The result also depends on how the refund is split, which is a sign the design is wrong.

**Why Design 1 works**

- It computes points on the amount kept before the refund and the amount kept after it, and applies the difference. The differences telescope, so the total taken back over any sequence of refunds equals `points(paid) - points(paid - total_refunded)`. It doesn't matter how the refunds are split or ordered.
- A full refund leaves the kept amount at 0, so all the points are removed exactly.
- It uses the order's stored `rate`, which is the rate on the purchase day, as the manager required.
- It re-checks that the refund is positive and at most what is left on the order, as the developer asked.
- The check runs before the order is mutated, so a rejected refund leaves no partial state.
- Negative balances are allowed, which matches the shop's policy.
- Extracting `points_for` keeps the earning rule in one place, so `purchase` and `refund` can't drift apart.

WINNER: 1