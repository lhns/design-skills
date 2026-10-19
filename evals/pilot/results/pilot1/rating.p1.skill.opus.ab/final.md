# Candidate B is the better design

**Candidate A breaks constraint 4. Candidate B keeps every constraint.**

## Breaking Candidate A

Constraint 4 says each refunded hour goes back to the grant it came from and keeps that grant's expiry. A records only `(hours, first_expiry)` per spend, so it returns all hours with the earliest expiry. A concrete case that breaks it:

- Day 0: grant 1h. It expires on day 90.
- Day 60: grant 5h. It expires on day 150.
- Day 61: spend 6h. One hour comes from grant 1 and five from grant 2.
- Day 100: refund.
  - **Constraint 4 requires** 5h back, because grant 2 is still live.
  - **A returns 0h,** because `first` (day 90) has passed.
  - **If the refund came on day 70 instead,** A would return 6h that all expire on day 90. That cuts 60 days off five of the hours.

A's comment ("never lets a refund outlive the credit it replaces") turns "keep each hour's own expiry" into "never exceed the original expiry". That is a weaker constraint. The design gets simpler only by dropping a requirement, which is false elegance. A's refund also creates a new grant entry instead of restoring the original one. That is harmless for the balance, but it is another sign that A does not record where each hour came from.

## Checking Candidate B

| Constraint | How B meets it |
|---|---|
| C1: 90-day expiry | `VALIDITY` is applied in `grant`. |
| C2: soonest expiry first | `spend` sorts live grants by `expires`. |
| C3: atomic, positive spend | Both checks run before any mutation, so a failed spend changes nothing. |
| C4: per-grant refund | `Spend.taken` keeps `(grant, hours)` pairs. A refund adds each amount back to that exact grant and skips grants that have expired. |
| C5: balance counts live grants only | `_live` filters by `at`. |

I found no input that breaks any of these.

## Is B's extra structure justified?

B has one more concept than A: `Spend.taken`, the record of which grant each hour came from. Constraint 4 forces it, because a per-grant refund is impossible without knowing the per-grant origin. A is shorter only because it leaves that constraint out.

**Deciding reason:** B keeps the per-grant record that constraint 4 requires, while A replaces it with a single expiry and returns the wrong hours with the wrong expiries.

WINNER: 2