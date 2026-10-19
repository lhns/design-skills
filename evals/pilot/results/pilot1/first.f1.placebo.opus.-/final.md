Thanks, Dele. Your notes were clear enough to write a first draft of the design. It's all in `design/`, and `design/README.md` lists what's in each file. Nothing is decided yet: every recommendation below is my suggestion until you agree to it.

## The design in brief

**One shared rota is the only record of who's coming.** People get into it in two ways:
- **Online:** volunteers who are happy to use a phone book through a personal link, with no password.
- **Paper:** everyone else keeps writing their name on the sheet on the door, exactly as now. Someone types those names into the rota.

Everything you need comes out of that one rota:
- a view of which shifts are short this week
- a printed sheet for the door
- a printed sheet for the shift lead, with tick boxes for who turned up
- reminders before each shift
- warnings before a certificate runs out
- the quarterly hours report, split by sorting, front of house and delivery

**Certificates are checked by the system, not the leads.** No one can be booked onto sorting or front of house unless their food hygiene certificate is still valid on the day of the shift. That's checked when the booking is made, so it also covers bookings months ahead. The same rule applies to the driver and a driving licence. Leads only work from their printed list, which already contains only people who passed the check.

**Deliveries are easy to drop.** If deliveries stop after March, you remove two rows from the weekly pattern. Nothing needs rebuilding.

**No ranking, ever.** There are no per-person totals and no attendance rates. Hours are only ever added up by activity.

**The group chat stays, but stops being where people book.** It keeps the news, the photos and the 8am "I need a driver now" appeals. For those appeals, you'll get a list of who could cover: for example, everyone with a licence who isn't already booked that day. That suggestion is written up as decision record 0001, waiting for your yes or no.

**On capping bookings:** I suggest not starting with a fixed limit like "no more than four". The real problem is that a booking someone won't keep makes a shift look covered when it isn't. So I'd start with a reminder that has a one-tap "I can't come". If that isn't enough after a month, bookings would only open for the weeks shown on the door sheet.

**What it runs on:** I lean towards a shared spreadsheet with a simple form, using the free Google or Microsoft accounts charities can get. That would cost nothing a month and wouldn't need a programmer to look after it. I'd like to talk this through with you before settling it.

## Open questions

These are in `design/open-questions.md`, with options and my recommendation for each:
- Does the delivery helper need a food hygiene certificate?
- Is there a maximum number of people for sorting or front of house?
- What are the start and end times of each shift? I need them for the hours report.
- How should we remind volunteers who only use paper?
- Is "the day before" early enough for reminders? A Saturday dropout found on Friday evening is hard to fill, so I've pencilled in two days.

## My question for you

**When someone writes their name on the door sheet, who could type it into the rota, and how soon?**

- **(a)** You, once a week. This keeps the work on your Sunday nights, and a certificate problem might only come to light days later.
- **(b)** Whoever is in the office types in new names at the end of each Tuesday, Thursday and Saturday, then prints a fresh sheet. This is what I'd recommend.
- **(c)** Paper volunteers ask someone at the desk to book them in. This would change their routine, which you've said you don't want.

The answer matters because it decides three things: how soon a missing certificate is noticed, how up to date your view of the gaps is, and whether the chasing actually comes off your plate. If (b) suits you, is there someone in the office on each open day who could do it?