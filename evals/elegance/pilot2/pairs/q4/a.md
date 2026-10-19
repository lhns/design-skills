# Candidate A

```python
from datetime import timedelta
from decimal import Decimal
from pathlib import Path
from string import Template

# Full refund if the learner withdraws at least this long before the first session.
FULL_REFUND_BEFORE = timedelta(days=10)

# Written and maintained by the office team.
TEMPLATE = Template(Path("templates/confirmation.txt").read_text())


def full_refund_deadline(enrolment):
    """Last day on which a withdrawal still gets the full fee back."""
    return enrolment.first_session - FULL_REFUND_BEFORE


def confirmation_email(enrolment):
    return TEMPLATE.substitute(
        name=enrolment.learner_name,
        course=enrolment.course_title,
        first_session=f"{enrolment.first_session:%A %d %B}",
        refund_deadline=f"{full_refund_deadline(enrolment):%A %d %B}",
    )


def refund_on_withdrawal(enrolment, today):
    if today <= full_refund_deadline(enrolment):
        return enrolment.fee_paid
    return Decimal("0.00")
```

`templates/confirmation.txt`:

```text
Dear $name,

You are enrolled on $course. Your first session is on $first_session.

If you withdraw on or before $refund_deadline, we refund your fee in full.
After that date we are unable to offer a refund.
```
