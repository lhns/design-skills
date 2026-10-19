"""Ticket prices for the island ferry."""

from decimal import Decimal, ROUND_CEILING


def quote(outbound, passengers, vehicle_length_m=None, return_date=None):
    """Return the bill as a list of (label, amount) lines, in print order.

    outbound and return_date are datetime.date; passengers is a list of birth dates.
    Amounts are Decimals. The bill total is the sum of the lines (see total()).
    """
    if not passengers:
        raise ValueError("at least one passenger is required")
    for b in passengers:
        if b > outbound:
            raise ValueError("birth date after travel date")
    if return_date is not None and return_date < outbound:
        raise ValueError("return before outbound")
    length = None
    if vehicle_length_m is not None:
        length = Decimal(str(vehicle_length_m))
        # the longest lane on the vessel
        if length <= 0 or length > Decimal("18.75"):
            raise ValueError("vehicle length out of range")

    lines = []

    if return_date is None:
        # single trip
        d = outbound
        if d.month in (7, 8):
            season = "high"
        elif d.month in (5, 6, 9):
            season = "shoulder"
        else:
            season = "low"
        adults = children = infants = 0
        for b in passengers:
            age = d.year - b.year - ((d.month, d.day) < (b.month, b.day))
            if age < 4:
                infants += 1
            elif age < 16:
                children += 1
            else:
                adults += 1
        if adults:
            if season == "high":
                fare = Decimal("27.50")
            elif season == "shoulder":
                fare = Decimal("22.00")
            else:
                fare = Decimal("18.00")
            lines.append(("Outbound: %d x adult" % adults, adults * fare))
        if children:
            if season == "high":
                fare = Decimal("13.50")
            elif season == "shoulder":
                fare = Decimal("11.00")
            else:
                fare = Decimal("9.00")
            lines.append(("Outbound: %d x child" % children, children * fare))
        if infants:
            lines.append(("Outbound: %d x infant" % infants, infants * Decimal("0.00")))
        if length is not None:
            if length < Decimal("5.00"):
                if season == "high":
                    price = Decimal("68.00")
                elif season == "shoulder":
                    price = Decimal("55.00")
                else:
                    price = Decimal("45.00")
                lines.append(("Outbound: vehicle (car)", price))
            elif length <= Decimal("7.00"):
                if season == "high":
                    price = Decimal("105.00")
                elif season == "shoulder":
                    price = Decimal("85.00")
                else:
                    price = Decimal("70.00")
                lines.append(("Outbound: vehicle (van)", price))
            else:
                metres = length.to_integral_value(rounding=ROUND_CEILING)
                if season == "high":
                    per_m = Decimal("17.00")
                elif season == "shoulder":
                    per_m = Decimal("14.00")
                else:
                    per_m = Decimal("12.00")
                lines.append(("Outbound: vehicle (long, %d m)" % metres, metres * per_m))
    else:
        # return trip
        # TODO: should the return leg use its own date?
        if outbound.month in (7, 8):
            season = "high"
        elif outbound.month in (5, 6, 9):
            season = "shoulder"
        else:
            season = "low"
        adults = children = infants = 0
        for b in passengers:
            age = outbound.year - b.year - ((outbound.month, outbound.day) < (b.month, b.day))
            if age < 4:
                infants += 1
            elif age < 16:
                children += 1
            else:
                adults += 1
        for leg in ("Outbound", "Return"):
            if adults:
                if season == "high":
                    fare = Decimal("27.50")
                elif season == "shoulder":
                    fare = Decimal("22.00")
                else:
                    fare = Decimal("18.00")
                lines.append(("%s: %d x adult" % (leg, adults), adults * fare))
            if children:
                if season == "high":
                    fare = Decimal("13.50")
                elif season == "shoulder":
                    fare = Decimal("11.00")
                else:
                    fare = Decimal("9.00")
                lines.append(("%s: %d x child" % (leg, children), children * fare))
            if infants:
                lines.append(("%s: %d x infant" % (leg, infants), infants * Decimal("0.00")))
            if length is not None:
                if length <= Decimal("5.00"):
                    if season == "high":
                        price = Decimal("68.00")
                    elif season == "shoulder":
                        price = Decimal("55.00")
                    else:
                        price = Decimal("45.00")
                    lines.append(("%s: vehicle (car)" % leg, price))
                elif length <= Decimal("7.00"):
                    if season == "high":
                        price = Decimal("105.00")
                    elif season == "shoulder":
                        price = Decimal("85.00")
                    else:
                        price = Decimal("70.00")
                    lines.append(("%s: vehicle (van)" % leg, price))
                else:
                    metres = length.to_integral_value(rounding=ROUND_CEILING)
                    if season == "high":
                        per_m = Decimal("17.00")
                    elif season == "shoulder":
                        per_m = Decimal("14.00")
                    else:
                        per_m = Decimal("12.00")
                    lines.append(("%s: vehicle (long, %d m)" % (leg, metres), metres * per_m))

    lines.append(("Booking fee", Decimal("2.50")))
    return lines


def total(lines):
    """Sum of the line amounts."""
    result = Decimal("0.00")
    for _, amount in lines:
        result += amount
    return result
