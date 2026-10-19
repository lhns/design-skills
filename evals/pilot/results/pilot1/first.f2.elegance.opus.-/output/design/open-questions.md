# Open forks

The forks are in order: the ones whose answers settle the most come first. Each one lists the options, what
each option forces, and a recommendation. Until someone answers, the recommendation is
used as a **designer choice**.

Who can answer: **Ines** directly; **Insurer** (Ines needs to ask them);
**Vendor** (the interlock supplier).

---

## F1. How does a member identify themselves on the website from home? (Ines)

C6 (fob only, no passwords) and C9 (book from home) conflict, because nobody can tap a fob at home.

| option | what it forces |
|--------|----------------|
| **a. Emailed sign-in link.** Enter your email address and click the link you receive. The device stays signed in for months. | One email address per member. There is nothing to remember, so there are no resets. If a member changes email, the desk updates it once. The member record is still keyed by fob. |
| b. Book without identifying yourself, then claim the booking by tapping at the machine. | Anyone can book in anyone's name. That breaks the fairness rule (C5) and the induction check at booking time (C1). |
| c. Fob number plus a PIN. | A PIN is a password, which breaks C6. |
| d. A permanent personal booking URL. | Same as (a) but the link never expires. If it is forwarded, someone else can book as you. |

**Recommendation: (a).** It removes exactly the problem Ines described (people
forgetting passwords and the desk resetting them) and keeps the fob as the
identity on site. It also narrows F0: we need software that supports
passwordless sign-in.

## F0. Buy or build? (designer, after F1)

Hosted makerspace-management products already exist that do interlock control,
training records, bookings and member billing (Fabman is one example; there are
others). C10 (no own server) and the approved budget both point towards buying.

**Recommendation:** treat `design.md` as the requirements checklist and evaluate products against it.
Must-haves: `people_required = 2` (two-person start), passwordless member
sign-in (F1), local decisions on the controllers (C13), induction export for the
insurer (C8), and compatibility with **our existing interlocks** (F8). Build only
if no product meets C7 and C13.

## F8. What are the existing interlocks? (Ines / Vendor)

Make and model, and whether they can (i) require two different fobs to start, (ii) keep
working offline from a local list, and (iii) report power-on and power-off times. This decides F0 and
F2. If (i) isn't possible, the table saw needs a new interlock.

## F2. What counts as "enforced" for two people on the table saw? (Insurer)

No fob system can prove that a person is still in the room. It can only prove that their fob was
used.

| option | what it forces |
|--------|----------------|
| **a. Two-fob arming.** Two different inducted fobs within the arming window. The session ends when the saw has been idle for a while, so each new work period needs both people again. | No new hardware beyond two-fob support. It shows two people were present at each start. |
| b. Both fobs stay docked at the saw while it runs. Removing either one stops the saw. | A dock reader. It shows the fobs are present, not the people. |
| c. (a) plus a camera record of each start. | Cameras and footage retention, which have privacy cost. |

**Recommendation: (a)**, then confirm with the insurer in writing before go-live.

## F3. Will the insurer accept a digital sign-off instead of the paper book? (Insurer)

| option | what it forces |
|--------|----------------|
| **a. Digital only.** The trainer and the member both tap their fobs at the desk tablet, and the trainer draws a signature on screen. Record: member, machine, trainer, date, signature image. | One record. Export to PDF for the renewal. Kept for 6 years. |
| b. The paper book stays the legal record and a digital copy feeds the interlocks. | Every induction written twice, and the two can drift apart. The book stays the insurer's source. |

**Recommendation: (a).** Fall back to (b) only if the insurer requires paper.

## F4. Laser tube: count hours, or always keep a spare? (Ines)

| option | what it forces |
|--------|----------------|
| a. Count hours. Use power-on time from the interlock, or better, the laser controller's own "laser on" total if it has one. Order a new tube when the hours left, at the current weekly usage, drop below the supplier's lead time. | A tube-fitted date, the lead time as a named setting, and an alert. It doesn't help when a tube fails early, which is what happened twice this year. |
| **b. Always keep one spare.** When the spare is fitted, order the next one. | No software at all. It also covers early failures. It costs one tube's worth of stock, and glass CO2 tubes slowly lose quality on the shelf. |

**Recommendation: (b), with (a) shown to staff as information** if the
software gives it to us for free. The deciding reason: only (b) survives a tube
that dies early.

## F5. How do we share laser time fairly? (Ines asked us to decide)

| option | what it forces |
|--------|----------------|
| a. A weekly cap (for example, 2 hours). | An unforced number. It blocks people even in quiet weeks when nobody else wants the laser. |
| **b. One upcoming booking per member per machine.** You can book your next slot once your current one has started or finished. There is also a maximum booking length per machine. | One condition and one named setting. Nobody can fill the calendar ahead of time. Free slots stay free to grab. |
| c. A lottery or fair-share priority for popular slots. | A ballot process and ranking logic. Only worth it if (b) isn't enough. |

**Recommendation: (b).** Watch who uses the laser for a month, then decide whether (c) is needed.
Maximum length: **designer choice** of 2 h for the laser, to check with Ines.

## F6. Materials: how do people pay without feeling a meter? (Ines)

| option | what it forces |
|--------|----------------|
| **a. Pay per item taken** (a sheet, an offcut, a spool), recorded by fob at the desk tablet or on your phone, and added to the monthly bill. | A price list of items and one line per item on the bill. No timing. |
| b. Raise the flat fee to include materials. | Nobody pays for what they actually use, which breaks C2. |
| c. Honesty box. | Cash handling, and no record. |

**Recommendation: (a).** Sub-question: is filament sold by the spool, or per print by
rough weight? Also, can the current billing system take extra lines on the monthly bill?

## F7. Should the 3D printers be bookable? (Ines is still thinking)

This doesn't block anything. `bookable` is a setting on Machine, so either answer is a
setting change. **Default (designer choice): not bookable.** If hogging continues,
switch on `bookable` and the same one-upcoming-booking rule from F5 applies.
