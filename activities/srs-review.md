# Activity: SRS review

**Mode:** chat or app · **Duration:** ~10 min · **Always first in a session**

## App protocol (preferred when a browser is available)

Serve + open `flashcards.html` and wait on the event file per AGENTS.md §HTML apps. Grades apply server-side; when the event arrives, comment on the results (lapses especially) and continue.

## Chat protocol (no browser)

1. `python3 tools/srs.py due` → take up to ~12 cards (oldest due first).
2. Per card, show the contextual cloze only:

   > *Can I ___ your pen? I forgot mine.*
   > pista: *pedir prestado*

3. Learner supplies the missing word/chunk (`borrow`). Do not accept a synonym when this card trains a specific form or collocation.
4. Reveal: **borrow** · *bó·rrou* · /ˈbɒr.əʊ/ · verb; the completed sentence with **borrow** marked; simple definition; full L1 translation; other senses if present.
5. Ask for an honest self-grade — **1 Again · 2 Hard · 3 Good · 4 Easy** — with next-interval hints. Exact and immediate = Good/Easy; correct but slow or inflected wrongly = Hard; wrong/blank = Again. A different valid sense is still a miss for this card's sentence.
6. `python3 tools/srs.py grade <id> <n>` after each.
7. On request, TTS the completed sentence after reveal. Never play the answer before retrieval.

## After the run

- Summary: X/Y, which cards lapsed.
- Lapsed 3+ times → flag in `errors.md`; consider rewriting that card with a stronger context (bad cards exist).
- If due count was 0: say so, spend the time on new cards from the current unit instead (≤15/day cap).
