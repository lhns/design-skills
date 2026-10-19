# Nested staff groups and permissions

A city's parks department runs a small internal system for staff permissions: who can book the minibus, use the tool store, see timesheets, and so on. People belong to groups, groups can contain other groups, and each permission is granted to some groups. The membership code is being rewritten; two candidates are below.

**From the system's ticket history:**

> **#118** Permissions page hung after a change to the Facilities groups. Someone had put Admin inside Facilities and Facilities inside Admin. Fixed in the membership lookup; the loop itself was removed by hand.
>
> **#131** Request: show on the permissions page why someone has a permission (which group). Parked.

**From the IT officer who maintains it:**

> Permissions are mostly granted high up so they cover whole teams: Timesheets is granted to the Parks group, the tool store to Grounds, the minibus to each crew. People are added to the lowest group that fits. The seasonal staff each crew takes on from April sit in a "Seasonal" group inside that crew.
>
> The org chart only changes a few times a year and I make the group changes myself. There are about 60 groups and 400 people; nothing is slow.

**From an HR email forwarded to IT last week:**

> Following consultation, from 1 November Grounds will be organised as two area teams, North and South. Crews 1-4 move to North and crews 5-8 to South, with their seasonal staff. Please set up the systems to match.

`group.name` is its name; `group.people` is a set of people; `group.subgroups` is a list of groups; `permission.groups` is the list of groups it is granted to.

Two candidate implementations follow. Which one is the better design?
