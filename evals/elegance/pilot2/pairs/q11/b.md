# Candidate B

```python
from datetime import date, timedelta

# School holidays as published by the council, (first, last) inclusive.
# Add a school year when the council confirms it.
HOLIDAYS = [
    # 2025-26
    (date(2025, 10, 27), date(2025, 10, 31)),
    (date(2025, 12, 22), date(2026, 1, 2)),
    (date(2026, 2, 16), date(2026, 2, 20)),
    (date(2026, 3, 30), date(2026, 4, 10)),
    (date(2026, 5, 25), date(2026, 5, 29)),
    (date(2026, 7, 20), date(2026, 8, 31)),
    # 2026-27
    (date(2026, 10, 26), date(2026, 10, 30)),
    (date(2026, 12, 21), date(2027, 1, 1)),
    (date(2027, 2, 22), date(2027, 2, 26)),
    (date(2027, 3, 22), date(2027, 4, 2)),
    (date(2027, 5, 31), date(2027, 6, 4)),
    (date(2027, 7, 21), date(2027, 8, 31)),
]


def club_days(first, last):
    days = []
    d = first
    while d <= last:
        if d.weekday() < 5 and any(a <= d <= b for a, b in HOLIDAYS):
            days.append(d)
        d += timedelta(days=1)
    return days
```
