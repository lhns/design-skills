# Candidate A is the better design

**Both are correct.** Each one computes the larger of the group and member discounts, adds early bird, caps the total at 30%, rounds the ticket total half-up to the cent, and adds the 2.00 fee undiscounted. For example, a member booking early gets 20% + 15% = 35%, capped to 30%, in both versions. So the choice comes down to who has to read and change the code, and how.

**The main reader is Bea, once a year, checking against the flyer.** Her complaint was that "nobody could tell what ran in which order." Candidate A answers that directly:

- It runs top to bottom in the same order as the flyer: pick the better of group or member, add early bird, apply the cap, then add the fee.
- Each flyer sentence maps to one or two lines, and the comments repeat the flyer's wording.
- Someone who "can read a bit of Python if it's plain" can follow it in a few minutes.

**Candidate B brings back the problem Bea complained about.** To know what runs when, you have to:

- understand a decorator that registers functions into a global list;
- sort that list in your head by step number;
- know that `group` and `member` both have step 10, so their relative order depends on where they appear in the file and on the sort being stable;
- see that `group_or_member` works by deleting an entry from a dict that earlier functions filled in, and follow `min("group", "member", key=q.discounts.get)` to see which one survives;
- notice that the cap and the rounding are not rules at all, but sit in `price()` after the loop.

The pricing logic is spread across six functions, a registry and a mutable `Quote` object. That is exactly what made last year's review take an afternoon.

**B's extensibility doesn't solve the hard part.** B is built for the residents' discount, which hasn't been approved. The committee also says that if it comes, "it'll have its own rules about what it combines with." Combination rules are the hard part, and in B they would need another step-numbered rule that edits the dict, placed correctly among the others. In A, the same change is a line or two in an obvious spot, for example adding it to the `max(...)` or as another `+=`, depending on the rule. This is a single, stable rule set reviewed once a year by two people, and the plugin structure costs more than it saves.

**A smaller point:** B keeps `RULES` as a module-level list that changes on import. Reloading the module or importing it in tests could register rules twice. A has no such hidden state.

WINNER: 1