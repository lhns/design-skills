"""Ticket prices for the island ferry.

The yearly fare change is an edit to the tables below; nothing else in the
module states a price, an age limit or a length limit.
"""

from collections import namedtuple
from decimal import Decimal, ROUND_CEILING
from enum import IntEnum


class Season(IntEnum):
    HIGH = 0
    SHOULDER = 1
    LOW = 2


def _season_of(date):
    if date.month in (7, 8):
        return Season.HIGH
    if date.month in (5, 6, 9):
        return Season.SHOULDER
    return Season.LOW


def _prices(high, shoulder, low):
    """One price per season, indexed by Season."""
    return tuple(Decimal(p) for p in (high, shoulder, low))


# --- Fare tables (the only place prices and limits are written) -------------

# In bill print order. A passenger belongs to the first band whose minimum age
# they have reached, so the last band must start at 0.
PassengerBand = namedtuple("PassengerBand", "label min_age fares")
PASSENGER_BANDS = [
    PassengerBand("adult", 16, _prices("27.50", "22.00", "18.00")),
    PassengerBand("child", 4, _prices("13.50", "11.00", "9.00")),
    PassengerBand("infant", 0, _prices("0.00", "0.00", "0.00")),  # listed for the manifest (#288)
]

# Flat-fare vehicle classes, shortest first. A vehicle belongs to the first
# class whose maximum length it does not exceed (inclusive, #402).
# A new class (e.g. motorbike) is one more row here.
VehicleClass = namedtuple("VehicleClass", "label max_length_m fares")
VEHICLE_CLASSES = [
    VehicleClass("car", Decimal("5.00"), _prices("68.00", "55.00", "45.00")),
    VehicleClass("van", Decimal("7.00"), _prices("105.00", "85.00", "70.00")),
]

# Anything longer than the last flat-fare class pays per started metre (#377).
LONG_VEHICLE_PER_METRE = _prices("17.00", "14.00", "12.00")
LONGEST_LANE_M = Decimal("18.75")

BOOKING_FEE = Decimal("2.50")


# --- Pricing ------------------------------------------------------------------

def _age_on(date, born):
    return date.year - born.year - ((date.month, date.day) < (born.month, born.day))


def _validate(outbound, passengers, length, return_date):
    if not passengers:
        raise ValueError("at least one passenger is required")
    if any(born > outbound for born in passengers):
        raise ValueError("birth date after travel date")
    if return_date is not None and return_date < outbound:
        raise ValueError("return before outbound")
    if length is not None and not 0 < length <= LONGEST_LANE_M:
        raise ValueError("vehicle length out of range")


def _passenger_lines(outbound, passengers, season):
    headcount = {band.label: 0 for band in PASSENGER_BANDS}
    for born in passengers:
        age = _age_on(outbound, born)
        band = next(b for b in PASSENGER_BANDS if age >= b.min_age)
        headcount[band.label] += 1
    return [
        ("%d x %s" % (headcount[band.label], band.label), headcount[band.label] * band.fares[season])
        for band in PASSENGER_BANDS
        if headcount[band.label]
    ]


def _vehicle_line(length, season):
    for vehicle in VEHICLE_CLASSES:
        if length <= vehicle.max_length_m:
            return ("vehicle (%s)" % vehicle.label, vehicle.fares[season])
    metres = length.to_integral_value(rounding=ROUND_CEILING)
    return ("vehicle (long, %d m)" % metres, metres * LONG_VEHICLE_PER_METRE[season])


def quote(outbound, passengers, vehicle_length_m=None, return_date=None):
    """Return the bill as a list of (label, amount) lines, in print order.

    outbound and return_date are datetime.date; passengers is a list of birth dates.
    Amounts are Decimals. The bill total is the sum of the lines (see total()).
    """
    length = None if vehicle_length_m is None else Decimal(str(vehicle_length_m))
    _validate(outbound, passengers, length, return_date)

    # Conditions of carriage 7.2 (#311): both legs of a return ticket are
    # priced on the outward date, and ages are taken on that date too.
    season = _season_of(outbound)
    leg_lines = _passenger_lines(outbound, passengers, season)
    if length is not None:
        leg_lines.append(_vehicle_line(length, season))

    legs = ["Outbound"] if return_date is None else ["Outbound", "Return"]
    lines = [("%s: %s" % (leg, label), amount) for leg in legs for label, amount in leg_lines]
    lines.append(("Booking fee", BOOKING_FEE))
    return lines


def total(lines):
    """Sum of the line amounts."""
    return sum((amount for _, amount in lines), Decimal("0.00"))
