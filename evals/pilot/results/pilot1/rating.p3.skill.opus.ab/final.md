**Design 2 (Candidate B) is better.**

**The deciding constraint is C4.** The two exports have different owners (the board, by circular, and the cooperative office, on member request) and change on different schedules. A change to one must never alter the other's output.

**Trying to break Candidate A against C4:**
- A circular reorders the board columns to grade first. The shared `row = [d.member_id, date, weight, d.grade]` line feeds both exports, so the edit either moves the statement columns too or forces a new `if for_board` branch.
- The office asks for weights in kg. The `weight` line holds both formats, so the edit happens right next to the board's format, and one slip changes the board report.
- A circular asks for rejected loads with a flag column. The `continue` and the trailing `if not for_board` block now interleave, and every later change has to reason about both exports at once.

Each change to either export touches code that also produces the other. C4 can only be kept by care, not by structure. The blast radius of every change is both exports.

**Candidate B against C4:** No line in `board_rows` affects `statement_rows`, and the reverse is also true. No input or change request to one function can alter the other's output. C4 holds by construction.

**Checking each concept in A:**
- The `for_board` flag is a concept no constraint names. C5 says each export has exactly one caller, so there is no shared caller choosing between modes.
- The flag produces four branches on itself and two dual-purpose lines. These are the classic signs of a representation that doesn't fit: two things forced into one.

**On duplication in B:**
- **Sort key:** both exports currently sort by `(d.date, d.ticket)`, but that is two facts that happen to coincide today, not one fact. Each authority can change its own ordering, so merging the keys would recouple the exports.
- **Loop shape:** the repeated loop is similar code that changes for different reasons. That is not duplication, and merging it is exactly what A did wrong.

**Counts:**

| | A | B |
|---|---|---|
| Flag parameters | 1 | 0 |
| Branches on export kind | 4 | 0 |
| Lines shared across exports | 3 | 0 |
| Concepts | 1 function serving 2 purposes | 2 functions with 1 purpose each |

A is shorter, but only because it gives up C4's guarantee.

**Deciding reason:** B makes C4 a structural fact, while A's shared lines and flag branches mean every format change to one export touches code that produces the other.

WINNER: 2