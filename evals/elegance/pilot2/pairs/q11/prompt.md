# Holiday club opening days

A charity runs a holiday club for children aged 5 to 11 in a primary school's hall. It opens on weekdays during the local council's school holidays, and parents book days online. The booking site asks one function which days the club runs; that function is being rewritten. Two candidates are below.

**From the club manager, Nadia:**

> We're open every weekday of the council's school holidays, bank holidays included, and never in term time. Our play workers are mostly teaching assistants from the council's schools, so they're only free in the holidays, and the hall is the school's.
>
> The council publishes its term dates as a table on its website, a school year at a time, after a consultation with schools and parents. The pattern is pretty steady, but they do move things: for 2026-27 they pushed the February half-term back a week to line up with the next county, and next summer starts on a Wednesday because of the way the training days fall.
>
> Parents can book up to twelve months ahead. Lots of them book the whole year in one go in October, as soon as the autumn newsletter goes out.

**From the council's term-dates page (copied 12 October):**

> 2025-26 and 2026-27: confirmed (see tables).
> 2027-28: proposed dates are out for consultation until 30 November. Final dates will be published in December.

**From the volunteer developer:**

> `club_days(first, last)` returns the dates in that range the club runs, inclusive. The booking page calls it for the next twelve months. I've checked both candidates against the council's tables for 2025-26 and 2026-27 and they agree on every date.

Two candidate implementations follow. Which one is the better design?
