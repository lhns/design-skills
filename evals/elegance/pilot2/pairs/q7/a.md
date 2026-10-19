# Candidate A

```python
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

TICKET = Decimal("64.00")
BOOKING_FEE = Decimal("2.00")
EARLY_BIRD_UNTIL = date(2027, 2, 28)
MAX_DISCOUNT = Decimal("0.30")


def price(order):
    """Amount charged: the tickets less discounts, plus the booking fee (never discounted)."""
    # Group and member discounts don't combine: the larger one applies.
    discount = max(
        Decimal("0.10") if order.tickets >= 6 else Decimal(0),
        Decimal("0.20") if order.member else Decimal(0),
    )
    # Early bird combines with either.
    if order.placed_on <= EARLY_BIRD_UNTIL:
        discount += Decimal("0.15")
    discount = min(discount, MAX_DISCOUNT)
    tickets = order.tickets * TICKET * (1 - discount)
    return tickets.quantize(Decimal("0.01"), ROUND_HALF_UP) + BOOKING_FEE
```
