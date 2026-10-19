# Candidate B

```python
def board_rows(deliveries):
    """Produce board report, in the format set by the board's latest circular.

    Accepted loads only. Columns: member id, ISO date, weight (whole kg), grade.
    """
    rows = []
    for d in sorted(deliveries, key=lambda d: (d.date, d.ticket)):
        if d.rejected:
            continue
        rows.append([d.member_id, d.date.isoformat(), f"{d.weight_kg:.0f}", d.grade])
    return rows


def statement_rows(deliveries):
    """Member statement, in the format set by the cooperative office.

    All loads. Columns: member id, date (dd.mm.yyyy), weight (t, 3 decimals),
    grade, reject reason, amount, running total.
    """
    rows = []
    running = 0
    for d in sorted(deliveries, key=lambda d: (d.date, d.ticket)):
        running += d.amount_cents
        rows.append([
            d.member_id,
            d.date.strftime("%d.%m.%Y"),
            f"{d.weight_kg / 1000:.3f}",
            d.grade,
            d.reject_reason or "",
            money(d.amount_cents),
            money(running),
        ])
    return rows
```
