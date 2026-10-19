# Free badminton slots

A community sports centre has four badminton courts, booked by the hour. Members book on the centre's website or at the desk; the website shows the free slots for each of the next 14 days. The booking module is being rewritten; two candidates are below.

**Schema (shared by both candidates):**

- `opening_hours(day, opens, closes)`: one row per date, written by the caretaker's admin page; a date with no row is closed.
- `court_block(court, starts_at, ends_at)`: a court out of use, also from the admin page.
- `booking(id, member, court, starts_at)`: unique on `(court, starts_at)`.

**From the centre manager:**

> We take about 40 bookings a day. The website is busiest on Monday mornings, when people book their week. The database is the small one that came with the website package; it's never been the problem.

**From the caretaker, Mo:**

> The hall is shared with the school next door. When the school tells me they need it for an exam or a parents' evening I change the opening hours on the admin page, sometimes only the afternoon before. Floor repairs are the same: if a board lifts I block that court straight away, it's a twisted ankle waiting to happen.

**From the manager, a bit later in the thread:**

> Last winter people turned up to a locked hall twice, with bookings they'd made online that same morning. I'd rather not have that again.

**From the developer:**

> `db` is a thin wrapper: `query`, `query_one`, `execute`, and `transaction()` as a context manager. Times are local; slots start on the hour.

Two candidate implementations follow. Which one is the better design?
