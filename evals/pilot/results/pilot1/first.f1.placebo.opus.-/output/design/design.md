# Design: volunteer shift rota (DRAFT v0.1, not reviewed)

Status: first draft, written straight from the brief. Not yet agreed with Dele.
Requirements and constraint ids (C1…, F1…, N1…) are in [requirements.md](requirements.md).

## 1. Overview

Right now, bookings are spread across the group chat, the paper sheet on the door and Dele's head. The design brings them into **one rota**. Two kinds of people feed it:

- volunteers who book online, and
- whoever types in the paper sheet.

Several things come out of it, all derived from that one rota:

- the gap view
- the printed sheets
- reminders
- certificate warnings
- the quarterly hours report

**Non-goals:**

- replacing the group chat's social role (news, photos)
- any recognition, points or ranking (C8)
- payroll-style timesheets
- managing the parcels or clients themselves

## 2. Core concepts

The table below lists every concept, the constraint that forces it, and what breaks without it.

| Concept | What it is | Forced by | Without it |
|---------|-----------|-----------|------------|
| **Volunteer** | Name, how to contact them (phone and/or email), and whether they book online or on paper | Goal, C3 | Nobody to book |
| **Qualification** | A kind (food hygiene, driving licence) plus an expiry date, held by a volunteer | C4, C13 | Can't enforce certificates |
| **Role** | Sorting, front of house, driver or delivery helper. Each role has an *activity* (for the report) and the qualifications it requires | C1, C4, C9, C13 | Can't say who may do what, or split hours |
| **Shift** | A date, a role, start and end times, and the minimum and maximum number of people | C1, C9 | Nothing to book |
| **Booking** | A volunteer on a shift. Its state is *booked*, *cancelled*, *attended* or *no-show* | Goal, C6, C9 | No rota, no hours |
| **Weekly pattern** | Rows of (weekday, role, times, min, max) used to generate shifts | C1, C11 | Shifts set up by hand every week; stopping deliveries would need a code change |

Required qualifications per role are a small table. It's data, not code:

| Role | Activity | Requires | Min | Max |
|------|----------|----------|-----|-----|
| Sorting | Sorting | Food hygiene | 4 | ? (Q5) |
| Front of house | Front of house | Food hygiene | 3 | ? (Q5) |
| Driver | Delivery | Driving licence | 1 | 1 |
| Delivery helper | Delivery | ? (Q4) | 1 | 1 |

Everything else is **derived** from these concepts. Nothing is stored twice:

- **Gap view (F3):** future shifts where the number of *booked* people is below the minimum.
- **Reminders (F6):** *booked* bookings whose shift starts within the reminder lead time.
- **Certificate warnings (F5):** qualifications that expire within the renewal lead time.
- **Hours report (F8):** the sum of (end − start) over *attended* bookings, grouped by activity and quarter.
- **Cover list (F11):** volunteers who are qualified for the role and have no booking that day.
- **Printouts:**
  - The **door sheet**, one per week. It shows each shift, the names already booked, and blank lines.
  - The **lead's sheet**, one per shift. It shows the names booked, with a tick box for attendance.

## 3. The invariant

> No booking in state *booked* or *attended* exists for a role unless the volunteer holds every qualification that role requires, **valid on the shift date**.

The check uses the shift date, not today. That means a certificate that will have expired by the shift is refused when the booking is made. This rule also covers bookings made months ahead. If a certificate record is corrected later, any bookings it affects are flagged to Dele.

Only one place in the system can create a booking. Online booking and typing in the paper sheet both go through it, so both are checked the same way. Leads never check anything (C5): the lead's sheet only lists people who passed. A lead's only rule is: *"if you're not on the sheet for sorting or front of house, see Dele before you start."*

## 4. Key flows

**Booking online (F1).** The volunteer opens a personal link. They see upcoming shifts for the roles they're qualified for, and tap one to book. Nothing appears that they would be refused for.

**Booking on paper (F2, C3).** Volunteers write their name on the door sheet as they do now. Someone types those names into the rota (who, and when, is **Q1**). If the system refuses an entry because a certificate is missing or expired, the person typing it in tells the volunteer. Then a fresh sheet is printed. Volunteers using paper change nothing.

**Reminder and cancel (F6, C6).** A reminder goes to each booked volunteer ahead of the shift. Online volunteers can cancel in one tap. The gap view updates immediately, and Dele hears about any shift that drops below its minimum. For paper-only volunteers with no phone or email on file, the reminder channel is an open question (Q6).

**Certificate expiry (F5, C4).** The volunteer and Dele are warned well before the expiry date. Renewal means entering a new expiry date. The rule in section 3 then lets that volunteer book again.

**Attendance and hours (F8, C9).** The lead ticks names on the lead's sheet and writes in anyone who turned up unbooked. The sheet goes back to the office and is typed in. A walk-in on sorting or front of house goes through the same qualification check as any booking. The quarterly report is a single query.

**Driver drops out (F11, C10).** Dele opens the cover list for "Driver, today". It shows everyone with a valid licence who isn't booked that day, with their phone numbers. Dele calls them or posts in the chat. The system doesn't try to replace the chat's urgency.

## 5. The group chat (C10)

The chat currently does three separate jobs, so each is decided separately (see [ADR 0001](adr/0001-group-chat-keeps-news-and-urgent-cover.md), proposed):

- **Booking:** moves to the rota. A booking made only in the chat doesn't count.
- **Urgent cover:** stays in the chat. The cover list helps Dele know who to ask.
- **News and photos:** stays in the chat. People like it, and it isn't a rota problem.

## 6. Cross-cutting concerns

- **No ranking (C8, F9).** The system has no per-person totals screen. It shows no attendance rate and no "most shifts". *No-show* exists as a booking state only so that hours are correct. It is never summed per person. If someone later asks for this feature, the answer is in C8.
- **Privacy (C14, N4).** We store the minimum: name, contact details, qualification kind and expiry date, and bookings. We don't store dates of birth or certificate scans. Only coordinators see contact details.
- **Cost (C12, N1).** £0 a month. The platform choice is fork Q2.
- **Resilience (N5).** The printed sheets are the fallback. If the system is down, the paper keeps working and gets typed in later.

## 7. Alternatives considered

- **A cap of N future bookings per person (C7).** Not recommended as the first move. N would be an arbitrary number. A cap also punishes the reliable people who book ahead, and it doesn't fix the real harm: a booking that hides a gap. See Q3.
- **Drop paper and make everyone use the app.** Ruled out by C3.
- **Leads check certificates at the door.** Ruled out by C5.

## 8. Testing and rollout (outline)

1. Enter the volunteer list and certificate dates. This alone gives a list of expired or expiring certificates, which is useful straight away.
2. Run for one month alongside the current way, with paper as the source of truth. Compare the gap view with what actually happened.
3. Switch booking out of the chat. Keep paper.
4. After the first quarter, compare the hours report with Dele's hand count.

Rollback: paper and the chat never stop working, so stopping the system loses nothing.

## 9. Open questions, risks and assumptions

See [open-questions.md](open-questions.md), [assumptions.md](assumptions.md) and [risks.md](risks.md).

## 10. Milestones (rough)

1. Volunteer and qualification register, plus expiry warnings. This removes the inspection risk first.
2. Weekly pattern, shifts, bookings, the gap view and printed sheets.
3. Online booking and reminders.
4. Attendance and the quarterly hours report. This must be ready before the first grant report after launch.
5. Cover list.
