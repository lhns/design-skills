**Design 2 (Candidate A) is better.**

**Why the constraints favor it:**

- **Knowledge has a single home.** Site facts (label, carrier, cutoff, Saturday shipping) live in one `SITES` table. In Design 1 they are scattered across four places: the `VALID_SITES` set, the label dict, the carrier conditional, and the cutoff and Saturday conditions inside `ship_date`. Adding a site means remembering to edit every one of them, and a miss would only show up as a wrong carrier or ship date, not as an error.
- **Change is frequent and made by whoever is on call.** Details change about once a year, and a fourth site is coming. This is an observed axis of change, so a data-driven design is not speculative generality. With Design 2, a new site is one table row and a cutoff change is a one-number edit. The on-call person doesn't need to understand the shipping logic to make it safely.
- **Design 1 has hidden defaults.** `carrier_for` returns Courier Alpha for anything not W3, and `ship_date` treats any non-S2 site as 16:00. A fourth site added to `VALID_SITES` but not to the other functions would silently get Alpha, a 16:00 cutoff, and no Saturday shipping. Design 2 forces every site to declare all of its attributes (a missing field is a construction error), and an unknown site cannot slip through.
- **Constraint 4 is enforced in one place.** The `site()` lookup does the validation and raises `ValueError`, and `is_valid_site` uses the same table, so the two can't drift apart. `from None` keeps the traceback clean.
- **Clarity.** Magic numbers (`14`, `16`, `"W3"`) become named, commented fields. The `ship_date` logic reads as policy (`s.cutoff_hour`, `s.ships_saturday`) rather than as site-specific special cases.

**Trade-offs and minor notes:**

- Design 2 is slightly longer and introduces a small dataclass. That is a modest cost, justified here because the dataclass has a real, repeated use and is not a one-off abstraction.
- For three sites with no expected change, Design 1 would be perfectly acceptable. The change history and the upcoming fourth site tip the balance.
- A possible refinement for both: Sunday is hardcoded as weekday 6, and `6`/`5` could be named constants. That is minor and applies equally to each design.

WINNER: 2