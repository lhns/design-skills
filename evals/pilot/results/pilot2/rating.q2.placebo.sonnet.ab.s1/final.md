**Design 1 is better.** The deciding fact is the audit comment, which is easy to miss because Rhea flags it as "unrelated".

**The audit requirement.** In June the auditor picks two of the previous year's quarterly reports, re-runs them from the system, and ticks them off line by line against the PDFs sent to the trust. So a past report must reproduce exactly, months or a year later. That is a real need for historical mapping, even though Rhea said she never resubmits old reports and has no use for old versions. Jonas's question was about "keeping old versions", and Rhea answered for her own workflow, not for the audit.

**Design 2 breaks this.** It has one mutable mapping read at run time. On 1 April, when Rhea moves VOL-TRAVEL and VOL-SUBS into "Programme delivery", re-running any earlier quarter will put those expenses under "Programme delivery" and drop the "Volunteer expenses" row. The rerun will no longer match the PDF. The comment "one answer for where a code belongs" describes the very property that causes the failure. This is not hypothetical: Rhea has already said the change is coming. Because expenses are never deleted, the underlying data stays stable, so the mapping is the only thing that would make the numbers drift. Design 2 also raises a bare `KeyError` for an unmapped code, with no context, though that is minor.

**Design 1 handles it.** Each mapping row has a valid-from date and rows are only appended, so `line_for(code, spent_on)` resolves each expense by its own date. Reports for past quarters stay the same after the 1 April change. Rhea's workflow stays simple: she appends rows rather than editing them. It is not over-engineered: there is no history table, UI, or versioning framework, just one extra date column and a small lookup. The cost is a few lines and a slightly bigger edit for Rhea (add rows instead of changing a value). The error message for an unmapped code is also actionable, naming the code and date.

**Caveats on Design 1.**
- The mapping is resolved by expense date, which is right as long as the trust's change takes effect on the grant-year boundary. That matches 1 April.
- Corrections posted as new rows carry their own `spent_on`. If a correction to a pre-April expense is dated after 1 April, it would land under the new line. That is a policy question worth confirming with Rhea, but it is not a flaw in the design.
- The linear scan per expense is fine at a few thousand rows a year.

Design 2 is simpler, and YAGNI would favour it if the audit comment did not exist. Given the audit, the history is a stated requirement, not speculative generality.

WINNER: 1