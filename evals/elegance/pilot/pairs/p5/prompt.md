# Shoe size conversion for one last

A small shoemaker sells one women's shoe model, built on a single last, in UK sizes 3 to 8. The web shop needs to convert between UK and EU sizes in both directions. The factory's chart is authoritative:

| UK | 3 | 3.5 | 4 | 4.5 | 5 | 5.5 | 6 | 6.5 | 7 | 7.5 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EU | 35.5 | 36 | 37 | 37.5 | 38 | 38.5 | 39 | 40 | 40.5 | 41 | 42 |

Constraints:

1. Both directions match the chart exactly.
2. A size not on the chart is rejected with `ValueError`, in either direction.
3. Sizes arrive as numbers (`6`, `6.0` and `6.5` are all possible).
4. The chart was set by hand at the factory years ago. Rows get adjusted individually after fitting complaints: twice in the last three years, each time moving one EU value by half a size.

Two candidate implementations follow. Which one is the better design?
