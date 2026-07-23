# Language-learning apps: key mechanics and how to replicate them in an AI tutor

> Project research base (2026-07). Grounds the design of activities and tools.

Recommended base architecture for everything: data lives in **markdown/JSON** (decks, learner profile, error log), scheduling logic in **one short Python script**, and the "intelligence" (generation, correction, conversation) in **agent skills** that read those files. The LLM is the tutor; scripts are the memory and the clock.

## 1. Anki + FSRS (spaced repetition)
**Key mechanic:** you don't review on a fixed calendar, but right before forgetting. FSRS models each card with 3 variables: **Difficulty** (D, 1-10), **Stability** (S = days until retention drops to 90%) and **Retrievability** (R = current probability of recall). After each review you self-grade (1 Again / 2 Hard / 3 Good / 4 Easy) and S and D are recalculated. FSRS-6 uses 21 trainable weights; it needs 20-30% fewer reviews than old SM-2 for the same retention.

**Minimal formulas to implement (FSRS-4.5/5, sufficient):**
- Forgetting curve: `R(t) = (1 + (19/81)·t/S)^(-0.5)` (t = days since review).
- Next interval for desired retention `r` (default 0.9): `I = (S·81/19)·(r^(-2) − 1)`. With r=0.9, I ≈ S.
- Initial S by grade: `S0 = w[grade-1]`, defaults ≈ `[0.4, 0.9, 2.3, 10.9]`.
- Initial D: `D0 = w4 − e^(w5·(grade−1)) + 1`, clamp 1-10.
- On success S grows depending on D (harder → grows less) and R (late review → grows more).

**Replicate simply:** don't reinvent the 21 weights. Use the **`py-fsrs`** library (pip) with default weights, or implement just the 2 formulas above. Cards in `cards.json` (`{front, back, S, D, last_review, due}`). A `review` flow lists what's due (`due <= today`), shows the card, reads your grade, updates S/D/due. That's a working SRS in ~60 lines. `ponytail:` start with fixed weights; run the optimizer only after thousands of reviews accumulate.

## 2. Duolingo — gamification
**What works (copy):** **streaks** — the #1 retention engine, leveraging loss aversion; a **small daily goal** (minimum XP) that reduces friction; **reminders**; short 3-5 min lessons (low activation barrier). **What's criticized (avoid):** leagues/leaderboards that reward time-in-app over real learning; decontextualized content and excessive translation; "gamification for its own sake" that produces Duolingo players, not speakers.

**Replicate simply:** a `progress.json` with `{streak, last_active_date, daily_goal, xp_today}`; the review script increments the streak if you studied today and breaks it if `today - last_active > 1 day`. Show it at the start of each session. Don't build leagues — focus the "reward" on real output produced (sentences said/written correctly), not minutes.

## 3. LingQ / Language Reactor — comprehensible input
**Key mechanic:** read/listen to real content with **instant translation on tapping any word**, marking words as "known/learning/new". The system colors the text by familiarity and gradually converts new into known. Language Reactor does the same over Netflix/YouTube subtitles (dual subtitles, per-sentence pause, saves words to an SRS).

**Replicate simply:** a `read-assisted` skill that takes a text (or generates one at the learner's level), shows it, and for any word the user asks about gives definition + in-context example + sends it to `cards.json`. Keep `known_words.txt` (known lemmas); the agent marks which words in the text are new for this learner and glosses only those. Key of the method: **95-98% known words** for input to be comprehensible — have the agent generate/choose texts that respect that ratio using `known_words.txt`.

## 4. Clozemaster — sentence mining with cloze
**Key mechanic:** learn vocabulary **inside real sentences**, not isolated words. Presents a sentence with one word blanked (cloze deletion) that you must complete; the sentence gives context, collocations and grammar for free. Combined with SRS.

**Replicate simply:** it's the best card format for the SRS in point 1. `make-cloze` skill: given a text or a target word, the agent generates natural sentences at the right level with the target word masked, saves `{sentence_with_blank, answer, full_sentence, translation}` to `cards.json`. Review shows the gapped sentence; correct → grade Good. Generate sentences from the learner's own input (articles, subtitles) so content stays relevant = real "sentence mining".

## 5. ELSA Speak — pronunciation assessment
**Key mechanic:** **phoneme-level** assessment, not word-level. Compares your audio against native pronunciation models and gives color-coded feedback (green/yellow/red) per sound, plus prosody (intonation, lexical stress, fluency). It points at exactly which sound you missed, not a global score.

**Replicate simply (the hardest part without dedicated infra):** the agent can't hear audio directly, so the pipeline is: record → **STT with word timestamps** (whisper.cpp or API) → compare transcription against the target text. True phoneme level requires a pronunciation-scoring model (e.g. Azure Speech "pronunciation assessment" API, which does give per-phoneme/word scores). **Honest lazy version:** use Azure Pronunciation Assessment or `wav2vec2` for the phonetic score; the agent interprets the score JSON and gives actionable advice ("your /θ/ in 'think' comes out as /s/ — put your tongue between your teeth"). Without a scoring API, limit to: does the whisper transcription match what you meant to say? (catches gross errors, not nuances).

## 6. italki / Cambly + AI tutors (Langua, TalkPal, Univerbal)
**What the human tutor brings:** real conversation, contextual correction, low/graduated social pressure, accountability. **How AI tutors replicate it:** an LLM that holds a voice conversation on any topic, adapts to level, and gives instant feedback. Langua = polished conversation; TalkPal = free-form voice/text chat; Univerbal = practical scenarios (ordering food, travel, business) with adaptive feedback. A 2025 study reports +75% speaking-score gains in 8 weeks with these apps. Their real advantage vs. humans: 24/7 availability, zero embarrassment, unlimited repetition.

**Replicate simply:** here the agent already IS the product. `conversation` skill with a fixed role (barista, interviewer), speaks only in the target language at the learner's CEFR level, keeps the conversation flowing, and ends with a **CORRECTIONS** block: errors + one-line fixes. Reads level and interests from the learner profile.

## 7. LLM-tutor design patterns (what actually works)
- **Roleplay + separate corrections:** the AI stays in character/immersion, and adds a `CORRECTIONS` section at the end of the turn with errors and a one-line explanation (doesn't break flow). Dedicated skill.
- **Generated graded readers:** "write a 200-word story at B1 using these 10 target words" → tailored comprehensible input. Reuses `known_words.txt` for the comprehensibility ratio.
- **Writing correction with a CEFR rubric:** the learner writes; the agent scores against CEFR criteria (grammatical range, coherence, vocabulary, accuracy) and returns a corrected version + 3 prioritized improvements. `correct-writing` skill with the rubric in markdown.
- **Exam simulation:** the agent acts as a Cambridge/IELTS examiner (speaking by parts, writing task with estimated band). Prompt carries the exam format.
- **Key to all of them:** the more concrete the context (CEFR level, profession, goal) in the profile, the more useful the output. Persist recurring errors in `errors.md` so the agent attacks systematic failures and generates cloze cards from them → closes the loop with the SRS.

## 8. Homemade voice (TTS/STT) on macOS/CLI
- **TTS (fast, offline, free):** macOS native `say` command. `say -v "?"` lists voices. Better offline quality: **Piper TTS**. APIs for premium voice: OpenAI TTS, ElevenLabs.
- **STT (offline):** **whisper.cpp** — 3 commands to build on Apple Silicon, runs 99 languages locally, free, with word timestamps (useful for pronunciation). API alternative: OpenAI Whisper API, Deepgram.
- **Voice-conversation pipeline in CLI:** record audio (`sox`/`ffmpeg`) → whisper.cpp transcribes → text to the agent (`conversation` skill) → response → `say` or Piper speaks it. All orchestrable in a ~30-line bash script.

---
**Minimum viable loop tying it all together:** profile (level) + `cards.json` (SRS with cloze) + `errors.md`. Session: (1) show streak, (2) review due cards with FSRS, (3) 5-min conversation, (4) the agent extracts new errors → generates cloze cards → adds them to the SRS. Start with SRS+cloze+conversation (text); add voice and exams later.

**Sources:** [FSRS/awesome-fsrs wiki](https://github.com/open-spaced-repetition/awesome-fsrs/wiki/ABC-of-FSRS) · [Domenic on FSRS](https://domenic.me/fsrs/) · [Talkio: best AI speaking apps 2026](https://www.talkio.ai/blog/best-ai-language-speaking-practice-apps-in-2026) · [Univerbal: AI language learning](https://blog.univerbal.app/ai-language-learning) · [ELSA Score explained](https://medium.com/@elsaspeak/discover-your-elsa-score-an-ai-powered-visualization-of-your-english-speaking-proficiency-in-369f46dba6bc) · [luisalima/local-whisper (whisper.cpp macOS)](https://github.com/luisalima/local-whisper) · [Borderset: Claude/ChatGPT prompts for English](https://www.borderset.com/blogs/posts/claude-and-chatgpt-prompts-for-learning-english)
