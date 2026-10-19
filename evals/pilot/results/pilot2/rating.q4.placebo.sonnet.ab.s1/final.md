**Candidate A is the better design.**

**The rule and the email must agree.** The complaints log is the key evidence. The board changed the cutoff from seven to ten days, but the email text still said "one week". Because the email is the learner's copy of the terms, the centre had to refund 23 people. The real problem is two places holding the same piece of knowledge (the refund window), and they drifted apart.

**Candidate B repeats that failure.** It keeps `FULL_REFUND_DAYS = 10` in Python and "ten days" in the template prose. When the board changes the rule a third time, a developer must change the code and Gwen must change the template, and nothing ties the two together. If either is forgotten, the email contradicts the actual refund behaviour. That is exactly the incident that cost 23 refunds.

**Candidate A gives the rule one home.** The cutoff lives in `FULL_REFUND_BEFORE`. Both `refund_on_withdrawal` and the email draw on `full_refund_deadline`, so the date shown to the learner is the one the refund logic uses. Changing the constant updates both.

**It also suits Gwen.** She edits a plain text template with `$name`-style placeholders, which she said she is fine with as long as she can move them around. She can reword, add parking notes and café hours, and reposition `$refund_deadline` without touching Python. The email also becomes more useful: it gives a concrete date rather than making the learner count back ten days.

**Boundary behaviour is correct.** The deadline day itself gets the full refund. A: `today <= first_session - 10 days` is equivalent to `(first_session - today).days >= 10`, so the two candidates behave identically on refunds. The difference is only in the email.

**Minor points on A.**
- `Template.substitute` raises `KeyError` if Gwen introduces a placeholder that isn't supplied. That is fail-fast behaviour, though an error message naming the placeholder would help. A test that renders the template for a sample enrolment would catch this before it ships.
- The template is read at import time, so edits need a restart. Acceptable at this scale.
- Both A and B assume `first_session` and `today` are `date` objects, which matches the "plain dates" note.

B is slightly simpler, but the simplicity is what lets the stated terms and the real behaviour diverge. A's one extra small function is justified by a real, costly incident.

WINNER: 1