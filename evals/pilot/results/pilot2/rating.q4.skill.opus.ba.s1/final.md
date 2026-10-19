# Design 2 (Candidate A) is better

## Constraints

- **C1.** The refund rule is a full refund if the learner withdraws on or before the deadline (first session minus 10 days), otherwise nothing. Withdrawing on the deadline day itself still gets the refund. The rule is in whole days.
- **C2.** The board sets the cutoff and changes it every couple of years, so the cutoff must be easy to change.
- **C3.** The confirmation email is the learner's legal copy of the terms. It must always match what the code actually refunds. The complaints log shows what a mismatch costs: 23 refunds in one term.
- **C4.** Gwen edits the template wording without touching Python. Placeholders are acceptable if she can move them around.

## Trying to break each design

**Boundary (C1).** Both designs are correct. In Design 1, a withdrawal exactly 10 days out gives `.days == 10`, which passes `>= 10`. In Design 2, the deadline day gives `today == deadline`, which passes `<=`. Neither can fail at the boundary.

**Cutoff change (C2 + C3).** The board moves the cutoff to 14 days, and the developer edits the constant.
- **Design 1:** the code now refunds at 14 days, but the template still says "ten days". The email and the code disagree until someone notices and gets Gwen to fix the template. This is the March incident again, built into the structure. The cutoff is stated in two places, owned by two different people.
- **Design 2:** the email's `$refund_deadline` and the refund check both come from `full_refund_deadline()`. They cannot diverge, so no input or event breaks C3.

**Wording change (C4).** Both designs let Gwen rewrite the text freely. Design 2 adds one placeholder, which Gwen has said she is fine with. It also gives the learner a concrete date rather than "ten days before", which is clearer for someone working in whole days. Neither design makes her touch Python.

## Concept count

Design 2 adds one function, `full_refund_deadline`. That function is the single source of the fact that both the email and the refund check depend on. Design 1 avoids the function by stating the fact twice. The extra concept is forced by C3, and it removes the duplicate.

One residual risk applies to both designs: Gwen could delete the placeholder and type a fixed sentence instead. That is a matter of template guidance, such as a comment in the template saying "keep `$refund_deadline`". It is not a difference between the designs.

## Ledger

- **Forced:** the deadline is computed in one place, and both the email and the refund derive from it (C3).
- **Designer choice:** show the deadline as a calendar date rather than a day count. This is clearer for learners, and Gwen can still reword around it.
- **Deleted:** the hard-coded "ten days" in the template.

**Deciding reason:** Design 1 states the cutoff in both the code and the template, so the next board change reproduces the incident that cost 23 refunds. Design 2 derives the email's terms from the same function that decides the refund, so the two cannot disagree.

WINNER: 2