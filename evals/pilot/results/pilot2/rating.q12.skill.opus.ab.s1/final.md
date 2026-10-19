# Candidate A is the better design

## Which constraint governs

The policy describes how the trustees worked the times out in 2019. Ruth's statement sets the constraint that applies now: **the website must show exactly the times on the leaflet, the season-ticket cards and the gate boards.** Those times are a fixed table of twelve values. A mismatch has already caused trouble once, when season-ticket holders queued at the gate after the old website disagreed with the boards.

The other constraints:
- The garden opens at 10:00.
- Last entry is one hour before closing.
- Closing times change on the first of each month.

## Candidate A

A stores the published table and derives the rest from it. Nothing in it can drift from the boards. The only way to break it is a typo, and anyone can check that by holding the dictionary up against the leaflet. Each concept traces to a constraint:
- `OPENS` comes from the 10:00 opening.
- `CLOSES` is the published table.
- Last entry is derived as closing minus one hour.

## Candidate B

B re-derives the table from a model of the sun. Each year it produces is a fresh guess at a table that never changes.

**1. It matches the table only where it was tested.** The volunteer checked 2026 and 2027. B depends on several inputs that the table does not:
- a sinusoid that stands in for real sunset and ignores the equation of time;
- day-of-year numbering, which shifts in leap years;
- the current daylight-saving rule.

Its margins are thin. For April, B computes 18:33 and rounds down to 18:30, only 3 minutes from the boundary. Any of these drifting a few minutes, or the summer-time dates changing, would flip a month. The website would then disagree with the painted boards, which is exactly the failure Ruth described.

**2. It is not faithful to the policy either.** Its "sunset" is an approximation, and the choice to sample the 15th is the author's own. So B does not reproduce the trustees' 2019 calculation. It is a third source that happens to agree for now.

**3. It cannot record a decision by the trustees.** Suppose the trustees moved one month's time by judgment. A changes one entry. B needs a special-case branch to override its model.

**4. Its extra concepts trace to no current constraint.** These are `sunset`, `last_sunday`, the summer-time flag, the constants 1071 and 105, mid-month sampling and `LATEST_CLOSE`. All of them would only matter if the trustees asked for times to follow the sun again. If that happens, the right move is to recompute the table once and print it, so the website, leaflet and boards stay one fact stated in one place.

## Deciding reason

The constraint is that the website matches the published boards. A stores those values directly. B approximates them with a model that has been verified for two years only and sits minutes from rounding boundaries.

WINNER: 1