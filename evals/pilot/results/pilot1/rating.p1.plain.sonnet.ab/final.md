**Design 2 is better.** Design 1 violates constraint 4, and Design 2 satisfies it.

**Design 1 (Candidate A)**
- A spend that draws from several grants is stored as a single `(hours, first expiry)` pair, so the per-grant breakdown is lost.
- On refund, every hour comes back with the soonest grant's expiry. Hours taken from a later-expiring grant return with a shorter life than they had, which breaks "each hour goes back to the grant it was taken from and keeps that grant's expiry".
- If the earliest grant has expired by refund time but the other grants have not, A drops the whole refund. Hours from the still-live grants are lost, though they should be returned.
- The code comment says the early expiry is safe because the refund "never outlives the credit it replaces". That is true, but it ignores that the refund can end up much shorter than the credit it replaces.
- A mutates and re-sorts `self.grants` in place and uses bare `[expires, hours]` lists, so the structure is opaque and fragile. `first = first or g[0]` also relies on truthiness.

**Design 2 (Candidate B)**
- Each spend records `(grant, hours taken)` pairs, so it keeps the exact provenance of every hour.
- Refund restores hours to the original grant object. The expiry is preserved automatically, and a grant that has expired by refund time is skipped, which matches the requirement exactly.
- Spend takes grants soonest-expiry first. The balance is checked before any mutation, so a failed spend changes nothing. Non-positive spends are rejected.
- `pop` on the spend id prevents double refunds.
- The `Grant` dataclass and `_live` helper make the code clearer.

Both designs share minor gaps. Neither validates grant amounts, and both raise `KeyError` on an unknown spend id. These don't change the verdict.

WINNER: 2