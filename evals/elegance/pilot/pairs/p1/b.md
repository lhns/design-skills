# Candidate B

```python
from dataclasses import dataclass, field
from datetime import datetime, timedelta

VALIDITY = timedelta(days=90)


@dataclass
class Grant:
    hours: int
    expires: datetime


@dataclass
class Spend:
    taken: list = field(default_factory=list)  # (grant, hours taken from it)


class Ledger:
    def __init__(self):
        self.grants = []
        self.spends = {}  # spend id -> Spend

    def grant(self, hours, at):
        self.grants.append(Grant(hours, at + VALIDITY))

    def balance(self, at):
        return sum(g.hours for g in self._live(at))

    def spend(self, spend_id, hours, at):
        if hours <= 0:
            raise ValueError("spend must be positive")
        if hours > self.balance(at):
            raise ValueError("insufficient credit")
        spend = Spend()
        left = hours
        for g in sorted(self._live(at), key=lambda g: g.expires):
            take = min(g.hours, left)
            if take:
                g.hours -= take
                spend.taken.append((g, take))
                left -= take
            if not left:
                break
        self.spends[spend_id] = spend

    def refund(self, spend_id, at):
        """Return each hour to the grant it came from; hours of expired grants are lost."""
        for g, hours in self.spends.pop(spend_id).taken:
            if g.expires > at:
                g.hours += hours

    def _live(self, at):
        return [g for g in self.grants if g.expires > at]
```
