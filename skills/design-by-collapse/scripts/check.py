#!/usr/bin/env python3
"""Design-consistency checker. Usage: python check.py [DESIGN_DIR]  (default ./design)"""
import os
import re
import sys

try:
    import yaml
except ImportError:
    print("pip install pyyaml")
    sys.exit(2)

ID_RE = re.compile(r"^[KXW][0-9]+$")


def load(d, name):
    path = os.path.join(d, name)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def live_opts(fork):
    return [o["id"] for o in fork.get("options") or [] if not o.get("eliminated_by")]


def rule1(d, r):
    """eliminated_by: live K/X only, with why; preferred_by: W only."""
    for f in d["forks"]:
        for o in f.get("options") or []:
            at = f"{f['id']}/{o['id']}"
            elim = o.get("eliminated_by") or []
            for e in elim:
                if e.startswith("W"):
                    r["E"].append(f"[rule 1] {at}: {e} is a value; values only rank, they never eliminate")
                elif e not in d["items"]:
                    r["E"].append(f"[rule 1] {at}: eliminated_by {e} does not exist")
                elif e not in d["live"]:
                    r["E"].append(f"[rule 1] {at}: eliminated_by {e} is superseded/withdrawn")
            if elim and not o.get("why"):
                r["E"].append(f"[rule 1] {at}: eliminated_by without why")
            for p in o.get("preferred_by") or []:
                if not (p in d["items"] and p.startswith("W")):
                    r["E"].append(f"[rule 1] {at}: preferred_by {p} is not an existing W id")


def rule3(d, r):
    """chosen must not name an eliminated option. Returns the shifted fork ids."""
    shifted = set()
    for f in d["forks"]:
        opt = next((o for o in f.get("options") or [] if o["id"] == f.get("chosen")), None)
        if opt and opt.get("eliminated_by"):
            shifted.add(f["id"])
            r["E"].append(f"[rule 3] {f['id']}: chosen '{opt['id']}' is eliminated; design shifted: move the choice")
    return shifted


def rule2(d, r, shifted):
    """Forced / open / conflict forks."""
    for f in d["forks"]:
        fid, lo = f["id"], live_opts(f)
        if not lo:
            r["N"].append(f"[rule 2] {fid}: conflict, every option is eliminated")
        elif len(lo) == 1:
            if f.get("chosen") != lo[0] and fid not in shifted:
                r["E"].append(f"[rule 2] {fid}: forced to '{lo[0]}' but chosen is '{f.get('chosen')}'")
        else:
            miss = [k for k in ("question", "default", "decide_by") if not f.get(k)]
            if miss:
                r["E"].append(f"[rule 2] {fid}: open fork missing {', '.join(miss)}")
            if f.get("default") and f["default"] not in lo:
                r["E"].append(f"[rule 2] {fid}: default '{f['default']}' is not a live option")
            r["N"].append(f"[rule 2] {fid}: open, {f.get('question', '(no question)')} "
                          f"(default {f.get('default')}, decide by {f.get('decide_by')})")


def rule4(d, r):
    """forced concepts trace to live K; detail concepts attach to the chosen option."""
    forks = {f["id"]: f for f in d["forks"]}
    for c in d["concepts"]:
        cid = c["id"]
        if c.get("verdict") == "forced":
            traces = c.get("traces") or []
            if not traces:
                r["E"].append(f"[rule 4] {cid}: forced concept has no traces")
            for t in traces:
                if not (t.startswith("K") and t in d["live"]):
                    r["E"].append(f"[rule 4] {cid}: trace {t} is not a live K id")
        elif c.get("verdict") == "detail":
            da = c.get("detail_of")
            if not da:
                r["E"].append(f"[rule 4] {cid}: floating, detail concept has no detail_of")
                continue
            fid, _, oid = da.partition("/")
            f = forks.get(fid)
            if not f or oid not in [o["id"] for o in f.get("options") or []]:
                r["E"].append(f"[rule 4] {cid}: detail_of {da} names no existing fork/option")
            elif oid not in live_opts(f) or oid != f.get("chosen"):
                r["E"].append(f"[rule 4] {cid}: stranded: re-attach or delete ({da} is not the live chosen option)")


def rule5(d, r, raw_items):
    """kernel ids valid and unique; from and superseded_by resolve."""
    seen = set()
    for it in raw_items:
        i = str(it.get("id"))
        if not ID_RE.match(i):
            r["E"].append(f"[rule 5] {i}: invalid id format")
        if i in seen:
            r["E"].append(f"[rule 5] {i}: duplicate id")
        seen.add(i)
        for v in it.get("from") or []:
            if v not in d["vision"]:
                r["E"].append(f"[rule 5] {i}: from {v} not found in vision.md")
        if it.get("status") == "superseded":
            s = it.get("superseded_by")
            if not s or s not in d["live"]:
                r["E"].append(f"[rule 5] {i}: superseded_by '{s}' is missing or not a live item")


def rule6(d, r):
    """Ratchet: a rising metric needs justification by live K ids."""
    rounds = d["rounds"]
    for prev, cur in zip(rounds, rounds[1:]):
        for m, v in (cur.get("counts") or {}).items():
            p = (prev.get("counts") or {}).get(m)
            if p is not None and v > p:
                ids = (cur.get("justified") or {}).get(m) or []
                if not ids or not all(k.startswith("K") and k in d["live"] for k in ids):
                    r["E"].append(f"[rule 6] round {cur.get('round')}: {m} rose {p}->{v} "
                                  f"without live K ids in justified")
    if rounds and rounds[-1].get("kernel_items") != len(d["live"]):
        r["W"].append(f"[rule 6] round {rounds[-1].get('round')}: kernel changed since last count: "
                      f"recount (counted {rounds[-1].get('kernel_items')}, now {len(d['live'])})")


def rule7(d, r):
    """A live kernel answer must leave its fork with exactly one live option."""
    forks = {f["id"]: f for f in d["forks"]}
    for i, it in d["items"].items():
        a = it.get("answers")
        if a and i in d["live"] and (a not in forks or len(live_opts(forks[a])) != 1):
            r["E"].append(f"[rule 7] {i}: answers {a} but answer not propagated "
                          f"(fork must exist with exactly one live option)")


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "design"
    r = {"E": [], "W": [], "N": []}
    texts = {n: load(base, n) for n in ("vision.md", "kernel.yaml", "forks.yaml", "concepts.yaml")}
    for n, t in texts.items():
        if t is None:
            r["E"].append(f"missing file {n}")

    def parse(n):
        return (yaml.safe_load(texts[n]) or {}) if texts[n] else {}

    raw_items = parse("kernel.yaml").get("items") or []
    concepts = parse("concepts.yaml")
    items = {}
    for it in raw_items:
        items.setdefault(str(it.get("id")), it)
    d = {
        "vision": set(re.findall(r"^\|\s*([A-Z]+[0-9]+)\s*\|", texts["vision.md"] or "", re.M)),
        "items": items,
        "live": {i for i, it in items.items() if it.get("status", "live") == "live"},
        "forks": parse("forks.yaml").get("forks") or [],
        "concepts": concepts.get("concepts") or [],
        "rounds": concepts.get("rounds") or [],
    }
    rule1(d, r)
    rule2(d, r, rule3(d, r))
    rule4(d, r)
    rule5(d, r, raw_items)
    rule6(d, r)
    rule7(d, r)
    for title, key in (("ERRORS", "E"), ("WARNINGS", "W"), ("NEEDS OWNER", "N")):
        if r[key]:
            print(f"{title} ({len(r[key])})")
            print("\n".join("  " + m for m in r[key]))
    n = [len(live_opts(f)) for f in d["forks"]]
    verdicts = {}
    for c in d["concepts"]:
        verdicts[c.get("verdict")] = verdicts.get(c.get("verdict"), 0) + 1
    last = d["rounds"][-1] if d["rounds"] else {}
    vs = ", ".join(f"{k} {v}" for k, v in sorted(verdicts.items(), key=str)) or "none"
    print(f"forks: {n.count(1)} forced, {sum(x >= 2 for x in n)} open, {n.count(0)} conflict | "
          f"concepts: {vs} | latest counts: {last.get('counts')}")
    sys.exit(1 if r["E"] else 0)


if __name__ == "__main__":
    main()
