# Candidate B is the better design

**Deciding reason:** "when to remind" and "when a fee may be charged" are different facts with different owners, so they must be separate values. Candidate A merges them into one, and that breaks the tenancy agreement the first time the board's reminder timing changes.

## Constraints

- **C1 (tenancy agreement, clause 4.3):** a late fee may be added only once rent is unpaid 7 days after its due date, at most once per unpaid month. It is contractual and the same in every tenancy.
- **C2 (treasurer's email):** "behind" on the dashboard must be exactly what triggers a reminder letter.
- **C3 (board minutes):** the reminder timing is a board policy that changes. From January it was trialled at 3 days for six months, with a report in July. Today is October 2026, so whether it stayed at 3, went back to 7, or became something else is an open question for the board. Either way, the board can change it without changing the contract.
- **C4 (inferred):** never charge the same month's fee twice. Both candidates meet this with `fee_charged`.

## Trying to break each design

**Candidate A** has one `OVERDUE_AFTER`, documented as clause 4.3, that drives all three outputs.
- It meets C2: the dashboard and reminders share `is_overdue`.
- Now carry out the board's decision (C3) by setting the value to 3 days. Rent due on 1 March and unpaid on 4 March is charged 15.00 on day 3. That breaks C1, a contractual limit, on every tenancy.
- The other route also fails. Leave the value at 7 and the reminder trial can't be run at all, so C3 is unmet.
- The comment makes this worse: it tells the next developer the value belongs to the contract, while the reminders silently depend on it too.
- The two lists share a number by coincidence, not because they are the same fact. Merging them is false elegance: it is simpler only because C3 was dropped.

**Candidate B** has `REMINDER_AFTER` for the dashboard and reminders, and `LATE_FEE_AFTER` for fees.
- It meets C2: the dashboard and reminders still share one predicate. Moving the reminder threshold moves both together, which is exactly what the treasurer asked for.
- It meets C1: the fee threshold stays tied to clause 4.3 whatever the board decides about reminders.
- It meets C3: the trial, its reversal, or any later policy is a one-line change that touches only one concept.
- I can find no input or policy change that breaks a constraint here.

## Weighing what's left

- **Concept count:** Candidate B has one more named value and one more predicate. Both are forced by C1 and C3 together, so the rise is justified.
- **Blast radius:** a change to reminder policy touches one concept in Candidate B. In Candidate A it touches the legal fee rule as well.

## Small fixes for Candidate B

- Give `REMINDER_AFTER` a comment naming its source, as `LATE_FEE_AFTER` has. For example: "board policy; trialled at 3 days Jan–Jun, see Sept minutes item 6." That lets the next reader see that it is meant to be changeable.
- Its current value should reflect what the board decided after the July report. The developer should confirm that rather than assume 7.
- `is_overdue` could be renamed to something like `is_in_arrears`. "Overdue" echoes the fee's 7-day wording, and the name could tempt someone to reuse it for fees.

## Ledger

- **Constraints:** C1 contractual fee threshold; C2 dashboard equals reminder trigger; C3 board-controlled reminder timing; C4 one fee per month (inferred).
- **Forced decisions:**
  - Two thresholds, because C1 and C3 belong to independent owners.
  - One shared predicate for the dashboard and reminders (C2).
- **Designer choices:** the current value of `REMINDER_AFTER` depends on the July outcome and should be confirmed.
- **Deletions:** none. Candidate A's single threshold is not a valid simplification.

WINNER: 2