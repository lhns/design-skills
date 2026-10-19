# 0003. Members sign in to the website by emailed link

Status: Proposed (2026-10-19). Waiting on Q1.

## Context
No passwords; the fob is the identity at the space (C5). Members must book from home, easily (C9).
A fob can't be tapped at home. One member must not be able to cancel or take another's booking (I5).
The old system's failure was forgotten passwords and constant resets.

## Options considered
See Q1 in [open-questions.md](../open-questions.md): emailed link, fob number + surname,
text-message code, booking only on site.

## Decision (proposed)
Emailed one-time sign-in link; the browser stays signed in on that device. There is no password, so
nothing to forget or reset. The fob stays the identity at the space; email is only how the website
reaches the same member.

## Consequences
Every member needs a current email address (A1). Front desk work becomes "update an email address",
which is rare, instead of password resets. If Ines rejects any website credential besides the fob,
C5 and C9 cannot both hold, and she has to choose which gives way.
