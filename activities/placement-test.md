# Activity: Placement test

**Mode:** chat (+ a short voice probe if available) · **When:** first run only · **Duration:** ~15–20 min

Determines the learner's CEFR level and creates their profile. Be warm and brief — this is their first impression.

## 1. Setup questions

**Very first message, before anything else: ask their native language.** They may not read English yet, so ask in two lines — English plus your best guess from how they greeted you (their wording, script, locale): *"What's your native language? / ¿Cuál es tu idioma nativo?"*. Just the question — no greeting speech, no explanation of how languages will be used later; that belongs in §5. From their answer on, run the setup and the test in that language.

Then ask, conversationally, not as a form: name; **which language they want to learn** (default English; no curriculum folder for it yet → AGENTS.md language policy: offer to generate one); why they're learning (goals); topics they enjoy (interests); realistic minutes per day; voice preference. Ask whether they want `always_on`, `when_required`, or `text_first`; explain that speaking practice works much better aloud and that text activities stay in text. Also ask where they can use voice: in the current agent/workspace, OpenAI Work/Codex voice, an external voice AI such as Claude or regular ChatGPT, or nowhere. Save the matching `voice_channel`; never assume Work/Codex voice is available.

## 2. Adaptive assessment

Start at A2 and move up/down by performance. At each level probe with 3–4 quick tasks drawn from that level's criterial features (see `languages/<target>/curriculum/overview.md` and `languages/<target>/cefr-syllabus.md`):

- **Grammar recognition:** 2 choose-the-correct-sentence items using that level's structures.
- **Production:** one short prompt ("Describe your typical morning", "What would you do if…") — judge range and accuracy, not just errors.
- **Vocabulary:** ~8 words sampled across levels — ask for meaning or use in a sentence.
- **Reading micro-check:** 2–3 sentences at that level, one comprehension question.

Rules: clearly comfortable → move up a level; struggling → move down; stop when you find the boundary (comfortable at X, struggling at X+1) → their level is X. Two probes per level are enough; don't drag it out.

## 3. Speaking probe (if voice available)

1 minute: introduce yourself / describe your city. Use the current agent's voice when active; otherwise ask the learner to turn it on if their preference allows it, then offer the optional bridge or the aloud fallback. Note pronunciation issues and fluency — this refines the level and seeds `placement_notes`, it rarely changes the level by itself.

## 4. Write everything

1. Copy `student.example/` → `student/` if not done.
2. Fill `student/profile.md` completely (including `placement_notes`: 2–3 lines of observed strengths/gaps).
3. Set `level` and `unit: 1` in `student/progress.json`.
4. Seed `student/known_words.txt`: generate ~150–400 highest-frequency words of the target language that this learner demonstrably handles at their level (be conservative — reading sessions will grow the list fast).
5. Seed 10–15 cards (`python3 tools/srs.py add`) from: words/structures they missed in the test + their interests. Card format per `docs/methodology.md`.
6. Log the errors observed → `student/errors.md`.

## 5. Present the result

Level + what it means concretely ("B1: you can handle most travel situations…"), the road ahead (units to next level, realistic timeline at their daily minutes), and how tomorrow works: *"Say **session** and I'll take care of the rest."*

Before the first lesson, in their L1, set the language expectation in two lines: **the material — texts, audio, conversation — is always in the target language, that's what makes it work**; explanations start in their language and shift to the target as they level up. And the escape hatch, said out loud once: *"if something doesn't land, just say 'en español' and I'll explain it there — no problem."*
