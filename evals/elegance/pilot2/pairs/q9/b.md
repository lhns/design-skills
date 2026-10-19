# Candidate B

```python
import re


def normalise(number):
    """'INV-0045', 'inv-0045 ' and '45' all become '45'."""
    digits = re.sub(r"\D", "", number)
    return digits.lstrip("0") or "0"


def same_invoice_year(a, b):
    """A supplier never reuses a number within the year printed on its invoices;
    some start again from 0001 each January. A missing date can't rule a match out."""
    if a.invoice_date is None or b.invoice_date is None:
        return True
    return a.invoice_date.year == b.invoice_date.year


def possible_duplicates(new, existing):
    """Earlier invoices that `new` should be held against until finance checks it."""
    return [
        e for e in existing
        if e.supplier_id == new.supplier_id
        and normalise(e.number) == normalise(new.number)
        and same_invoice_year(e, new)
    ]
```
