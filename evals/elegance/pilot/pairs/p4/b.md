# Candidate B

`routing.yaml`:

```yaml
# First matching rule wins. Every condition in `when` must hold.
- queue: enterprise-desk
  when: {customer_tier: {eq: enterprise}}
- queue: billing-escalations
  when: {subject: {contains_any: [refund]}, amount: {gt: 500}}
- queue: billing
  when: {subject: {contains_any: [refund, invoice, receipt]}}
- queue: security
  when: {subject: {contains_any: [password, login]}, channel: {eq: phone}}
- queue: self-service
  when: {subject: {contains_any: [password, login]}}
- queue: localized
  when: {language: {ne: en}}
- queue: general
  when: {}
```

`routing.py`:

```python
import yaml

OPS = {
    "eq": lambda value, arg: value == arg,
    "ne": lambda value, arg: value != arg,
    "gt": lambda value, arg: value is not None and value > arg,
    "contains_any": lambda value, arg: any(word in value.lower() for word in arg),
}

with open("routing.yaml") as f:
    RULES = yaml.safe_load(f)


def _matches(ticket, when) -> bool:
    return all(
        OPS[op](getattr(ticket, field), arg)
        for field, condition in when.items()
        for op, arg in condition.items()
    )


def route(ticket) -> str:
    return next(rule["queue"] for rule in RULES if _matches(ticket, rule["when"]))
```
