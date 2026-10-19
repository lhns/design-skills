# Design 1 (Candidate A) is better

**Candidate B will break on 1 November.** Its loop guard is a depth cap set to the current deepest chain: `Parks > Grounds > Crew > Seasonal`, with depth 0 to 3. The HR reorganisation adds one level:

```
Parks (0) > Grounds (1) > North/South (2) > Crew (3) > Seasonal (4)
```

When Timesheets (granted to Parks) is checked, the Seasonal groups are at depth 4. That is past `MAX_DEPTH`, so they return an empty set. All seasonal staff would lose Timesheets access. The only sign would be a log warning that nobody watches.

This is the worst kind of failure. It is silent, it denies access to real people, and it comes from an org-chart change that is already scheduled. The IT officer makes group changes by hand a few times a year, so nobody would think to update a constant buried in the code. The comment above `MAX_DEPTH` also makes it clear the value only describes today's structure.

B also handles #118 poorly:
- **It doesn't detect loops.** It guesses that deep nesting means a loop. Legitimate deep nesting is wrongly cut off.
- **Real loops are only bounded, not handled.** With Admin and Facilities containing each other, B keeps going around the cycle until it hits the cap. The warning it logs says "nested too deep" rather than naming the cycle.
- **Shared subgroups are walked once per path.** It is harmless at this scale, but it is wasted work.

**Candidate A fixes the actual problem.** It does a standard graph traversal with a `seen` set:
- Any group loop terminates, and each group is visited exactly once.
- There is no depth assumption, so the North/South level and any future level just work.
- It is iterative, so there is no recursion limit to think about.
- It has no constants to maintain and is easy to read.

**Possible improvements to A, none blocking:**
- A loop is almost certainly a configuration mistake. A could log it when it revisits a group, so the IT officer finds out, as happened in #118.
- `has_permission` builds full member sets. The scale is about 60 groups and 400 people, and nothing is slow, so this is fine as written (YAGNI).
- #131 ("why does someone have this permission?") is parked. A's traversal could later be extended to record the path to the person, but that shouldn't be built now.

WINNER: 1