# Candidate A

```python
from datetime import time

OPENS = time(10, 0)

# Closing time by month, as set by the trustees and printed on the leaflet and gate boards.
CLOSES = {
    1: time(15, 0), 2: time(15, 30), 3: time(16, 30), 4: time(18, 30),
    5: time(19, 0), 6: time(19, 0), 7: time(19, 0), 8: time(18, 30),
    9: time(18, 0), 10: time(17, 0), 11: time(15, 0), 12: time(15, 0),
}


def hours_on(day):
    closes = CLOSES[day.month]
    return OPENS, time(closes.hour - 1, closes.minute), closes
```
