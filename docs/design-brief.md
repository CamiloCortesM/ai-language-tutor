# Design brief — HTML apps (paste-ready prompt)

> Master prompt for designing/building the visual screens in `apps/`. Paste it into Claude (or any design-capable AI) as-is, or use it as the spec when building the apps directly. Keep this file as the single source of truth for visual decisions.

---

## The prompt

You are designing the visual layer of **an open-source AI language tutor**: a repo that turns any AI coding agent into a personal language tutor with memory. The agent handles lessons in chat and speaking through a voice model; five self-contained HTML apps handle visual activities. Design and build all five screens plus a shared theme, with strong visual coherence — they must feel like one product.

### Product personality

Warm, focused, encouraging — a beautiful study desk, not a casino. Think "modern paper": the calm of a well-made notebook with the energy of a great mobile app. Gamification is subtle (streak, progress), never noisy (no confetti storms, no leagues). The learner should feel smart, not marketed to.

### Design system (shared `apps/theme.css`, CSS custom properties)

- **Color:** light mode = warm paper background (#FAF7F2 family), near-black ink text; dark mode = deep warm charcoal, soft off-white text. ONE vibrant accent for primary actions and progress (suggested: emerald #10B981 family) plus a small semantic set: success green, error coral/red, warning amber. SRS grade buttons have a fixed scale: Again = coral, Hard = amber, Good = emerald, Easy = sky blue — identical across all apps.
- **Typography:** a friendly geometric display face for numbers/headlines (streak count, scores) and a highly readable text face for learning content; system-font fallback stack. Learning content (cards, reader text) is set LARGE — 20px+ — it is the hero of every screen. UI labels stay small and quiet.
- **Shape & depth:** generous border-radius (12–16px), soft layered shadows, cards on paper. No borders where spacing can do the job.
- **Motion:** fast and physical (150–250ms, ease-out). Card flips rotate in 3D; correct answers get one small springy check; progress bars fill smoothly. Motion always means something; nothing loops or bounces idly. Respect `prefers-reduced-motion`.
- **Shared chrome:** every app has the same slim top bar — app name on the left, streak flame + today's progress on the right — so switching apps feels like changing rooms, not products.

### Screens

**1. `dashboard.html` — home.** The first thing the learner sees. Hero row: streak (flame + big number), daily-goal ring, current level chip (A1…C1) with progress bar to next level. Below: vocabulary growth area chart (known words over time), a "due today" card count with CTA to flashcards, and a compact "your top 3 recurring errors" list. One primary CTA: **Start today's session**. Empty states matter: day 0 should look inviting, not blank.

**2. `flashcards.html` — SRS review.** One card centered, everything else recedes. Front: a complete sentence in large type with exactly one cloze blank, plus a small L1 meaning cue; no audio can reveal the answer yet. Tap/space to flip — 3D rotation reveals the word/chunk, pronunciation, the completed sentence with the answer highlighted, L1 meaning, simple definition, translation and optional image. Audio reads the completed sentence only after reveal. Four grade buttons (Again/Hard/Good/Easy) keep the fixed color scale and interval previews. Keyboard: space = flip, 1–4 = grade.

**3. `quiz.html` — written test.** One question at a time, progress dots on top. Question types: multiple choice (big tappable option cards), gap-fill (inline input in the sentence), sentence reorder (tappable word chips). Instant feedback per question: chosen option turns green/coral, one-line explanation appears below, then a Next button — never auto-advance on a wrong answer. Final screen: score ring, per-question review list (✓/✗ with corrections), "errors were added to your deck" note.

**4. `reader.html` — assisted reading.** The most typographic screen: the story set like a beautiful book page (comfortable measure, generous leading). New-for-this-learner words are softly highlighted; tapping one opens a small popover: definition, example sentence, [+ add to deck] which morphs into a checkmark. Per-paragraph speaker buttons for TTS read-along. Footer: reading progress and count of words collected this session.

**5. `dictation.html` — precision listening.** A compact stack of generated sentences, each with its own learner-controlled audio player and transcript folded behind “show text.” The learner writes in chat, then reveals the matching sentence to check it; no answer appears automatically.

### Technical constraints (hard)

- Each app is ONE self-contained HTML file (inline CSS/JS) that links only the shared `theme.css`. Vanilla JS, no frameworks, no build step, no external CDNs/fonts — must work fully offline.
- Data comes from tiny local endpoints (`/api/deck`, `/api/progress`, `/api/quiz`, `/api/text`, `/api/dictation`, `/api/tts`) served by a stdlib Python server; POST results back to matching endpoints. Design must degrade gracefully to demo/sample data when endpoints are absent (so the files also open standalone via file://).
- Audio uses `/api/tts` when configured and browser `speechSynthesis` as the local fallback.
- Mobile-first responsive: flawless from 360px phone to desktop; thumb-reachable primary actions on mobile.
- Accessibility: WCAG AA contrast in both themes, visible focus states, full keyboard operation (flashcards and quiz especially), aria-labels on icon buttons. Light + dark via `prefers-color-scheme`.

### Coherence checklist (verify before finishing)

Same tokens everywhere; same top bar everywhere; the four grade colors never change meaning; one accent color for all primary actions; same radius/shadow/motion values; a screenshot of any two apps side by side should read as one product.

---

## Notes

- The agent generates activity content (quiz JSON, graded texts, deck data) — apps only present and grade it. Keep content and presentation decoupled.
- All five apps ship; keep demo data so each remains inspectable without learner files.
