**Design 2 (Candidate A) is the better design.** Design 1 breaks on 1 November.

### Why Design 1 fails

Design 1 detects group loops (#118) with a depth cap: `MAX_DEPTH = 3`, matching today's deepest chain:

```
Parks(0) > Grounds(1) > Crew(2) > Seasonal(3)
```

The HR reorganisation adds a level:

```
Parks(0) > Grounds(1) > North/South(2) > Crew(3) > Seasonal(4)
```

From the Parks and Grounds roots, Seasonal is now at depth 4. `members` logs a warning and returns `set()` for it. So from 1 November every seasonal worker silently loses **Timesheets** (granted to Parks) and the **tool store** (granted to Grounds).

- Nobody gets an error. There is only a log line that a busy IT officer is unlikely to read.
- The officer is making the change correctly, as HR asked, and nothing tells him the code assumes a fixed depth.
- The only signal will be seasonal staff reporting missing access.

The underlying flaw is that depth stands in for loop detection, and the two are unrelated:

- A legitimately deep hierarchy is wrongly treated as a loop.
- A real loop is only cut off after expanding the cycle several times.
- Every reorg forces someone to remember to bump a constant whose purpose is easy to misread.

### Why Design 2 is right

Design 2 tracks visited groups (`seen`). That is the direct, correct answer to #118:

- A loop such as Admin ⇄ Facilities terminates, with each group visited once.
- There is no depth assumption, so the North/South level, or any future one, just works.
- It also handles diamonds, where one group is reachable by two paths, without duplicate work.

It is shorter, has no magic number, and has no silent failure mode. At about 60 groups and 400 people, performance doesn't matter for either design.

### Minor notes on Design 2 (not blocking)

- `has_permission` recomputes `members` for every granted group. That's fine at this scale and simpler than caching, so leave it until it's measured as a problem.
- #131 ("show which group grants the permission") is parked. Don't build it now (YAGNI). If it is picked up, the traversal is easy to extend to record the path, which a depth-capped recursion doesn't make any easier.
- A test with a two-group loop and a five-level chain would lock in exactly the behaviour that Design 1 gets wrong.

WINNER: 2