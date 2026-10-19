# Rent arrears: dashboard, reminders and late fees

A housing co-operative with about 140 homes collects rent monthly. A volunteer developer is tidying the arrears module, which drives three things: the arrears dashboard the treasurer reviews each week, the friendly reminder letter, and the late-payment charge. Some background from the co-op's records:

**Tenancy agreement, clause 4.3 (same wording in every tenancy):**

> Rent is due on the first day of each month. If any rent remains unpaid seven days after it is due, the Co-operative may add a late-payment charge of 15.00 to the account, once for each unpaid month.

**Email from the treasurer, last spring:**

> Can we please make sure the dashboard and the reminder letters agree about who is behind? At the year-end review the auditor found three households on the dashboard who had never been sent a letter, and asked us why. It looked sloppy. Whatever counts as "behind" on the dashboard should be exactly what triggers a letter.

**Minutes of the September board meeting, item 6 (arrears):**

> Arrears are up slightly on last year. Discussed whether letters go out too late to help. Agreed: from January, trial sending the friendly reminder sooner, after three days, for six months, and compare. Housing officer to report back in July.

**Notes from the developer:**

> Each monthly charge is one row with `due` (a date), `paid`, `reminded` and `fee_charged` flags. The nightly job calls the three functions below and acts on what they return. Everything runs once a day, so dates are enough.

Two candidate implementations follow. Which one is the better design?
