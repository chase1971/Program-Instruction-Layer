# Momentum handoff — VP deck: Campus Readiness finished, AI in the Classroom started

**Written:** 2026-11-13  
**App / area:** `AI presentations` (VP stage track)  
**Phase:** Campus Readiness has 8 slides. New "AI in the Classroom" section has 2 example slides. More classroom examples next.

---

## Objective and current phase

Chase is building the VP of Instruction presentation after the AAC&U conference. Goal: convince the VP to expand Lone Star's AI work by showing how much thought and work other institutions put in, and cool class examples.

Track order now (VP stop index): `campus-readiness` 23 → `campus-maturity` 24 → `campus-uri` 25 → `campus-three-pathways` 26 → `campus-networked` 27 → `campus-14day` 28 → `campus-aligning-values` 29 → `campus-coherence` 30 → `classroom-examples` (divider) 31 → `class-barking-tree` 32 → `class-misuse-literacy` 33 → `ai-frameworks` 34 → `fw-*` (TAKE AI.M, A.S.K.E.D., Five Pillars, Cognitive Pyramid, Flipping, Teaching with AI, Six Moves) → `future-ideas`. Recompute indices from `tracks` stops after edits; never guess `s=`.

Each slide has: overview (stage), long detail page behind the top up arrow, talk notes in `notes.js`, and a medium draft in `panel-summary-trims.js`.

## Chase's desired feel (critical)

- **Overview bullets read like Chase speaking out loud.** One or two complete sentences. No lead-in labels ("Challenge.", "Retriever:"), no colons, no fragments, no unexplained names (say what a tool is the first time). Short is fine; he talks over the slide. Rule now lives in `AI presentations/AGENTS.md` § "Overview bullets read like Chase speaking out loud". Exemplars: `class-barking-tree`, `campus-uri`, `campus-three-pathways`.
- Detail page keeps the full long write-up (also in sentences, no labels). Notes hold the real talk track.
- **Classroom examples point:** students using AI to do things they likely could not do without it, across fields of study. Separate from the classroom frameworks section.
- Campus Readiness point: how much thought and work campuses put in (challenge, steps, what they put in place, results). Doc: `docs/campus-readiness-story.md`.
- He cares about what the transcript really says. Check transcripts before asserting; say plainly when a source is thin (e.g. the Boise "small group out in front terrified the rest" line is one sentence, not expanded).
- Slide text is his voice. His own interpretation goes in notes, never attributed to the speakers.

## Accepted decisions

| Decision | Why |
|---|---|
| Brazelton (NAU) digital maturity slide is first in Campus Readiness | Shows the 5-point scale and the split: 99 of 100 R1s at level 3 or 4, baccalaureate and associate's 57 and 50 at 0 or 1 |
| Boise "weaknesses" bullet kept, using the speaker's wording | He likes it: shows how fast faculty get out of sync, supports his argument for faster training |
| Classroom section transition title is just "AI in the Classroom" | No colon |
| Classroom slides use dimmed campus photo backgrounds (`page.bg`) | He wanted the college-image look; overlay darkened to about .88-.92 deep navy because it was hard to read |
| Texas Tech overview = 4 sentence-style bullets | He talks over it |
| Misuse to Literacy (Lyon College): claim is "unexplained and unverifiable," not "wrong" | Transcript: bare answer and IRS-grounded answer both gave 15% and $3,750; only the reasoning differed |
| Socratic AI Tutors already done | It is the Five Pillars slide (Harford nursing); do not redo |

## Rejected directions / do not rediscover

- Label openers and colon fragments on overview bullets (he finds them weird).
- "Still live" as a label. The Boise weaknesses bullet is a plain sentence instead.
- Describing the first Lyon answer as wrong, or attributing "classes drift out of sync" to Boise State.
- Putting SIAC on the VP track; Netlify deploys; launching the stage or any GUI without asking; em dashes.

## Current implementation state

**Repos:** `AI presentations` (primary), `Programs/` root (handoff, scorecard). **Nothing committed or pushed.**

**Key files (all under `AI presentations/site/`):**
- `shared/content-classroom.js` (new): classroom divider, Texas Tech, Lyon College + detail pages; preloads `bg` photos
- `shared/content-campus.js`: 8 campus slides + details (about 272 lines)
- `shared/content.js`: VP stops; sections now include `ref-campus` and `ref-classroom`
- `shared/notes.js`, `shared/panel-summary-trims.js`: notes and medium trim drafts for every new slide
- `v2-stage.html`: new page-level `page.bg` support (`.slide-bg` + dark overlay). Script tag for `content-classroom.js` added to all six stage/notes HTML files.
- Background photos reuse `media/campus-1..9.jpg` (generic Unsplash). Divider uses `campus-6`, Texas Tech `campus-7`, Lyon `campus-8`.

**Verified:** `node --check` on all edited JS, headless stop-order and detail-page checks. **Not looked at on the stage** (no GUI launched); Chase opens it himself. The darker overlay has not been seen yet.

## Open questions and constraints

- Chase said he will return to the older Campus Readiness slides later: some detail pages still have label openers ("Structure:", "Design rule:", "Poll results to borrow:") and some overview bullets are semicolon-heavy. Not done.
- Campus Readiness slides have no `bg` photo; he was only asked about classroom ones. Offered, not answered.
- Real Texas Tech or Lyon photos not sourced (licensing). Reuse of generic campus photos is the current state.
- Mentioned but unconfirmed with Chase: the Brazelton "57 and 50" figures have an unclear denominator in the transcript.
- `content.js` ~586 lines, watch the cap; keep new slides in satellite files.

## Exact next step

Pick the next classroom example from the in-class bucket (Chase chooses). Candidates he was shown: Real Conversations (AI interview and stakeholder simulations), Closing the Gap Between Classroom and Career, Players to Designers (students building AI-assisted sustainability games), Student AI Partners as Co-Designers, The Bias They Didn't Notice, Creativity is a Choice, Pixels to Parameters. Ask which one if unclear. Build it in `content-classroom.js` the same way as `class-barking-tree`: spoken-sentence overview, detail page, notes, medium trim, VP stop after `class-misuse-literacy` and before `ai-frameworks`, `bg` campus photo.

**Read first:** `AI presentations/AGENTS.md` (the spoken-bullets section and Everything-on-screen-is-Chase's-voice) → `site/shared/content-classroom.js` → matching `notes.js` keys. Source transcripts are in `C:\Users\chase\My Drive\AACU\unwatched\` (docx for watched sessions in `C:\Users\chase\My Drive\AACU\`).

---

## Handy links (local)

- Classroom divider: `http://127.0.0.1:8765/ai-presentations/v2-stage.html#t=vp&s=31&b=0`
- Texas Tech: `...#t=vp&s=32&b=0` · Lyon College: `...#t=vp&s=33&b=0`
- Campus Readiness divider: `...#t=vp&s=23&b=0`
- Summary trim: `http://127.0.0.1:8765/ai-presentations/aacu-summary-trim.html`
