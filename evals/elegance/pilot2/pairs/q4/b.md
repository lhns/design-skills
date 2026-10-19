# Candidate B

```python
from decimal import Decimal
from pathlib import Path
from string import Template

# Full refund if the learner withdraws at least this many days before the first session.
FULL_REFUND_DAYS = 10

# Written and maintained by the office team.
TEMPLATE = Template(Path("templates/confirmation.txt").read_text())


def confirmation_email(enrolment):
    return TEMPLATE.substitute(
        name=enrolment.learner_name,
        course=enrolment.course_title,
        first_session=f"{enrolment.first_session:%A %d %B}",
    )


def refund_on_withdrawal(enrolment, today):
    if (enrolment.first_session - today).days >= FULL_REFUND_DAYS:
        return enrolment.fee_paid
    return Decimal("0.00")
```

`templates/confirmation.txt`:

```text
Dear $name,

You are enrolled on $course. Your first session is on $first_session.

If you withdraw at least ten days before your first session, we refund your
fee in full. After that we are unable to offer a refund.
```
