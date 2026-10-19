**Design 1 (Candidate B) is the better design.**

**Why Design 2 fails.** It matches on the date the invoice *reached us*, with a 60-day window. Theo says the scenery-hire firm and the printers send a quarterly statement a couple of weeks after quarter end, with a copy of every invoice from that quarter stapled behind it. An invoice received in early January has its copy arrive in mid-April, about 100 days later. That is outside the window, so the copy is not held and goes into the payment run. This is exactly the scenery-hire double payment the theatre is trying to prevent. The post room can't always tell copies from originals, so the problem can't be handled upstream. Any received-date window short enough to avoid January false alarms will miss these statement copies. Since Ingrid says a missed duplicate costs the payment while a hold costs a few minutes, Design 2 gets the trade-off backwards.

**Why Design 1 works.**
- It keys on the *printed* invoice year. A statement copy carries the same printed date as the original, so it is matched however late it arrives.
- Suppliers that restart at 0001 each January are handled. A January 2026 "0001" has a different printed year from the January 2025 "0001", so there is no false alarm.
- A missing date (faxed or photocopied invoices) can't rule out a match, so the invoice is held. That is the cheap failure Ingrid prefers.
- Both designs normalise the number the same way and ignore amount, as Ingrid suggested.

**Remaining weaknesses in Design 1.**
- A mistyped printed year would cause a miss.
- Undated invoices will produce some extra holds against last year's invoices for restart-numbering suppliers. That is acceptable.
- Neither design filters to genuinely *earlier* invoices, despite the docstring. That is minor.

Design 1 also has a clearer rationale. Its `same_invoice_year` function states the business rule directly, whereas Design 2's window is an arbitrary constant that contradicts the known statement behaviour.

WINNER: 1