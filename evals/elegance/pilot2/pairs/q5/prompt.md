# Pallet locations in a cold store

A cold-storage warehouse keeps chilled and frozen pallets for food wholesalers. Every pallet has a barcode. Handheld scanners record three kinds of scan: `received` at the dock, `moved` when a pallet is put into a location (a freezer or chiller bay, such as `F2-14`), and `shipped` when it is loaded onto a lorry. The stock screen shows where each pallet is now. The location module is being rewritten; two candidates are below.

**From the operations manager:**

> The handhelds queue scans when they lose Wi-Fi and upload them when they're back in range. Inside the freezers there is no signal at all, so a driver's scans from a long freezer run turn up in one batch, sometimes an hour later. The loading-bay handhelds are almost as bad, the bay doors block the signal. Each scan carries the time it was taken; the handheld clocks are synced to the server every time they connect.
>
> Customers sometimes refuse a pallet at delivery. The lorry brings it back the same day and we receive it again at the dock like any other pallet, same barcode, and put it away.

**Recent tickets on the old system:**

> **#41** Pallet showed as in F2 after it had been shipped. A late move from a freezer handheld came in after the shipped scan. Fixed: moves are ignored once a pallet has shipped.
>
> **#47** Pallets jumping back to DOCK in the afternoon. The dock PC uploads its receive scans in one go at the end of the shift, after the pallets' first moves. Fixed: a receive doesn't override a known location.
>
> **#49** Two moves of the same pallet arrived in the wrong order (two drivers, both in freezers). Fixed: a move older than the last applied move is ignored.

Volumes are small (a few thousand scans a day). Scans are never edited or deleted.

Two candidate implementations follow. Which one is the better design?
