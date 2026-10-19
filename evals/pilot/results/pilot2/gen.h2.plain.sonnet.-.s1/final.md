I refactored `fares.py` so each fare fact is stated once, and all 10 tests pass. That's the 6 existing tests plus 4 new ones. The files are at the repo root, not under `fixture/` as the brief said.

**What changed**
- **One code path for both trip types.** The single and return branches are gone. `quote` builds one list of per-leg lines, repeats it for "Outbound" and, if there is a return date, "Return", then adds the booking fee once.
- **Fares live in tables at the top of the module.** These cover passenger fares by season, age bands, vehicle classes, the per-metre rate, the booking fee and the 18.75 m lane limit. The yearly price change is now an edit to those tables.
- **Helpers.** Season now comes from a month table. Age and band lookups and the vehicle line are small helper functions.
- **Same output.** Bill lines, labels, order, validation and `total()` are unchanged. Infants still appear at 0.00, and that 0.00 is now a row in the fare table.

**Tickets**
- **#402 (fixed):** a 5.00 m car on a single crossing is now a car, because both trip types use the same "up to and including" rule. Return trips already did this.
- **#311:** I kept pricing on the outward date, since the ticket says that is intended. I replaced the old TODO with a docstring note citing clause 7.2.
- **#377:** the per-started-metre rule is unchanged, and I added a test for 8.1 m charged as 9 m.
- **#288 and #350:** nothing needed here.
- **#415 (family ticket) and #421 (spreadsheet):** I did nothing, because there is no decision on either. The tables are plain dicts, so loading them from a file later would be a small change.

**Design choices of mine**
- **Motorbikes:** adding the class is one new row in `VEHICLE_CLASSES`, which is ordered by maximum length. That assumes motorbikes are told apart by length. If they are chosen by vehicle type, the lookup would need a type argument.
- **Infants in the fare table:** I put infants in the passenger fare table at 0.00 rather than special-casing them. A future infant fare is then a data edit.
- **Month and age tables:** season by month and age bands are also tables, not if-chains.

I added tests for #402, #377, #311 and a return trip with a vehicle and an infant.