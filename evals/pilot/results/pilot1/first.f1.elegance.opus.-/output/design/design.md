# Volunteer shift rota: design

Status: **draft 1** (19 Oct 2026), from Dele's brief. Nothing here has been confirmed by Dele yet.
Open forks and questions are in `notes.md`.

## 1. Constraints

Ids are used throughout. Source: Dele's brief, unless marked *inferred*.

| Id | Constraint | Source |
|---|---|---|
| C1 | Open Tue, Thu, Sat. Each open day: sorting (at least 4), front of house (at least 3). Sat also: delivery run, one driver and one helper. | brief |
| C2 | Main goal: Dele should no longer spend Sunday night working out who is coming and finding people to fill gaps. | 3 Sept |
| C3 | The paper sheet on the office door stays. Volunteers who won't use an app are not made to change. | 3 Sept |
| C4 | Nobody without a valid food hygiene certificate works sorting or front of house. Certificates expire 3 years after issue. Drivers don't need one. | 10 Sept, inspector |
| C5 | The certificate check is not left to shift leads. | 10 Sept |
| C6 | Volunteers get a reminder the day before their shift. | 12 Sept |
| C7 | Limit how far ahead people can book themselves, because long-range sign-ups often turn into no-shows. Dele left the size of the limit to us. | 12 Sept |
| C8 | No points, badges, "volunteer of the month", leaderboards, rankings or scores. Ever. | 17 Sept |
| C9 | Total volunteer hours every quarter, split by activity: sorting, front of house, delivery. | 17 Sept, council grant |
| C10 | The group chat is also used for urgent cover (e.g. driver drops out at 8am), and for news and photos, which people like. | 19 Sept |
| C11 | Home deliveries may stop after March 2027 (van lease ends). Plan for them, but removing them must be cheap. | 24 Sept |
| C12 | No monthly fees without committee approval. Equipment: office laptop and printer. | 24 Sept |
| C13 | The van driver needs a driving licence. | *inferred* ("someone with a licence") |
| C14 | The grant figures must be true hours actually worked, not hours people signed up for. | *inferred* (grant reporting) |
| C15 | Some days the food bank is closed even though it's a Tue/Thu/Sat (Christmas, bank holidays). | *inferred* |
| C16 | Whoever looks after this after the build is not a programmer. | *inferred* (volunteer organisation, no budget) |

## 2. The shared concept

Most of the constraints are cases of one sentence:

> **A sign-up counts toward cover only if the person holds every qualification the role needs, valid on the date of the shift.**

- C4 (hygiene certificate for sorting and front of house) is that rule with `role → food hygiene`.
- C13 (licence for the driver) is the same rule with `driver → driving licence`. A licence is not a separate mechanism.
- "Drivers don't need a certificate" (C4) is just the driver role not listing food hygiene.
- Expiry (C4) is the "valid on the date of the shift" part. Someone who signs up in October for a January shift, with a certificate that runs out in December, is caught. A check done only when they signed up would miss them.
- C5 holds because the system applies the rule to every sign-up, paper and online. The shift lead is never asked to judge a certificate.

**Invariant:** the cover figures, the gap list, the printed day sheet and the "who could cover" list all use this one rule. No screen or printout counts a person the rule rejects.

## 3. Data model (the whole core)

Five kinds of record. Everything else is derived from them.

| Record | Fields | Forced by |
|---|---|---|
| **Person** | name, phone, email (optional), personal sign-up link | C2, C6 |
| **Qualification held** | person, kind (`food hygiene` / `driving licence`), expires on | C4, C13 |
| **Role** | name, activity (`sorting` / `front of house` / `delivery`), qualifications needed | C1, C4, C9, C13 |
| **Need** | weekday, role, minimum, maximum, start time, end time | C1, C9 (hours need times) |
| **Sign-up** | person, date, role, attended (yes / no / not yet recorded) | C2, C9, C14 |

Plus one list: **closed dates** (C15).

The starting data, in full:

```
Roles
  sorter            activity sorting         needs food hygiene
  front of house    activity front of house  needs food hygiene
  driver            activity delivery        needs driving licence
  delivery helper   activity delivery        needs nothing

Needs          (times and the sorting/front maxima to be confirmed by Dele)
  Tue sorter 4+     Tue front of house 3+
  Thu sorter 4+     Thu front of house 3+
  Sat sorter 4+     Sat front of house 3+
  Sat driver exactly 1     Sat delivery helper exactly 1
```

**C11 test (deliveries end in March):** delete the two Saturday delivery rows from Needs. No code changes. Past delivery sign-ups stay, so the quarterly reports still add up. The core has no idea that delivery is special, because it isn't: it's two rows.

**Why driver and helper are two roles, not one "delivery" role with 2 places:** only the driver needs a licence (C13), and the qualification rule hangs on the role. The `activity` field then puts both back together for the grant (C9).

## 4. What is derived (no new records)

Each of these is a view over the five records. None of them stores anything.

| Output | What it is | Meets |
|---|---|---|
| **Rota / gap view** | For each open date in the window: each need, the people counted toward it, and how many short. Sign-ups the rule rejects are shown to Dele as problems, not counted. | C2, C4, C5 |
| **Weekly gap email to Dele** | The same view for the coming week, sent automatically. This replaces Sunday night. | C2 |
| **"Who could cover"** | For a date and role: people who are qualified for it and not already working that day, with phone numbers. Dele uses it to message the right people directly, or posts in the group chat as now. | C2, C10 |
| **Printed door sheet** | The rota for the open window, with names already signed up and blank lines for the places left. A blank line on the sorting and front-of-house columns says "food hygiene certificate needed". | C3, C7 |
| **Printed day sheet** | For the shift lead: who is coming, and a sign-in column. It lists only people the rule accepts, so the lead's only job is "is your name on the sheet". | C5, C14 |
| **Day-before reminder** | One message to each person signed up for tomorrow. | C6 |
| **Certificate running out** | A message to the person (copy to Dele) when their certificate expires before the end of the open window, i.e. before a shift they could book. | C4 ("people forget") |
| **Quarterly hours** | Sum over attended sign-ups in the quarter of (end − start), grouped by the role's activity. | C9, C14 |

### The one number: the booking window

C7 forces a limit but not its size. Rather than a per-person cap, the rota is **open a fixed number of weeks ahead**; you can't sign up for a date beyond it. Reason for this shape:

- It treats paper and online alike. The door sheet only has dates inside the window printed on it, so paper gets the same limit with no extra rule (C3).
- The certificate warning reuses it: "expires before the window ends" means "expires before a shift you could already book".
- Nobody has a personal count to track or be compared on (C8).

Proposed value: **4 weeks** (designer choice). Reason: long enough that regulars can plan a month, short enough that "every Saturday till Christmas" is impossible. Dele can change it; it is one setting.

## 5. Channels

| Channel | Used for |
|---|---|
| **Paper sheet on the door** | Signing up, for anyone who prefers it (C3). It's printed from the system. Someone types the new names in (see notes, fork F1). |
| **Personal link** | Signing up and cancelling online. Each volunteer gets their own link, so there's no password. The page only offers roles they're qualified for, in dates inside the window. |
| **Group chat** | Stays, for news, photos and urgent shouts (C10). It stops being a place to sign up. Fork F3. |
| **Email** | Reminders and certificate warnings to people who have email. People without email: see fork F2. |

## 6. Platform (designer choice, see fork F4)

**Recommendation:** a Google Sheet as the data store (one tab per record type), with a small Google Apps Script attached for the sign-up pages, emails and printouts.

- Free with an ordinary Google account; no server and no monthly fee (C12).
- Dele can see and correct every record in a spreadsheet, and anyone who can use a spreadsheet can look after it (C16).
- The free email allowance (about 100 recipients a day) is far more than the roughly 10 to 15 reminders on a busy day.
- Prints from the office laptop.

The rule in §2 is checked on online sign-ups and whenever any view is built, so typing a paper name straight into the sheet can't get round it.

## 7. Deliberately left out

| Left out | Why |
|---|---|
| Points, badges, streaks, per-person hour totals or attendance rates on any screen | C8. Attendance is recorded only to produce the grant totals by activity. |
| A no-show tracker or penalties | Not asked for; would edge toward scoring people (C8). The window (C7) and reminders (C6) address no-shows. |
| Shift-lead role in the system | Leads rotate weekly and must not be relied on (C5). They get a printed sheet. |
| Replacing the group chat | People like it and it does things a rota shouldn't (C10). |
| A special "delivery" module | C11. Delivery is two rows in Needs. |
| A separate licence-check feature | Same rule as certificates (§2). |
