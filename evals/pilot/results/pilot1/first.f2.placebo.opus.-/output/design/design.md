# Design: machine bookings and inductions

Status: **Draft 0.1, 2026-10-19. Not reviewed, not approved.** Constraint ids (C…, I…) refer to
[requirements.md](requirements.md); open forks (Q…) are in [open-questions.md](open-questions.md).

## 1. Overview

The workshop needs to (a) know and enforce who may use which machine, (b) keep induction records
the insurer accepts, (c) let members book contested machines from home without passwords, and
(d) know the laser tube's hours. The workshop already has fobs and two fob-controlled interlocks;
the design builds on them.

**Goals:** C1, C3, C4, C5, C6, C7, C9 met, hosted (C10).

**Non-goals (v1):** taking membership payments; supervising the woodshop with staff in the evening
(ruled out by C6); per-minute or per-hour charging for machines (ruled out by C2); interlocks on
machines that have none today (designer choice, see §4).

## 2. The concepts

Seven concepts. Each names the constraint that forces it.

| Concept | What it is | Forced by |
| --- | --- | --- |
| **Member** | A person with a membership. Has one or more fobs (credentials) and an email address. Everything else hangs off the member, not the fob. | C5, I1 |
| **Machine** | A thing that can be used. Has two settings: `people_required` (how many inducted members must tap to power it) and `bookable`. Laser also has `tube_installed_on`. | F1, C6, C3 |
| **Induction** | Member × machine × level (`user` or `trainer`), signed off by a trainer-level member on that machine, with date. Append-only. | C1, C7 |
| **Interlock rule** | A machine powers on when, within one tap window, distinct members numbering at least `people_required` have tapped, each holding an induction on that machine. | C1, C6 |
| **Session log** | One row per interlock power-on: machine, members who tapped, start, end. | C3, C4 |
| **Booking** | Member × machine × time slot, for machines with `bookable = true`. | C4, C9 |
| **Sign-in link** | Website sign-in by a one-time link emailed to the member. No password exists. | C5, C9 (ADR 0003) |

### What is derived rather than added

- **Trainers** are not a separate role: a trainer is a member with a `trainer`-level induction on that
  machine. Who may sign off on the lathe is answered by the induction table itself.
- **The table saw two-person rule** is not a special case: it is `people_required = 2` on the saw.
  The laser is `people_required = 1`. Same rule, one number per machine.
- **Laser tube hours** are not a separate counter: they are the sum of laser sessions since
  `tube_installed_on`. A tube change is recorded by updating that date.
- **No-show detection** needs no check-in step: a booking with no matching session in its first
  minutes is unused (from the session log).
- **"Is it really the same handful of people?"** is answered from the session log and bookings, with
  no extra feature.

### The invariant

> An interlocked machine is powered only while its induction rule holds for the members who tapped.
> Every power-on is in the session log, and every induction it relied on has a signed record.

Any change that lets a machine power on without a logged session, or lets an induction exist without
a trainer sign-off, is wrong.

## 3. Key flows

### 3.1 Induction sign-off (C1, C7)
1. Trainer runs the induction at the machine as today.
2. On the desk tablet (or the machine's reader), the trainer taps their fob, then the member taps theirs,
   and the trainer confirms machine and level.
3. The system checks the trainer holds a `trainer` induction on that machine, then records
   member, machine, level, trainer, timestamp.
4. Whether step 2 is the insurer's "signature", or a drawn signature must also be captured on the
   tablet, depends on the insurer (Q2). The paper book stops being written either way, unless the
   insurer insists on wet ink, in which case the book becomes the signature record and the system
   holds a reference to its page (ADR 0002).

### 3.2 Starting the table saw in the evening (C6, I2)
1. Member A taps the saw's reader. Nothing happens yet; the reader shows "waiting for second person".
2. Member B taps within the tap window. The controller checks both against its cached induction list.
3. Both inducted on the table saw → power on, session logged with both names. Otherwise → stays off,
   the reader shows why (e.g. "B is not inducted on the table saw").
4. Works with the internet down, from the cache; the log syncs later.

Open with the insurer (Q3): whether "both tap to start" is enough, or presence must be re-confirmed
during the session.

### 3.3 Laser (C1, C3)
Same rule with `people_required = 1`. Each session adds to tube hours. Staff get a warning when
`(1,000 h − hours used) ÷ recent hours per week` falls below the supplier's lead time for a tube
plus the time staff need to place an order. This is a condition, not a fixed "warn at 900 h", so it
adjusts itself when the laser gets busier.

### 3.4 Booking from home (C4, C5, C9)
1. Member opens the booking page and enters their email address.
2. They get a sign-in link by email; the browser stays signed in on that device for a long period, so
   most bookings need no email at all.
3. They pick a free slot. The fairness rule (Q4) is checked.
4. If no session starts on the machine within the grace period after the slot starts, the booking is
   released and the slot shows as free.

Interlocks do **not** check bookings (designer choice): the interlock stays ignorant of the optional
booking concept, and walk-up use of a free laser keeps working. If people start using others'
booked slots, revisit.

## 4. Choices and forks

Decisions costly to reverse are ADRs; everything else is listed here.

| Topic | Status | Summary |
| --- | --- | --- |
| Build or buy | Proposed, [ADR 0001](adr/0001-buy-hosted-platform.md) | Buy a hosted makerspace platform that meets the must-haves; build only a gap filler if one is missing. |
| Enforcement point and induction register | Proposed, [ADR 0002](adr/0002-interlock-enforces-digital-induction-register.md) | The digital induction register is the source of truth; the interlocks enforce it. |
| Website sign-in | Proposed, [ADR 0003](adr/0003-email-sign-in-link.md), Q1 | Emailed one-time link; no password. |
| Laser fairness rule | Designer choice, Q4 | Each member holds at most one upcoming laser booking at a time, plus no-show release. No weekly hour quota. |
| 3D printers | Designer choice, Q5 | Not bookable in v1. Making them bookable later is a setting (`bookable = true`), not new work. |
| Materials | Designer choice, Q6 | Outside the machine system: sold as items (a sheet, a spool) and added to the monthly bill. Nothing is tied to machine time. |
| Interlocks on other machines | Designer choice | None in v1. Only C6 demands *enforcement*, and only for the saw. Bandsaw, lathe, printers and bench rely on inductions plus trust, as today. Adding a reader later is configuration. |

## 5. Cross-cutting concerns

- **Safety and reliability.** Interlocks work offline from a cached induction list (I2). If the cache
  is stale, a newly inducted member may have to wait for the next sync; a removed induction may stay
  valid until then. Sync interval is a reasoned bound: short enough that today's inductions work
  tonight (minutes, not hours).
- **Security.** No passwords. Fob loss: staff disable the old fob and issue a new one; inductions stay
  with the member (I1). Sign-in links expire after one use and a short time.
- **Records.** Inductions are append-only; a correction is a new record that references the old one.
  Six-year retention applies to induction records only; bookings and session logs can follow a shorter
  retention (to decide).
- **Privacy.** The session log records who used what and when. Use it for tube hours, no-shows and
  fairness figures; say so to members.
- **Operations.** Front desk tasks: issue/replace fobs, record tube changes, export induction records.

## 6. Testing and rollout

1. **Spike** (before committing to a platform): confirm the shortlisted platform's interlock can do the
   two-person rule and offline caching on the actual saw (R1, R2).
2. **Back-fill** all inductions from the paper book (I4), checked by a second person.
3. **Table saw first**, because the insurer requirement is the hardest: run the two-person rule for two
   weeks in the evenings with the woodworkers, keep the paper book in parallel during this period only.
4. **Laser**: interlock + session log + tube hours, then bookings with the fairness rule.
5. **Website bookings** switch over; old system kept read-only for a month.
6. **Rollback:** the interlocks can be switched back to their current behaviour; the paper book stays
   available until the insurer has accepted the digital records.

## 7. Risks and open questions

See [risks.md](risks.md), [assumptions.md](assumptions.md) and [open-questions.md](open-questions.md).
Highest: R1 (insurer rejects tap-to-start as enforcement), R2 (no platform does the two-person rule).

## 8. Milestones (rough)

1. Ines answers Q1–Q6; insurer answers Q2–Q3.
2. Platform shortlist and spike on the table saw.
3. Design review and sign-off (record date here).
4. Back-fill inductions; table saw live.
5. Laser live with tube hours; bookings live.
6. Decide printers (Q5) and materials (Q6) with real usage data.

## Ledger

- **Forced:** digital induction register (C6 needs the interlock to know inductions); one interlock rule
  with `people_required` per machine (C1, C6); session log (C3); passwordless remote sign-in (C5 + C9);
  hosted (C10); offline interlocks (I2).
- **Designer choices (provisional):** email sign-in link; one-upcoming-booking fairness rule; printers
  not bookable; materials sold as items on the monthly bill; interlocks ignore bookings; no new interlocks.
- **Deleted:** trainer role (is an induction level); tube-hour counter (derived from sessions); weekly hour
  quota (replaced by a condition); per-minute charging (C2); staff-supervised evenings (C6); paper book as
  a parallel record after rollout (pending Q2).
