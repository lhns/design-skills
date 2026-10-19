"""Regression tests for tickets #402, #377, #311 and #288."""

import datetime
import os
import sys
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fares import quote, total  # noqa: E402

D = datetime.date
ADULT = D(1990, 1, 1)


def vehicle_line(lines):
    return next(line for line in lines if "vehicle" in line[0])


def test_5m_car_single_is_a_car():  # #402
    assert vehicle_line(quote(D(2026, 2, 10), [ADULT], vehicle_length_m="5.00")) == (
        "Outbound: vehicle (car)", Decimal("45.00"))


def test_just_over_5m_is_a_van():
    assert vehicle_line(quote(D(2026, 2, 10), [ADULT], vehicle_length_m="5.01"))[0] == "Outbound: vehicle (van)"


def test_5m_car_return_is_a_car():
    lines = quote(D(2026, 2, 10), [ADULT], vehicle_length_m=5, return_date=D(2026, 2, 12))
    assert [l for l in lines if "vehicle" in l[0]] == [
        ("Outbound: vehicle (car)", Decimal("45.00")), ("Return: vehicle (car)", Decimal("45.00"))]


def test_long_vehicle_per_started_metre():  # #377
    assert vehicle_line(quote(D(2026, 1, 15), [ADULT], vehicle_length_m="8.1")) == (
        "Outbound: vehicle (long, 9 m)", Decimal("108.00"))


def test_return_priced_on_outbound_date():  # #311
    lines = quote(D(2026, 8, 30), [ADULT], return_date=D(2026, 10, 3))
    assert lines[1] == ("Return: 1 x adult", Decimal("27.50"))


def test_return_lists_infants_on_both_legs():  # #288
    lines = quote(D(2026, 2, 10), [ADULT, D(2025, 1, 1)], return_date=D(2026, 2, 11))
    assert [l for l in lines if "infant" in l[0]] == [
        ("Outbound: 1 x infant", Decimal("0.00")), ("Return: 1 x infant", Decimal("0.00"))]
    assert total(lines) == Decimal("38.50")


def test_vehicle_length_limits():
    for bad in (0, -1, "18.76"):
        try:
            quote(D(2026, 2, 10), [ADULT], vehicle_length_m=bad)
        except ValueError:
            continue
        raise AssertionError("expected ValueError for %r" % (bad,))
    quote(D(2026, 2, 10), [ADULT], vehicle_length_m="18.75")
