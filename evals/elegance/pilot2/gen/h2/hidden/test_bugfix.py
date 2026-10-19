"""Hidden check of the requested bug fix (#402) for h2 (judge only).

Fails on the original fixture by design; must pass after the refactor.
Imports fares.py from ../fixture by default; set TARGET_DIR to test another copy.
"""

import datetime
import os
import sys
from decimal import Decimal

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("TARGET_DIR", os.path.join(_HERE, os.pardir, "fixture")))

from fares import quote  # noqa: E402

D = datetime.date


def test_car_up_to_and_including_5m():
    """#402: cars are up to and including 5.00 m, on singles and returns."""
    for length in (5, 5.0, "5.00", Decimal("5.00")):
        single = quote(D(2026, 5, 20), [D(1990, 1, 1)], length)
        assert single[1] == ("Outbound: vehicle (car)", Decimal("55.00")), (length, single)
        ret = quote(D(2026, 5, 20), [D(1990, 1, 1)], length, D(2026, 5, 22))
        assert ("Outbound: vehicle (car)", Decimal("55.00")) in ret
        assert ("Return: vehicle (car)", Decimal("55.00")) in ret
    assert quote(D(2026, 5, 20), [D(1990, 1, 1)], "5.01")[1][0] == "Outbound: vehicle (van)"


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
