# Pacing outgoing text alerts: Design 2 (Candidate A) is the better choice

The deciding constraint is gateway agreement 4.2 together with 4.3. Design 1 breaks it, and Design 2 respects it.

## Design 1 (token bucket) breaks the contract in its first second

- The bucket starts full (`tokens = BURST = 10`). The first ten `pace()` calls therefore return immediately.
- Clause 4.2 says the gateway accepts **at most one message per sender ID in any one-second interval**. That is a hard sliding window, not a long-run average. A token bucket only enforces the average. That is exactly the wrong model here.
- When the river team presses the button, roughly ten messages go out back to back. About nine of them get a 429 error.
- Those failures go back on the queue and through `pace()` again. Meanwhile the bucket refills whenever the queue is idle, so every lull followed by a burst costs up to nine more rejections.
- Two such episodes in a day exceed the 20-rejection limit in 4.3. The sender ID is then **suspended for 24 hours**, and only the support desk can lift it.
- That is the worst possible outcome for this service. A flood warning that reaches nobody is far worse than one that is slow. The owner's stated priority is "all of them go out and nobody is skipped". The burst buys a few seconds on the first ten messages and puts every message at risk.
- The docstring calls this a "standard token-bucket limiter", which makes the choice look justified. But nothing in the requirements asks for bursts. This is a mismatch between the abstraction and the actual contract.

## Design 2 (fixed minimum interval) models the real rule

- It enforces a minimum gap between consecutive submits, which is what 4.2 actually says. This holds after idle periods, after retries, and on the very first message, because there is no stored-up allowance to spend.
- `MIN_INTERVAL = 1.05` is a named constant, and its comment explains the margin. The margin is sensible: the gateway measures arrival times, not our monotonic clock, so network jitter can squeeze two sends closer together on its side.
- It is simpler, with no fractional token state. The injected `clock` and `sleep` make it easy to test deterministically.
- Throughput meets the owner's needs:
  - 1,500 messages take about 26 minutes.
  - 2,000 messages take about 35 minutes.
  - Even a perfect 1.0 s pacer would need about 33 minutes for 2,000, so the gateway caps throughput, not the design. If the 30-minute target matters at the top end, the levers are the gateway agreement (more sender IDs or a higher rate) or a slightly smaller margin. Bursting is not one of them.

## Minor notes on Design 2 (none blocking)

- `self.last` is recorded before the submit, not after. Any submit latency therefore only widens the real gap, which is the safe direction.
- It might be worth a test showing that a 429 from the gateway is logged loudly. If one ever happens, that is a signal that the margin is too thin, and the team should know long before reaching 20.

WINNER: 2