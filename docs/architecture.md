# Architecture — AI Language Tutor (A1 → C1)

> Synthesis of the research in `docs/research/`. Status: proposal, pending approval before building.

## Design principles

1. **Portable / harness-agnostic.** Everything the tutor needs lives in markdown that any AI agent (Claude Code, Codex, Cursor, Gemini CLI…) can read. Entry point: `AGENTS.md` (a convention most agents already support); `CLAUDE.md` just redirects to it. "Skills" are plain markdown files in `activities/` — instructions, not proprietary code.
2. **The LLM is the tutor; files are the memory; scripts are the clock.** Code exists only where the LLM is a poor substitute: SRS scheduling (FSRS) and the streak. Everything else (generating texts, correcting, conversing, examining) is instructions.
3. **Multi-language by design — on both sides.** The method (`activities/`, `docs/methodology.md`) is language-agnostic. Everything specific to a **target** language lives under `languages/<target>/` (curriculum, vocab lists); English ships first, adding a language = adding a folder. The learner's **native** language (any L1) is just a profile field: curriculum files are target-language-only, and all L1-specific material — hints, translations, contrastive explanations — is generated at runtime for that learner. Optional `l1-notes/<L1>.md` files capture known pitfalls per language pair (Spanish ships first); when absent, the tutor uses its own contrastive knowledge.
4. **Multi-user.** Learner data lives in `student/` (gitignored). The repo ships `student.example/` as a template; the placement test fills it in on first use.
5. **Evidence-based** (see `docs/research/evidence-based-methods.md`): Nation's four strands ~25% each, comprehensible input at 95–98% known words, spaced retrieval practice, brief explicit grammar with *focus on form*, correction via *prompts* (self-correction), HVPT/minimal pairs for pronunciation.
6. **Voice is optional.** Where the agent has voice (or on macOS via `tools/voice.sh`: record → whisper.cpp → `say`), speaking activities use it; otherwise there is a text fallback.

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
│   ├── listening.md       # dictation, comprehension (TTS when voice available)
│   ├── writing.md         # writing task + CEFR-rubric correction
│   ├── pronunciation.md   # minimal pairs, shadowing, L1-specific trouble sounds
│   ├── grammar-lesson.md  # brief explicit lesson + communicative practice
│   ├── fluency.md         # 4/3/2 and automatization activities
│   └── exam-simulator.md  # Cambridge-style mock exam (gate to next level)
├── languages/
│   └── english/
│       ├── curriculum/
│       │   ├── overview.md    # A1→C1 map: hours, vocab targets, level-up criteria
│       │   ├── a1/            # ~10-12 units per level: unit-01.md, unit-02.md…
│       │   ├── a2/  b1/  b2/  c1/   # each unit: grammar + target vocab + functions
│       │   └── vocab/         #   + can-do statements + suggested activities
│       │       └── oxford-{a1..c1}.txt   # word lists per level (Oxford 3000/5000)
│       └── l1-notes/
│           └── spanish.md     # typical errors for Spanish speakers (phonology, grammar, false friends)
├── student/               # learner data (gitignored)
│   ├── profile.md         # shared: name, L1, languages studied, daily time, voice config
│   ├── active.txt         # which language is active ("switch to X" updates it)
│   └── <language>/        # one folder PER language studied — fully independent:
│       ├── progress.json  #   streak, level, current unit, history
│       ├── errors.md      #   recurring-error log (feeds lessons and cloze cards)
│       ├── known_words.txt #  known lemmas (drives the comprehensibility ratio)
│       └── cards.json     #   SRS deck (cloze cards with FSRS state)
├── student.example/       # commented template of all of the above
├── apps/                  # self-contained HTML apps (no frameworks, no build)
│   ├── flashcards.html    # SRS review UI: flip cards, Again/Hard/Good/Easy, browser TTS
│   ├── quiz.html          # written tests per unit: MCQ, gap-fill; self-grading
│   ├── dashboard.html     # streak, vocab growth, level progress, top errors
│   └── reader.html        # LingQ-style assisted reading: tap word → gloss → card
└── tools/
    ├── srs.py             # FSRS (minimal formulas) + due list + streak. Python stdlib.
    ├── serve.py           # ~30-line stdlib server: serves apps/ + reads/writes student/
    └── voice.sh           # optional macOS: record → whisper.cpp → say
```

## HTML apps

Visual activities live in `apps/` as self-contained HTML pages served by `tools/serve.py` (Python stdlib, no dependencies): it serves the static files and exposes tiny GET/POST endpoints so the apps can read and persist `student/` data (deck, quiz results, progress). The agent generates activity content (quiz JSON, graded texts) and opens the app; the app handles presentation, self-grading and saving. Browser `speechSynthesis` provides free TTS everywhere (audio on cards, listening in reader); browser speech recognition (Chrome) is a later option for in-app speaking drills. The chat keeps what HTML can't do: conversation, intelligent correction, lessons.

## Interaction modes: chat vs. voice ("call mode")

Every activity declares a `mode`, and the tutor enforces it — speaking a language cannot be learned by typing:

| Mode | Meaning | Activities |
|---|---|---|
| `chat` | Text is fine | srs-review, reading, writing, grammar-lesson, quiz |
| `voice-preferred` | Use voice if available; chat is an acceptable fallback | conversation at A1–A2, listening (TTS audio counts) |
| `voice-required` | The point IS speaking aloud. The tutor must run this in call/voice mode and says so explicitly | conversation from B1 up, pronunciation, fluency (4/3/2), the speaking paper of exam-simulator |

How voice happens depends on the harness, in order of preference: (1) the agent's native voice/call mode (e.g. Claude or ChatGPT mobile voice); (2) `tools/voice.sh` locally (record → whisper.cpp → agent → TTS); (3) no voice available → the tutor still forces production: "read your answer aloud 3 times, then type it" — and marks the step as done-in-fallback in `progress.json` so speaking debt is visible.

Learners also set a **voice preference** in their profile: `always` (the whole session runs in voice/call mode where the harness supports it, and chat activities get oral variants — oral quiz, dictation), `when_required` (default — voice only where the mode demands it), or `text_first` (text everywhere, speaking debt tracked).

The daily session plan always shows each step with its mode up front (e.g. 🎙️ = you will speak), so the learner knows before starting that today has a mandatory speaking block. Level-up exams always include the spoken paper — you cannot reach B1+ without demonstrated speaking.

## Learner flow

1. **First use:** clone the repo, open your agent, say "let's start" → the agent reads `AGENTS.md` → `student/profile.md` doesn't exist → it runs `activities/placement-test.md` (adaptive interview + graded tasks using each level's criterial features) → creates the profile, seeds `known_words.txt` and the first cards.
2. **Daily session:** "today's session" → `activities/session.md` builds the menu from the configured time and the four strands. Example, 45 min: 10' SRS → 15' input (unit reading/listening) → 15' output (conversation or writing) → 5' focus on form over the error log → wrap-up: update progress, create cloze cards from new errors.
   - **Days are NOT identical.** Short time budgets can't fit all four strands daily, so the session builder balances strands **across the week** (recent activities are logged in `progress.json`): conversation one day, reading the next, pronunciation another, fluency weekly. The plan always adapts to the learner's configured daily minutes.
   - **Continuity is automatic.** When the tutor opens an HTML app, `serve.py` writes an event file (`student/.event-<app>.json`) the moment the app posts its results; the tutor waits on that file (with a timeout) and resumes by commenting on the results — no need for the learner to say "I finished". Universal fallback in harnesses that can't wait: the learner says "done".
3. **Leveling up:** after finishing a level's units, `exam-simulator.md` builds a Cambridge-style exam; passing (~70%) promotes the profile to the next level.

## The memory loop (what makes it "remember")

- Every activity ends by writing: new errors → `errors.md`; new vocab → `cards.json` (as cloze in context); mastered words → `known_words.txt`; session → `progress.json`.
- Every activity starts by reading: profile + recurring errors + current unit. Today's conversation attacks yesterday's mistakes, and generated texts respect the 95–98% known-word ratio.

## Build phases

| Phase | Contents | Outcome |
|---|---|---|
| **1. Core** | AGENTS.md, methodology.md, placement-test, session, srs.py + srs-review, conversation, English curriculum A1–A2, student.example, serve.py + core apps (flashcards, quiz, dashboard) | You can genuinely study with it |
| **2. Full course** | reading + reader.html, writing (CEFR rubrics), listening, grammar-lesson, fluency, English curriculum B1–B2, exam-simulator | Complete course through B2 |
| **3. Polish** | pronunciation + voice.sh, English curriculum C1, l1-notes, public README, license, GitHub repo | Open-source, usable by anyone; structure ready for more languages |

## Deliberate simplifications (and their ceilings)

- `ponytail:` FSRS with default weights and minimal formulas in stdlib; run the optimizer only if a user accumulates thousands of reviews.
- `ponytail:` pronunciation scoring = whisper transcription vs. target text (catches gross errors); true phoneme-level scoring needs an external API (Azure Pronunciation Assessment) — documented as an optional extension.
- `ponytail:` no app, no web, no database: flat files. If a UI ever exists, the data is already JSON/markdown.
