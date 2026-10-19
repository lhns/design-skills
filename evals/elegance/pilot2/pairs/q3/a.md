# Candidate A

```python
from datetime import timedelta
from decimal import Decimal

# Rent counts as overdue once it is still unpaid seven days after its due date
# (tenancy agreement, clause 4.3).
OVERDUE_AFTER = timedelta(days=7)
LATE_FEE = Decimal("15.00")


def is_overdue(charge, today):
    return not charge.paid and today >= charge.due + OVERDUE_AFTER


def dashboard(charges, today):
    """Charges shown on the treasurer's arrears dashboard."""
    return [c for c in charges if is_overdue(c, today)]


def reminders_due(charges, today):
    """Charges whose household gets the friendly reminder letter today."""
    return [c for c in charges if is_overdue(c, today) and not c.reminded]


def late_fees_due(charges, today):
    """(charge, fee) pairs to post today, at most one fee per charge."""
    return [(c, LATE_FEE) for c in charges if is_overdue(c, today) and not c.fee_charged]
```
