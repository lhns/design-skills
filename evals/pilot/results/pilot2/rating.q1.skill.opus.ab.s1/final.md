# Design 2 is better

**Deciding reason:** Design 2 keeps the invariant the terms require, and Design 1 breaks it whenever refund amounts have cents.

## The governing constraint

The terms say: "we take back the points you earned on them, so that your balance ends up as if you had not bought them."

Points are earned per *whole euro spent in one purchase*. So after any number of refunds, the points an order has contributed must equal the points that the kept amount would have earned:

> points from order = `int(paid − refunded) × rate`

Both designs meet the other constraints equally well:
- the rate comes from the purchase day (`order.rate`);
- refunds are bounded;
- several refunds per order are recorded;
- balances can go negative.

## Breaking Design 1

Design 1 takes back `int(amount) × rate` for each refund on its own. Truncation does not distribute over subtraction, so it drifts:

- **Single refund with cents:** the order is paid 30.50 and 10.75 is refunded. The kept amount is 19.75, which should earn 19 points. Design 1 removes 10 points and leaves 20, one point too many.
- **Several small refunds:** this is the manager's typical case. The order is paid 20.00, then refunded 0.50 and later another 0.50. The kept amount is 19.00, which should earn 19 points. Design 1 removes 0 + 0 and leaves 20. Every refund under 1.00 removes nothing, however many there are.
- **Full refund in pieces:** the order is paid 10.00 and refunded 4.50 and then 5.50. The balance should go back to 0. Design 1 removes 4 + 5 = 9 and leaves 1 point for a fully returned order.

Since points are spendable like money, this is real value leaking. It is a failure of a stated constraint, not a style issue.

## Why Design 2 holds

Each refund adjusts the balance by `points_for(kept_after) − points_for(kept_before)`. These differences telescope. After any sequence of refunds, the order's net contribution is exactly `points_for(paid − refunded)`. That is the invariant, and it holds by construction for any number of partial refunds.

## Concept count

The extra pieces in Design 2 are justified:
- `points_for` states the earning rule once and both operations reuse it. Design 1 states the rule twice, and its second statement is the wrong one.
- `_add` removes a duplicated balance update. It also handles a refund for a customer missing from `balances` without a `KeyError`.

Design 2 is a few lines longer. Every addition traces to the "as if you had not bought them" constraint, and Design 1 is shorter only because it drops that constraint.

WINNER: 2