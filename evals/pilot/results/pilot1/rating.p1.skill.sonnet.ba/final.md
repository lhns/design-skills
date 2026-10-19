**Design 1 is the better design, because it is the only one that meets constraint 4.**

**Design 2 breaks C4.** It records a spend as `(hours, first expiry)` and refunds every hour with the soonest expiry among the grants touched. C4 says each hour goes back to the grant it came from, with that grant's expiry. Two concrete failures:

- Grant A (10h, expires day 90) and grant B (10h, expires day 150). A spend of 15h takes 10 from A and 5 from B. Refunding on day 80 returns 15h all expiring on day 90, so B's 5h lose 60 days of validity. A refund on day 95 returns nothing, although B's 5h are still live and C4 says they must come back.
- Its comment claims the refund never outlives the credit it replaces. That is true, but the constraint also forbids shortening the credit, and the design does shorten it.

The design collapses a spend into one number plus one expiry. That is a lossy representation of what C4 requires: a spend is a set of (grant, hours) pairs. Its brevity comes from dropping that fact, which makes it falsely elegant.

**Design 1 meets every constraint.**

- C1: `grant` sets `expires = at + VALIDITY`, for paid and goodwill grants alike.
- C2: it sorts live grants by `expires` and takes from the earliest first.
- C3: the check runs before any mutation, so a failed spend changes nothing. Non-positive spends are rejected.
- C4: `Spend.taken` keeps `(grant, hours)` pairs. Refund returns each portion to its own grant, which keeps its expiry. A portion is dropped only if that grant has expired by `at`.
- C5: `_live` filters on `expires > at`, and `balance` uses it.
- C6: all times are passed in, and amounts are integers.

**Concept check.** Design 1 has one extra concept, `Spend`, which records where the hours came from. C4 forces it. Design 2 has fewer parts, but it needs a comment to justify a deviation from the constraint, and that is an exception clause in disguise.

**Shared weaknesses, not differentiators.** Both designs have these gaps:

- Neither validates grant amounts.
- Neither handles a duplicate `spend_id`, which would overwrite the earlier record.
- Neither handles refunding an unknown id; both raise `KeyError`.

Design 1 is also slightly sloppier about leaving zero-hour grants in the list, which is harmless.

**Deciding reason:** only Design 1 returns each hour to the grant it came from with that grant's expiry, which is what C4 requires.

WINNER: 1