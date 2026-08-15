# Architecture — AI Language Tutor (A1 → C1)

> Synthesis of the research in `docs/research/`. Living design document — kept in sync with the implementation.

## Design principles

1. **Portable / harness-agnostic.** Everything the tutor needs lives in markdown that any AI agent (Claude Code, Cursor, Gemini CLI…) can read. Entry point: `AGENTS.md` (a convention most agents already support); `CLAUDE.md` just redirects to it. "Skills" are plain markdown files in `activities/` — instructions, not proprietary code.
2. **The LLM is the tutor; files are the memory; scripts are the clock.** Code exists only where the LLM is a poor substitute: SRS scheduling (FSRS) and the streak. Everything else (generating texts, correcting, conversing, examining) is instructions.
3. **Multi-language by design — on both sides.** The method (`activities/`, `docs/methodology.md`) is language-agnostic. Everything specific to a **target** language lives under `languages/<target>/` (curriculum, vocab lists); English ships first, adding a language = adding a folder. The learner's **native** language (any L1) is just a profile field: curriculum files are target-language-only, and all L1-specific material — hints, translations, contrastive explanations — is generated at runtime for that learner. Optional `l1-notes/<L1>.md` files capture known pitfalls per language pair (Spanish ships first); when absent, the tutor uses its own contrastive knowledge.
4. **Multi-user.** Learner data lives in `student/` (gitignored). The repo ships `student.example/` as a template; the placement test fills it in on first use.
5. **Evidence-based** (see `docs/research/evidence-based-methods.md`): Nation's four strands ~25% each, comprehensible input at 95–98% known words, spaced retrieval practice, brief explicit grammar with *focus on form*, correction via *prompts* (self-correction), HVPT/minimal pairs for pronunciation.
6. **Modality follows the activity.** Normal teaching stays in text. Conversation, pronunciation production, fluency and assessed speaking use a real voice model through the saved route in `profile.md`; they are deferred, never typed, when voice is unavailable. TTS (`tools/tts.py`) covers read-alouds and precision audio.

## Repo structure

```
learning-language/
├── README.md              # for humans: what this is, get started in 3 steps
├── AGENTS.md              # for the agent: tutor identity, rules, what to read and when
├── CLAUDE.md              # 1 line: "Read AGENTS.md"
├── docs/
│   ├── research/          # evidence behind the design (already written)
│   ├── methodology.md     # the tutor's pedagogical rules (distilled from research)
│   └── architecture.md
├── activities/            # portable "skills" (plain markdown, language-agnostic)
│   ├── placement-test.md  # adaptive test → determines level, creates the profile
│   ├── session.md         # THE DAILY ENTRY POINT: orchestrates by time/level
│   ├── srs-review.md      # due-card review (uses tools/srs.py)
│   ├── conversation.md    # roleplay at the learner's level + CORRECTIONS block
│   ├── reading.md         # generated graded reader / assisted reading (LingQ-style)
│   ├── listening.md       # text-guided dictation/comprehension with fixed TTS audio
│   ├── story-listening.md # voice-model story comprehension + spoken questions
│   ├── writing.md         # writing task + CEFR-rubric correction
│   ├── pronunciation.md   # minimal pairs, shadowing, L1-specific trouble sounds
│   ├── grammar-lesson.md  # brief explicit lesson + communicative practice
│   ├── fluency.md         # 4/3/2 and automatization activities
│   ├── exam-simulator.md  # official-exam-style mock (Cambridge/DELF/…) — gate to next level
│   └── generate-language.md # generates the curriculum for a new target language
├── languages/
│   └── english/
│       ├── cefr-syllabus.md   # per-level spec: can-do, criterial grammar, vocab, official exams
│       ├── curriculum/
│       │   ├── overview.md    # A1→C1 map: hours, vocab targets, level-up criteria
│       │   ├── a1/            # ~10-12 units per level: unit-01.md, unit-02.md…
│       │   ├── a2/  b1/  b2/  c1/   # each unit: grammar + target vocab + functions
│       └── l1-notes/
│           └── spanish.md     # typical errors for Spanish speakers (phonology, grammar, false friends)
├── student/               # learner data (gitignored)
│   ├── profile.md         # shared: name, L1, languages studied, daily time, voice route
│   ├── active.txt         # which language is active ("switch to X" updates it)
│   └── <language>/        # one folder PER language studied — fully independent:
│       ├── progress.json  #   streak, level, current unit, weekly focus, history
│       ├── errors.md      #   recurring-error log (feeds lessons and cards)
│       ├── known_words.txt #  known lemmas (drives the comprehensibility ratio)
│       ├── cards.json     #   contextual cloze deck with FSRS state
│       └── img/           #   card images (downloaded once via srs.py img, offline after)
├── student.example/       # commented template of all of the above
├── portable/
│   └── voice-tutor.md     # voice bridge: run spoken lessons in any voice AI
├── apps/                  # self-contained HTML apps (no frameworks, no build)
│   ├── flashcards.html    # SRS review UI: flip cards, Again/Hard/Good/Easy, browser TTS
│   ├── quiz.html          # written tests per unit: MCQ, gap-fill; self-grading
│   ├── dashboard.html     # streak, vocab growth, level progress, top errors
│   ├── dictation.html     # replayable precision listening
│   └── reader.html        # assisted reading: tap word → gloss → contextual card
└── tools/
    ├── srs.py             # FSRS (minimal formulas) + due list + streak. Python stdlib.
    ├── serve.py           # stdlib server: serves apps/ + JSON API over student/
    ├── tts.py             # neural TTS (edge-tts free / OpenAI / ElevenLabs) with cache
    └── voice_selfcheck.py # verifies the durable external-voice contract
```

## HTML apps

Visual activities live in `apps/` as self-contained HTML pages served by `tools/serve.py` (Python stdlib, no framework): it serves the static files and exposes tiny GET/POST endpoints over `student/` data. The agent generates activity content and opens the app; the app handles presentation, grading and saving. `/api/tts` uses the configured provider, with browser `speechSynthesis` as fallback. Text teaching stays in chat; learner-speaking activities use the saved voice-model route.

## Interaction modes: text vs. required voice

Every activity declares a mode; the learner is never asked to choose text versus voice:

| Mode | Meaning | Activities |
|---|---|---|
| `chat` | Interaction stays in text; app/TTS audio may supply listening material | SRS, reading, writing, grammar, quiz, precision listening |
| `voice-required` | The learner must speak to a voice model | conversation at every level, pronunciation production, fluency, story/live listening, weekly/exam speaking |

Setup stores `voice_channel` as `external` or `none`. For every `voice-required` step, the tutor emits one self-contained block with the finite `STEP_N → optional CORRECTION → FINISHED` controller, the A1–C1 language-support policy and a populated Lesson Pass JSON from `portable/voice-tutor.md`. The external chat returns Lesson Report JSON automatically or after a fixed post-call text request. No preconfigured project or prior chat memory is required. With no available route, the step is deferred and `speaking_debt` is logged — typing never completes speaking.

The daily session plan shows each step's mode up front (e.g. 🎙️ = you will speak). Level-up exams always include the spoken paper — you cannot reach B1+ without demonstrated speaking.

## Learner flow

1. **First use:** clone the repo, open your agent, say "let's start" → the agent reads `AGENTS.md` → `student/profile.md` doesn't exist → it runs `activities/placement-test.md` (adaptive interview + graded tasks using each level's criterial features) → creates the profile, seeds `known_words.txt` and the first cards.
2. **Daily session:** "today's session" → `activities/session.md` builds the menu from the configured time and the four strands. Example, 45 min: 10' SRS → 15' input (unit reading/listening) → 15' output (conversation or writing) → 5' focus on form over the error log → wrap-up: update progress, create cards from new errors.
   - **Days are NOT identical.** Short time budgets can't fit all four strands daily, so the session builder balances strands **across the week** (recent activities are logged in `progress.json`): conversation one day, reading the next, pronunciation another, fluency weekly. The plan always adapts to the learner's configured daily minutes.
   - **Continuity is automatic.** When the tutor opens an HTML app, `serve.py` writes an event file (`student/.event-<app>.json`) the moment the app posts its results; the tutor waits on that file (with a timeout) and resumes by commenting on the results — no need for the learner to say "I finished". Universal fallback in harnesses that can't wait: the learner says "done".
3. **Leveling up:** after finishing a level's units, `exam-simulator.md` builds a Cambridge-style exam; passing updates the active language's progress to the next level.

## The memory loop (what makes it "remember")

- Every activity ends by writing: new errors → `errors.md`; new vocab → `cards.json` (sentence-first contextual cloze, `docs/methodology.md` §3); mastered words → `known_words.txt`; session → `progress.json`.
- Every activity starts by reading: profile + recurring errors + current unit. Today's conversation attacks yesterday's mistakes, and generated texts respect the 95–98% known-word ratio.

## Build phases

| Phase | Contents | Outcome |
|---|---|---|
| **1. Core** | AGENTS.md, methodology.md, placement-test, session, srs.py + srs-review, conversation, English curriculum A1–A2, student.example, serve.py + core apps (flashcards, quiz, dashboard) | You can genuinely study with it |
| **2. Full course** | reading + reader.html, writing (CEFR rubrics), listening, grammar-lesson, fluency, English curriculum B1–B2, exam-simulator | Complete course through B2 |
| **3. Polish** | pronunciation, English curriculum C1, l1-notes, voice bridge, public README, license, GitHub repo | Open-source, usable by anyone; structure ready for more languages |

## Deliberate simplifications (and their ceilings)

- `ponytail:` FSRS with default weights and minimal formulas in stdlib; run the optimizer only if a user accumulates thousands of reviews.
- `ponytail:` five plain local HTML apps, no frontend framework and no database; flat JSON/markdown remains the source of truth.
