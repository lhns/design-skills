**Candidate A is the better design.**

**Behavior.** The two are equivalent, and both match the flyer:
- Group and member savings take the larger of the two.
- Early bird adds on top of either.
- The total is capped at 30%.
- The ticket total is rounded half-up to the cent after discounts.
- The 2.00 booking fee is added after rounding and never discounted.

For example, a member booking early gets 20% + 15% = 35%, which is capped to 30%. Neither candidate has a correctness advantage, so the choice comes down to how easy each is to review and change.

**Why A wins**
- **It reads like the flyer.** Kofi and Bea check the code line by line against the flyer each autumn. A has one short function, and its comments follow the flyer's sentences in order: group or member, then early bird, then the cap, then the fee. A reviewer can check it in a few minutes.
- **Order is visible.** Bea's complaint last year was that nobody could tell what ran in which order. In A, the order is simply the order of the lines.
- **It uses only plain Python.** A needs just `max`, `if` and `min`, which fits Bea's "a bit of Python if it's plain".

**Why B is worse**
- **It brings back the ordering problem.** B hides the order behind numeric `step` values, a global `RULES` list that is re-sorted on every registration, and decorators. To know what runs when, you must collect the step numbers from across the file. `group` and `member` share step 10, and which runs first depends on definition order and sort stability.
- **Rules interact through shared mutable state.** The "don't combine" rule `group_or_member` has to delete entries that earlier rules put into a dict, and it only works if its step number stays between the others. The flyer's single sentence "you get the better one" becomes a rule that undoes other rules.
- **The extensibility is speculative and wouldn't help.** The residents' discount might never happen, and its combination rules are unknown. In B, adding it would still mean a new rule, a step number, and probably another reconciliation rule that edits the dict, plus checking the interplay with the cap. In A, it would be one or two lines next to the existing `max` and `if`, in a place a reviewer would look anyway.
- **It adds no benefit at this scale.** At a few thousand orders a year, B's structure brings no performance or maintenance gain.

If the residents' discount is approved, the right move is to edit A's small function and review it against the new flyer. A rule framework is not needed.

WINNER: 1