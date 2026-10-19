**Design 2 is better.**

Both implementations behave identically for the three current sites: same validation, labels, carriers, cutoffs, and weekend handling. The difference is in how they handle change, and constraint 5 makes that the deciding factor.

**Design 1 (scattered conditionals)**
- Site facts are spread across five places: the `VALID_SITES` set, the label dict inside `packing_label`, the `code == "W3"` check in `carrier_for`, and the `14 if code == "S2" else 16` and `code != "W3"` checks in `ship_date`.
- Adding a fourth site means editing all of them. Missing one fails silently. For example, if you add "E4" to `VALID_SITES` and the label dict but forget `carrier_for`, it gets Courier Alpha by default, and the cutoff defaults to 16 with no Saturday shipping.
- The `else` branches act as implicit defaults, so a new site gets plausible but possibly wrong behavior instead of an error.
- Changes happen about once a year, made by whoever is on call. That person is unfamiliar with the code, under pressure, and has to find every place a site code is hard-coded.
- The validity set and the label dict can drift apart, since they are two separate sources of truth.

**Design 2 (data table)**
- Each site's facts live in one record. Adding a site is a single line, and changing a cutoff, carrier, or Saturday rule is a one-value edit.
- The frozen dataclass requires every field to be supplied, so a new site cannot be added half-configured. A missing field raises `TypeError` at import time instead of silently picking a default.
- Validation, labels, carriers, and dispatch dates all derive from the same `SITES` dict, so they cannot disagree.
- The logic in `ship_date` is generic and does not need to change when sites change. Only data changes, which is the lower-risk kind of edit for an on-call engineer.
- The `site()` helper centralizes the `ValueError` behavior, with `from None` keeping the traceback clean. `is_valid_site` correctly does not raise.

**Tradeoffs**
Design 2 is slightly longer, and a dataclass is a bit more structure for three sites. That cost is small and is outweighed by the expected change pattern: a new site is coming and attributes change yearly. Design 1 is acceptable only for a fixed, never-changing set.

WINNER: 2