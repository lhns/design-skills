# Village hall bookings: design

Status: first draft, 2026-10-19, written from Gwen's brief. Nothing here has been checked with the committee yet.
Open questions and the session log are in `notes.md`.

## 1. Constraints

These are things Gwen said, or facts about the hall. Ones marked *inferred* are my reading of what she said.

| id | Constraint | Source |
|----|-----------|--------|
| C1 | Amplified music stops at 23:00. The committee has to be able to **show** this is enforced, and a rule the hirer has to follow doesn't count. If it's breached again, the licence will probably be reviewed. | licence, licensing officer's email |
| C2 | Nobody goes to the hall at night and nobody is on call at night, whether at the hall or from home. | committee agreement |
| C3 | Everyone is a volunteer and there's no money to pay staff. | brief |
| C4 | Keys stay as they are: hirers collect them from the shop and return them through the shop's letterbox. | "don't fix what isn't broken" |
| C5 | No deposits. Keeping back money because of a judgment about damage or mess is what caused the 2023 row. | 2023 history |
| C6 | No double bookings. People can see which dates are free without asking anyone. | brief |
| C7 | No chasing cheques, and dates shouldn't sit pencilled in by people who then go quiet and cancel. | brief |
| C8 | Hirers stop ringing Gwen at home. | brief |
| C9 | The lunch club and whist drive organisers don't use email. They ring to book extra dates. | brief |
| C10 | The kitchen gets left dirty, and the next group (often the Tuesday lunch club) walks into it. | brief |
| C11 | Saturdays are under pressure. The dance school has every Saturday morning, Pilates wants Saturday afternoons, and families can't get a Saturday until spring. Saturday-night parties, with a disco, pay for the roof fund. | brief |
| C12 | The upstairs room might not be available to let next year (the playgroup wants it). | brief |
| C13 | Prices: upstairs room £12/h, main hall £25/h, £30/h on Saturday nights. | brief |
| C14 | It needs to work from January, when Gwen is away until March. She's available Monday and Wednesday mornings. | brief |
| C15 | *Inferred:* whatever we use has to be run by volunteers who aren't technical. We don't build custom software. | C3, C14 |

## 2. The core concept

Almost everything in the brief comes down to one question: **who has which room, and when, and has it been paid for?**
So the design is built around a single **booking** record:

> booking = room · start–end · hirer · paid?

- One shared calendar of bookings that anyone can see. Free dates are simply the gaps. (C6)
- **A booking only exists once it's paid.** Nothing gets pencilled in, so there are no cheques to chase and nobody can hold a date without committing to it. (C7)
- **Rooms are a list in the system, not built into it.** If the upstairs room goes to the playgroup, someone removes one line and nothing else changes. (C12)
- **Prices are a table:** room × time band. (C13)

The invariant: **for any room, at most one paid booking covers any given minute.** Any process or tool that can break this is wrong.

Regulars aren't a separate kind of thing. A **standing booking** is just a rule that produces ordinary bookings (every Tuesday 10–14, main hall + kitchen). Regulars pay for each term in advance, so the same invariant and the same "paid = exists" rule cover them.

## 3. The 23:00 music cut-off (C1, C2)

This is the part that carries legal risk, so I've kept it separate from the booking system on purpose. The booking system can't enforce anything at 23:00, because no person is there and no software is involved. Only a piece of equipment can.

C1 rules out any control that relies on the hirer. C2 rules out any control that relies on a person being there at night. The only option left is the one the hall already owns: **the time switch on the sound limiter, set to cut the supply at 23:00.**

It only satisfies C1 if all three of these hold:

1. **It covers every socket a disco could use.** If it only cuts the stage sockets, a DJ can run an extension lead from a wall socket and carry on. **This is unconfirmed, and it's the most important open question** (see notes.md, Q1). If the switch is stage-only, the electrician needs to extend it to the hall's other sockets, or those sockets need to be on the same switched circuit. That costs money, and C1 means it's needed anyway.
2. **The time is still right after clock changes and power cuts.** Clocks go back on **Sunday 25 October 2026**. A mechanical switch that's been set correctly will be an hour wrong after that unless someone resets it.
3. **Tampering is visible, and the checks are written down.** That's how the committee can show enforcement. Fit a lockable or sealed cover. Keep a log with one line per check: date, time shown on the switch, seal intact (yes/no), initials.
   - **When to check:** the first daytime visit after (a) every Saturday-night hire, (b) every clock change, and (c) every power cut. These are the events that could break the switch, so each check is tied to a risk rather than to a fixed timetable.
   - Gwen is already at the hall on Monday mornings, which comes after every weekend hire. January to March needs someone to cover this (Q2).

What it can't cover: battery-powered speakers. No switch can stop those. We should say so openly to the licensing officer rather than claim the system is complete. The hire agreement still includes the 23:00 rule, but it's backup, not the control.

What the booking system does here: Saturday-night bookings show "power to all main-hall sockets cuts at 23:00" when they're made. Then nobody can say they didn't know, and DJs can plan for it. Nothing else.

## 4. How people book

**Reuse first:** don't build anything. Use an off-the-shelf village-hall booking service (Hallmaster is one example, and there are others). The things we need are standard features: a public calendar, online payment at the point of booking, recurring bookings, and room/price tables. Running costs would be a subscription and card fees. Whether the committee will pay those is Q4. If not, the fallback is a public Google Calendar plus a payment link. It's free, but a volunteer has to enter each booking after payment, so it's weaker for C14.

| Who | How they book | How they pay | Satisfies |
|-----|---------------|--------------|-----------|
| Anyone with internet | Picks a free slot on the hall website | Card, when booking. The booking exists once paid | C6, C7, C8 |
| Anyone without internet | Rings the **hall phone number** (not Gwen's home). It goes to voicemail, and messages are dealt with on Monday and Wednesday mornings | To be decided (Q5) | C8, C9 |
| Regulars (lunch club, whist, Pilates, dance school) | Standing booking, renewed each year | Each term in advance | C7, C9 |
| Regulars' extra dates | **Booked once a year, in one phone call:** Christmas lunch, AGM, summer outing tea, etc. They're the same every year. Anything unexpected goes through the hall phone | Added to that term's bill | C9, C8 |

The hall phone can be a cheap SIM or a voicemail number. It replaces Gwen's home number on every notice, form and website page. It only gets answered in daytime hours, which also fits C2.

**Cancellations (no deposit, C5).** Proposal: *if you cancel, you get your money back once someone else books the slot.* This uses a condition rather than an arbitrary "4 weeks' notice" rule, and it makes up exactly the loss Gwen described (two weddings turned away for a Saturday that ended up empty). Nobody makes a judgment call about anyone, which is what caused the 2023 row. Even so, the committee has to agree it, because people might see it as a deposit by another name (Q6).

## 5. Saturdays (C11)

Split Saturday into three bookable parts: morning, afternoon and evening. The dance school's mornings don't actually clash with christening teas or party evenings.

Designer choice (Q3): **standing bookings can't take Saturday afternoons or evenings.** Those slots stay open for one-off hires. The dance school keeps its mornings. Pilates gets a weekday slot instead.
I've used a rule about which slots regulars can have rather than "max 12 Saturdays", because 12 is an arbitrary number. It would also only ever affect regulars, since no family books twelve Saturdays. So the rule says what it's actually for.

## 6. Kitchen (C10)

C5 rules out holding money back, and C2 rules out checking at night. What's left:
- **The hirer takes all rubbish away.** No bags are left inside the building. This is in the booking confirmation and on a card in the kitchen, together with a short checklist for leaving the kitchen.
- **Check on Monday morning.** Gwen already goes in then. It comes after every weekend hire and before the Tuesday lunch club. It can be the same visit as the time-switch check in §3. It doesn't need another trip.
- **Consequence:** each booking has a named hirer, so a mess can be traced to them. Someone who leaves it dirty isn't offered another booking. That isn't money being kept back, so the 2023 problem doesn't come up again.

Designer choice. Gwen only asked for the problem to stop, so this is open to change.

## 7. Before January (C14)

1. **Before 25 Oct:** find out what the time switch covers (Q1). Set it to 23:00, seal it, and start the log.
2. **November:** the committee decides Q3–Q6. Choose the booking service and enter rooms, prices and standing bookings. Book the regulars' 2027 extra dates in one phone call each.
3. **November:** set up the hall phone number. Copy the existing diary into the calendar. Any double bookings will show up here, so sort them out.
4. **December:** put the hall phone number and website on every notice instead of Gwen's number. Find someone to cover Monday mornings from January to March (Q2).

## 8. Ledger

**Forced**
- Time switch on the limiter as the 23:00 control (C1 + C2 leave nothing else). It must cover every socket, and there must be a seal and a log.
- One shared calendar with one booking record (C6).
- A booking exists only once paid (C7).
- Rooms and prices kept as data (C12, C13).
- A phone route that isn't Gwen's home and works without email (C8 + C9).
- No custom software (C15).

**Designer choices (provisional)**
- Off-the-shelf booking service rather than Google Calendar (Q4).
- Regulars' annual extra dates booked in one go.
- Saturday split into three. Standing bookings kept out of Saturday afternoons and evenings (Q3).
- Refund on cancellation once the slot is re-let (Q6).
- Kitchen: take-it-home rule, Monday check, refusing future bookings.
- Checks tied to events (Saturday hire, clock change, power cut) rather than a fixed timetable.

**Deleted or not adopted**
- "12 Saturdays each": arbitrary number, replaced by the slot rule.
- Deposits and damage charges (C5).
- Any change to keys (C4).
- Hirer-dependent clause as the music control: kept only as backup (C1).
- A separate "regular" type of booking: a standing booking just produces ordinary bookings.
- Pencilled or provisional bookings: replaced by paid = exists.
