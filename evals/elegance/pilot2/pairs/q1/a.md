# Candidate A

```python
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Order:
    customer: str
    paid: Decimal                 # amount paid for the whole order
    rate: int                     # points per whole euro on the purchase day (1, or 2 on Double Points Days)
    refunded: Decimal = Decimal("0.00")


class Points:
    def __init__(self):
        self.balances = {}        # customer -> points, may go below zero

    def purchase(self, order):
        earned = int(order.paid) * order.rate
        self.balances[order.customer] = self.balances.get(order.customer, 0) + earned

    def refund(self, order, amount):
        """Record a refund on the order and take back the points earned on the refunded amount."""
        if amount <= 0 or order.refunded + amount > order.paid:
            raise ValueError("refund must be positive and at most what is left on the order")
        order.refunded += amount
        self.balances[order.customer] -= int(amount) * order.rate
```
