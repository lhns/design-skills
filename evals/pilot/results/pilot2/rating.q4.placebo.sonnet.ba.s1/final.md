The deciding fact is the complaints log. The board has changed the cutoff twice in four years, and the last change left emails saying "one week" while the rule was ten days. That cost 23 refunds, because the email counts as the learner's copy of the terms.

**Design 1 (Candidate B)** states the rule in two places: `FULL_REFUND_DAYS = 10` in Python, and "ten days" hard-coded in the template prose. They are the same piece of knowledge, and they can drift apart. That is exactly what happened in spring. When the board changes the cutoff, a developer edits the constant, Gwen has to remember to edit the wording, and nothing enforces that she does. Gwen is also asked to maintain a number that is really policy.

**Design 2 (Candidate A)** gives the rule a single home. `FULL_REFUND_BEFORE` drives both the refund decision and the date shown in the email, through `full_refund_deadline`. A board change is one edit in one place, and the email cannot disagree with the behaviour. The email also becomes more useful to the learner, since it states a concrete date instead of making them count back ten days.

**Fit with the stakeholders:**
- Gwen only needs to move a `$refund_deadline` placeholder around in text, which she has said is fine. She never edits Python.
- The deadline-day rule ("withdrawal on the deadline day still gets the full refund") is matched exactly: `today <= deadline` is the same as "at least ten days before". The email says "on or before", which is accurate.
- Dates are plain dates, so subtracting a `timedelta` is safe, with no time-of-day or timezone ambiguity.
- No partial-refund machinery was added, which respects YAGNI.

**Minor caveats on Design 2:**
- `Template.substitute` raises `KeyError` if Gwen introduces an unknown placeholder. That is fail-fast behaviour and applies to both designs.
- The template is read at import time, so edits need a restart. That is also true of both.
- The formatted date could include the year to be unambiguous, but that is optional polish.

Design 2 removes the duplicated rule that caused a real, costly incident, while keeping the code just as small and simple.

WINNER: 2