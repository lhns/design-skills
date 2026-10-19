**Constraint check (C4 is the decider).** Refund must return each hour to the grant it was taken from, keeping that grant's expiry, and drop hours whose grant has expired at refund time.

**Design 1 breaks C4.** It records one expiry per spend (the first grant's) and refunds all hours under it. A concrete failure:
- Grant 5h at day 0 (expires day 90) and 5h at day 30 (expires day 120). Spend 8h at day 31: 5h from the first grant, 3h from the second. `first` = day 90.
- Refund at day 100. Correct: the 5h from the first grant are lost (expired), and 3h return to the day-120 grant. Design 1: the expiry day 90 is not after day 100, so all 8h are dropped. 3 live hours are lost.
- Refund at day 80 gives the opposite error. All 8h return with expiry day 90, so the 3h that belonged to a day-120 grant now expire 30 days early.

Its comment claims the shortcut is safe, but it is safe only against over-crediting, not against under-crediting or shortened expiry. The constraint says "each hour goes back to the grant it was taken from", and a single expiry per spend cannot represent that.

Other defects in A:
- `first = first or g[0]` is fine for datetimes, but the sort `self.grants.sort()` compares `[expires, hours]` lists, so ties compare hours. This is harmless, though the sort is a hidden mutation.
- Refunds append new grants rather than restoring the originals, so fragments accumulate.
- `refund` with an unknown id raises `KeyError` and a double refund is blocked only via `pop`. B behaves the same here.

**Design 2 meets all constraints.**
- C1: `at + VALIDITY` for every grant.
- C2: sorts live grants by expiry and draws in that order.
- C3: validates before mutating; it checks positivity and sufficiency first, so a failed spend changes nothing.
- C4: the `taken` list stores `(grant, hours)` pairs, so refund restores each hour to its own grant, keeping the expiry. Expired grants are skipped.
- C5: `balance` counts only live grants.
- C6: the caller passes `at`, and there are no clock reads.

**Concept count.** B has two more types (`Grant`, `Spend`), but each one traces to C4. The spend must remember per-grant provenance, and the grant must have identity so it can be restored. A's smaller shape is false elegance, because it drops that constraint. A also carries an unjustified exception in its comment-justified approximation. B has no special-case branches beyond the `take` guard, which is a skip of empty grants.

One minor point for B: `spend` could skip the `if take` check by filtering out empty grants in `_live`, but that is cosmetic.

**Deciding reason:** only Design 2 stores which grant each hour came from, which C4 forces. Design 1 collapses that into one expiry and refunds the wrong amount or the wrong expiry.

WINNER: 2