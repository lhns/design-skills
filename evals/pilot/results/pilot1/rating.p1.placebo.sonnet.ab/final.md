**Design 2 is better.** Design 1 breaks constraint 4 and has a latent crash.

**Design 1 problems**

- **Refund semantics are wrong.** A spend can draw from several grants with different expiries. Design 1 refunds all hours as a single grant with the *first* (soonest) expiry. Its comment claims this is safe, but it is wrong in both directions:
  - Hours taken from a later-expiring grant come back with an earlier expiry, so they are lost sooner than they should be.
  - If the soonest grant has expired by refund time, the whole refund is dropped, including hours from grants that are still live. That violates "each hour goes back to the grant it was taken from and keeps that grant's expiry."
- **Refund can crash.** `refund` compares `expires > at` for an unknown spend id; `pop` raises a bare `KeyError`. More importantly, the `first = first or g[0]` idiom is fragile, and `expires` could be `None` only in edge cases, but the real issue is the lack of any explicit error contract.
- **Clarity.** Anonymous `[expires, hours]` lists, `g[0]`/`g[1]`, and `self.grants.sort()` (which sorts by hours on ties and mutates state as a side effect) hurt readability. The spend loop packs three conditions into one `if`.
- **Refund double-merge.** Refunds append new grant records instead of restoring the original, so grant identity is lost.

**Design 2 strengths**

- It records exactly which grant each hour came from (`Spend.taken` holds `(grant, hours)`), so refunds restore hours to the original grant with its original expiry, and skip only grants that have actually expired. This matches constraints 4 and 5 precisely.
- Validation is split into clear, separate errors (non-positive vs. insufficient), and both happen before any mutation, so a failed spend changes nothing (constraint 3).
- Named `Grant` and `Spend` types, a `_live` helper, and a docstring on `refund` make it much easier to read.
- Sorting uses a key on expiry and does not mutate the ledger's list.

**Minor issues in Design 2** (not decisive)

- `Spend.taken` is typed as a bare `list`; `list[tuple[Grant, int]]` would be clearer.
- Re-using a `spend_id` silently overwrites the earlier record, and refunding an unknown id raises a bare `KeyError`. Both should be explicit errors.
- `grant` doesn't validate `hours > 0`.
- Those are small, easily fixed gaps; Design 1 shares them and additionally gets the core refund rule wrong.

WINNER: 2