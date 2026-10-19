"""Hidden tests for h2 (judge only). Run with `python -m pytest` or `python test_hidden.py`.

Imports fares.py from ../fixture by default; set TARGET_DIR to test another copy.
All tests pass on the original fixture. The requested #402 fix is checked separately
in test_bugfix.py.
"""

import datetime
import itertools
import os
import sys
from decimal import Decimal, ROUND_CEILING

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("TARGET_DIR", os.path.join(_HERE, os.pardir, "fixture")))

from fares import quote, total  # noqa: E402

D = datetime.date

# --- Independent reference (with #402 fixed) ------------------------------------

_FARES = {  # category: (low, shoulder, high)
    "adult": ("18.00", "22.00", "27.50"),
    "child": ("9.00", "11.00", "13.50"),
    "infant": ("0.00", "0.00", "0.00"),
}
_CAR = ("45.00", "55.00", "68.00")
_VAN = ("70.00", "85.00", "105.00")
_PER_METRE = ("12.00", "14.00", "17.00")


def _season(d):
    if d.month in (7, 8):
        return 2
    if d.month in (5, 6, 9):
        return 1
    return 0


def _age(b, d):
    return d.year - b.year - ((d.month, d.day) < (b.month, b.day))


def _category(age):
    return "infant" if age < 4 else "child" if age < 16 else "adult"


def _reference(outbound, passengers, length=None, return_date=None):
    if length is not None:
        length = Decimal(str(length))
    s = _season(outbound)  # one pricing date for the whole booking
    counts = {"adult": 0, "child": 0, "infant": 0}
    for b in passengers:
        counts[_category(_age(b, outbound))] += 1
    lines = []
    for leg in ["Outbound"] + (["Return"] if return_date is not None else []):
        for cat in ("adult", "child", "infant"):
            if counts[cat]:
                lines.append(("%s: %d x %s" % (leg, counts[cat], cat), counts[cat] * Decimal(_FARES[cat][s])))
        if length is not None:
            if length <= Decimal("5.00"):
                lines.append(("%s: vehicle (car)" % leg, Decimal(_CAR[s])))
            elif length <= Decimal("7.00"):
                lines.append(("%s: vehicle (van)" % leg, Decimal(_VAN[s])))
            else:
                m = length.to_integral_value(rounding=ROUND_CEILING)
                lines.append(("%s: vehicle (long, %d m)" % (leg, m), m * Decimal(_PER_METRE[s])))
    lines.append(("Booking fee", Decimal("2.50")))
    return lines


# --- Behaviour ------------------------------------------------------------------

def test_matches_reference_grid():
    outbounds = [D(2026, 1, 20), D(2026, 4, 30), D(2026, 5, 1), D(2026, 6, 30), D(2026, 7, 1),
                 D(2026, 8, 31), D(2026, 9, 1), D(2026, 9, 30), D(2026, 10, 1)]
    returns = [None, 0, 2, 40]  # days after the outbound date
    adult = D(1980, 1, 1)
    passenger_lists = [
        [adult],
        [adult, D(2015, 3, 3), D(2024, 2, 2)],
        [adult, D(2010, 9, 1)],  # child turns 16 on 1 Sep 2026
        [D(2022, 7, 1), D(2022, 5, 1), D(2010, 7, 2)],  # infant turns 4 on 1 Jul 2026
        [adult, adult, D(2012, 5, 2), D(2012, 5, 2), D(2025, 1, 1)],
    ]
    lengths = [None, 4.2, 5.01, 7, "7.00", 7.01, 8, "8.0", 12.3, 18.75]
    for o, r, p, v in itertools.product(outbounds, returns, passenger_lists, lengths):
        rd = None if r is None else o + datetime.timedelta(days=r)
        got = quote(o, p, v, rd)
        want = _reference(o, p, v, rd)
        assert got == want, (o, rd, p, v, got, want)
        assert total(got) == sum((a for _, a in want), Decimal("0.00"))


def test_return_priced_at_outbound_season():
    lines = quote(D(2026, 8, 31), [D(1990, 1, 1)], 4, D(2026, 9, 2))
    assert lines == [
        ("Outbound: 1 x adult", Decimal("27.50")),
        ("Outbound: vehicle (car)", Decimal("68.00")),
        ("Return: 1 x adult", Decimal("27.50")),
        ("Return: vehicle (car)", Decimal("68.00")),
        ("Booking fee", Decimal("2.50")),
    ]
    assert total(lines) == Decimal("193.50")
    # and the other way round: outbound in the shoulder season, return in high season
    lines = quote(D(2026, 6, 30), [D(1990, 1, 1)], None, D(2026, 7, 2))
    assert [a for _, a in lines] == [Decimal("22.00"), Decimal("22.00"), Decimal("2.50")]


def test_return_uses_ages_on_outbound_date():
    # turns 16 on 1 Sep: outbound 31 Aug is a child, and so is the return leg on 2 Sep
    lines = quote(D(2026, 8, 31), [D(2010, 9, 1)], None, D(2026, 9, 2))
    assert [l for l, _ in lines] == ["Outbound: 1 x child", "Return: 1 x child", "Booking fee"]
    assert lines[1][1] == Decimal("13.50")
    # turns 4 on 1 Jul: infant on both legs
    lines = quote(D(2026, 6, 30), [D(2022, 7, 1), D(1990, 1, 1)], None, D(2026, 7, 2))
    assert lines == [
        ("Outbound: 1 x adult", Decimal("22.00")),
        ("Outbound: 1 x infant", Decimal("0.00")),
        ("Return: 1 x adult", Decimal("22.00")),
        ("Return: 1 x infant", Decimal("0.00")),
        ("Booking fee", Decimal("2.50")),
    ]


def test_single_uses_its_own_date():
    lines = quote(D(2026, 9, 2), [D(1990, 1, 1)])
    assert lines[0] == ("Outbound: 1 x adult", Decimal("22.00"))
    assert quote(D(2026, 8, 31), [D(1990, 1, 1)])[0][1] == Decimal("27.50")


def test_birthday_on_travel_date():
    def cats(travel, birth):
        return [l for l, _ in quote(travel, [birth])][:-1]

    assert cats(D(2026, 5, 10), D(2010, 5, 10)) == ["Outbound: 1 x adult"]
    assert cats(D(2026, 5, 9), D(2010, 5, 10)) == ["Outbound: 1 x child"]
    assert cats(D(2026, 5, 10), D(2022, 5, 10)) == ["Outbound: 1 x child"]
    assert cats(D(2026, 5, 9), D(2022, 5, 10)) == ["Outbound: 1 x infant"]
    # born 29 Feb: 15 on 28 Feb 2028 (child), 16 on 29 Feb 2028 (adult)
    assert cats(D(2028, 2, 28), D(2012, 2, 29)) == ["Outbound: 1 x child"]
    assert cats(D(2028, 2, 29), D(2012, 2, 29)) == ["Outbound: 1 x adult"]
    # born 29 Feb 2024: still 3 on 28 Feb 2028, 4 on 29 Feb 2028
    assert cats(D(2028, 2, 28), D(2024, 2, 29)) == ["Outbound: 1 x infant"]
    assert cats(D(2028, 2, 29), D(2024, 2, 29)) == ["Outbound: 1 x child"]
    # non-leap year: born 29 Feb 2012 is 14 on 28 Feb 2027 and 15 on 1 Mar 2027
    assert cats(D(2027, 2, 28), D(2012, 2, 29)) == ["Outbound: 1 x child"]
    assert cats(D(2027, 3, 1), D(2012, 2, 29)) == ["Outbound: 1 x child"]


def test_infant_line_printed_at_zero():
    lines = quote(D(2026, 3, 3), [D(1990, 1, 1), D(2025, 1, 1), D(2025, 6, 6)])
    assert lines == [
        ("Outbound: 1 x adult", Decimal("18.00")),
        ("Outbound: 2 x infant", Decimal("0.00")),
        ("Booking fee", Decimal("2.50")),
    ]
    only_infant = quote(D(2026, 3, 3), [D(2025, 1, 1)])
    assert only_infant == [("Outbound: 1 x infant", Decimal("0.00")), ("Booking fee", Decimal("2.50"))]


def test_long_vehicle_started_metre():
    def label(length):
        return quote(D(2026, 1, 15), [D(1990, 1, 1)], length)[1]

    assert label(8) == ("Outbound: vehicle (long, 8 m)", Decimal("96.00"))
    assert label("8.0") == ("Outbound: vehicle (long, 8 m)", Decimal("96.00"))
    assert label(8.0) == ("Outbound: vehicle (long, 8 m)", Decimal("96.00"))
    assert label("8.01") == ("Outbound: vehicle (long, 9 m)", Decimal("108.00"))
    assert label(8.1) == ("Outbound: vehicle (long, 9 m)", Decimal("108.00"))
    assert label(7.1) == ("Outbound: vehicle (long, 8 m)", Decimal("96.00"))
    assert label(18.75) == ("Outbound: vehicle (long, 19 m)", Decimal("228.00"))


def test_validation():
    ok = D(1990, 1, 1)
    cases = [
        (D(2026, 5, 5), []),
        (D(2026, 5, 5), [D(2026, 5, 6)]),
        (D(2026, 5, 5), [ok], None, D(2026, 5, 4)),
        (D(2026, 5, 5), [ok], 0),
        (D(2026, 5, 5), [ok], "0"),
        (D(2026, 5, 5), [ok], -3),
        (D(2026, 5, 5), [ok], 18.76),
        (D(2026, 5, 5), [ok], 20),
    ]
    for args in cases:
        try:
            quote(*args)
        except ValueError:
            continue
        raise AssertionError("expected ValueError for %r" % (args,))
    quote(D(2026, 5, 5), [D(2026, 5, 5)], 18.75, D(2026, 5, 5))  # all on the limits: valid


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print("ok  ", t.__name__)
        except AssertionError as e:
            failed += 1
            print("FAIL", t.__name__, str(e)[:120])
    print("%d passed, %d failed" % (len(tests) - failed, failed))
    sys.exit(1 if failed else 0)
