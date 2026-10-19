# Candidate B is the better design

**Deciding reason:** the chart is the constraint (C1, C4). B stores each chart row once and derives the inverse. A stores a formula the constraints never ask for, then patches it with two correction tables that must be kept in sync by hand.

## Trying to break each design

**C1, exact match.** Both pass today. I checked A row by row:
- For UK 6 the formula gives 39.37, which rounds to 39.5; the adjustment makes it 39.
- For UK 7.5 it gives 41.275, which rounds to 41.5; the adjustment makes it 41.
- In the other direction, EU 39 gives 5.709, which rounds to 5.5; the adjustment makes it 6.
- Every other row falls out of the rounding, some only narrowly. UK 6.5 gives 40.005, and EU 37.5 gives UK 4.528.

So A is correct, but only by coincidence of rounding margins.

**C2, rejection.** Both pass. A guards with a round-trip check, `uk_to_eu(uk) != eu`. For example, EU 39.5 maps to UK 6, but `uk_to_eu(6)` returns 39, so A rejects it. B rejects through a missing key.

**C3, numeric input.** Both pass. `6.0 == 6` and they hash the same, so B's dict lookup and A's `in UK_SIZES` both accept it.

**C4, rows edited by hand.** This is where A breaks. Suppose next year's complaint moves UK 6.5 from EU 40 to 40.5:
- In B, you edit one number.
- In A, you have to:
  1. recompute the geometric value;
  2. add an entry to `UK_TO_EU_ADJUST`;
  3. work out what `eu_to_uk(40.5)` now produces, and see that it collides with UK 7;
  4. reason about `EU_TO_UK_ADJUST`.

  An edit can also silently move a row that sits near a rounding boundary. One fact, an EU value, lives in two places in A: the forward adjustment and the inverse adjustment. A's blast radius for a one-row change is the whole formula. B's is one cell.

## Concept count

| | A | B |
|---|---|---|
| Unforced numbers | 3 constants (barleycorn, offset, Paris point) | 0 |
| Correction tables | 2 | 0 |
| Rounding rule | 1 | 0 |
| Exception entries | 3 (the adjustments) | 0 |
| Facts stated twice | yes (adjustments mirror each other) | no (inverse derived) |
| Chart table | 0 | 1 |

A's physical model is a named theory that deletes no cases. It reproduces most rows, then needs exceptions for the rest. The constraints say the domain is irregular: hand-set and individually adjusted. So the guide's rule applies: use a table, and name C4 as the reason.

## One gap in B worth closing

`EU_TO_UK` silently drops a row if an edit ever maps two UK sizes to the same EU size. Then `eu_to_uk` would return only one of them, and C1 would fail without any warning. One line restores the invariant:

```python
assert len(EU_TO_UK) == len(UK_TO_EU), "chart must be one-to-one"
```

WINNER: 2