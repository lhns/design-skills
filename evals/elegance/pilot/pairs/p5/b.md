# Candidate B

```python
# The factory chart, copied as published.
UK_TO_EU = {
    3: 35.5, 3.5: 36, 4: 37, 4.5: 37.5, 5: 38, 5.5: 38.5,
    6: 39, 6.5: 40, 7: 40.5, 7.5: 41, 8: 42,
}
EU_TO_UK = {eu: uk for uk, eu in UK_TO_EU.items()}


def uk_to_eu(uk):
    try:
        return UK_TO_EU[uk]
    except KeyError:
        raise ValueError(f"no such UK size: {uk}") from None


def eu_to_uk(eu):
    try:
        return EU_TO_UK[eu]
    except KeyError:
        raise ValueError(f"no such EU size: {eu}") from None
```
