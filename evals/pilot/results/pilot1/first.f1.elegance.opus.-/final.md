Hi Dele, thanks for the brief. It's clearer than you think. I've written a first draft of the design and kept my working notes alongside it:

- `design/design.md`: what you need from the system, the design, and what I've deliberately left out
- `design/notes.md`: the questions still open, each with my recommendation, plus a log of our sessions

**The core idea.** One rule handles most of what you described: *a sign-up only counts if the person has whatever the role needs, still valid on the day of the shift.* Sorting and front of house need a food hygiene certificate. The driver needs a licence. The delivery helper needs nothing.

That single rule means:
- Certificates are checked against the shift date, not the day someone signed up. So someone whose certificate runs out in December can't quietly be counted for a January shift.
- The shift lead never checks anything. Their printed sheet only lists people who passed the check.
- The 8am "I need someone with a licence" list comes from the same rule.

**What the system keeps.** Only five things: people, their certificates and licences, roles, how many people each day needs, and who signed up (and whether they came). Everything else is worked out from those. That includes the gap list that replaces your Sunday nights, the printed door sheet, the day-before reminders, certificate expiry warnings, and the quarterly hours by activity.

**If deliveries stop in March,** we delete two rows of setup and nothing else changes. The hours for past deliveries still count in the reports.

**On capping sign-ups,** I'm suggesting a different approach from a per-person cap. The rota would only be open 4 weeks ahead. The printed door sheet only shows those weeks, so paper and online follow the same rule. Nobody has a personal count either, which matters given how you feel about ranking people.

**Things I've assumed for now, which you can change:**
- **Platform:** a Google Sheet with a small script attached. It's free and has no monthly fee.
- **The group chat stays** for news, photos and urgent shouts, but people stop signing up there.
- **Attendance:** volunteers tick a sign-in column on the printed day sheet.
- **Reminders for people without email:** a short daily phone list for now.

**My question for you:** the paper sheet only works if someone types the new names into the system. Who could do that, and how often? I see three options:

- **(a) You, once a week.** This is simple, but some of your Sunday-night work comes back.
- **(b) Whoever locks up after each open day.** It's about five minutes, three times a week, and they'd also type in that day's sign-in ticks. The rota is never more than two days out of date, and you're free of it.
- **(c) Paper volunteers tell you, and you enter it.** This puts the work on your phone instead.

I recommend (b), with you as the backup. Is there someone at the office on Tuesdays, Thursdays and Saturdays who could take that on?