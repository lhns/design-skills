# 0002. The interlocks enforce a digital induction register

Status: Proposed (2026-10-19). The signature part depends on Q2.

## Context
The table saw's two-person rule must be enforced, in the evenings, without staff (C6). Enforcement
at the machine means the machine must know who is inducted on it. The insurer wants trainer
signature and date, kept six years (C7). Today that is a paper book (F6).

## Options considered
- **Keep the paper book only.** Cannot meet C6: the saw can't read the book.
- **Paper book for signatures plus a digital list for the interlocks.** Meets C6 and C7, but the same
  fact (who is inducted) lives in two places and they will drift.
- **Digital register only; the trainer signs off with their fob (or a drawn signature on a tablet).**
  One record. Meets C7 if the insurer accepts it (Q2).

## Decision (proposed)
The digital induction register is the single source of truth. Interlocks enforce it with one rule:
power on when `people_required` distinct inducted members have tapped. Trainer sign-off is captured
digitally. The paper book stays only if the insurer requires wet ink, and then only as the signature
record, referenced from the digital entry.

## Consequences
The interlock rule covers the laser and the saw with one parameter. Existing paper entries must be
back-filled before go-live (I4). The paper book itself is still kept for six years from its last entry.
