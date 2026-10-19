I refactored `billing.py` so each customer class is a table entry and `compute_bill` is one loop that applies it. A fourth class is now one more `TARIFFS` entry, and a rate change is a one-line edit.

The new version gave the same lines (labels, order, amounts), the same `ValueError`s and the same `bill_total` as the original on 300,000 random inputs. Those covered odd `days`, fractional months, bad inputs and zero usage. `test_visible.py` passes. I added `test_billing.py` with 8 edge-case tests (summer markup, proration, off-season irrigation, senior rounding, validation), and they pass. I ran the files directly with `python`, because pytest isn't installed here.

The files were at the repo root, not in `fixture/`, so I edited them in place.

**What changed**
- **Tariff table:** `TARIFFS` holds one `Tariff` per class: service charge, tiers, waived months and senior discount. Each tier is a `Tier` with a rate, a cumulative limit per 30 days (none means unlimited) and a `seasonal` flag.
- **Seasonal constants:** `SUMMER_MONTHS`, `SUMMER_MARKUP` and `STANDARD_DAYS` are each stated once.
- **Computation:** each tier bills the usage between the previous tier's limit and its own. Limits are prorated by `days / 30`, nothing is rounded except line amounts (via `cents()`), and zero-quantity tiers produce no line.
- **Senior discount:** it is a share of the Tier 1 line, set only for residential.
- **`bill_total`:** now a single `sum`.

**Design choices**
- **Cumulative limits:** the limits are cumulative (10, 30), as the original stated them, so the quantity per tier is derived rather than written out.
- **Months as tuples:** `waived_months` and `SUMMER_MONTHS` are tuples tested with `in`, not ranges. That keeps odd inputs like `month=4.5` behaving exactly as before.
- **Dataclasses:** I used two small frozen dataclasses so the table reads as plain facts. They are the only abstractions added.
- **Validation order:** the unknown-class check still comes after the usage, month and days checks, so the same error wins when several inputs are bad.

**One difference from the original:** an unhashable `customer_class`, such as a list, now raises `TypeError` instead of `ValueError`, because it is looked up in a dict. I judged that not worth extra code.