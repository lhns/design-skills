"""Ticket prices for the island ferry."""

from collections import Counter
from decimal import Decimal, ROUND_CEILING

# --- The annual fare review edits only this section. ---

# Seasons by month; any month not listed is "low".
SEASON_MONTHS = {"high": (7, 8), "shoulder": (5, 6, 9)}


def _fares(high, shoulder, low):
    return {"high": Decimal(high), "shoulder": Decimal(shoulder), "low": Decimal(low)}


# Price of one leg, per season. "long" is per started metre.
FARES = {
    "adult": _fares("27.50", "22.00", "18.00"),
    "child": _fares("13.50", "11.00", "9.00"),
    "infant": _fares("0.00", "0.00", "0.00"),
    "car": _fares("68.00", "55.00", "45.00"),
    "van": _fares("105.00", "85.00", "70.00"),
    "long": _fares("17.00", "14.00", "12.00"),
}

# Passenger bands in bill order, with the minimum age on the travel date.
AGE_BANDS = (("adult", 16), ("child", 4), ("infant", 0))

# Vehicle classes, shortest first: (name, longest length in metres, inclusive).
# Anything longer is "long". A new class goes here and in FARES.
VEHICLE_CLASSES = (("car", Decimal("5.00")), ("van", Decimal("7.00")))

# The longest lane on the vessel.
MAX_VEHICLE_LENGTH_M = Decimal("18.75")

BOOKING_FEE = Decimal("2.50")

# --- Pricing rules. ---


def _season(date):
    return next((s for s, months in SEASON_MONTHS.items() if date.month in months), "low")


def _age(birth, on):
    return on.year - birth.year - ((on.month, on.day) < (birth.month, birth.day))


def _band(age):
    return next(name for name, minimum in AGE_BANDS if age >= minimum)


def _vehicle_line(length, season):
    for name, longest in VEHICLE_CLASSES:
        if length <= longest:
            return "vehicle (%s)" % name, FARES[name][season]
    metres = int(length.to_integral_value(rounding=ROUND_CEILING))
    return "vehicle (long, %d m)" % metres, metres * FARES["long"][season]


def quote(outbound, passengers, vehicle_length_m=None, return_date=None):
    """Return the bill as a list of (label, amount) lines, in print order.

    outbound and return_date are datetime.date; passengers is a list of birth dates.
    Amounts are Decimals. The bill total is the sum of the lines (see total()).
    """
    if not passengers:
        raise ValueError("at least one passenger is required")
    if any(b > outbound for b in passengers):
        raise ValueError("birth date after travel date")
    if return_date is not None and return_date < outbound:
        raise ValueError("return before outbound")
    length = None
    if vehicle_length_m is not None:
        length = Decimal(str(vehicle_length_m))
        if length <= 0 or length > MAX_VEHICLE_LENGTH_M:
            raise ValueError("vehicle length out of range")

    # Clause 7.2 of the conditions of carriage (ticket #311): a return ticket is
    # priced on the outward date, so season and ages come from `outbound` for both legs.
    season = _season(outbound)
    counts = Counter(_band(_age(b, outbound)) for b in passengers)

    one_leg = [
        ("%d x %s" % (counts[band], band), counts[band] * FARES[band][season])
        for band, _ in AGE_BANDS
        if counts[band]
    ]
    if length is not None:
        one_leg.append(_vehicle_line(length, season))

    legs = ["Outbound"] if return_date is None else ["Outbound", "Return"]
    lines = [("%s: %s" % (leg, label), amount) for leg in legs for label, amount in one_leg]
    lines.append(("Booking fee", BOOKING_FEE))
    return lines


def total(lines):
    """Sum of the line amounts."""
    return sum((amount for _, amount in lines), Decimal("0.00"))
