# Candidate B

```python
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

TICKET = Decimal("64.00")
BOOKING_FEE = Decimal("2.00")
EARLY_BIRD_UNTIL = date(2027, 2, 28)
MAX_DISCOUNT = Decimal("0.30")

RULES = []  # (step, rule), run in step order


def rule(step):
    """Register a pricing rule; a new discount is one more decorated function."""
    def register(fn):
        RULES.append((step, fn))
        RULES.sort(key=lambda r: r[0])
        return fn
    return register


@dataclass
class Quote:
    order: object
    discounts: dict = field(default_factory=dict)  # name -> rate
    fees: Decimal = Decimal("0.00")


@rule(10)
def group(q):
    if q.order.tickets >= 6:
        q.discounts["group"] = Decimal("0.10")


@rule(10)
def member(q):
    if q.order.member:
        q.discounts["member"] = Decimal("0.20")


@rule(20)
def group_or_member(q):
    """Group and member discounts don't combine: keep the larger."""
    if "group" in q.discounts and "member" in q.discounts:
        del q.discounts[min("group", "member", key=q.discounts.get)]


@rule(30)
def early_bird(q):
    if q.order.placed_on <= EARLY_BIRD_UNTIL:
        q.discounts["early"] = Decimal("0.15")


@rule(90)
def booking_fee(q):
    q.fees += BOOKING_FEE


def price(order):
    """Amount charged: the tickets less discounts, plus fees (never discounted)."""
    q = Quote(order)
    for _, apply in RULES:
        apply(q)
    discount = min(sum(q.discounts.values(), Decimal(0)), MAX_DISCOUNT)
    tickets = order.tickets * TICKET * (1 - discount)
    return tickets.quantize(Decimal("0.01"), ROUND_HALF_UP) + q.fees
```
