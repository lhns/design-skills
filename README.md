# elegance-skill

A Claude Code skill that steers models toward elegant designs and code. Here "elegant" means a few independent concepts, each forced by a constraint, with everything else derived. The skill also changes how models compare and rate designs.

**Status: v0, untested.** The skill only counts if it measurably beats both no skill and a length-matched generic clean-code text. How that is measured is in [`evals/PLAN.md`](evals/PLAN.md), committed before any run; results will go in `evals/results/`.

## Contents
| Path | Purpose |
| --- | --- |
| `skills/elegance/SKILL.md` | The skill |
| `evals/PLAN.md` | Eval method and pre-registered success criteria |

## Install
After the evals pass, link the skill into your user skills:

```sh
ln -s "$PWD/skills/elegance" ~/.claude/skills/elegance      # macOS/Linux/Git Bash
mklink /D "%USERPROFILE%\.claude\skills\elegance" "%CD%\skills\elegance"   :: Windows cmd (admin or developer mode)
```

Don't install it while running evals: a user-level copy leaks into the baseline runs.

## Editing
Changes to `SKILL.md` go through the evals: keep what measurably improves outputs and cut the rest. The skill should pass its own rubric, with few concepts, few exception clauses, and nothing untraced.
