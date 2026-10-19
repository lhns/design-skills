# Loyalty points on returns

An independent bookshop runs a loyalty scheme at its tills and on its web shop. Points are credited when an order is paid and can be spent like money later (100 points = 1.00 off). We are rewriting the points module. Below is what we collected before starting; candidate implementations of the core follow.

**From the scheme's terms (printed on the back of the card):**

> You earn 1 point for every whole euro you spend in one purchase, and 2 points per whole euro on Double Points Days. Points are added to your card as soon as you pay. If you return items, we take back the points you earned on them, so that your balance ends up as if you had not bought them. Points cannot be exchanged for cash.

**From the shop manager, answering our questions:**

> Double Points Days are the first Saturday of every month. The rate that counts is the one on the day you bought, obviously, not the day you bring it back.
>
> Returns are almost always one or two books out of a bigger order. People buy three, read the first chapter of one, and bring it back. We refund the exact price of the returned books, so an order can get several refunds over a few weeks. Gift cards and vouchers are handled elsewhere and never reach this module.
>
> Balances can go below zero if someone spends their points and then returns the book. That's fine, it just sits there until the next purchase.

**From the developer who kept the old system running:**

> All amounts are Decimal with two places. The till already stops a refund larger than what is left on the order, but check it here too. Orders are never edited after payment; corrections are refunds.

The module needs `purchase(order)`, which credits points, and `refund(order, amount)`, which records a refund on that order and takes the points back.

Two candidate implementations follow. Which one is the better design?
