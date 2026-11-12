# Momentum handoff — Guided Practice as Homework slide (VP stop 18)

**Written:** 2026-11-11  
**Continue in:** fresh task (any tool / model)

> AACU Day 1 panels handoff from earlier today stays at
> `agent docs/momentum-handoffs/2026-11-11_aacu-day1-extract-panels.md` if that thread resumes.
> This slot is now the **gj-homework deck** continuation.

---

## Objective and current phase

Chase is polishing the **AI presentations** VP track slide **Guided Practice as Homework**
(`gj-homework`, stop **`s=18`**): left column builds beside a looping 11.2 homework demo video.

Phase: **slide content and layout are in place.** Video is human-UI typed/selected (not
auto-fill), plays at **4x**. Build sequence is bullets → most-missed skills chart → survey
percents → quotes. Chart text was just bumped larger. Chase has not asked for further edits
after the font bump; next agent should wait for his reaction or a concrete next ask.

---

## Chase's desired feel

- Demo must look like a real student: **typing and selecting**, not `adminGiveAnswer` flashes.
- Video stays on the **right**; left column swaps builds. He talks while the clip loops.
- Explain the assignment first (bullets), then show **struggle data MyLab cannot show**
  (most-missed guided skills), then survey numbers, then quotes.
- Chart labels must read from presentation distance. Compact chart text was rejected.
- No surprise GUIs. Presentation links are `http://127.0.0.1:8765/...` only.

Talk framing he wants for the chart: he captured first-try miss data so he can see where
students struggled most, something he could not do on MyLab Math.

---

## Accepted decisions

- **Open link:** `http://127.0.0.1:8765/ai-presentations/v2-stage.html#t=vp&s=18&b=0`
  Chart build: `#t=vp&s=18&b=2`. `#s=` is the **track stop**, not `DECK.pages` index.
- **Split:** `split: [52, 48]` (text / media). CSS must use `Nfr` values for `--text-fr` /
  `--media-fr` (unitless broke the grid and put video under the text).
- **Video:** `site/media/gj-homework-demo.mp4`, `rate: 4`, `autoplay`, `nochip`. ~110s source.
- **Build 1 — points** (`only: true`, `textcol: true`), four bullets only:
  1. Built to replace MyLab Math for 11.2.
  2. Six problems; 1–2 fully guided; 70% first-try correct earns full credit.
  3. Problem 3 choice: guided path or MyLab-style right/wrong.
  4. Of 14 finishers, **9 chose right or wrong**, **5 chose guided**.
  Dropped: problems 4–6 "enter the answer" note, and any fifth bullet.
- **Build 2 — bars** (`only: true`, `textcol: true`): title "Most missed guided skills",
  `max: 13`, note "First-try misses on guided problems." Data from Teacher Console screenshot:
  Replacement math 13, Target cell 7, Transform type 7, Solution 6, Scaling notation 5,
  Replacement notation 3, Matrix entry 3, Solution type 3, Scaling math 1.
- **Build 3 — stats** (survey %): 79% preferred guided · 71% easy to use · 86% confident.
  Vertical stack in textcol (large values, not bars).
- **Builds 4+ — quotes** (unchanged student survey lines).
- **`only: true` + points:** engine shares one build so bullets appear together (not staggered).
- **Hidden textcol builds** collapse height so the video does not ride down beside empty space
  (`.textcol > .blk[data-build]:not(.is-in)` height 0).
- **Typography:** `.textcol .chart` is **`1.15em`** (was 0.92em). Documented in
  `AI presentations/AGENTS.md` § Stage typography. Do not shrink under 1.15em to fit rows.

**Problem 3 fact check:** in-app Teacher Console choice is 9 solution_only / 5 guided.
Survey "preferred guided" (11/14-ish → 79%) is a **different** question. Do not merge them.

---

## Rejected directions

- Auto-fill / `adminGiveAnswer`-only recording (looked fake).
- Video caption on the homework clip.
- Survey bars or tiny horizontal %; he wanted large vertical percentages.
- Putting stats beside or under the video in a broken grid (unitless `fr` bug).
- Keeping a fifth bullet about problems 4–6.
- Treating survey preference as the Problem 3 choice count (9 vs 5 is correct for P3).
- Shrinking left-column chart text below 1.15em for density.

---

## Current implementation state

**AI presentations (uncommitted, mixed with parallel AACU/other work):**

- `site/shared/gj-evidence.js` — `gj-homework` block as above (`rate: 4`, builds 1–9).
- `site/v2-stage.html` — textcol chart `1.15em`, collapse rules, stats sizing, split `fr`.
- `site/shared/engine.js` — `textcol: true` keeps charts/stats in the left column; `together||only`
  for points build sharing.
- `site/shared/notes.js` — gj-homework speaker notes match the build order and talk point.
- `site/media/gj-homework-demo.mp4` — human-UI recording.
- `AI presentations/AGENTS.md` — Stage typography section added.
- Many unrelated dirty files (AACU review HTML, colleges, etc.). **Do not** fold those into
  this task's commits unless Chase asks.

**student-portal (uncommitted, from recording work):**

- `?record-gp=1` mount, `GuidedPracticeRecordView`, `scripts/record-gp-homework.mjs`,
  matrix drive hints / cell attrs, Playwright + `npm run record:gp-homework`.
- Re-record only if Chase wants a different pacing or problem.

**Verified this chat:** chart at build 2; last bullet removed; font bump applied. No browser
launch after the font change (Chase opens the stage himself). No commit/push.

---

## Open questions and constraints

- Whether 1.15em chart text is enough after he looks, or one more bump.
- Whether any chart rows should be dropped if nine rows still feel tight at the new size.
- Netlify deploy is **never** unless he says so in the same message.
- Never open the deck or portal GUI without asking first.
- `content.js` was already near extract line; GJ evidence lives in `gj-evidence.js` on purpose.

---

## Exact next step

Read `AI presentations/AGENTS.md` (voice + Stage typography), then open
`site/shared/gj-evidence.js` `gj-homework` and wait for Chase's reaction to
`#t=vp&s=18&b=2` (chart size / talk fit). Do not re-record or reshuffle builds unless he asks.

**Read first:** `AI presentations/AGENTS.md` · `site/shared/gj-evidence.js` · Stage CSS around
`.textcol .chart` in `site/v2-stage.html`.
