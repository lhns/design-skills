# Pacing outgoing text alerts: Candidate A (Design 2) is the better design

Candidate B looks more flexible, but its flexibility is exactly what the gateway agreement forbids.

## Constraints
- **C1 (4.2):** at most one submit in any one-second interval. This is a sliding-window limit, not an average.
- **C2 (4.3):** more than 20 rejections in a day means a 24-hour suspension, lifted only by hand. A burst that breaks C1 is therefore a service outage, not a slowdown.
- **C3 (owner):** every message goes out and nobody is skipped. Speed comes second.
- **C4 (developer):** there is one worker and one gateway client. Retries go through `pace()`.

## Trying to break each design

**Candidate B (token bucket, Design 1)** breaks on the first flood warning.
- The bucket starts full at `BURST = 10`. After any quiet spell it refills to 10.
- So the first 10 `pace()` calls return immediately and 10 submits go out within milliseconds.
- That gives 9 rejections (429) per burst.
- A second quiet spell followed by a burst in the same day exceeds 20, and the sender ID is suspended for 24 hours. That breaks C2 and C3: residents in the valley get nothing.
- A token bucket enforces a long-run *average*. C1 is a per-interval *ceiling*, so the only burst size the agreement allows is 1.
- With `BURST = 1` it degenerates into Candidate A, with an extra concept (fractional tokens) and no margin.
- `BURST = 10` is an unforced number. No constraint names it, and the one constraint that does speak forbids it.
- The "faster first ones" wish doesn't rescue it. Rejected messages aren't faster; they are retries that also count toward suspension.

**Candidate A (minimum interval, Design 2)** holds up.
- Consecutive submits start at least 1.05 s apart, so no one-second window can contain two. C1 holds.
- A failed network submit that did reach the gateway is still spaced correctly, because the retry passes through `pace()`. C4 holds.
- The `0.05` margin is one named bound with a stated reason: clock and network jitter between our send time and the gateway's receive time. That is how a forced bound should look.
- `last` is set when `pace()` returns, before the submit. The real gap between submits is therefore at least 1.05 s, never less.
- The design has one concept (the time of the last submit) and one branch (the first call). Nothing in it is unforced.

## A note on C3's half hour
Neither design can meet a strict half-hour target, and none could:
- 2,000 messages at the legal maximum of 1 per second take about 33 minutes.
- At 1.05 s per message, Candidate A takes about 35 minutes.

This is a property of the gateway contract, not of the pacer. If the owner needs 2,000 messages in under 30 minutes, the options are a second registered sender ID or a negotiated rate. Squeezing the margin, or adding a burst, would only risk suspension. The owner's actual priority, "all of them go out and nobody is skipped", is met by A.

## Ledger
- **Forced:** the burst size is 1, because C1 is a per-interval ceiling. That makes the minimum-interval pacer the forced design.
- **Designer choice:** the 0.05 s margin. It is reasoned but provisional, and could be tuned against observed jitter.
- **Deleted:** the bucket capacity, fractional tokens and refill logic. No constraint needs them.

**Deciding reason:** Candidate B's burst of 10 breaks the gateway's one-message-per-second ceiling and leads to a 24-hour suspension, while Candidate A keeps every constraint with a single concept.

WINNER: 2