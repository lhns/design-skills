# Enrolment confirmation and withdrawal refunds

An adult-education centre runs evening courses (pottery, languages, bookkeeping) in ten-week blocks. When someone enrols, the system sends a confirmation email. When someone withdraws, the system works out the refund. A developer is rewriting the enrolment module and has two candidates for this part. Some background:

**From the centre manager, Odile:**

> Our withdrawal terms are on the website and in the confirmation email. The board sets them; they've changed twice in four years. Right now it's a full refund if you withdraw at least ten days before your first session, and nothing after that. We don't do partial refunds, it's too fiddly at the desk.
>
> The office team writes the emails, not the developers. Gwen rewrites the confirmation text every term or two, to add parking notes, the café hours and so on. She edits the template file herself and doesn't want to wait for a developer for a wording change.

**From Gwen, in the same thread:**

> I'm fine with the odd placeholder in the template as long as I can move it around in the text. Please don't make me edit Python.

**From the centre's complaints log, summarised by Odile:**

> Spring term: the board moved the cutoff from seven to ten days in March. Emails sent between March and June still said "one week". Trading standards advice was that the email is the learner's copy of the terms, so we refunded everyone enrolled in that window who withdrew between seven and ten days out. Twenty-three refunds.

Dates are plain dates; sessions start in the evening, and the desk works in whole days. A withdrawal on the deadline day itself still gets the full refund.

Two candidate implementations follow. Which one is the better design?
