# Activity: SRS review

**Mode:** chat or app · **Duration:** ~10 min · **Always first in a session**

## App protocol (preferred when a browser is available)

Serve + open `flashcards.html` and wait on the event file per AGENTS.md §HTML apps. Grades apply server-side; when the event arrives, comment on the results (lapses especially) and continue.

## Chat protocol (no browser)

1. `python3 tools/srs.py due` → take up to ~12 cards (oldest due first).
2. Per card, show front + hint only:

   > **Can I ___ your pen? I forgot mine.**
   > *(pedir prestado)*

3. Learner answers. Reveal the full card: sentence with the answer marked, `word /ipa/ · pos`, definition, translation.
4. Ask for an honest self-grade — **1 Again · 2 Hard · 3 Good · 4 Easy** — with next-interval hints. A correct-but-slow answer is Hard, not Good. A synonym that fits is fine language but a miss for *this* card ("'use' works! The target was *borrow* — grade yourself on that").
5. `python3 tools/srs.py grade <id> <n>` after each.
6. With `voice: always` or on request: say the sentence aloud (TTS/voice mode) before showing it — listening + recall in one.

## After the run

- Summary: X/Y, which cards lapsed.
- Lapsed 3+ times → flag in `errors.md`; consider rewriting that card with a stronger context (bad cards exist).
- If due count was 0: say so, spend the time on new cards from the current unit instead (≤15/day cap).
