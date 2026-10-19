**Design 2 (Candidate A) is better.** Design 1 will silently break on 1 November.

**Design 1 (depth cap)**
- It guards against the #118 loop with `MAX_DEPTH = 3`, justified by the deepest current chain, Parks > Grounds > Crew > Seasonal. That chain reaches depth 3 from Parks, which is exactly the cap.
- The HR email adds a level: Grounds becomes North/South, with the crews and their Seasonal groups beneath. The chain is then Parks > Grounds > North > Crew > Seasonal, which is depth 4.
- Anything below the cap returns `set()` with only a log warning. Seasonal staff would lose Timesheets, the tool store and the minibus, with no error. Nobody would notice until staff complained, probably in April when the seasonal intake arrives.
- The cap also doesn't really detect loops. A loop that starts below depth 0 still recurses up to the cap, and it can repeat work or re-add members.
- A person who is reachable only through the over-deep path looks the same as someone with no permission. That is a silent failure in an access-control check.

**Design 2 (visited set)**
- It tracks the groups it has already seen, so a loop terminates however the groups are nested. Loops like #118 are harmless, and the result is correct because group membership through a cycle is simply the union of all the groups in it.
- It has no assumption about nesting depth, so the North/South reorganisation and any later restructuring work without code changes.
- It also visits each group once, so diamond-shaped nesting is handled efficiently. It is iterative, so there is no recursion limit either.
- It is simple and correct for the current scale of 60 groups and 400 people.

Neither candidate addresses #131 (showing why someone has a permission). That feature is parked, and a visited-set traversal could be extended to record the path later.

WINNER: 2