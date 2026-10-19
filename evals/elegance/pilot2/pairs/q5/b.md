# Candidate B

```python
from bisect import insort
from collections import defaultdict

scans = defaultdict(list)  # pallet -> its scans, in the order they were taken


def apply(scan):
    """Record one scan, whenever it arrives."""
    insort(scans[scan.pallet], scan, key=lambda s: s.at)


def location_of(pallet):
    """Where the pallet is: what its most recently taken scan says (None: not in the building)."""
    if not scans[pallet]:
        return None
    latest = scans[pallet][-1]
    if latest.kind == "shipped":
        return None
    return "DOCK" if latest.kind == "received" else latest.location
```
