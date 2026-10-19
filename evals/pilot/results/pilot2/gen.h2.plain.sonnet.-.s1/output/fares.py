"""Ticket prices for the island ferry.

The yearly fare change is an edit to the tables below; nothing else states a price.
"""

from decimal import Decimal, ROUND_CEILING

# --- Fare tables -------------------------------------------------------------

SEASON_BY_MONTH = {
    1: "low", 2: "low", 3: "low", 4: "low",
    5: "shoulder", 6: "shoulder",
    7: "high", 8: "high",
    9: "shoulder",
    10: "low", 11: "low", 12: "low",
}

# Prices per leg, per person. Dict order is bill order.
PASSENGER_FARES = {
    "adult": {"high": Decimal("27.50"), "shoulder": Decimal("22.00"), "low": Decimal("18.00")},
    "child": {"high": Decimal("13.50"), "shoulder": Decimal("11.00"), "low": Decimal("9.00")},
    "infant": {"high": Decimal("0.00"), "shoulder": Decimal("0.00"), "low": Decimal("0.00")},
}

# Passengers younger than the limit (in whole years on the outward date) are in the
# band; anyone older than every limit is an adult.
YOUNGER_THAN = [(4, "infant"), (16, "child")]

# Per leg, per vehicle. Each class takes vehicles up to and including max_length_m,
# checked in order. Adding a class (e.g. motorbikes) is one more row.
VEHICLE_CLASSES = [
    ("car", Decimal("5.00"), {"high": Decimal("68.00"), "shoulder": Decimal("55.00"), "low": Decimal("45.00")}),
    ("van", Decimal("7.00"), {"high": Decimal("105.00"), "shoulder": Decimal("85.00"), "low": Decimal("70.00")}),
]

# Anything longer is charged per started metre.
LONG_VEHICLE_PER_METRE = {"high": Decimal("17.00"), "shoulder": Decimal("14.00"), "low": Decimal("12.00")}

MAX_VEHICLE_LENGTH_M = Decimal("18.75")  # the longest lane on the vessel

BOOKING_FEE = Decimal("2.50")


# --- Pricing -----------------------------------------------------------------

def _age_on(birth, day):
    return day.year - birth.year - ((day.month, day.day) < (birth.month, birth.day))


def _passenger_band(age):
    return next((band for limit, band in YOUNGER_THAN if age < limit), "adult")


def _vehicle_line(length, season):
    for name, max_length_m, prices in VEHICLE_CLASSES:
        if length <= max_length_m:
            return "vehicle (%s)" % name, prices[season]
    metres = length.to_integral_value(rounding=ROUND_CEILING)
    return "vehicle (long, %d m)" % metres, metres * LONG_VEHICLE_PER_METRE[season]


def quote(outbound, passengers, vehicle_length_m=None, return_date=None):
    """Return the bill as a list of (label, amount) lines, in print order.

    outbound and return_date are datetime.date; passengers is a list of birth dates.
    Amounts are Decimals. The bill total is the sum of the lines (see total()).

    A return ticket is priced entirely on the outward date (conditions of carriage,
    clause 7.2): both legs use the outward season and the passengers' ages that day.
    """
    if not passengers:
        raise ValueError("at least one passenger is required")
    if any(birth > outbound for birth in passengers):
        raise ValueError("birth date after travel date")
    if return_date is not None and return_date < outbound:
        raise ValueError("return before outbound")
    length = None
    if vehicle_length_m is not None:
        length = Decimal(str(vehicle_length_m))
        if length <= 0 or length > MAX_VEHICLE_LENGTH_M:
            raise ValueError("vehicle length out of range")

    season = SEASON_BY_MONTH[outbound.month]

    headcount = {band: 0 for band in PASSENGER_FARES}
    for birth in passengers:
        headcount[_passenger_band(_age_on(birth, outbound))] += 1

    # Everything priced per leg, in print order; the same for the outward and return leg.
    leg_lines = [
        ("%d x %s" % (count, band), count * PASSENGER_FARES[band][season])
        for band, count in headcount.items()
        if count
    ]
    if length is not None:
        leg_lines.append(_vehicle_line(length, season))

    legs = ["Outbound"] if return_date is None else ["Outbound", "Return"]
    lines = [("%s: %s" % (leg, label), amount) for leg in legs for label, amount in leg_lines]
    lines.append(("Booking fee", BOOKING_FEE))
    return lines


def total(lines):
    """Sum of the line amounts."""
    return sum((amount for _, amount in lines), Decimal("0.00"))
