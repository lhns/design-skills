# Design 1 (Candidate A) is better

## The deciding issue: Candidate B breaks on 1 November

Candidate B handles group loops (#118) by capping nesting depth. `MAX_DEPTH = 3` is set to the deepest chain that exists today: Parks > Grounds > Crew > Seasonal. The HR email adds a level. From 1 November the chain becomes:

```
Parks (0) > Grounds (1) > North/South (2) > Crew (3) > Seasonal (4)
```

Timesheets is granted to Parks. When `members(Parks)` reaches the Seasonal groups, they are at depth 4, which is greater than `MAX_DEPTH`, so they return an empty set. **Every seasonal worker loses Timesheets access** as soon as the IT officer makes the restructure.

This is the worst way for it to fail:
- **It is silent where it matters.** The permissions page just answers "no". The only signal is a log warning that a team which rarely changes groups is unlikely to read.
- **It is partial.** The tool store (granted to Grounds) and minibus (granted to crews) still work for seasonal staff. So the problem looks like a strange Timesheets bug, not a nesting limit.
- **It mislabels the cause.** The warning says deep nesting "is treated as a group loop". Someone investigating would go looking for a cycle that doesn't exist.

Raising the constant would fix this case, but that is the real flaw. The limit encodes today's org chart into the code, and that limit is wrong whenever the org chart grows. It also doesn't detect loops properly. It just stops after N levels, and on a loop it still walks and repeats work up to that depth.

## Why Candidate A is right

- **Loops are handled correctly.** The `seen` set stops a cycle like Admin ⇄ Facilities after one visit, so the #118 hang cannot happen again. Nothing is skipped.
- **Depth doesn't matter.** Adding North/South, or any later restructure, needs no code change.
- **It's iterative.** There's no recursion limit and no extra bookkeeping.
- **Performance is fine.** With about 60 groups and 400 people, recomputing `members` for each check costs nothing, as the IT officer says.

## Minor notes (not deciding)

- Candidate A drops the loop warning that B has. If you want to know a loop exists (#118 was removed by hand), you could log when a group is reached twice on the same path. But a group can also legitimately appear under two parents, so that check needs care.
- Neither candidate addresses #131 ("why does this person have this permission"). Candidate A's traversal could easily be changed to record the path to the person, but that ticket is parked.

WINNER: 1