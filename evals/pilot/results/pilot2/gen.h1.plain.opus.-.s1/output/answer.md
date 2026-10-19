# Solar-credit allocation: design

My own design choices are marked **(choice)**.

## Stored data
Append-only: nothing is overwritten or deleted.

- **Member**: id, supplier account number.
- **Share ledger**: (member, effective date, ±shares, recorded at). A member's holding on a day is the sum of their entries effective by that day.
- **Readings**: (month, meter, kWh, received at), for the array and each member account. A supplier correction is a new row; the latest row is current.
- **Settlements**: one per run, holding each member's credit and the kWh sold for every month the run settles, plus the statements and file as sent.

Every calculation depends only on the month and the inputs "as known at T" (rows recorded by T).

## Working out a month
1. **Weight** = share-days in the month (4.2). **Cap** = the member's import. A reading still missing at run time counts as 0 **(choice)**; when it arrives it is handled as a correction.
2. **Fill (4.3):** share generation G among uncapped members by weight. Anyone over their cap is fixed at it and dropped; the rest is shared again. Repeat until nobody exceeds their cap or everyone is capped.
3. **Whole kWh (choice: largest remainder):** round all shares down, then give the leftover kWh one each to the largest fractions, ties broken by member id. A capped share is already whole, and an uncapped share is below an integer cap, so no cap is broken.
4. **Sold** = G − Σcredits = max(0, G − Σcaps). Credits plus sold kWh equal G exactly (4.4). The community account is gone.

## Monthly run (by the 8th)
At time T:
- Settle the month just ended, using inputs as known at T.
- Re-settle every earlier month whose inputs changed since its last settlement (corrections, backdated entries). Adjustment = new credit − total already credited for that month, per member and for kWh sold.
- Store the new settlement. Earlier settlements are never changed.

## Supplier file
- A credit line for each member with a non-zero credit.
- An adjustment line for each member and corrected month, tagged with that month (positive or negative, never zero).
- An export-sale line for the kWh sold **(choice)**.

No line is ever zero, so the 5-share minimum goes; a member whose credit rounds to 0 just has no line.

## Statements
Printed from the stored settlement, never from a new run. Each shows share-days, import, generation, credit, whether the cap applied, and any adjustments with their month and reason. Statements are final; reprints match the original (#29).

## Audit
The method is deterministic, so re-running a month with inputs as known at the original T reproduces what was sent. Current inputs give the original plus the adjustments since. No CSV folder is needed.

## Share register changes
Every change is a ledger entry. Its effective date is the first day the new holder holds the shares **(choice)**.

- **Purchase or new member:** + entry; shares count from that day.
- **Transfer:** − for the seller, + for the buyer, same date. In #14, Hal gets 13 days of May for the 10 shares and his daughter 18; no 15th-of-the-month rule.
- **Redemption, partial or full:** − entry. The member stays on record.
- **Late or backdated entry** dated in a settled month: the next run re-settles that month and sends adjustments.
- **Mistake:** fixed with a reversing entry, never an edit.

## Removed
Overwriting, the 5-share minimum, the 15th-of-the-month rule, round-to-nearest, the community account, CSV copies, and statements made by re-running.
