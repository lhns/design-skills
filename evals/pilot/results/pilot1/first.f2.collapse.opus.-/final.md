Thanks, Ines. I've written the first-round design and my notes in `design/`. `design/design.md` is the current design. The other files keep your words (`vision.md`), the rules taken from them (`kernel.yaml`), the decisions still open (`forks.yaml`) and the parts of the design (`concepts.yaml`). A script that checks these files against each other runs without errors.

**What I took from your notes.** Please correct anything I've got wrong; the full list is in `kernel.yaml`.
- Everyone must be inducted on a machine before using it, and a trainer signs them off.
- The table saw needs two inducted people, and the system has to enforce that. There are no staff in the woodshop in the evenings, and closing early isn't an option.
- The insurer wants each trainer's signature and the date at renewal, kept for six years.
- No passwords. Members keep booking from home, and it has to be easy.
- A laser tube lasts about 1,000 hours of cutting.
- Budget is approved. I've treated "rather not run our own server" as a strong preference, not a hard rule.

**The core idea I'm proposing.** On site, the only thing a member ever does is tap their fob. A machine switches on only if that person is inducted on it. The same taps handle the rest:
- the table saw also needs a second inducted person to tap before it starts;
- your first tap during a booking confirms you've turned up, and a booking nobody turns up for frees up after a short wait;
- the time the laser is switched on adds up to the tube's hours. That count can only run ahead of the real cutting time, so the spare-tube warning comes early, never late.

**Two things your notes already settle:**
- **Paper book or digital:** the system has to have a digital record. The saw can only enforce "both inducted" if it knows who is inducted, and it can't read the paper book. What's still open is whether the paper book stays as the signed copy for the insurer. That depends on whether they accept electronic signatures, which is a question for them.
- **Who enforces the saw rule:** the saw itself, because no one else is there in the evenings.

**My suggestions on your open questions.** None of these is decided until you say so.
- **Laser sharing:** instead of a two-hours-a-week cap, each member holds one upcoming laser booking at a time. There's no number to tune, slots don't sit empty in quiet weeks, and it stops people booking far ahead.
- **3D printers:** you said you're still thinking, so I won't ask yet. For now the design shows each printer's status (free, or printing with time left) on the website, with no bookings.
- **Materials:** sell acrylic by the sheet and filament by the spool before people start, or let them bring their own. Nothing is metered while anyone works.

There are 12 open decisions in total. Each has a default, so work can continue meanwhile. I also need some facts, not decisions:
- the make and model of your current interlocks and of the laser's controller;
- how long the supplier takes to deliver a new tube;
- what time members can get in before 10:00.

**Question for Ines:** Your 9 Oct note says the fob is a member's identity, "full stop". Your 16 Oct note says booking from home has to keep working and be easy. At home there's no fob reader, so the website needs another way to know it's really you. Which of these is acceptable?
- **A (my recommendation): an emailed sign-in link.** You type your email, click the link it sends you, and you can book. There's no password to forget, so nothing for the front desk to reset. The fob stays the only identity in the building. For example, Priya books the laser for Thursday 19:00 from her phone on Monday night, then taps her fob at the laser on Thursday to claim it. Slack and Notion sign people in this way.
- **B: a personal booking link.** Each member gets one private web address, bookmarks it, and books from it. The front desk has to reissue it if it's lost or shared, and anyone who has it can book as you.
- **C: typing your fob number.** Fob numbers aren't secret, so anyone could book or cancel as someone else. That would also let people get around the one-booking laser rule.
- **None of these:** if the fob really must be the only way to identify a member, home booking can't work as it does now. I'd need to hear which of your two notes gives way.