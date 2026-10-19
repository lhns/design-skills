# Skill pilot runner

```
python evals/pilot/run.py --run-id pilot1 [--track rating,audit,gen,first] [--dry-run] [--concurrency 4]
python evals/pilot/grade.py --run-id pilot1
```

Results go to `evals/pilot/results/<run-id>/<track>.<item>.<condition>.<model>.<order>/`; `report.md`, `grades.json` and `ledger.json` sit at `results/<run-id>/`. Rerunning skips runs that already have `meta.json` (delete a run dir to redo it). Stdlib only; PyYAML is used for `truth.yaml` if installed.

## Modes
- **Lean** (`rating`, `audit`, and every judge call): one `claude -p --tools "" --system-prompt-file ... --output-format json` call from an empty dir. System prompt = "You are a senior software engineer." plus the condition's SKILL.md bodies (frontmatter stripped). No "Use the X skill" sentence.
- **Full** (`gen`, `first`): fresh temp git repo under `%TEMP%/skillpilot/`, skills installed in `.claude/skills/`, tools Read/Write/Edit/Glob/Grep/Bash/Skill, `--max-budget-usd 3`, 15 min timeout. New or changed files are copied to `output/`. Models: gen `g2` sonnet, other gen items opus; first opus.

## Conditions
Elegance tracks (rating, gen): `plain`, `placebo` (clean-code), `skill` (elegance). Collapse tracks (audit, first): `elegance`, `placebo` (+design-process), `collapse` (+design-by-collapse).

## Budget
Tokens (input + cache creation + cache read + output) are summed per skill in `ledger.json` (elegance: rating, gen; design-by-collapse: audit, first), judge calls included. Runs are ordered rating, audit, gen, first, and item by item. Before the first run (or judge call) of an item, the ledger is checked; at 1,900,000 the whole item is skipped ("budget"), so every item that runs has all its conditions. Runs already in flight can overshoot a little. `--dry-run` prints the matrix and a pessimistic estimate (lean 4k, full 150k, judge 8k).

## Input formats assumed
- rating: `pairs/<id>/{prompt,a,b}.md`, `truth.yaml` with `better` (a|b), `longer`, `kind`, `reason`.
- gen: `gen/<id>/task.md`, `check.md` (judge only), optional `fixture/` (copied to the run dir) and `hidden/test_hidden.py` (run by the grader against the run's output with `pytest`, falling back to `python test_hidden.py`).
- audit: `audit/a<n>.md` and `audit/truth.yaml`: a mapping `a<n>: [error, ...]` (error = string or mapping), or a list of entries with a `doc`/`item`/`id` key. A doc with no entries is clean.
- first: `first/<id>/brief.md`, `check.md` (judge only).

## Grading
Judges (opus, lean, JSON only) see only the check/truth and the run's text with skill names replaced by "the guide"; no condition names. Rating is parsed from the last `WINNER: n` and mapped through the order. Audit reports detection (matched true errors / total), false alarms per doc and the share of clean docs with any alarm. The report also gives mean cost, duration and tokens per track and condition, skill-invocation rate (full runs only) and the token ledger.
