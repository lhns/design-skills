# Risks

| Id | Risk | Likelihood | Impact | Mitigation / how we learn early |
| --- | --- | --- | --- | --- |
| R1 | The insurer does not accept "two inducted members tap to start" as enforcing the two-person rule. | Medium | High: needs presence-checking hardware. | Ask now (Q3), before choosing hardware. |
| R2 | No hosted platform supports a two-person interlock rule or offline caching. | Medium | High | Shortlist against ADR 0001 must-haves; spike on the real saw. Fallback: platform for records and bookings, plus a small dedicated controller for the saw. |
| R3 | Members tap for each other and walk away ("tap and leave"). | Medium | High (safety, insurance) | Saw reader shows both names; session log is reviewable; insurer guidance from Q3. Technology alone cannot fully prevent it. |
| R4 | Internet or service outage on an evening blocks the saw or laser. | Medium | Medium | Offline cache in the interlock controller (NFR2); test by pulling the network cable during the spike. |
| R5 | Back-filling the paper book misses someone, who is then locked out. | Medium | Low–medium | Back-fill before go-live, second-person check, staff can add an induction same day. |
| R6 | The insurer wants wet-ink signatures, keeping the paper book alive. | Low–medium | Low | Design survives it (Q2); the book becomes the signature record only. |
| R7 | Vendor lock-in or vendor shutdown loses six years of induction records. | Low | High | Require export of induction records; keep a yearly export the workshop owns. |
| R8 | The fairness rule doesn't change who gets the laser. | Medium | Low | Measure from the session log after a month; fall back to Q4 option C. |
