"""Monthly water bill for a small municipal utility.

All tariff facts live in the tables below. To change a rate, edit it there; to add a
customer class, add one entry to TARIFFS.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import NamedTuple, Optional, Tuple

D = Decimal

STANDARD_DAYS = 30  # tier limits are quoted per 30-day period and prorated by billing days
SUMMER_MONTHS = (6, 7, 8)
SUMMER_SURCHARGE = D("1.15")  # multiplies the rate of every tier flagged `seasonal`


class Tier(NamedTuple):
    up_to: Optional[Decimal]  # cumulative m3 limit per standard period; None = unbounded
    rate: Decimal  # per m3
    seasonal: bool = False  # subject to the summer surcharge


class Tariff(NamedTuple):
    service_charge: Decimal
    tiers: Tuple[Tier, ...]  # in ascending order; labelled "Tier 1", "Tier 2", ...
    no_service_months: Tuple[int, ...] = ()  # months in which the service charge is waived
    senior_discount: Optional[Decimal] = None  # fraction off the Tier 1 amount


TARIFFS = {
    "residential": Tariff(
        service_charge=D("8.00"),
        tiers=(
            Tier(D(10), D("1.20")),
            Tier(D(30), D("1.85"), seasonal=True),
            Tier(None, D("2.60"), seasonal=True),
        ),
        senior_discount=D("0.5"),
    ),
    "commercial": Tariff(
        service_charge=D("25.00"),
        tiers=(
            Tier(D(50), D("1.50")),
            Tier(None, D("1.95"), seasonal=True),
        ),
    ),
    "irrigation": Tariff(
        service_charge=D("12.00"),
        tiers=(Tier(None, D("2.10")),),
        no_service_months=(11, 12, 1, 2, 3),
    ),
}


def _cents(amount):
    return amount.quantize(D("0.01"), rounding=ROUND_HALF_UP)


def _tier_quantities(tiers, usage, period):
    """Yield (tier, m3 billed in that tier) for each tier, filling the cheapest first."""
    floor = D(0)
    for tier in tiers:
        ceiling = usage if tier.up_to is None else min(usage, tier.up_to * period)
        yield tier, ceiling - floor
        if tier.up_to is not None:
            floor = tier.up_to * period


def compute_bill(customer_class, usage_m3, month, days=30, senior=False):
    """Return the bill as a list of (label, amount) lines, in print order.

    Amounts are Decimals rounded to the cent. The bill total is the sum of the lines.
    """
    usage = D(str(usage_m3))
    if usage < 0:
        raise ValueError("usage cannot be negative")
    if not 1 <= month <= 12:
        raise ValueError("month must be 1..12")
    if days <= 0:
        raise ValueError("days must be positive")
    try:
        tariff = TARIFFS[customer_class]
    except (KeyError, TypeError):  # TypeError: unhashable class, still just "unknown"
        raise ValueError("unknown customer class: %r" % (customer_class,)) from None

    period = D(days) / D(STANDARD_DAYS)
    summer = month in SUMMER_MONTHS

    lines = []
    if month not in tariff.no_service_months:
        lines.append(("Service charge", tariff.service_charge))

    tier_amounts = {}
    for number, (tier, quantity) in enumerate(_tier_quantities(tariff.tiers, usage, period), 1):
        if quantity > 0:
            rate = tier.rate * SUMMER_SURCHARGE if tier.seasonal and summer else tier.rate
            tier_amounts[number] = _cents(quantity * rate)
            lines.append(("Tier %d" % number, tier_amounts[number]))

    if senior and tariff.senior_discount and 1 in tier_amounts:
        lines.append(("Senior discount", -_cents(tier_amounts[1] * tariff.senior_discount)))

    return lines


def bill_total(lines):
    """Sum of the printed line amounts."""
    return sum((amount for _label, amount in lines), D("0.00"))
