# Design 1 (Candidate A) is better

## The deciding requirement

Jonas and Rhea agreed that mapping history isn't needed because "we never resubmit old reports." Rhea's later comment contradicts that. Every June the auditor reruns two of the previous year's quarterly reports from the app and checks them line by line against the PDFs sent to the trust.

From 1 April, VOL-TRAVEL and VOL-SUBS move into "Programme delivery":

- **Candidate B** edits the mapping in place. After the change, rerunning any earlier quarter puts those codes under "Programme delivery", and "Volunteer expenses" disappears. The rerun no longer matches the submitted PDF, and the audit fails. The only workarounds are reverting the mapping by hand during the audit or keeping old copies of the code, which is exactly the retyping and side-channel work FIN-31 is meant to remove. B's comment "the app has one answer for where a code belongs" is the bug: the correct answer depends on *when*.
- **Candidate A** stores rows with a `valid from` date and never edits or removes them. `line_for` resolves each expense against the mapping in force on `spent_on`. Old quarters reproduce exactly, and new quarters pick up the change. The audit rerun works with no extra steps.

This isn't speculative generality (YAGNI). There is a known, recurring consumer (the annual audit) and a known upcoming change (1 April). B is simpler only because it skips a real requirement.

## Cost of A

The cost is small:

- About ten extra lines and one helper with a clear name and docstring.
- An append-only list is easy for Rhea to maintain: she adds `("VOL-TRAVEL", "Programme delivery", date(<year>, 4, 1))` and leaves the old row in place.
- Performance is a linear scan per expense, which is trivial for a few thousand expenses a year and a few dozen mapping rows.
- An unknown code still fails loudly. A's `KeyError` message names the code and date, which is more actionable than B's bare `KeyError: 'XYZ'`.

## Suggested tweaks to A (non-blocking)

1. **Duplicate start dates.** If the same code gets two rows with the same `valid from`, `max(starts)` silently breaks the tie by comparing line names alphabetically. Add a load-time check that `(code, start)` pairs are unique.
2. **Tests.** Cover a quarter before 1 April and one after for VOL-TRAVEL, so a rerun of an old quarter is pinned to the old line. Also test a code used before its first `valid from`.
3. **Document the rule.** A short comment should say that expenses are mapped by `spent_on`, not by report run date, since that's what makes audit reruns stable.

WINNER: 1