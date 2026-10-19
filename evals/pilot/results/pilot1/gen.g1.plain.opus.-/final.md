I've written the design to `answer.md`. It's 592 words by `wc -w`, under the 600 limit.

**The idea:** who is on call at any moment is calculated from a few small tables, with no cache. One rule makes the past fixed: an edit may only change answers from the moment it is made onward. Nothing is ever hard-deleted, so the current data always reproduces past answers and past payroll. That makes the nightly cache and the archived payroll snapshots unnecessary.

**What's stored:**
- **Engineers:** never deleted, so people who have left still show up correctly in old payroll.
- **Rotation list:** one row per change, each starting from a week that hasn't begun.
- **Week assignments from swaps:** each swap writes two rows giving each week to the other person.
- **Holiday cover:** one row per date.
- **Overrides:** each has a creation sequence number and a `deleted_at` time instead of being removed.

**On call at time T:** the first match wins:
1. The latest-created override still in force at T.
2. Holiday cover for T's local date.
3. A swap assignment for T's week.
4. The rotation.

Weeks run from Monday 09:00 local time, converted with the timezone database, so DST weeks are simply 167 or 169 hours long and no hour correction is needed. The new requirement works without special handling: Chris's override is created after Ana's, so Chris wins for Wednesday afternoon and Ana covers the rest.

**Planning page and payroll:** the range is cut into segments wherever a handover, holiday midnight or override start/end falls. Each segment is looked up once and neighbours with the same person are merged. This works for any date range, years ahead included. Payroll uses the same segments for the local month and adds up real elapsed minutes per engineer.

**My design choices (labelled in the doc):**
- **Swaps:** stored as fixed week assignments rather than one week number replaced by another. A later change to the rotation list then can't quietly swap different people.
- **Leavers:** when someone leaves, their swapped weeks that haven't started go back to the normal rotation.
- **Holiday cover:** can only be added or changed for dates that haven't started; same-day changes use an override.
- **Overrides:** a start time in the past is moved up to now. Deleting one sets `deleted_at` to now, so the part already served still counts. Editing an override means deleting it and creating a new one.
- **Payroll:** a month that hasn't ended is marked provisional.

The doc ends with a list of what the current system drops, for example the "shortest override wins" rule and splitting overrides at Monday handovers.