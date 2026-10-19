# Design 2 (Candidate A) is better

**Constraints**
- C1: label and carrier for each site.
- C2: cutoff hour per site.
- C3: no Sunday shipping; only W3 ships on Saturday.
- C4: unknown codes raise `ValueError`.
- C5: sites get added and edited by whoever is on call.

**Trying to break each design**

For today's three sites, both designs behave the same. Both meet C1–C4. Comparing hour against a whole-hour cutoff is fine because every cutoff is on the hour. The difference shows up under C5: a fourth site, or a changed fact, edited by someone unfamiliar with the code.

- **Design 1** stores each site's facts in five places:
  - `VALID_SITES`
  - the label dict
  - the carrier ternary
  - the cutoff ternary
  - the Saturday condition

  Each ternary also has a hidden default. That leaves concrete ways to break it:
  - Add `"E4"` to `VALID_SITES` and forget the label dict: `packing_label("E4")` raises `KeyError`, which violates C4.
  - Add E4 with a 15:00 cutoff, Courier Beta and Saturday shipping, but miss the ternaries: E4 silently gets Courier Alpha, 16:00 and no Saturday. Nothing fails. Orders just ship on the wrong dates with the wrong carrier.
  - Move W3 to Courier Alpha: the edit goes inside an `if code == "W3"` expression whose meaning is spread across functions.
- **Design 2** keeps one record per site, and every field is required. If a new site omits a fact, the code fails when the module is imported, not quietly in production. Validity is derived from `SITES`, so the code list cannot drift from the facts, and every lookup goes through `site()`, so C4 holds for any code. A per-site change is a one-field edit.

**Concept counts**

| | Design 1 | Design 2 |
|---|---|---|
| Places stating site facts | 5 (validity twice: in `VALID_SITES` and in the dict keys) | 1 table |
| Special-case branches on specific codes | 3 (`== "W3"`, `== "S2"`, `!= "W3"`) | 0 |
| Silent defaults for unlisted sites | 3 | 0 |
| Unnamed numbers in logic | 14, 16 inline | named field `cutoff_hour` |

Design 2 adds one concept, the `Site` record. C1–C3 force it: they are all per-site facts, so they belong on one per-site entity. The only rule that stays in code is "Sunday never ships", which is genuinely global.

**Deciding reason:** Design 1 states each site's facts in several places, with silent defaults. Adding the fourth site (C5) can violate C4 or ship on the wrong days without any error. Design 2 keeps every site fact in one complete record, so neither failure can happen.

WINNER: 2