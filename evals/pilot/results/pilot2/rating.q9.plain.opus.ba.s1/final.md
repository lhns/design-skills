**Design 1 (Candidate B) is better.** It scopes the number match by the year printed on the invoice. That is exactly the scope in which these suppliers' numbers are unique. Design 2 uses a 60-day window on the date received, which misses the duplicates the theatre is most exposed to.

**Why Design 2's 60-day window fails**

- **Quarterly statements.** The scenery-hire firm and the printers send copies of each quarter's invoices a couple of weeks after the quarter ends. An invoice received in early January comes back as a copy in mid-April, about 100 days later. With a 60-day window, roughly the first half of every quarter's copies get through and are paid again. These come from the very supplier who caused last year's double payment.
- **Late re-sends.** A supplier chasing payment may re-send an invoice, with a late-payment note and a slightly different amount, more than two months later. That is outside the window, so it is missed.
- **The window is a compromise between two needs.** Lengthening it to catch statement copies brings back the January false alarms for suppliers who restart numbering. Shortening it misses more duplicates. No value satisfies both. Ingrid's priority is clear: a missed duplicate costs the payment, a hold costs minutes. Design 2 makes the costly error in exchange for avoiding the cheap one.

**Why Design 1 handles each scenario**

- **Numbering restarts in January.** Last year's 0001 and this year's 0001 have different printed years, so there is no false alarm. This directly fixes Theo's complaint.
- **Statement copies.** A copy carries its original's printed date, so it shares that year and is held. This holds even for Q4 copies arriving in January, because the printed date is still last year's.
- **Late re-sends.** These are caught regardless of how long afterwards they arrive.
- **Missing printed date (faxes and photocopies).** It deliberately treats this as a possible match. The cost is an occasional extra hold, which Ingrid explicitly accepts. That is safer than silently letting a possible duplicate through.
- **Amount.** Like Design 2, it correctly ignores the amount, and both use the same number normalisation.

**Minor caveats with Design 1**

- A mistyped year on entry could hide a duplicate.
- Invoices with no readable date will produce some extra holds for finance to clear.

Both risks fall on the cheap side or are rare. Design 2's misses are systematic and fall on the expensive side.

WINNER: 1