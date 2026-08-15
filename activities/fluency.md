# Activity: Fluency development

**Mode:** voice-required · **Duration:** ~10 min · At least weekly

**Only known language** — zero new vocabulary, zero new grammar. The goal is speed and automaticity with what they already own. If they're reaching for new words, the topic is too hard — swap it.

## 4/3/2 (the staple)

1. Learner picks (or you offer) an easy, personal topic: my family, my job, my last trip, my favorite show.
2. 1 minute to think — **no notes**.
3. Use the saved `voice_channel` and the `fluency` type in `portable/voice-tutor.md`. The finite plan is exactly: preparation, round 1, round 2, round 3. Preparation completes when the learner says ready or skip. Each timed round completes only when its timer ends after the learner speaks, or the learner explicitly stops/skips; a short utterance alone does not complete it. They give the same talk **4 → 3 → 2 minutes** (A1–A2: 2 → 1.5 → 1); set `closing: none` and give no corrections at any point.
4. Rounds back-to-back; the shrinking clock forces faster retrieval of the same content.

After: point at fluency gains only ("round three had almost no pauses") — accuracy feedback and accuracy-error logging are off today by design.

## Alternatives (rotate in)

- **Timed re-reading**: finite `fluency` plan with exactly three timed passes of one previous text.
- **Question sprint** (A1–A2): finite `fluency` plan with 10 exact known questions, then the same 10 once more, faster.

## Write-backs

Log the step (topic, rounds, rough words-per-round trend). If the saved voice route is unavailable, reschedule rather than fake it and log `"speaking_debt": true`.
