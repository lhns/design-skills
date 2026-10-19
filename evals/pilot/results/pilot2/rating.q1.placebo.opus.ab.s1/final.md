**Design 2 is better.** The deciding issue is correctness: Design 1 truncates each refund on its own, so the customer can end up with the wrong balance.

**What the terms require.** "Your balance ends up as if you had not bought them." After any set of refunds, the points left from an order should equal the points the *remaining* amount would have earned: `int(paid − refunded) × rate`. Truncating to whole euros does not distribute over subtraction, so `int(a) − int(b) ≠ int(a − b)` in general.

**Where Design 1 goes wrong.** It takes back `int(amount) × rate` for each refund on its own:

- Order paid 20.00 (20 pts), refund 10.50: Design 1 removes 10, leaving 10. The kept amount is 9.50, which earns 9. The customer keeps 1 point too many.
- Order paid 30.00, refunds of 10.50 and then 9.50: Design 1 removes 10 + 9 = 19, leaving 11. The kept 10.00 earns 10.
- A full refund in several parts (e.g. 30.00 as 10.50 + 10.50 + 9.00) removes 10 + 10 + 9 = 29 and leaves 1 point on a fully returned order.

The manager said orders routinely get several partial refunds of exact book prices, which are rarely whole euros. So this error is the normal case, not an edge case. The points also slowly leak in the customer's favour, and 100 points are worth 1.00.

**How Design 2 gets it right.** It computes the points kept before and after the refund and applies the difference. Many refunds add up to the same result as one equal refund. A full refund always returns the order's points to exactly zero, whatever the cents. The rule "whole euros × rate" lives in one place (`points_for`), shared by purchase and refund, so the two cannot drift apart. That is DRY applied to an actual business rule.

**Smaller points:**

- Both store the purchase-day rate on the order, which matches the manager's rule about Double Points Days.
- Both check the refund ceiling in the module, as the old developer asked.
- Both allow negative balances, as the manager allows.
- Design 2's `_add` also handles a customer with no entry yet. Design 1's `refund` would raise `KeyError` there, which can't happen if purchase always runs first, but it's slightly sturdier.
- Design 2 is a few lines longer, and that extra code carries the rule. It isn't speculative.

One gap shared by both: neither has tests. A test with split, non-whole-euro refunds that sum to the full order is the one that tells these two designs apart, and it should be in the suite.

WINNER: 2