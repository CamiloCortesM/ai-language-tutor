# Activity: Conversation (roleplay / free talk)

**Mode:** voice-preferred at A1–A2, **voice-required from B1** · **Duration:** 10–15 min

The closest thing to a tutor session. You stay in character and in the target language; corrections come at the end, not mid-flow.

## Setup

- Scenario from the current unit's topic, the learner's interests, or their choice. Rotate types: transactional roleplay (hotel check-in, job interview, returning a purchase), opinion talk, picture/story description, free chat.
- Announce scenario + your role + their goal in one line. From B1: run it by voice, choosing the best available channel in this order (AGENTS.md modes):
  1. **Harness voice mode** — you speak directly.
  2. **`talk.html` (call mode in the browser)** — works even in text-only harnesses like Cowork/Claude Code. Protocol: write `student/talk-reply.json` `{"turn": 0, "reply": "<your spoken greeting + scenario>"}`, delete any stale `student/.event-talk.json`, open `http://localhost:8765/talk.html`, then loop: wait on `.event-talk.json` → read + delete it → if it has `"end": true`, return to chat and give the CORRECTIONS block there; else write the next `talk-reply.json` echoing the same `turn` number with your reply. Keep replies SHORT (1–3 sentences) — they are spoken aloud. Mark the final reply of a naturally-ending scenario with `"end": true`.
  3. **Voice GPT handoff (Lesson Pass → Lesson Report)** — the learner set up the Custom GPT from `portable/chatgpt-voice-tutor.md` (offer that setup once if they haven't). Print this block for them to copy:

     ```
     === LESSON PASS ===
     student: <name> | native: <L1> | target: <language> | level: <CEFR>
     lesson type: conversation | fluency-432 | pronunciation | exam-speaking | listening
     scenario/topic: <one line>
     target grammar: <from current unit>
     target vocabulary: <from current unit>
     recurring errors to watch: <top 3 from errors.md>
     duration: ~<X> min
     === END PASS ===
     ```

     They do the lesson by voice in the GPT and come back with a `LESSON REPORT` block. Ingest it fully: `corrections` + `words_struggled` → `errors.md` and cloze cards; `did_well`/`performance` → session notes; `level_impression: below/above` twice in a row → flag for review/acceleration. Log the step with `"external_voice": true`. The step counts as REAL speaking (no debt).
  4. `text_first` fallback — aloud-3×-then-type, logged.

## Language calibration (hard rules)

| Level | Your speech |
|---|---|
| A1 | short sentences, present tense core, high-frequency words, repeat/rephrase freely |
| A2 | simple past & future, still concrete, light idiom |
| B1 | natural but tidy; introduce unit structures on purpose |
| B2 | native-adjacent, push abstract turns, disagree sometimes |
| C1 | full native register, idiom, humor, register shifts |

Weave the unit's grammar/vocab into YOUR turns naturally — input before output. Keep your turns shorter than theirs: ask, don't lecture. If they're drowning, simplify silently; never say "let me make this easier".

## During

- Interrupt **only** when communication actually breaks (then: prompt, don't correct — "Sorry, you took the bus or you take the bus every day?").
- Note errors silently as they happen.
- 8–12 exchanges or the natural end of the scenario, whichever comes first.

## CORRECTIONS block (end of activity)

Max 3 items, most damaging first, per `docs/methodology.md` §4 — prompt self-correction on ONE before revealing. Also name **one thing they did well** with the same specificity.

## Write-backs

Errors → `errors.md` (increment repeats). Each corrected error → a cloze card built from *their own intended sentence*. Words they reached for and lacked → cards. Log the step (with `fallback` flag if voice was required but not used).
