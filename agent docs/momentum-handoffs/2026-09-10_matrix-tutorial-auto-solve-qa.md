# Momentum handoff — 2026-09-10 — Student Portal Matrix tutorial + Auto Solve QA

> **Written:** 2026-09-10 (evening, post–Auto Solve nav fixes) · **Repos:** student-portal, Matrix app, Macro App, App Dashboard, electron-toolbar, student-session-kit (all uncommitted)

## Objective and current phase

Ship the **Gauss-Jordan Matrix tutorial** inside **Student Portal** for M1324 students, viewed in the **812×460 horizontal Chrome launcher** (`student-portal-horizontal` / **Portal Wide**). Also: **Reset scores** for instructor test student (CHASE1) in Macro App Teacher Console.

Phase: **feature green locally, QA outstanding** — layout and completion flow accepted; Auto Solve nav/skip/animation behavior fixed this session but **not yet re-verified by Chase**. Six repos dirty; nothing committed. Migration 011 live on Supabase.

## Chase's desired feel

- **Shaped window matters** — never hand Chase raw browser URLs; use **Portal Wide** (812×460) or **Portal Debug** launchers.
- **One white panel** — navy header through bottom rounded curve; no gray/navy band below the card.
- **Home screen** — matrix visible, intro text beside it, small **Start Tutorial** + **Auto Solve**; no "step 1" label on open.
- **Red Exit** near Next (~20px offset) returns to **home**, not assignments Back.
- **No auto-resume** for this tutorial on load.
- **User watermark** — subtle muted **"User CHASE1"** beside Back in assignment headers.
- **Step 9 popover** — all content visible without scrolling in 812×460; text and reciprocal animation side-by-side.
- **Tutorial complete** — no abrupt "3 of 3" result screen; after Finish, land on **tutorial home** with green **Tutorial complete** in the intro box + Auto Solve review message; **Auto Solve** pulses; header **← Back** still goes to Assignments when leaving the app entirely.
- **Auto Solve** — nav bar matches tutorial (**Auto: OFF** | Back | Next | Exit); Next during animation **skips** to next step's correct matrix; Next while **resting** **plays** the next step's animation; Back jumps to previous step resting; sum-step animations **40% faster** than tutorial.
- **Reset scores** — one click on CHASE1 instructor row in Matrix report.

## Accepted decisions

| Decision | Why |
|---|---|
| Mount Matrix parts via `MatrixSolver` / Part 2 / Part 3 directly in portal | Matrix app owns part-selector chrome; portal supplies nav |
| Portal props on `MatrixSolver`: `hideStartControls`, `rightPanel`, `skipIntroOnStart`, `popoverWidthExtra`, etc. | Home vs in-tutorial; Part 1 popover starts at step 1 |
| `useMatrixTutorialAttempt` — no mid-step resume; hydrate `completedParts` from in-progress blob or completed attempt history | Home unlock + Auto Solve on re-entry without resuming mid-tutorial |
| Completion → `handleExitToHome` + `MatrixTutorialHomePanel completed={true}` | No `MatrixTutorialResult` screen; Chase rejected abrupt score screen |
| `MatrixAutoSolveNav` + `hideControls` on `MatrixAutoSolver` in portal | Same nav chrome as `MatrixTutorialNav` |
| Auto Solve Next: `isRunningRef` → `jumpToStepResting(+1)`; else `advanceToNextStep()` | Skip mid-animation without killing future animations |
| `manualNavRef` + `currentStepIndexRef` | Prevent double-step skip from autoplay effect racing manual Next |
| `AUTO_SOLVE_SUM_SPEED = 0.6` + `timingScale` on multiply-then-add animations | Sum steps 40% faster in Auto Solve only |
| Part 2 step 3 popover **390px** | Three-line wrap for row-replacement intro |
| Part 3 step 3 fraction input ~30% smaller than original | Chase tuned via two 20%+10% reductions |
| Reset via RPC `reset_student_attempts(p_student_id)` | Macro App service role; migration **011** |
| **`student-portal-horizontal-debug`** + toolbar **Portal Debug** tile | `?s=CHASE1&layout-debug=1#/matrix-tutorial` |

## Rejected directions

- Separate **Tutorial complete** result screen with "3 of 3" and **Back to Assignments** footer — Chase rejected; lands on home instead.
- **Every** Next click using `jumpToStepResting` — killed all animations after first skip; fixed to two-mode Next.
- Handing Chase `localhost` links — use launchers only.
- End-of-session commit/push as part of this handoff — not requested.

## Current implementation state

### student-portal (dirty)

| Area | Files |
|---|---|
| Tutorial view / home / completion | `MatrixTutorialView.tsx`, `MatrixTutorialHomePanel.tsx`, `MatrixTutorialNav.tsx`, `MatrixAutoSolveNav.tsx`, `useMatrixTutorialAttempt.ts`, `useMatrixTutorialParts.ts`, `matrixTutorialActivity.ts` |
| User label | `PortalUserLabel.tsx` |
| Layout / debug | `index.css`, `matrix-embed.css`, `useLayoutDebug.ts`, `LayoutDebugLegend.tsx`, `portal-layout-debug.css`, `launch-horizontal-debug.bat` |
| Types | `matrix-app.d.ts` — `MatrixAutoSolver` ref + portal props |

### Matrix app (dirty)

| File | Change |
|---|---|
| `matrix-auto-solver.tsx` | `forwardRef`, `hideControls`, `jumpToStepResting`, two-mode Next/Back, manual-nav guard, sum speed |
| `matrix-solver.tsx` | Portal props; hide Auto Solve tip bubble when `rightPanel` present |
| `matrix-tutorial-overlay-part-2.tsx` | Step 3 width 390px |
| `matrix-tutorial-overlay-part-3.tsx` | Smaller fraction input; step 5 copy |
| `matrix-tutorial-overlay.tsx` | Step 9 layout; `popoverWidthExtra` |
| `row-multiply-then-add-animation*.tsx` | `timingScale` prop |
| `animation-timing.ts` | `AUTO_SOLVE_SUM_SPEED`, `AUTO_SOLVE_MULTIPLY_ADD_STEP_DURATION_MS` |

### Macro App (dirty — reset scores)

| Layer | Files |
|---|---|
| RPC | `electron-app/student-progress-io.js`, `preload.js` |
| UI | `ConsoleMatrixReportScreen.tsx`, prop chain, `teacher-console-matrix-report.css` |
| Service | `studentProgressService.ts`, `macroApp.d.ts` |

### Other dirty repos

| Repo | Change |
|---|---|
| App Dashboard | `apps.json` — horizontal + debug portal entries |
| electron-toolbar | `scripts-panel.html` — Portal Debug tile |
| student-session-kit | `011_reset_student_attempts.sql` (applied via `db:push`; file uncommitted) |

### Verification

- `npm run build` student-portal — **passes** (last run this session)
- Matrix app `animation-timing.test.ts` — **passes**
- Chase confirmed overall layout **"looks good"** on Portal Wide (earlier session)
- **Reset scores** — not confirmed by Chase (Macro App restart required)
- **Auto Solve** nav/skip/animation fixes — implemented this session; **Chase has not re-QA'd**
- **Full tutorial walkthrough** after completion-flow + popover tweaks — **not formally confirmed**

### Launcher tiles

| Tile | apps.json id | openQuery |
|---|---|---|
| Portal Wide | `student-portal-horizontal` | `?s=CHASE1` |
| Portal Debug | `student-portal-horizontal-debug` | `?s=CHASE1&layout-debug=1#/matrix-tutorial` |

Close other portal Chrome windows before launching — shared profile/localStorage.

## Open questions and constraints

- **Auto Solve QA** — Next mid-animation (skip, one step, correct matrix); Next while resting (animation plays); Back then Next (animation replays); Auto ON/OFF; sum steps feel 40% faster.
- **Full tutorial QA** — Parts 1–3, step 9 popover, Finish → home completion box, Auto Solve unlock, re-entry.
- **Reset scores smoke test** — restart Macro App → Teacher Console → Matrix report → Reset on CHASE1 row.
- **Remove layout debug** when Chase is done — launcher, CSS, legend still present.
- **Commit/push** — wait for "put on GitHub" or end-of-session; skip `Macro App/config/d2l-courses.json` unless asked.
- **Never open GUI/browser without permission** — QA is Chase's launchers.
- **`MatrixTutorialResult.tsx`** — orphaned (unused); safe to delete when cleaning up.

## Exact next step

1. **Chase:** On **Portal Wide**, QA **Auto Solve** — skip mid-animation, advance while resting, Back+Next, confirm matrix always correct.
2. **Chase:** Walk full tutorial → Finish → home completion message → Auto Solve; optionally test **Reset scores** in Macro App.
3. **Agent (after Chase reports):** Fix any QA findings; if all green, ask whether to remove debug launcher/CSS, delete `MatrixTutorialResult.tsx`, and commit all six repos.

## Read first (fresh agent)

1. This file
2. `School Scrips/student-portal/AGENTS.md`
3. `School Scrips/student-portal/src/features/matrix-tutorial/MatrixTutorialView.tsx`
4. `School Scrips/Matrix app/src/app/components/matrix-auto-solver.tsx` — Next/Back/skip logic
5. `School Scrips/student-portal/src/features/matrix-tutorial/MatrixAutoSolveNav.tsx`
6. `School Scrips/Macro App/renderer/src/components/teacher-console/screens/ConsoleMatrixReportScreen.tsx`
7. `School Scrips/App Dashboard/docs/LAUNCHER.md` — shaped Chrome / launcher tiles
