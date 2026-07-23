# Activity: Reading (comprehensible input)

**Mode:** chat (app `reader.html` when shipped) · **Duration:** 10–20 min

## Generate the text

- Topic: current unit's theme crossed with the learner's `interests` (profile). Length by level: A1 ~80–120 words · A2 ~150–200 · B1 ~250–350 · B2 ~400–500 · C1 ~500+ with real stylistic range.
- **The 95–98% rule is the whole method** (`docs/methodology.md` §2): almost every word from `student/known_words.txt` (+ proper nouns + transparent cognates for their L1); the 2–5% new words are the unit's target vocabulary, each appearing 2+ times in different sentences.
- Weave in the unit's grammar naturally. Vary genres across sessions: story, dialogue, email, news brief, review, forum post.

## Run it

**App mode (preferred with a browser):** write `student/reading-current.json` (format in AGENTS.md §HTML apps), open `reader.html`, wait on the event(s). The learner reads with tap-to-gloss words and can hit **▶ Read to me** — the browser voice reads paragraph by paragraph while the text highlights along (reading-while-listening).

**Coach the three-pass technique** (methodology §10 — teach it the first time, then one-line reminders):
1. Read once straight through, no stopping — just get the story.
2. Second pass: guess unknown words from context first; tap ONLY the ones that still block understanding.
3. **Read to me** + read along aloud, imitating the voice (shadowing) — ear and mouth in one pass.

**Chat mode:** present the text (title + level + ~minutes). Read-aloud options, learner's choice: with agent voice mode, read it yourself while they follow the text in chat; otherwise `python3 tools/tts.py say "<paragraph>"` paragraph by paragraph (cross-platform, best free voice available).

Rotate the listening arrangement across sessions — each trains something different:
1. **Read-along** (default): audio + text together — links sound to spelling, trains prosody.
2. **Listen first**: audio only, ask for the gist, then reveal the text and read.
3. **Read then listen**: silent read, questions, then audio pass at full speed.

Then, in any mode:
- Any word the learner asks about → simple target-language definition + L1 translation + one extra example → **cloze card** from the sentence where they found it (app does this automatically via the + button).
- 2–3 comprehension questions — one literal, one inferential, (B1+) one opinion answered in the target language.
- Optional 30-second oral summary (counts toward speaking; great for `voice: always`).

## Write-backs

Tapped words → cards (respect the 15/day cap; overflow queues for tomorrow). Target words they read smoothly and later reuse → candidates for `known_words.txt`. Comprehension failures → note in `errors.md` if grammar-caused. Log the step.
