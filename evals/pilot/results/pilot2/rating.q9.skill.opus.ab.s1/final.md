# Candidate B is the better design

**Constraints**
- **C1:** A missed duplicate costs the payment. A false hold costs a few minutes. So when unsure, hold.
- **C2:** Invoice numbers vary in format, so normalise them.
- **C3:** Don't match on amount.
- **C4:** Some suppliers restart numbering every January. Don't flood January with false alarms.
- **C5:** The printed invoice date is sometimes empty.
- **C6:** Quarterly statements carry copies of every invoice from the quarter. They arrive a couple of weeks after the quarter ends, and the post room can't always tell a copy from an original.

Both candidates handle C2 and C3 the same way. The difference is how they deal with C4.

**Breaking Candidate A**

The scenery-hire firm sends an invoice that arrives on 5 January. The Q1 statement arrives around 14 April with a copy stapled behind it. That is about 99 days between receipts, which is more than the 60-day window, so A does not hold the copy and it gets paid. This is last year's incident, through exactly the channel Theo described. Any copy of an invoice from the first month or so of a quarter falls outside the window.

The 60 is an unforced number trying to meet two opposing pressures:
- C6 needs a window of at least about 3.5 months.
- C4 needs it short.

No single value satisfies both. Widening it to about 110 days still causes January clashes for the reset suppliers, because their December invoices would match new January ones. Receipt date is the wrong representation: it is incidental to when the invoice was issued.

**Breaking Candidate B**

- **Statement copy:** it carries the same printed date as the original, so the years are equal and B holds it. C6 is met however late the statement arrives.
- **January reset:** a new 0001 is dated this year and last year's 0001 is dated last year, so there is no false alarm. C4 is met.
- **Missing date:** `same_invoice_year` returns True and the invoice is held. That costs minutes, which C1 explicitly accepts. C5 is met in the safe direction.
- **December invoice copied in a January statement:** the printed year is still the same, so B holds it.

I could not construct an input that makes B miss a real duplicate. The exception is a mistyped printed year, and A has an equivalent blind spot in receipt timing.

B's one concept is "a supplier doesn't reuse a number within a printed year". It is derived from Theo's description of the reset suppliers. It replaces an arbitrary bound with a condition, and the null case leans the way Ingrid's cost asymmetry says it should.

**Deciding reason:** A's 60-day receipt window misses the statement copies that caused last year's double payment, while B keys on the printed year, which handles both the January resets and late statement copies.

WINNER: 2