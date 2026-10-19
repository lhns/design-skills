# Candidate A

```python
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Pallet:
    location: str | None = None        # None: not in the building
    moved_at: datetime | None = None   # time of the move that set `location`
    shipped: bool = False


pallets = defaultdict(Pallet)


def apply(scan):
    """Update a pallet's location from one scan. Scans may arrive late."""
    p = pallets[scan.pallet]
    if scan.kind == "received":
        # The dock PC uploads at the end of the shift, often after the first
        # move (#47); a receive only places a pallet that has no location yet.
        # It also brings back a refused pallet.
        p.shipped = False
        if p.location is None:
            p.location = "DOCK"
    elif scan.kind == "moved":
        # Moves uploaded after the pallet shipped (#41), or older than the move
        # already applied (#49), are ignored.
        if p.shipped or (p.moved_at is not None and scan.at < p.moved_at):
            return
        p.location = scan.location
        p.moved_at = scan.at
    elif scan.kind == "shipped":
        p.shipped = True
        p.location = None


def location_of(pallet):
    return pallets[pallet].location
```
