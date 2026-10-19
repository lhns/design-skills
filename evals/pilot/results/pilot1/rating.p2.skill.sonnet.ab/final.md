**Constraints**
- C1: three sites with label and carrier (N1/S2 → Alpha, W3 → Beta).
- C2: cutoff 14:00 at S2, 16:00 at N1 and W3.
- C3: no Sunday shipping; Saturday only at W3.
- C4: all functions except `is_valid_site` raise `ValueError` on an unknown code.
- C5: a fourth site is coming. Site details change about once a year, and whoever is on call makes the change.

**Shared concept.** Every constraint is a case of one thing: a site is a record of facts (label, carrier, cutoff, Saturday). Validity, labels, carriers and ship dates are all lookups or derivations from that record. Variation between sites is data. It is not a new kind of site or a new branch.

**Design 1** states each site fact once, in one row of a table. The code is the same for every site. Under C5, adding a site is one row, and changing a cutoff, carrier or Saturday rule is one edited field. The `site()` lookup is the only place that enforces C4, so no function can forget it. The dataclass names each field, which helps the on-call person.

**Design 2** spreads the same facts across code:
- Site identity is stated in four places: `VALID_SITES`, the label dict, the carrier test and the cutoff test.
- Behavior is keyed on special-case branches (`code == "W3"` for both carrier and Saturday, `code == "S2"` for the cutoff).
- Adding a fourth site means editing four places, and nothing links them. If you forget the label dict, you get a `KeyError` instead of the required `ValueError`, because `_check` passes against `VALID_SITES`.
- The carrier rule is also wrong by default: any new site silently gets Courier Alpha.
- Each function must remember to call `_check`, so C4 depends on discipline.

**Trying to break each design**
- Design 2: add "E4" to `VALID_SITES` but not to the label dict. `packing_label("E4")` raises `KeyError`, which breaks C4. Or add a site that ships Saturday and forget the `code != "W3"` test, which gives a silently wrong date. Neither can happen in Design 1, because a new row cannot be half-defined (the dataclass requires every field).
- Design 1: I found no input that breaks a constraint. Both designs give the same results for the three current sites, so the only difference is how they handle C5.

**Counts**
- Facts stated in more than one place: Design 1 has none, Design 2 has several (the site list, plus the W3 and S2 literals scattered across functions).
- Special-case branches: Design 1 has none per site, Design 2 has three (`W3` carrier, `S2` cutoff, `W3` Saturday).
- Concepts: Design 1 adds one (`Site`), which C5 forces. Design 2 saves it but pays in duplication and exception clauses.

**Deciding reason:** Design 1 keeps every site fact in one place, so a new site or a yearly change is a single data edit that cannot be left half done. Design 2 gets the same behavior today but fails C5 and risks C4 as soon as a site is added.

WINNER: 1