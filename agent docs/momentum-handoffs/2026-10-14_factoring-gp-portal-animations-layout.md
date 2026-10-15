# Momentum handoff — Factoring GP portal: animations, step 2 stagger, FOIL bake

**Written:** 2026-10-14 (day-valid only)
**Repos touched:** `School Scrips/Factoring Guided Practice`, `School Scrips/student-portal` (embed CSS only), `Programs/` (handoff, session scorecard)
**Git:** nothing committed or pushed. No GitHub, no end-of-session, no Netlify.

---

## 1. Objective and phase

Chase is polishing **Factoring Guided Practice** embedded in the **student portal** (landscape,
Move box / Copy, `@factoring-guided/` alias). This session added **in-app WAAPI transitions**
(no Manim for these), **feedback after correct roots**, **bubble UI tightening** (boxes, +/- alignment,
paren spacing), and a **FOIL layout bake** from Copy JSON.

**Phase:** Implementation is in place and builds/tests green. Chase should **visually verify** on
portal dev — especially animations, step 2 stagger, FOIL arcs/labels after bake, and dwell-friendly
box sizes. Prior handoff items (per-step prompts, error float, Correct flash on bubble check) remain
valid unless superseded below.

---

## 2. Chase's desired feel (use his words)

- **Build-in (step 1):** Parentheses **drop in, spread, fill with boxes/x/signs, then = 0** — must
  **end on the same live DOM** as the interactive skeleton (no approximate-then-snap). First shot on
  build-in was **“perfect.”**
- **After correct bubble check:** Bubble **shrinks up** into the compact **step 1** KaTeX line, then
  **step 2** — **one factor at a time**: binomial **drops**, then **= 0** appears, then the **other
  factor** — **not both together**.
- **After correct roots:** **Correct!** ~2.2s, then next problem — same for **Use answer** on solve
  (no instant skip).
- **Bubble UI:** Number boxes **tighter** (not smaller font); **+/- boxes** aligned by moving the
  **whole sign box down**, not nudging the glyph. **Parens** should **not overlap** grey boxes —
  small gap between paren and inner row (user rejected tight negative margins that caused overlap).
- **FOIL:** Tuned arcs/boxes with Move box; latest Copy JSON baked (see §3).
- **Move box / Copy** still the tuning path; modals no backdrop dismiss (root AGENTS).

---

## 3. Accepted decisions (implemented)

### Portal embed layout bake (2026-10-14, Chase Copy — FOIL)

Owner: `Factoring Guided Practice/src/app/config/factoringPortalEmbedLayout.ts`

- `infoBlockRectPct`: 65.3, 1.7, 24.3, 33.2 (matches `doubleBubblePrompt`)
- `stepLinesPct`: step 1 — 11.5 / 8.8 / **13.2** / **numDyPct 1.8**; step 2 — 28.2 / 9.1 / **13.8**
- `bubbleProductsTuning`: `outerLabelDy` **-37**, `outerArcBowDy` **10** (was -43 / -7)
- Other keys unchanged from prior bake (equation, knob, correct/error floats, `infoBlockRectPctByStep`)

Session layout key still **`factoring-layout-placed-v22`** — local sessionStorage can override bake
until Move box off / cleared.

### Animations (WAAPI, portal + !layoutTuner)

| Hook / area | Behavior |
|---|---|
| `useParenBuildAnimation.ts` | On **Set up parentheses** mount only; ~1.6s build-in; `prefers-reduced-motion` skips |
| `useFactorSplitTransition.ts` | On **solveRoots** + `confirmedFactoredProduct`: shrink bubble → step 1 reveal → stagger step 2 |
| Step 2 stagger | `splitSetEqualZeroLine()` + `FactoringStepLineFloat` factor pairs; binomial drop then `= 0` fade per factor |
| `useFactoringCorrectFlash.ts` | Bubble check + **rootsConfirmed** (~2.2s); `advanceAfterRootsConfirmed` after delay |

### Roots / cheat

- `submitRoots` sets `rootsConfirmed`; no immediate `advanceToNextProblem`
- `applyCorrectAnswer` on solveRoots uses same path (no cheat skip)

### Step number centering

- `numDyPct` on `StepPartPct`; drag **number** adjusts X + numDy only (`useFactoringStepLineDrag.ts`)
- Step 1 seeded **numDyPct: 1.8**

### Bubble CSS (`factoring-double-bubble.css`)

- Fields: ~1.7rem tall, auto width, minimal horizontal padding; sign box **1.7rem**, `align-self: flex-end`
- Slot **gap: 0.14rem** between paren and inner (no negative paren margins)
- Skeleton step line: `padding-left: 0.45rem` for centering nudge

### Portal CSS (`student-portal/src/styles/factoring-guided-embed.css`)

- Step 2 factor pair + `= 0` text styling for stagger layout

---

## 4. Rejected / do not redo

- **Manim video** for build-in / split — must end on live UI (Chase approved in-app first).
- **Negative paren margins** that pull **)** into number boxes (overlap).
- **Instant advance** on correct roots or Use answer on solve without Correct flash.
- **Step 2 both factors dropping as one block** — replaced with staggered binomial then = 0.
- **Single global prompt rect** for all steps (prior handoff — still do not revert).

---

## 5. Current implementation state

### Factoring Guided Practice (dirty, uncommitted)

**New files:** `useParenBuildAnimation.ts`, `useFactorSplitTransition.ts`, prior session floats/flash hooks.

**Key touched:** `factoringPortalEmbedLayout.ts`, `FactoringPracticeView.tsx`, `FactoringStepLineFloat.tsx`,
`FactoringParenSkeletonFloat.tsx`, `FactoringDoubleBubbleStage.tsx`, `FactoringParenSkeleton.tsx`,
`practiceSession.ts` (`rootsConfirmed`, `advanceAfterRootsConfirmed`), `practiceRules.ts` (`splitSetEqualZeroLine`),
`factoring-double-bubble.css`, tests (`practiceSession`, `factoringPortalEmbedLayout`).

**Verify:** `npm run test` (29 pass), `npm run build` green. Agent did not open GUI.

### student-portal (dirty, uncommitted)

`factoring-guided-embed.css` — sign height, factor-pair / eq-zero styles.

### Verification Chase should run

1. Portal dev — problem 1, **Set up parentheses** → build-in once.
2. Bubble products → correct Check → shrink to step 1 → **first** `(…) ` down, **= 0**, **second** `(…)`, **= 0**, **2.)**
3. Correct roots → **Correct!** ~2.2s → next problem; same with **Use answer** on solve.
4. FOIL labels/arcs match baked tuning (toggle Move box off to confirm bake).
5. Parens clear of grey boxes; +/- boxes aligned with number row.

---

## 6. Open questions / constraints

- **`useFactoringPortalLayout.ts` ~620+ lines** — over 500; extract before large adds.
- **`factoring-guided-embed.css` ~793 lines** — over 700 cap; prefer FGA package CSS for new rules.
- **FOIL anchors** depend on bubble field sizes — if box CSS changes again, may need Move box re-tune.
- **GCF path** to solveRoots: no bubble split animation (only `confirmedFactoredProduct` path).
- **No Netlify deploy** unless explicit in message.
- **Context-heavy session** — fresh agent should read this file first, not replay full chat.

---

## 7. Read first (fresh agent)

| Need | Path |
|---|---|
| Root rules | `Programs/AGENTS.md` |
| Portal factoring row | `School Scrips/student-portal/AGENTS.md` |
| Layout bake | `School Scrips/Factoring Guided Practice/.../factoringPortalEmbedLayout.ts` |
| Build-in hook | `.../useParenBuildAnimation.ts` |
| Split / step 2 hook | `.../useFactorSplitTransition.ts` |
| Portal embed CSS | `School Scrips/student-portal/src/styles/factoring-guided-embed.css` |
| Bubble CSS | `.../factoring-double-bubble.css` |

Prior same-day handoffs (prompt/error/flash, older FOIL): `2026-10-14_factoring-gp-portal-prompt-error-layout.md`,
`2026-10-14_factoring-gp-portal-foil-layout.md` — partially superseded by this doc for animations + latest bake.

---

## 8. Exact next step

Chase **visual pass** on portal dev: confirm **build-in**, **split transition stagger**, **roots Correct flash**,
and **FOIL** after baked `outerLabelDy` / `outerArcBowDy`. If anything is off, Move box → Copy → paste into
`factoringPortalEmbedLayout.ts` (or `bubbleProductsTuning` / `stepLinesPct` keys). Optional: tune paren **gap**
(0.14rem) if still tight/loose. **Git sync only if Chase asks.**
