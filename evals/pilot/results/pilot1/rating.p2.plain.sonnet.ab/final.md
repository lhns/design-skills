**Candidate A (Design 1) is the better design.**

**Why A wins**

- **Single source of truth.** Every fact about a site (label, carrier, cutoff, Saturday shipping) lives in one `SITES` record. The four functions are thin readers of that table. In B, the same site identity is scattered across five places: `VALID_SITES`, the label dict, the carrier conditional, the cutoff conditional, and the Saturday conditional.

- **Adding the fourth site is a data change.** In A, you add one line to `SITES`. Validation, label, carrier, cutoff and Saturday rules all follow. In B, you must edit `VALID_SITES`, the label dict, and the carrier and cutoff logic, and fix the Saturday check. If one is missed, the failure is silent. For example, a new site added to `VALID_SITES` and the label dict but not the carrier branch would quietly be assigned "Courier Alpha". B's `else` fallbacks (`"Courier Alpha"`, `16`) make a forgotten edit a wrong answer instead of an error.

- **Changes happen yearly and are made by whoever is on call.** That favors a design where a change is a one-line, low-context edit to a table, with the field names documenting the meaning (`cutoff_hour`, `ships_saturday`). In B, the on-call person has to understand the logic in several functions and hardcoded special cases like `code == "S2"` and `code != "W3"`. Changing W3's carrier or giving N1 Saturday shipping means editing control flow, which is riskier.

- **Validation cannot drift.** In A, `is_valid_site` and the `ValueError` behavior derive from the same dict keys, so the "valid" set and the "known" set can't disagree. In B, `VALID_SITES` and the other mappings are separate and can diverge.

- **Constraint 4 is met in one place.** `site()` is the single choke point raising `ValueError`. B repeats `_check` in each function, which is easy to forget in a new one.

**Minor notes on A**

- `from None` suppresses the noisy `KeyError` chain, which is a good touch.
- Mixing positional `label` with keyword arguments is fine, but you could make all fields keyword-only.
- Both versions share the same behavior on the edge cases: the cutoff is inclusive (`>=`), and the weekend skip loop handles Sunday and non-Saturday sites correctly. So the difference is purely maintainability, and A is clearly stronger there.

B is acceptable for exactly three static sites, but the stated requirements (a fourth site soon, yearly attribute changes, edits by rotating on-call staff) are precisely the case where table-driven data beats scattered conditionals.

WINNER: 1