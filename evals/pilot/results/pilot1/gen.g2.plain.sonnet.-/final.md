I refactored `billing.py` into a table of tariffs plus one generic calculation. It gives identical results to the original on about 274,000 generated inputs. The 10 tests in `test_visible.py` pass when run directly. `pytest` isn't installed here, so I couldn't run `python -m pytest`.

The inputs covered all three classes, an unknown class, months 0–13 and 6.5, and day counts from -3 to 90. They also covered negative, fractional and string usage, and `senior` both ways. I compared lines, labels, order, amounts and `ValueError` messages. The files are in the working directory root, not `fixture/`, so I edited them there.

**What changed**
- **Tariff table:** every rate, tier limit, service charge, seasonal flag and off-season month now sits in one `TARIFFS` entry per class. The summer months, the 1.15 surcharge and the 30-day period each appear once.
- **One calculation:** the three per-class branches are now a single path.
  1. It prorates the tier limits.
  2. It splits usage across the tiers.
  3. It applies the summer surcharge to the tiers flagged `seasonal`.
  4. It rounds each line half-up.
- **Rounding unchanged:** only line amounts are rounded; rates, prorated limits and quantities are not. `bill_total` still sums the printed lines.
- **Adding a class or changing a rate:** a fourth class, such as one with a different tier count, is one new `TARIFFS` entry with no new code. A rate change is a one-value edit.

**My design choices**
- **Cumulative limits:** `Tier.up_to` holds cumulative limits (10, 30, unbounded), as the tariff is quoted, not per-tier widths.
- **Irrigation off-season:** I kept the original list of off-season months (`no_service_months`) rather than inverting it to an in-season range. A non-integer month such as 4.5 would otherwise change behaviour.
- **Senior discount:** it's a per-class fraction of the Tier 1 amount (`senior_discount=0.5` for residential). Other classes ignore `senior`, as before.
- **Validation order:** it is unchanged, with the class lookup last. An unhashable class still raises the same `ValueError`.
- **Tests:** I added five to `test_visible.py` for the summer surcharge, proration by days, irrigation off-season, the residential-only senior discount, and invalid inputs.