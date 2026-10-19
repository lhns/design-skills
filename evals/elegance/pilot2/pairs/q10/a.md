# Candidate A

```python
def members(group):
    """Everyone in `group`, directly or through nested groups. A group loop (#118) is harmless."""
    people, seen, todo = set(), set(), [group]
    while todo:
        g = todo.pop()
        if g in seen:
            continue
        seen.add(g)
        people |= g.people
        todo.extend(g.subgroups)
    return people


def has_permission(person, permission):
    return any(person in members(g) for g in permission.groups)
```
