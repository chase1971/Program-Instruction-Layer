# Momentum handoff: 11.2 Homework layout, help triggers, solution-type panel

**Written:** 2026-10-23. Valid for today's continuation only.
**Nothing is committed or pushed.** Uncommitted work in `School Scrips/Matrix app`, `School Scrips/student-portal`, `School Scrips/student-session-kit` (migration 100), `School Scrips/Macro App`, and `Programs/scripts/serve-programs-docs.js`. Commit only on "pull", "put on GitHub", or end of session.

This overwrites the 2026-10-22 guided-practice polish handoff. That work remains in the files; this handoff is **homework + layout preview** continuation.

## Objective and phase

Chase is polishing **11.2 Homework** (Gauss-Jordan guided practice embed) in the student portal with tester cheats: yellow help labels, green correct-check placement, solution-type MCQ layout, and instructor **Layout preview** (was Check preview).

Last finished change: fixed `ReferenceError: currentSlot is not defined` in `GuidedPracticeSolver.tsx` (green check slot now uses `currentQuestion?.slot`). He has not re-confirmed homework after that fix.

## Chase's desired feel

- Portal only for review. No launch/deploy unless he asks in the same message.
- Yellow "Need help with…?" is **one system** (`GuidedPracticeHelpTrigger`). Widen by **CSS max-width**, not by shifting anchors unless he asks to move position.
- When he says "bring it in" or "shrink width", change **label width**, not anchor offset. When he says "move left/right", that is **position**.
- Layout preview: drag green check and visible yellow help on the **current step**, then **Save** (banner). No second tool.
- Green check is **only visible continuously in Layout preview**; during normal play it flashes ~0.7s on a correct answer.

## Accepted decisions

- Student-facing homework title: **11.2 Homework** (capital H). Portal + Macro catalog + migration `100_gauss_jordan_homework_title_capitalize.sql`.
- Infinite-solution homework problem **first on Start**; home card without "Four problems".
- Solution-type step: MCQ **1 / 2 + Submit** in right panel (`GuidedPracticeSolutionTypePanel`), not in the blue prompt.
- Help triggers beside matrix: **viewport-portaled** from matrix/row anchors (`useViewportAnchorPosition`) so embed layout cannot squeeze labels into a vertical strip.
- Help label max-width (compact wide): `min(calc(9.625rem + 15px - 30px), 78vw)` in Matrix `theme.css` and portal `guided-practice-fraction-help.css`.
- **Layout preview** (banner): drags **green check** + **yellow help** for the active step; **Save** writes check offsets to existing localStorage + `helpTriggerOffsets` in agent scratch JSON via `POST http://127.0.0.1:8765/__layout/gp-correct-check-offsets`.
- Help layout keys: `fraction:{slot}` (row-entry), `notation:scale` / `notation:replace`.
- Tutorial tile: **Gauss-Jordan Method Tutorial** (session-kit migration 098).

## Rejected / corrected (do not rediscover)

- **Do not** fix narrow yellow labels by only bumping `max-width` while trigger stays `placement="parent"` inside the matrix column. Portal embed will still crush it. Use viewport portal + anchor.
- **Do not** move help triggers 30px left when Chase asked to **shrink width 30px** (he corrected this explicitly).
- **Do not** put solution-type choices back inside the blue prompt box.
- **Do not** launch GUI or Netlify for verification.
- Dev **HMR**: portal **CSS-only** edits often hot-update in place; **Matrix app `.tsx` / hooks** usually full-refresh and reset homework to **home** (`screen: 'home'` in `GuidedPracticeHomeworkView`). Use **Resume** after reload; tune help width in portal CSS when possible to avoid losing step progress.

## Current implementation state

Key files (uncommitted):

- **Layout preview:** `useGuidedPracticeLayoutPreview.ts`, `helpTriggerLayoutPosition.ts`, `gpLayoutPreviewPublish.ts`, `guidedPracticeHelpLayoutKey.ts`, `GuidedPracticeCheckLayoutBannerControls.tsx` (button **Layout preview**), `GuidedPracticeHelpTrigger.tsx` (anchor, layout offset, preview drag), `GuidedPracticeCorrectCheckSlot.tsx`, `correctCheckPosition.ts`.
- **Solver:** `GuidedPracticeSolver.tsx` (~740 lines, near cap). Uses layout hook at top; `slot={currentQuestion?.slot}` on check slot.
- **Solution-type panel:** `GuidedPracticeSolutionTypePanel.tsx`, session submit select + submit flow, tests in `guided-practice-infinite-solution.test.tsx`.
- **Portal:** homework views, `guided-practice.css` (`overflow: visible` on inset), fraction-help CSS, check layout banner.
- **Docs server:** `scripts/serve-programs-docs.js` accepts optional `helpTriggerOffsets` in save body.
- **Migrations:** `099` (11.2 homework lowercase in DB), `100` (11.2 Homework capitalize). Push session-kit when syncing.

Tests passed (headless, Matrix app): including `helpTriggerLayoutPosition.test.ts`, `correctCheckPosition.test.ts`, `guided-practice-infinite-solution.test.tsx`, full suite 178 tests after layout work.

## Open questions and constraints

- Chase reported **multiplying fractions** help shoved to top-left; fix was no render at `0,0` until anchor ready + layout offsets. He should confirm on **row-entry** step after refresh.
- **Green check "disappeared"** after save: likely saved translate off-screen or only visible on flash. Use **Layout preview** to drag back and Save; check `localStorage` key `matrix-gp-correct-check-offsets-v1`.
- **GuidedPracticeSolver.tsx** is near 700/800 line cap. Next feature work in this file should **extract**, not inline.
- `GuidedPracticeSolver` had hooks after early returns historically; layout hook now runs unconditionally at top. Do not add hooks below fraction-help early returns.

## Read first

- `School Scrips/Matrix app/src/app/components/guided-practice/GuidedPracticeSolver.tsx` (layout wiring only; do not read whole file if grep suffices).
- `School Scrips/Matrix app/src/app/components/guided-practice/GuidedPracticeHelpTrigger.tsx`
- `School Scrips/Matrix app/src/app/components/guided-practice/useGuidedPracticeLayoutPreview.ts`
- Portal `GuidedPracticeHomeworkView.tsx` (screen home/work, banner controls).
- Scratch offsets (when docs server running): http://127.0.0.1:8765/scratch/gp-correct-check-offsets.json

## Exact next step

Open **11.2 Homework**, resume problem 1, row-entry step with **multiplying fractions** help. Confirm yellow label sits under/near the typed row (not header corner). Turn **Layout preview** on: drag yellow help and green check if needed, **Save**, reload once, confirm positions stick. If anything still wrong, one screenshot + which step slot (`checkSlot` in banner sr-only / session snapshot) is enough to adjust offsets or CSS width only.
