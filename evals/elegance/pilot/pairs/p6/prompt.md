# Parking garage pricing by time band

A municipal parking garage charges per minute, at a rate that depends on the time of day.

Constraints:

1. Day band 06:00-22:00 costs 5 cents per minute. Night band 22:00-06:00 costs 2 cents per minute.
2. Each minute of a stay is charged at the rate of the band it falls in.
3. Stays may last up to 7 days and cross midnight any number of times.
4. Entry and exit are naive local datetimes in whole minutes (the gate drops seconds). The garage ignores daylight saving changes.
5. If exit is not after entry, the price is 0.
6. The council revises the bands about once a year (a band may be split or moved). The function returns the price in cents.

Two candidate implementations follow. Which one is the better design?
