**Candidate A (Design 2) is the better design.** Candidate B quietly removes permissions once the November reorganisation lands. Candidate A handles every known case with a single concept.

**Constraints**
- **C1:** A person has a permission if they belong to a granted group, directly or through any depth of nesting.
- **C2:** A group loop must not hang the system (#118). Loops are created by hand, so one can happen again.
- **C3:** From 1 November the chain becomes Parks > Grounds > North/South > Crew > Seasonal (HR email).
- **C4:** About 60 groups and 400 people, with no performance pressure. #131 ("why does someone have this") is parked, so neither design owes it anything.

**Trying to break B**
- Take a seasonal worker in Crew 2 after 1 November, and ask whether they get Timesheets, which is granted to Parks.
- The depths are Parks 0, Grounds 1, North 2, Crew 2 at 3, Seasonal at 4.
- Since 4 > `MAX_DEPTH`, B returns an empty set and logs a warning.
- Every seasonal worker therefore silently loses Timesheets, which violates C1.
- B's own comment shows the cause: the bound was fitted to today's deepest chain, a number that reality doesn't force.
- B also uses depth as a stand-in for "is this a loop". So it rejects legitimate deep nesting, which is a false positive. It also keeps walking a real loop up to the cap instead of noticing it, so the check is wrong in both directions.
- Fixing B means changing a number every time the org chart deepens. That is a large blast radius for a routine HR change.

**Trying to break A**
- With a loop such as Admin ⊂ Facilities ⊂ Admin, each group is visited once because of `seen`. The walk terminates and still returns everyone, so C2 holds.
- Arbitrary depth works, including the new North/South level, so C1 and C3 hold.
- If the same group is reachable by two paths, it is visited once, which is also correct.
- I could not find an input that breaks A.

**Concept count**
- A has one concept: graph reachability with a visited set. The limit is a condition, "stop when there is nothing new to visit".
- B has a depth parameter, an arbitrary constant, a log line and a special-case early return. None of these is forced by a constraint, and together they cause the failure above.

**Deciding reason:** A expresses loop safety as "don't revisit a group", which is exactly what C2 needs. B replaces that with a guessed depth cap, and the HR change on 1 November breaks it.

WINNER: 2