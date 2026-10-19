"""Monthly water bill for a small municipal utility.

Tariffs are data: to adjust a rate or add a customer class, edit TARIFFS only.
"""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

D = Decimal

STANDARD_PERIOD_DAYS = 30  # tier limits below are per this many days
SUMMER_MONTHS = frozenset({6, 7, 8})
SUMMER_SURCHARGE = D("1.15")  # multiplies the rate of tiers marked `summer_surcharge`


@dataclass(frozen=True)
class Tier:
    rate: Decimal  # per m3
    upto_m3: Decimal | None = None  # cumulative upper limit per standard period; None = no limit
    summer_surcharge: bool = True


@dataclass(frozen=True)
class Tariff:
    service_charge: Decimal
    tiers: tuple[Tier, ...]  # ascending by limit; printed as "Tier 1", "Tier 2", ...
    service_charge_waived_months: frozenset = frozenset()
    senior_tier1_discount: Decimal | None = None  # fraction taken off the Tier 1 line


TARIFFS = {
    "residential": Tariff(
        service_charge=D("8.00"),
        tiers=(
            Tier(D("1.20"), upto_m3=D(10), summer_surcharge=False),
            Tier(D("1.85"), upto_m3=D(30)),
            Tier(D("2.60")),
        ),
        senior_tier1_discount=D("0.5"),
    ),
    "commercial": Tariff(
        service_charge=D("25.00"),
        tiers=(
            Tier(D("1.50"), upto_m3=D(50), summer_surcharge=False),
            Tier(D("1.95")),
        ),
    ),
    "irrigation": Tariff(
        service_charge=D("12.00"),
        service_charge_waived_months=frozenset({11, 12, 1, 2, 3}),  # off-season
        tiers=(Tier(D("2.10"), summer_surcharge=False),),
    ),
}


def compute_bill(customer_class, usage_m3, month, days=30, senior=False):
    """Return the bill as a list of (label, amount) lines, in print order.

    Amounts are Decimals rounded to the cent. The bill total is the sum of the lines.
    Raises ValueError for negative usage, a month outside 1..12, non-positive days
    or an unknown customer class.
    """
    usage = D(str(usage_m3))
    if usage < 0:
        raise ValueError("usage cannot be negative")
    if not 1 <= month <= 12:
        raise ValueError("month must be 1..12")
    if days <= 0:
        raise ValueError("days must be positive")
    if customer_class not in TARIFFS:
        raise ValueError("unknown customer class: %r" % (customer_class,))

    tariff = TARIFFS[customer_class]
    lines = []
    if month not in tariff.service_charge_waived_months:
        lines.append(("Service charge", tariff.service_charge))
    tier_lines = _tier_lines(tariff, usage, month, period=D(days) / STANDARD_PERIOD_DAYS)
    lines += tier_lines
    if senior and tariff.senior_tier1_discount and tier_lines:
        # Any usage fills Tier 1 first, so the first tier line is always Tier 1.
        _label, tier1_amount = tier_lines[0]
        lines.append(("Senior discount", -_to_cents(tier1_amount * tariff.senior_tier1_discount)))
    return lines


def bill_total(lines):
    """Sum of the printed line amounts."""
    return sum((amount for _label, amount in lines), D("0.00"))


def _tier_lines(tariff, usage, month, period):
    """One line per tier that has usage in it. Limits scale with the billing period."""
    summer = month in SUMMER_MONTHS
    lines = []
    lower = D(0)
    for number, tier in enumerate(tariff.tiers, start=1):
        upper = usage if tier.upto_m3 is None else min(usage, tier.upto_m3 * period)
        quantity = upper - lower
        if quantity > 0:
            rate = tier.rate * SUMMER_SURCHARGE if summer and tier.summer_surcharge else tier.rate
            lines.append(("Tier %d" % number, _to_cents(quantity * rate)))
        lower = upper
    return lines


def _to_cents(amount):
    return amount.quantize(D("0.01"), rounding=ROUND_HALF_UP)
