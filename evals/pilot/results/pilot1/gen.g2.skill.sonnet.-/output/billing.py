"""Monthly water bill for a small municipal utility.

Every tariff fact lives in TARIFFS (and the two seasonal constants below);
compute_bill only applies them.
"""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

D = Decimal

SUMMER_MONTHS = (6, 7, 8)
SUMMER_MARKUP = D("1.15")  # applies to tiers flagged `seasonal`
STANDARD_DAYS = 30  # tier limits are quoted for a period of this many days


@dataclass(frozen=True)
class Tier:
    rate: Decimal  # per m3
    upto: int = None  # cumulative limit in m3 per standard period; None = unlimited
    seasonal: bool = False  # does the summer markup apply?


@dataclass(frozen=True)
class Tariff:
    service_charge: Decimal
    tiers: tuple
    waived_months: tuple = ()  # months without a service charge
    senior_discount: Decimal = D(0)  # share of the Tier 1 amount, 0 = none


TARIFFS = {
    "residential": Tariff(
        service_charge=D("8.00"),
        tiers=(
            Tier(D("1.20"), upto=10),
            Tier(D("1.85"), upto=30, seasonal=True),
            Tier(D("2.60"), seasonal=True),
        ),
        senior_discount=D("0.5"),
    ),
    "commercial": Tariff(
        service_charge=D("25.00"),
        tiers=(Tier(D("1.50"), upto=50), Tier(D("1.95"), seasonal=True)),
    ),
    "irrigation": Tariff(
        service_charge=D("12.00"),
        tiers=(Tier(D("2.10")),),
        waived_months=(11, 12, 1, 2, 3),
    ),
}


def cents(amount):
    return amount.quantize(D("0.01"), rounding=ROUND_HALF_UP)


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
    if customer_class not in TARIFFS:
        raise ValueError("unknown customer class: %r" % (customer_class,))

    tariff = TARIFFS[customer_class]
    period = D(days) / D(STANDARD_DAYS)
    summer = month in SUMMER_MONTHS

    lines = []
    if month not in tariff.waived_months:
        lines.append(("Service charge", tariff.service_charge))

    # Each tier bills the usage between the previous tier's limit and its own.
    tier_lines = []
    billed = D(0)  # usage covered by the tiers so far
    for n, tier in enumerate(tariff.tiers, start=1):
        covered = usage if tier.upto is None else min(usage, tier.upto * period)
        quantity, billed = covered - billed, covered
        if quantity > 0:
            rate = tier.rate * SUMMER_MARKUP if summer and tier.seasonal else tier.rate
            tier_lines.append(("Tier %d" % n, cents(quantity * rate)))
    lines += tier_lines

    if senior and tariff.senior_discount and tier_lines:
        _label, tier1 = tier_lines[0]
        lines.append(("Senior discount", -cents(tier1 * tariff.senior_discount)))

    return lines


def bill_total(lines):
    """Sum of the printed line amounts."""
    return sum((amount for _label, amount in lines), D("0.00"))
