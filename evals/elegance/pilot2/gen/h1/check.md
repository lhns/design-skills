# h1 check (judge only)

## Constraint checklist
The task states none of these as a list; they are in the rules, the treasurer's email, the tickets and the scale note. Each must hold in `answer.md`. A dropped constraint fails the run, however elegant the rest.

1. **Share-days (4.2).** Each member's weight for a month is the sum over the month's days of the shares they held that day. A mid-month transfer, purchase or redemption splits the month between holders. Members who have left still count for the days they held shares.
2. **Cap and full redistribution (4.3).** No member is credited more than their import that month. Credit above a cap goes to the members still under their caps, in proportion to their share-days, **repeatedly**, until no one is over their cap or everyone is capped. What nobody can use is recorded as sold.
3. **Whole kWh that add up (4.4).** Credits are whole kWh; credited plus sold equals the metered generation exactly; rounding never pushes a member above their cap; no residue goes to a non-member account.
4. **Statements are final and re-runs reproduce them.** Re-running any issued month gives exactly the issued statement and supplier file, whatever has changed since: transfers, redemptions, corrected readings.
5. **Corrections become adjustments.** A corrected import for an issued month leads to a recomputation of that month with the corrected input, and each member's difference from the issued figures goes on their next statement, positive or negative. The issued month stays as issued.
6. **Supplier file.** No zero-kWh lines (ticket #22). Every member with a non-zero credit is included, however few shares they hold.

## Planted traps

| Trap | Pass | Fail |
| --- | --- | --- |
| **The obvious design: pro rata, cap, hand the excess round once.** One redistribution pass is the natural reading of 4.3 and is wrong whenever the pass pushes another member over their cap. | Redistribution repeats until stable (water-filling: repeatedly cap anyone over, share the excess among the uncapped by share-days), or an equivalent closed form; anything left is sold. | A single pass; or excess goes straight to "sold" or to the community fund while uncapped members could still use it; or members are truncated at their cap after one pass with the overflow dropped. Test 1 below. |
| **Re-running from current data.** Recomputing an issued month from the register as it stands now, or from the latest import readings, is the elegant "single source of truth" and breaks finality (the auditor's failure and #29). An append-only transfer log fixes transfers but not corrections. | The inputs a statement used are kept unchanged (frozen per issued month, or versioned so a re-run selects the version used at issue), and so are the outputs. Share changes are dated rows, never overwrites; members who leave are not deleted. | The register is still overwritten or rows are deleted; or imports are overwritten by corrections; or "re-run" recomputes from the latest data; or statements are stored as files while the system can still produce different figures for the same month without saying which is authoritative. |
| **Corrections applied in place.** | A correction triggers a recomputation of that month with the corrected reading; the difference per member (which can be non-zero for members whose own reading did not change, because of redistribution) becomes an adjustment line on the next statement. | The issued month is reissued or its stored figures changed; or only the corrected member gets an adjustment, so the other members' redistribution effects are ignored (accept this only if the design argues it explicitly; it contradicts "what the member should have had"). |
| **Arbitrary limit: the 5-share minimum.** Its real cause is that the supplier rejects zero-kWh lines. | The minimum is gone; zero-kWh lines are left out of the supplier file (a condition on the line, not on the member). | Any minimum share count or minimum credit kept or introduced (5 shares, 10 kWh, ...). |
| **Accretion that contradicts 4.2: the 15th-of-the-month rule.** | Gone; share-days instead. Mentioning why is a plus. | Kept, or replaced by another whole-month approximation (month-end or month-start holdings, majority of the month). |
| **Rounding residue to the community account.** | Gone. Largest remainder (or an equivalent method) among members below their cap, so credited + sold = generation and caps hold. Any tie-break rule is fine if stated. | Residue to any non-member account; or each credit rounded to nearest with the sum left to drift; or rounding that can exceed a cap. |
| **Back-dated register changes.** (Plus, not a fail on its own.) | A transfer entered after its month was issued is either refused for the issued month or handled like a correction, through an adjustment. | |

## Reference design (6 concepts)
1. **Holdings**: dated rows `(member, shares delta, effective date)`, append-only. Share-days for any month come from them. Nothing is deleted.
2. **Month inputs**: generation and each member's import as received, with corrections stored as new versions (received date), never overwritten.
3. **Allocate(weights, caps, generation)**: water-filling: give everyone `generation * w / W`; while anyone is over their cap, fix them at the cap and share the excess among the rest by weight; stop when no one is over or everyone is capped; the rest is sold. Then floor every uncapped credit and hand the leftover kWh one by one by largest remainder (ties by member number). Imports are whole kWh, so capped credits are already whole.
4. **Issued month**: the input versions used and the resulting credits and sold kWh, stored when the statement goes out. A re-run of an issued month reads this record, or recomputes from the same input versions; both give the same figures.
5. **Adjustment**: when a correction for an issued month arrives, Allocate runs on the corrected inputs; each member's difference from the issued credits becomes a line on their next statement.
6. **Supplier file**: one line per member with a non-zero credit or adjustment.

Gone: the overwritten register, the run-time register read, the 15th-of-the-month rule, the 5-share minimum, the community-account residue, the CSV register copies, reprinting by re-running from current data.

A design with 5-7 concepts at this level is on target. Count tables, rules, jobs and special accounts as concepts. More than about 9 means accretion survived.

## Counterexamples to try

1. **Water-filling.** Generation 1,000 kWh. A has 50 shares, B 30, C 20, all for the whole month. Imports: A 300, B 400, C 1,000.
   - Pro rata: A 500, B 300, C 200. A is capped at 300; 200 kWh to share between B and C, 30:20.
   - One pass gives B 420 and C 280: B is over its cap of 400. Truncating B to 400 and selling the 20 kWh is also wrong, since C can use it.
   - Expected: A 300, B 400, C 300, sold 0.
   - Variant: C's import is 250. Expected: A 300, B 400, C 250, sold 50.
2. **Share-days.** May has 31 days. Hal holds 10 shares and transfers all of them to his daughter effective 14 May; nobody else's holding changes, and the month's total is 2,500 shares for every day. Weights: Hal 13 days x 10 = 130 share-days, daughter 18 x 10 = 180, out of 2,500 x 31 = 77,500. With 9,300 kWh and nobody capped: Hal 15.6, daughter 21.6 before rounding. The 15th rule gives the daughter all 37; month-end holdings do too.
3. **Rounding.** Generation 1,000 kWh, three members with equal share-days, nobody capped: 333.33 each. Expected: 333, 333, 334 (or any tie-break rule stated), total 1,000, nothing to a community account.
4. **Correction after issue.** May issued with test 1's figures (A 300, B 400, C 300). On 20 July the supplier corrects B's May import from 400 to 450.
   - Re-running May must still give A 300, B 400, C 300.
   - Recomputed May with the correction: A 300, B 420, C 280. Adjustments on the next statement: B +20, C -20 (C's own reading never changed). A design that adjusts only B over-credits the month by 20 kWh against the meter.
5. **Small holder and zero lines.** A member with 2 shares in December (2,500 kWh, 2,500 shares, nobody capped) gets 2 kWh: they must be in the file. A member who joins on 31 December with 1 share gets about 1/77,500 of 2,500 kWh, about 0.03 kWh, so 0 or 1 depending on remainders; if 0, their line is left out of the file and the kWh go to someone else, so the total still matches.
6. **Leaver.** A member redeems all shares on 10 June. A re-run of May and the June statement both include them (May fully, June for 9 days of holding if redemption is effective on the 10th); a register that deletes them fails both.
