# On-call roster: design

## Principles

- **One pure resolver.** On-call answers are computed from stored facts on demand; nothing is materialised. *[Choice]*
- **Facts are append-only.** Each fact row has `recorded_at` and a nullable `retracted_at`, both set by the server clock. A fact is *live at T* when `recorded_at ≤ T < retracted_at` (null means never retracted). Resolving T reads only facts live at T, so edits only affect later moments and the past stays fixed (req 6). *[Choice: one bitemporal filter instead of a "not in the past" check per edit.]*
- Instants are stored in UTC. Weeks and holidays use the local calendar (tz database).

## Stored data

| Fact | Fields (plus `recorded_at`, `retracted_at`) |
|---|---|
| Engineer | id, name. Never deleted. |
| RotationEra | from_week, ordered engineers |
| Swap | week_a, week_b |
| Holiday | local date, cover engineer |
| Override | engineer, start, end, replaces (information only) |

**Week n** starts at local Monday 09:00 on `epoch_monday + 7n days`. DST weeks are simply 167 or 169 hours (req 1).

## On call at T

`on_call(T)` reads facts live at T. The first rule that matches wins:

1. **Override:** among overrides with `start ≤ T < end`, the latest `recorded_at` (ties broken by id).
2. **Holiday:** if T's local date is a holiday, its cover engineer.
3. **Rotation:** `w'` is the swap partner of `week(T)`, or `week(T)` itself if it has none. Take the era with the greatest `from_week ≤ w'`. The answer is `engineers[(w' − from_week) mod length]`. *[Choice: a new list starts with its first engineer.]*

Nested covers follow from rule 1 alone. Chris's override is newer than Ana's, so Chris has Wednesday 13:00–17:00 and Ana has the rest of Tuesday to Thursday.

Paging needs three indexed lookups: well under a second, no cache.

## Planning range and payroll

`timeline(from, to)` returns segments `(start, end, engineer)`:

- Collect the boundaries inside the range: handovers, holiday midnights, and override starts and ends. For the part already past, also collect each fact's `recorded_at` and `retracted_at`.
- The answer is constant between neighbouring boundaries. Evaluate `on_call` at the start of each segment, then merge neighbours with the same engineer.

This works for any range and any distance ahead (req 7).

**Payroll(month)** sums elapsed hours per engineer from `timeline` over the local calendar month. Rows are never rewritten and engineers persist, so a past month always reproduces exactly (req 8). *[Choice: pay elapsed hours, so a DST day counts as 23 or 25 hours.]*

## Edits

Every edit inserts a row or retracts one. Nothing is updated in place or deleted.

- **Rotation change:** insert an era whose `from_week` is after the current week. To replace a planned era, retract it first. Gaps in the current week need overrides (req 2).
- **Swap:** insert a row; retract it to cancel. Reject it if either week is already in a live swap. *[Choice: pairs only, no chains.]*
- **Holiday:** insert a row. To change the cover, retract the row and insert a new one.
- **Override:** insert one row of any length. Reject it if `end ≤ start` or the engineer is unknown.
- **Delete override:** set `retracted_at = now`.

Late edits apply from when they were recorded: an 08:00 override entered at 08:20 starts at 08:20. *[Choice: corrections to the past are payroll adjustments, outside this design.]*

## Removed

The DST correction, override splitting, "shortest wins", the holiday exception for older overrides, `schedule_cache` with its nightly job, payroll snapshots and hard deletes.
