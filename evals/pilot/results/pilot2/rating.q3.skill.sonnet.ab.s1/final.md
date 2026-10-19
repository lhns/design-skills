**Design 2 (B) is better.** Its extra constant traces to a real constraint, while A's single threshold only looks simpler because it merges two different facts.

**Constraints**
- C1 (clause 4.3): the late fee may be added only when rent is unpaid 7 days after the due date. This is contractual and applies to every tenancy.
- C2 (treasurer): what the dashboard calls "behind" must be exactly what triggers a letter.
- C3 (board, September): from January, trial the reminder at 3 days for six months. The reminder threshold is going to change, and then change back.
- C4 (inferred): never charge more than one fee per unpaid month. Both designs meet this through `fee_charged`.

**Trying to break A.** In January, the developer changes `OVERDUE_AFTER` to 3 days to run the trial. Because the fee, the reminder and the dashboard all share that one constant, the nightly job now charges 15.00 fees three days after the due date. That breaks C1 and charges tenants something the agreement doesn't allow. The alternative is to split the constant at that point. A's comment says the constant comes from clause 4.3, but the reminder policy is not a clause 4.3 rule. A states one fact where two exist, and it fails as soon as C3 takes effect.

**Trying to break B.**
- Setting `REMINDER_AFTER` to 3 moves the dashboard and the letters together, because both use `is_overdue`. C2 holds, and the auditor's problem can't recur.
- `LATE_FEE_AFTER` stays at 7, so C1 holds.
- The two constants are both 7 today, but they change for different reasons: one is board policy and the other is contract. That is not duplication. Merging them is what makes A fragile.

**Concept count.** B has one more constant and one more predicate than A. Both trace to C1 and C3. A has fewer concepts only by dropping the distinction between policy and contract, which is false elegance.

**Minor points on B**
- `is_overdue` is now driven by `REMINDER_AFTER`. A name like `is_behind` would describe it better, but that is cosmetic.
- When the trial ends in July, the housing officer decides whether to revert the constant or keep it at 3. That is a policy decision, not code.

**Ledger**
- Constraints: C1, C2, C3, C4 (inferred).
- Forced decisions: the fee threshold is separate from the reminder threshold, and the dashboard and the reminder share one predicate.
- Designer choices: none new. The 3-day trial value comes from the board.
- Deletions: none. A's single threshold is rejected because it violates C1 once C3 applies.

Deciding reason: the reminder timing is a policy that will change, while the fee timing is a contractual rule that must not, so B keeps them as separate constants.

WINNER: 2