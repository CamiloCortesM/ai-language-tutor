# AI Language Tutor

<p align="center">
  <img src="assets/tutor-mascot.png" alt="AI Language Tutor mascot reading a book" width="240">
</p>

Turn any AI coding agent into a personal language tutor with memory — a full CEFR course from A1 to C1 that lives in a folder.

No accounts, no subscriptions, no servers. The **agent is the tutor** (it teaches, corrects, converses and examines you), **plain files are the memory** (your level, errors, vocabulary and streak persist between sessions), and **one small script is the clock** (FSRS, the modern spaced-repetition algorithm). Everything is built on evidence-based language pedagogy — see [`docs/methodology.md`](docs/methodology.md).

Works with **Claude Code, Cowork, Codex, Cursor, OpenCode, Gemini CLI** — anything that reads `AGENTS.md`. macOS, Windows and Linux.

## Features

- **Placement test** — a friendly ~15-minute adaptive chat that finds your real CEFR level and builds your profile. No preparation needed.
- **Daily sessions** — one word (`session`) plans your day: spaced review, comprehensible reading, conversation, writing, pronunciation… balanced across the week and fitted to the minutes you have.
- **Real curriculum** — 60 CEFR units for English (A1→C1): criterial grammar, vocabulary, functions and Cambridge-style level exams.
- **Spaced repetition** — word-first flashcards: the word, how it sounds and a real example on the front; the meaning in your language (plus a picture when it helps) on the back. Scheduled with FSRS, generated from *your* errors and readings.
- **Speaking that counts** — conversation, fluency drills and spoken exams use the current agent's integrated voice when available. An optional Lesson Pass bridge supports another voice AI when needed.
- **Browser apps** — flashcards, quizzes, assisted reader with read-along audio and a progress dashboard. Self-contained HTML, served locally.
- **Natural voices, free** — neural TTS via edge-tts, no key or account. Paid voices (OpenAI, ElevenLabs) optional, never required.
- **Any native language, any target** — the tutor explains in *your* language; English ships complete, and other target languages are generated in place on request.
- **Private by design** — everything runs and stays on your machine.

## Quick start

> Requirements: an AI coding agent + Python 3. Recommended once: `pip3 install edge-tts` (free neural voices).

1. Clone or download this repo.
2. Open your AI agent in the folder — no terminal needed: in the Claude desktop app, open the folder with **Cowork**.
3. Say **`let's start`** and take the placement test.

From then on, your daily class is one word: **`session`**. In Claude Code, Cursor, OpenCode and Gemini CLI you can also type `/start` and `/session`.

## How a session works

The tutor reads your memory, greets you with your streak and due cards, and runs a plan shaped to your daily minutes — for example: 10' flashcard review → 15' reading at 95–98% known words → 15' spoken roleplay → 5' grammar targeting your most repeated error. Every activity writes back what it learned about you: new errors become flashcards, mastered words unlock harder texts, and tomorrow's class starts where today's ended.

Speaking steps are enforced, not optional — you cannot pass B1 without a spoken exam. When your agent has integrated voice, turn it on and do the lesson there. If voice is off, the tutor reminds you before a speaking step; if it is unavailable or you prefer another AI, use the optional [voice bridge](portable/voice-tutor.md).

## Languages

- **Learn English today** — complete curriculum, from any native language: hints, translations and explanations are generated in yours.
- **Learn anything else** — say *"I speak Spanish and I want to learn French"*: the tutor generates the French curriculum in your copy, level by level, and teaches the same way. Generated curricula are marked for review — contribute yours back!
- **Several at once** — each language keeps its own deck, streak, level and errors in `student/<language>/`. Say *"switch to French"* and everything follows.

## Repo layout

```
AGENTS.md            the tutor's brain — identity, rules, memory protocol
docs/                methodology, architecture, and the research behind them
activities/          the 12 lesson types the tutor can run (plain markdown)
languages/english/   curriculum: 60 CEFR units + notes per native language
apps/                browser apps: flashcards, quiz, reader, dashboard
portable/            optional voice bridge for another voice AI
tools/               srs.py (FSRS) · serve.py (local API) · tts.py (voices)
student.example/     template for your data — your real student/ is gitignored
```

## Privacy & API keys

Your data never leaves your machine: profile, errors and progress live in `student/` (gitignored), and the only server is `localhost`. The default stack needs **zero API keys**. If you opt into a paid voice, pass the key only as an environment variable (`export OPENAI_API_KEY=...`) — never write keys into files in this folder and never paste them into the chat: the agent can read both. Keys are sent only to their provider over HTTPS and never written to disk.

## Contributing

The most valuable contributions, in order:

1. **A language you generated** — `languages/<target>/` from the tutor's generator, reviewed by you.
2. **L1 notes** — typical errors for your native language (`languages/english/l1-notes/<your-language>.md`).
3. **Curriculum review** — corrections to units by teachers or advanced learners.
4. **Windows/Linux testing** — the tooling is cross-platform by design; field reports welcome.

Keep the spirit: plain files, no frameworks, free by default, works in any agent.

## License

[MIT](LICENSE) — use it, fork it, translate it, build on it.
