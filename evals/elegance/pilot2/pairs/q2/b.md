# Candidate B

```python
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Expense:
    code: str
    spent_on: date
    amount: Decimal


# Budget code -> reporting line. Rhea edits this when a code moves; every report
# reads it at run time, so the app has one answer for where a code belongs.
MAPPING = {
    "PRG-SESSIONS": "Programme delivery",
    "PRG-VENUES": "Programme delivery",
    "VOL-TRAVEL": "Volunteer expenses",
    "VOL-SUBS": "Volunteer expenses",
    "ADM-AUDIT": "Governance",
    "ADM-INSURE": "Core costs",
}


def quarterly_report(expenses, first_day, last_day):
    """Totals per reporting line for expenses made between the two dates, inclusive."""
    totals = defaultdict(Decimal)
    for e in expenses:
        if first_day <= e.spent_on <= last_day:
            totals[MAPPING[e.code]] += e.amount
    return dict(sorted(totals.items()))
```
