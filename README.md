# design-skills

Claude Code skills for designing systems and code. Each skill is a separate folder and can be installed on its own.

| Skill | What it does | Needs |
| --- | --- | --- |
| [`elegance`](skills/elegance/SKILL.md) | Steers designs and code toward a few independent concepts, each forced by a constraint, and changes how models compare and rate designs | — |
| [`design-by-collapse`](skills/design-by-collapse/SKILL.md) | Runs a design with a stakeholder over several sessions: keeps the owner's constraints apart from the designer's choices, maps the solution space as forks, asks focused questions, and keeps the design movable when constraints change. Includes a consistency check (`scripts/check.py`, Python 3 + PyYAML) | `elegance` |

**Status: v0. Two pilot waves, no measurable difference vs the placebo yet.** A skill counts only if it measurably beats the alternatives on outcomes. Results so far (`evals/pilot/results/`):
- **Pilot 1 and pilot 2** (pilot 2 on commit `d25e6f5`): both skills, single-shot tracks. Rating pairs, audits and first sessions were at ceiling in every condition, including no skill, for Opus and Sonnet. Design and code tasks showed no difference at 1–2 samples. No harm measured.
- **Cost:** elegance adds about 35–40% tokens on design tasks; design-by-collapse costs 2.6–7.6× tokens on a first session.
- **Untested:** the effects the skills claim over time (no accretion across rounds, plasticity, no re-asking) need multi-session or iterative tests, which haven't run yet.
- **Changed since pilot 2:** the "simple" term (irreducibility, emergence) and the composition preference in reviewing.

Each eval plan was committed before any run:
- [`evals/elegance/PLAN.md`](evals/elegance/PLAN.md)
- [`evals/design-by-collapse/PLAN.md`](evals/design-by-collapse/PLAN.md)

Results will go in each plan's `results/` folder.

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

Don't install them while running evals: user-level copies leak into the baseline runs.

## Editing
Changes to a skill go through its evals: keep what measurably improves outputs, and cut the rest. Each skill should pass the elegance rubric itself: few concepts, few exception clauses, nothing untraced.

The check has its own tests: `python skills/design-by-collapse/scripts/tests/test_check.py`.
