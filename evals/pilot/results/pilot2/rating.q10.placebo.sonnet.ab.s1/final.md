**Design 1 (Candidate A) is better.**

**Candidate B breaks on the planned reorganisation.** `MAX_DEPTH = 3` is hard-coded to match today's deepest chain, Parks > Grounds > Crew > Seasonal. HR's email says that from 1 November Grounds will have North and South area teams, with crews and their seasonal staff moving underneath. The chain becomes Parks > Grounds > North > Crew > Seasonal, which is one level deeper than the limit allows.

- Seasonal staff would sit at depth 4, so `members()` would skip them with only a log warning.
- Permissions granted high up, such as Timesheets on Parks, would silently stop applying to seasonal staff.
- The IT officer makes the group changes themselves and would have no reason to expect a hidden depth cap, so the failure would be hard to trace.
- A depth limit is a proxy for "this is a loop". It treats legitimate deep nesting as an error and returns a wrong answer rather than failing loudly.
- Its cycle handling is also crude. A real loop is followed to the cap, repeating work, instead of being detected.

**Candidate A handles the actual problem directly.** The `seen` set detects revisits, so loops like the Admin/Facilities one in #118 are harmless. Nesting depth is unrestricted, so the reorganisation and any future restructuring work without code changes. It is iterative, so there is no recursion limit either. With about 60 groups and 400 people, recomputing `members` per permission group is fast enough, so there is no need for caching.

**Possible follow-ups, none of which change the verdict:**
- Ticket #131 (showing why someone has a permission) is parked. If it is picked up, A's traversal could be extended to return the path or group, but that is not needed now (YAGNI).
- Silently tolerating a loop might hide a configuration mistake. Logging when a revisit happens would be cheap, though it is optional.

WINNER: 1