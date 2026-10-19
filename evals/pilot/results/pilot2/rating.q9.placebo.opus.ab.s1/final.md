# Candidate B is the better design

## Why A fails

Candidate A treats two invoices as possible duplicates only if they **arrived within 60 days** of each other. The comment says this is a compromise between catching re-sent invoices and avoiding January false alarms. Theo's quarterly statements break that compromise.

- The scenery-hire firm and the printers send a statement a couple of weeks after each quarter ends, with copies of every invoice from that quarter.
- An invoice received in early January has its copy arrive with the Q1 statement in mid-April. That is about 100 days later.
- The post room can't always tell a copy from an original, so the copy may be entered as a new invoice.
- It falls outside the 60-day window, so A returns `[]` and the copy goes into the payment run.

This is exactly how last year's scenery-hire invoice got paid twice, and it involves one of the two suppliers Theo named. Ingrid's cost asymmetry is clear: a hold costs minutes, a miss costs the payment. A's window is tuned against false alarms at the expense of misses, which is the wrong way round.

Widening the window doesn't fix this. Any window long enough to catch the statement copies, at roughly 3.5 months or more, will collide with January renumbering at year boundaries. The timing of arrival is simply the wrong signal.

## Why B works

Candidate B uses the **year printed on the invoice**, which is the real scope of a supplier's numbering.

- **January restarts.** A new "0001" dated 2026 does not match last year's "0001" dated 2025, so the old false alarms go away.
- **Statement copies.** A copy keeps its original printed date, so it matches the original whenever it arrives. The Q4 copies that arrive in January are included, because they still carry last year's date.
- **Unreadable dates.** When the date is missing, B errs toward holding, which costs a few minutes. This is the right default given Ingrid's costs, and the docstring says so explicitly.

The design is also clean. The rule lives in a small, well-named predicate, `same_invoice_year`. The docstring states the domain assumption it relies on. There is no magic constant whose correctness depends on how the post room happens to batch its work.

## Shared points

- Both use the same `normalise` and correctly ignore the amount, as Ingrid asked.
- One gap applies to both: an all-letter number normalises to `"0"`, so such invoices would all match each other. Because that over-holds rather than missing a duplicate, it is acceptable here, but it is worth a test.
- B should get tests for the three cases above: the statement copy arriving after 90 days or more, a January restart, and a missing date. A test like the first would have caught A's flaw.

WINNER: 2