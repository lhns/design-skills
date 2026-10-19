# Open questions and forks

The questions are ordered by how much of the design each answer settles. Each one lists the options, what each option forces, and my recommendation. Where I've gone ahead without an answer, the recommendation is marked **designer choice (provisional)**. A designer choice is my suggestion and can still change. It only becomes settled when Dele decides it.

## Q1. How do paper bookings get into the rota? Who types them in, and when? (Owner: Dele)

This is where C3 (paper stays), C4/C5 (certificate rule, not checked by leads) and the goal (Dele's Sunday night) meet.

| Option | Forces |
|--------|--------|
| A. Dele types the sheet in once a week | The gap view is only correct once a week, and the work stays on Dele. A certificate problem is found days after the person signed. |
| B. Whoever is in the office types in new names at the end of each open day (Tue/Thu/Sat), then reprints the door sheet | The gap view is never more than 2–3 days out of date. Certificate problems are caught while the volunteer may still be in the building. Needs a named person each day. |
| C. Volunteers using paper tell someone at the desk, who books them in on the spot | Correct straight away, but it changes what paper volunteers do. That conflicts with C3. |

**Recommendation: B.** It leaves paper volunteers' routine untouched and keeps the work off Dele. It does depend on someone being in the office on open days (A1).

## Q2. Platform (Owner: Dele + committee if any cost)

| Option | Forces |
|--------|--------|
| A. Shared spreadsheet + form + small script (Google Workspace or Microsoft 365, both free for registered charities) | £0. A volunteer who knows spreadsheets can look after it. The certificate check and reminders run as a script, which is less robust. |
| B. Small purpose-built web app on free hosting | Enforces the rules properly. Needs someone technical to keep it running, and free hosting offers can change. |
| C. Off-the-shelf volunteer rota service | Usually has a monthly fee (C12). Rarely enforces certificates. Some include points or badges (C8). |
| D. Program on the office laptop only | No online booking (F1 fails). The laptop becomes a single point of failure. |

**Recommendation: A, as a designer choice (provisional).** It's the only option that meets both N1 (£0) and N3 (a non-developer can run it). B is next if A turns out too fragile. This depends on A4 and A5, so I'll ask about it after Q1.

## Q3. Bookings made far ahead (C7) (Owner: Dele)

The harm isn't the number of bookings. It's that a booking that won't happen makes a shift *look* covered.

| Option | Forces |
|--------|--------|
| A. Cap: at most N future bookings per person | Needs an arbitrary N. Also limits reliable people. |
| B. Bookings open only for the weeks shown on the printed door sheet | The limit follows the sheet that already exists, so it isn't a new number. Paper and online stay the same. |
| C. Reminder with "can't come", and nothing else (F6) | No new rule. Relies on people answering. |

**Recommendation: C now, plus B if it's still a problem after a month.** This counts as a designer choice until Dele decides. It is deliberately not a per-person no-show count, which would edge towards scoring (C8).

## Q4. Does the delivery helper need a food hygiene certificate? (Owner: Dele / inspector)

Parcels are presumably sealed, but I don't know. The answer changes one row in the role table and nothing else.

## Q5. Is there a maximum per shift for sorting and front of house? (Owner: Dele)

Space in the warehouse, or too many people standing around. If there's no maximum, a booking never blocks anyone else.

## Q6. Reminders for paper-only volunteers (Owner: Dele)

Email is free. Text messages cost a few pence each, which is no monthly fee but still a cost (C12). A phone call puts the work back on Dele. Do the over-70s mostly have a mobile that gets texts?

## Q7. Shift times (Owner: Dele)

Start and end times for each role on each day. These are needed for the hours report (C9).

## Q8. How far ahead should the reminder go? (Owner: Dele)

Dele said "the day before". A Saturday dropout found on Friday evening is hard to fill. Two days ahead gives more time to find cover. Designer choice for now: **2 days**, kept as one named setting.

## Q9. Does the grant need anything beyond total hours per activity? (Owner: Dele)

For example, the number of distinct volunteers, or hours per person. If it needs hours per person, that touches C8, and Dele and I would need to talk it through.
