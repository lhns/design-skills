**Design 1 is better.**

The key fact is the complaints log: the email is the learner's copy of the terms, and when the board changed the cutoff from seven to ten days, emails that still said "one week" cost the centre 23 refunds. The email text and the refund rule must therefore never disagree.

**Candidate B** hard-codes "ten days" in the template prose while the rule lives in `FULL_REFUND_DAYS` in Python. These are two independent sources of truth. The board has changed the terms twice in four years, so a third change is likely. A developer updating the constant can easily forget the template, or Gwen can edit the wording without knowing the rule changed. That is exactly the spring-term failure, and nothing in the code ties the two together.

**Candidate A** keeps a single source of truth. The email is rendered from the same `full_refund_deadline()` function the refund logic uses, so the email and the refund cannot drift apart. It also gives the learner a concrete date, which is clearer than "ten days before" and leaves less room for dispute. The deadline-day rule is satisfied: `today <= deadline` gives a full refund on the deadline day itself, which matches B's `>= 10` days check for whole-day dates.

On Gwen's needs: the template is still a plain text file she can edit without touching Python. She only has to keep a `$refund_deadline` placeholder, which she is happy with and can move around in the text. The wording around it (parking notes, café hours) is hers to change freely.

A minor point is that `timedelta` and the extra function add slight complexity, but this is small and justified. A's remaining weakness is that the template could drop the placeholder, but that is a much smaller risk than a hard-coded number going stale.

WINNER: 1