**Design 1 is the better design.** Design 2 breaks constraint 4, and Design 1 satisfies every constraint.

## Design 2 (Candidate A): incorrect refunds

Constraint 4 says each hour goes back to the grant it came from and keeps that grant's expiry. Design 2 records only the total hours and the *earliest* expiry among the grants touched, then refunds everything under that one expiry. This gives two wrong outcomes:

- **Hours lost early:** Say a spend takes 2h from grant X (expires day 10) and 3h from grant Y (expires day 80). If the booking is cancelled on day 20, X has expired, so only 2h should be lost. Design 2 sees `expires <= at` and drops all 5h, including the 3h from Y that is still valid.
- **Hours expiring early:** If the cancellation happens on day 5, the refund creates a 5h grant that expires on day 10. The 3h that belonged to Y now expire 70 days sooner than they should, which silently shortens the customer's credit.

The code comment claims the approach "never lets a refund outlive the credit it replaces". That is true, but it is the wrong goal. The requirement is to preserve each hour's own expiry, not to be conservative. The comment justifies a deviation from the spec rather than meeting it.

Other weaknesses:
- The `[expires, hours]` lists are positional and cryptic. `g[0]`, `g[1]`, and `first = first or g[0]` hide intent.
- Sorting the shared list in `spend` is a side effect, and the guard `g[0] > at and g[1] and left` is dense.
- Refunds append new grants instead of restoring the original ones, so the list grows with each refund.
- It merges the "invalid" and "insufficient" errors into one vague message.

## Design 1 (Candidate B): correct

- **Constraint 2:** It sorts live grants by expiry and takes from the soonest first.
- **Constraint 3:** It validates positivity and sufficiency before mutating anything, so a failed spend changes nothing. It also gives distinct, actionable messages.
- **Constraint 4:** It records `(grant, hours)` pairs per spend. A refund returns each portion to its own grant if that grant is still unexpired, and it drops only the expired portions.
- **Constraint 5:** `balance` counts only live grants through `_live`.
- **Readability:** Named `Grant` and `Spend` types, a single `_live` helper, and a docstring that states the contract.

Small improvements it could use, none of them blocking:
- Reject duplicate `spend_id`s, since they currently overwrite silently.
- Raise a clear error for an unknown `spend_id` instead of a bare `KeyError`.
- Validate that `grant` hours are positive.
- Use a typed `list[tuple[Grant, int]]` for `taken`.

These are polish. Design 2's flaw is a functional bug against the stated requirements.

WINNER: 1