**Design 1 is better.** It keeps the constraint that a missed duplicate costs the payment. Design 2's 60-day window drops it.

**Constraints**
- C1: A missed duplicate costs the payment, while a held invoice costs a few minutes. Errors should therefore fall on the side of holding.
- C2: Numbers arrive in varying shapes, and amounts can't be matched on. Both designs handle this the same way, with `normalise` and no amount check.
- C3: Some suppliers restart numbering each January, so a same-number invoice from a previous year is not a duplicate.
- C4: The printed invoice date is sometimes empty.
- C5: Statements arrive about two weeks after quarter end, with copies of every invoice from that quarter stapled behind. The post room can't always tell a copy from an original.

**Trying to break each design**
- **Design 2, C5:** An invoice entered on 3 January is copied behind the statement that arrives about 15 April. That is roughly 100 days later, so it falls outside the 60-day window. The copy isn't held and gets paid twice, which is exactly the scenery-hire loss. Any window shorter than a quarter plus the statement lag misses such copies.
- **Design 2, C3:** The window handles the January restart only by luck. A December 0045 and a January 0045 from a restarting supplier are within 60 days, so they still raise a false alarm. The window is also a number that was picked, not derived from anything. Its comment says it is "long enough to catch a re-sent invoice", but nothing in the constraints supports that length.
- **Design 2, C4:** It uses `received_on`, which is always present, so it copes with a missing printed date. It copes only because it never looks at the date that distinguishes the cases.
- **Design 1, C5:** A copy carries the same printed date as its original, so it has the same year and is held, however many months later it arrives. A Q4 copy arriving in January is still held.
- **Design 1, C3:** Last year's 0045 and this year's 0045 have different printed years, so there is no false alarm.
- **Design 1, C4:** A missing date returns `True`, which holds the invoice. That is the safe direction under C1, and the cost is a few minutes.
- **Design 1, remaining weakness:** A mis-typed printed year could hide a duplicate. This is rare, and Design 2 has the same kind of risk through its window.

**Why Design 1 fits**
- **Matching rule:** It matches on the fact that actually separates reuse from re-sending. A supplier doesn't reuse a number within the year printed on its invoices.
- **Missing dates:** Design 1 turns uncertainty into a hold rather than a miss.
- **No invented number:** It has no unforced constants, no window to tune and no exception clauses.

**Ledger**
- Constraints: C1 to C5 above.
- Forced: matching on supplier, normalised number and printed year. A missing date must not rule a match out.
- Designer choices: none in Design 1. Design 2's 60-day value is an unforced choice and it fails C5.
- Deletions: Design 1 needs no time window and no tuning constant.

Design 1 wins because it never lets a copy slip through on grounds the constraints don't support, whereas Design 2's arbitrary window misses quarterly statement copies.

WINNER: 1