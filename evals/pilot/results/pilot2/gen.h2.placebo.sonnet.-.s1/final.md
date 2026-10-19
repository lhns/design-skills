I refactored `fares.py` and fixed #402. The 6 visible tests and my 7 new ones pass. pytest isn't installed here, so I ran them as plain scripts.

The files sit at the repo root, not in `fixture/` as the brief said, so I worked in place.

**What changed**
- Single and return trips now share one code path. The passenger and vehicle lines for one leg are built once, then repeated for "Outbound" and, if there's a return date, "Return".
- Every fare fact now lives in one table at the top of the module:
  - **Passenger bands:** adult from 16, child from 4, infant from 0, with their prices.
  - **Flat-fare vehicle classes:** car up to 5.00 m, van up to 7.00 m, with their prices.
  - **Long vehicles:** the per-metre rate, plus the 18.75 m longest-lane limit.
  - **Booking fee:** 2.50.
- The yearly fare change is now an edit to those tables. The motorbike class next year is one more row in the vehicle table, with no new branches.
- `quote` now reads as validate, price one leg, repeat per leg, add the fee.

**Tickets**
- **#402 (fixed):** a single crossing used `< 5.00` for cars while return trips used `<= 5.00`. There is now one rule, so a 5.00 m car pays the car fare either way.
- **#311 (kept):** both legs are priced on the outward date, per clause 7.2. I replaced the old "should the return leg use its own date?" TODO with a comment citing the clause.
- **#288 and #377 (kept):** infant lines still print at 0.00, and long vehicles still charge per started metre.
- **#350, #415, #421:** left alone. #350 was fixed in the booking service, and #415 and #421 have no decision yet.

**Design choices (mine)**
- I used `Season` as an `IntEnum`, and each price is a three-value tuple (high, shoulder, low). That way every row states its prices once, without repeating season keys.
- Passengers go in the first age band they qualify for, so a band's age limit is written once.
- `total` is now a `sum` seeded with `Decimal("0.00")`, so it behaves as before.
- Ages for return tickets are still taken on the outward date, as before.

The new tests are in `test_fares.py`. They cover the 5.00 m boundary on single and return trips, 8.1 m charged as 9 m, return-trip season and infant lines, and the vehicle length limits.