# Design 1 (Candidate A) is the better design

The decision rests on clause 4.2. The gateway does not enforce an *average* of one message per second. It enforces **at most one message in any one-second interval**. That is a minimum spacing rule, and Candidate A implements exactly that. Candidate B implements a different contract that breaks the rule by design.

## Why Candidate B is unsafe

The bucket starts full (`tokens = BURST = 10`) and refills to 10 after any quiet spell of 10 seconds or more. Most days are quiet, so the bucket is usually full when the river team presses the button. The first ten messages then go out back to back, with no sleep at all.

- The gateway accepts the first one and rejects about **nine with 429**.
- Clause 4.3 suspends the sender ID after more than 20 rejections in a calendar day. Three bursts in one day trigger suspension: two flood warnings, or one warning plus an ordinary road-closure batch after a pause. Even fewer are needed if the rejected messages are retried and bounce again.
- A suspension lasts **24 hours** and only the operator's support desk can lift it. This would happen during a flood, which is the worst possible time to lose the service. The owner's main requirement, "all of them go out and nobody is skipped", fails completely.

The burst also gains almost nothing. The long-run rate is still 1 per second, so 2,000 messages take about 33 minutes either way. B's comments describe a "standard token bucket" and "the gateway's 1 per second". That is the wrong mental model: a correct, textbook algorithm aimed at a contract the gateway doesn't have. A `BURST` of 1 would make it correct, but then it is just a more complicated version of A.

## Why Candidate A fits

- **It matches the contract directly.** Each submit is spaced at least `MIN_INTERVAL` after the previous one. The 0.05 s margin covers clock and network jitter, and the comment explains that margin.
- **It works from a cold start.** The first message after idle goes out immediately, which suits "the faster the first ones go out the better". It can never produce two submits inside one second.
- **Retries are safe.** A failed submit is re-paced like any other message, so there is no special case.
- **It is simple.** It has one state variable and one sleep, and the clock and sleep are injected so it is easy to test.

## Minor notes on A (not blocking)

- 2,000 × 1.05 s ≈ 35 minutes, slightly over the half hour the owner mentioned. 1,500 messages take about 26 minutes. B is no faster in the long run, and staying under the suspension threshold matters far more. Still, the owner should hear the real figure. The margin could be reduced, for example to 1.02, if testing against the gateway shows that is safe.
- `self.last = self.clock()` records the time when `pace()` returns, not when the gateway actually receives the message. In a single-threaded worker that submits immediately afterwards, this is fine.
- Better names would be `last_submit_at` instead of `last`, and something like `SubmitPacer`. These are cosmetic.

**Summary:** B's burst allowance is precisely what clause 4.2 forbids, and with clause 4.3 it can take the alert service offline for a day during an emergency. A is simpler and respects the gateway's limits.

WINNER: 1