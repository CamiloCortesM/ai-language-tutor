# Activity: Conversation (roleplay / free talk)

**Mode:** voice-required at every level · **Duration:** 10–15 min

The closest thing to a tutor session. The voice tutor stays in character and the learner actually speaks; this activity is never converted to text.

## Setup and handoff

- Choose a scenario from the current unit, the learner's interests or their request. Rotate transactional roleplay, opinion talk, picture/story description and free conversation.
- Write **6–8 exact, numbered learner-facing questions** that form one coherent scene. Each question is used once and has `complete_when: one good-faith learner answer, including "I don't know" or "skip"`. The answer to the last one is the objective end; duration is only a pacing target.
- Set `closing: one_self_correction_if_available`, then populate the canonical **LESSON PASS JSON** for the external voice tutor using the controller in `portable/voice-tutor.md`.
- Give the learner handoff instructions and both report-recovery options from `AGENTS.md` before starting. If the channel is `none` or unavailable, defer the activity and log `"speaking_debt": true`; do not run a typed roleplay.
- After central report validation, ingest the returned `LESSON REPORT`: `corrections` + contextual `words_struggled` entries → errors and cards; `pronunciation` → perception/production error lines and the next pronunciation target queue; `did_well`/`performance` → session notes; supported `level_impression: below/above` twice running → flag for review/acceleration. Ignore `not_assessed`. A report with `completed: false` is logged as partial, never as a completed activity.

## Language calibration

Use the single A1–C1 language policy in `portable/voice-tutor.md`; do not restate it here. Weave the unit's grammar and vocabulary into the tutor's turns naturally — input before output. Keep tutor turns shorter than learner turns. Simplify silently if the learner is drowning.

During the numbered plan, note errors without interrupting. Interrupt only when communication breaks, using a prompt rather than a correction. The shared controller prevents courtesy-only dead ends, repeated questions and extra rounds.

## Write-backs

Errors → `student/<active>/errors.md` (increment repeats). Each corrected error → a contextual cloze card based on the learner's intended sentence; words they reached for and lacked → contextual cards. Log completed or partial status and any `speaking_debt`.
