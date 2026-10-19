---
name: design-process
description: Guides designing a system together with a stakeholder over several sessions, from gathering requirements through decisions, a design doc, and review before implementation.
---

# Design Process

Use this process when designing a system collaboratively with a stakeholder across multiple sessions. The aim is a shared understanding of the problem, a design the stakeholder trusts, and a written record that survives between sessions. Adapt the depth to the size of the problem: a small tool needs a page of notes, a larger system needs the full set.

## Start by understanding the problem

Before proposing solutions, learn what the stakeholder actually needs.

- Ask what problem they are solving, who the users are, and what success looks like. Ask why before asking how.
- Find out what exists today: current systems, workflows, workarounds, and pain points.
- Identify the constraints: deadline, budget, team skills, existing infrastructure, compliance or regulatory rules, and anything that cannot change.
- Separate the problem from the stakeholder's proposed solution. A requested feature is often a symptom of a deeper need, so ask what it would let them do.
- Define scope explicitly, including what is out of scope. Non-goals prevent drift.

## Ask good clarifying questions

- Ask a few focused questions at a time rather than a long list. Prioritize those whose answers would change the design most.
- Prefer concrete questions with examples: "Walk me through what happens when an order is cancelled" beats "What are your requirements for orders?"
- Offer options when you can, with a recommended default, so the stakeholder can react instead of inventing answers from scratch.
- When an answer is vague, restate it in your own words and ask them to confirm.
- If you must proceed without an answer, state the assumption you are making and record it (see below).
- Note who is the decision maker for each topic, since different stakeholders may own different questions.

## Requirements

Capture requirements in two groups.

**Functional requirements** describe what the system does: the capabilities, workflows, inputs, outputs, and rules. Write them as testable statements or user stories, such as "A user can reset their password by email." Include the main flow and the notable error cases.

**Non-functional requirements** describe how well it does it: performance, scalability, availability, reliability, security, privacy, usability, maintainability, observability, cost, and compliance. Make them measurable where possible. "Fast" is not a requirement; "95 percent of searches return in under one second at expected load" is.

For each requirement, record its priority (must, should, could) and, if useful, its source. Check requirements for conflicts, gaps, and ambiguity, and ask the stakeholder to resolve them. Expect requirements to change as understanding grows, and track changes rather than overwriting them silently.

## Keep an assumptions list and a risk list

Maintain two living lists in the repository, for instance in `docs/assumptions.md` and `docs/risks.md`.

**Assumptions.** Record everything you are treating as true without proof: expected load, available integrations, user behavior, team capacity. For each, note the owner, how it can be validated, and its status (open, confirmed, or invalidated). Review the list at the start of each session and act on invalidated items, since they may undermine earlier decisions.

**Risks.** Record what could go wrong: technical unknowns, dependencies, schedule pressure, unclear requirements, security exposure. For each, note likelihood, impact, and a mitigation or a plan to learn more, such as a prototype or spike. Address the highest risks early, while changing course is still cheap.

## Explore options and record decisions as ADRs

When a significant choice arises, do not decide silently. Lay out the realistic options, the criteria that matter, and the trade-offs, then reach a decision with the stakeholder.

Record each significant decision as an Architecture Decision Record in `docs/adr/`, numbered sequentially, for example `docs/adr/0003-use-a-relational-database.md`. Keep each short:

- **Title and number.**
- **Status.** Proposed, accepted, deprecated, or superseded.
- **Context.** The forces and constraints behind the decision.
- **Options considered.** Brief, with the main pros and cons.
- **Decision.** What was chosen and why.
- **Consequences.** What becomes easier, what becomes harder, and what to revisit.

Treat accepted ADRs as history. If a decision changes, write a new ADR that supersedes the old one and link the two, instead of editing the original. Write ADRs for choices that are costly to reverse, such as data stores, service boundaries, major dependencies, and public interfaces. Routine choices do not need one.

## Iterate with the stakeholder

Design is a conversation across sessions, not a single presentation.

- Begin each session by summarizing where you left off: decisions made, open questions, and changed assumptions.
- Show work early and in rough form. Sketches, diagrams, and short outlines invite correction before much effort is invested.
- Present a recommendation with reasoning, not just a menu of options, while leaving the decision to the stakeholder.
- Use plain language, define jargon, and adjust the level of detail to the audience.
- Confirm understanding by asking them to restate or critique the design. Silence is not agreement.
- End each session with a short written summary: what was decided, what is still open, who owns each action, and what happens next.
- Prefer vertical slices and early validation. A thin end-to-end prototype often teaches more than another round of discussion.

## Write the design doc

Once the shape is clear, consolidate it into a design document, kept in `docs/` under version control. A useful structure:

1. **Overview.** The problem, goals, and non-goals in a few paragraphs.
2. **Requirements.** Functional and non-functional, prioritized.
3. **Proposed design.** Architecture, main components and their responsibilities, data model, interfaces, and key flows. Use diagrams where they clarify.
4. **Alternatives considered.** Why they were not chosen, linking to ADRs.
5. **Cross-cutting concerns.** Security, privacy, reliability, performance, observability, and operations.
6. **Testing and rollout.** How the system will be verified, deployed, and migrated, including rollback.
7. **Risks and open questions.** Linked to the risk and assumption lists.
8. **Milestones.** A rough sequence of deliverables.

Write for a reader who was not in the room. Keep it as short as the problem allows. A concise, accurate document is more useful than an exhaustive one nobody reads.

## Review before implementing

Do not start building until the design has been reviewed and the stakeholder has signed off.

- Walk the stakeholder through the document and check it against the stated requirements, one by one.
- Invite review from people who will build, operate, and use the system. Ask them specifically to look for gaps, hidden complexity, and risks.
- Trace a few realistic scenarios end to end, including failure cases, to test whether the design holds.
- Resolve or explicitly defer open questions, and make sure every blocking assumption is validated or accepted as a risk.
- Record approval and the date in the document so it is clear which version was agreed.

## Keep documents up to date

Documentation that drifts from reality is worse than none.

- Treat docs as part of the work: update them in the same change that alters the behavior or design.
- When implementation reveals that the design was wrong, fix the document and record the reason, with a new ADR if a decision changed.
- Review the assumptions and risk lists regularly, and close items that are resolved.
- Mark outdated documents clearly as superseded, or remove them, and keep an index in `docs/` so people can find the current ones.
- Use version control history as the record of how the design evolved.

## Summary

Understand before designing, ask before assuming, write decisions down, and keep the stakeholder involved at every step. Keep the written record small, current, and honest, and review the design before building it.
