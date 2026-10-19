**Design 1 (Candidate A) is better.**

**Why A wins**

- **Single authoritative home for site knowledge.** Each site's label, carrier, cutoff and Saturday rule live in one `SITES` table. In B, the same facts are scattered across four places: `VALID_SITES`, the label dict, the carrier conditional, and the cutoff and Saturday conditionals in `ship_date`. B's `VALID_SITES` and label dict can silently drift apart, since nothing ties them together.
- **It matches the stated axis of change.** Site details change about once a year, by whoever is on call, and a fourth site is coming. With A, adding a site or changing a cutoff is a one-line data edit, with no logic touched. With B, the on-call person must find and edit several functions. Missing one produces a `KeyError` (the label dict) or a silently wrong default (a new site would get Courier Alpha and a 16:00 cutoff, since B's conditionals fall through to defaults).
- **Safer defaults.** In B, `code == "W3"` and `code == "S2"` hard-code identities, and every other valid code falls into an implicit "else" branch. A's explicit fields force the editor to state each value for a new site. A frozen dataclass with required fields makes forgetting one a loud error at import time.
- **Error handling is centralized.** `site()` is the one place that raises `ValueError` for unknown codes (constraint 4), and `is_valid_site` stays the lone exception. B repeats `_check` in each function, so a new function can forget it.
- **Logic and data are separated.** `ship_date` in A reads as policy ("after cutoff, roll forward; skip non-shipping days"), and the site-specific numbers are data. That is easier to test and review.

**Where B is fine**

B is shorter and perfectly adequate for three static sites. But its simplicity is false economy given the known growth and yearly changes. A's table is not speculative generality: the fourth site and the yearly edits are real, observed requirements.

**Minor notes on A (non-blocking)**

- `SITES` entries mix positional and keyword args; using keywords throughout would be slightly more consistent.
- Magic numbers `5` and `6` for weekdays could be named constants (or use `calendar.SATURDAY`/`SUNDAY`).
- The `while` loop terminates because Sunday is never a shipping day, which is a fine invariant, but it would be worth a short comment if Sunday shipping ever becomes configurable.

WINNER: 1