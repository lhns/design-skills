# Candidate A

```python
def route(t) -> str:
    subject = t.subject.lower()
    if t.customer_tier == "enterprise":
        return "enterprise-desk"
    if "refund" in subject:
        if t.amount is not None and t.amount > 500:
            return "billing-escalations"
        return "billing"
    if "invoice" in subject or "receipt" in subject:
        return "billing"
    if "password" in subject or "login" in subject:
        return "security" if t.channel == "phone" else "self-service"
    if t.language != "en":
        return "localized"
    return "general"
```
