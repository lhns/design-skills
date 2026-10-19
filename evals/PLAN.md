# Eval plan

The skill counts only if it changes outputs. Models using it must produce designs and code that keep every constraint with fewer concepts, and must pick the better design more often. They must do better than without it, and better than with a generic clean-code text of the same length. This plan was committed before any run, so its thresholds are fixed in advance.

## Conditions
Every prompt asks for an elegant result and says: "No user is available: choose, and label your own design choices."

| Condition | Extra context |
| --- | --- |
| plain | none |
| placebo | `placebo.md` installed as a skill in `.claude/skills/clean-code`: generic clean-code guidance, length-matched to `SKILL.md`; the prompt tells the model to use it |
| skill | the skill in `.claude/skills/elegance`; the prompt tells the model to use it |

The main comparison is skill vs placebo. Both load the same way, so they differ only in content.

- **Skill use is verified:** a run counts as "skill confirmed" when its `stream-json` output shows a `Skill` call for its condition's skill. Results are reported for all runs and for confirmed runs.
- **Natural triggering is measured separately,** with skill-creator's description loop.

## Isolation
- **Each run:** `claude -p` in a fresh temp dir.
- **Flags:**
  - `--setting-sources project` (no user CLAUDE.md, advisor or plugins);
  - pinned `--model` and `--effort`;
  - subagent tools disallowed;
  - prompt passed via stdin.
- **Concurrency:** about 4.
- **First check that it holds:** the flags exist, and no advisor or user instructions appear in the transcript.

## Tracks
### Generation (Opus and Sonnet, every task, 3 samples)
- **Synthetic design and code tasks** from varied domains, for example:
  - retry/limit policy;
  - payment-provider extension;
  - permissions model;
  - feature-flag sprawl;
  - event pipeline;
  - undo/redo.
- **Outside material:** 3–4 known refactoring katas (Gilded Rose, Tennis, Trivia), not written from this theory.
- **Each task:**
  - states its constraints and plants one that is tempting to drop;
  - has hidden tests and adversarial checks, such as an input that breaks a stated constraint, or a scaled input that breaks an arbitrary limit;
  - has a reference answer that only the judge sees.
- **Grading, in order:**
  1. **Executable checks.** A dropped constraint fails the run, whatever its size.
  2. **Normalization.** Sonnet reduces each output to a fixed template holding only the final design or code, which removes vocabulary that would reveal the condition and any self-reported counts.
  3. **Opus judge, blind to the condition.** It counts concepts, exception clauses ("except", "only if", "unless") and special cases from the normalized artifact. It also compares outputs pairwise in both orders, and only verdicts that agree in both orders count.
  4. **Diagnostics only:** LOC, cyclomatic complexity, tokens, duration.

### Rating (Opus and Sonnet, no tools)
- **Pairs:** about 36 A/B design or code pairs, each asked in both orders, with 1 sample per pair, condition and model.
- **Metric:** pick accuracy.
- **Balanced:** in half the pairs the longer option is correct.
- **Trap kinds:**
  - accreted vs derived;
  - shorter but drops a stated constraint;
  - clever golf vs plain;
  - premature abstraction vs concrete;
  - arbitrary limit vs condition;
  - forced clean model vs an honest lookup table for an irregular domain.

## Against bias and overfitting
- **Who writes the items:** fresh agents write tasks, pairs and references from this plan. They never see the skill text.
- **Holdout:** a separate holdout set, larger than the train set, is written by another agent and runs once at the end.
- **Iteration:** only on train-set transcripts and scores.
- **Ceiling pilot:** the baseline is first piloted on candidate items, and items it already aces are dropped. Scoring uses fresh runs.
- **Statistics:** a paired bootstrap at task and pair level.

## Steps
1. **Verify isolation** and skill detection. Time one run per track and model, extrapolate the cost, and confirm or shrink the scale.
2. **Write the items and tools in parallel:**
   - train set, holdout set and pairs (separate fresh agents);
   - `run.py`, `grade.py`, `report.py`;
   - `placebo.md`.
3. **Pilot** the baseline and prune ceiling items.
4. **Round 1 on the train set.** Read the transcripts as well as the scores: where did the skill help, hurt, add false elegance, or add cost?
5. **Revise the skill,** up to 3 rounds. Cut what doesn't measurably help.
6. **Run the holdout once.** Commit the results under `results/` and the summary in the README.
7. **Tune the description** for triggering. Run the loop from a scratch dir with its own `.claude/`, so it doesn't write into the user's global commands.

## Success criteria (holdout)
On both models, skill vs placebo, with a 95% bootstrap interval excluding 0:
- the executable pass rate is not lower;
- judge-counted concepts and exception clauses are lower;
- the skill wins at least 60% of the order-consistent pairwise verdicts;
- rating accuracy is higher, overall and on the "drops a constraint" pairs.

Token and time overhead is reported. If the skill doesn't beat the placebo, the README says so, and the skill is cut down to what measurably helps.

## Layout
```
evals/
  PLAN.md         this file
  placebo.md      installed as skills/clean-code/SKILL.md in placebo runs
  gen/<task>/     task.md, constraints, fixture/, hidden checks, reference.md (judge only)
  pairs/<pair>/   a.md, b.md, truth.yaml (winner, trap kind)
  holdout/        same shape
  run.py  grade.py  report.py
  results/iteration-N/
```
