# Prepaid desk-hour credits

A coworking space sells prepaid desk-hour packs. Front-desk staff can also grant free hours as goodwill. Booking a desk spends hours; cancelling a booking refunds them. We need the core ledger: `grant`, `spend`, `refund` and `balance`. Persistence and the HTTP layer are out of scope.

Constraints:

1. Every grant expires 90 days after it was made, paid packs and goodwill alike.
2. A spend uses the hours that expire soonest first.
3. A spend larger than the unexpired balance fails and changes nothing. Spends must be positive.
4. Cancelling a booking refunds its spend: each hour goes back to the grant it was taken from and keeps that grant's expiry. Hours whose grant has expired by the time of the refund are not returned.
5. The balance at time `t` counts only hours in grants unexpired at `t`.
6. Amounts are whole hours. Times are timezone-aware datetimes, and the caller passes them in.

Two candidate implementations follow. Which one is the better design?
