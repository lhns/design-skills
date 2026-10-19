# Design 1 (Candidate A) is better

**Constraints**
- **C1:** Group loops can happen. Ticket #118 shows one did, and it hung the page. The design must terminate when one exists.
- **C2:** Permissions are granted high in the tree and inherited by everyone below. Timesheets goes to Parks, and Seasonal staff sit at the bottom.
- **C3:** On 1 November the hierarchy gains a level: Parks > Grounds > North/South > Crew > Seasonal.
- **C4:** Scale is small (60 groups, 400 people), so performance doesn't decide anything.

**Trying to break each design**

*Candidate B.* Depth is counted from the group a permission is granted to: Parks = 0, Grounds = 1, North = 2, Crew = 3, Seasonal = 4. After the reorg, `depth > MAX_DEPTH` is true at Seasonal. When `has_permission(seasonal_person, Timesheets)` is checked against Parks, that subtree returns `set()`.

So every seasonal worker silently loses Timesheets on 1 November. The only sign is a log warning, which reads like a loop warning. The code's own comment, "the deepest chain we have…", records the assumption that the HR email is about to make false.

B does terminate on a loop. But it does so by recursing until it reaches a number, not by detecting the loop. It cannot tell a cycle from a legitimately deep tree. Every future reorg can break it again. It breaks C2 under C3.

*Candidate A.* A `seen` set ends the traversal at the first group it revisits. So:
- a loop terminates (C1);
- any depth works (C2, C3);
- there is no number to keep in step with the org chart.

I could not find an input that breaks it. The ID `#118` is now stated in the docstring, but the function no longer contains a special case for it.

**Concept count**
- **A:** one concept, the visited set. It is forced by C1 and is a condition: "stop at a group already seen".
- **B:** a depth counter, an unforced number (`MAX_DEPTH = 3`), a fact stated twice (the comment describing the current tree, plus the constant that must match it), and a logging path. It also never visits the same group twice only by accident.

A has fewer concepts and no arbitrary bound. It also has a smaller blast radius: when the org chart changes, nothing in A needs to change.

**Side note on #131 ("why does this person have it")**

This request is parked, so neither design needs to address it. If it is picked up later, A's traversal is the natural place to record the path that reached each person.

**Deciding reason:** B treats depth as a stand-in for "loop", and the November reorg makes that stand-in false: seasonal staff would silently lose permissions. A detects the loop itself, so the reorg cannot break it.

WINNER: 1