**Design 2 (Candidate A) is better.** The deciding reason is that its loop guard is a condition, "stop at a group already visited", while Candidate B's is a depth number that the HR change breaks in two weeks.

**Constraints**
- C1: A group loop must not hang the page (#118, stated).
- C2: Permissions granted high up must reach everyone below, including seasonal staff in crews (IT officer, stated).
- C3: From 1 November, Grounds splits into North and South, with crews and their seasonal staff beneath them (HR email, stated). The deepest chain becomes Parks > Grounds > North > Crew > Seasonal, which is 5 levels.
- Not constraints: #131 (parked) and performance (60 groups, 400 people, nothing is slow).

**Trying to break each design**
- **B on 1 November:** `members(Parks)` runs at depth 0 for Parks, 1 for Grounds, 2 for North, 3 for Crew and 4 for Seasonal. Depth 4 is greater than `MAX_DEPTH = 3`, so Seasonal returns an empty set, and the only trace is a log warning. Seasonal staff silently lose Timesheets and the tool store, which violates C2 after the reorganisation. The code comment ("deepest chain we have is…") records a fact that HR has already invalidated. B also handles a loop only by cutting off deep branches, not by recognising the loop.
- **A:** `seen` guarantees each group is expanded once, so C1 holds at any nesting depth. Members of a loop are correctly treated as one set, and C2 and C3 hold with no change. I can't construct an input that breaks it. The group count is finite, so it always terminates.

**How each rejected the alternatives**
- B's `MAX_DEPTH` is an unforced number. Reality forces "stop on a loop", not "stop at 3". It also conflates two problems: loop detection and depth limits. Only the first is needed.
- A's `seen` set is the minimal condition that solves #118 and nothing more.

**Counts:** A has one guard (`seen`) and no magic numbers or logging branch. B has one constant, one early-return branch and a logging path, and it has a latent failure mode that triggers on a known date.

**Ledger**
- Constraints: C1, C2, C3.
- Forced: a visited-set guard, which is independent of depth.
- Designer choices: none.
- Deletions: `MAX_DEPTH`, the depth parameter and the warning branch.

WINNER: 2