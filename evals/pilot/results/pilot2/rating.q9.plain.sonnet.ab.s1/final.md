**Design 2 (Candidate B) is better.**

The deciding asymmetry is Ingrid's: a held invoice costs a few minutes, while a missed duplicate costs the payment. The check should therefore lean toward holding when unsure.

**Candidate A fails on the statement case.**
- It compares the dates the invoices reached the theatre, with a 60-day window.
- The scenery-hire firm and the printers send a quarterly statement about two weeks after quarter end, with a copy of every invoice from that quarter behind it.
- An invoice received in early January and its copy arriving in mid-April are roughly 100 days apart, so A misses it.
- The post room can't tell copies from originals, so these copies get entered as new invoices. Because they fall outside the window, A releases them into the payment run, and these are exactly the double payments the rewrite is meant to stop. The scenery-hire double payment is the same kind of case.
- Any late re-send or a supplier chasing payment after more than 60 days is missed in the same way.
- The window is a proxy for "same numbering cycle". It is both too short for real duplicates and arbitrary for the January restart problem.

**Candidate B uses the right signal.**
- The printed invoice date is the same on an original and its copy, however long the copy takes to arrive. Statement copies and late re-sends are therefore caught.
- Requiring the same invoice year separates last January's 0045 from this January's 0045 for the printers and the lighting-hire firm. This removes the false alarms Theo described without a time window.
- When either date is missing, it can't rule a match out, so the invoice is held. This is the right default given the cost asymmetry. The result is a few extra minutes of checking on faxed or photocopied invoices.
- It leaves amount out of the match, as Ingrid advised, and normalises numbers so "INV-0045", "inv-0045 " and "45" all match.

**B's remaining weaknesses are minor and fail safe.**
- Stripping non-digits can merge distinct prefixes, which causes only extra holds.
- A mistyped year could cause a miss, which is rare.
- A copy of a December invoice that arrives in January still carries the old year, so it is still matched.

A misses real duplicates in a scenario the brief describes explicitly. B's flaws only cost a few minutes of checking.

WINNER: 2