# Candidate B

```python
import math
from datetime import date, time, timedelta

OPENS = time(10, 0)
LATEST_CLOSE = 19 * 60  # minutes; staff shifts end by 19:30 (visitor policy, section 2)


def last_sunday(year, month):
    d = date(year, month + 1, 1) - timedelta(days=1)
    return d - timedelta(days=(d.weekday() + 1) % 7)


def sunset(day):
    """Approximate sunset at the garden (52 N), local clock time, in minutes after midnight."""
    n = day.timetuple().tm_yday
    gmt = 1071 + 105 * math.sin(2 * math.pi * (n - 81) / 365)
    summer_time = last_sunday(day.year, 3) <= day < last_sunday(day.year, 10)
    return gmt + (60 if summer_time else 0)


def hours_on(day):
    """Visitor policy, section 2: an hour before sunset, rounded down to the half hour,
    no later than 19:00, set for the whole month (taken mid-month)."""
    closes = min(LATEST_CLOSE, (sunset(day.replace(day=15)) - 60) // 30 * 30)
    h, m = divmod(int(closes), 60)
    return OPENS, time(h - 1, m), time(h, m)
```
