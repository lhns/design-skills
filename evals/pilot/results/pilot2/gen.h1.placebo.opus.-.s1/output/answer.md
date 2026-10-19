# Solar-credit allocation: design

**Core idea:** recorded facts are never overwritten. An allocation is a pure function of the facts known at a given time, and what was sent is stored as sent. My choices are marked **[choice]**.

## Stored data (append-only, every row has `recorded_at`)

- **Member**: id, name, supplier account. Never deleted.
- **ShareEvent**: member, `effective_date`, ±shares, reason. Replaces the overwritten register.
- **Generation**: month, export-meter kWh.
- **ImportReading**: member, month, kWh. Corrections are new rows; the latest wins.
- **IssuedLine**: member, `for_month`, `issued_month`, kWh, kind (`credit`/`adjustment`). Plus one `sold` line per month for the co-op.

Dropped: community account, 5-share minimum, 15th-of-month rule, CSV snapshots, re-running for statements.

## Working out a month (rules 4.2–4.4)

`allocate(month, known_at)` uses only facts with `recorded_at ≤ known_at`.

1. **Weight** = share-days. A day's holding includes every event dated on or before it **[choice: the receiver holds shares from the transfer date]**. In #14, Hal gets 13 May-days for the 10 shares and his daughter gets 18.
2. **Cap** = the import reading. A missing reading counts as cap 0 for now and is flagged **[choice]**: over-crediting is lost for good, while under-crediting can be fixed later.
3. **Fill to caps**, in exact fractions: split what remains among uncapped members by weight. Anyone who reaches their cap is fixed there, and the rest is split again until nobody else reaches a cap.
4. **Round** by largest remainder: round every share down, then give the leftover kWh one at a time to the largest fractions (ties go to the lower member id). Caps are whole numbers, so rounding up never breaks a cap.
5. **Sold** = generation − Σ credits. Rule 4.4 holds exactly, with no balancing account.

## Monthly run (one command, by the 8th)

1. Record the generation and import readings.
2. Store `allocate(M, now)` as `credit` lines plus a `sold` line, all with `issued_month = M`.
3. **Revisions**: for each earlier month with facts recorded since the last run, compare `allocate(old, now)` with the sum of the lines already issued for it. Store each non-zero difference as an `adjustment` (±) issued in M, and do the same for `sold`. This also catches redistribution: one member's correction shifts others' credit.
4. **Supplier file**: one line per non-zero line issued in M, tagged with its `for_month` **[choice: adjustments are separate lines, not netted]**. Zero lines are never written, which fixes #22 without leaving out small holders. The `sold` total goes on the export invoice.
5. **Statement**: the member's lines issued in M, with share-days, import, whether the cap applied, and each adjustment's month and reason.

## Re-runs, reprints, audit

- **Reprint** (#29): rebuilt from the stored lines, so it is always identical.
- **Audit**: `allocate(M, issue time of M)` reproduces the original exactly, even after later transfers or corrections, because the inputs are append-only and the calculation is deterministic. The adjustment lines explain every difference since then.
- Statements are final. Corrections only ever appear as new lines.

## Register changes

- **Purchase**: +n on the issue date; counts from that day.
- **Transfer**: −n giver, +n receiver, same date; split by day.
- **Redemption**: −n; share-days stop, and the member stays for history and adjustments.
- **New member**: a Member row, then a purchase.
- **Mistake**: a reversing event plus a correct one; nothing is edited.
- **Dated in an issued month**: an event with a past `effective_date`; adjustments at the next run.

**[choice]** Revisions have no time limit. Register errors can turn up later than the supplier's three-month window, and the same mechanism handles both.
