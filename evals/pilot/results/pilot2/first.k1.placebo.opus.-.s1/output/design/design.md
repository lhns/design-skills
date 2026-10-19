# Proposed design (draft 1, 2026-10-19, not agreed)

## Overview

The diary moves into one online calendar that everyone can see. One-off hirers book and pay online. Regulars keep phoning, but they ring a hall number, not Gwen's home. The 23:00 music limit is enforced by the building itself, not by the hirer. Keys stay exactly as they are.

**Non-goals:** keys (C5), deposits (C6), anyone attending the hall at night (C4), deciding the playgroup question (C17; it's the committee's).

## Concepts

Each part of the design and the constraint that forces it. If a part can't name a constraint, it's been left out.

### 1. Booking: one record type for everything (C8, C9, C11, C17)
A booking is a **room + start + end + hirer + state**. Nothing else is a separate kind of thing:
- a **regular hirer** is a *series* of bookings (lunch club every Tuesday);
- **the playgroup taking the upstairs room**, if it happens, is just a long series (C17 needs nothing extra);
- a **room closed for repairs** is a booking with the hall itself as hirer.

The calendar refuses overlaps in the same room (F1). That one rule ends double-booked Saturdays. The public view shows only booked or free (F2).

**Booking states:** `held` → `confirmed`, or `held` → `lapsed`; and `confirmed` → `cancelled`.

### 2. Pay to confirm, with a hold that lapses (C13, C14)
- A one-off request goes on the calendar as **held**. The hirer gets the price and the payment details at once.
- The booking is **confirmed when the money arrives**. Nobody chases payments, because unpaid bookings simply aren't confirmed.
- If nothing arrives by the end of the hold period, the hold **lapses** and the date is free again (F4). *Designer choice:* the hold lasts **7 days**. That covers a bank transfer plus one of Gwen's Monday/Wednesday checks. It's one named value and can be changed.
- **Cancellation:** *designer choice, needs the committee (ADR 0002).* The money is refunded in full **if the date gets re-let**. Otherwise it's kept. This is a condition, not a fixed number of weeks. It answers the wedding problem directly: if the slot gets used, the person who cancelled loses nothing.
- **Regulars** pay for their series termly, in advance, by standing order or a single cheque (designer choice). This replaces one cheque per date.

This answers Gwen's question ("make everyone pay online when they book?"): **yes for one-off hirers. Regulars pay termly instead, because the lunch club and whist drive can't pay online (C11).**

Keeping money when someone cancels is close to the 2023 deposit row (C6). The difference is that the cancellation rule is announced in advance and is objective: nobody has to judge a sticky floor. Even so, it's the committee's call (risk R4).

### 3. Price from a table (C7)
| Room | Rate |
| --- | --- |
| Upstairs room | £12/h |
| Main hall | £25/h |
| Main hall, Saturday night | £30/h |

Open: when does "Saturday night" start? What does the kitchen cost? Is it part of the main hall? (Q5)

### 4. Saturday rule (C15, C18)
Gwen suggested a 12-Saturdays-a-year cap. That would end the dance school's Saturday mornings, and it still wouldn't free the afternoons. The scarce slots are **Saturday afternoon and evening**, since families and parties want those. Proposed rule (ADR 0003): **standing series may not include Saturday after 12:00. Those slots are for one-off bookings.** The dance school is unaffected. Pilates is offered another weekday slot rather than Saturday afternoons. No number has to be counted or policed.

### 5. The 23:00 cut-off is done by the building (C2, C3, C4, C18)
The officer has ruled out anything that relies on the hirer, and no volunteer can be there at night. That leaves the building itself. **The time switch the electrician already fitted cuts the power to the music sockets at 23:00 every night.**
- The switch is only proof of enforcement if it covers **every socket a disco could use** in the main hall. If a DJ can run a cable to a wall socket that isn't on the switch, the control depends on the hirer again. **This is Q1, and it decides whether the plan works.** If the switch doesn't cover them, the electrician has to put those sockets on it too. Fridges, lighting and emergency circuits stay off it.
- *Designer choice:* set the cut-off at **22:58**. "Not a minute after" leaves no room for a cheap switch's clock drifting. Two minutes covers drift between checks, and the check log shows how much it has actually drifted.
- **Clock changes:** if the switch doesn't adjust for summer time by itself, it must be re-set on **25 Oct 2026** and **28 Mar 2027**. The second date falls during Gwen's absence (R1).
- **Evidence for the officer (N4):** a one-page record giving the circuits switched, the time set, and dated monthly checks done by daylight (does the switch show the right time, does a test cut work). It goes in the hire terms and is sent to the licensing officer. Sending it is the committee's step.
- Hirers are told before paying: *"Power to the music sockets switches off at 23:00. Plan your last song for 22:50."* (F8)

### 6. Kitchen: rubbish leaves with the hirer (C16, C6, C4)
No deposits and no night visits means there's no penalty to impose and nobody to check that evening. So the design takes away the thing that went wrong: **there are no hall bins for hirers. Hirers take all their rubbish home** (bin bags provided), and this is stated before they pay. *Designer choice:* a daylight check on Monday morning (Gwen's day; someone else Jan–Mar) catches weekend problems before Tuesday's lunch club. Hirers who leave a mess more than once aren't offered another booking. That's a booking decision, not money withheld. Q6 asks whether the bins can go.

### 7. Contact without Gwen's home phone (C10, C11, C12)
- A **hall phone number**, cheap pay-as-you-go or a voicemail number (N1). Its message says "for free dates and booking, see [web address]; otherwise leave a message, we call back Monday or Wednesday morning."
- The lunch club and whist drive ring this number for extra dates. Gwen (or her stand-in Jan–Mar) adds those dates to their series.
- Gwen's home number is taken off everything public.

### 8. Tooling (C19, N1, N2)
*Designer choice, not yet researched:* use a ready-made village-hall booking service if one is free or nearly free and does F1–F4 itself (no overlaps, public availability, request plus payment, holds that lapse). Otherwise use a shared calendar with a public free/busy view, a request form, and bank-transfer payment using the booking reference. That fallback can't refuse overlaps or lapse holds by itself, so a volunteer would do both. Choose after Q4 (budget).

## Cover January–March 2027 (C12)
Most of this exists so that it runs without Gwen. Even so, someone has to (a) check the payments and the voicemail once a week, (b) do the Monday kitchen check, and (c) re-set the time switch on 28 Mar 2027. Who that is hasn't been decided (Q3).

## Milestones (rough)
1. **Now:** answer Q1. Get the electrician to set the time switch and, if needed, extend it to the other sockets. Start the check log. This is urgent whatever else happens.
2. **November:** the committee decides ADRs 0002 and 0003 and the budget. Choose the tooling.
3. **Late November:** move the diary into the calendar, including the regular series and every 2027 booking Gwen already has. Set up the hall phone.
4. **December:** run both for a few weeks while Gwen is still here. Hand over to the stand-in.
5. **January:** Gwen away. System live.
