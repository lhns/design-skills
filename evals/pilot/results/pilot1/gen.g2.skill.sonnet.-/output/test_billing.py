"""Edge cases beyond the visible tests. Run with `python -m pytest` or `python test_billing.py`."""

import os
import sys
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from billing import bill_total, compute_bill  # noqa: E402


def raises_value_error(*args, **kwargs):
    try:
        compute_bill(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_summer_markup_hits_upper_tiers_only():
    lines = compute_bill("residential", 40, month=7)
    assert lines == [
        ("Service charge", Decimal("8.00")),
        ("Tier 1", Decimal("12.00")),
        ("Tier 2", Decimal("42.55")),
        ("Tier 3", Decimal("29.90")),
    ]


def test_commercial_summer_second_tier():
    lines = compute_bill("commercial", 60, month=8)
    assert lines == [
        ("Service charge", Decimal("25.00")),
        ("Tier 1", Decimal("75.00")),
        ("Tier 2", Decimal("22.43")),
    ]


def test_tier_limits_are_prorated_not_rounded():
    # 15 days: Tier 1 limit is 5 m3, Tier 2 limit is 15 m3.
    lines = compute_bill("residential", 20, month=1, days=15)
    assert lines == [
        ("Service charge", Decimal("8.00")),
        ("Tier 1", Decimal("6.00")),
        ("Tier 2", Decimal("18.50")),
        ("Tier 3", Decimal("13.00")),
    ]


def test_irrigation_off_season_has_no_service_charge():
    assert compute_bill("irrigation", 10, month=12) == [("Tier 1", Decimal("21.00"))]
    assert compute_bill("irrigation", 0, month=1) == []


def test_zero_usage_bills_service_charge_only():
    assert compute_bill("residential", 0, month=5, senior=True) == [("Service charge", Decimal("8.00"))]


def test_senior_discount_rounds_half_up_and_is_residential_only():
    lines = compute_bill("residential", 1.25, month=1, senior=True)  # Tier 1 = 1.50
    assert lines[-1] == ("Senior discount", Decimal("-0.75"))
    lines = compute_bill("residential", 1.1, month=1, senior=True)  # Tier 1 = 1.32
    assert lines[-1] == ("Senior discount", Decimal("-0.66"))
    lines = compute_bill("residential", 0.5, month=1, days=30, senior=True)  # Tier 1 = 0.60
    assert lines[-1] == ("Senior discount", Decimal("-0.30"))
    assert compute_bill("commercial", 5, month=1, senior=True) == compute_bill("commercial", 5, month=1)


def test_total_is_sum_of_lines():
    lines = compute_bill("residential", 12.345, month=6, senior=True)
    assert bill_total(lines) == sum(a for _l, a in lines)
    assert bill_total([]) == Decimal("0.00")


def test_validation_errors():
    assert raises_value_error("residential", -1, month=1)
    assert raises_value_error("residential", 1, month=0)
    assert raises_value_error("residential", 1, month=13)
    assert raises_value_error("residential", 1, month=1, days=0)
    assert raises_value_error("industrial", 1, month=1)


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print("ok  ", t.__name__)
    print("%d passed" % len(tests))
