# Skill pilot runner

```
python evals/pilot/run.py --run-id pilot1 [--track rating,audit,gen,first] [--dry-run] [--concurrency 4]
    [--items pilot2] [--conditions plain,skill] [--models opus] [--item-list q1,q3,b2] [--samples N]
python evals/pilot/grade.py --run-id pilot1
python evals/pilot/grade.py --run-id pilot1 --prune-report
```

`--items` picks the item set (`evals/elegance/<items>/`, `evals/design-by-collapse/<items>/`; default `pilot`, wave 2 `pilot2`) and is recorded in `results/<run-id>/items.txt` for grade.py. `--conditions`, `--models` and `--item-list` are allow-list filters (default all); e.g. `--conditions plain --models opus` for a baseline-only prune run. `--samples N` repeats every cell N times; run ids end in `.s1`, `.s2` and reports pool the samples.

Results go to `evals/pilot/results/<run-id>/<track>.<item>.<condition>.<model>.<order>.s<n>/`; `report.md`, `grades.json` and `ledger.json` sit at `results/<run-id>/`. Rerunning skips runs that already have `meta.json` (delete a run dir to redo it). Stdlib only; PyYAML is used for `truth.yaml` if installed.

## Modes
- **Lean** (`rating`, `audit`, and every judge call): one `claude -p --tools "" --system-prompt-file ... --output-format json` call from an empty dir. System prompt = "You are a senior software engineer." plus the condition's SKILL.md bodies (frontmatter stripped). No "Use the X skill" sentence.
- **Full** (`gen`, `first`): fresh temp git repo under `%TEMP%/skillpilot/`, skills installed in `.claude/skills/`, tools Read/Write/Edit/Glob/Grep/Bash/Skill, `--max-budget-usd 3`, 15 min timeout. New or changed files are copied to `output/`. Models: gen from optional `gen/<id>/meta.yaml` key `model` (default opus; wave 1 `g2` without a meta.yaml stays sonnet); first opus.

## Conditions
Elegance tracks (rating, gen): `plain`, `placebo` (clean-code), `skill` (elegance). Collapse tracks (audit, first): `elegance`, `placebo` (+design-process), `collapse` (+design-by-collapse).

## Budget
Tokens (input + cache creation + cache read + output) are summed per skill in `ledger.json` (elegance: rating, gen; design-by-collapse: audit, first), judge calls included. Runs are ordered rating, audit, gen, first, and item by item. Before the first run (or judge call) of an item, the ledger is checked; at 1,900,000 the whole item is skipped ("budget"), so every item that runs has all its conditions. The cap is per run-id. Runs already in flight can overshoot a little. `--dry-run` prints the matrix and a pessimistic estimate (lean 4k, full 150k, judge 8k).

## Input formats assumed
- rating: `pairs/<id>/{prompt,a,b}.md`, `truth.yaml` with `better` (a|b), `longer`, `kind`, `reason`.
- gen: `gen/<id>/task.md`, `check.md` (judge only), optional `fixture/` (copied to the run dir) and `hidden/test_hidden.py` (run by the grader against the run's output with `pytest`, falling back to `python test_hidden.py`).
- audit: `audit/a<n>.md` and `audit/truth.yaml`: a mapping `a<n>: [error, ...]` (error = string or mapping), a mapping `a<n>: {errors: [...], acceptable_extra: [...]}`, or a list of entries with a `doc`/`item`/`id` key. A doc with no entries is clean.
- first: `first/<id>/brief.md`, `check.md` (judge only).

## Grading
Judges (opus, lean, JSON only) see only the check/truth and the run's text with skill names replaced by "the guide"; no condition names. Rating is parsed from the last `WINNER: n` and mapped through the order. The audit judge classifies every finding as `planted:<index>`, `real` (genuine problem a strict reviewer would raise; includes `acceptable_extra` matches), `defensible` or `wrong`. Audit reports detection (planted errors found / total), mean real, defensible and wrong findings per doc, and the share of clean docs with a wrong finding.

`--prune-report` reads existing grades (no judging) and lists per rating pair and audit doc how the baseline did, marking ACED items that can be dropped. Rating baseline = condition `plain`, aced if correct in both orders on every model and sample. Audit baseline = condition `elegance`, aced if all planted errors were found with zero wrong findings. The report also gives mean cost, duration and tokens per track and condition, skill-invocation rate (full runs only) and the token ledger.
