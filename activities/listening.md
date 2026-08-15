# Activity: Listening

**Mode:** chat + generated audio · **Duration:** 10–15 min

The interaction stays in text; audio comes from `dictation.html` or TTS. Live voice-model storytelling is the separate `story-listening` activity, so never ask the learner to choose text versus voice here.

## Formats (rotate)

1. **Dictation** (A1–B1 staple): 4–6 sentences using unit grammar/vocabulary, spoken at natural-but-clear pace. Immediate per-sentence check exposes exactly which sounds and word boundaries they do not parse.
2. **Comprehension:** a short spoken text (same generation rules as reading — 95–98% known words), then 3 questions in chat. B2+ hears it once unless replay is part of the stated format.
3. **Micro-listening** (A1–A2): minimal-pair rows and numbers/dates/times — hear it, type it.

## Run it

With a browser, use `dictation.html` for every precision format. Write `student/dictation-current.json` (AGENTS.md §HTML apps), open the app and let the learner control replay. The app provides one player per sentence and keeps text folded behind “show text.”

No browser → use TTS one item per turn, repeat verbatim on request (A1–A2: up to twice), and keep the answer out of visible commands. An explanation and its audio never share a turn.

- Check answers and classify every miss: unknown vocabulary or perception of a known word.
- When connected speech caused it, name the link briefly: `ran out of` → “ra-nau-tov”.
- No audio available → swap for reading and log the swap; never fake listening by showing the script first.

## Write-backs

Perception failures on known words → the pronunciation target queue and `student/<active>/errors.md`. Unknown useful words → contextual cloze cards. Log the step.
