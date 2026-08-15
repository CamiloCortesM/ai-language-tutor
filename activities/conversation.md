# Activity: Conversation (roleplay / free talk)

**Mode:** voice-required at every level · **Duration:** 10–15 min

The closest thing to a tutor session. The voice tutor stays in character and the learner actually speaks; this activity is never converted to text.

## Setup and handoff

- Choose a scenario from the current unit, the learner's interests or their request. Rotate transactional roleplay, opinion talk, picture/story description and free conversation.
- Write **6–8 exact, numbered learner-facing questions** that form one coherent scene. Each question is used once. The answer to the last one is the objective end; duration is only a pacing target.
- Set `closing: one_self_correction_if_available`, then use the saved `voice_channel` and the canonical controller in `portable/voice-tutor.md`: run it here for `same_workspace`, populate **CODEX/WORK VOICE ACTIVITY** for `codex_work`, or populate the canonical **LESSON PASS JSON** for `external`.
- Give the model-confusion and hang-up warning from `AGENTS.md` before starting on every route. If the channel is `none` or unavailable, defer the activity and log `"speaking_debt": true`; do not run a typed roleplay.
- For `codex_work`, include absolute paths and exact Memory write-backs. For `external`, ingest the returned `LESSON REPORT`: `corrections` + contextual `words_struggled` entries → errors and cards; `pronunciation` → perception/production error lines and the next pronunciation target queue; `did_well`/`performance` → session notes; `level_impression: below/above` twice running → flag for review/acceleration. A report with `completed: false` is logged as partial, never as a completed activity.

## Language calibration

| Level | Voice tutor's speech |
|---|---|
| A1 | short sentences, present tense core, high-frequency words, repeat/rephrase freely |
| A2 | simple past and future, still concrete, light idiom |
| B1 | natural but tidy; introduce unit structures on purpose |
| B2 | native-adjacent, push abstract turns, disagree sometimes |
| C1 | full native register, idiom, humor, register shifts |

Weave the unit's grammar and vocabulary into the tutor's turns naturally — input before output. Keep tutor turns shorter than learner turns. Simplify silently if the learner is drowning.

During the numbered plan, note errors without interrupting. Interrupt only when communication breaks, using a prompt rather than a correction. The shared controller prevents courtesy-only dead ends, repeated questions and extra rounds.

## Write-backs

Errors → `student/<active>/errors.md` (increment repeats). Each corrected error → a contextual cloze card based on the learner's intended sentence; words they reached for and lacked → contextual cards. Log completed or partial status and any `speaking_debt`.
