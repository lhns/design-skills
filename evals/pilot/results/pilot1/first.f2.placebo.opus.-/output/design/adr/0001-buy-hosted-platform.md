# 0001. Buy a hosted makerspace platform rather than build

Status: Proposed (2026-10-19)

## Context
The workshop would rather not run a server (C10), and the budget is approved (C11). What's needed
(member records, fobs, inductions, interlocks, bookings, usage logs) is what makerspace management
platforms sell. The unusual requirement is the table saw two-person rule (C6).

## Options considered
- **Hosted makerspace platform with its own machine readers.** No server; vendor maintains it. Risk:
  may not support a two-person rule or offline operation.
- **Hosted platform plus a small custom controller for the table saw only.** Covers the gap if the
  platform lacks the two-person rule; adds one bespoke component to maintain.
- **Build our own hosted app.** Fits exactly, but the workshop then owns software for years. Nothing
  in the brief requires it.

## Decision (proposed)
Buy a hosted platform. Shortlist only platforms that meet these must-haves, in this order:
1. Per-machine rule needing N distinct inducted members to power on (N = 2 for the saw). (C6)
2. Interlocks decide and log offline, then sync. (I2)
3. Member sign-in on the website without a password (e.g. emailed link). (C5, C9)
4. Induction records with trainer, date and sign-off; exportable; six-year retention. (C7)
5. Bookings with a per-member limit on upcoming bookings. (C4)
6. Session log with machine-hours reporting. (C3)

If no platform meets (1)–(2), take the second option: platform plus a small saw controller.
Example to evaluate (unverified): Fabman, which sells hosted machine access with trainings and
bookings. Its fit to (1) and (2) must be checked with the vendor.

## Consequences
Little software to maintain. The design's concepts must map onto the platform's; where they don't,
revisit the design, not work around it. Vendor lock-in is a risk (R7), mitigated by export.
