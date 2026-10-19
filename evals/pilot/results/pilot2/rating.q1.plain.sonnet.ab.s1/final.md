**Design 2 (Candidate B) is better.**

**The deciding requirement.** The card terms say a return must leave the balance "as if you had not bought them". Points are earned as `floor(paid) × rate` on the whole purchase, and the shop manager says one order can receive several partial refunds over a few weeks. So the total taken back across all refunds has to equal the points earned on the refunded portion. Flooring each refund separately does not give that.

**Candidate A.** It takes back `int(amount) × rate` for each refund separately. Because the floor of a sum is at least the sum of the floors, this under-deducts whenever refunds have cents:
- An order of 3.00 at rate 1 earns 3 points. Refunding 1.50 and then 1.50 takes back 1 + 1 = 2 points, so the customer keeps 1 point on a fully refunded order.
- An order of 1.00 refunded as 0.50 + 0.50 earns 1 point and takes back 0.
- The result also depends on how the refund is split, which is arbitrary from the customer's point of view.

Each refund can only leave the customer with too many points, never too few, so this loophole can be exploited. It also raises `KeyError` if the customer has no balance entry, though that is minor.

**Candidate B.** It computes the points on the part of the order still kept before and after the refund, and takes back the difference. These differences telescope:
- The total taken back is always `points(paid) − points(still kept)`.
- A full refund, however it is split or ordered, returns the balance exactly to its pre-purchase value.
- A partial refund leaves the customer with exactly the points for what they kept.

It also uses the rate stored on the order, which is the purchase-day rate, as the manager requires. It keeps the validation against over-refunding, and it handles negative balances and missing customers through `_add`. The `points_for` helper means the earning rule lives in one place, so `purchase` and `refund` cannot drift apart.

WINNER: 2