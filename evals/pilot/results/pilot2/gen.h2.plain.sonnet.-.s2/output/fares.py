"""Ticket prices for the island ferry.

All fares live in the tables below; the pricing code contains no prices.
"""

from collections import Counter
from decimal import Decimal, ROUND_CEILING

D = Decimal

# --- Fare tables (the yearly update touches only this section) --------------

SEASON_BY_MONTH = {
    1: "low", 2: "low", 3: "low", 4: "low",
    5: "shoulder", 6: "shoulder",
    7: "high", 8: "high",
    9: "shoulder",
    10: "low", 11: "low", 12: "low",
}

SEASONS = ("high", "shoulder", "low")


def _by_season(high, shoulder, low):
    return dict(zip(SEASONS, map(D, (high, shoulder, low))))


# Passenger categories in bill order: (label, minimum age, fare).
# Infants are listed at 0.00 so they appear on the bill (ticket #288).
PASSENGERS = [
    ("adult", 16, _by_season("27.50", "22.00", "18.00")),
    ("child", 4, _by_season("13.50", "11.00", "9.00")),
    ("infant", 0, _by_season("0.00", "0.00", "0.00")),
]

# Vehicle classes by increasing length: (label, longest length in metres
# included, flat fare). Add a motorbike class here.
VEHICLES = [
    ("car", D("5.00"), _by_season("68.00", "55.00", "45.00")),
    ("van", D("7.00"), _by_season("105.00", "85.00", "70.00")),
]
# Anything longer is charged per started metre (ticket #377).
LONG_VEHICLE_PER_METRE = _by_season("17.00", "14.00", "12.00")
LONGEST_LANE_M = D("18.75")

BOOKING_FEE = D("2.50")

# --- Pricing ----------------------------------------------------------------


def _age(birth, on):
    return on.year - birth.year - ((on.month, on.day) < (birth.month, birth.day))


def _passenger_category(age):
    return next(label for label, minimum, _ in PASSENGERS if age >= minimum)


def _vehicle_line(length, season):
    """Return (label, amount) for one crossing of a vehicle of this length."""
    for label, longest, fare in VEHICLES:
        if length <= longest:
            return "vehicle (%s)" % label, fare[season]
    metres = length.to_integral_value(rounding=ROUND_CEILING)
    return "vehicle (long, %d m)" % metres, metres * LONG_VEHICLE_PER_METRE[season]


def _leg_lines(season, counts, length):
    """Lines for one crossing, without the leg prefix."""
    lines = [
        ("%d x %s" % (counts[label], label), counts[label] * fare[season])
        for label, _, fare in PASSENGERS
        if counts[label]
    ]
    if length is not None:
        lines.append(_vehicle_line(length, season))
    return lines


def quote(outbound, passengers, vehicle_length_m=None, return_date=None):
    """Return the bill as a list of (label, amount) lines, in print order.

    outbound and return_date are datetime.date; passengers is a list of birth dates.
    Amounts are Decimals. The bill total is the sum of the lines (see total()).
    """
    if not passengers:
        raise ValueError("at least one passenger is required")
    if any(birth > outbound for birth in passengers):
        raise ValueError("birth date after travel date")
    if return_date is not None and return_date < outbound:
        raise ValueError("return before outbound")
    length = None
    if vehicle_length_m is not None:
        length = D(str(vehicle_length_m))
        if length <= 0 or length > LONGEST_LANE_M:
            raise ValueError("vehicle length out of range")

    # Both legs use the outward date for season and ages (conditions of
    # carriage 7.2, ticket #311).
    season = SEASON_BY_MONTH[outbound.month]
    counts = Counter(_passenger_category(_age(b, outbound)) for b in passengers)
    leg_lines = _leg_lines(season, counts, length)

    legs = ["Outbound"] if return_date is None else ["Outbound", "Return"]
    bill = [("%s: %s" % (leg, label), amount) for leg in legs for label, amount in leg_lines]
    bill.append(("Booking fee", BOOKING_FEE))
    return bill


def total(lines):
    """Sum of the line amounts."""
    return sum((amount for _, amount in lines), D("0.00"))
