# Candidate A

```python
from datetime import datetime, time, timedelta

# (start, end, cents per minute). The bands tile the day; end <= start means the next day.
BANDS = [
    (time(6), time(22), 5),
    (time(22), time(6), 2),
]


def price(entry: datetime, exit: datetime) -> int:
    """Each band occurrence's overlap with the stay, in minutes, times its rate."""
    total = 0
    day = entry.date() - timedelta(days=1)  # a night band that began the evening before entry
    while day <= exit.date():
        for start, end, rate in BANDS:
            band_start = datetime.combine(day, start)
            band_end = datetime.combine(day + timedelta(days=1 if end <= start else 0), end)
            overlap = min(band_end, exit) - max(band_start, entry)
            if overlap > timedelta(0):
                total += int(overlap.total_seconds()) // 60 * rate
        day += timedelta(days=1)
    return total
```
