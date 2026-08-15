# Activity: Daily session (orchestrator)

**Mode:** mixed — each step declares its own · **Trigger:** "session", "let's study", or similar

## 1. Load context

Read `student/profile.md`, `student/active.txt`, `student/<active>/progress.json` and `student/<active>/errors.md`. Run `python3 tools/srs.py streak` and `python3 tools/srs.py stats`.

## 2. Greet with context (5 lines max)

Streak, due cards, one thing from last session ("yesterday *borrow* tripped you twice"), and today's plan.

## 3. Build today's plan

Use the session template for their `daily_minutes` (`docs/methodology.md` §8), then adjust:

- Due cards > 0 → SRS review always goes first.
- ~7 study days since the last `weekly-check` history entry → it takes today's activity slot (`activities/weekly-check.md`).
- A `focus` set in `progress.json` (by the weekly check) wins ties among activities that can run and biases material choice — texts, scenarios and prompts lean toward it until the next check moves it.
- Check the last ~7 `history` entries for strand drift (§1) and `speaking_debt` flags. If the saved voice route is unavailable, filter every voice-required activity out of today's slots, keep the debt visible and choose the next neglected text strand. This applies to focus, debt and rotation; never spend a one-activity day merely deferring its only activity.
- One-activity days rotate: conversation → reading → listening → story-listening → writing → pronunciation → fluency → grammar+quiz.
- Unit finished → its checkpoint quiz. All units finished → propose the exam simulation.
- A `viewing: recommended` in recent history without a matching `watched` → ask in the greet; if they watched it, 2-min debrief + mine their jotted expressions into cards (methodology §11).

Present the plan with mode icons before starting: `1) 🃏 Review (12) → 2) 📖 Reading → 3) 🎙️ Conversation → 4) ✏️ Wrap`. The learner can swap steps — flexibility beats the plan, but voice-required steps can only be swapped, never silently converted to text.

## 4. Run the steps

Each step follows its own file in `activities/`. Between steps: one transition line, no ceremony. App steps: serve, open, wait on the event file, comment results (AGENTS.md §HTML apps). Keep the total time honest — if the budget is 30 min, cut material, not corrections.

## 5. Wrap up (always, even if the session was cut short)

1. `CORRECTIONS`-digest: the 1–3 things to remember from today.
2. Write-backs per AGENTS.md: errors, new cards (≤15/day), mastered words, `history` entry (date, activities, minutes, `speaking_debt` flags, one-line notes).
3. Advance `unit` in progress.json if its material was completed.
4. 1–2× per week (check recent history for the last `viewing:` note): recommend a menu of 3–4 movies/episodes per methodology §11 — matched to level and interests, with the subtitle setup and one rotating technique tip. Log the menu in the history notes.
5. Close with: what improved today + streak + a one-line teaser of tomorrow.
