# Momentum handoff — Transformations graphing (portal embed)

**Written:** 2026-09-29 (Tuesday)

## Objective and current phase

Chase is polishing **Graphing Transformations Homework** in the **student portal** embed (`School Scrips/student-portal` + `School Scrips/transformations-app`). Layout, navigation, save/resume, and wrong-answer feedback are largely done. **Axis label clutter** on wide “Graph from your table” modals was just fixed. No git push or end-of-session in this handoff.

## Chase's desired feel

- Portal homework should feel like other portal apps: **← Back to home** (styled `portal-quiz__back-btn`), title in navy bar (**Graphing Transformations Homework**, white).
- Content clears the **left notch** (~50px inset); avoid vertical scrollbars in the white panel when possible.
- **In-activity ← Back** is OK; **first-try scoring must not reset** (session logger locks slots).
- Wrong answers in Stage 4 should **pulse the correct choice in green** (Identifying style), not solid red+green.
- Wide graphs (>10 data units visible): **no ±1 axis labels** — show **even integers only**; grid lines stay every 1 unit.
- Save state should match Identifying: **every click / sub-step** persists; reload returns to exact Stage 4 step (`tableBuild` blob).

## Accepted decisions

| Topic | Decision |
|--------|-----------|
| Portal banner back | `PortalQuizBackToPortalButton` → **← Back to home** (returns to transformations homework home, not classwork tiles). |
| In-activity back | Enabled in portal; `useGraphingSessionLogger` still write-once per slot. |
| Stage 4 wrong UI | `TableBuildPanel`: `TF_PULSE_CORRECT_BASE` + `animate-answer-grid-correct-pulse`; no red on wrong pick. |
| Portal progress | `GraphingProgressV1.tableBuild` + `useGraphingEmbedProgress`; skip intro reset on restore via `skipTableBuildResetRef`. |
| Graph axis labels | `resolveGraphGridLabelSteps` in `TableBuildGraphModal.tsx`: if visible span > 10 on either axis → `labelStep: 2` (evens only). Stretched cubics still use `tickSteps(scale)`. |
| Teacher Console title | Macro App still uses shorter `Graphing Transformations` in `transformationsSlotCatalog.ts`; portal uses `Graphing Transformations Homework` in `transformationsSharedActivity.ts`. |

## Rejected / do not redo

- **`portal-quiz__header-status`** for the homework title (red alert styling).
- **`portal-quiz__back`** plain text (no button styling).
- Disabling in-activity back in portal solely for scoring (scoring is server-side / logger-side).
- Static red+green operation buttons on Stage 4 wrong (replaced with pulse-correct-only).

## Current implementation state (key files)

**Portal**

- `student-portal/src/features/transformations/TransformationsGraphingView.tsx`
- `student-portal/src/app/components/PortalQuizBackToPortalButton.tsx`
- `student-portal/src/styles/transformations-embed.css` (animations, table header flash, parent function min-height)
- `student-portal/src/styles/portal-base.css` (`portal-quiz__header-title`)
- `student-portal/src/features/transformations/useTransformationsGraphingAttempt.ts`

**Transformations app**

- `GraphingTransformationsView.tsx` (~980 lines — **over 800 cap**; portal save logic extracted to `useGraphingEmbedProgress.ts`)
- `useGraphingEmbedProgress.ts`, `graphingProgress.ts`, `graphingTableBuildProgress.ts`
- `TableBuildPanel.tsx` — wrong-answer pulse
- `TableBuildGraphModal.tsx` — `resolveGraphGridLabelSteps`, `WIDE_VIEW_DATA_SPAN = 10`
- `tableBuildGraphTicks.test.ts` — 2 tests passing

**Verification**

- `npm test -- --run src/app/portal/graphingProgress.test.ts` (transformations-app)
- `npm test -- --run src/app/components/GraphingTransformations/tableBuildGraphTicks.test.ts` (transformations-app)

**Uncommitted:** All of the above likely dirty across `Programs/`, `transformations-app`, `student-portal` sibling repos — no commit/push this handoff.

## Open questions / constraints

- **GraphingTransformationsView.tsx** file size flag — future work should extract more before adding features.
- Chase may want **stages 1–3** wrong grids to pulse correct only (currently unchanged).
- **Identifying portal** banner back could match graphing (`Back to home` + back-btn) — not requested yet.
- **Never display without permission** — do not launch portal/GUI for Chase; hand off manual refresh checks.
- Frozen: Calendar 2.0.

## Exact next step

1. Refresh portal dev + transformations embed; open Problem 3 Stage 4 → **Graph** modal; confirm axis labels skip ±1 and show -2, 2, 4… when span > 10.
2. If Chase wants tighter/looser threshold, adjust `WIDE_VIEW_DATA_SPAN` in `TableBuildGraphModal.tsx` only.
3. If next work is unrelated, start fresh task from this handoff; if continuing graphing polish, grep `graphing-portal-embed` and `TransformationsGraphingView` first.

## Read first (fresh agent)

1. This file.
2. `School Scrips/student-portal/AGENTS.md` (portal embed patterns).
3. `School Scrips/transformations-app/src/app/portal/graphingProgress.ts` + `useGraphingEmbedProgress.ts` for resume behavior.
