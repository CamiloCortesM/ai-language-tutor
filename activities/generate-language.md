# Activity: Generate a new target language

**Mode:** chat · **When:** the learner wants a language with no `languages/<target>/` folder yet (e.g. "hablo español pero quiero aprender francés")

Turns the repo's structure into a curriculum factory: English is the reference implementation; any language follows its shape.

## 1. Confirm and set up

1. Confirm the target language and tell them honestly it will be generated (and reviewed as they use it), unlike the shipped English one.
2. Create `student/<target>/` (copy the file set from `student.example/english/`), add the language to `learning:` in the profile, write `student/active.txt`.

## 2. Generate the curriculum — level by level, never all at once

First create `languages/<target>/cefr-syllabus.md` following the structure of `languages/english/cefr-syllabus.md`: per-level can-do, **that language's** CEFR-criterial grammar, vocab ranges, and the official exam formats — DELF/DALF for French, Goethe for German, JLPT-mapped for Japanese, etc. It is the source the units, placement test and exam simulator read.

Then `languages/<target>/curriculum/overview.md` (adapt the English one: guided hours, vocab targets, exam per level).

Then generate ONLY the level the learner needs now (A1 for a beginner; their placement level otherwise), 12 units, using the English units as the structural template:

- Same sections: Can-do / Grammar focus / Target vocabulary (10–12, target-language-only with simple glosses) / Functions & phrases / Suggested activities / Watch out.
- Grammar must be **that language's CEFR-criterial grammar** (what French A1 actually teaches: articles and gender, être/avoir, -er verbs… — not a translation of the English units).
- Start every generated file with: `> Generated curriculum — review welcome.`
- Non-Latin scripts: add a romanization/script-learning thread to the first units.

Generate the next level when the learner is ~2 units from finishing the current one.

## 3. L1 notes

Generate `languages/<target>/l1-notes/<native_language>.md` (pronunciation priority queue, grammar traps, false friends) following `languages/english/l1-notes/spanish.md` as the model.

## 4. Run the placement test

`activities/placement-test.md` as usual, in the new language, seeding `student/<target>/`.

## 5. Suggest contributing

The generated folder is exactly what the project needs to officially support that language: suggest opening a PR. The next learner finds it ready.

## Switching between languages (already-set-up learner)

"Switch to French" → write `student/active.txt`, greet in that language, run sessions normally. Streaks, decks and levels are fully independent per language; the apps and `tools/srs.py` follow `active.txt` automatically. Warn once if a language goes untouched ~2 weeks (its SRS reviews pile up).
