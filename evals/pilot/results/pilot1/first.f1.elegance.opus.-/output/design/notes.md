# Designer notes

Companion to `design.md`. Session log, open forks (ordered by how much each answer settles), and the ledger.

## Session log

- **19 Oct 2026**: read Dele's brief (notes from 3 to 24 Sept). Wrote draft 1. No answers from Dele yet. Meetings: Thursday afternoons suit Dele.

## Open forks

Each fork has a recommendation that draft 1 already assumes, so the design isn't blocked. Each one stays a designer choice until Dele answers.

### F1. How paper sign-ups get into the system. *Settles the most*

C2 and C3 together force paper sign-ups to end up in the same roster as online ones. Without that, Dele is still reconciling two lists on Sunday nights. The certificate rule (C4/C5), reminders (C6) and the hours figures (C9) also only work for people the system knows about. The question is who types them in, and when.

| Option | What it forces |
|---|---|
| a. Dele types them in once a week | Simple, but it brings back some Sunday-night work (C2 only partly met). Paper sign-ups made late in the week aren't checked until then. |
| b. Whoever closes the office types that day's new paper names in (Tue/Thu/Sat), maybe 5 minutes | Roster is never more than 2 days out of date, and Dele is free of it. Needs one willing person per open day, and they'd need access to the sheet. |
| c. Paper volunteers phone or tell Dele, who enters it | Moves the work to Dele's phone. Worst for C2. |

**Recommendation: b**, with Dele as the fallback. The same person collects the day sheet's sign-in ticks (F5), so it's one small task at the end of each open day.

Linked problem: if someone with no valid certificate writes their name in a sorting slot, the system flags it when it's typed in, and Dele (not the lead) contacts them.

### F2. Reminders for people without email

C6 applies to everyone, but texts cost money (C12) and many paper volunteers may not use email.

| Option | What it forces |
|---|---|
| a. Email only; people without email get no reminder | Fails C6 for exactly the people most likely to be on paper. |
| b. The system prints or emails Dele a short "call these people" list each day before an open day | Free. Costs someone a few calls. |
| c. Texts sent from the office mobile, if it has unlimited texts, through a free phone app linked to the sheet | Free if the plan already includes texts. Needs a phone left on and charged at the office. |
| d. A paid SMS service | Monthly or per-message cost; needs the committee (C12). |

**Recommendation: b now; c if the office has a suitable phone.** I need to know: does the food bank have its own mobile?

### F3. The group chat

| Option | What it forces |
|---|---|
| a. Keep the chat for news, photos and urgent shouts; sign-ups only through paper or link | One roster. Needs a clear "sign up here, not in the chat" message, and gentle redirection for a while. |
| b. Keep chat sign-ups too; Dele copies them in | A third channel to reconcile. Undoes C2. |
| c. Close the chat | Loses the urgent-cover channel and the social side people like (C10). |

**Recommendation: a.** The "who could cover" list makes urgent shouts more targeted, but the chat stays.

### F4. Platform

| Option | What it forces |
|---|---|
| a. Google Sheet + Apps Script | Free, no server, data visible as a spreadsheet. Needs a Google account owned by the food bank, not a person. |
| b. Microsoft 365 equivalent (Excel Online + Power Automate) | Only sensible if the food bank already has free charity Microsoft 365. Automation is clumsier. |
| c. A small web app on a free hosting tier | Nicer pages, but free tiers change or disappear, and it needs a programmer to look after it (C16). |
| d. A program on the office laptop only | Nobody can sign up from home, and reminders stop when the laptop is off. |

**Recommendation: a**, unless the food bank already runs on Microsoft 365. I need to know which accounts the food bank already has.

### F5. Recording attendance (for true hours, C14)

| Option | What it forces |
|---|---|
| a. Volunteers tick a sign-in column on the printed day sheet; ticks are typed in with F1 | True figures. Doubles as evidence for the inspector of who worked. |
| b. Assume everyone signed up attended unless marked absent | Less typing, but over-reports hours to the council if no-shows go unmarked. |
| c. The shift lead marks attendance in the system | Puts work back on leads (against the spirit of C5). |

**Recommendation: a.**

### F6. Smaller facts I need

- Start and end times of each shift (sorting, front of house, delivery), for the hours report.
- Is there a maximum for sorting and front of house (space, tasks), or is more always fine?
- Does the delivery helper handle open food? Draft 1 assumes not, so no certificate. If they do, add food hygiene to that role (one line).
- Exactly 1 helper, or "at least 1" if the van has a spare seat?
- Do we need a valid licence only, or also van insurance approval / a minimum age for drivers? Each would be one more qualification kind, with no new mechanism.
- The 4-week booking window: OK, or different?
- The council's quarter dates (calendar quarters or financial year?).
- Under-18 volunteers or anyone with other restrictions? Not mentioned; ignored for now.

## Ledger (draft 1)

**Constraints:** C1–C16 in `design.md` §1 (C13–C16 inferred).

**Forced**
- One roster for all sign-up channels (C2 + C3).
- Eligibility is checked by the system on every sign-up, against the shift date, not the sign-up date (C4 expiry + C5).
- Licence and certificate are the same mechanism, a qualification needed by a role (C4 + C13).
- Driver and helper are separate roles (only the driver needs a licence); `activity` on Role groups them for the grant (C9 + C13).
- Attendance is recorded per sign-up (C14); hours come from need times (C9).
- Delivery is just data (C11).
- No per-person scores, totals or rates on any screen (C8).
- No paid service (C12).

**Designer choices (provisional)**
- Booking window instead of a per-person cap; 4 weeks.
- Personal link instead of passwords.
- Certificate warning fires when expiry falls inside the booking window (reuses the window).
- Weekly gap email to Dele.
- Recommended answers to F1–F5.

**Deleted / not built**
- Per-person sign-up cap (replaced by the window, which also covers paper).
- Separate licence check, separate delivery module.
- Shift-lead accounts.
- No-show tracking/penalties.
- Any gamification.

**Concept count:** 5 record types + closed dates + 1 setting (window). One rule. Everything else is a view.
