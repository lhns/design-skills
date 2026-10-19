I've written the design to `answer.md`. It comes to 598 words, just under the 600 limit.

**The core idea:** each stored fact applies only from the moment it was recorded until the moment it is withdrawn. Nothing is ever updated or deleted. So a later edit can't change who was on call at a past moment, and payroll for a past month always comes out the same. That one rule removes the 90-day schedule cache, the nightly rebuild job and the archived payroll snapshots.

**What's stored:**
- **Engineers:** never deleted.
- **Rotation list changes:** each one records the ordered list and the week it starts from.
- **Assignments:** one table for swapped weeks, holiday cover and overrides. Each row has a layer, and the order is swapped week < holiday < override. Swaps have to lose to holiday cover, so they can't be stored as overrides.

**Who is on call at a given time:** if any assignments apply, the highest layer wins, and within a layer the most recently created one wins. Otherwise the rotation list answers. Weeks are counted on the local calendar, so weeks with a clock change just run 167 or 169 hours.

**The new requirement:** while Chris covers Wednesday 13:00–17:00 inside Ana's Tuesday–Thursday cover for Ben, Chris is on call and is shown as replacing Ana. After 17:00 it is Ana again, shown as replacing Ben.

**Planning page and payroll:** the roster for any date range is worked out on request, not read from a cache. It splits the range at every handover and at every point where an assignment starts or stops applying, and works for any range. Payroll is the same calculation for a calendar month, adding up the hours per engineer.

**What the old system loses:**
- the 168-hour week count and its daylight-saving correction;
- the swapped-week index mapping;
- splitting overrides at the Monday handover;
- the rule that the shorter override wins;
- the old exception where an earlier override loses to holiday cover;
- the 90-day limit on the planning page;
- physically deleting rows.

**My own design choices,** all labelled in the file:
- "Whom it replaces" is worked out when shown, not stored, so it can't contradict the data.
- Allowance is paid for actual elapsed hours, so a clock-change night counts as 23 or 25 hours.
- When someone leaves, their future swapped weeks are withdrawn and those weeks fall back to the list.
- Rotation position is counted from the start of each new list.
- There is no cache, because paging needs only a few indexed lookups.