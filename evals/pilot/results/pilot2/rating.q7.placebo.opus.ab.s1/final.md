**Design 1 (Candidate A) is better.**

Both candidates compute the same price. Each takes the better of the group and member discounts, adds early bird, caps the total at 30%, rounds the ticket total half-up to the cent, and then adds the 2.00 booking fee. The difference is how easily people can read and change the code, and here A wins.

**Bea can check A line by line against the flyer.** Her yearly review compares the code with the flyer, and last year's problem was that "nobody could tell what ran in which order." A reads from top to bottom in the flyer's own order:

1. The better of group and member.
2. Plus early bird.
3. Cap at 30%.
4. Round, then add the fee.

The comments use the flyer's wording. Someone who "can read a bit of Python if it's plain" can follow all of it.

**B brings back the problem the rewrite was meant to fix.** To know what runs when, the reader has to understand three things:
- a decorator registry,
- a global list that is re-sorted on every registration,
- numeric step numbers (10, 20, 30, 90).

The order is spread across decorators, and `group_or_member` silently depends on running after the two step-10 rules. Some of the logic also stays outside the rules: the 30% cap and the rounding still sit in `price()`. So the "every rule is a plugin" picture doesn't hold, and the reader has to look in both places anyway.

**The residents' discount doesn't justify B's framework.** That discount is speculative, which is what YAGNI warns against. Bea also says that if it arrives, it will have "its own rules about what it combines with." That is exactly the part B's registry doesn't make easy: it would need another pairwise rule like `group_or_member`, with a carefully chosen step number. In A, adding it means changing a few lines inside the `max(...)` or near the early-bird check, which is a small and obvious edit.

**Scale doesn't call for B's flexibility.** There is one developer, a few thousand orders a year, and one review session per year. The extra indirection costs reading time at every review and buys nothing that is needed now.

**Small improvement for A:** name the rates as constants (`EARLY_BIRD_RATE`, `GROUP_RATE`, `MEMBER_RATE`, `GROUP_MIN_TICKETS`) next to the existing ones. Then the committee's yearly changes all happen in one block at the top.

WINNER: 1