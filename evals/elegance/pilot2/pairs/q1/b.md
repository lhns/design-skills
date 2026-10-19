# Candidate B

```python
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Order:
    customer: str
    paid: Decimal                 # amount paid for the whole order
    rate: int                     # points per whole euro on the purchase day (1, or 2 on Double Points Days)
    refunded: Decimal = Decimal("0.00")


def points_for(amount, rate):
    """Points a purchase of `amount` earns: whole euros times the day's rate."""
    return int(amount) * rate


class Points:
    def __init__(self):
        self.balances = {}        # customer -> points, may go below zero

    def purchase(self, order):
        self._add(order.customer, points_for(order.paid, order.rate))

    def refund(self, order, amount):
        """Record a refund on the order and take back the points for the refunded part."""
        if amount <= 0 or order.refunded + amount > order.paid:
            raise ValueError("refund must be positive and at most what is left on the order")
        kept_before = order.paid - order.refunded
        order.refunded += amount
        kept_after = order.paid - order.refunded
        self._add(order.customer, points_for(kept_after, order.rate) - points_for(kept_before, order.rate))

    def _add(self, customer, points):
        self.balances[customer] = self.balances.get(customer, 0) + points
```
