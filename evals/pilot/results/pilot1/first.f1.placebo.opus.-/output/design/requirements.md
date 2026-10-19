# Requirements: volunteer shift rota

Source: Dele's brief (notes dated 3–24 Sept), received 2026-10-19.
Ids are stable. If a requirement changes, mark the old text ~~struck~~ with the date and add the new text. Don't silently overwrite.

## Constraints (things Dele stated, or things that reality forces)

| Id | Constraint | Source |
|----|-----------|--------|
| C1 | Open Tue, Thu, Sat. Each open day has sorting (min 4) and front of house (min 3). Saturday also has a delivery run: exactly 1 driver + 1 helper. | Brief |
| C2 | About 90 volunteers on the books, about 40 active in any month. | Brief |
| C3 | Many volunteers (half are over 70) won't use an app. The paper sheet on the office door stays, and they are not asked to change. | 3 Sept |
| C4 | Nobody works sorting or front of house without a valid food hygiene certificate. Certificates expire 3 years after issue. Drivers don't need one. | 10 Sept, environmental health inspector |
| C5 | Shift leads don't check certificates. Leads change weekly. | 10 Sept |
| C6 | No-shows leave sorting short. A reminder before the shift is wanted. | 12 Sept |
| C7 | Some people book many weeks ahead and then often don't come. Dele asked for a cap, "whatever's sensible". | 12 Sept |
| C8 | No points, badges, "volunteer of the month", leaderboards, or any ranking or scoring of people. Ever. | 17 Sept, firm |
| C9 | The council grant needs total volunteer hours every quarter, split by sorting / front of house / delivery. | 17 Sept |
| C10 | The group chat is used for sign-up, for urgent cover (e.g. the driver drops out at 8am Saturday), and for news and photos, which people like. | 19 Sept |
| C11 | Deliveries may stop after March 2027 when the van lease ends. Not yet decided. | 24 Sept |
| C12 | No monthly fees without committee approval. Equipment: the office laptop and a printer. | 24 Sept |
| C13 | *Inferred:* the driver needs a valid driving licence (and probably approval to drive the van). | "someone with a licence" |
| C14 | *Inferred:* we hold personal data (names, contact details, certificate dates), so UK GDPR applies. Keep it minimal, restrict who can see it. | Reality |
| C15 | *Inferred:* whoever keeps it running is a volunteer, not a developer. | Reality, to confirm (A5) |

## Goal

**The goal:** Dele no longer spends Sunday night working out who is coming and chasing people to fill gaps. Success means Dele can see the gaps for the coming week at a glance, early enough to fill them, without piecing it together from the chat and the door.

## Functional requirements

| Id | Requirement | Priority | From |
|----|-------------|----------|------|
| F1 | Volunteers who use a phone or computer can book and cancel shifts themselves. | Must | Goal, C10 |
| F2 | Volunteers who don't can keep writing their name on a paper sheet on the door. Those names get into the same rota. | Must | C3 |
| F3 | For each upcoming shift, Dele can see how many people are booked against the minimum, and which shifts are short. | Must | Goal, C1 |
| F4 | The rota can't record anyone on sorting or front of house unless their food hygiene certificate is valid **on the date of the shift**. The same goes for the driver role and a driving licence. Leads don't have to check anything. | Must | C4, C5, C13 |
| F5 | Volunteers (and Dele) get a warning well before a certificate expires, so it can be renewed in time. | Must | C4 ("people forget") |
| F6 | People booked on a shift get a reminder in advance, with an easy way to say "I can't come". Cancelling makes the gap show up straight away. | Must | C6 |
| F7 | Bookings made far ahead don't hide gaps that will turn out to be real. (Exact mechanism is fork Q3.) | Should | C7 |
| F8 | Who actually turned up is recorded. The quarterly report gives total hours per activity. | Must | C9 |
| F9 | The system never shows people ranked, scored or compared. Hours appear only as totals per activity, never per person. | Must | C8 |
| F10 | The weekly pattern of shifts is data, not code. Stopping deliveries means removing two rows from it. | Must | C11 |
| F11 | When someone drops out at short notice, Dele can quickly see who could cover. Example: everyone who is licensed to drive and isn't already booked that day, with their phone number. | Could | C10 |

## Non-functional requirements

| Id | Requirement | Priority | From |
|----|-------------|----------|------|
| N1 | Running cost £0 a month. Any cost needs committee sign-off first. | Must | C12 |
| N2 | Volunteers who book online can do it from a phone in a couple of taps. No account or password to remember. | Must | C3, C2 |
| N3 | A non-developer volunteer can run it and fix routine problems. | Must | C15 |
| N4 | Personal data can only be seen by Dele and named coordinators. Volunteers see shift coverage but not other people's contact details or certificates. | Must | C14 |
| N5 | If the system is down on an open day, the printed sheet still works. Paper is always a fallback. | Should | C3, C12 |
