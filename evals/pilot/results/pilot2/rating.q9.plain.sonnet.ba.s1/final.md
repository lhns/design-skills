**Design 1 (Candidate B) is the better design.** Its year-based rule fits how invoices actually arrive, and Design 2's received-date window both misses real duplicates and still raises false alarms.

**Design 2's window fails in both directions.**
- **It misses real duplicates.** Scenery hire and the printers send a quarterly statement a couple of weeks after quarter end, with a copy of every invoice from that quarter stapled behind it. An invoice received early in a quarter can be about 3.5 months old by the time its copy arrives, which is well beyond 60 days. The post room can't always tell a copy from an original, so the copy would pass the check and be paid again. That is the scenery-hire double payment the theatre has already suffered, and Ingrid says a missed duplicate costs the payment.
- **It still produces January false alarms.** A supplier that restarts at 0001 and sends INV-0045 in late November, then a different INV-0045 in January, falls inside 60 days. The window only partly fixes the problem Theo described.
- **It depends on an arbitrary constant.** Any window is a trade-off between the two failures above, and the statement lag means no value works.

**Design 1 matches how the data behaves.**
- **It keys on the printed invoice date's year.** A copy carries the same printed date as its original, however late it arrives, so statement copies are caught. A restarted numbering sequence has a different year, so those false alarms disappear.
- **It fails safe when the date is missing.** If the post room can't read the date on a fax or photocopy, `same_invoice_year` returns `True` and the invoice is held. A few minutes of review is a far cheaper error than a missed duplicate.
- **It ignores amount.** This follows Ingrid's point that copies can differ by a few cents.
- **It normalises invoice numbers** the same way Design 2 does.

**Remaining weaknesses in Design 1:**
- A mistyped year would hide a match.
- Stripping all non-digits could conflate numbers like "A-45" and "B-45". That is acceptable given the cost asymmetry.
- It doesn't exclude the invoice itself or statements, but that is outside what's being compared.

Overall, Design 1 handles both the January restarts and the statement copies, while Design 2 misses the latter.

WINNER: 1