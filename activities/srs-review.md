# Activity: SRS review

**Mode:** chat or app · **Duration:** ~10 min · **Always first in a session**

## App protocol (preferred when a browser is available)

Serve + open `flashcards.html` and wait on the event file per AGENTS.md §HTML apps. Grades apply server-side; when the event arrives, comment on the results (lapses especially) and continue.

## Chat protocol (no browser)

1. `python3 tools/srs.py due` → take up to ~12 cards (oldest due first).
2. Per card, show the word side only:

   > **borrow** · *bó·rrou* · /ˈbɒr.əʊ/ · verb
   > *Can I **borrow** your pen? I forgot mine.*

3. Learner says what it means (L1 is fine) — better yet, meaning + a quick sentence of their own.
4. Reveal the other side: meaning in their L1, simple definition, translation of the example, other senses if the card has them.
5. Ask for an honest self-grade — **1 Again · 2 Hard · 3 Good · 4 Easy** — with next-interval hints. Instant and sure = Good/Easy; slow or fuzzy = Hard; wrong or blank = Again. Knowing a *different* sense than the card's is a miss for *this* card ("as = 'mientras' is real, but this card is as = 'como (rol)' — grade on that").
6. `python3 tools/srs.py grade <id> <n>` after each.
7. On request: TTS the word before the reveal (ear-check the pronunciation) or the example sentence after it.

## After the run

- Summary: X/Y, which cards lapsed.
- Lapsed 3+ times → flag in `errors.md`; consider rewriting that card with a stronger context (bad cards exist).
- If due count was 0: say so, spend the time on new cards from the current unit instead (≤15/day cap).
