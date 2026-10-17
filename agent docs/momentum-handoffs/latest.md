# Momentum handoff — Factoring GP portal double-bubble control grid

**Written:** 2026-10-16 (day-valid only)
**Repos touched:** `School Scrips/Factoring Guided Practice`, `School Scrips/student-portal`, `Programs/` (agent docs, `scripts/serve-programs-docs.js`)
**Git:** nothing committed or pushed from this thread. No GitHub, no end-of-session, no Netlify deploy.

---

## 1. Objective and phase

Chase is polishing the **student-portal embed** of **Factoring Guided Practice** (double-bubble /
FOIL step, GCF path, Move box layout tuner with `?factoring-layout=1`).

**Phase now:** Double-bubble **action buttons** (Swap last terms, Pick new first terms, Clear, Pick
new last terms) were merged into a **single 2×2 grid** with equal cells. Sizing/padding was wrong
(tiny then bloated); last turn **restored committed compact styling** from portal CSS. Chase has
**not yet confirmed** the post-fix look in the portal after that CSS change.

Earlier in the same uncommitted batch (same repos): GCF keeps step 1 when step 2 bubble shows;
inner quadratic |c| ≤ 60 after GCF; red Clear + pick-new-first keeps last terms/signs; step number
“2.)” alignment; layout auto-sync to `agent docs/scratch/factoring-guided-layout-latest.json`;
problem-1 numeric-GCF trinomial priority.

---

## 2. Chase's desired feel (his words / corrections)

- Four bubble buttons should read as **one packaged 2×2 grid**, **same size**, **lined up** — not
  four floats that look mismatched.
- **Clear** should match the other buttons (not a tiny red pill).
- Size should match what **Pick new … terms** was before (**9.5rem** column width) — not invented
  percentages that squash labels.
- **Thin, minimal padding** — do **not** add tall cells (he called out extra padding explicitly).
- **“Pick new first terms” on one line** (no wrapped/overlapping text).
- **Do not guess styling** — use what was already in the tree (`factoring-gcf-menu-btn--bubble-action-compact` in `student-portal/src/styles/factoring-guided-embed.css`, last committed spec).
- Layout tuning: prefers **auto layout file for agents** over Copy/paste when docs server runs.
- **Do not launch GUI** without asking (dwell/focus). Handoff = statement of what to run, not prompts.

---

## 3. Accepted decisions

- **One layout rect:** `bubbleControlsGridRectPct` in `factoringPortalEmbedLayout.ts`; Move box
  moves/resizes the **whole grid** via `useFloatingRectTuner` (not four `useFactoringBubbleKnobDrag`
  hooks). Placed layout key **`factoring-layout-placed-v36`**.
- **Student view positioning:** `FactoringBubbleControlsFloat` uses rect **x/y only**; width comes
  from CSS `calc(2 * 9.5rem + 0.28rem)` so cells stay 9.5rem. **Move box on** still applies full
  rect % for resize outline.
- **Baked grid default:** `{ xPct: 49.2, yPct: 53.5, wPct: 35.5, hPct: 28.5 }` (envelops legacy
  knob anchor points). Legacy `bubbleKnobPct` / `bubbleNewFirstPct` / etc. remain deprecated in config.
- **Grid UI:** `FactoringBubbleKnob` `gridFour` order: Swap | Pick new first / Clear | Pick new last.
- **Engine:** `clearDoubleBubble` (full reset); `resetFirstNumbers` keeps constants + signs, returns
  to coeffs then `bubbleProducts` when constants already filled.
- **Export/copy layout:** `formatFactoringLayoutForAgent` exports `bubbleControlsGridRectPct` only
  (four point keys removed). Diff/sync in `src/app/services/factoringLayoutPlacedDiff.ts`.
- **Tests:** `npm test` in Factoring GP — **76 passed** after grid + sizing work (last run this session).

---

## 4. Rejected directions

- **17.5% × 17.5% grid rect** — crushed buttons; caused overlapping label text.
- **min-height 2.75rem + height: 100%** on grid cells — “made up” fat buttons; Chase rejected.
- **`bubble-clear-match` / `--full-width-btn` per-float hacks** removed when grid landed; do not
  reintroduce parallel sizing mechanisms.
- Reverting to **four independent Move box knobs** (replaced by one grid tuner).

---

## 5. Implementation state / verification

### Bubble grid (most recent edits)

| Area | Files |
|---|---|
| Grid component | `FactoringBubbleControlsFloat.tsx`, `FactoringBubbleKnob.tsx`, `FactoringDoubleBubbleStage.tsx`, `FactoringPracticeView.tsx` |
| Layout hook | `useFactoringPortalLayout.ts` (`bubbleControlsGrid`, v36 storage) |
| Baked constants | `factoringPortalEmbedLayout.ts` |
| Portal CSS | `student-portal/src/styles/factoring-guided-embed.css` — grid + **restore compact**: `min-height: 1.35rem`, `padding: 0.1rem 0.4rem`, `font-size: 0.6875rem`, `white-space: nowrap` on `.factoring-bubble-controls-grid .factoring-gcf-menu-btn` |
| App CSS | `Factoring Guided Practice/src/styles/factoring-double-bubble.css` (mirror grid rules) |

**Reference styling (pre-grid, committed):** `.factoring-gcf-menu-btn--bubble-action-compact` in
`factoring-guided-embed.css` (padding `0.1rem 0.4rem`, min-height `1.35rem`, was `white-space: normal`
for multi-line pick buttons in **separate** floats; grid now uses **nowrap** for one line).

**Git show baseline for per-button floats:** commit `7ef363c` in Factoring GP repo
(`FactoringBubbleControlsFloat.tsx` with `only={which}` per button).

### Broader uncommitted Factoring GP (same working tree)

Engine/layout/session: `practiceSession.ts`, `useFactoringPracticeSession.ts`, `generators.ts`,
`config.ts`, `partialFactoredDisplay.ts`, `useStepNumAnchorAlign.ts`, layout agent sync services,
tests (`buildSetProblem1Sweep`, `factoringLayoutPlacedDiff`, etc.).

### Portal / Programs (parallel dirty — not this thread's focus)

`student-portal` also has **rational functions** video assets/guide/css modified. `Programs/` has
Manim rational-function work and overwritten `latest.md` (this handoff replaces rational-functions
handoff in `latest.md`; dated copy `2026-10-16_rational-functions-examples-2-3.md` preserved).

### Layout scratch file

`agent docs/scratch/factoring-guided-layout-latest.json` — still `{ layout: null }` unless Chase
moved floats with docs server running. POST endpoint: `scripts/serve-programs-docs.js` →
`POST /__layout/factoring-guided-portal`.

---

## 6. Open questions / constraints

- **Visual sign-off pending** on thin + nowrap grid after last CSS fix (Chase should hard-refresh
  portal embed on double-bubble **products** step).
- If labels clip at narrow stage widths: prefer **slightly smaller font in grid only** before
  re-allowing wrap — Chase wanted one line.
- **Move box** with grid: tuner mode uses full rect %; if outline size fights intrinsic 9.5rem
  width, may need one more CSS pass (student vs tuner).
- **Do not deploy Netlify** unless Chase says so in-message.
- **PowerShell:** no `&&`.

---

## 7. Read first (fresh agent)

1. This file (`agent docs/momentum-handoffs/latest.md`).
2. `School Scrips/Factoring Guided Practice/AGENTS.md` (layout bake + scratch JSON link).
3. `School Scrips/student-portal/AGENTS.md` if touching embed CSS.
4. For styling truth: `git show 7ef363c:src/app/components/FactoringBubbleControlsFloat.tsx` and
   committed `factoring-guided-embed.css` bubble-action-compact block — **extend, don't reinvent**.

---

## 8. Exact next step

**Verify Chase's last request in the portal:** hard-refresh factoring guided practice embed, reach
**bubbleProducts** (all four binomial numbers filled, FOIL controls visible). Confirm 2×2 grid:
equal **thin** cells, **one-line** labels, Clear same size as Swap. If wrong, diff grid CSS against
`.factoring-gcf-menu-btn--bubble-action-compact` and fix only grid-scoped rules — do not re-add
2.75rem min-heights. If position is off, bake from Move box JSON or
`agent docs/scratch/factoring-guided-layout-latest.json` into `bubbleControlsGridRectPct` and bump
placed storage key.
