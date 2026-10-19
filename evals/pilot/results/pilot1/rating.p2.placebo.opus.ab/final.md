**Design 1 is better.** Both behave identically today; the difference is how they handle the change the constraints predict.

**Where site facts live.**
- **Design 1:** Each site's facts sit in one `SITES` row. Adding the fourth site, or changing a cutoff or carrier, is a one-line edit. The functions never change.
- **Design 2:** One site's facts are spread across five places: `VALID_SITES`, the label dict, the carrier conditional, the cutoff conditional and the Saturday conditional. An on-call engineer who adds a site has to find all of them.

**How Design 2 fails when someone misses a spot.** It fails silently, through implicit defaults:
- A new site added only to `VALID_SITES` is quietly assigned Courier Alpha, a 16:00 cutoff and no Saturday shipping. Nothing errors, so wrong ship dates and wrong carriers reach customers.
- If it is added to `VALID_SITES` but not to the label dict, `packing_label` raises `KeyError` instead of the required `ValueError`, which breaks constraint 4.
- Conditionals like `code != "W3"` and `code == "S2"` encode rules as exceptions to unnamed defaults. A reader cannot see that N1 has a 16:00 cutoff without working it out.

**Why Design 1 holds up.**
- A site cannot be valid without having every attribute. Leaving one out of `Site(...)` is an immediate `TypeError`.
- Validation and lookup are the same operation (`site()`), so constraint 4 holds for every function by construction.
- `ship_date` reads as policy (`s.cutoff_hour`, `s.ships_saturday`) rather than as special cases for particular sites.
- The frozen dataclass documents the shape of a site, with comments on the meaning of the cutoff.

**Is Design 1 over-engineered?** No. It is about the same length as Design 2, adds no speculative abstraction, and models exactly the facts the constraints list. With a known upcoming site and yearly edits by rotating staff, putting the data in one place is the YAGNI-compliant choice, not a premature one.

**Minor nit for Design 1:** Naming the weekday numbers (`SATURDAY = 5`, `SUNDAY = 6`) would read better than the bare 5 and 6. Design 2 has the same issue.

WINNER: 1