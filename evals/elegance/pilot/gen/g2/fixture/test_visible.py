"""Visible tests. Run with `python -m pytest` or `python test_visible.py`."""

import os
import sys
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from billing import bill_total, compute_bill  # noqa: E402


def test_residential_three_tiers_winter():
    lines = compute_bill("residential", 40, month=1)
    assert lines == [
        ("Service charge", Decimal("8.00")),
        ("Tier 1", Decimal("12.00")),
        ("Tier 2", Decimal("37.00")),
        ("Tier 3", Decimal("26.00")),
    ]
    assert bill_total(lines) == Decimal("83.00")


def test_residential_senior_discount():
    lines = compute_bill("residential", 5, month=2, senior=True)
    assert lines == [
        ("Service charge", Decimal("8.00")),
        ("Tier 1", Decimal("6.00")),
        ("Senior discount", Decimal("-3.00")),
    ]


def test_commercial_single_tier():
    lines = compute_bill("commercial", 20, month=4)
    assert lines == [("Service charge", Decimal("25.00")), ("Tier 1", Decimal("30.00"))]


def test_irrigation_in_season():
    lines = compute_bill("irrigation", 10, month=5)
    assert lines == [("Service charge", Decimal("12.00")), ("Tier 1", Decimal("21.00"))]


def test_unknown_class_rejected():
    try:
        compute_bill("industrial", 1, month=1)
    except ValueError:
        return
    raise AssertionError("expected ValueError")


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print("ok  ", t.__name__)
    print("%d passed" % len(tests))
