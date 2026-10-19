# Pilot report: pilot1

## gen

| condition | model | n | constraints held | traps passed | concepts | special cases | dup facts | hidden tests |
|---|---|---|---|---|---|---|---|---|
| placebo | opus | 1 | 100% (8/8) | 100% (6/6) | 7.00 | 2.00 | 0.00 | - |
| placebo | sonnet | 1 | 100% (5/5) | 100% (9/9) | 8.00 | 5.00 | 1.00 | 100% (1/1) |
| plain | opus | 1 | 100% (8/8) | 100% (6/6) | 8.00 | 4.00 | 2.00 | - |
| plain | sonnet | 1 | 100% (5/5) | 100% (9/9) | 7.00 | 2.00 | 0.00 | 100% (1/1) |
| skill | opus | 1 | 100% (8/8) | 100% (6/6) | 6.00 | 2.00 | 1.00 | - |
| skill | sonnet | 1 | 80% (4/5) | 100% (9/9) | 8.00 | 3.00 | 0.00 | 100% (1/1) |

## Cost, duration, skill invocation

| track | condition | runs | mean cost $ | mean sec | mean tokens | skill invoked |
|---|---|---|---|---|---|---|
| gen | placebo | 2 | 0.27 | 86.67 | 137,081 | 100% (2/2) |
| gen | plain | 2 | 0.23 | 82.99 | 114,531 | - |
| gen | skill | 2 | 0.31 | 111.18 | 157,452 | 100% (2/2) |

## Token ledger (cap 2,000,000 per skill)

| skill | tokens |
|---|---|
| elegance | 1,223,692 |
| design-by-collapse | 1,681,329 |
