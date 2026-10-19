# Pacing outgoing text alerts

A district council runs a free text-message alert service: residents sign up for flood warnings, road closures and bin-day changes for their area. Messages go out through a mobile operator's SMS gateway under one registered sender ID. A single worker process takes queued messages and submits them to the gateway one at a time. The pacing part of that worker is being rewritten; two candidates are below.

**From the service owner:**

> Most days we send a few hundred messages, spread out. Flood warnings are the exception: the river team presses the button and 1,500 to 2,000 people in the valley need the message. The faster the first ones go out the better, but what really matters is that all of them go out and nobody is skipped. Half an hour to reach everyone is acceptable; we've been doing that for years.

**From the gateway agreement (section 4, Traffic), pasted by the developer:**

> 4.1 Messages must be submitted from the registered sender ID only.
> 4.2 Throughput: one (1) message per second per sender ID. The gateway accepts at most one message from a sender ID in any one-second interval; further messages in that interval are rejected with status 429.
> 4.3 A sender ID receiving more than 20 rejections under 4.2 in a calendar day is suspended for 24 hours. Suspension is lifted by the operator's support desk only.
> 4.4 Message bodies longer than 160 characters are split and charged per part.

**From the developer:**

> The worker is single-threaded: it calls `pace()` before each submit and nothing else talks to the gateway. Timing uses the monotonic clock. A failed submit (network error) goes back on the queue, and is submitted again later through `pace()` like any other message.

Two candidate implementations follow. Which one is the better design?
