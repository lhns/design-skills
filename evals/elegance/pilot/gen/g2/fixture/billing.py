"""Monthly water bill for a small municipal utility."""

from decimal import Decimal, ROUND_HALF_UP


def compute_bill(customer_class, usage_m3, month, days=30, senior=False):
    """Return the bill as a list of (label, amount) lines, in print order.

    Amounts are Decimals rounded to the cent. The bill total is the sum of the lines.
    """
    usage = Decimal(str(usage_m3))
    if usage < 0:
        raise ValueError("usage cannot be negative")
    if not 1 <= month <= 12:
        raise ValueError("month must be 1..12")
    if days <= 0:
        raise ValueError("days must be positive")
    period = Decimal(days) / Decimal(30)
    lines = []

    if customer_class == "residential":
        lines.append(("Service charge", Decimal("8.00")))
        limit1 = Decimal(10) * period
        limit2 = Decimal(30) * period
        if usage <= limit1:
            t1 = usage
            t2 = Decimal(0)
            t3 = Decimal(0)
        elif usage <= limit2:
            t1 = limit1
            t2 = usage - limit1
            t3 = Decimal(0)
        else:
            t1 = limit1
            t2 = limit2 - limit1
            t3 = usage - limit2
        amount1 = Decimal("0.00")
        if t1 > 0:
            amount1 = (t1 * Decimal("1.20")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            lines.append(("Tier 1", amount1))
        if t2 > 0:
            rate2 = Decimal("1.85")
            if month in (6, 7, 8):
                rate2 = rate2 * Decimal("1.15")
            amount2 = (t2 * rate2).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            lines.append(("Tier 2", amount2))
        if t3 > 0:
            rate3 = Decimal("2.60")
            if month in (6, 7, 8):
                rate3 = rate3 * Decimal("1.15")
            amount3 = (t3 * rate3).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            lines.append(("Tier 3", amount3))
        if senior and t1 > 0:
            discount = (amount1 / 2).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            lines.append(("Senior discount", -discount))

    elif customer_class == "commercial":
        lines.append(("Service charge", Decimal("25.00")))
        limit1 = Decimal(50) * period
        if usage <= limit1:
            t1 = usage
            t2 = Decimal(0)
        else:
            t1 = limit1
            t2 = usage - limit1
        if t1 > 0:
            amount1 = (t1 * Decimal("1.50")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            lines.append(("Tier 1", amount1))
        if t2 > 0:
            if month in (6, 7, 8):
                amount2 = (t2 * Decimal("1.95") * Decimal("1.15")).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )
            else:
                amount2 = (t2 * Decimal("1.95")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            lines.append(("Tier 2", amount2))

    elif customer_class == "irrigation":
        if month in (11, 12, 1, 2, 3):
            pass  # irrigation meters pay no service charge off-season
        else:
            lines.append(("Service charge", Decimal("12.00")))
        if usage > 0:
            amount1 = (usage * Decimal("2.10")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            lines.append(("Tier 1", amount1))

    else:
        raise ValueError("unknown customer class: %r" % (customer_class,))

    return lines


def bill_total(lines):
    """Sum of the printed line amounts."""
    total = Decimal("0.00")
    for _label, amount in lines:
        total += amount
    return total
