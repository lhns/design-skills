# Candidate A

```python
import time

MIN_INTERVAL = 1.05  # seconds between submits: the gateway's 1 per second, plus clock margin


class Pacer:
    def __init__(self, clock=time.monotonic, sleep=time.sleep):
        self.clock = clock
        self.sleep = sleep
        self.last = None  # time of the previous submit

    def pace(self):
        """Block until the next message may be submitted."""
        if self.last is not None:
            wait = self.last + MIN_INTERVAL - self.clock()
            if wait > 0:
                self.sleep(wait)
        self.last = self.clock()
```
