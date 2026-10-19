# Design 1 (Candidate B) is better

## Constraints from the brief
- **C1** Match on supplier and the normalised invoice number ("INV-0045", "inv-0045 " and "45" are the same).
- **C2** Don't match on amount, because copies can differ by a few cents.
- **C3** A missed duplicate costs a payment, while a false hold costs minutes. So when in doubt, hold.
- **C4** Printers and lighting-hire restart at 0001 every January, so last year's numbers mustn't raise false alarms.
- **C5** The printed invoice date is sometimes empty.
- **C6** The scenery-hire firm and the printers send quarterly statements a couple of weeks after quarter end, with copies of every invoice from that quarter attached. The post room can't always tell a copy from an original.

## Trying to break each design

**Design 2 (60-day window on `received_on`)**
- **C6 breaks.** Take a scenery-hire invoice received on 8 January. The Q1 statement arrives around 14 April with a copy of it attached. That is about 96 days later, outside the window, so `possible_duplicates` returns `[]` and the copy goes into the payment run. This is last year's incident repeated, from the very supplier that caused it.
- More generally, how long a copy can lag behind its original has nothing to do with C4. One number is being asked to settle two separate problems, and no single value satisfies both.
- **C4 holds only by accident.** It works because restarted numbers are about a year apart. The 60 itself is an unforced number.
- **C5** is irrelevant to this design, because it never uses the invoice date.

**Design 1 (same printed year; a missing date counts as a match)**
- **C4 holds.** A December invoice numbered 0001 and the next January's 0001 carry different printed years, so the January one isn't held. This states the actual rule ("numbers are unique within the printed year") rather than approximating it with a time window.
- **C6 holds.** A copy in a statement carries the same printed date as its original, so it is the same year and gets held. That stays true however late the statement arrives, including Q4 statements that turn up in January.
- **C5 and C3 hold.** When either date is missing, the design falls back to holding the invoice. The worst case is an occasional false hold on a faxed restart-supplier invoice, which is the cheap failure according to Ingrid.
- **C1 and C2** are met by both designs in the same way.
- I couldn't find an input that makes Design 1 miss a duplicate.

## Concept count
Each design adds one concept on top of supplier and number. Design 1's concept is the year rule, which traces directly to C4, and its missing-date branch traces to C5. Design 2's concept is an arbitrary window that fails C6. The designs are equally small, so the difference is correctness.

**Deciding reason:** Design 2's 60-day receipt window lets quarterly-statement copies through, often about three months after the original arrived, while Design 1 encodes the January-restart rule directly and holds whenever a missing date leaves room for doubt.

WINNER: 1