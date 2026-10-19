PROBLEM: C3: The constraint is broader than what Rosa said. She said "don't make students type those long sample IDs. They get them wrong every time." That is about students typing long IDs. C3 turns it into "No manual entry of sample IDs anywhere," which covers any typing, by anyone, of any code. That is the designer's conclusion written into a constraint. It should be recorded verbatim, or kept as an assumption until Rosa confirms the wider reading.

PROBLEM: D3, "short code" ruled out by C3: The elimination rests on that broadened paraphrase. A short code is exactly the fix for the problem Rosa described, which was long IDs that get mistyped. Her own words do not rule it out. Only the designer's inference does.

PROBLEM: D3, status "decided": Rosa never chose "wait until the scanner is fixed." It is only what was left after an elimination she didn't make. It is a designer choice and should be marked open, with a question to Rosa.

PROBLEM: C4: The constraint keeps the fact and drops the requirement. Rosa said the scanner dies "and then the whole class is stuck." Her complaint is that the class gets stuck. C4 records only that the scanner fails, so a fallback that leaves the class stuck appears to satisfy it. This weakens her constraint to make the design simpler.

PROBLEM: D3, choice: Waiting for a repair is the "whole class is stuck" outcome Rosa complained about. It also conflicts with C2 for every session until the repair.

PROBLEM: D3, "keeping samples in the fridge": Storing samples meant for -20 °C in a fridge is a separate decision with consequences for sample integrity. Neither Rosa nor reality forces it. It is bundled into D3 with no fork, no options and no assumption recorded.

PROBLEM: D3, scope: The fallback is aimed at the wrong step. In the design, freezing a sample means printing a label, which does not need the scanner. The scanner is used only when a sample is taken out. "Leave new samples in the fridge" therefore addresses a step the outage doesn't block. Meanwhile, nothing is decided for the step that is blocked: removal, and recording that removal.

PROBLEM: D3, options: The option list is incomplete. A spare or handheld scanner, lookup by student name on the terminal, and recording removals later were never listed. A fork must list every option, including eliminated ones.

PROBLEM: D4, status "decided": Rosa stated a fact about discarding old samples. She did not choose to have the terminal produce a discard list. That mechanism is a designer choice and should stay open.

PROBLEM: D4, "older than one term": What counts as one term is undecided. It could be a calendar term, or a term's length counted from the freeze date. A list run at the end of term also misses samples that pass one term partway through the next term. This is a fork that was never recorded.

PROBLEM: Design, "scan its label when they take it out": No constraint is cited for scanning out. It is unclear what it serves, presumably keeping D4's list accurate. If it does serve D4, then scanner outages (C4) leave removed samples on the list, and that interaction was never examined.

PROBLEM: D1, "freezer-grade" and "so the scanner can read it": Both are designer assumptions, but they are only recorded as a parenthetical. They are not listed as assumptions the choice depends on.

PROBLEM: D1, D2, open decisions: There is no recorded question, default, decide-by event or date asked. Both forks have sat open since January with no record of what was asked or when they must be settled.

PROBLEM: C2: "Students find their tubes quickly" is a paraphrase of a complaint ("ten minutes hunting"). It was never confirmed as a requirement, nor given a target. It should be marked as an assumption until Rosa confirms it.