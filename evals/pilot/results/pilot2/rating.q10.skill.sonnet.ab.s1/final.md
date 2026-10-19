**Constraints**
- C1 (ticket #118): group loops happen and must not hang the page. The lookup must terminate on cyclic input.
- C2 (IT officer): permissions are granted high up and people sit in the lowest group, so membership must be transitive through nesting.
- C3 (inferred from the HR email): the hierarchy will change. From 1 November, Grounds gains North and South between it and the crews, so the chain becomes Parks > Grounds > North > Crew > Seasonal. That is depth 4.
- C4 (inferred): a permission check must never wrongly deny access to someone who has it, and must not grant it to someone who shouldn't.
- C5: small data (60 groups, 400 people), so performance is not a constraint.
- C6 (#131, parked): showing why someone has a permission is not required now.

**Try to break each design**

*Candidate B*
- The input is the 1 November reorganisation. Seasonal staff under Crew 1 sit at depth 4 from Parks: Parks (0), Grounds (1), North (2), Crew 1 (3), Seasonal (4). With `MAX_DEPTH = 3`, the check `depth > MAX_DEPTH` fails at depth 4, so that group is skipped. Seasonal staff, and anyone else at that depth, silently lose Timesheets and the tool store. The only trace is a log warning that nobody reads. That breaks C2 and C4.
- Its comment, "the deepest chain we have is…", is a number taken from today's org chart. The HR email shows it is about to be wrong.
- On a real loop it does terminate (C1), but it does so by exploring the loop up to the depth limit. The cost is exponential in the branching factor, and it returns a partial result anyway.
- A depth bound is not a condition tied to a constraint. It conflates "too deep" with "cyclic", and the two are different problems.

*Candidate A*
- Loop (Admin in Facilities in Admin): `seen` stops revisiting, so it terminates. Everyone in both groups is returned, which is correct because membership in a loop is mutual (C1).
- Deeper nesting after November: there is no depth limit, so North is handled with no code change (C2, C3).
- Diamonds (a group reachable by two paths) are visited once, so no duplicated work.
- Recomputing `members(g)` per check is wasteful but fine at this scale (C5).
- It can't explain why someone has a permission (C6), but that is parked and not required. Tracking the visited path could add it later without changing the core.

**Deciding reason:** A ends on a real condition (a group already seen), so it handles loops and any nesting depth. B hard-codes a depth taken from today's chart, which the 1 November reorganisation breaks, and that silently strips permissions from seasonal staff.

**Ledger**
- Constraints: C1 terminate on loops; C2 transitive membership; C3 hierarchy deepens in November; C4 no wrong denial or grant; C5 small data; C6 parked.
- Deletions: A needs no `MAX_DEPTH`, no logging branch and no recursion parameter.
- Designer choices: none added.

WINNER: 1