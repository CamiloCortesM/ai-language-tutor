# Activity: Listening

**Mode:** voice-preferred (needs audio: agent voice or `tools/tts.py`, learner's choice) · **Duration:** 10–15 min

Three audio sources, per AGENTS.md — pick by lesson kind:
- **Comprehension lessons** (formats 2 and interactive gist work): best as a **voice-GPT handoff** (`lesson type: listening` in the Lesson Pass — include the topic, target vocab, and any exact sentences) or your own voice mode. Natural speech + live questions beats synthetic audio here.
- **Precision work** (dictation, micro-listening, exam audio): `python3 tools/tts.py say` or in-chat TTS — repeats MUST be identical, never paraphrased.
- No audio at all → swap for reading and log the swap; never fake listening by having them read.

## Formats (rotate)

1. **Dictation** (A1–B1 staple): 4–6 sentences using unit grammar/vocab, spoken at natural-but-clear pace, learner writes each. Immediate per-sentence check — dictation exposes exactly which sounds and word boundaries they don't parse.
2. **Comprehension**: a short spoken text (same generation rules as reading — 95–98% known words, level-length), then 3 questions. B2+: play it once only, like real life.
3. **Micro-listening** (A1–A2): minimal-pair rows and numbers/dates/times — hear it, write it.

## Run it

- Speak or TTS the material; repeat once on request (A1–A2: twice).
- Check answers; every mishearing is data: was it vocabulary (unknown word) or perception (known word, unrecognized sound)?

## Write-backs

Perception failures on known words → feed `pronunciation.md`'s target queue (note the sound pair in `errors.md`, e.g. `heard "ship" as "sheep"`). Unknown words → cards. Log the step.
