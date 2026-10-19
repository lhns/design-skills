# Grant spend report by reporting line

A small charity runs youth programmes funded mainly by one grant-making trust. Staff tag every expense with an internal budget code. Each quarter the charity sends the trust a spend report: totals per *reporting line*, the trust's own categories. A mapping says which reporting line each budget code belongs to. The report used to be built in a spreadsheet; it is moving into the charity's small finance app, and two candidate designs for the mapping and the report are below.

**Ticket FIN-31 (opened by the finance officer, Rhea):**

> The quarterly spend report should come straight out of the finance app so nobody retypes numbers. The trust's template has one row per reporting line. Codes and lines are listed on the shared drive. I'm the only one who edits the mapping, a handful of times a year: new codes when we start a project, or when the trust changes its lines.

**Comments on FIN-31:**

> **Rhea:** Heads-up for the design: the trust is folding "Volunteer expenses" into "Programme delivery" from the grant year starting 1 April. I'll move VOL-TRAVEL and VOL-SUBS across when we get there.
>
> **Jonas (developer):** Is there any reason to keep old versions of the mapping? I'd rather not build history nobody uses.
>
> **Rhea:** Not that I know of. We never resubmit old reports. Once a quarter's report is sent it's done.
>
> **Rhea:** Unrelated, but so it's written down somewhere: the annual audit is in June. Same as last year, the auditor picks two of the previous year's quarterly reports, runs them again from our system, and ticks them off line by line against the PDFs we sent the trust.

Expenses are never deleted; corrections are posted as new expense rows. Amounts are Decimal. The finance app is single-user and small (a few thousand expenses a year).

Two candidate implementations follow. Which one is the better design?
