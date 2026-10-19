# Eval plan: design-by-collapse

The skill counts only if it changes outcomes. A designer using it with an owner across sessions must keep the owner's constraints intact, avoid planted traps, and keep the design movable when constraints change. It has to do this better than with the elegance skill alone, and better than with the elegance skill plus a generic design-process text. This plan was committed before any run, so its thresholds are fixed in advance.

## Conditions
The designer is Opus in every condition. Isolation is the same as in the elegance plan:
- `claude -p` in a fresh temp dir;
- `--setting-sources project`;
- pinned model and effort;
- no subagent tools;
- prompts via stdin.

| Condition | Skills installed |
| --- | --- |
| elegance | `elegance` |
| placebo | `elegance` + `design-process`: a generic process skill (gather requirements, record decisions as ADRs, ask clarifying questions), length-matched to `design-by-collapse` |
| collapse | `elegance` + `design-by-collapse` |

Every prompt asks the designer to work with the owner and keep the design in files under `design/`, in any shape. A run counts as "skill confirmed" when the transcript shows the condition's process skill being loaded. Results are reported for all runs and for confirmed runs.

## Sessions and the simulated owner
- **Fresh sessions.** Every owner turn starts a fresh `claude -p` session that sees only the repo files and the new owner message. Only the files carry the design from one session to the next, which is what the method claims to need.
- **Turn cap and snapshots.** A run stops at 12 owner turns, or earlier when the designer declares the design complete. `design/` and the transcript are snapshotted after every session.
- **The simulated owner is Sonnet with an atomic answer key.** Each entry answers one specific decision.
  - **What it reveals:** it releases an entry only when a question targets that entry. A broad question ("what do you want?") gets a short restatement of the original brief, nothing more.
  - **When it can't answer:** if it can't locate an answer in its key from the question as asked, it replies that it can't tell what is being asked. It doesn't judge the question's format.
  - **Scripted lines:** where the key says so, it answers "not sure yet". At scripted turns it approves the designer's latest proposal ("looks good").
  - **Injected change:** at a scripted turn it adds a new constraint.
- **Question quality** is rated separately, from the transcripts, by a blind grader that doesn't know the condition.

## Scenarios
Synthetic and neutral, from varied domains: 4 for training and 6 for the holdout. Each scenario has:
- an owner corpus (the opening brief plus statements);
- for half of them, an accreted earlier design to rescue;
- an atomic answer key;
- a reference design: its constraints, forks with the correct forced and open status, and its concepts.

Each scenario plants these traps:

| Trap | Passes when |
| --- | --- |
| An inference that tempts eliminating concepts that also serve other problems | No inference appears as an owner constraint, and those concepts survive or become questions |
| The owner approves a designer document | Nothing from that document becomes an owner constraint |
| A bundled decision | It is split into one decision per problem |
| A decision with one option left | It is reported, never asked |
| "Not sure yet" | The decision stays open with a default, and is not filled in later without the owner |
| A concept the owner excluded | It is never reintroduced |
| An arbitrary limit | It becomes a condition, or a named bound with a reason |
| A constraint injected mid-run that eliminates a chosen option | In the next snapshot the choice and its dependent details have moved, and nothing from the old choice remains |

## Grading
Grading must not favour the skill's own file shapes, so every run is first extracted into one neutral schema.

1. **Extraction.** Sonnet extracts each snapshot of `design/`, whatever its shape, into:
   - constraints, each marked owner-given or designer-chosen, with its source quote;
   - decisions, each with its options, what ruled each option out, the current choice, and whether it is open;
   - open questions with defaults;
   - concepts.
2. **Trap checks.** These use the extractions, the per-session snapshots (plasticity) and the transcripts:
   - an answered question asked again;
   - a forced decision asked;
   - acting before an answer the work depended on.
3. **Final design.** A blind Opus judge works on normalized artifacts. It tries a counterexample against each constraint, counts concepts against the reference, and compares pairs in both orders. Only verdicts that agree in both orders count.

**Primary metric:** trap pass rate, clustered by scenario.

**Secondary metrics:**
- inferences recorded as owner constraints;
- accretion recall and precision on rescue scenarios;
- owner turns until the design converges;
- the simulated owner's "can't tell what is being asked" rate;
- final concept count and constraint satisfaction;
- tokens and duration.

## Audit track
About 40 neutral design documents, each a short prose design plus a plain decision table, with planted errors:
- an inference stated as an owner constraint;
- a value used to rule out an option;
- two problems bundled into one decision;
- a forced decision asked anyway;
- an approval recorded as a constraint;
- a choice that a newer constraint has ruled out;
- a detail that belongs to no decision.

Each document has between 0 and 2 errors, and some have none, so false alarms count. Each condition is asked, single-turn with no tools, to find the problems. Metrics: detection rate and false-alarm rate. This track is cheap and carries most of the statistical weight.

## Against bias and overfitting
- **Who writes the items:** fresh agents write scenarios, keys, references and audit items from this plan. They never see the skill texts.
- **Holdout:** a separate agent writes the holdout set, and it runs once, at the end.
- **What the designer sees:** nothing about traps. Prompts read like normal owner requests.
- **What iteration uses:** only training transcripts and scores.
- **Placebo:** written once and reviewed for length and genericity. It is never tuned against results.

## Steps
1. **Check setup:** verify the isolation, skill detection and the fresh-session loop. Time one scenario end to end, then extrapolate the cost and confirm or shrink the scale.
2. **Write items and tools in parallel:** training scenarios, holdout scenarios, audit items, the owner simulator prompt, `run.py`, `grade.py`, and the placebo skill.
3. **Pilot the elegance condition.** Drop audit items it already aces, then score on fresh runs.
4. **Round 1** on the training scenarios, 3 samples per condition. Read the transcripts as well as the scores: where did the skill help, hurt, over-ask or stall?
5. **Revise** the skill, up to 3 rounds. Cut what doesn't measurably help.
6. **Holdout:** 6 scenarios × 3 samples × 3 conditions, plus the audit track. Commit the results under `results/` and the summary in the README.

## Success criteria (holdout)
Collapse must beat both elegance and placebo:
- **trap pass rate** higher, with the 95% bootstrap interval (resampling scenarios) excluding 0;
- **audit detection rate** higher, with the 95% interval excluding 0, and the false-alarm rate not higher;
- **"can't tell" rate and final concept count** not worse.

The token and time overhead is reported. If collapse doesn't win, the README says so, and the skill is cut down to what measurably helps.

## Layout
```
evals/design-by-collapse/
  PLAN.md
  placebo/SKILL.md      the design-process placebo
  owner_sim.md          simulator prompt
  scenarios/<name>/     brief.md, key.yaml, reference.yaml, old-design/ (rescue only)
  holdout/              same shape
  audit/<n>.md + audit/truth.yaml
  run.py  grade.py
  results/iteration-N/
```
