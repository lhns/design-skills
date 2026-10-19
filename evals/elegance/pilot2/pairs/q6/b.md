# Candidate B

```python
import time

RATE = 1.0      # tokens per second: the gateway's 1 per second
BURST = 10      # bucket capacity


class TokenBucket:
    """Standard token-bucket limiter: long-run rate RATE, short bursts up to BURST."""

    def __init__(self, clock=time.monotonic, sleep=time.sleep):
        self.clock = clock
        self.sleep = sleep
        self.tokens = float(BURST)
        self.updated = clock()

    def _refill(self):
        now = self.clock()
        self.tokens = min(BURST, self.tokens + (now - self.updated) * RATE)
        self.updated = now

    def pace(self):
        """Block until the next message may be submitted."""
        self._refill()
        if self.tokens < 1:
            self.sleep((1 - self.tokens) / RATE)
            self._refill()
        self.tokens -= 1
```
