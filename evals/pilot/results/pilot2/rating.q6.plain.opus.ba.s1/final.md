# Design 2 (Candidate A, the fixed-interval pacer) is better

## The gateway contract rules out bursts

Section 4.2 is a hard per-interval limit, not a long-run average. The gateway accepts at most one message from the sender ID in any one-second interval. Section 4.3 makes going over very costly: more than 20 rejections in a day suspends the sender ID for 24 hours, and only the operator's support desk can lift it. For this service, a suspension means that during a flood nobody gets warned. The service owner's real requirement is "all of them go out and nobody is skipped," and a suspension is the one outcome that fails it outright.

## Design 1 (token bucket) breaks the contract by design

- **It bursts when a flood warning starts.** The bucket begins full (`tokens = BURST = 10`) and refills to 10 after any 10 seconds of idle time. Quiet periods are normal ("a few hundred messages, spread out"), so when the river team presses the button, the first 10 messages go out back to back. The gateway accepts one and rejects about 9 with 429.
- **Suspension follows quickly.** Three bursts in a day (around 27 rejections) exceed the limit of 20. That could be one flood alert plus two bin-day batches, or ordinary traffic after idle gaps. Retried messages also return through `pace()` and can land in a refilled bucket, which adds more rejections.
- **Shrinking the burst is not enough.** Even with `BURST = 1`, the token bucket spaces submits at exactly 1.000 s with no margin. Scheduler jitter, sleep overshoot followed by catch-up, or network latency variation between the worker and the gateway can then put two arrivals inside one gateway second.
- **The burst brings little benefit.** Only the first ~10 messages would arrive faster, and the gateway rejects most of them anyway. Total delivery time for 2,000 messages is the same, because 1 msg/s is the floor either way.

## Design 2 matches what the contract and the owner ask for

- **Guaranteed spacing.** Two submits are never closer than 1.05 s, whatever the history or idle time. There is no stored credit to spend, so there is never a burst.
- **Safety margin.** The 0.05 s margin absorbs timing jitter. `last` is recorded after the sleep, from the monotonic clock, so any oversleep only makes the gap longer, never shorter.
- **Fits the deadline.** 1,500 messages take about 26 minutes. 2,000 take about 35 minutes, compared with a theoretical minimum of 33 minutes at the contract's rate. So 2,000 messages slightly exceed the half hour under either design. That is a limit of the gateway contract, not of the code, and the owner should be told. Options to discuss are a second registered sender ID, if the operator allows it, or ordering the queue so the highest-risk addresses go first.
- **Retries are handled safely.** A failed submit still sets `last`. That is conservative and correct, because a "network error" may happen after the gateway has already received and counted the message.
- **Simpler.** There is less state, and it is easy to test with the injected `clock` and `sleep`.

## Minor suggestions for Design 2

- Log every 429 response and alert on the first one, so the team is warned long before reaching 20.
- Optionally stop sending after a few 429s in a day rather than risk suspension.
- Make sure that if the process restarts, the new process does not submit within 1 s of the old one's last send. For example, wait `MIN_INTERVAL` at startup.

WINNER: 2