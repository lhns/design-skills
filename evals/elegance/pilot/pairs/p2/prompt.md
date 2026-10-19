# Warehouse site facts for order dispatch

An online garden-supplies shop ships from three warehouse sites, each identified by a site code. The dispatch module answers four questions for the rest of the system: is a site code valid, what label goes on the packing slip, which carrier collects from the site, and on which date an order placed at a given local time will ship.

Constraints:

1. Sites: N1 "North / Lakeside" and S2 "South / Harbour" are collected by Courier Alpha; W3 "West / Ridge" by Courier Beta.
2. Same-day cutoff (local time): 14:00 at S2, 16:00 at N1 and W3. Orders placed at or after the cutoff ship on the next shipping day.
3. No site ships on Sunday. Only W3 ships on Saturday.
4. Every function except `is_valid_site` rejects an unknown site code with `ValueError`.
5. A fourth site opens next spring. Site details (cutoff, carrier, Saturday shipping) have changed about once a year, and each change has been made by whoever was on call.

Two candidate implementations follow. Which one is the better design?
