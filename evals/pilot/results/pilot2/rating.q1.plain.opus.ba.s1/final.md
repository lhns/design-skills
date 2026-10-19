**Design 1 (Candidate B) is the better design.** It is the only one that meets the rule on the card: *"your balance ends up as if you had not bought them."*

**Why Design 2 fails**

Design 2 takes back `int(amount) * rate` for each refund. Points were earned by rounding down the *whole order*, so rounding down each *refund* on its own does not undo them. The manager says the common case is partial refunds, sometimes several per order. That is exactly where the error builds up.

- **Three books at 9.99, all returned one at a time.** The order is 29.97, which earns 29 points. Each refund takes back `int(9.99) = 9`, so 27 in total. The customer keeps **2 points** for an order fully refunded. Design 1 ends at `points_for(0) = 0`.
- **Order of 30.50, refund 10.75.** The kept amount is 19.75, which should be worth 19 points, so 11 should be removed. Design 2 removes only 10.
- **Order of 20.00, two refunds of 0.50.** The kept amount is 19.00, worth 19 points. Design 2 removes 0 each time and leaves 20.

The error always favours the customer. With repeated small refunds it can be exploited, and it breaks the stated terms.

**Why Design 1 is right**

On each refund, Design 1 works out the points owed on what the customer still keeps, before and after the refund, and applies the difference:

`points_for(kept_after) - points_for(kept_before)`

The running total therefore always equals `points_for(paid - refunded, rate)`. That is exactly "as if you had not bought them," however the refunds are split. It also:

- uses the purchase-day `rate` stored on the order, as the manager asked;
- validates the refund against what is left on the order, as the old system's developer asked;
- lets balances go negative.

It also keeps the earning rule in one place (`points_for`), shared by `purchase` and `refund`. If the rule changes, the two cannot drift apart.

Both designs mutate `order.refunded` before adjusting the balance, and neither is atomic. That is a minor point and the same in both.

WINNER: 1