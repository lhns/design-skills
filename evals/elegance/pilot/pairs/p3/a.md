# Candidate A

```python
def export_rows(deliveries, for_board):
    """Rows for the produce board report (for_board=True) or a member statement."""
    rows = []
    running = 0
    for d in sorted(deliveries, key=lambda d: (d.date, d.ticket)):
        if for_board and d.rejected:
            continue
        date = d.date.isoformat() if for_board else d.date.strftime("%d.%m.%Y")
        weight = f"{d.weight_kg:.0f}" if for_board else f"{d.weight_kg / 1000:.3f}"
        row = [d.member_id, date, weight, d.grade]
        if not for_board:
            running += d.amount_cents
            row += [d.reject_reason or "", money(d.amount_cents), money(running)]
        rows.append(row)
    return rows
```
