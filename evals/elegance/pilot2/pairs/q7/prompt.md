# Festival ticket prices

A volunteer-run folk festival sells weekend tickets online. The pricing function turns an order into the amount charged. It is being rewritten after last year's version became hard to follow; two candidates are below.

**The price list for next year, as printed on the flyer:**

> Weekend ticket 64.00. Early bird: book by 28 February and save 15%. Groups of six or more save 10%. Festival members save 20% (member and group savings don't combine; you get the better one). Early-bird savings combine with either. Total savings are capped at 30%. A booking fee of 2.00 per order applies to every order.

**From the ticketing coordinator, Bea:**

> Every autumn the committee sets next year's prices and discounts, then I sit down with Kofi (our one developer) and we go through the pricing code line by line against the flyer before tickets go on sale. Last year that took an afternoon because nobody could tell what ran in which order. I can read a bit of Python if it's plain.
>
> The committee talks every year about adding a residents' discount for the two villages next to the site. It hasn't happened yet, and if it does it'll have its own rules about what it combines with, like the others.

**From Kofi:**

> One order, one call, a few thousand orders a year. Amounts are Decimal; the ticket total is rounded to the cent, half-up, after discounts. `order` has `tickets` (int), `member` (bool) and `placed_on` (date).

Two candidate implementations follow. Which one is the better design?
