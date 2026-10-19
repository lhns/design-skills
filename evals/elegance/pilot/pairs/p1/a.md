# Candidate A

```python
from datetime import timedelta

VALIDITY = timedelta(days=90)


class Ledger:
    def __init__(self):
        self.grants = []  # [expires, hours] pairs
        self.spent = {}   # spend id -> (hours, expiry to refund with)

    def grant(self, hours, at):
        self.grants.append([at + VALIDITY, hours])

    def balance(self, at):
        return sum(h for expires, h in self.grants if expires > at)

    def spend(self, spend_id, hours, at):
        if hours <= 0 or hours > self.balance(at):
            raise ValueError("invalid or insufficient credit")
        self.grants.sort()
        left, first = hours, None
        for g in self.grants:
            if g[0] > at and g[1] and left:
                take = min(g[1], left)
                g[1] -= take
                left -= take
                first = first or g[0]
        # Hours are drawn soonest-expiry first, so refunding them all with the
        # first grant's expiry never lets a refund outlive the credit it replaces.
        self.spent[spend_id] = (hours, first)

    def refund(self, spend_id, at):
        hours, expires = self.spent.pop(spend_id)
        if expires > at:
            self.grants.append([expires, hours])
```
