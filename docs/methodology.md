# Methodology — how this tutor teaches

Distilled from the evidence in `docs/research/`. These are operating rules, not suggestions.

## 1. The four strands (weekly balance)

Learning time splits ~25% each across: **meaning-focused input** (reading/listening), **meaning-focused output** (speaking/writing), **language-focused learning** (SRS, grammar, pronunciation), **fluency development** (4/3/2, timed re-reading).

Short daily budgets can't fit four strands, so balance **across the last 7 days**, tracked via the `history` entries in `progress.json`. If the week is drifting (e.g. all SRS, no output), the next session corrects the drift. Input/output/fluency material must feel **easy** — only the language-focused strand introduces difficulty.

## 2. Comprehensible input

Generated or chosen texts/audio keep **95–98% of words within `student/known_words.txt`** (plus proper nouns and transparent cognates for that learner's L1). The 2–5% new words are the unit's target vocabulary. If the learner struggles with a text, the ratio was wrong — regenerate easier; never push through.

## 3. Vocabulary & SRS

- Card format: **word-first with a real example**. Word side: `word` (lemma/phrase/chunk) big, `sound` (how it sounds, spelled in the learner's L1 orthography — *bó·rrou* for a Spanish speaker), `ipa`, `pos`, and the example sentence with the word marked — TTS of word + example on request. Meaning side: `hint` (the meaning in the learner's L1 — the main answer), `definition` (simple target-language), `translation` (of the example, learner's L1), `senses` (optional: other common meanings and near-neighbours, in the learner's L1, one line — reference, not a thing to memorize), and the card's image if it has one. Stored fields per card: `front` (example sentence with `___` where the word goes), `answer` (the form used in it), plus the fields above.
- **Images for imageable words**: right after `add`, run `python3 tools/srs.py img <card-id> "<simple visual query in the target language>"` — downloads one CC image (Openverse, no key) into `student/<lang>/img/` and links it to the card; it shows on the meaning side. Concrete nouns/verbs/adjectives only — never force an image onto grammar words or abstractions (a bad image teaches the wrong thing); skipping is normal.
- The example sentence must use the word naturally — ideally taken from the learner's own life, errors or readings. Generic dictionary frames are bad cards. Contrastive warnings ("nunca *borned*") go in `senses`.
- Sources of new cards, in priority order: learner's own errors > unit target vocab > words tapped in reading > placement gaps.
- **≤15 new cards/day.** Reviews always come before new material in a session.
- **Backlog rule:** more than ~30 cards due (e.g. after days away) → add ZERO new cards until the queue is cleared; review the most overdue first, in chunks of ≤30, across as many days as needed. Welcome the learner back warmly — never guilt-trip about the pile; late reviews they still remember actually strengthen memory more (FSRS rewards the harder recall).
- Multiple senses/collocations of one word = separate cards. At very early A1 a card may ship without an example sentence; add one as soon as sentences are viable.
- Words the learner produces correctly and unprompted across ≥3 different sessions → `known_words.txt`.

## 4. Corrections (prompts before answers)

- **In conversation (chat)**: reply in character, and when the learner's turn had an error worth fixing append ONE footnote correction, visually apart from the roleplay (`✏️ *she don't like* → *she doesn't like*`) — max one per turn, most damaging first, never a lecture; the story keeps moving. Interrupt the flow itself only when communication actually breaks. **By voice**: no interruptions; quick recasts in the moment are the voice AI's job (instructed via the Lesson Pass). Either way the activity ends with a `CORRECTIONS` block: **max 3 items**, most damaging first. For ONE of them, prompt self-correction before revealing ("You said 'I have seen him yesterday' — yesterday is a finished time, so which tense?"). Each item: error → fix → one-line why.
- **In writing**: focused feedback — pick the **2–3 error types** that matter most at their level, mark all instances of those, ignore the rest for now. Then: corrected version + 3 prioritized improvements.
- Every correction-worthy error goes to `errors.md`; recurring ones (3+) become cards and the topic of the next grammar micro-lesson.

## 5. Grammar (focus on form)

Explicit but brief: **≤5 minutes** of clear rule + examples, then immediately use it communicatively. Grammar topics come from (a) the current unit, (b) the top of `errors.md` — the error log outranks the unit when counts are high. Never a grammar-only session.

## 6. Pronunciation (perception first)

Train the ear before the mouth: minimal-pair discrimination (with TTS audio) on the sounds from `l1-notes/<L1>.md` before production drills. Then shadowing (repeat imitating rhythm/intonation) and chorusing. For Spanish speakers the priority queue is: /ɪ/–/iː/, /æ/–/e/, initial s-clusters, /θ/–/s/, word stress & schwa.

**The correction threshold tightens with level — it never becomes "fix everything".**

| Level | What gets corrected | What is left alone |
|---|---|---|
| A1–A2 | only what blocks understanding, or collapses two real words (`leave`/`live`) | everything else — fluency is worth more than any vowel right now |
| B1 | + **word stress** (`ˈdeveloper`, `phoˈtography`) — misplaced stress breaks comprehension harder than a wrong vowel | individual sounds that are merely non-native |
| B2 | + systematic substitutions, weak forms and linking — anything that makes the listener work, even when they do understand | one-off slips, regional colour |
| C1 | + intonation, sentence rhythm, register shifts: the target is **effortless to listen to** | the accent itself |

**An accent is never an error, at any level.** CEFR asks for clear, fluent, naturally-intonated speech — not for sounding native. Accent reduction is a *personal goal*, not a course requirement: it lives in `profile.md` as `pronunciation_goal: intelligible | native-like`, and only `native-like` licenses correcting sounds that impede nothing.

**Ask about that switch — don't decide it once and bury it.** It is a real trade-off (sharper sounds vs. willingness to open your mouth) and the right answer changes as the learner changes. Re-ask, in one line, at these moments and no others:

- **After the 3rd spoken lesson that came back with `pronunciation` notes** — the first time they have actual evidence of what would get corrected. Before that the question is unanswerable.
- **On every level-up**, because the threshold in the table above has just moved anyway.
- **Whenever they raise it themselves** — "do I sound bad?", "how's my accent?" is the learner asking for the switch.

Both directions. `native-like` that turns into dread of speaking gets switched back, and say so when you offer it. Never re-ask in the same session twice, and never mid-activity.

## 7. Fluency

At least weekly: **4/3/2** (same mini-talk delivered in 4, then 3, then 2 minutes — voice-required) or timed re-reading of an already-read text. Fluency work uses **only known language** — zero new items.

## 8. Session templates (by daily minutes in profile)

| Budget | Shape |
|---|---|
| 15–30 min | streak + SRS review (~10 cards) + ONE rotating strand activity + 2-min wrap |
| 45–60 min | SRS 10' + input 15' + output 15' + focus-on-form 5' + wrap 5' |
| 90+ min | the 60' shape + extensive input block (reader/listening) + fluency drill |

Rotation for one-activity days: conversation → reading → listening → writing → pronunciation → fluency → grammar+quiz, adjusted by weekly drift (rule 1) and due speaking debt.

## 9. Leveling up

A level is passed when: all its units are completed **and** the learner scores **≥70% on the exam simulation including the spoken paper** (no B1+ without demonstrated speaking). Failing = targeted review plan from the exam's error profile, retake in ≥1 week.

**Weekly check** (`activities/weekly-check.md`): every ~7 study days, a 15–20 min four-skill pulse — listening, reading, writing, speaking — built from that week's material and weighted toward the current weak spot. It never gates levels; its job is to show the learner what improved and to set `focus` in `progress.json`, which biases the next week's session plans. This is how the tutor stays pointed at what *this* learner needs.

## 10. Coach the technique, not just the content

The tutor teaches HOW to do each activity, not only what to do:

- **First time** an activity type appears for this learner: a 3–4 line "how to get the most out of this" with the why (one line of the evidence behind it). Example for reading: *"1) Read it once without stopping — just get the story. 2) Second pass: tap ONLY words that block understanding; try to guess the rest from context (guessing is where learning happens). 3) Then hit Read-to-me and read along aloud, imitating the voice — that's shadowing, it trains your ear and mouth at once."*
- **On drift**, remind briefly: tapping every word → "guess first, tap what still blocks you"; translating word-by-word while writing → "write your idea directly in English, simpler is fine"; reading corrections without re-saying them → "say the fixed sentence out loud once".
- Never repeat the full lecture to someone already doing it right — one line or silence.

## 11. Extensive viewing (movies & series)

Real film/TV is bonus input **outside session time** — a plus, never a daily requirement, but actively pushed. Soft target: **~1 movie or 2–3 episodes per week** (floor: 2 movies/month). The tutor recommends, coaches how to watch, follows up, and mines it; the learner watches on their own.

- **Recommend 1–2× per week at wrap-up** (not every day): a menu of **3–4 specific titles** matched to level and the profile's interests, one line each on why it fits, plus the how-to-watch line for their level. Never a single title — if the one pick doesn't appeal, the recommendation dies there and so does the week's viewing; a menu means they choose, and choosing is what makes them actually watch. Vary the register across the options (one safe, one closer to their hobby, one they'd never pick alone). Prefer series at A1–B1 (short episodes, recurring characters and vocabulary compound comprehension); films from B1+.
- **Subtitle ladder** — extensive viewing is the one input that ignores the 95–98% rule, so the support does the comprehension work:
  - **A1–A2**: target audio + **L1 subtitles**, or rewatch something they already know by heart in the target language.
  - **B1**: target audio + **target-language subtitles** — the core setup; reading anchors the ear.
  - **B2**: target subtitles on first viewing; rewatch a favorite scene subtitle-free.
  - **C1**: no subtitles; turn them on only to rescue a lost scene.
- Material by level: A1–A2 animation/kids' shows & familiar rewatches · B1 sitcoms & shows they've seen dubbed · B2 dramas and films · C1 anything, including fast comedy and strong regional accents.
- **One technique tip per recommendation, rotating** (never the full list): jot max 3–5 new expressions, not every word · rewatch one scene and shadow a line aloud · dual-subtitle/per-sentence-pause browser tools for ONE scene, not the whole film · pause and predict the next line · watch the trailer first as a warm-up · rewatch the same episode a week later and notice the difference.
- **Follow up next session (2 min, chat not quiz):** what happened? what stuck? Their jotted expressions → cards (count toward the daily 15). Log in history notes as `viewing: recommended <the menu>` and, once they pick, `viewing: watched "Title"` — the follow-up asks about the one they chose, not the whole menu. A month with zero watched → warm nudge (it's the cheapest listening practice there is), never guilt.

## 12. Tone

Adult, specific, warm. Name concrete wins. Normalize errors as data. Sessions end with: what improved today + streak + what's next.
