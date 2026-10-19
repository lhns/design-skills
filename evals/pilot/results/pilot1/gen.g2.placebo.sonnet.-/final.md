I refactored `billing.py` so each tariff fact is stated once, in a data table. The visible tests pass, along with four tests I added. I also ran 200,000 random inputs through the old and new code, and every bill and every `ValueError` matched. The inputs included bad months, days and usage, unknown classes, odd `days` values, and seniors.

Two notes on the setup:
- **File location:** the files are at the repo root, not in `fixture/` as the task described, so I edited them there.
- **Running tests:** `pytest` isn't installed here, so I ran `python test_visible.py` instead.

**What changed**
- **Tariff table:** a `TARIFFS` dict holds one `Tariff` per customer class. Each has a service charge, an ordered list of tiers and any waived months, and each `Tier` has a rate, a limit and a summer-surcharge flag. A rate change is a one-value edit. A fourth class is one new entry.
- **Constants:** the 30-day base period, the summer months and the 1.15 surcharge are each named once.
- **`compute_bill`:** it validates the inputs, then adds the service charge, then the tier lines. A shared `_tier_lines` function replaces the three copy-pasted branches. A `_to_cents` helper does the half-up rounding.
- **`bill_total`:** now a single `sum` over the line amounts.

**Design choices (mine, since no user was available)**
- **Cumulative limits:** each tier stores its cumulative upper limit, not its width. That reproduces the old arithmetic exactly, so prorated limits aren't rounded differently.
- **Senior discount:** it is a per-tariff fraction of the Tier 1 line, not a residential special case. Any class can get one by setting that field.
- **Unknown-class check:** it runs after the usage, month and days checks, so the same bad input raises the same error as before.
- **Skipped abstractions:** I didn't add classes or a rule engine, since three flat classes don't need them.

I added tests for the commercial summer surcharge, day proration, the irrigation off-season and invalid inputs to `test_visible.py`.