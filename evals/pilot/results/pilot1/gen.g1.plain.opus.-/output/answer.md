# On-call roster: redesign

## Core idea

`oncall(T)` is a **pure function** of a few small tables, with nothing precomputed. One rule fixes the past: **an edit may only change answers from the moment of the edit onward.** So the current data reproduces every past answer, and because nothing is hard-deleted, no snapshots are needed.

Instants are stored in UTC; local rules use the city's tz-database zone.

## Stored data

| Table | Columns | Meaning |
|---|---|---|
| `engineers` | id, name, active | Never deleted |
| `rotation_eras` | from_week, engineers[] | Week n → `list[(n − from_week) mod len]` |
| `week_pins` | week, engineer | Whole week assigned by a swap |
| `holiday_cover` | date, engineer | Local `[date 00:00, date+1 00:00)` |
| `overrides` | id, engineer, replaces, start, end, created_seq, deleted_at | `replaces` is for display only |

**Week n** starts on the local Monday 09:00 that is 7n days after the epoch Monday. In UTC, DST weeks last 167 or 169 hours.

**Live interval of an override** = `[start, min(end, deleted_at))`.

## On call at T

The first match wins:

1. The live override containing T with the highest `created_seq`.
2. `holiday_cover` for T's local date.
3. `week_pins` for `week(T)`.
4. The era with the largest `from_week ≤ week(T)`.

Swaps sit below holidays and overrides sit above everything, as requirements 4 and 5 ask.

**New requirement:** Chris's Wednesday 13:00–17:00 override is created after Ana's Tue–Thu override, so step 1 returns Chris for that afternoon and Ana for the rest of her cover. Nesting needs no special handling.

**Paging:** four indexed point lookups (overrides indexed on start/end) take milliseconds. There is no cache.

## Planning range [a, b)

Collect every boundary inside the range: week handovers, holiday midnights, and override starts and live ends. Within each segment between boundaries the answer is constant, so evaluate `oncall` once per segment and merge neighbours with the same engineer. A segment is shown as, e.g., "Chris (covering for Ana)".

Any range works, years ahead included; cost grows with weeks and edits, not hours.

## Payroll

Take the planning segments for the local month `[1st 00:00, next 1st 00:00)`. Sum real elapsed minutes (UTC differences) per engineer and convert to hours once. Past months reproduce exactly because of the core rule, and leavers still resolve. *(Choice: a month that has not ended is marked provisional.)*

## Edits

Each edit is one transaction at server time `now`, and it may not change any instant before `now`.

- **Rotation list change:** add an era whose `from_week` has not started; it replaces any era for the same week. Current-week gaps use overrides. *(Choice: a leaver's pins in weeks that have not started are removed, so those weeks revert to the rotation.)*
- **Swap weeks a and b:** both weeks must not have started. Write two pins, giving each week to the other week's current owner. *(Choice: pins rather than index substitution, so a later list change cannot silently swap different people.)*
- **Holiday cover:** add, change or remove rows only for dates that have not started. Today is handled with an override.
- **Create override:** `start` is clamped to at least `now`, and the override takes the next `created_seq`. `replaces` defaults to `oncall(start)`.
- **Delete override:** set `deleted_at = now`. The part already passed stays, and a future override vanishes. An edit is delete plus create.

## Removed

The cache and nightly job, payroll snapshots, override splitting, the DST index correction, "shortest wins", "holiday beats older override", index-substitution swaps and hard deletes.
