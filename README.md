# AI Language Tutor

Turn any AI coding agent (Claude Code, Codex, Cursor…) into a personal language tutor with memory. CEFR-based curriculum from A1 to C1, spaced repetition, real speaking practice, and progress that persists between sessions — all in plain files, no accounts, no servers.

**Status: work in progress.** English (from any native language) ships first.

## Quick start

1. Clone (or download) this repo.
2. Open your AI agent in the folder — **no terminal needed**: in the Claude desktop app, open the folder with **Cowork**; or use Claude Code, Codex, Cursor, etc.
3. Say **"let's start"** — you'll get a placement test and a profile. From then on, one word runs your daily class: **"session"**.

Requirements: any AI coding agent + Python 3. Works on macOS, Windows and Linux.

**Recommended — natural voices, free:** run `pip3 install edge-tts` once and every read-aloud — stories, flashcards, dictation — switches from the robotic system voice to free neural voices (no API key, no account). Audio is cached locally. Pick a voice with `TUTOR_TTS_VOICE` (e.g. `en-US-AriaNeural`). Paid alternatives (OpenAI, ElevenLabs) are supported but never required — everything in this project works on free tiers.

## How it works

- The **agent is the tutor** — it converses, corrects, explains, and examines you, following `AGENTS.md` and the evidence-based method in `docs/methodology.md`.
- **Files are the memory** — your level, streak, error log, known words and card deck live in `student/` (gitignored, yours).
- **One small script is the clock** — `tools/srs.py` schedules flashcard reviews with FSRS, the modern Anki algorithm.
- **Spoken lessons can run anywhere** — your agent's voice mode, the built-in browser call mode (`apps/talk.html`), or ChatGPT voice via a Custom GPT (`portable/chatgpt-voice-tutor.md`): your tutor hands it a Lesson Pass, the GPT runs the class by voice, and its Lesson Report syncs back into your memory.

See `docs/architecture.md` for the full design and `docs/research/` for the evidence behind it.

## Repo layout

```
AGENTS.md            the tutor's brain — identity, rules, memory protocol
docs/                methodology (the pedagogical rules) + architecture + research
activities/          the 11 lesson types the tutor can run (plain markdown)
languages/english/   curriculum: 60 CEFR units (A1→C1) + notes per native language
apps/                browser apps: flashcards, quiz, reader, talk (call mode), dashboard
portable/            run spoken lessons in ChatGPT voice via a Custom GPT
tools/               srs.py (FSRS scheduler) · serve.py (local API) · tts.py (neural voices)
student.example/     template for your data — your real student/ folder is never committed
.claude/commands/    /start and /session shortcuts for Claude Code users
```

In Claude Code you can type **/start** and **/session** instead of writing the words.

## Privacy

Everything runs on your machine. Your profile, errors and progress live in `student/` (gitignored). No accounts, no telemetry, no server beyond `localhost`.

## License

MIT — use it, fork it, translate it, build on it. See `LICENSE`.
