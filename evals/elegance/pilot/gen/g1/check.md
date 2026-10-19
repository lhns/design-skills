# g1 check (judge only)

## Constraint checklist
Each must hold in `answer.md`. A dropped constraint fails the run, however elegant the rest.

1. Weekly round-robin with handover Monday 09:00 **local**, correct across daylight-saving weeks (167 h and 169 h weeks).
2. List changes take effect from a week not yet started; earlier weeks are unaffected.
3. Whole-week swaps between two engineers.
4. Holiday cover replaces rotation and swaps for the whole local calendar day.
5. Overrides: any interval, to the minute, any length, overlapping and nested; the newest wins where they overlap; overrides beat holidays and rotation; deletion supported.
6. The past is fixed: no edit changes who was on call at a past moment; past payroll reproduces exactly.
7. "Now" answered within a second; the planning page answers **any** range, including more than a year ahead.
8. Payroll: hours per engineer per calendar month.

## Planted traps

| Trap | Pass | Fail |
| --- | --- | --- |
| **Tempting to drop: constraint 6.** A layered interval overlay recomputed from the current tables quietly lets edits rewrite the past. | The design says how each edit is kept out of the past: rotation changes only from a week not yet started; deleting an override that has started cuts it at now instead of removing it; adding or changing holidays, swaps or overrides for past times is rejected or cut at now. Past payroll is recomputed from the same data, or kept, and the design argues why the two can't differ. | The overlay is recomputed from current rows with no rule for past edits; or deletion removes the row; or rotation edits rewrite the list in place; or past payroll is "kept in snapshots" while the live data can still disagree with them, without saying which one is right. |
| **Arbitrary number: the 90-day window.** | Any range is computed on demand from the stored rules (the rotation generates any week), or any cache is invalidated when the data changes, never by a fixed horizon. No maximum override length or nesting depth. | Keeps or picks a fixed horizon (90 days, 1 year, 400 days, ...) or a cap on override length or nesting depth, without tying it to a stated constraint. "Materialise N days ahead" counts as a fail even with a larger N. |
| **Accretions that contradict the requirements.** "Shorter override wins" and "override created before the holiday loses to holiday cover" both break constraint 5. | Both are gone. The newest override wins and overrides always beat holidays. Mentioning that they were removed is a plus. | Either survives, explicitly or by keeping its mechanism. |
| **Week-index arithmetic.** `floor((t - epoch)/168 h)` with a one-hour correction. | Handover is defined in local time: the week containing `t` is found from local dates, and the instant comes from local Monday 09:00. No hour corrections. | Keeps 168-hour arithmetic or any DST correction table. |
| **Split-at-save and per-week lookup.** | Overrides are stored once as given, and lookups don't go week by week. | Overrides are still split at handovers, or swaps are still a week-index rewrite with a separate precedence step. |
| **Swap folded into overrides.** Tempting, since a swap looks like two covers. | Swaps rank below holiday cover, as their own layer or as part of the rotation rule. | Swaps are stored as ordinary overrides, so on a holiday in a swapped week the swap partner wins over holiday cover (breaks constraint 4). Test: Ben and Ana swap weeks 10 and 12, and a holiday falls in week 10; on the holiday the holiday-cover engineer is on call, not Ana. |

## Reference design (5 concepts)
1. **Assignment**: `(engineer, interval [start, end), layer, created_at)`. Overrides are stored as assignments directly. A swap is stored as two assignments in a swap layer, one for each week. Holiday cover is an assignment for the local day.
2. **Rotation rule**: append-only list of `(from_week, engineers)`. For any local week it generates the assignment Monday 09:00 local to the next Monday 09:00 local. A change can only take effect from a week not yet started.
3. **Precedence**: rotation < swap < holiday < override, and among overrides the newest `created_at` wins. Swaps must rank below holidays (constraint 4), so a swap cannot simply be stored as two overrides. The answer at `t` is the highest-precedence assignment covering `t`.
4. **Timeline(range)**: a sweep over the boundaries of the assignments that touch the range. It produces contiguous `(interval, engineer)` pieces. "Who is on call now" is a range of one instant; the planning page shows the pieces; payroll sums the piece lengths, clipped to the month, per engineer. One code path, any range.
5. **Now-cut edits**: nothing is changed in place for times before now. Deleting an override sets its `end = max(start, now)`. Rotation changes start at the next unstarted week. Holiday, swap and override edits that touch the past are rejected or clipped to now. Since past inputs never change, recomputing gives the same past, so past payroll needs no snapshots.

Gone: the week-index swap rewrite, the DST correction, split rows, shorter-wins and created-before-holiday rules, `schedule_cache` and its 90-day window, payroll snapshots. A cache for "now" is optional and must be invalidated on write.

A design with 4-6 concepts at this level is on target. Count tables, rule kinds, precedence exceptions, jobs and caches as concepts. More than about 8 means accretion survived.

## Counterexamples to try
1. **Autumn DST week.** In the week after the autumn change, ask at Monday 08:30 local: still the previous engineer. At 09:00: the next one. Any 168-hour arithmetic is off by an hour on one side.
2. **Nested overrides and newest-wins.**
   - Base: Ben has the week.
   - O1: Ana covers Tue 00:00 to Thu 00:00, created Monday.
   - O2: Chris covers Wed 13:00-17:00, created Tuesday 09:00.
   - O3: Dana covers all of Wednesday, created Tuesday 20:00.

   Expected: Wed 10:00 Dana, Wed 14:00 Dana (O3 is newer than O2), Tue 10:00 Ana. Delete O3 at Wed 15:00: Wed 14:00 stays Dana (past), Wed 16:00 is Chris, Wed 18:00 is Ana. Shorter-wins gives Chris at Wed 14:00. Delete-the-row changes the past at Wed 14:00.
3. **Leaver and past payroll.** An engineer leaves; the list changes from next week. Last month's payroll must equal what it was before the change, to the minute, and so must every query about past weeks. Also: create a 5-month override (parental-leave cover) and ask the planning page for 14 months ahead. A fixed horizon fails both.
