# Requirements

Status: draft, 2026-10-19. Sources are dates in Ines's brief. *Inferred* items are not Ines's words;
they follow from the context and need her confirmation.

## Facts about the space (from the brief)

- F1. Machines: woodshop (table saw, bandsaw, lathe), 1 laser cutter, 3 × 3D printers, 1 electronics bench.
- F2. About 180 members on a flat monthly fee.
- F3. Members enter with a key fob.
- F4. The table saw and the laser already sit behind fob-controlled power interlocks.
- F5. Staff on site 10:00–18:00; members may stay until 22:00.
- F6. Inductions today: a paper sign-off book at the front desk, signed by trainers.
- F7. Members book from home through the website today.

## Constraints

| Id | Constraint | Source | Priority |
| --- | --- | --- | --- |
| C1 | A member must be inducted on a machine, and signed off by a trainer, before using it. | 2 Oct | Must |
| C2 | Members pay for the materials they use, but must never feel a meter running while they work. | 2 Oct | Must (how: open, Q6) |
| C3 | The workshop must know how many cutting hours the laser tube has used (life ≈ 1,000 h) early enough to order a spare. | 6 Oct | Must |
| C4 | Laser access should be fairer: today the same handful of people get it. Rule left to the designer. | 6 Oct | Should (rule: Q4) |
| C5 | No member passwords. At the space, the fob is the member's identity. | 9 Oct | Must |
| C6 | The table saw only runs with two people present who are both inducted on it. This must be enforced, not on trust (insurer). It must work in the evenings with no staff; closing the woodshop early is not an option. | 9 Oct | Must |
| C7 | Induction records show the trainer's signature and the date, can be shown to the insurer at renewal, and are kept for six years. | 14 Oct | Must |
| C8 | 3D printers get hogged by long (≈14 h) prints. Whether to make them bookable is undecided. | 14 Oct | Open (Q5) |
| C9 | Members can book from home through the website, and it is easy. | 16 Oct | Must |
| C10 | The workshop does not run its own server. | 16 Oct | Should ("rather not") |
| C11 | Budget is approved by the board. | 16 Oct | Context |

### Inferred constraints (need confirmation)

| Id | Constraint | Why it follows |
| --- | --- | --- |
| I1 | Inductions belong to the member, not to the fob. | Fobs get lost and replaced; a new fob must not wipe someone's inductions. |
| I2 | The interlocks keep working when the internet or the hosted service is down. | Evenings have no staff (F5) and the table saw rule must be enforced (C6); a dead link must not mean either "saw unusable all evening" or "saw unprotected". |
| I3 | Induction records of members who have left are still kept for six years. | C7 covers all records the insurer may ask about; data protection law then needs a stated reason to keep them, which C7 provides. |
| I4 | Existing inductions in the paper book are carried into the new system. | Otherwise every current member would be locked out of the table saw and laser on day one. |
| I5 | One member cannot cancel or take another member's booking. | The laser is contested (C4), so anonymous or guessable booking access would be abused. |

## Functional requirements

| Id | Requirement | Traces to | Priority |
| --- | --- | --- | --- |
| FR1 | A trainer signs a member off on a machine; the record holds member, machine, trainer, date and the trainer's sign-off. | C1, C7 | Must |
| FR2 | An interlocked machine powers on only when the required number of distinct members, each inducted on it, have tapped (laser: 1, table saw: 2). | C1, C6 | Must |
| FR3 | Staff can produce the induction records for the insurer, for any period in the last six years. | C7 | Must |
| FR4 | Every interlock session is logged: machine, members, start, end. | C3, C4 | Must |
| FR5 | The system shows laser tube hours used since the last tube change, and warns staff in time to order a spare. | C3 | Must |
| FR6 | A member can book a bookable machine from home on the website without a password. | C5, C9 | Must |
| FR7 | Laser bookings follow a fairness rule (Q4). | C4 | Should |
| FR8 | A laser booking that is not used is released so others can use the slot. | C4 | Should |
| FR9 | Staff can replace a member's fob without losing their inductions or bookings. | I1 | Must |
| FR10 | Existing paper inductions are entered before the interlock rules go live. | I4 | Must |
| FR11 | Members are charged for materials in a way that does not meter their time (Q6). | C2 | Should |

## Non-functional requirements

| Id | Requirement | Traces to | Priority |
| --- | --- | --- | --- |
| NFR1 | Hosted service; no server on site that the workshop has to maintain. Small interlock controllers at machines are acceptable. | C10 | Should |
| NFR2 | Interlocks decide from a locally cached induction list and log locally when offline, syncing later. | I2 | Must |
| NFR3 | Induction records are retained for six years, cannot be silently edited, and survive a change of vendor (exportable). | C7 | Must |
| NFR4 | Booking from home takes no more steps than today's website; a first-time member succeeds without help from the front desk. | C9, C5 | Must |
| NFR5 | Personal data handled under data protection law; members can see what is held about them. | I3 | Must |
