"""Visible tests. Run with `python -m pytest` or `python test_visible.py`."""

import datetime
import os
import sys
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fares import quote, total  # noqa: E402

D = datetime.date


def test_single_adult_low_season():
    lines = quote(D(2026, 2, 10), [D(1990, 6, 1)])
    assert lines == [("Outbound: 1 x adult", Decimal("18.00")), ("Booking fee", Decimal("2.50"))]
    assert total(lines) == Decimal("20.50")


def test_child_and_infant_single():
    lines = quote(D(2026, 10, 3), [D(2015, 1, 1), D(2024, 5, 5)])
    assert lines == [
        ("Outbound: 1 x child", Decimal("9.00")),
        ("Outbound: 1 x infant", Decimal("0.00")),
        ("Booking fee", Decimal("2.50")),
    ]


def test_van_in_shoulder_season():
    lines = quote(D(2026, 5, 20), [D(1985, 3, 3), D(1986, 4, 4)], vehicle_length_m=6)
    assert lines == [
        ("Outbound: 2 x adult", Decimal("44.00")),
        ("Outbound: vehicle (van)", Decimal("85.00")),
        ("Booking fee", Decimal("2.50")),
    ]
    assert total(lines) == Decimal("131.50")


def test_long_vehicle_8m():
    lines = quote(D(2026, 1, 15), [D(1980, 1, 1)], vehicle_length_m="8.0")
    assert ("Outbound: vehicle (long, 8 m)", Decimal("96.00")) in lines


def test_same_season_return():
    lines = quote(D(2026, 7, 10), [D(1990, 1, 1)], return_date=D(2026, 7, 12))
    assert lines == [
        ("Outbound: 1 x adult", Decimal("27.50")),
        ("Return: 1 x adult", Decimal("27.50")),
        ("Booking fee", Decimal("2.50")),
    ]


def test_car_up_to_and_including_5m_single():  # ticket #402
    lines = quote(D(2026, 1, 15), [D(1980, 1, 1)], vehicle_length_m="5.00")
    assert ("Outbound: vehicle (car)", Decimal("45.00")) in lines
    lines = quote(D(2026, 1, 15), [D(1980, 1, 1)], vehicle_length_m="5.01")
    assert ("Outbound: vehicle (van)", Decimal("70.00")) in lines


def test_long_vehicle_started_metre():  # ticket #377
    lines = quote(D(2026, 1, 15), [D(1980, 1, 1)], vehicle_length_m="8.1")
    assert ("Outbound: vehicle (long, 9 m)", Decimal("108.00")) in lines


def test_return_priced_on_outward_date():  # ticket #311, clause 7.2
    lines = quote(D(2026, 8, 30), [D(1990, 1, 1)], return_date=D(2026, 10, 3))
    assert lines[1] == ("Return: 1 x adult", Decimal("27.50"))


def test_return_repeats_every_line_per_leg_with_one_booking_fee():
    lines = quote(D(2026, 6, 1), [D(1990, 1, 1), D(2024, 1, 1)], 4, D(2026, 6, 2))
    assert [label for label, _ in lines] == [
        "Outbound: 1 x adult", "Outbound: 1 x infant", "Outbound: vehicle (car)",
        "Return: 1 x adult", "Return: 1 x infant", "Return: vehicle (car)",
        "Booking fee",
    ]


def test_no_passengers_rejected():
    try:
        quote(D(2026, 1, 1), [])
    except ValueError:
        return
    raise AssertionError("expected ValueError")


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print("ok  ", t.__name__)
    print("%d passed" % len(tests))
