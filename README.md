# AI Language Tutor

Turn any AI coding agent (Claude Code, Codex, Cursor…) into a personal language tutor with memory. CEFR-based curriculum from A1 to C1, spaced repetition, real speaking practice, and progress that persists between sessions — all in plain files, no accounts, no servers.

**Status: work in progress.** The English curriculum (A1→C1, 60 units) ships first — and it works **from any native language**: the tutor explains, hints and translates in yours. Want to learn a different language? Ask your tutor — it will offer to generate that curriculum for you in place (and you can contribute it back).

## Quick start

1. Clone (or download) this repo.
2. Open your AI agent in the folder — **no terminal needed**: in the Claude desktop app, open the folder with **Cowork**; or use Claude Code, Codex, Cursor, etc.
3. Say **"let's start"** — the tutor gives you a **placement test**: a friendly 15-minute chat (a few questions about you, then short tasks that adapt to how you do) that finds your real CEFR level and creates your profile. No studying, no preparation — just answer honestly. From then on, one word runs your daily class: **"session"**.

Want a language other than English? Just say so — *"I speak Spanish and I want to learn French"* — and the tutor sets it up: it generates the French curriculum right in your copy (level by level, marked as generated), creates your French profile, and teaches you exactly the same way.

## Learning more than one language

Yes — each language is fully independent: its own deck, streak, level, error log and progress, in its own folder (`student/english/`, `student/french/`…). Say **"switch to French"** and everything — sessions, flashcards, dashboard — follows. Your profile (name, native language, daily minutes) is shared; nothing else is.

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
.claude/ .cursor/ .opencode/ .gemini/   /start and /session shortcuts per agent
```

**Shortcuts:** in Claude Code, Cursor, OpenCode and Gemini CLI you can type **/start** and **/session**. In any other agent (Codex, Cowork, …) just say the words — **"let's start"** and **"session"** work everywhere, because `AGENTS.md` defines them.

## Privacy & API keys

Everything runs on your machine. Your profile, errors and progress live in `student/` (gitignored). No accounts, no telemetry, no server beyond `localhost`.

**API keys (all optional):** the default stack needs **zero keys** — free neural voices via edge-tts, free browser speech recognition. If you choose a paid voice (OpenAI/ElevenLabs), provide the key **only as an environment variable** in your shell profile (`export OPENAI_API_KEY=...`). Never write keys into any file inside this folder and never paste them into the chat — anything in the folder or the conversation can be read by the AI agent. The tools only ever send the key to its provider over HTTPS; it is never written to disk, cached, or committed.

## License

MIT — use it, fork it, translate it, build on it. See `LICENSE`.
