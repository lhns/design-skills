I've written the design to `answer.md`. It comes to 593 words, under the 600 limit. It's a written design only; nothing has been built or tested.

- **Stored data:** nothing is overwritten any more. Share changes, meter readings and supplier corrections are all added as new dated rows. So any month can be worked out again exactly as it was known on the day it was first run. That answers the auditor's mismatches and the mortgage statement that couldn't be reproduced (#29).
- **Share-days:** each member's portion of the month is based on the shares they held on each day, as the AGM rules (4.2) say. This replaces the 15th-of-the-month rule. In Hal's case (#14), he gets 13 days of May for the 10 shares and his daughter gets 18.
- **The January cap:** generation is shared out in proportion to share-days. Anyone who would get more than they imported gets exactly their import, and what's left is shared again among the rest. This repeats until everyone is within their import. Only energy nobody can use is sold to the supplier.
- **Rounding:** I chose to round everyone down, then give the leftover kWh one each to whoever was closest to the next kWh. This never pushes anyone over their cap, and credits plus sold kWh always equal the metered generation. The "community account" is no longer needed.
- **Supplier file:** members with zero credit simply get no line. That stops the supplier rejecting the file without the 5-share minimum, which is dropped.
- **Statements and corrections:** statements are printed from what was stored when they were sent, never from a fresh run. When a supplier correction or a backdated share change comes in, the next monthly run works that month out again. The difference, up or down, goes on the next statement and supplier file, labelled with the month it corrects.

My own design choices are marked **(choice)** in the document. The main ones:
- **Missing import reading:** if a member's reading hasn't arrived by run time, it counts as 0, and the late reading is handled like a correction.
- **Rounding:** the round-down-then-share-leftovers method above, with ties broken by member id.
- **Sold energy:** it goes to the supplier as a separate export-sale line in the file.
- **Transfer dates:** the effective date of a share change is the first day the new holder holds the shares.