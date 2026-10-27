# Recorded technical training Q&A

The [two published exchanges](../docs/qa.mjs) are selected from stored technical training conversations. Both prompts explicitly describe exercises, not customer vehicles. The Vietnamese question and answer text is preserved; English is an **editorial translation**, not a claim that the model originally answered in English.

The images in this repository are rendered from these excerpts. They are **not Telegram screenshots**. Persistence in a local conversation log does not independently prove delivery on Telegram. Full transcripts and internal account/session metadata are not published.

## What was reviewed

1. **Measurements need circuit context:** without a diagram and applicable limits, a static reading cannot by itself classify the branch as good or faulty. The example distinguishes passive ground from a PWM-controlled terminal.
2. **Intermittent failures need failure-time evidence:** a result before an intermittent stop does not rule out a fault at the stop; command, waveform and current should be compared in the relevant event window. No part is declared failed in the published answer.

This is a focused review of the displayed reasoning, not a certification of all assistant answers or an OEM procedure for a real vehicle. Other reviewed answers contained overclaims and were not selected. The public examples do not erase those known limitations.

## Independent references used after the conversation

- [Fluke — Diagnosing voltage drops](https://www.fluke.com/en-au/learn/blog/automotive/electrical-automotive-troubleshooting): relevant general measurement principles and testing under operating load.
- [Pico Automotive staff — Data over PWM?](https://www.picoauto.com/support/viewtopic.php?t=22356): PWM signals and comparing current/signal behavior in automotive diagnostics.

These references support a general-principle review; they were not verified as the original model’s citations and do not establish the wiring or limits of a particular vehicle. No manufacturer repair is implied.
