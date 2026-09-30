# Momentum handoff — Transformations portal (graphing polish + shared result)

**Written:** 2026-09-29 (Tuesday)

## Objective and current phase

Chase is polishing **Transformations Homework** in the **student portal**: graphing embed (Stages 1–5), wrong-answer pulse UX, and the **shared result screen** used by both **Identifying** and **Graphing** after submit. Graphing layout, save/resume, axis labels, and most feedback UI were done before this continuation; this session focused on **pulse sync**, **parent-equation alignment**, **Stage 5 table collapse in embed**, and **result celebrations + button layout**. No git commit/push or end-of-session in this handoff.

## Chase's desired feel

- Wrong-review screens: **every pulsing control** (green correct choice + blue Next) must share the **same rate, start time, and visual “breath”** — not opposite or snappy vs slow.
- Green pulse should **grow a ring** at peak (more highlight), not fade lighter; blue Next must **match that same ring pulse**, not opacity dip.
- Stages 2–3: parent function equation (**y = x²**, etc.) stays in the **same screen position** when stepping graph ↔ table.
- Stage 5: middle columns **collapse/merge** into final x/y table (animation), then Graph + Next → — same as standalone app.
- Result screen (both modes): **confetti** at pass (≥ 70% first-try), **storm + rain + ⛈️** below 70%; **Review mistakes** and **Back to menu** on **one row**, compact.
- Portal graphing still: ← Back to home, navy title, notch inset, no spurious scrollbars when possible.
- **Do not launch GUI for Chase** — hand off refresh checks; never display without permission.

## Accepted decisions

| Topic | Decision |
|--------|-----------|
| Wrong-review pulse clock | Single **`graphingReviewPulseStore`** (rAF) + **`useGraphingReviewPulsePhase`**; all targets read same phase each frame. |
| Pulse visuals | **`graphingReviewRingLayer()`** only — 2px→4px ring, shared alpha curve; green/blue differ by color only. Applied via inline styles in **`TableBuildPanel`**, **`GraphingReviewNextButton`**, **`ParentFunctionTable`**. |
| CSS fallback | `animate-*-pulse` keyframes updated to ring-only (no border-color flash at 50%); synced path prefers JS store when active. |
| Parent equation slot | Stages 1–3 left column **fixed 22rem**; **`graphing-parent-function__math`** left-aligned + min-height (portal + app CSS). |
| Stage 5 collapse in portal | **`table-col-collapse-inner`** rules copied to **`student-portal/src/styles/transformations-embed.css`** (standalone uses `transformations-app/src/styles/index.css`). |
| Result celebration | **`TransformationsResultCelebration`**: tier from **`firstTryPct >= TRANSFORMATIONS_PASS_PCT` (70)**; confetti vs rain; overlay **`z-index: 5`**, body **`z-index: 6`**; canvas sized via ResizeObserver on **`.transformations-result__stage`**. |
| Result actions | **`transformations-result__actions`**: row, flex, smaller buttons (~9–12rem). |
| Shared result | **`TransformationsResult.tsx`** — both **`TransformationsGraphingView`** and **`TransformationsIdentifyingView`**. |

## Rejected / do not redo

- **CSS-variable-only sync** on `.graphing-pulse-sync` without JS — green buttons’ inline styles + `transition: box-shadow 100ms` fought it; felt out of sync.
- **Opacity pulse on blue Next** while green uses ring — felt opposite at apex.
- **Border/background color animation** on green during synced pulse — made green feel faster/snappier than Next.
- Re-enabling separate **0.75s vs 1s** CSS animation durations for Next vs green.

## Current implementation state (key files)

**Pulse (transformations-app)**

- `src/app/components/GraphingTransformations/graphingReviewPulseStore.ts`
- `graphingReviewPulseStyles.ts` — `graphingReviewPulseRing`, `graphingReviewRingLayer`, correct/next/table helpers
- `useGraphingReviewPulsePhase.ts`
- `GraphingReviewNextButton.tsx`
- `GraphingTransformationsView.tsx` — `startGraphingReviewPulse` / `stop` in `useLayoutEffect` when wrong-review active
- `panels/TableBuildPanel.tsx`, `FunctionTablePanel.tsx`, `FunctionNamePanel.tsx`, `FunctionGraphPanel.tsx`, `ParentFunctionTable.tsx`
- `IdentifyingTransformations/shared/ActionButton.tsx` — optional `pulseBoxShadow`
- `src/styles/index.css` — ring keyframes for fallbacks

**Portal embed CSS**

- `student-portal/src/styles/transformations-embed.css` — pulse fallbacks, **table collapse**, **result celebration + actions**, parent-function slot (mirror app where needed)

**Result (student-portal)**

- `src/features/transformations/TransformationsResult.tsx`
- `TransformationsResultCelebration.tsx`

**Graphing (unchanged this session but context)**

- `GraphingTransformationsView.tsx` (~980 lines — **over 800 cap**; extract before large features)
- `useGraphingEmbedProgress.ts`, `TableBuildGraphModal.tsx` (`WIDE_VIEW_DATA_SPAN = 10`), `TableBuildPanel.tsx`

**Verification (headless only this session)**

- `npm test -- --run src/app/portal/graphingProgress.test.ts` (transformations-app) — passed earlier in arc; re-run if touching progress.

**Uncommitted:** Likely dirty across **`Programs/`**, **`School Scrips/student-portal`**, **`School Scrips/transformations-app`** — no commit/push this handoff.

## Open questions / constraints

- Chase has **not visually confirmed** post-fix: confetti on pass, storm under 70%, inline result buttons, Stage 5 collapse animation, Stage 4 pulse “same breath” — refresh portal dev only (no shutdown required; hard refresh if stale).
- **No middle “cloud” tier** for 70–79% on Transformations result (Logic uses 80/70 splits); only pass confetti vs fail storm. Add only if Chase asks.
- **`GraphingTransformationsView.tsx` file size** — future work: extract before adding features.
- Frozen: Calendar 2.0. **Never display without permission.**

## Exact next step

1. Refresh portal dev; finish or open **Graphing** → trigger **Stage 4 wrong** (e.g. miss a transformation): confirm green + Next **same ring pulse**.
2. Complete a problem to **Stage 5** → **Next** on full table → confirm **collapse animation**, then two-column table + Graph.
3. Submit **Graphing** and **Identifying** results: **≥70%** confetti visible; **&lt;70%** rain + ⛈️; both buttons **one row**.
4. If anything still off, grep `graphingReviewPulse` / `TransformationsResultCelebration` first; do not reintroduce separate CSS animation loops for wrong-review.

## Read first (fresh agent)

1. This file.
2. `School Scrips/student-portal/AGENTS.md` (portal embed, no GUI without ask).
3. `School Scrips/transformations-app/src/app/components/GraphingTransformations/graphingReviewPulseStore.ts` + `graphingReviewPulseStyles.ts` for pulse behavior.
4. `School Scrips/student-portal/src/features/transformations/TransformationsResultCelebration.tsx` for result tiers.
