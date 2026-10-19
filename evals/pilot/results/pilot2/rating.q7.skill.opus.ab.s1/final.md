# Festival ticket prices: Candidate A is the better design

**Candidate A is better.** Both candidates compute the same prices, but A states the flyer's rules in flyer order with nothing else around them. Bea's main constraint is to check the code line by line, in plain Python, and see what runs in which order. B rebuilds the very problem that made last year's review take an afternoon.

## Constraints
- **C1** Ticket 64.00. Early bird (booked by 28 Feb) saves 15%. Groups of six or more save 10%. Members save 20%.
- **C2** Group and member discounts don't combine; the better one applies. Early bird combines with either.
- **C3** Total savings are capped at 30%.
- **C4** A booking fee of 2.00 per order, never discounted.
- **C5** Decimal amounts. The ticket total is rounded to the cent, half-up, after discounts.
- **C6** Bea and Kofi check the code against the flyer line by line each year. It must be plain Python with an obvious order.
- **Not a constraint:** the residents' discount. It "hasn't happened yet", and its combining rules are unknown.

## Trying to break each candidate

| Case | A | B |
|---|---|---|
| Member, early bird (35% → capped at 30%) | 30% | 30% |
| Group and member, late booking | max = 20% | deletes the smaller, so 20% |
| Group of 6, member, early bird | 20 + 15 → 30% | 30% |
| 0 tickets | 2.00 | 2.00 |
| Rounding before the fee | yes | yes |

I found no input that breaks C1–C5 in either candidate. So correctness doesn't decide this; C6 and the concept count do.

## Checking each concept in B
- **The registry, `@rule(step)`, the step numbers and the sorting:** no constraint needs these. The step numbers (10/20/30/90) are arbitrary, and the order of execution is spread across decorators. That is exactly "nobody could tell what ran in which order" (C6).
- **`group_or_member`:** this states C2 as a deletion that runs after the fact. Its correctness depends on running after the two rules at step 10. A single `max` expresses the same fact directly.
- **`Quote.fees` as an accumulator:** it holds one fee and could just be a constant.
- **The extension point:** it serves a discount that doesn't exist yet. It also doesn't absorb that discount's real difficulty, its combining rules. Those would still need hand-written ordering logic, either as another numbered step or by changing `group_or_member`. In A, the same change is one more term in the `max`, or one more `+=`, in the place where the flyer's rule reads.
- **A hidden hazard:** `RULES` is global state that is mutated when the module is imported, so re-importing or reloading the module registers every rule twice.

## Ledger
- **Forced by the constraints:** taking the max of group and member, adding the early bird, the 30% cap, rounding half-up before the fee, and an undiscounted fee. Both candidates do all of this.
- **Designer choices:** none of consequence in A.
- **Deletions, going from B to A:** the registry, the step numbers, the `Quote` type, the fee accumulator and the post-hoc deletion rule. Removing them breaks no constraint, and the result is easier to audit against C6.

**Deciding reason:** A meets every pricing rule in about ten lines that read in flyer order, while B adds an ordering mechanism that no constraint needs. That mechanism undermines the one constraint the coordinator stressed: reading the code line by line in a visible order.

WINNER: 1