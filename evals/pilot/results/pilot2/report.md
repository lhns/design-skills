# Pilot report: pilot2

## audit

| condition | model | n | detection | real/doc | defensible/doc | wrong/doc | clean docs with a wrong finding |
|---|---|---|---|---|---|---|---|
| collapse | opus | 8 | 100% (11/11) | 4.88 | 3.25 | 0.12 | 50% (1/2) |
| elegance | opus | 8 | 100% (11/11) | 4.25 | 2.88 | 0.12 | 50% (1/2) |
| placebo | opus | 8 | 100% (11/11) | 4.50 | 2.12 | 0.12 | 0% (0/2) |

## Cost, duration, skill invocation

| track | condition | runs | mean cost $ | mean sec | mean tokens | skill invoked |
|---|---|---|---|---|---|---|
| audit | collapse | 8 | 0.08 | 28.98 | 9,492 | n/a (lean) |
| audit | elegance | 8 | 0.07 | 28.59 | 7,008 | n/a (lean) |
| audit | placebo | 8 | 0.08 | 29.11 | 9,573 | n/a (lean) |

## Token ledger (cap 2,000,000 per skill)

| skill | tokens |
|---|---|
| elegance | 1,635,507 |
| design-by-collapse | 1,015,279 |
