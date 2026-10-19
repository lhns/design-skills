# Design 1 (Candidate A) is the better design

## Both are correct today

I checked each against the constraints as they stand:

- **C1 to C3 (sites, carriers, cutoffs, weekends):** both give the same answers.
  - S2 cuts off at 14:00; N1 and W3 at 16:00. "At or after" is `hour >= cutoff`.
  - Sunday is always skipped.
  - Saturday is skipped unless the site is W3.
  - Example: S2 at Friday 15:00 goes to Saturday, which is skipped, so Monday. W3 at Friday 15:00 ships Friday.
- **C4 (unknown code raises `ValueError`):** both hold. A uses `site()`; B uses `_check()`.

So the difference lies entirely in C5: a fourth site, and yearly edits by whoever is on call.

## Trying to break each under C5

**Candidate B** spreads one fact, "what a site is", over five places:
- `VALID_SITES`
- the label dict
- the carrier ternary
- the cutoff ternary
- the Saturday check

Adding site E4 means editing all five. Each place fails differently if missed:
- **Carrier, cutoff or Saturday check missed:** the `else` branches give E4 Courier Alpha, a 16:00 cutoff and no Saturday shipping. Wrong dispatch dates or carriers follow, with no error at all.
- **Label dict missed:** E4 is "valid", but `packing_label("E4")` raises `KeyError`. That breaks C4's contract, which promises `ValueError` only for unknown codes.
- **Second Saturday site (an expected yearly change):** `code != "W3"` must be rewritten into a set, and the carrier ternary must become a lookup when a third carrier appears. The structure has to change, not just the data.

**Candidate A** keeps one fact in one place.
- A site is a single row, and `Site` has no defaults. A row with a missing field fails at import.
- Valid codes are `SITES` itself, so validity can't disagree with the data.
- Changing a cutoff, carrier or Saturday flag is a one-field edit by anyone on call. No logic is touched.
- I found no event in C5 that breaks it.

## Concept count

| | A | B |
|---|---|---|
| Facts stated in two places | 0 | site set stated in 2 places (`VALID_SITES` plus the label dict) |
| Hard-coded site branches | 0 | 3 (`== "W3"` twice, `== "S2"`) |
| Places to edit for a new site | 1 | 5 |
| Silent wrong default possible | no | yes (3 `else` paths) |

A's extra `Site` dataclass is the one concept that C1 to C3 are all cases of. It is forced by C5, not ornamental. B is a few lines shorter only because it encodes the data as branches.

**Deciding reason:** under C5, B turns every site change into edits across five places, where a missed edit silently produces wrong ship dates or carriers. A turns it into a single checked table row.

WINNER: 1