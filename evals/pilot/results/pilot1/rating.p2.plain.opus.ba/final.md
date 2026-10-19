**Design 2 is better.** It is labelled "Candidate A" in its heading. Both designs behave the same today, so the difference is how easily they can be changed.

**Same behaviour.** Both reject unknown codes with `ValueError`, except in `is_valid_site`. Both apply the cutoffs (14:00 at S2, 16:00 at N1 and W3) with an at-or-after comparison, and both skip Sunday everywhere and Saturday everywhere except W3. Comparing on the hour is fine because every cutoff falls exactly on the hour.

**Why Design 2 wins, given constraint 5:**

1. **Each site's facts live in one place.** In Design 2, each site is a single `Site(...)` row with named fields. In Design 1, the same facts are spread across four places:
   - `VALID_SITES`
   - an inline label dict
   - a `code == "W3"` carrier ternary
   - `14 if code == "S2" else 16` and `code != "W3"` inside the date logic

2. **Adding a site is safer.** In Design 2, the fourth site next spring is one new row. Python makes you supply every field, so you can't forget its cutoff or carrier. In Design 1, an on-call engineer must find and edit four spots. Missing any of them fails silently in at least two ways:
   - The new site quietly gets Courier Alpha, a 16:00 cutoff and no Saturday shipping, because those are what the "else" branches assume.
   - If the code is added to `VALID_SITES` but the label is forgotten, `packing_label` raises a `KeyError` instead of a sensible error.

3. **Yearly changes are data edits, not logic edits.** Suppose N1 starts shipping on Saturdays. In Design 2 you flip `ships_saturday=True`. In Design 1 you have to rewrite the condition, for example to `code not in ("W3", "N1")`. That is easy to get wrong for someone unfamiliar with the code.

4. **The rules are easier to read and test.** `SITES` reads like a direct copy of constraints 1–3, and the field comments explain what each value means. `ship_date` contains no site names, so you can test it against any `Site` value.

Design 1 is a bit shorter, but that saving is small compared with the maintenance risk.

WINNER: 2