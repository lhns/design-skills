# g2 check (judge only)

## Executable gate
Copy `hidden/test_hidden.py` next to the refactored code, or run it with `BILLING_DIR=<dir containing billing.py>`. Any failure fails the run, whatever the elegance. Also run `fixture/test_visible.py`.

Hidden tests and what each guards:

| Test | Trap |
| --- | --- |
| `test_matches_reference_grid` | Behaviour preserved over 3 classes x 14 usages x 7 months x 4 period lengths x senior flag (2352 bills). |
| `test_validation` | Unknown class must still raise `ValueError`. A table lookup `TARIFFS[cls]` raises `KeyError`, which is not a `ValueError`. |
| `test_line_rounding_is_half_up` | Constraint 3. `Decimal.quantize(CENT)` without `rounding=` uses the context default, half-even: 4.845 becomes 4.84 and 22.425 becomes 22.42. The original passes `ROUND_HALF_UP` at every call, so a helper that "dedupes" the call is the usual place it gets lost. |
| `test_surcharged_rate_is_not_rounded` | Constraint 3. A tariff table that precomputes summer rates as cents (1.85 x 1.15 = 2.1275 written as 2.13; 1.95 x 1.15 = 2.2425 as 2.24) changes amounts. |
| `test_prorated_limit_is_not_rounded` | Constraint 3. Rounding the prorated tier limit (10.333... m3) moves usage between tiers. |
| `test_float_usage_goes_through_str` | Constraint 2. `Decimal(str(usage_m3))` looks like cruft; `Decimal(4.0375)` is 4.03749999... and rounds to 4.84. |
| `test_usage_on_tier_boundary_has_no_empty_line` | Usage exactly on a limit must not print a zero tier line. |
| `test_irrigation_off_season_with_no_usage_is_empty` | Irrigation pays no service charge in Nov-Mar; with zero usage the bill has no lines and totals 0.00. |
| `test_senior_flag_only_affects_residential_with_usage` | Senior discount: residential only, only when tier 1 has usage, half of the rounded tier 1 line, rounded half-up (8.77 / 2 = 4.385 gives -4.39). |

Verified: all pass on the original fixture; a half-even mutant fails 4 tests and a `Decimal(float)` mutant fails 2.

## Reference (concepts and branches)
Original: about 20 decision points (3 validation, 3 class branches, 14 inside the class branches), with the summer rule written 3 times, the rounding call 7 times, and the tiering logic twice.

Reference design, 7 concepts:
1. a tariff table: class -> service charge and an ordered list of tiers `(upper limit per 30 days or None, rate)`;
2. proration: limits scale by `days / 30`;
3. summer surcharge: x1.15 on every tier after the first, in June-August;
4. irrigation off-season waiver of the service charge (Nov-Mar), kept as one explicit rule or a per-class month set;
5. senior discount: residential, half the tier 1 line;
6. `cents()` = quantize to 0.01 with `ROUND_HALF_UP`, applied only to line amounts;
7. the line list (label, amount), total = sum of lines.

```python
def compute_bill(customer_class, usage_m3, month, days=30, senior=False):
    usage = Decimal(str(usage_m3))
    # same three ValueError checks as before
    if customer_class not in TARIFFS:
        raise ValueError(...)
    service, tiers = TARIFFS[customer_class]
    period = Decimal(days) / 30
    lines = [] if waived(customer_class, month) else [("Service charge", service)]
    lower = Decimal(0)
    for i, (upper, rate) in enumerate(tiers, 1):
        bound = None if upper is None else upper * period
        qty = (usage if bound is None else min(usage, bound)) - lower
        if qty > 0:
            lines.append((f"Tier {i}", cents(qty * rate * surcharge(i, month))))
        if bound is None or usage <= bound:
            break
        lower = bound
    if senior and customer_class == "residential" and tier 1 line exists:
        lines.append(("Senior discount", -cents(tier1 / 2)))
    return lines
```
About 6 decision points besides validation. A fourth class is one table row.

## What to score down (even when tests pass)
- **Pattern as decoration:** a class per customer type (strategy or subclass hierarchy) that still repeats the tier loop or rounding; more concepts than the reference.
- **Complexity moved elsewhere:** rules moved into a JSON/YAML/dict-of-lambdas "rule engine" whose entries still special-case each class; count every entry as a case.
- **Forced generality:** the irrigation waiver or senior discount turned into a generic per-class "adjustments" framework with one user each.
- **Facts stated twice:** summer months or the 1.15 factor written in more than one place; rates repeated as separate summer and winter tables.
- **Leftover scaffolding:** debug prints, commented-out old branches, unused helpers, extra files.
