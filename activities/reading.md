# Activity: Reading (comprehensible input)

**Mode:** chat (app `reader.html` when shipped) · **Duration:** 10–20 min

## Generate the text

- Topic: current unit's theme crossed with the learner's `interests` (profile). Length by level: A1 ~80–120 words · A2 ~150–200 · B1 ~250–350 · B2 ~400–500 · C1 ~500+ with real stylistic range.
- **The 95–98% rule is the whole method** (`docs/methodology.md` §2): almost every word from `student/<active>/known_words.txt` (+ proper nouns + transparent cognates for their L1); the 2–5% new words are the unit's target vocabulary, each appearing 2+ times in different sentences.
- Weave in the unit's grammar naturally. Vary genres across sessions: story, dialogue, email, news brief, review, forum post.

## Run it

**App mode (preferred with a browser):** write `student/reading-current.json` (format in AGENTS.md §HTML apps), open `reader.html`, wait on the event(s). The learner reads with tap-to-gloss words and can hit **▶ Read to me** — the browser voice reads paragraph by paragraph while the text highlights along (reading-while-listening). Every word is tappable: glossary words show their gloss; any other word offers **💬 Ask the tutor**, which fires an `askWord` event (word + the sentence it came from). **Answer asks as they arrive**: brief L1 gloss + why it's used that way in that sentence, then delete the event and keep waiting. Events also carry cumulative `added` objects (word + exact sentence + gloss) and `asks`, so the final event preserves the whole session — dedupe against what you already handled.

**Coach the three-pass technique** (methodology §10 — teach it the first time, then one-line reminders):
1. Read once straight through, no stopping — just get the story.
2. Second pass: guess unknown words from context first; tap ONLY the ones that still block understanding.
3. **Read to me** + follow the text while listening — connect sound, spelling and phrasing. Speaking practice remains a separate `voice-required` activity.

**Chat mode:** present the text (title + level + ~minutes). Read-aloud via `python3 tools/tts.py say "<paragraph>"` paragraph by paragraph (cross-platform, best free voice available).

Rotate the listening arrangement across sessions — each trains something different:
1. **Read-along** (default): audio + text together — links sound to spelling, trains prosody.
2. **Listen first**: audio only, ask for the gist, then reveal the text and read.
3. **Read then listen**: silent read, questions, then audio pass at full speed.

Then, in any mode:
- Any word the learner asks about → simple target-language definition + L1 translation → **contextual cloze card** using the exact sentence where they found it. The app's + button queues that sentence for the tutor; the tutor creates the validated card after the event arrives.
- 2–3 comprehension questions — one literal, one inferential, (B1+) one opinion answered in the target language.
- Optional 2-sentence written summary. Any assessed oral summary belongs in a separate `voice-required` step.

## Write-backs

Tapped words → cards (respect the 15/day cap; overflow queues for tomorrow). Target words they read smoothly and later reuse → candidates for `known_words.txt`. Comprehension failures → note in `errors.md` if grammar-caused. Log the step.
