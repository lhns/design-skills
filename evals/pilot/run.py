#!/usr/bin/env python3
"""Run the skill pilot: one isolated `claude -p` session per (track, item, condition, model, order).

Lean tracks (rating, audit): single turn, no tools, guidance injected as the system prompt.
Full tracks (gen, first): real harness session in a temp git repo with the skills installed.
"""
import argparse, hashlib, json, os, shutil, stat, subprocess, tempfile, threading, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS = Path(__file__).resolve().parent / "results"
TIMEOUT = 15 * 60
FULL_ARGS = ["--setting-sources", "project", "--strict-mcp-config", "--tools", "Read,Write,Edit,Glob,Grep,Bash,Skill",
             "--disallowed-tools", "Agent", "--max-budget-usd", "3", "--effort", "high",
             "--permission-mode", "bypassPermissions", "--output-format", "stream-json", "--verbose"]

SKILL_SRC = {
    "elegance": ROOT / "skills/elegance",
    "design-by-collapse": ROOT / "skills/design-by-collapse",
    "clean-code": ROOT / "evals/elegance/placebo/clean-code",
    "design-process": ROOT / "evals/design-by-collapse/placebo/design-process",
}
# condition -> (installed skills, skill sentence for full mode); the last skill is the one under test
ELEGANCE_CONDS = {
    "plain": ([], ""),
    "placebo": (["clean-code"], "Use the clean-code skill."),
    "skill": (["elegance"], "Use the elegance skill."),
}
COLLAPSE_CONDS = {
    "elegance": (["elegance"], "Use the elegance skill."),
    "placebo": (["elegance", "design-process"], "Use the elegance and design-process skills."),
    "collapse": (["elegance", "design-by-collapse"], "Use the elegance and design-by-collapse skills."),
}
TRACK_CONDS = {"rating": ELEGANCE_CONDS, "gen": ELEGANCE_CONDS, "audit": COLLAPSE_CONDS, "first": COLLAPSE_CONDS}
TRACK_ORDER = ["rating", "audit", "gen", "first"]  # cheap lean tracks first
LEAN = {"rating", "audit"}
SKILL_OF_TRACK = {"rating": "elegance", "gen": "elegance", "audit": "design-by-collapse", "first": "design-by-collapse"}
BUDGET_STOP = 1_900_000
EST = {"lean": 4_000, "full": 150_000, "judge": 8_000}

PAIRS = GEN = AUDIT = FIRST = None
ITEMS = None


def set_items(items):
    """Point the item roots at evals/<skill>/<items>/ (wave 1: pilot, wave 2: pilot2)."""
    global PAIRS, GEN, AUDIT, FIRST, ITEMS
    ITEMS = items
    PAIRS = ROOT / f"evals/elegance/{items}/pairs"
    GEN = ROOT / f"evals/elegance/{items}/gen"
    AUDIT = ROOT / f"evals/design-by-collapse/{items}/audit"
    FIRST = ROOT / f"evals/design-by-collapse/{items}/first"


set_items("pilot")


def read(p):
    return Path(p).read_text(encoding="utf-8")


def models_for(track, item):
    if track == "rating":
        return ["opus", "sonnet"]
    if track == "gen":
        mp = GEN / item / "meta.yaml"
        if mp.exists():
            import yaml
            return [(yaml.safe_load(read(mp)) or {}).get("model", "opus")]
        return ["sonnet"] if ITEMS == "pilot" and item == "g2" else ["opus"]
    return ["opus"]


def item_ids(track):
    if track == "rating":
        return sorted(d.name for d in PAIRS.glob("*") if d.is_dir())
    if track == "gen":
        return sorted(d.name for d in GEN.glob("*") if d.is_dir())
    if track == "audit":
        return sorted(f.stem for f in AUDIT.glob("a*.md"))
    return sorted(d.name for d in FIRST.glob("*") if d.is_dir())


def base_prompt(track, item):
    if track == "gen":
        return (read(GEN / item / "task.md").rstrip() + "\n\nAim for an elegant result. "
                "No user is available: choose, and label your own design choices.")
    if track == "audit":
        return (read(AUDIT / f"{item}.md").rstrip() + "\n\nReview this design record for problems in how decisions "
                "were made and recorded. List each as `PROBLEM: <where>: <what is wrong>`, or write `NO PROBLEMS`.")
    return ("You are the designer. The stakeholder's brief follows; they will answer questions in later sessions. "
            "Keep the design and your notes in files under design/. End your reply with the one question you would "
            "ask the stakeholder now.\n\n" + read(FIRST / item / "brief.md"))


def rating_prompt(item):
    d = PAIRS / item
    return (read(d / "prompt.md").rstrip() + "\n\nDesign 1:\n\n{1}\n\nDesign 2:\n\n{2}\n\n"
            "Which design is better? End your answer with a line `WINNER: 1` or `WINNER: 2`.")


def build_prompt(r, lean):
    sentence = "" if lean else TRACK_CONDS[r["track"]][r["condition"]][1]
    if r["track"] == "rating":
        d = PAIRS / r["item"]
        one, two = ("a", "b") if r["order"] == "ab" else ("b", "a")
        text = rating_prompt(r["item"]).replace("{1}", read(d / f"{one}.md").rstrip()).replace(
            "{2}", read(d / f"{two}.md").rstrip())
    else:
        text = base_prompt(r["track"], r["item"])
    return text + (" " + sentence if sentence else "")


def matrix(tracks, conds=None, models=None, items=None, samples=1):
    """Runs ordered item by item (all conditions of an item together) so budget skips keep items balanced.
    conds, models, items: optional allow-lists."""
    runs = []
    for track in [t for t in TRACK_ORDER if t in tracks]:
        for item in item_ids(track):
            if items and item not in items:
                continue
            for cond in TRACK_CONDS[track]:
                if conds and cond not in conds:
                    continue
                for model in models_for(track, item):
                    if models and model not in models:
                        continue
                    for order in (["ab", "ba"] if track == "rating" else ["-"]):
                        for s in range(1, samples + 1):
                            runs.append(dict(name=f"{track}.{item}.{cond}.{model}.{order}.s{s}", track=track,
                                             item=item, condition=cond, model=model, order=order, sample=s))
    return runs


def strip_frontmatter(text):
    if text.startswith("---"):
        parts = text.split("---", 2)
        return parts[2].strip() if len(parts) == 3 else text
    return text.strip()


def system_prompt(track, cond):
    guides = [strip_frontmatter(read(SKILL_SRC[s] / "SKILL.md")) for s in TRACK_CONDS[track][cond][0]]
    return "\n\n".join(["You are a senior software engineer."] + guides)


def usage_tokens(u):
    u = u or {}
    return sum(u.get(k) or 0 for k in ("input_tokens", "cache_creation_input_tokens",
                                       "cache_read_input_tokens", "output_tokens"))


_ledger_lock = threading.Lock()


def ledger_get(run_id, skill):
    p = RESULTS / run_id / "ledger.json"
    return json.loads(p.read_text()).get(skill, 0) if p.exists() else 0


def ledger_add(run_id, skill, tokens):
    with _ledger_lock:
        p = RESULTS / run_id / "ledger.json"
        d = json.loads(p.read_text()) if p.exists() else {}
        d[skill] = d.get(skill, 0) + tokens
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(d, indent=1))


def lean_call(sys_prompt, prompt, model, timeout=TIMEOUT):
    """One no-tools, single-turn call from an empty dir. Returns dict(text, tokens, cost, duration_ms, stderr, raw)."""
    with tempfile.TemporaryDirectory(prefix="lean_") as d:
        sp = Path(d) / "sp.md"
        sp.write_text(sys_prompt, encoding="utf-8")
        work = Path(d) / "w"
        work.mkdir()
        cmd = [shutil.which("claude") or "claude", "-p", "--setting-sources", "project", "--strict-mcp-config",
               "--tools", "", "--system-prompt-file", str(sp), "--model", model, "--output-format", "json"]
        t0 = time.time()
        try:
            p = subprocess.run(cmd, input=prompt, cwd=work, capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=timeout)
            out, err = p.stdout, p.stderr
        except subprocess.TimeoutExpired:
            out, err = "", "TIMEOUT"
    try:
        j = json.loads(out)
    except ValueError:
        j = {}
    return dict(text=j.get("result", ""), tokens=usage_tokens(j.get("usage")), cost=j.get("total_cost_usd"),
                duration_ms=j.get("duration_ms") or int((time.time() - t0) * 1000), stderr=err, raw=out)


def rmtree(p):
    def fix(fn, path, exc):  # git objects are read-only on Windows
        os.chmod(path, stat.S_IWRITE)
        fn(path)
    if Path(p).exists():
        shutil.rmtree(p, onerror=fix)


def snapshot(d):
    return {str(p.relative_to(d)): hashlib.md5(p.read_bytes()).hexdigest() for p in d.rglob("*")
            if p.is_file() and not {".git", ".claude"} & set(p.relative_to(d).parts)}


def write_meta(out, r, **kw):
    meta = dict(run_id=r["name"], track=r["track"], item=r["item"], condition=r["condition"], model=r["model"],
                order=r["order"], sample=r["sample"], **kw)
    (out / "meta.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")


def run_lean(run_id, r, out):
    prompt = build_prompt(r, lean=True)
    (out / "prompt.txt").write_text(prompt, encoding="utf-8")
    res = lean_call(system_prompt(r["track"], r["condition"]), prompt, r["model"])
    (out / "out.json").write_text(res["raw"], encoding="utf-8")
    (out / "stderr.txt").write_text(res["stderr"], encoding="utf-8")
    (out / "final.md").write_text(res["text"], encoding="utf-8")
    write_meta(out, r, duration_ms=res["duration_ms"], total_cost_usd=res["cost"], mode="lean",
               skills_installed=TRACK_CONDS[r["track"]][r["condition"]][0], expected_skill=None,
               skills_invoked=[], tokens=res["tokens"], final_text=res["text"])
    ledger_add(run_id, SKILL_OF_TRACK[r["track"]], res["tokens"])


def run_full(run_id, r, out):
    work = Path.home() / ".skillpilot" / run_id / r["name"]  # not under TEMP: Git Bash shows TEMP as /tmp, which file tools resolve to C:\tmp
    rmtree(work)
    work.mkdir(parents=True)
    subprocess.run(["git", "init", "-q"], cwd=work, check=True)
    skills = TRACK_CONDS[r["track"]][r["condition"]][0]
    for s in skills:
        shutil.copytree(SKILL_SRC[s], work / ".claude/skills" / s)
    if r["track"] == "gen" and (GEN / r["item"] / "fixture").is_dir():
        shutil.copytree(GEN / r["item"] / "fixture", work, dirs_exist_ok=True)
    before = snapshot(work)
    prompt = build_prompt(r, lean=False)
    (out / "prompt.txt").write_text(prompt, encoding="utf-8")

    cmd = [shutil.which("claude") or "claude", "-p", "--model", r["model"]] + FULL_ARGS
    t0, timed_out = time.time(), False
    try:
        p = subprocess.run(cmd, input=prompt, cwd=work, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=TIMEOUT)
        stdout, stderr = p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        timed_out = True
        dec = lambda x: x.decode("utf-8", "replace") if isinstance(x, bytes) else (x or "")
        stdout, stderr = dec(e.stdout), dec(e.stderr) + "\nTIMEOUT"
    (out / "out.jsonl").write_text(stdout, encoding="utf-8")
    (out / "stderr.txt").write_text(stderr, encoding="utf-8")

    invoked, final_text, cost, dur, tokens = [], "", None, None, 0
    for line in stdout.splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "assistant":
            for c in ev.get("message", {}).get("content", []):
                if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") == "Skill":
                    invoked.append(c.get("input", {}).get("skill"))
        elif ev.get("type") == "result":
            final_text, cost, dur = ev.get("result", ""), ev.get("total_cost_usd"), ev.get("duration_ms")
            tokens = usage_tokens(ev.get("usage"))
    after = snapshot(work)  # keep new or changed files
    for rel, h in after.items():
        if before.get(rel) != h:
            dst = out / "output" / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(work / rel, dst)
    (out / "final.md").write_text(final_text or "", encoding="utf-8")
    write_meta(out, r, duration_ms=dur or int((time.time() - t0) * 1000), total_cost_usd=cost, mode="full",
               skills_installed=skills, expected_skill=skills[-1] if skills else None, skills_invoked=invoked,
               timed_out=timed_out, tokens=tokens, final_text=final_text)
    ledger_add(run_id, SKILL_OF_TRACK[r["track"]], tokens)
    rmtree(work)


def run_one(run_id, r):
    out = RESULTS / run_id / r["name"]
    if (out / "meta.json").exists():
        return "skip"
    rmtree(out)
    out.mkdir(parents=True)
    (run_lean if r["track"] in LEAN else run_full)(run_id, r, out)
    return "done"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--track", default="rating,gen,audit,first")
    ap.add_argument("--items", default="pilot", help="item set: evals/*/<items>/ (pilot, pilot2)")
    ap.add_argument("--conditions", default="", help="comma list filter, e.g. plain,skill (default all)")
    ap.add_argument("--models", default="", help="comma list filter, e.g. opus (default all)")
    ap.add_argument("--item-list", default="", help="comma list of item ids, e.g. q1,q3,b2 (default all)")
    ap.add_argument("--samples", type=int, default=1, help="runs per cell, ids get .s1, .s2 ...")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--concurrency", type=int, default=4)
    a = ap.parse_args()
    set_items(a.items)
    csv = lambda x: [v for v in x.split(",") if v]
    runs = matrix(a.track.split(","), csv(a.conditions), csv(a.models), csv(a.item_list), a.samples)
    if a.dry_run:
        counts, est = {}, {}
        for r in runs:
            k = (r["track"], r["condition"], r["model"])
            counts[k] = counts.get(k, 0) + 1
            sk = SKILL_OF_TRACK[r["track"]]
            est[sk] = est.get(sk, 0) + EST["lean" if r["track"] in LEAN else "full"] + (
                0 if r["track"] == "rating" else EST["judge"])
        for k, n in sorted(counts.items(), key=lambda kv: TRACK_ORDER.index(kv[0][0])):
            print(*k, n)
        print("total runs", len(runs))
        for sk, t in est.items():
            print(f"estimated tokens {sk}: {t:,} (stop at {BUDGET_STOP:,})")
        return
    (RESULTS / a.run_id).mkdir(parents=True, exist_ok=True)
    (RESULTS / a.run_id / "items.txt").write_text(a.items)  # grade.py reads the item set from here
    group_ok, lock, n = {}, threading.Lock(), [0]

    def work(r):
        key = (r["track"], r["item"])
        with lock:  # the first run of an item decides for the whole item, keeping conditions balanced
            if key not in group_ok:
                group_ok[key] = ledger_get(a.run_id, SKILL_OF_TRACK[r["track"]]) < BUDGET_STOP
            ok = group_ok[key]
        return run_one(a.run_id, r) if ok else "budget"

    with ThreadPoolExecutor(a.concurrency) as ex:
        futs = [(ex.submit(work, r), r) for r in runs]
        for f, r in futs:
            try:
                status = f.result()
            except Exception as e:  # no meta.json written, so a rerun retries it
                status = f"ERROR {e!r}"
            n[0] += 1
            print(f"[{n[0]}/{len(runs)}] {r['name']} {status}", flush=True)


if __name__ == "__main__":
    main()
