**Constraints**
- C1: site → label and carrier (N1, S2 share Alpha; W3 uses Beta).
- C2: per-site cutoff (14:00 at S2, 16:00 at N1 and W3).
- C3: no Sunday shipping; only W3 ships Saturday.
- C4: all functions except `is_valid_site` raise `ValueError` on an unknown code.
- C5: a fourth site is coming. Site details change about once a year, and whoever is on call makes the change.

**Core concept.** Every constraint is a fact about a site, keyed by code: label, carrier, cutoff, Saturday shipping. One table row per site covers them all. Site facts are data, and shipping logic is a single rule that reads that data.

**Design 1** states the site facts in several places:
- The set of valid codes lives in `VALID_SITES`.
- Labels live in a dict inside `packing_label`.
- The carrier lives in an `== "W3"` branch.
- The cutoff lives in a `== "S2"` branch with the numbers 14 and 16.
- Saturday shipping lives in a `!= "W3"` branch.

Adding a fourth site touches five places. If one is missed, the code still runs. For example, a new site added to `VALID_SITES` but not to the label dict raises `KeyError` instead of the required `ValueError` (C4). A new site would silently get Alpha and a 16:00 cutoff from the defaults in the branches. Under C5, a change made by whoever is on call is exactly where this kind of omission happens. The code also bakes in "everything that isn't W3 is Alpha" and "everything that isn't S2 is 16:00", which are facts nobody stated.

**Design 2** has one `Site` record and one `SITES` table. Validity, the error path (`site()` is the only place that raises), and the shipping rule all derive from that table. A new site is one row. A cutoff or carrier change is one edit to one value. A missing field in a new row fails at construction, because the dataclass has no defaults. `ship_date` has the same logic as in Design 1, but it reads the site's data rather than comparing site codes.

**Breaking attempts**

| Constraint | Design 1 | Design 2 |
|---|---|---|
| C1–C3 | Correct for the three sites | Correct for the three sites |
| C4 | Breaks if a code is added to one place and not another (`KeyError`) | One raise point, so it cannot diverge |
| C5 | Five places to edit, with silent wrong defaults | One row |

Design 2 adds one concept, the `Site` record. C5 forces it, because it is the single place where each site fact is stated. It also removes the special-case branches on site codes, the duplicated code list, and the unforced defaults.

**Ledger**
- Constraints: C1–C5.
- Forced: a per-site table (C5, C1–C3). One validation point (C4).
- Designer choices: the frozen dataclass and the field names.
- Deletions: the `VALID_SITES` duplicate, three code-literal branches, and the `_check` helper.

Deciding reason: Design 2 states each site fact once, so the fourth site and the yearly changes (C5) are single-row edits that cannot leave the code partly updated, while Design 1 spreads those facts across five places.

WINNER: 2