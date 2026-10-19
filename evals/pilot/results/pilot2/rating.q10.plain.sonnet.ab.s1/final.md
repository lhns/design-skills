**Candidate A is the better design.**

**Candidate B has a hard-coded depth limit that the 1 November reorganisation breaks.**
- `MAX_DEPTH = 3` is justified by the current deepest chain, Parks > Grounds > Crew > Seasonal. That puts Seasonal at depth 3, which is just allowed.
- The HR email says Grounds will be split into North and South, with the crews and their seasonal staff moving under them. The chain becomes Parks > Grounds > North > Crew > Seasonal, so Seasonal sits at depth 4.
- Anyone reaching Timesheets (granted to Parks) or the tool store (granted to Grounds) only through a Seasonal group would silently lose the permission. The only trace is a log warning, and `members` returns an empty set for that branch.
- The limit is also a poor way to detect loops. It cuts off legitimate deep nesting, and a real loop is still re-walked up to the depth limit, repeating work and logging warnings each time.
- Fixing it means someone has to remember to edit the constant. The IT officer makes the group changes personally, so a mistake here would be easy to miss.

**Candidate A handles the actual problem, loops, directly.**
- It tracks visited groups, so a cycle like Admin ⇄ Facilities (#118) terminates after visiting each group once.
- It has no limit on depth, so adding North and South levels, or any later restructuring, needs no code change.
- It is iterative, so there is no recursion limit.
- At about 60 groups and 400 people, the cost of recomputing membership per check is irrelevant.

Neither candidate implements #131 (showing why someone has a permission), but that is parked and not a deciding factor. A would be easier to extend for it by recording the path while traversing.

WINNER: 1