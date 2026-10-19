**Design 2 is better.** The terms say a return should leave the balance "as if you had not bought them". Points are earned on whole euros of the amount kept, so a refund must take back the difference in points before and after. Design 1 instead takes back points on the refunded amount alone, and that comes out wrong whenever cents are involved.

**Where Design 1 goes wrong:**

- **Cents in a single refund.** An order paid 30.50 at rate 1 earns 30 points. A refund of 10.75 leaves 19.75 kept, which is worth 19 points. So 11 points should come back, but Design 1 takes back `int(10.75) = 10`. The customer keeps one point they shouldn't have.
- **Several partial refunds.** The manager says an order can get several refunds over a few weeks, so the truncation error adds up. In an extreme case, a 30.00 order refunded entirely in 0.50 pieces loses 0 points per refund. The customer ends up with all 30 points and nothing bought. A realistic case: three refunds of 9.99 on a 29.97 order. Each takes back 9 points, so 27 in total. The correct answer is 29 points, because nothing is kept.
- **Double Points Days.** Rate 2 doubles every one of these errors.

**How Design 2 handles it:**

- **It computes the correct total.** Each refund changes the balance by `points_for(kept_after) - points_for(kept_before)`. Summed over any sequence of refunds, the changes add up to exactly `points_for(final kept) - points_for(paid)`. The balance always equals what the kept part of the order would have earned, which is what the terms require.
- **It keeps the rate from the purchase day.** It uses `order.rate`, as the manager asked, and Design 1 does too.
- **It defines the earning rule once.** Both `purchase` and `refund` use `points_for`, so they can't drift apart if the rule changes later.
- **It handles an unknown customer safely.** `_add` uses `.get(customer, 0)`. Design 1's `-=` would raise `KeyError` for a customer with no balance entry. Such an order shouldn't normally exist, but Design 2 is more robust.

Both designs validate the refund against what is left on the order, as the old system's developer asked. Both allow negative balances, which the manager accepts.

WINNER: 2