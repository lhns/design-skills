# Candidate A

```python
import re
from datetime import timedelta

# Long enough to catch a re-sent invoice, short enough that suppliers who restart
# their numbering each January don't clash with last year's invoices.
DUPLICATE_WINDOW = timedelta(days=60)


def normalise(number):
    """'INV-0045', 'inv-0045 ' and '45' all become '45'."""
    digits = re.sub(r"\D", "", number)
    return digits.lstrip("0") or "0"


def possible_duplicates(new, existing):
    """Earlier invoices that `new` should be held against until finance checks it."""
    return [
        e for e in existing
        if e.supplier_id == new.supplier_id
        and normalise(e.number) == normalise(new.number)
        and abs(new.received_on - e.received_on) <= DUPLICATE_WINDOW
    ]
```
