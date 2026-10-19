"""Hidden tests for g2 (judge only). Run with `python -m pytest` or `python test_hidden.py`.

Imports billing.py from ../fixture by default; set BILLING_DIR to test another copy.
"""

import itertools
import os
import sys
from decimal import Decimal, ROUND_HALF_UP

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("BILLING_DIR", os.path.join(_HERE, os.pardir, "fixture")))

from billing import bill_total, compute_bill  # noqa: E402

# --- Independent reference, used for the behaviour grid -------------------------

_CENT = Decimal("0.01")
_SUMMER = (6, 7, 8)
_OFF_SEASON_NO_SERVICE = {"irrigation": (11, 12, 1, 2, 3)}
_TARIFFS = {  # class: (service charge, [(tier upper bound per 30 days or None, rate)])
    "residential": ("8.00", [(10, "1.20"), (30, "1.85"), (None, "2.60")]),
    "commercial": ("25.00", [(50, "1.50"), (None, "1.95")]),
    "irrigation": ("12.00", [(None, "2.10")]),
}


def _cents(x):
    return x.quantize(_CENT, rounding=ROUND_HALF_UP)


def _reference(customer_class, usage_m3, month, days=30, senior=False):
    usage = Decimal(str(usage_m3))
    period = Decimal(days) / Decimal(30)
    service, tiers = _TARIFFS[customer_class]
    lines = []
    if month not in _OFF_SEASON_NO_SERVICE.get(customer_class, ()):
        lines.append(("Service charge", Decimal(service)))
    lower = Decimal(0)
    first_tier = None
    for i, (upper, rate) in enumerate(tiers):
        bound = None if upper is None else Decimal(upper) * period
        qty = (usage if bound is None else min(usage, bound)) - lower
        if qty > 0:
            r = Decimal(rate) * (Decimal("1.15") if i > 0 and month in _SUMMER else 1)
            amount = _cents(qty * r)
            lines.append(("Tier %d" % (i + 1), amount))
            if i == 0:
                first_tier = amount
        if bound is None or usage <= bound:
            break
        lower = bound
    if senior and customer_class == "residential" and first_tier is not None:
        lines.append(("Senior discount", -_cents(first_tier / 2)))
    return lines


# --- Behaviour ------------------------------------------------------------------

def test_matches_reference_grid():
    classes = ["residential", "commercial", "irrigation"]
    usages = [0, 3, "4.0375", 7.31, 10, "10.33", 25, 30, "31.01", "47.5", 50, "51.7", 60, "123.456"]
    months = [1, 3, 4, 6, 8, 9, 11]
    days = [28, 29, 30, 31]
    for c, u, m, d, s in itertools.product(classes, usages, months, days, [False, True]):
        got = compute_bill(c, u, m, days=d, senior=s)
        want = _reference(c, u, m, days=d, senior=s)
        assert got == want, (c, u, m, d, s, got, want)
        assert bill_total(got) == sum((a for _, a in want), Decimal("0.00"))


def test_validation():
    for args in [("residential", -1, 1), ("residential", 1, 0), ("residential", 1, 13), ("other", 1, 1)]:
        try:
            compute_bill(*args)
        except ValueError:
            continue
        raise AssertionError("expected ValueError for %r" % (args,))
    try:
        compute_bill("residential", 1, 1, days=0)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for days=0")


# --- The tempting constraint: only line amounts are rounded, half-up -------------

def test_line_rounding_is_half_up():
    # 4.0375 * 1.20 = 4.845 exactly: half-up gives 4.85, half-even gives 4.84.
    assert ("Tier 1", Decimal("4.85")) in compute_bill("residential", "4.0375", 1)
    # 10 * 1.95 * 1.15 = 22.425: half-up 22.43 (half-even 22.42, rounded rate 2.24 -> 22.40).
    assert ("Tier 2", Decimal("22.43")) in compute_bill("commercial", 60, 7)


def test_surcharged_rate_is_not_rounded():
    # 10 * (1.85 * 1.15 = 2.1275) = 21.275 -> 21.28; a pre-rounded rate 2.13 gives 21.30.
    assert ("Tier 2", Decimal("21.28")) in compute_bill("residential", 20, 7)


def test_prorated_limit_is_not_rounded():
    # 31-day period: tier 1 ends at 10.333..., so 10.33 m3 is all tier 1.
    assert compute_bill("residential", "10.33", 2, days=31) == [
        ("Service charge", Decimal("8.00")),
        ("Tier 1", Decimal("12.40")),
    ]


def test_float_usage_goes_through_str():
    # Decimal(4.0375) is 4.03749999..., which would round to 4.84.
    assert ("Tier 1", Decimal("4.85")) in compute_bill("residential", 4.0375, 1)


# --- Edge cases -------------------------------------------------------------------

def test_usage_on_tier_boundary_has_no_empty_line():
    assert [l for l, _ in compute_bill("residential", 10, 1)] == ["Service charge", "Tier 1"]
    assert [l for l, _ in compute_bill("residential", 30, 7)] == ["Service charge", "Tier 1", "Tier 2"]
    assert [l for l, _ in compute_bill("commercial", 50, 7)] == ["Service charge", "Tier 1"]


def test_irrigation_off_season_with_no_usage_is_empty():
    lines = compute_bill("irrigation", 0, 12)
    assert lines == []
    assert bill_total(lines) == Decimal("0.00")


def test_senior_flag_only_affects_residential_with_usage():
    assert compute_bill("residential", 0, 1, senior=True) == [("Service charge", Decimal("8.00"))]
    assert compute_bill("commercial", 5, 1, senior=True) == compute_bill("commercial", 5, 1)
    assert ("Senior discount", Decimal("-4.39")) in compute_bill("residential", 7.31, 1, senior=True)


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print("ok  ", t.__name__)
    print("%d passed" % len(tests))
