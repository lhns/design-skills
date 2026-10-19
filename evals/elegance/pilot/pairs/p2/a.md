# Candidate A

```python
from dataclasses import dataclass
from datetime import date, datetime, timedelta


@dataclass(frozen=True)
class Site:
    label: str            # printed on packing slips
    carrier: str
    cutoff_hour: int      # local; orders at or after it ship the next shipping day
    ships_saturday: bool


SITES = {
    "N1": Site("North / Lakeside", carrier="Courier Alpha", cutoff_hour=16, ships_saturday=False),
    "S2": Site("South / Harbour", carrier="Courier Alpha", cutoff_hour=14, ships_saturday=False),
    "W3": Site("West / Ridge", carrier="Courier Beta", cutoff_hour=16, ships_saturday=True),
}


def site(code: str) -> Site:
    try:
        return SITES[code]
    except KeyError:
        raise ValueError(f"unknown site: {code}") from None


def is_valid_site(code: str) -> bool:
    return code in SITES


def packing_label(code: str) -> str:
    return site(code).label


def carrier_for(code: str) -> str:
    return site(code).carrier


def ship_date(code: str, ordered_at: datetime) -> date:
    s = site(code)
    day = ordered_at.date()
    if ordered_at.hour >= s.cutoff_hour:
        day += timedelta(days=1)
    while day.weekday() == 6 or (day.weekday() == 5 and not s.ships_saturday):
        day += timedelta(days=1)
    return day
```
