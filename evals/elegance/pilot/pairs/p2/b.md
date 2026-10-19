# Candidate B

```python
from datetime import date, datetime, timedelta

VALID_SITES = {"N1", "S2", "W3"}


def _check(code: str) -> None:
    if code not in VALID_SITES:
        raise ValueError(f"unknown site: {code}")


def is_valid_site(code: str) -> bool:
    return code in VALID_SITES


def packing_label(code: str) -> str:
    _check(code)
    return {"N1": "North / Lakeside", "S2": "South / Harbour", "W3": "West / Ridge"}[code]


def carrier_for(code: str) -> str:
    _check(code)
    return "Courier Beta" if code == "W3" else "Courier Alpha"


def ship_date(code: str, ordered_at: datetime) -> date:
    _check(code)
    day = ordered_at.date()
    if ordered_at.hour >= (14 if code == "S2" else 16):
        day += timedelta(days=1)
    while day.weekday() == 6 or (day.weekday() == 5 and code != "W3"):
        day += timedelta(days=1)
    return day
```
