# Solar-credit allocation: design

**Invariant:** a month's allocation depends only on what was recorded up to a given date. That makes statements reproducible and turns every correction into a difference between two allocations.

## Stored data (append-only, every row has `recorded_on`)

1. **Member**: account number. Kept at zero shares, since corrections may still reach it.
2. **Share entry**: member, effective date, ±shares. A holding on any day is the sum of entries up to that day.
3. **Reading**: meter, month, kWh. The meter is a member account (import) or the array (generation). A supplier correction is a new row.
4. **Run**: run date. Sent files are archived as evidence only.

The community account, the 5-share minimum, the 15th rule and the CSV folder are gone.

## Allocating month *m* as of date *t*

`allocate(m, t)` is a pure function. It uses only rows recorded by *t*, and the latest reading per meter.

1. **Weight** (4.2): share-days in *m*. *Choice:* an entry counts from the start of its effective date. Hal (#14) keeps 13 days on his 10 shares, and his daughter gets 18.
2. **Cap** (4.3): the member's import. *Choice:* no reading yet means cap 0. That never breaks the supplier limit, and the late reading comes in as a correction.
3. **Water-fill** (4.3): find λ with Σ min(capᵢ, λ·weightᵢ) = min(G, Σ caps). Unusable credit is shared out in the same proportions.
4. **Whole kWh** (4.4): round down, then hand out the remaining kWh by largest fractional part, ties by account. Whole-kWh caps mean no one is pushed over their cap.
5. **Sold** = G − Σ credits. This is non-zero only when every member is capped. Credits plus sold equal G exactly.

## Monthly run (by the 8th)

For run date *t* and previous run *t′*, for every month *m*:

> line(member, m) = allocate(m, t) − allocate(m, t′)

- For the new month this is the full credit. For earlier months it is the correction, positive or negative.
- A late reading or a backdated share entry re-water-fills the whole month, so several members may move, as 4.3 requires.
- Zero lines are left out (#22). Sold kWh goes to the supplier on the same difference basis.
- No time window is needed: any correction is settled at the next run.

*Assumption, to confirm with the supplier:* each line carries the month it credits, so the supplier checks it against that month's import. Otherwise a positive adjustment could be lost to the current month's cap.

## Statements, reprints, audit

- **Statement** for run *t*: the member's lines, with the weight, import and cap behind each one. It is final once sent.
- **Reprint** (#29) and **audit**: recompute as of the same *t*. Inputs are only added, never changed, so the result matches what was sent, whatever happened since. A mismatch points to a program fault.

## Register changes

| Change | Entries |
|---|---|
| Purchase / new member | +n |
| Redemption (partial or full) | −n; never below 0; member kept |
| Transfer | −n seller, +n buyer, same date |
| Mistake | compensating entry, never an edit |
| Backdated (already-run month) | allowed; settled at the next run |

## Ledger

- **Forced:** dated append-only entries and readings; water-fill; correction = difference between allocations.
- **Designer choices:** effective-date convention; missing reading → cap 0; largest remainder; backdating allowed; one readings table; month-tagged lines.
- **Deleted:** community account (breaks 4.4, no meter); 5-share minimum and 15th rule (both break 4.2); CSV folder and overwritten readings (made re-runs unreproducible).
