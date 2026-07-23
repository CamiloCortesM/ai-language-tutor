# Activity: Daily session (orchestrator)

**Mode:** mixed — each step declares its own · **Trigger:** "session", "let's study", or similar

## 1. Load context

Read `student/profile.md`, `student/progress.json`, `student/errors.md`. Run `python3 tools/srs.py streak` and `python3 tools/srs.py stats`.

## 2. Greet with context (5 lines max)

Streak, due cards, one thing from last session ("yesterday *borrow* tripped you twice"), and today's plan.

## 3. Build today's plan

Use the session template for their `daily_minutes` (`docs/methodology.md` §8), then adjust:

- Due cards > 0 → SRS review always goes first.
- Check the last ~7 `history` entries for strand drift (§1) and speaking debt (`fallback` flags) — the neglected strand wins today's activity slot.
- One-activity days rotate: conversation → reading → listening → writing → pronunciation → fluency → grammar+quiz.
- Unit finished → its checkpoint quiz. All units finished → propose the exam simulation.
- Honor `voice: always` (whole session by voice, oral variants) per AGENTS.md.

Present the plan with mode icons before starting: `1) 🃏 Review (12) → 2) 📖 Reading → 3) 🎙️ Conversation → 4) ✏️ Wrap`. The learner can swap steps — flexibility beats the plan, but voice-required steps can only be swapped, never silently converted to text.

## 4. Run the steps

Each step follows its own file in `activities/`. Between steps: one transition line, no ceremony. App steps: serve, open, wait on the event file, comment results (AGENTS.md §HTML apps). Keep the total time honest — if the budget is 30 min, cut material, not corrections.

## 5. Wrap up (always, even if the session was cut short)

1. `CORRECTIONS`-digest: the 1–3 things to remember from today.
2. Write-backs per AGENTS.md: errors, new cards (≤15/day), mastered words, `history` entry (date, activities, minutes, fallback flags, one-line notes).
3. Advance `unit` in progress.json if its material was completed.
4. Close with: what improved today + streak + a one-line teaser of tomorrow.
