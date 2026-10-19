I rewrote `fares.py` so the prices sit in tables and one code path prices both single and return trips. The 8 tests pass: the 6 visible ones plus 2 I added. The files are in the repo root, not `fixture/`; I worked there.

**What changed**
- **Fare tables:** the passenger fares, vehicle classes, per-metre rate, booking fee, month-to-season map and longest-lane limit are each stated once, at the top of the file. The yearly price change only touches that section.
- **Motorbikes:** next year this is one new row in `VEHICLES`, with no code change.
- **Single and return trips:** both build the same set of lines for one crossing, and a return repeats it with a `Return:` prefix. The bill order is unchanged.

**Tickets**
- **#402 (fixed):** a 5.00 m car on a single crossing is now a car. The single branch had `<` where the return branch had `<=`. I added a regression test.
- **#288 and #377:** behaviour is kept. Infants still print at 0.00, listed as a 0.00 fare in the table. Long vehicles are still charged per started metre.
- **#311:** behaviour is kept, since clause 7.2 sets the return fare on the outward date. Season and passenger ages are both taken from that date. I replaced the old `TODO` with a comment citing the clause and added a test.
- **#350:** not touched, because it was fixed in the booking service.
- **#415 and #421:** not implemented. There are no family prices and no spreadsheet decision, so I didn't guess.

**My design choices**
- **Tables in Python:** I kept the fare tables in the module, not in an external file, because #421 has no decision. Moving them out later is easy.
- **Passenger categories:** they're listed adult, child, infant with a minimum age each, so the classification and the bill order come from the same list.
- **`total()`:** it is now a single `sum` and returns the same result.