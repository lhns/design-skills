**Design 1 is better.**

**Behaviour today is the same.** Both handle the four questions correctly:

- Both use an "at or after cutoff" rule (`hour >= cutoff`).
- Both skip Sundays, and skip Saturdays for every site except W3.
- Both raise `ValueError` for unknown codes, except in `is_valid_site`.

So the choice depends on constraint 5: a new site next spring, yearly detail changes, and edits made by whoever is on call.

**Design 1 puts each fact in one place.**
- Each site is a single `Site` record in `SITES`.
- Adding the fourth site means adding one line. Changing a cutoff, carrier or Saturday policy means editing one named field.
- Validity comes from the same table, so a site can't be "valid" while missing a label or carrier.
- The frozen dataclass forces every field to be filled in. A new site therefore can't silently inherit a default.
- An unfamiliar on-call engineer can see and change everything about a site without reading the logic.

**Design 2 scatters site facts across the code.**
- Each site's details are spread over four places: `VALID_SITES`, the label dict, and the conditionals in `carrier_for` and `ship_date`.
- Several of those facts are hidden in defaults:
  - `code == "W3"` means "Beta, otherwise Alpha".
  - `code == "S2"` means "14:00, otherwise 16:00".
  - `code != "W3"` means "no Saturday".
- Adding site E4 to `VALID_SITES` and the label dict would compile and pass a quick check. But E4 would silently get Courier Alpha, a 16:00 cutoff and no Saturday shipping, whether or not that's true.
- Likewise, moving Saturday shipping to N1 means rewriting a boolean expression rather than flipping a field. That kind of edit is easy to get wrong under on-call pressure.
- These failures don't raise errors. They show up as the wrong carrier or a wrong ship date.

**Shared limitation:** both store the cutoff as a whole hour. A future 15:30 cutoff would need a change in either design. In Design 1 that is one field type (e.g. `datetime.time`) changed in one place.

WINNER: 1