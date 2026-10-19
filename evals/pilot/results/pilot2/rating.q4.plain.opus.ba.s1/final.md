# Design 2 (Candidate A) is the better design

The deciding factor is the incident in the complaints log. When the board moved the cutoff, the code changed but the email text didn't, and the centre had to honour the email. That cost twenty-three refunds.

**Design 1 repeats that failure.** The cutoff exists in two places:
- the constant `FULL_REFUND_DAYS = 10` in Python
- the words "at least ten days" in Gwen's template

Nothing links them. When the board next changes the terms, a developer will update the constant. Gwen's template will keep saying "ten days" until someone remembers to edit it. The comment says the office team owns that file, so the developer may not even think to look. Under the trading standards advice, the email wins, so the centre pays.

**Design 2 makes the rule the single source of truth.**
- `full_refund_deadline()` computes the deadline once.
- `refund_on_withdrawal()` uses it to decide the refund.
- `confirmation_email()` uses it to fill the template.

Changing `FULL_REFUND_BEFORE` therefore changes the decision and the learner's copy of the terms together. Gwen still controls the wording. She gets one placeholder, `$refund_deadline`, which she can move anywhere in the text, as she said she was happy to do, and she never touches Python.

**Smaller advantages of Design 2:**
- **It states a date, not a count.** "On or before Monday 12 January" is clearer than "at least ten days before". The desk doesn't need to argue about whether day 10 counts or how to count days.
- **It names the deadline.** The docstring says the deadline is the last day that still qualifies. This matches Odile's rule that withdrawing on the deadline day itself gets a full refund. The `<=` comparison makes that explicit.
- **Both designs give the same result.** `today <= first_session - 10 days` is equivalent to `(first_session - today).days >= 10`. Design 2 doesn't make the logic worse.

**Remaining gap in Design 2:** `Template.substitute` ignores unused keyword arguments. If Gwen deleted `$refund_deadline` and typed "ten days" back in, nothing would warn anyone. A small test or load-time check that the template contains the placeholder would close this gap. Even without it, Design 2 makes the correct approach the easy one, while Design 1 depends on two people remembering to edit two files.

WINNER: 2