# Constraints and requirements

Source is Gwen's brief (2026-10-19) unless marked *inferred*. Constraints are the facts the design has to satisfy. Anything I've decided myself lives in design.md as a designer choice.

## Constraints

| Id | Constraint | Source |
| --- | --- | --- |
| C1 | All volunteers. Nobody is employed and there is no money to pay anyone. | brief |
| C2 | Amplified music must stop by 23:00, "not a minute after" (premises licence). | brief |
| C3 | The committee must be able to **show** that C2 is enforced. Controls that rely on the hirer (e.g. a clause in the hire agreement) don't count. A further breach is likely to trigger a licence review. | licensing officer's email |
| C4 | No volunteer goes to the hall at night or is on call at night, on site or from home. | brief (agreed when Gwen took the diary) |
| C5 | Keys stay as they are: collected from the shop and returned through the shop's letterbox. | brief: "don't fix what isn't broken" |
| C6 | No deposits. Holding back money over the state of the hall caused a public row in 2023. | brief |
| C7 | Prices: upstairs room £12/h, main hall £25/h, £30/h on Saturday nights. | brief |
| C8 | Two bookings must never overlap in the same room. | brief (double-booked Saturdays) |
| C9 | People can see which dates are free without asking Gwen. | brief |
| C10 | Hirers stop ringing Gwen at home. She is available Monday and Wednesday mornings. | brief |
| C11 | The lunch club and whist drive organisers (in their 80s, no email) must still be able to book extra dates, by phone or in person. | brief |
| C12 | Gwen is away January to March 2027. Whatever we build has to be running before then and keep running without her. | brief |
| C13 | Unpaid "pencilled" dates must not block other hirers indefinitely. | brief (two weddings turned away for a date that ended up empty) |
| C14 | The money owed for a booking is collected without anyone chasing it. | brief (three June cheques still outstanding) |
| C15 | Families can get a Saturday for one-off events. At the moment regular bookings crowd them out until spring. | brief |
| C16 | The kitchen is left clean and with no rubbish, so the next user (e.g. Tuesday lunch club) isn't affected. | brief (prawn shells) |
| C17 | The upstairs room may be let full-time to the playgroup next year (committee hasn't decided). | brief |
| C18 | Saturday-night parties with a disco are the main income for the roof fund. They must stay possible. | brief |
| C19 | Running costs must be close to zero. *inferred from C1* | inferred |

Existing regular hirers: lunch club (Tuesdays), whist drive (Thursday evenings), Pilates (twice a week; now asking for Saturday afternoons too), dance school (every Saturday morning since 2022).

## Functional requirements

| Id | Requirement | Priority | From |
| --- | --- | --- | --- |
| F1 | One calendar holds every booking for every room, and it refuses any booking that overlaps an existing one. | must | C8 |
| F2 | Anyone can see free and booked times for each room online, without hirers' names. | must | C9 |
| F3 | A one-off hirer can ask for a date online and pay without speaking to anyone. | must | C10, C14 |
| F4 | A request that isn't paid within the hold period lapses by itself and the date shows as free again. | must | C13 |
| F5 | Regular hirers have a standing series of bookings. Their extra dates can be added by a volunteer after a phone call or a note. | must | C11 |
| F6 | The price is worked out from the room, day and hours. Nobody quotes it by hand. | should | C7, C14 |
| F7 | Mains power to every socket that amplified equipment can use in the main hall is cut at 23:00 by a time switch, with no person involved, and each check of it is recorded. | must | C2, C3, C4 |
| F8 | Every hirer is told, before paying, that the power cuts at 23:00 and that they must take their rubbish away with them. | must | C2, C16 |
| F9 | Phone calls go to a hall number, not Gwen's home. They're answered by voicemail and dealt with during volunteer hours. | must | C10, C11 |
| F10 | The rule for regular bookings on Saturday afternoons and evenings is enforced when a series is set up. | should | C15, C18 |
| F11 | A room can be taken out of letting, or let as a block, without changing the system. | could | C17 |

## Non-functional requirements

| Id | Requirement | From |
| --- | --- | --- |
| N1 | Running cost of no more than a few pounds a month. The committee confirms the ceiling (Q4). | C19 |
| N2 | A volunteer can run it after an hour's handover. No technical skills needed. | C1, C12 |
| N3 | Keeps working for three months with nobody checking it more than once a week. | C12 |
| N4 | The licensing evidence (switch setting and check log) can be shown to the licensing officer whenever asked. | C3 |
