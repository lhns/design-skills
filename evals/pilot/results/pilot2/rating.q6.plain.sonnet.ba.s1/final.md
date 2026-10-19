**Design 2 (Candidate A) is the better design.** The deciding factor is the gateway's hard limit, and Candidate B breaks it by construction.

**Candidate B (token bucket, burst 10)**
- Section 4.2 allows at most one message in any one-second interval. A bucket that starts full with `BURST = 10` submits 10 messages back to back at startup, and again after any idle period.
- The first flood warning therefore produces about 9 rejections with status 429 in its first second. Each later burst after an idle gap adds more, and so do retries of failed submits.
- Under 4.3, more than 20 rejections in a day suspends the sender ID for 24 hours, and only the operator's support desk can lift it. Two flood alerts in a day, or one alert plus a few retries, could trigger that.
- A suspension would block flood warnings, which are the service's most important traffic, so it is the worst possible failure.
- Bursting also doesn't help the owner. Sending 10 messages at once saves about 10 seconds on a run of 30 minutes or more.
- Token buckets are the right tool when the provider allows bursts. Here the provider explicitly forbids them.

**Candidate A (minimum interval of 1.05 s)**
- It enforces a strict spacing between consecutive submits, which is exactly what 4.2 requires. The 5% margin absorbs network jitter and differences between the worker's clock and the gateway's, so submits never land in the same one-second window.
- It never bursts, including after idle periods, and it handles retries correctly because they go through `pace()` like any other message.
- It is simple and has no state beyond the last submit time.
- The cost is speed. 1,500 messages take about 26 minutes and 2,000 take about 35 minutes. That is slightly over the owner's "half an hour", but they said it is acceptable and it matches what the service has done for years. Everyone is reached and nobody is skipped, which is what the owner says matters most.
- The margin could be tightened to something like 1.02 s if the 35-minute worst case matters. That is a minor tuning choice and doesn't change which design is better.

One small point for Candidate A: `self.last` is set after the sleep, from a fresh `clock()` call. This is fine because it records the actual submit time and can only increase the spacing.

Candidate A trades a few minutes of speed for never risking a 24-hour suspension. Candidate B risks that suspension for no real gain.

WINNER: 2