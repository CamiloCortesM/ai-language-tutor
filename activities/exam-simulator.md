# Activity: Exam simulator (level gate)

**Mode:** mixed — written papers in chat/app, **speaking paper voice-required, no exceptions** · **Duration:** 45–90 min, can split across 2 days (papers are independent)

Run when all 12 units of the level are done, or on request as practice (practice runs don't gate).

## Build the exam

Model it on the level's official exam format for the active language (`languages/<target>/cefr-syllabus.md`). English → Cambridge: A1/A2 → Key-style (reading/writing + listening + speaking) · B1 → Preliminary · B2 → First (adds Use of English: word formation, key-word transformation, open cloze) · C1 → Advanced. Other languages → the exam mapped in their syllabus (DELF/DALF, Goethe, JLPT…). Scale to ~half the parts of the real exam per paper — enough signal, not a whole afternoon. Content draws on the level's units; nothing above level.

Exam conditions: no hints, no corrections mid-paper, time limits stated per part (soft-enforced). Say so up front.

## Papers

1. **Reading (+ Use of English from B2)** — texts follow the known-words rule *for the level*, not for the learner (this is a test, not input).
2. **Writing** — level task from `writing.md` table, scored with the CEFR rubric under exam strictness.
3. **Listening** — spoken texts, questions after one play (two at A1–A2).
4. **Speaking** — interview + picture/topic long turn + (B1+) discussion. Before handoff, write every prompt as a finite numbered plan in `portable/voice-tutor.md`, with observable completion for each and `closing: none`. Use the saved voice route. If it is unavailable, schedule this paper separately; the exam cannot gate the level and no typed substitute counts.

## Scoring & verdict

Per-paper % and overall (papers weighted equally). **Gate: ≥70% overall AND ≥60% on every paper** (`docs/methodology.md` §9).

- **Pass:** update `level` in `student/<active>/progress.json`, reset `unit: 1`, celebrate with specifics, preview the new level.
- **Fail:** no drama — produce the error profile (which units/structures failed), build a targeted review plan (those units back into rotation), retake in ≥1 week. Log everything to `errors.md` and the session history.
