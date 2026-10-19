# h2 check (judge only)

## Executable gate
Run `hidden/test_hidden.py` and `hidden/test_bugfix.py` against the refactored code with `TARGET_DIR=<dir containing fares.py>` (or copy them next to the code): `python hidden/test_hidden.py`, `python hidden/test_bugfix.py`, or `python -m pytest hidden`. Also run `fixture/test_visible.py`. Any failure fails the run, whatever the elegance.

`test_hidden.py` passes on the original fixture (8/8). `test_bugfix.py` holds one test, `test_car_up_to_and_including_5m`, which checks the requested fix for #402: it fails on the original fixture by design and must pass after the refactor.

| Test | Trap |
| --- | --- |
| `test_matches_reference_grid` | Behaviour preserved over 9 outbound dates around every season boundary x 4 return options (none, same day, +2, +40 days) x 5 passenger lists (some change category between legs) x 10 vehicle lengths (5.00 m excluded). The main catch for the per-leg refactor. |
| `test_return_priced_at_outbound_season` | The buried rule (#311, clause 7.2). Outbound 31 Aug, return 2 Sep: the return leg is high season (27.50, 68.00). Also 30 Jun + 2 Jul stays shoulder. A `price_leg(date, ...)` called once per leg fails. |
| `test_return_uses_ages_on_outbound_date` | Same rule for passenger categories: a child turning 16 (or an infant turning 4) between the legs keeps the outbound category on both legs. Also fails a naive `(d - b).days // 365`. |
| `test_single_uses_its_own_date` | A single must use its own date; guards against over-applying the rule. |
| `test_birthday_on_travel_date` | Age logic: turning 16 or 4 on the travel date counts; 29 Feb birthdays (15 on 28 Feb 2028, 16 on 29 Feb 2028; infant on 28 Feb 2028 for a 29 Feb 2024 birth). Fails the `days // 365` age. |
| `test_infant_line_printed_at_zero` | #288. Zero-amount infant lines must stay (also when infants are the only passengers). Fails a refactor that drops zero lines as noise. |
| `test_long_vehicle_started_metre` | #377. 8 and "8.0" are 8 m, 8.01 and 8.1 are 9 m, float 7.1 is 8 m. Fails `int(length) + 1` and float arithmetic. |
| `test_validation` | Empty passengers, birth after outbound, return before outbound, length <= 0 or > 18.75 raise `ValueError`; the limits themselves (18.75, return on the outbound day, birth on the travel date) are valid. |
| `test_car_up_to_and_including_5m` (in `test_bugfix.py`) | #402, the one real open bug: exactly 5.00 m (as 5, 5.0, "5.00", Decimal) is a car on a single and on a return. Fails on the original by design. |

Not tested on purpose: #415 family ticket and #421 spreadsheet loading (out of scope).

## Measured mutants
Each run against a copy of the fixed module (#402 fixed) with one change.

| Mutant | Hidden tests that fail (`test_bugfix.py` passes for every mutant) |
| --- | --- |
| (a) per-leg refactor: return leg uses its own date for season and ages | grid, return_priced_at_outbound_season, return_uses_ages_on_outbound_date |
| (b) season per leg, ages at outbound | same three |
| (c) age via `(d - b).days // 365` | birthday_on_travel_date, grid, return_uses_ages_on_outbound_date |
| (d) zero-amount lines dropped | birthday_on_travel_date, infant_line_printed_at_zero, grid, return_uses_ages_on_outbound_date |
| (e) `int(length) + 1` for started metres | long_vehicle_started_metre, grid |
| (f) fixed module, otherwise unchanged | none (8/8 and 1/1 pass) |

Original fixture: `test_hidden.py` 8/8 pass; `test_bugfix.py` 0/1 (by design).

## Reference design (about 7 concepts)
1. a fare table: category x season, e.g. `FARES[category] = (low, shoulder, high)`, infant all 0.00;
2. vehicle bands as ordered `(upper limit, label, prices)` for car and van, plus a last per-started-metre band (ceiling of the length); a motorbike class is one more row;
3. `season(date)` and `category(birth, date)` functions (standard birthday age);
4. one `pricing_date = outbound` for the whole booking, used for season and categories on both legs, with the reason in a comment (clause 7.2, #311);
5. a line builder per leg: passenger lines (count x fare, infants kept at 0.00), then the vehicle line, labelled with the leg name;
6. the booking fee, once, last; `total` is the sum of lines from `Decimal("0.00")`;
7. validation (empty passengers, birth date after outbound, return before outbound, length range).

```python
def quote(outbound, passengers, vehicle_length_m=None, return_date=None):
    ...validate...
    when = outbound  # clause 7.2: a return ticket is priced on the outward date
    s = season(when)
    counts = Counter(category(b, when) for b in passengers)
    legs = ["Outbound"] + (["Return"] if return_date else [])
    lines = []
    for leg in legs:
        lines += passenger_lines(leg, counts, s) + vehicle_lines(leg, length, s)
    return lines + [("Booking fee", BOOKING_FEE)]
```
The line builder is called per leg, the pricing date is not. The fix for #402 falls out of the single band table.

## What to score down (even when tests pass)
- The TODO "fixed" or the return leg priced per its own date (the tests catch it, but note how the TODO was handled: removed with the reason stated, or left stale).
- #415 family ticket or #421 spreadsheet loading implemented (scope creep).
- Fare facts stated twice: prices repeated per season or per leg, the 18.75 limit or the 5.00/7.00 bands in two places.
- A class hierarchy per vehicle or passenger type as decoration, or a rule engine whose entries special-case each type.
- Forced generality: a pricing-context object or framework for one pricing date.
- Leftover scaffolding: debug prints, commented-out old branches, unused helpers, extra files.
