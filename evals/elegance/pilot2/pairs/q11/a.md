# Candidate A

```python
from datetime import date, timedelta


def easter(year):
    """Easter Sunday in the Gregorian calendar (anonymous Gregorian algorithm)."""
    a, (b, c) = year % 19, divmod(year, 100)
    d, e = divmod(b, 4)
    g = (b - (b + 8) // 25 + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month, day = divmod(h + l - 7 * m + 114, 31)
    return date(year, month, day + 1)


def monday_on_or_after(d):
    return d + timedelta(days=-d.weekday() % 7)


def monday_on_or_before(d):
    return d - timedelta(days=d.weekday())


def weeks(first_monday, n):
    return first_monday, first_monday + timedelta(weeks=n - 1, days=4)


# Where the council departed from its usual pattern: (school year, holiday) -> (first, last).
COUNCIL_CHANGES = {
    (2026, "february"): (date(2027, 2, 22), date(2027, 2, 26)),
    (2026, "summer"): (date(2027, 7, 21), date(2027, 8, 31)),
}


def holidays(y):
    """Holidays of the school year starting in September of year `y`, as (first, last) weekdays."""
    usual = {
        "october": weeks(monday_on_or_before(date(y, 10, 27)), 1),
        "christmas": weeks(monday_on_or_after(date(y, 12, 19)), 2),
        "february": weeks(monday_on_or_after(date(y + 1, 2, 15)), 1),
        "easter": weeks(easter(y + 1) - timedelta(days=6), 2),
        "may": weeks(monday_on_or_before(date(y + 1, 5, 31)), 1),
        "summer": (monday_on_or_after(date(y + 1, 7, 20)), date(y + 1, 8, 31)),
    }
    return [COUNCIL_CHANGES.get((y, name), period) for name, period in usual.items()]


def club_days(first, last):
    days = []
    d = first
    while d <= last:
        school_year = d.year if d.month >= 9 else d.year - 1
        if d.weekday() < 5 and any(a <= d <= b for a, b in holidays(school_year)):
            days.append(d)
        d += timedelta(days=1)
    return days
```
