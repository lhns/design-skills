# Candidate B

```python
from datetime import datetime, timedelta

SLOT = timedelta(hours=1)
COURTS = (1, 2, 3, 4)


def free_slots(db, day):
    """Bookable, unbooked (court, start) pairs on `day`, from the current hours, blocks and bookings."""
    hours = db.query_one("SELECT opens, closes FROM opening_hours WHERE day = ?", day)
    if hours is None:
        return []
    booked = {
        (r.court, r.starts_at)
        for r in db.query("SELECT court, starts_at FROM booking WHERE date(starts_at) = ?", day)
    }
    blocks = db.query(
        "SELECT court, starts_at, ends_at FROM court_block WHERE date(starts_at) <= ? AND date(ends_at) >= ?",
        day, day,
    )
    free = []
    start, closes = datetime.combine(day, hours.opens), datetime.combine(day, hours.closes)
    while start + SLOT <= closes:
        for court in COURTS:
            blocked = any(b.court == court and b.starts_at < start + SLOT and start < b.ends_at for b in blocks)
            if not blocked and (court, start) not in booked:
                free.append((court, start))
        start += SLOT
    return free


def book(db, member, court, starts_at):
    with db.transaction():
        if (court, starts_at) not in free_slots(db, starts_at.date()):
            raise SlotUnavailable(court, starts_at)
        # The unique (court, starts_at) index stops two desks booking the same slot.
        db.execute(
            "INSERT INTO booking (member, court, starts_at) VALUES (?, ?, ?)",
            member, court, starts_at,
        )


def cancel(db, booking_id):
    db.execute("DELETE FROM booking WHERE id = ?", booking_id)
```
