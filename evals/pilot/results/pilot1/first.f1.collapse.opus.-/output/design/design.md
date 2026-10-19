# Volunteer shifts: design (round 1, 2026-10-19)

This is the current suggested design. Every choice marked *(F n)* is provisional and waits on Dele; K/X/W ids are Dele's own words (`kernel.yaml`, quoted in `vision.md`). Open questions are in `forks.yaml`, concepts in `concepts.yaml`.

## The idea in one line
**One list of who is coming to which shift (the register), and everything else is a view of it.** The door sheet is printed from the list, gaps are counted from it, reminders and certificate checks run off it, and the grant hours are added up from it. Sunday night stops being detective work (K7) because there is only one place to look.

## What's in the register
| Part | What it is | Why it exists |
| --- | --- | --- |
| Volunteer | name, phone/email, how they get reminders *(F7)* | K5, K6 |
| Qualification | food hygiene certificate date (expiry = date + 3 years); driving licence *(F6)* | K10, K11, K12, K17 |
| Role table | one row per role: activity, day, minimum, qualification needed, hours *(F12)* | K1-K4, K10, K12, K16, K18 |
| Commitment | one row per person per shift role; marked when they arrive *(F10)* | K7, K14, K16 |

The role table today:

| Activity | Days | Minimum | Needs |
| --- | --- | --- | --- |
| Sorting | Tue, Thu, Sat | 4 | food hygiene certificate (K10) |
| Front of house | Tue, Thu, Sat | 3 | food hygiene certificate (K10) |
| Delivery driver | Sat | 1 | licence, no certificate (K12, *F6*) |
| Delivery helper | Sat | 1 | nothing *(F5, assumed)* |

If the van goes after March (K18), the two delivery rows are deleted and nothing else changes; past delivery hours stay in the reports.

**Rule that always holds:** nobody holds a sorting or front-of-house place on a date after their certificate has run out (K10, K11). The register checks this, not the shift lead (K13, F4 — forced: leads are ruled out by K13, self-declaration by K11).

## How it is used
- **Signing up.** People who like phones use a free online form *(F2)*; the form refuses a food role if the certificate will have run out by that date. Everyone else ticks the door sheet (K9).
- **The door sheet** *(F3)* is printed from the register for each period *(F9: two weeks)*: names down the side, a box per shift, boxes greyed where that person can't do that role on that date. Tick to sign up; initial your box on the day when you arrive *(F10)*. Blank rows at the bottom for new people. Online sign-ups appear on the next print.
- **Cap on long sign-ups** *(F8)*: you can only sign up for shifts on the current sheet. "Every Saturday till Christmas" (K15) can't happen; regulars just tick again each fortnight. No one's record is counted or held against them (X2).
- **Evening run** *(F11)*, Monday, Wednesday and Friday evenings, by Dele or a helper, about 10 minutes: type new ticks and yesterday's initials; the register shows tomorrow's gaps and any certificate problems; reminders go (email automatically, a short list of people to text or ring *(F7)*). Gaps get chased then, not all on Sunday.
- **8am driver dropout** *(F15)*: shout in the chat as now; the register also gives a list of licensed volunteers' phone numbers.
- **Group chat** *(F14)*: stays for news, photos and emergencies (W2); sign-ups move to the form or the sheet.
- **Grant hours** (K16): hours present, by activity, for any date range, so it works whatever the council's quarters are. Totals only, never per person *(F17; X1, X2)*.
- **Certificate renewals** *(F16)*: the register lists people whose certificate ends within a lead time and tells them, so they can renew before they lose their boxes.

## Tool *(F13)*
A free Google account for the food bank: Google Sheets is the register, Google Forms is the sign-up form, a small script sends the email reminders and prints the grid. No monthly fee (K20); runs on the office laptop and printer (K19). If Dele chooses office-only entry *(F2)*, a spreadsheet on the laptop alone is enough.

## Walk-throughs
- *Certificate runs out mid-fortnight.* Expiry 15 Nov; sheet for 10-23 Nov greys that person's food boxes from 15 Nov on. They can still drive or help on the van.
- *Signs up twice* (form and sheet). Same person, same shift, same role: one row; no double count.
- *Ticks the sheet Monday afternoon for Tuesday sorting.* Monday's evening run picks it up, the reminder goes, the gap count is right.
- *No-show.* No initials, so no hours counted (K16 stays honest). The gap was visible the night before only if they cancelled; reminders (W1) are the defence. Nobody is marked down (X2).
- *Writes their name in a greyed box anyway, on the morning.* The evening run already happened, so this is caught afterwards, not before. **This is a real limit:** with paper (K9) and no lead checking (K13), a same-day write-in can only be flagged after the fact. The greyed box is the guard. Dele should know this.
- *Van lease ends in March.* Delete two role rows. Nothing else moves.

## Assumptions I'm working on (not yet Dele's words)
A1 one list beats nightly reconciliation; A2 enough volunteers would use a phone form; A3 the laptop has internet; A4 a printed grid still counts as "the paper sheet"; A5 delivery parcels are closed, so the helper needs no certificate; A6 any licensed volunteer may drive the van; A7 paper users can be texted or rung; A8 the Christmas problem is booking far ahead; A9 two weeks is the right sheet length; A10 grant hours mean hours actually worked; A11 someone can see the sheet the evening before each opening day; A12 shifts have fixed times; A13 renewing a certificate takes some weeks.

## Open questions (one per meeting, in order)
1. **F2** who types sign-ups in (asked 2026-10-19).
2. F3 printed grid OK in place of the blank sheet? / F11 who can do the evening run?
3. F12 shift times (needed for hours); F5 van helper and certificates; F6 who may drive.
4. The rest (F7-F9, F13-F18) mostly follow from those or can wait.

## Ledger
- **Constraints:** K1-K20, X1-X2, W1-W2 (Dele's words).
- **Forced:** certificate check done by the register (F4: K13 rules out leads, K11 rules out self-declaration); one list rather than merged sources (F1 option "several sources" ruled out by K7); not everyone online (K9); no limit based on no-shows (X2); no per-person totals on show (X1, X2).
- **My choices, waiting on Dele:** F1-F3, F5-F18 as listed above.
- **Deleted / not built:** any points, badges, rankings or reliability scores (X1, X2); delivery-specific logic beyond two table rows (K18).
- **Counts, round 1:** 15 concepts (7 forced, 8 hang on open forks), 1 exception (paper can be flagged, not refused, forced by K9), 0 unforced numbers.
