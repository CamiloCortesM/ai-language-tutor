# Activity: Story listening

**Mode:** voice-required · **Duration:** 8–12 min

The tutor tells a short, level-appropriate story aloud in the target language. The learner listens and answers questions aloud. It trains comprehension of natural speech without showing the story text first.

## Run it

1. Use the saved `voice_channel` and `portable/voice-tutor.md`; if unavailable, defer and log `speaking_debt` rather than substituting text.
2. Pick a topic from the current unit or the learner's interests. Keep the story at 95–98% known words and introduce at most 2–3 useful new words.
3. Build a finite listening plan: STEP_1 tells the exact story and ends with one gist question; STEP_2 asks one detail question; STEP_3 asks one opinion/prediction question. A1–A2 may request one verbatim replay; B1+ gets one play unless they explicitly request a replay. Set `closing: one_self_correction_if_available`.
4. Do not reveal the story text before the learner answers. The shared controller ends immediately after the final answer, with one self-correction attempt only if a real error occurred.

## Write-backs

Log missed known words as perception errors, unknown useful words as contextual cards, and the activity in `student/<active>/progress.json` history as `story-listening`. A deferred activity is speaking debt, not completed listening.
