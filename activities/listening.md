# Activity: Listening

**Mode:** voice-preferred (audio via `tools/tts.py`, the current agent's voice, or an optional bridged lesson) · **Duration:** 10–15 min

Before starting, offer two paths when both are available: **app** for learner-controlled replay or **voice** for a live listening lesson. Recommend the path that matches the format, but let the learner choose.

Three audio sources, per AGENTS.md — pick by lesson kind:
- **Voice lesson** (best for comprehension): use the current agent's voice when active. Tell a short level-appropriate text or dialogue, then ask gist, detail and opinion questions aloud. If it is unavailable, use the optional bridge (`lesson type: listening` in the Lesson Pass — include the topic, target vocab, and any exact sentences). Natural speech + live questions beats synthetic audio here.
- **App lesson** (best for precision): use `dictation.html` for dictation, micro-listening, or any material the learner should replay identically and at their own pace. Repeats MUST be identical, never paraphrased.
- No audio at all → swap for reading and log the swap; never fake listening by having them read.

## Formats (rotate)

1. **Dictation** (A1–B1 staple): 4–6 sentences using unit grammar/vocab, spoken at natural-but-clear pace, learner writes each. Immediate per-sentence check — dictation exposes exactly which sounds and word boundaries they don't parse.
2. **Comprehension**: a short spoken text (same generation rules as reading — 95–98% known words, level-length), then 3 questions. B2+: play it once only, like real life.
3. **Micro-listening** (A1–A2): minimal-pair rows and numbers/dates/times — hear it, write it.

## Run it

**Dictation (and any precision format) defaults to `dictation.html`.** Write `student/dictation-current.json` (format in AGENTS.md §HTML apps), open `http://localhost:8765/dictation.html`, and from then on **the learner controls the audio** — the app gives one player per sentence with play, scrub and right-click loop, and keeps each sentence's text folded behind "show text". If the learner explicitly chooses voice, deliver one sentence at a time by voice, repeat it verbatim on request, and do not show its text before their answer.

The split is the point:

| Browser | Chat |
|---|---|
| the audio, replayed as many times as they want | they type what they heard |
| the text, folded, opened only to self-check | you analyse the mishearing, then say which sentence is next |

Why not play it from chat: audio fired from the terminal starts while the learner is still reading your message, they can't replay it without asking you every time, and the command line shows them the sentence in plain text before they hear it — which invalidates the exercise. One sentence per turn; they move it forward.

No browser → speak or TTS the material in chat, repeating on request (A1–A2: twice), and keep the sentence out of any visible command.

- Check answers; every mishearing is data: was it vocabulary (unknown word) or perception (known word, unrecognized sound)?
- **Name the connected-speech rule when it's the cause** — `ran out of` → "ra-nau-tov". Learners read this as their own failure; it's linking, and it's the main reason B1 reading coexists with A2 listening.

## Write-backs

Perception failures on known words → feed `pronunciation.md`'s target queue (note the sound pair in `errors.md`, e.g. `heard "ship" as "sheep"`). Unknown words → cards. Log the step.
