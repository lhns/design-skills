# Mill Lane Workshop: bookings and inductions (design v0.1)

Status: first draft, 2026-10-19. Built from Ines's brief (see `stakeholder-log.md`).
The open forks are in `open-questions.md`. Anything marked **designer choice** is
provisional and changes if a stakeholder answer contradicts it.

## 1. Constraints

Sources: **I** = Ines's own words, **R** = reality (law, hardware, physics),
**inf** = inferred from context. Only these remove options.

| id  | constraint | source |
|-----|------------|--------|
| C1  | Nobody uses a machine until a trainer has inducted them on that machine. | I, 2 Oct |
| C2  | Members pay for the materials they use. | I, 2 Oct |
| C3  | No member ever feels a meter running while they work. | I, 2 Oct |
| C4  | The laser must not go down for lack of a replacement tube. A tube lasts about 1,000 cutting hours, and two have failed without warning this year. | I, 6 Oct; R |
| C5  | Laser time is spread fairly. Today it is booked solid and the same few people get it. | I, 6 Oct |
| C6  | No member passwords. The fob is the member's identity. | I, 9 Oct |
| C7  | The table saw only runs with two people present who are both inducted on it. The system must enforce this, not trust people. It has to work with no staff on site (18:00-22:00). | I, 9 Oct; insurer |
| C8  | The insurer can see every induction with the trainer's signature and the date, kept for six years. | I, 14 Oct; insurer |
| C9  | Members can book from home through the website, and it is easy. | I, 16 Oct |
| C10 | We don't run our own server. | I, 16 Oct |
| C11 | Table saw and laser already have fob-controlled power interlocks. Members already have fobs. | R |
| C12 | Staff on site 10:00-18:00. Members until 22:00. | R |
| C13 | Losing the internet must not let an uninducted person start an interlocked machine, and must not let one person start the table saw alone. | inf (from C1, C7) |
| C14 | Induction records stay after a member leaves, for the six years in C8 (and that retention is the stated reason for keeping their personal data). | inf (C8, data-protection law) |

Not yet a constraint: whether 3D printers are bookable. Ines is still deciding,
so the design must let her decide either way without rework (see F7).

## 2. What the constraints force

- **Inductions must be digital** (C1, C7, C11). The interlocks have to know, at the
  moment of a tap, whether a fob is inducted on that machine. A paper book can't
  tell them that. If the paper book stayed the only record, every induction would
  be written twice (book and interlock list), and the two would drift apart. The
  open question is only whether the digital record can **replace** the book for the
  insurer (F3), not whether there is one.
- **The fob identifies the member everywhere on site** (C6, C11). That covers
  machines, inductions and materials.
- **Home booking needs one more way to recognise a member,** because a fob can't be
  tapped at home (C6 vs C9). That conflicts with "fob, full stop". F1 resolves it.
- **Hosted software** (C10). The only things on site are the interlock controllers,
  which already exist (C11).
- **Interlock controllers decide locally** (C13). Each controller keeps a copy of
  the rules for its machine: who is inducted, and today's bookings. The cloud
  updates that copy, but a tap is never decided by the cloud. With no copy, a
  controller refuses to start the machine (fail closed).
- **Nothing members see is priced by time** (C3). Time is measured only for staff
  (laser tube life), and members never see a count-up or a cost per minute.

## 3. The concepts

Six concepts. Each is listed with the constraint that breaks without it.

| concept | what it is | forced by |
|---------|------------|-----------|
| **Member** | A person, identified by their fob ID. Has a name and an email address. | C6, C9 |
| **Machine** | A thing that needs an induction. Three settings: `interlocked` (C11), `bookable` (C5, F7), `people_required` (1, or 2 for the table saw; C7). | C1 |
| **Qualification** | Member M may use machine X, granted by trainer T on date D. `level` is `user` or `trainer`. A trainer is just someone qualified at trainer level, so there is no separate trainer concept. Records are append-only: revoking adds a new record instead of deleting one. | C1, C7, C8, C14 |
| **Booking** | Member M holds machine X from time S to time E. | C5, C9 |
| **Charge** | Member M took material item I, at a fixed price per item. It goes on the monthly bill. | C2, C3 |
| **Rule** | One function, described below. | C1, C5, C7 |

### The rule (the shared concept)

Inductions, the two-person table saw and bookings are all cases of one question:
*may this set of fobs use this machine now?*

```
may_use(machine, fobs, now) =
      count(f in fobs where qualified(f, machine)) >= machine.people_required
  and (no booking holds machine at now  or  that booking's member is in fobs)
```

- **Laser**: `people_required = 1`. One inducted tap turns it on.
- **Table saw**: `people_required = 2`. Two different inducted fobs, tapped within one
  arming window, turn it on. It is the laser rule with a different number, not a
  special mode.
- **Bandsaw, lathe, bench, printers** (not interlocked): the same rule runs at
  booking time, if the machine is bookable, so you can only book what you're
  inducted on. On the floor, C1 still relies on people for these machines.
  Nothing in the brief asks for more.
- The booking condition means a booked slot really belongs to the person who
  booked it. Outside booked slots, anyone inducted can walk up and use the
  machine. (**Designer choice**: this makes bookings binding without adding a
  "check-in" concept.)

The **invariant**: an interlocked machine is powered only while `may_use` was true
at its last arming. Any change that can power a machine another way is wrong.

### Things the design doesn't need

- **Trainer** as a separate type. It is a Qualification at `trainer` level.
- **Member passwords** (C6).
- **A stored laser-hours counter.** If one is needed (F4), it is computed from the
  interlock's power-on log since `laser.tube_fitted_on`. It is not a stored number
  that someone has to keep correct.
- **A consumables or parts subsystem.** Only one part (the laser tube) needs
  tracking. One case isn't a pattern.
- **Time-based pricing** (C3).

## 4. How each constraint is met (break attempts)

| constraint | attempt to break it | why it holds |
|------------|---------------------|--------------|
| C1 | An uninducted member taps the laser. | `qualified` is false, so the laser stays off. On non-interlocked machines it relies on people (see the rule above). |
| C3 | A member watches cost go up while cutting. | No member-facing time or price display exists. Charges are per item taken. |
| C4 | The tube dies after 400 hours. | Under F4(b) the spare is already on the shelf. An hour counter alone (F4(a)) would **not** survive this. |
| C5 | One member books every Tuesday evening for a month. | With one upcoming booking per member per machine (F5) they can hold only the next one. |
| C6 | A member forgets their login. | There is nothing to forget. A sign-in link is emailed on request (F1). |
| C7 | A member taps their fob twice, or uses a friend's fob who isn't there. | Two **different** inducted fobs are needed. A borrowed fob is beyond any fob system: see F2. |
| C7 | 19:30, no staff. | The rule runs on the controller and needs no staff. |
| C8 | The insurer asks for 2021 sign-offs in 2027. | Qualifications are append-only and kept for 6 years. Whether a fob tap counts as a signature is F3. |
| C13 | Internet is down at 20:00. | The controller uses its local copy. With no copy, it fails closed. |

## 5. Ledger

**Forced**: digital induction record; the fob as on-site identity; hosted software;
local decisions on the controllers; no member-facing time meter; one `may_use` rule
with `people_required` as a per-machine number.

**Designer choices (provisional)**: bookings are binding on interlocked machines;
inductions are recorded by trainer and member tapping at a desk tablet; printers
start as not bookable (F7); the defaults in F1, F4, F5 and F6.

**Deleted**: trainer type, passwords, stored hour counter, parts subsystem,
weekly hour cap (see F5), time-based pricing.

**Counts**: 6 concepts, 0 exception clauses in the rule, 1 per-machine number
(`people_required`), and unforced numbers held as named settings: booking
maximum length, arming window.
