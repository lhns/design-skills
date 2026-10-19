PROBLEM: Constraints, C5: Mira said "Most volunteers aren't comfortable with apps, so the shed panel is what they'll use." That describes what volunteers will use. It does not exclude remote control or alerts. "No remote or app control; everything happens at the shed panel" is the designer's conclusion written as an owner constraint. At most it is an assumption until Mira confirms it.

PROBLEM: Constraints, C6: The paraphrase drops "wherever I am." Mira's actual requirement is that she can be reached remotely. "Learns of a stuck valve promptly" weakens it so that a panel light could seem to satisfy it.

PROBLEM: Decisions, D4: Text message and app are eliminated by C5, which is an inference and not an owner statement. The fork is then marked "decided" without Mira answering it. Only the owner collapses a fork.

PROBLEM: Decisions, D4 / Design: The chosen option breaks C6 as Mira stated it. A light in the shed is not seen "wherever I am." In last August's case, a valve stuck over a weekend with nobody in the shed, the light would go unseen and bed 4 would flood again. This is a conflict between Mira's two statements. It should go to her, not be settled by the designer.

PROBLEM: Decisions, D2 and D6: Both are recorded as asked of Mira on 03-09. That is two questions in one round, when only one is allowed per round. Neither records the exact question text, so the next session cannot tell what was asked or match her answer to it.

PROBLEM: Decisions, D2/D3/D5/D6: The open forks have no question and no decide_by event. Seven months on (today is 2026-10-19), the record cannot show whether any default has already locked in an option, for example whether the flow meter has been installed.

PROBLEM: Decisions, D3 / D6: There is a hidden coupling between the two forks. The design's "today's litres" display, which serves C3 and D6, needs the flow meter. If D3 chose "moisture rising while valves closed," the litre count and both D6 options would disappear. D3's choice is carried by two problems, and the record lists only one.

PROBLEM: Decisions, D3: The "moisture rising while valves are closed" option is not checked against reality. Rain also raises moisture, so the option gives false alarms outdoors. Neither the record nor a source notes this, and the option is not ranked on it.

PROBLEM: Design, stop button / stuck valve: The design was not probed for this scenario. If a valve is stuck open, the stop button only closes valves, so it cannot stop the water. That breaks C2 ("stop all watering") in exactly the failure Mira described. A master shut-off on the supply, or some other response to a fault, is an undecided behavior and should be a fork.

PROBLEM: Design, "Moisture readings are kept for 400 days on the controller's SD card": This concept and its number trace to no constraint and no fork. It is an accretion. Either delete it or raise it as a fork with a reason.

PROBLEM: Design, zone thresholds and the 2,000-litre amber point: Per-zone threshold values are numbers that are neither cited bounds nor forks. Who sets them, and where, is also undecided. The C4 paraphrase "watered separately" (from "needs different watering") is also unconfirmed. D1 rests on it as "decided."

PROBLEM: Record structure: The constraints mix verbatim facts with paraphrases, and nothing marks which is which. C3 is a fact about pricing, not a requirement. No classes (constraint, value, exclusion) are recorded, so assumptions such as C5 look identical to Mira's own constraints.