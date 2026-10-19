# Candidate A

```python
# free_slot(court, starts_at) lists every bookable, unbooked slot for the next
# 14 days, so the website reads it with one indexed query. The nightly job
# (jobs/rebuild_free_slots.py) regenerates it from opening_hours and
# court_block; booking and cancelling keep it current during the day.


def free_slots(db, day):
    return db.query(
        "SELECT court, starts_at FROM free_slot WHERE date(starts_at) = ? ORDER BY starts_at, court",
        day,
    )


def book(db, member, court, starts_at):
    with db.transaction():
        taken = db.execute(
            "DELETE FROM free_slot WHERE court = ? AND starts_at = ?", court, starts_at
        ).rowcount
        if not taken:
            raise SlotUnavailable(court, starts_at)
        db.execute(
            "INSERT INTO booking (member, court, starts_at) VALUES (?, ?, ?)",
            member, court, starts_at,
        )


def cancel(db, booking_id):
    with db.transaction():
        b = db.query_one("SELECT court, starts_at FROM booking WHERE id = ?", booking_id)
        db.execute("DELETE FROM booking WHERE id = ?", booking_id)
        db.execute("INSERT INTO free_slot (court, starts_at) VALUES (?, ?)", b.court, b.starts_at)
```
