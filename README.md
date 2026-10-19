# design-skills

Claude Code skills for designing systems and code. Each skill is a separate folder and can be installed on its own.

| Skill | What it does | Needs |
| --- | --- | --- |
| [`elegance`](skills/elegance/SKILL.md) | Steers designs and code toward a few independent concepts, each forced by a constraint, and changes how models compare and rate designs | — |
| [`design-by-collapse`](skills/design-by-collapse/SKILL.md) | Runs a design with a stakeholder over several sessions: keeps the owner's constraints apart from the designer's choices, maps the solution space as forks, asks focused questions, and keeps the design movable when constraints change. Includes a consistency check (`scripts/check.py`, Python 3 + PyYAML) | `elegance` |

**Status: v0. Two pilot waves, no measurable difference vs the placebo yet.** A skill counts only if it measurably beats the alternatives on outcomes. Results so far (`evals/pilot/results/`):
- **Pilot 1 and pilot 2** (pilot 2 on commit `05a9f25`): both skills, single-shot tracks. Rating pairs, audits and first sessions were at ceiling in every condition, including no skill, for Opus and Sonnet. Design and code tasks showed no difference at 1–2 samples. No harm measured.
- **Cost:** elegance adds about 35–40% tokens on design tasks; design-by-collapse costs 2.6–7.6× tokens on a first session.
- **Untested:** the effects the skills claim over time (no accretion across rounds, plasticity, no re-asking) need multi-session or iterative tests, which haven't run yet.
- **Changed since pilot 2:**
  - the "simple" term (irreducibility, emergence) and the composition preference in reviewing;
  - the rule reworded: every part can say why it's there;
  - existing parts are reported as deletion candidates, not removed;
  - docs and tests are out of scope;
  - patterns may supply guarantees;
  - repo conventions count as constraints;
  - design-by-collapse: records in `docs/design/` and ADRs.

Each eval plan was committed before any run:
- [`evals/elegance/PLAN.md`](evals/elegance/PLAN.md)
- [`evals/design-by-collapse/PLAN.md`](evals/design-by-collapse/PLAN.md)

Pilot results are in `evals/pilot/results/`: a report, grades and each run's prompt and final answer. Raw session transcripts aren't published.

## Field trial (current evaluation)
The pilots measured neither harm nor benefit, so the skills are now on trial in real codebases. The trial answers "does it help here, does it hurt", not "does it work in general". Per session:
- **Count only sessions where the skill actually fired.** Invoke it explicitly (`/elegance`, `/design-by-collapse`), or check the transcript for the `Skill` call.
- **Record countable signs**, not impressions: tokens, diff size, concepts or modules added vs removed, special-case branches, magic numbers, duplicates, tests green, bugs found later.
- **Watch for harm:**
  - a constraint dropped for simplicity (a regression; one case is reason to stop);
  - a restructure forced into a small task;
  - an unneeded question or block;
  - records or ADRs nobody reads;
  - an inference written into a constraint;
  - something removed as unforced that served a purpose nobody had listed (a pattern, a guarantee, docs).
- **Run a cheap A/B for substantial tasks:** the same task in two worktrees, skill on and off, then diff the results.

After a few weeks, cut any rule that never shows up in the transcripts.

## Install
Link the skills you want into your user skills folder. `design-by-collapse` needs `elegance` too. Without it, the skill still works but says that its design tests are missing.

```sh
# macOS/Linux/Git Bash
ln -s "$PWD/skills/elegance" ~/.claude/skills/elegance
ln -s "$PWD/skills/design-by-collapse" ~/.claude/skills/design-by-collapse
```
```bat
:: Windows cmd (admin or developer mode)
mklink /D "%USERPROFILE%\.claude\skills\elegance" "%CD%\skills\elegance"
mklink /D "%USERPROFILE%\.claude\skills\design-by-collapse" "%CD%\skills\design-by-collapse"
```

For controlled evals, uninstall them first (user-level skills stay visible even with `--setting-sources project`), or use the runner's lean mode.

## Editing
Changes to a skill go through its evals: keep what measurably improves outputs, and cut the rest. Each skill should pass the elegance rubric itself: few concepts, few exception clauses, nothing untraced.

The check has its own tests: `python skills/design-by-collapse/scripts/tests/test_check.py`.

## License
Apache-2.0, see [LICENSE](LICENSE).
