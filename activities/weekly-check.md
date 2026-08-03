# Activity: Weekly check (progress pulse)

**Mode:** mixed — speaking part voice-preferred · **Duration:** 15–20 min · **Cadence:** every ~7 study days (session.md proposes it)

Not the level gate — that's `exam-simulator.md`. This is a short four-skill pulse whose job is to (a) show the learner what actually improved this week and (b) decide what next week focuses on. It should feel like a highlight reel of the week, not an exam.

## Build it (4 parts, ~4 min each)

Content comes from THIS week's material (units covered, new cards, recent errors). Difficulty at level. Weight the parts toward the current `focus` in `progress.json` and the top of `errors.md` — the weak skill gets the longest part. No hints during a part; feedback after all four.

1. **Listening** — 3–4 TTS sentences (dictation.html, or chat with `tts.py`) + 2 comprehension questions.
2. **Reading** — one short known-words text + 3 questions (chat or quiz.html).
3. **Writing** — 3–4 sentences on a prompt that forces the week's structures.
4. **Speaking** — 1-min mini-talk on a week topic: current agent voice if active; otherwise the optional bridge (Lesson Pass, `lesson type: exam-speaking`, ~4 min), else aloud-3×-then-type, logged as fallback.

## Score & steer

- Per part: **✓ solid · ± wobbly · ✗ needs work** — no percentages, this gates nothing.
- Verdict to the learner, 2 lines: what clearly improved since last week (be specific — "your past-tense questions came out clean first try") + what next week focuses on and why.
- Write that focus to `progress.json` as `"focus": "<one concrete thing>"` (e.g. `"listening at natural speed"`, `"past simple questions"`). Session planning biases toward it until the next check moves it.

## Write-backs

New errors → `errors.md`; misses worth keeping → cards. History entry: `weekly-check: L✓ R± W✓ S✗ → focus: <X>`. Log fallback flags as usual.
