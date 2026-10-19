#!/usr/bin/env python3
"""Grade a pilot run: parse rating winners, blind-judge gen/audit/first outputs, write report.md + grades.json."""
import argparse, json, random, re, subprocess, sys, tempfile, threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import run as R  # shared paths, ledger and the lean claude call

JUDGE_SYS = "You are a strict, fair evaluator. Output JSON only."
JUDGE_MODEL = "opus"
SCRUB = [(re.compile(p, re.I), "the guide") for p in
         (r"design[- ]by[- ]collapse", r"collapse", r"elegance", r"clean[- ]code", r"design[- ]process")]
TEXT_EXT = {".md", ".py", ".yaml", ".yml", ".txt", ".json", ".toml", ".csv", ""}
MAX_FILE = 30_000


def load_yaml(path):
    text = Path(path).read_text(encoding="utf-8")
    try:
        import yaml
        return yaml.safe_load(text)
    except ImportError:  # flat `key: value` fallback, enough for rating truth
        return {k.strip(): v.strip().strip("'\"") for k, _, v in (l.partition(":") for l in text.splitlines()
                                                                  if ":" in l and not l.startswith("#"))}


def scrub(t):
    for rx, rep in SCRUB:
        t = rx.sub(rep, t)
    return t


def files_block(d):
    """Text of every file under d (relative paths), scrubbed; paths carry no condition information."""
    parts = []
    for p in sorted(Path(d).rglob("*")):
        if p.is_file() and p.suffix in TEXT_EXT:
            parts.append(f"--- FILE {scrub(str(p.relative_to(d)).replace(chr(92), '/'))} ---\n"
                         + scrub(p.read_text(encoding="utf-8", errors="replace"))[:MAX_FILE])
    return "\n\n".join(parts) or "(no files)"


def extract_json(text):
    a, b = text.find("{"), text.rfind("}")
    try:
        return json.loads(text[a:b + 1])
    except ValueError:
        return None


def judge(run_id, track, prompt):
    res = R.lean_call(JUDGE_SYS, prompt, JUDGE_MODEL, timeout=600)
    R.ledger_add(run_id, R.SKILL_OF_TRACK[track], res["tokens"])
    return extract_json(res["text"]) or {"error": "unparsable judge output", "raw": res["text"][:500]}


# ---------- per-track grading ----------
def grade_rating(m):
    pair = R.PAIRS / m["item"]
    truth = load_yaml(pair / "truth.yaml")
    hits = re.findall(r"WINNER:\s*([12])", m["final_text"] or "")
    if not hits:
        return {"parsed": False, "kind": truth.get("kind")}
    shown_first = "a" if m["order"] == "ab" else "b"
    other = "b" if shown_first == "a" else "a"
    pick = shown_first if hits[-1] == "1" else other
    return {"parsed": True, "correct": pick == str(truth["better"]).lower(), "kind": truth.get("kind"),
            "longer": truth.get("longer")}


def hidden_tests(m, run_dir):
    hidden = R.GEN / m["item"] / "hidden" / "test_hidden.py"
    if not hidden.exists():
        return None
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        if (R.GEN / m["item"] / "fixture").is_dir():
            R.shutil.copytree(R.GEN / m["item"] / "fixture", d, dirs_exist_ok=True)
        if (run_dir / "output").is_dir():
            R.shutil.copytree(run_dir / "output", d, dirs_exist_ok=True)
        R.shutil.copy(hidden, d / "test_hidden.py")
        for cmd in ([sys.executable, "-m", "pytest", "-q", "test_hidden.py"], [sys.executable, "test_hidden.py"]):
            try:
                p = subprocess.run(cmd, cwd=d, capture_output=True, text=True, timeout=120,
                                   env={**R.os.environ, "BILLING_DIR": str(d)})
            except subprocess.TimeoutExpired:
                return False
            if "No module named pytest" not in p.stderr:
                return p.returncode == 0
    return False


def grade_gen(m, run_dir, run_id):
    d = R.GEN / m["item"]
    prompt = f"""Judge a solution to the task below. You see only the task, the judge-only check, and the solution.

TASK:
{R.read(d / 'task.md')}

JUDGE-ONLY CHECK:
{R.read(d / 'check.md')}

SOLUTION REPLY:
{scrub(m['final_text'] or '')}

SOLUTION FILES:
{files_block(run_dir / 'output')}

Reply with JSON only: {{"constraints_held": n, "constraints_total": n, "traps": [{{"name": "...", "pass": true}}],
"concepts": n, "special_cases": n, "duplicated_facts": n, "notes": "..."}}
Count concepts, special cases (exception clauses) and facts stated in two places as the check describes."""
    g = judge(run_id, "gen", prompt)
    g["hidden_pass"] = hidden_tests(m, run_dir)
    return g


def audit_truth(item):
    t = load_yaml(R.AUDIT / "truth.yaml")
    if isinstance(t, list):  # list of {doc: a1, ...} entries
        t = [e for e in t if str(e.get("doc", e.get("item", e.get("id", "")))).replace(".md", "") == item]
    elif isinstance(t, dict):
        t = next((v for k, v in t.items() if str(k).replace(".md", "") == item), [])
        t = t.get("errors", []) if isinstance(t, dict) else t
    return t or []


def grade_audit(m, run_dir, run_id):
    truth = audit_truth(m["item"])
    listing = "\n".join(f"{i}: {json.dumps(e) if not isinstance(e, str) else e}" for i, e in enumerate(truth)) or "(none: clean document)"
    prompt = f"""A reviewer was asked to find planted decision-record errors in this document.

DOCUMENT:
{R.read(R.AUDIT / (m['item'] + '.md'))}

TRUE ERRORS (index: description):
{listing}

REVIEWER OUTPUT:
{scrub(m['final_text'] or '')}

For each PROBLEM the reviewer listed, say which true error index it identifies (same defect in the same place), or null if it matches none. Reply with JSON only: {{"found": [{{"truth_index": 0, "text": "..."}}]}}. Use an empty list for NO PROBLEMS."""
    g = judge(run_id, "audit", prompt)
    found = g.get("found") or []
    hit = {f["truth_index"] for f in found if isinstance(f, dict) and isinstance(f.get("truth_index"), int)}
    g.update(truth_total=len(truth), matched=len(hit), false_alarms=sum(1 for f in found if not isinstance(f, dict) or f.get("truth_index") is None))
    return g


def grade_first(m, run_dir, run_id):
    d = R.FIRST / m["item"]
    prompt = f"""Judge a designer's first session. You see the brief, the judge-only check, the designer's files and final reply.

BRIEF:
{R.read(d / 'brief.md')}

JUDGE-ONLY CHECK:
{R.read(d / 'check.md')}

DESIGNER FILES:
{files_block(run_dir / 'output')}

FINAL REPLY:
{scrub(m['final_text'] or '')}

Reply with JSON only: {{"traps": [{{"name": "...", "pass": true, "evidence": "..."}}], "question_is_good": true}}"""
    return judge(run_id, "first", prompt)


# ---------- report ----------
def mean(xs):
    xs = [x for x in xs if x is not None]
    return f"{sum(xs) / len(xs):.2f}" if xs else "-"


def pct(a, b):
    return f"{100 * a / b:.0f}% ({a}/{b})" if b else "-"


def table(head, rows):
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] + ["| " + " | ".join(map(str, r)) + " |" for r in rows]) + "\n"


def group(metas, key):
    g = defaultdict(list)
    for m in metas:
        g[key(m)].append(m)
    return sorted(g.items())


def trap_rate(g):
    t = [x for x in g.get("traps") or [] if isinstance(x, dict)]
    return sum(bool(x.get("pass")) for x in t), len(t)


def summarize(track, ms, grades):
    G = lambda m: grades.get(m["run_id"], {})
    rows = []
    for (cond, model), xs in group(ms, lambda m: (m["condition"], m["model"])):
        gs = [G(m) for m in xs if G(m) and "error" not in G(m)]
        if track == "rating":
            ok = sum(g.get("correct", False) for g in gs)
            parsed = sum(g.get("parsed", False) for g in gs)
            rows.append([cond, model, len(xs), pct(ok, parsed), len(gs) - parsed])
        elif track == "gen":
            h, t = sum(g.get("constraints_held", 0) for g in gs), sum(g.get("constraints_total", 0) for g in gs)
            tp = [trap_rate(g) for g in gs]
            hid = [g["hidden_pass"] for g in gs if g.get("hidden_pass") is not None]
            rows.append([cond, model, len(gs), pct(h, t), pct(sum(a for a, _ in tp), sum(b for _, b in tp)),
                         mean([g.get("concepts") for g in gs]), mean([g.get("special_cases") for g in gs]),
                         mean([g.get("duplicated_facts") for g in gs]), pct(sum(hid), len(hid))])
        elif track == "audit":
            clean = [g for g in gs if g["truth_total"] == 0]
            rows.append([cond, model, len(gs), pct(sum(g["matched"] for g in gs), sum(g["truth_total"] for g in gs)),
                         mean([g["false_alarms"] for g in gs]), pct(sum(g["false_alarms"] > 0 for g in clean), len(clean))])
        else:
            tp = [trap_rate(g) for g in gs]
            rows.append([cond, model, len(gs), pct(sum(a for a, _ in tp), sum(b for _, b in tp)),
                         pct(sum(bool(g.get("question_is_good")) for g in gs), len(gs))])
    head = {"rating": ["condition", "model", "runs", "accuracy", "unparsable"],
            "gen": ["condition", "model", "n", "constraints held", "traps passed", "concepts", "special cases", "dup facts", "hidden tests"],
            "audit": ["condition", "model", "n", "detection", "false alarms/doc", "clean docs with alarm"],
            "first": ["condition", "model", "n", "traps passed", "good question"]}[track]
    out = table(head, rows)
    if track == "rating":
        kinds = sorted({G(m).get("kind") for m in ms if G(m)} - {None}, key=str)
        conds = sorted({m["condition"] for m in ms})
        kr = []
        for k in kinds:
            row = [k]
            for c in conds:
                gs = [G(m) for m in ms if m["condition"] == c and G(m).get("kind") == k]
                row.append(pct(sum(g.get("correct", False) for g in gs), sum(g.get("parsed", False) for g in gs)))
            kr.append(row)
        out += "\nAccuracy by kind (models pooled):\n\n" + table(["kind"] + conds, kr)
    return out


def cost_table(ms):
    rows = []
    for (track, cond), xs in group(ms, lambda m: (m["track"], m["condition"])):
        full = [m for m in xs if m.get("mode") == "full"]
        inv = pct(sum(m["expected_skill"] in m["skills_invoked"] for m in full if m["expected_skill"]),
                  sum(1 for m in full if m["expected_skill"])) if full else "n/a (lean)"
        rows.append([track, cond, len(xs), mean([m.get("total_cost_usd") for m in xs]),
                     mean([(m.get("duration_ms") or 0) / 1000 for m in xs]), f"{sum(m.get('tokens', 0) for m in xs) // len(xs):,}", inv])
    return table(["track", "condition", "runs", "mean cost $", "mean sec", "mean tokens", "skill invoked"], rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--tracks", default="rating,gen,audit,first")
    ap.add_argument("--concurrency", type=int, default=4)
    a = ap.parse_args()
    root = R.RESULTS / a.run_id
    metas = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(root.glob("*/meta.json"))]
    metas = [m for m in metas if m["track"] in a.tracks.split(",")]
    gp = root / "grades.json"
    grades = json.loads(gp.read_text()) if gp.exists() else {}
    lock, ok = threading.Lock(), {}

    def do(m):
        rid = m["run_id"]
        if rid in grades and "error" not in grades[rid]:
            return
        if m["track"] == "rating":
            grades[rid] = grade_rating(m)
            return
        key = (m["track"], m["item"])
        with lock:  # budget skips whole items so conditions stay balanced
            if key not in ok:
                ok[key] = R.ledger_get(a.run_id, R.SKILL_OF_TRACK[m["track"]]) < R.BUDGET_STOP
        if not ok[key]:
            print("budget", rid)
            return
        fn = {"gen": grade_gen, "audit": grade_audit, "first": grade_first}[m["track"]]
        grades[rid] = fn(m, root / rid, a.run_id)
        print("graded", rid, flush=True)

    with ThreadPoolExecutor(a.concurrency) as ex:
        list(ex.map(do, metas))
    gp.write_text(json.dumps(grades, indent=1), encoding="utf-8")

    rep = [f"# Pilot report: {a.run_id}\n"]
    for track in R.TRACK_ORDER:
        ms = [m for m in metas if m["track"] == track]
        if ms:
            rep.append(f"## {track}\n\n" + summarize(track, ms, grades))
    rep.append("## Cost, duration, skill invocation\n\n" + cost_table(metas))
    led = json.loads((root / "ledger.json").read_text()) if (root / "ledger.json").exists() else {}
    rep.append("## Token ledger (cap 2,000,000 per skill)\n\n" + table(["skill", "tokens"], [[k, f"{v:,}"] for k, v in led.items()]))
    (root / "report.md").write_text("\n".join(rep), encoding="utf-8")
    print("wrote", root / "report.md")


if __name__ == "__main__":
    main()
