# AI Language Tutor

<p align="center">
  <img src="assets/tutor-mascot.png" alt="AI Language Tutor mascot reading a book" width="240">
</p>

Turn any AI coding agent into a personal language tutor with memory — a full CEFR course from A1 to C1 that lives in a folder.

Beyond your AI coding agent, the core needs no additional account, subscription or remote server. The **agent is the tutor** (it teaches, corrects, converses and examines you), **plain files are the memory** (your level, errors, vocabulary and streak persist between sessions), and **one small script is the clock** (FSRS, the modern spaced-repetition algorithm). Everything is built on evidence-based language pedagogy — see [`docs/methodology.md`](docs/methodology.md).

Works with **Claude Code, Cowork, Codex, Cursor, OpenCode, Gemini CLI** — anything that reads `AGENTS.md`. macOS, Windows and Linux.

## Features

- **Placement test** — a friendly ~15-minute adaptive chat that finds your real CEFR level and builds your profile. No preparation needed.
- **Daily sessions** — one word (`session`) plans your day: spaced review, comprehensible reading, conversation, writing, pronunciation… balanced across the week and fitted to the minutes you have.
- **Real curriculum** — 60 CEFR units for English (A1→C1): criterial grammar, vocabulary, functions and Cambridge-style level exams.
- **Spaced repetition** — sentence-first cloze cards: retrieve a word or chunk inside a real sentence, then reveal its pronunciation, completed context, meaning and optional picture. Scheduled with FSRS and generated from *your* errors and readings.
- **Speaking that counts** — normal lessons stay in text; conversation, fluency, pronunciation and spoken exams automatically use the voice route saved during setup. One finite controller supports separate Codex/Work voice tasks and external voice projects.
- **Browser apps** — flashcards, quizzes, assisted reader, replayable dictation and a progress dashboard. Self-contained HTML, served locally.
- **Natural voices, free** — neural TTS via the cloud-based edge-tts service, no key or account. Browser/OS voices work locally; OpenAI and ElevenLabs are optional.
- **Any native language, any target** — the tutor explains in *your* language; English ships complete, and other target languages are generated in place on request.
- **Local memory** — the deck and progress stay in local files. Cloud voice/TTS receives only the text or lesson context sent to it; optional Openverse image lookup receives the search phrase.

## Quick start

> Requirements: an AI coding agent + Python 3. Recommended once: `pip3 install edge-tts` (free neural voices).

1. Clone or download this repo.
2. Open your AI agent in the folder — no terminal needed: in the Claude desktop app, open the folder with **Cowork**.
3. Say **`let's start`** and take the placement test.

From then on, your daily class is one word: **`session`**. In Claude Code, Cursor, OpenCode and Gemini CLI you can also type `/start` and `/session`.

## How a session works

The tutor reads your memory, greets you with your streak and due cards, and runs a plan shaped to your daily minutes — for example: 10' flashcard review → 15' reading at 95–98% known words → 15' spoken roleplay → 5' grammar targeting your most repeated error. Every activity writes back what it learned about you: new errors become flashcards, mastered words unlock harder texts, and tomorrow's class starts where today's ended.

Speaking steps are enforced, not optional — you cannot pass B1 without a spoken exam. Setup asks once where voice is available and reuses that route automatically. If it is unavailable, the tutor defers the spoken step and tracks the debt; it never pretends typing was speaking. The finite [voice bridge](portable/voice-tutor.md) supports Codex/Work and external voice projects.

## Languages

- **Learn English today** — complete curriculum, from any native language: hints, translations and explanations are generated in yours.
- **Learn anything else** — say *"I speak Spanish and I want to learn French"*: the tutor generates the French curriculum in your copy, level by level, and teaches the same way. Generated curricula are marked for review — contribute yours back!
- **Several at once** — each language keeps its own deck, streak, level and errors in `student/<language>/`. Say *"switch to French"* and everything follows.

## Repo layout

```
AGENTS.md            the tutor's brain — identity, rules, memory protocol
docs/                methodology, architecture, and the research behind them
activities/          lesson procedures and the daily orchestrator (plain markdown)
languages/english/   curriculum: 60 CEFR units + notes per native language
apps/                browser apps: flashcards, quiz, reader, dictation, dashboard
portable/            optional voice bridge for another voice AI
tools/               srs.py (FSRS) · serve.py (local API) · tts.py (voices)
student.example/     template for your data — your real student/ is gitignored
```

## Privacy & API keys

Profile, errors and progress live in `student/` (gitignored), and the app server binds to `localhost`. The text-only stack and browser/OS TTS need **zero API keys and no cloud audio service**. Edge TTS is free but cloud-based: it receives the text to synthesize; OpenAI, ElevenLabs and voice models receive the text or lesson context sent to them. `srs.py img` sends only the visual search phrase to Openverse and downloads the chosen result. The rest of the course memory remains local. Pass API keys only as environment variables (`export OPENAI_API_KEY=...`) — never write them into this folder or paste them into chat.

## Contributing

The most valuable contributions, in order:

1. **A language you generated** — `languages/<target>/` from the tutor's generator, reviewed by you.
2. **L1 notes** — typical errors for your native language (`languages/english/l1-notes/<your-language>.md`).
3. **Curriculum review** — corrections to units by teachers or advanced learners.
4. **Windows/Linux testing** — the tooling is cross-platform by design; field reports welcome.

Keep the spirit: plain files, no frameworks, free by default, works in any agent.

## License

[MIT](LICENSE) — use it, fork it, translate it, build on it.
