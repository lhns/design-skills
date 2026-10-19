# 0002. One-off bookings are confirmed by payment; unpaid holds lapse

**Status:** proposed (2026-10-19). Needs the committee.

## Context
People pencil in dates, go quiet, then cancel, and other hirers are turned away meanwhile (C13). Cheques have to be chased (C14). No deposits (C6). The lunch club and whist drive can't pay online (C11).

## Options considered
- **Pencil in, pay later (today's way):** fails C13 and C14.
- **Deposit to hold a date:** ruled out by C6.
- **Pay in full to confirm; unpaid request held 7 days, then lapses:** meets C13 and C14 with no deposit.
- **Refund on cancellation** (a fork within the option above):
  - always refund: lets late cancellations leave empty Saturdays again (C13, partly);
  - refund if cancelled N weeks ahead: needs N to be picked, and the number isn't forced by anything;
  - **refund if the date is re-let:** a condition that asks for exactly what C13 needs (the slot gets used).

## Decision (proposed)
One-off hirers pay in full to confirm. Unpaid holds lapse after 7 days. Refund in full if the date is re-let. Regulars pay termly in advance.

## Consequences
- Nobody chases cheques. The calendar only shows dates that are actually committed.
- Keeping money on a cancellation could be read as a deposit by another name (R4). That's why this one is for the committee.
- Someone has to match incoming payments to bookings each week (A6).
