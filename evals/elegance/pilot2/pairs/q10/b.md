# Candidate B

```python
import logging

log = logging.getLogger(__name__)

# Nesting deeper than this is treated as a group loop (#118). The deepest chain we
# have is Parks > Grounds > Crew > Seasonal.
MAX_DEPTH = 3


def members(group, depth=0):
    """Everyone in `group`, directly or through nested groups."""
    if depth > MAX_DEPTH:
        log.warning("groups nested deeper than %d under %s; skipping", MAX_DEPTH, group.name)
        return set()
    people = set(group.people)
    for sub in group.subgroups:
        people |= members(sub, depth + 1)
    return people


def has_permission(person, permission):
    return any(person in members(g) for g in permission.groups)
```
