# On-call roster: design

## Core rule
**A record applies only from the moment it is recorded until the moment it is retracted.** Rows are never updated or deleted, so no edit reaches a moment that has passed (req. 6).

## Stored data
- `engineer(id, name)`: never deleted.
- `rotation_era(from_week, engineers[], recorded_at)`: the ordered list from a week on.
- `assignment(engineer, start, end, layer, recorded_at, retracted_at)`, where `layer` is `week < holiday < override`:
  - *week*: a swapped week, Monday 09:00 to Monday 09:00;
  - *holiday*: one local calendar day, 00:00 to 00:00;
  - *override*: any interval, to the minute.

Instants are UTC; week and day boundaries use the city's timezone.

## Week
`week(T)` counts local Mondays from an epoch Monday to the latest local Monday 09:00 ≤ T. DST weeks simply last 167 or 169 h.

## On call at T
1. Candidates are assignments with `start ≤ T < end` and `recorded_at ≤ T < retracted_at` (null means never retracted).
2. If there are any, the highest layer wins. Within a layer, the latest `recorded_at` wins.
3. Otherwise the rotation answers. Take the era with the largest `from_week ≤ week(T)` (on a tie, the latest recorded). The engineer is `engineers[(week(T) − from_week) mod n]`.

"Replaces" is the answer at T with the winning assignment removed. *Designer choice:* derived, not stored, so it cannot disagree.

**New requirement:** Ana covers Tue–Thu for Ben, then Chris covers Wed 13–17, recorded later. At Wed 14:00 both are candidates and Chris is newer, so Chris is on call, replacing Ana. At Wed 18:00 it is Ana, replacing Ben.

**Paging:** a few indexed lookups take milliseconds; no cache.

## Planning range [a, b)
The boundaries are a, b, every handover in the range, and each assignment's effective endpoints `max(start, recorded_at)` and `min(end, retracted_at)`. Between two neighbouring boundaries the answer is constant. Resolve each segment once and merge equal neighbours. Works for any range; past segments show what actually happened.

## Payroll
Take the planning range for the local calendar month and sum the segment durations per engineer. *Designer choice:* pay elapsed hours, so DST nights count as 23 or 25 h. Past inputs never change, so reruns reproduce exactly.

## Edits
Every edit inserts rows or sets `retracted_at = now`.
- **Change the list:** insert an era. Its `from_week` must not have started; for the same week, the newest era wins.
- **Leave:** insert an era without that engineer. *Designer choice:* their future week assignments are also retracted, so those weeks fall back to the list. A gap in the current week is covered by an override.
- **Swap weeks A and B** (neither started): insert two week assignments, each giving one week to the other week's current occupant. To unswap, retract both. Chained swaps just work.
- **Holiday:** insert a holiday assignment. Change cover: insert a newer one. Remove: retract.
- **Override:** insert one. If it starts in the past, it applies only from `recorded_at`. **Delete** = retract: it stops applying now; its past part stays history.

## Ledger
- **Forced:** local-calendar weeks (1); eras by `from_week` (2); layer order (3–5: swaps lose to holidays, so a swap cannot be an override); latest-recorded wins (5); the recorded/retracted window (6); a computed timeline, not a 90-day cache (7).
- **Designer choices:** swaps as week assignments; index counted from the era's start; derived "replaces"; elapsed-hour pay; leaving retracts future week assignments; no cache.
- **Deleted:** the 168 h index and DST correction; swap index mapping; splitting overrides at handovers; shorter-wins; the older-override-loses-to-holiday exception; `schedule_cache`, nightly job and 90-day limit; payroll snapshots; hard deletes.
