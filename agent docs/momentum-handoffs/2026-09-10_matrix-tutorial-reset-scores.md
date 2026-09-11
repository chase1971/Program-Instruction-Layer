# Momentum handoff — 2026-09-10 — Student Portal Matrix tutorial + Teacher Console reset scores

> **Written:** 2026-09-10 (evening) · **Repos:** student-portal, Matrix app, App Dashboard, electron-toolbar, Macro App, student-session-kit (all uncommitted except migration already pushed to Supabase)

## Objective and current phase

Ship the **Gauss-Jordan Matrix tutorial** inside **Student Portal** for M1324 students, viewed in the **812×460 horizontal Chrome launcher** (`student-portal-horizontal` / **Portal Wide**). Tutorial flow, home screen, exit-to-home, viewport-fit layout, Part 1 step numbering, user watermark label, and step 9 popover layout are implemented. Chase confirmed **2026-09-10: "this looks good"** on the overall layout fix.

Also: **Reset scores** for instructor test student (CHASE1) in Macro App Teacher Console Matrix report — **implemented and migration live**; Chase has not yet verified in running Macro App.

Phase: **feature green locally** — tutorial walkthrough QA still outstanding; optional layout-debug cleanup; commit/deploy when Chase asks.

## Chase's desired feel

- **Shaped window matters** — never hand Chase raw browser URLs; use **Portal Wide** (812×460) or **Portal Debug** launchers. Full-browser links are useless for sizing judgment.
- **One white panel** — navy header through bottom rounded curve; **no gray/navy band** below the card.
- **Home screen** — matrix visible, intro text beside it, small **Start Tutorial** + **Auto Solve** (not a giant Tutorial button). No "step 1" label on open; flashing restored on buttons when applicable.
- **Red Exit** near Next (~20px offset) returns to **home**, not assignments Back.
- **No auto-resume** for this tutorial on load (resume is for homework later; teacher-console toggle deferred).
- **Cannot type URLs** — launchers must bake query params (`?s=CHASE1`, `layout-debug=1`) into `apps.json` `openQuery`.
- Layout debug overlays are **optional/dev** — too messy for daily use; Chase identifies frames by color when needed.
- **User watermark** — subtle muted **"User CHASE1"** beside Back in assignment headers (for screenshots / knowing which test code is active).
- **Step 9 popover** — all content visible without scrolling in 812×460; text and reciprocal animation **side-by-side**, tight gap (not a huge empty flex gap).
- **Reset scores** — one click next to instructor name in Matrix report to wipe attempts and retest scoring end-to-end.

## Accepted decisions

| Decision | Why |
|---|---|
| Mount Matrix parts via `MatrixSolver` / Part 2 / Part 3 directly in portal — not Matrix `App.tsx` | Matrix app owns part-selector chrome; portal supplies nav |
| Portal props on `MatrixSolver`: `hideStartControls`, `rightPanel`, `skipIntroOnStart`, `ref.startTutorial`, `skipIntroStepZero`, `popoverWidthExtra` | Home vs in-tutorial; Part 1 popover starts at step 1 not step 2 |
| `skipIntroOnStart` always true in `MatrixTutorialView.tsx` | Intro moved to home screen |
| `useMatrixTutorialAttempt` — no resume on load; phase starts `'tutorial'` | Chase: resume later for homework, not this walkthrough |
| Eager-import `MatrixTutorialView` in `App.tsx` (no lazy/Suspense) | Removed double loading flash |
| Matrix CSS scoped in `matrix-embed.css` — do **not** import Matrix `theme.css` / second Tailwind | Would repaint portal globals |
| Flex column fill for `.portal-quiz--matrix` chain (`100dvh`, white body bg) | Fixes gray below card in 460px-tall window |
| `PortalUserLabel.tsx` in matrix tutorial + generic quiz headers | Watermark-style user code beside Back |
| Step 9 layout: 2-line text \| `ReciprocalAnimation compact` \| Next (`ml-auto`); `popoverWidthExtra={20}` | Fits Portal Wide without scroll; tuned down from 100/120/50 |
| **`student-portal-horizontal-debug`** launcher + toolbar tile **Portal Debug** (🔍) | `openQuery`: `?s=CHASE1&layout-debug=1#/matrix-tutorial` |
| Reset via Supabase RPC `reset_student_attempts(p_student_id)` — service role only | Macro App Teacher Console; deletes all attempts (cascade items) |
| Reset button only on **`isInstructorPin`** rows in Matrix report | Chase's CHASE1 test row only |

## Rejected directions

- **`max-height: 500px` + inner scroll on `.matrix-embed`** — shrank usable area to ~200px; reverted.
- **Handing Chase `localhost` or `127.0.0.1` links** — wrong viewport; use launchers.
- **Nested rectangular card inside curved panel** — removed; one white shell.
- **Big custom Tutorial button on home** — Chase wanted original small Start Tutorial + Auto Solve restored.
- **Step 9 inline reciprocal animation** — switched to side-by-side row layout.
- **`flex-1` on step 9 paragraph** — caused giant empty gap between sentence and animation.
- **`popoverWidthExtra` at 100 / 120 / 50** — too wide or still awkward; **20** accepted.
- **Migration `010_reset_student_attempts.sql`** — collided with existing `010_matrix_tutorial.sql`; renamed to **`011_reset_student_attempts.sql`**.
- **End-of-session commit/push as part of this handoff** — not requested.

## Current implementation state

### student-portal (dirty)

| Area | Files |
|---|---|
| Tutorial view / home / exit | `MatrixTutorialView.tsx`, `MatrixTutorialHomePanel.tsx`, `MatrixTutorialNav.tsx`, `useMatrixTutorialParts.ts`, `useMatrixTutorialAttempt.ts`, `matrixTutorialActivity.ts` |
| User label | `PortalUserLabel.tsx` — used in `MatrixTutorialView.tsx`, `GenericQuizQuestionCard.tsx` |
| Layout fill fix | `src/styles/index.css` (`.portal-quiz--matrix` flex chain), `matrix-embed.css` |
| Layout debug | `useLayoutDebug.ts`, `LayoutDebugLegend.tsx`, `portal-layout-debug.css`, `data-layout-frame` on shell/panel/view |
| App wiring | `App.tsx`, `PortalShell.tsx`, `PortalContentPanel.tsx` |
| Launcher | `launch-horizontal-debug.bat` |

### Matrix app (dirty)

| File | Change |
|---|---|
| `matrix-solver.tsx` | Portal props: `skipIntroStepZero`, `popoverWidthExtra` |
| `matrix-tutorial-overlay.tsx` | Step 9 side-by-side layout; skip intro step zero |
| `reciprocal-animation.tsx` | `compact` prop for smaller inline fraction display |
| `use-matrix-tutorial.ts` | `startTutorial({ skipIntro?: boolean })` |

### Macro App (dirty — reset scores)

| Layer | Files |
|---|---|
| Supabase RPC caller | `electron-app/student-progress-io.js` — `resetStudentAttempts()` |
| IPC | `preload.js` — `student-progress:reset-student-attempts` |
| Renderer | `studentProgressService.ts`, `macroApp.d.ts`, `ConsoleMatrixReportScreen.tsx` (Reset scores button on instructor row), prop chain through `ConsoleAppsScreen`, `TeacherConsoleWorkspace`, `AppMainPanel` |
| CSS | `teacher-console-matrix-report.css` — `.matrix-report-name-cell`, `.matrix-report-reset-btn` |

### student-session-kit (dirty — migration file uncommitted)

- `supabase/migrations/011_reset_student_attempts.sql` — **already applied** to remote Supabase via `npm run db:push`

### App Dashboard (dirty)

- `apps.json` — `student-portal-horizontal-debug` entry

### electron-toolbar (dirty)

- `scripts-panel.html` — **Portal Debug** tile

### Reference (optional)

- `agent docs/scratch/student-portal-matrix-layout-frames.html` — nested diagram (not shaped window)

### Verification

- `npm run build` in student-portal — **passes**
- `npm run build:renderer` in Macro App — **passes**
- Supabase migration 011 — **pushed successfully**
- Chase verified overall layout on **Portal Wide** — **looks good**
- Step 9 popover — iterated from Chase screenshots; final width/layout not formally re-confirmed after `popoverWidthExtra={20}`
- Reset scores — **not yet tested by Chase** (Macro App restart required for preload change)
- Agent browser MCP — **failed** (`ECONNREFUSED 127.0.0.1:9227`); visual QA is Chase's launchers only

### Launcher tiles (Chase uses tiles, not URLs)

| Tile | apps.json id | Window | openQuery |
|---|---|---|---|
| Portal Wide | `student-portal-horizontal` | 812×460 | `?s=CHASE1` |
| Portal Debug | `student-portal-horizontal-debug` | 812×460 | `?s=CHASE1&layout-debug=1#/matrix-tutorial` |
| Student Portal (vertical) | `student-portal` | 460×812 | `?s=CHASE1` |

Close other portal Chrome windows before launching — shared `chrome-mobile-profile` / `localStorage` student code.

## Open questions and constraints

- **Tutorial step-by-step QA** on Portal Wide (Parts 1–3, submit, Exit to home, Auto Solve after completion) — not fully walked after step 9 / user label changes.
- **Auto Solve after re-entry bug (likely):** `useMatrixTutorialAttempt` does not hydrate `completedParts` from saved progress; after submit, `resume_attempt` returns nothing (completed) — Auto Solve may stay disabled when reopening tutorial. Flagged, not fixed.
- **Reset scores smoke test** — restart Macro App → Teacher Console → Apps → Matrix report → Reset scores on CHASE1 row → confirm cells clear → rerun tutorial from portal.
- **Remove layout debug** (launcher + CSS + legend) when Chase is done diagnosing — keep until he says otherwise.
- **Teacher Console** publish toggle + resume policy — explicitly deferred.
- **Netlify deploy** — only when Chase asks (`npm run deploy:prod` in student-portal).
- **Commit/push** — dirty across **6 repos** (student-portal, Matrix app, App Dashboard, electron-toolbar, Macro App, student-session-kit); wait for "put on GitHub" or end-of-session. Skip machine-local `Macro App/config/d2l-courses.json` unless Chase wants it.
- **Never display without permission** — QA is Chase's launcher, not agent opening Chrome/GUI.

## Exact next step

1. **Chase:** Restart Macro App, open Teacher Console → Apps → Gauss-Jordan Matrix Tutorial → click **Reset scores** on the CHASE1 instructor row; confirm report clears.
2. **Chase:** On **Portal Wide**, walk full tutorial (home → Start Tutorial → Parts 1–3 including step 9 popover → submit → Exit → reopen → Auto Solve). Report any clip/scroll/overlap issues.
3. **Agent (after Chase reports):** Fix any QA findings; if all green, ask whether to remove debug launcher/CSS and commit all six repos.

## Read first (fresh agent)

1. This file
2. `School Scrips/student-portal/AGENTS.md`
3. `School Scrips/student-portal/src/features/matrix-tutorial/MatrixTutorialView.tsx`
4. `School Scrips/Matrix app/src/app/components/matrix-tutorial-overlay.tsx` — step 9 layout
5. `School Scrips/Macro App/renderer/src/components/teacher-console/screens/ConsoleMatrixReportScreen.tsx` — reset button
6. `School Scrips/student-session-kit/supabase/migrations/011_reset_student_attempts.sql`
7. `School Scrips/App Dashboard/docs/LAUNCHER.md` — shaped Chrome / `viewOf` / profile sharing
