# Botanic garden opening hours

A small botanic garden run by a trust shows its opening hours on its website and on the ticket machine at the gate: today's opening time, last entry and closing time. The function behind both is being rewritten. Two candidates are below.

**From the trust's visitor policy (adopted 2011, section 2):**

> The garden opens at 10:00 every day of the year. It closes one hour before sunset, rounded down to the half hour, and no later than 19:00 so that staff shifts end by 19:30. Closing times change on the first of each month. Last entry is one hour before closing.

**From the visitor services manager, Ruth:**

> The trustees set the times from that policy back in 2019 and they've stayed the same ever since. They're on the leaflet, on the season-ticket cards, and painted on the boards at both gates, so whatever the website says has to match those. The one time the old website showed a different closing time from the gate boards, we had a queue of unhappy season-ticket holders at the gate.
>
> For reference, the closing times are: January 15:00, February 15:30, March 16:30, April 18:30, May to July 19:00, August 18:30, September 18:00, October 17:00, November and December 15:00.

**From the volunteer developer:**

> `hours_on(day)` returns `(opens, last_entry, closes)` as `datetime.time`. I checked both candidates against Ruth's list for every day of 2026 and 2027 and they match. The garden is at about 52 degrees north; clocks go forward on the last Sunday of March and back on the last Sunday of October.

Two candidate implementations follow. Which one is the better design?
