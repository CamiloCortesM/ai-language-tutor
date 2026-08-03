# Activity: Conversation (roleplay / free talk)

**Mode:** voice-preferred at A1–A2, **voice-required from B1** · **Duration:** 10–15 min

The closest thing to a tutor session. You stay in character and in the target language; corrections come at the end, not mid-flow.

## Setup

- Scenario from the current unit's topic, the learner's interests, or their choice. Rotate types: transactional roleplay (hotel check-in, job interview, returning a purchase), opinion talk, picture/story description, free chat.
- Announce scenario + your role + their goal in one line, then follow the voice-channel priority in `AGENTS.md`. For `codex_work`, put the complete conversation details, absolute project root and exact Memory write-backs into the **CODEX/WORK VOICE ACTIVITY** prompt. Define 6–8 numbered roleplay questions followed by exactly one correction attempt. The voice task must use three states: numbered ROLEPLAY steps, CORRECTION, then FINISHED. During ROLEPLAY every response ends with the next required question—never a courtesy-only dead end. The answer to the final question triggers CORRECTION; the very next learner utterance triggers FINISHED regardless of what they say. FINISHED gives the `VOICE RESULT`, tells the learner they may end the call, and the post-call transcript handoff immediately updates and verifies the project files. Never restart, ask “anything else?”, wait for `done`, or offer another scenario. Only for `external`, populate and send this Lesson Pass:

     ```
     === LESSON PASS JSON ===
     {
       "student": "<name>",
       "native_language": "<L1>",
       "target_language": "<language>",
       "level": "<CEFR>",
       "lesson_type": "<conversation | fluency-432 | pronunciation | exam-speaking | listening>",
       "scenario": "<one line>",
       "target_grammar": ["<from current unit>"],
       "target_vocabulary": ["<from current unit>"],
       "recurring_errors": ["<top 3 from errors.md>"],
       "pronunciation_focus": ["<top 1–2 sound targets, or none yet>"],
       "correction_style": "quick recast in the moment (max 1 per learner turn), full corrections at the end",
       "duration_minutes": <number>
     }
     === END PASS ===
     ```

     For `codex_work`, the voice task performs these write-backs itself. For `external`, ingest the `LESSON REPORT`: `corrections` + `words_struggled` → `errors.md` and cards; `pronunciation` → `errors.md` as `percepción/producción` lines and the next pronunciation step's target queue (methodology §6 — perception before production); `did_well`/`performance` → session notes; `level_impression: below/above` twice in a row → flag for review/acceleration. Log the step with `"external_voice": true`. The step counts as REAL speaking (no debt).
  `text_first` fallback — aloud-3×-then-type, logged.

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

- **Real-time micro-corrections (chat):** reply in character; if their turn had an error worth fixing, append ONE footnote line, visually apart from the roleplay — `✏️ *I have 20 years* → *I'm 20 years old*`. Max one per turn, the most damaging error; the rest wait for the end block. No explanations in the footnote — the story never stops for grammar.
- Interrupt the flow itself **only** when communication actually breaks (then: prompt, don't correct — "Sorry, you took the bus or you take the bus every day?").
- Note everything else silently as it happens.
- 8–12 exchanges or the natural end of the scenario, whichever comes first.

## CORRECTIONS block (end of activity)

Max 3 items, most damaging first, per `docs/methodology.md` §4 — prompt self-correction on ONE before revealing. Also name **one thing they did well** with the same specificity.

## Write-backs

Errors → `errors.md` (increment repeats). Each corrected error → a card whose example sentence is *their own intended sentence* (word = the corrected chunk). Words they reached for and lacked → cards. Log the step (with `fallback` flag if voice was required but not used).
