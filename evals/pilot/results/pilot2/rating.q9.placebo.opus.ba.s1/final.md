**Design 1 (Candidate B) is better.** It keys the decision on the printed invoice year, which matches how suppliers actually number invoices. Candidate A's time window on the received date misses exactly the kind of duplicate that cost the theatre money last year.

**Why Candidate A fails**

A 60-day window on `received_on` can't satisfy both of Theo's constraints at once.

- **Quarterly statements break it.** The scenery-hire firm and the printers send a statement a couple of weeks after each quarter ends, with copies of that quarter's invoices stapled behind. Suppose an original arrives on 5 January and its copy arrives with the Q1 statement around 14 April. That is about 99 days apart, outside the window, so the copy goes straight into the payment run. That is the scenery-hire scenario again.
- **Widening the window doesn't fix it.** A window of 100+ days would catch the statement copies. But then a January 0001 would clash with last year's late-autumn 0001 again, bringing back the false alarms the old system had.
- **The window tracks the wrong thing.** The reason a number can repeat is the supplier's numbering year. The gap between arrivals is only a rough stand-in for that, and it breaks down in the cases above.

**Why Candidate B works**

- **Statement copies are caught.** A stapled copy carries the same printed date as the original, so it is the same year and gets held, however many months later it arrives. Q4 copies that arrive in January still have December dates, so they match the December originals.
- **January restarts don't raise false alarms.** INV-0001 dated 2026 doesn't match INV-0001 dated 2025.
- **Missing dates fail safe.** If the post room can't read the date, `same_invoice_year` returns `True`, so the invoice is held. Ingrid has spelled out the trade-off: a hold costs minutes, a miss costs the payment. The occasional January false alarm on an unreadable fax is the right price.
- **It ignores amount,** as Ingrid asked. Both candidates do this.
- **It's clear.** The rule has a name (`same_invoice_year`), and its docstring states the domain assumption and the missing-date policy.

**Minor notes on B (not blocking)**

- `normalise` turns a number with no digits into `"0"`, so all digitless numbers from one supplier would match each other. That errs toward holding, which is acceptable, but a test should cover it.
- It's worth adding tests for: a Q1 statement copy arriving in April, a Q4 copy arriving in January, a January 0001 against last year's 0001, and a missing date on either side.

WINNER: 1