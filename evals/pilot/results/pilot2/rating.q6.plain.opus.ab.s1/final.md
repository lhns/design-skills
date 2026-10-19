**Design 1 (Candidate A) is better.** Candidate B breaks the gateway agreement on the very first flood warning.

**The constraint**

Section 4.2 is a hard rule: at most one message in any one-second interval. It is not a long-run average. Section 4.3 makes breaking it costly: more than 20 rejections in a day suspends the sender ID for 24 hours, and only the operator's support desk can lift it. A suspension during a flood means *nobody* gets the warning. That is the outcome the service owner cares most about.

**Candidate B (token bucket, BURST = 10)**

- The bucket starts full and refills to 10 whenever the worker is idle. Most days are spread-out traffic, so it is almost always full when the river team presses the button.
- The first 10 messages therefore go out back-to-back. The gateway accepts one and rejects about 9 with 429. A second burst that day, or a burst after any idle gap of 10 seconds or more, adds about 9 more. A third crosses 20, and the sender ID is suspended for a day.
- The rejected messages are a problem in their own right. The developer only says *network* failures are re-queued. A 429 is a successful exchange with a rejection status, so those residents may simply be skipped. That violates "nobody is skipped".
- Even with BURST = 1, `RATE = 1.0` with no margin leaves no allowance for jitter between the worker's clock and the gateway's.
- The burst buys nothing. The gateway won't deliver faster than 1/s, so a bucket designed for "average rate with bursts" doesn't fit a per-interval cap.

**Candidate A (minimum interval of 1.05 s)**

- It enforces spacing between every pair of consecutive submits, which is exactly what 4.2 requires. The 0.05 s margin absorbs network and clock jitter.
- `last` is stamped right before the submit. Any time spent in the submit call only adds to the spacing, so errors fall on the safe side.
- After an idle period it sends immediately, so the first warning goes out with no delay.
- Re-queued network failures pass through `pace()` like any other message, so retries can't break the spacing.
- Throughput: 1,500 messages take about 26 minutes; 2,000 take about 35 minutes. The upper end slightly exceeds the "half an hour" figure. No compliant design can do better, though: even at exactly 1.0/s, 2,000 messages take 33 minutes. The limit is the gateway's, not the pacer's. If 30 minutes becomes a hard requirement, the fix is commercial (a higher rate tier or a second sender ID, per 4.1/4.2), not a burst allowance.

**Optional small improvements to A**

- Treat a 429 as a pacing signal: re-queue the message and back off, rather than dropping it.
- Count rejections per day and alert well before 20.

WINNER: 1