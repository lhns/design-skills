# Candidate A

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


# (budget code, reporting line, valid from). Rhea adds a row when a code moves;
# rows are never edited or removed.
MAPPING = [
    ("PRG-SESSIONS", "Programme delivery", date(2024, 4, 1)),
    ("PRG-VENUES", "Programme delivery", date(2024, 4, 1)),
    ("VOL-TRAVEL", "Volunteer expenses", date(2024, 4, 1)),
    ("VOL-SUBS", "Volunteer expenses", date(2024, 4, 1)),
    ("ADM-AUDIT", "Governance", date(2024, 4, 1)),
    ("ADM-INSURE", "Core costs", date(2024, 4, 1)),
]


def line_for(code, on):
    """The reporting line of `code` for an expense made on `on`."""
    starts = [(start, line) for c, line, start in MAPPING if c == code and start <= on]
    if not starts:
        raise KeyError(f"no reporting line for {code} on {on}")
    return max(starts)[1]


def quarterly_report(expenses, first_day, last_day):
    """Totals per reporting line for expenses made between the two dates, inclusive."""
    totals = defaultdict(Decimal)
    for e in expenses:
        if first_day <= e.spent_on <= last_day:
            totals[line_for(e.code, e.spent_on)] += e.amount
    return dict(sorted(totals.items()))
```
