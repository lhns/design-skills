# Duplicate supplier invoices

A regional theatre pays about 200 suppliers. Paper and PDF invoices are scanned by the post room and entered into the accounts system, which holds any invoice that looks like a duplicate of one already entered until someone in finance checks it. Last year the theatre paid a scenery-hire invoice twice and only got the money back after months of chasing. The duplicate check is being rewritten; two candidates are below.

**From the finance manager, Ingrid:**

> Each invoice has the supplier, the supplier's invoice number, the date printed on the invoice, the amount, and the date it reached us. Numbers come in all shapes: "INV-0045", "inv-0045 ", sometimes a bare "45". Amounts on a copy can differ by a few cents when the supplier's system adds a late-payment note, so I wouldn't match on amount.
>
> A held invoice costs us a few minutes to clear. A missed duplicate costs us the payment.

**From the accounts assistant, Theo:**

> Watch out for the printers and the lighting-hire firm: they start their numbering again at 0001 every January. In the old system every January was a mess of false alarms against last year's invoices.
>
> The post room types in the printed invoice date when they can read it. On some faxed or photocopied invoices they can't, and the date is left empty.
>
> The post room scans everything that arrives, including statements. The scenery-hire firm and the printers send a statement every quarter, a couple of weeks after the quarter ends, with a copy of each invoice from that quarter stapled behind it. The post room can't always tell a copy from an original.

**From the developer:**

> `possible_duplicates(new, existing)` returns the existing invoices that `new` should be held against; an empty list means it goes into the next weekly payment run. Volumes are small enough to scan the supplier's invoices in memory.

Two candidate implementations follow. Which one is the better design?
