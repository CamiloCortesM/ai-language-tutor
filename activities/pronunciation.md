# Activity: Pronunciation

**Mode:** voice-required for production (perception drills use fixed TTS) · **Duration:** 5–10 min

## Pick the target sound

Priority: (1) perception failures logged by `listening.md`, (2) the priority queue in `languages/<target>/l1-notes/<L1>.md`, (3) sounds you noticed in conversation. One target pair/feature per session.

## 1. Perception first (minimal pairs)

Train the ear before the mouth (`docs/methodology.md` §6):
1. Present the pair with 3–4 word pairs (*ship/sheep, chip/cheap, live/leave*) — explain the articulatory difference in one line each.
2. Drill: say ONE word of a pair (TTS or voice), learner says which they heard. 8–12 trials, **feedback after every trial**, varying words and order. Track the score.
3. <80% → same pair again next time; ≥90% two sessions running → next target.

## 2. Production second

- Use the saved `voice_channel` and `portable/voice-tutor.md`. Build a finite **production-only** plan before starting: exactly 3 word/pair repetitions, 2 short-sentence repetitions and, at B1+, 3 numbered passes of one shadowing chunk; every good-faith attempt completes its step. Set `closing: none` because feedback happens per trial. If voice is unavailable, keep any perception score but defer production and log `"speaking_debt": true`; never substitute typing.
- **Repeat-after-me** on the same pairs, then on short sentences packing the target sound ("Please sit in that seat").
- **Shadowing** (B1+): speak a 2–3 sentence chunk, learner repeats near-simultaneously imitating rhythm and intonation, 3 passes. With whisper/STT available, compare their transcription against the target and point at gross mismatches only — no phoneme-level scoring without a real scoring API.
- Word stress & schwa (huge for most L1s): mark the stressed syllable in this week's new vocab, exaggerate-then-normalize.

## Write-backs

Perception scores per pair → session log (the queue lives on trends). Persistently confused pairs → note in `student/<active>/errors.md`. Log whether production completed; otherwise log `speaking_debt`.
