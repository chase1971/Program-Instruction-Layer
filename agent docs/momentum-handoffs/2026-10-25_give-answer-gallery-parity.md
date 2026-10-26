# Momentum handoff: Give answer cheat, homework nav strip, frame gallery parity, Teacher Console white preview

**Written:** 2026-10-25. Valid for today's continuation only.
**Nothing is committed or pushed.** No Netlify deploy was run (and none is wanted unless Chase says so in that message).

## Objective and current phase

Three threads in one long chat, all code-complete and headless-tested, **none walked through end to end by Chase after the last change**:

1. **11.2 homework "Give answer" admin cheat** (types the right answer without submitting; selection steps click the right choice and advance).
2. **Homework problem strip** (1-6 pills) hosting Give answer, with admin able to jump to any problem.
3. **Frame gallery must match the real app exactly** (Chase uses it to place the check mark, prompt boxes, help triggers; a mismatch makes the gallery pointless).
4. (Earlier in chat) **Macro App Teacher Console embedded preview white screen** on cold launch.

## Chase's desired feel

- Give answer sits **right beside the active problem number in the top strip**, same height as the number pills (can be wider). Not on the blue instruction-card badge.
- With admin/cheats he can **click any problem number** (1-6) to open it.
- The frame gallery must be an **absolute-position truth source**: "These definitely absolutely have to match... if I'm using the frame gallery to determine positioning, and then it doesn't give me the right positioning, there's no purpose for it." He thinks of positions as absolute; they are not (see below).
- He reviews in the portal / Macro App preview, never MP4s. Handoffs are statements, not questions.

## Accepted decisions (facts)

- **Give answer lives in `UnguidedPracticeProblemNav`** (student-portal) next to the *active* pill. `GuidedPracticeOverlay` badge button is kept for non-homework callers but hidden in homework/gallery via `hideOverlayAdminGiveAnswer`.
- **Active problem number follows `workingProblemId`** (open problem), not saved `displayProblemNumber`. `openProblem` now calls `focusHomeworkProblem` so progress index stays in sync.
- **Admin jump:** `homeworkProblemNavItems({ adminBypassLocks })` marks every non-active pill clickable when `hasAdminCheats()`.
- **Nav clicks failed before** because the strip was outside `.matrix-tutorial-nav__steps` (parent nav is `pointer-events: none`). Strip now uses `matrix-tutorial-nav__steps` + explicit `pointer-events: auto`. Give answer is no longer `disabled` (faded via `--inactive` class instead) so dwell clicks are never swallowed.
- **Frame gallery now renders one shared shell** (`FrameStage.tsx`: same `portal-content-wrap > panel > body-plain > portal-quiz portal-quiz--guided-practice` chain + real header, then `section.matrix-embed--with-nav` with the nav strip, then the inset). Thumbnails and live view render the identical tree; thumbs only scale it. Both use `box-content` so the stage is a true 812x460.
- **Root cause of the check-mark mismatch (measured live in the Macro App preview):** the check mark is NOT absolute. `GuidedPracticeCorrectCheckSlot` is a flex sibling after the matrix grid, moved by a saved `translate(x,y)` per slot (`matrix-gp-correct-check-offsets-v1`, e.g. `setup-augmented-matrix` = -200,65). In gallery frames the homework keypad was open **inside that same flex row**, pushing the check's starting point ~230px right; in the app the keypad is closed when the check shows. **Fix:** `HomeworkMatrixEntryPhase.tsx` now wraps the keypad in `absolute left-full top-0 ml-[30px]` so it is out of flow. Measured after: check base x=426 = grid right edge; keypad at 456 (= +30); check lands at x~226, matching Chase's app screenshot.
- Bots/tests (`frameBot.tsx`, `frameTransitions.test.tsx`) now scope button lookups to `.matrix-guided-practice-inset` because the strip's number buttons and header Back button broke text/index-based lookups.

## Rejected directions / do not rediscover

- Putting Give answer on the instruction card badge for homework (Chase rejected: wrong spot).
- `disabled` on Give answer (blocked clicks).
- Rendering gallery thumbs as the bare solver (different layout from live and app).
- Converting check offsets to absolute coordinates: considered, **not done**. It would invalidate all saved offsets and needs Chase's say-so. Only proposal, not a decision.

## Current implementation state

**Matrix app** (`School Scrips/Matrix app`): `GuidedPracticeOverlay.tsx`, `GuidedPracticeSolver.tsx` (+ `.types.ts`: `adminGiveAnswer`, `adminGiveAnswerEnabled`, `hideOverlayAdminGiveAnswer`, `onAdminGiveAnswerEnabledChange`), `ThreeVarHomeworkSolver.tsx` (+ types), `UnguidedPracticeSolver.tsx` (handle now exposes `adminGiveAnswer`), `HomeworkMatrixEntryPhase.tsx` (keypad out of flow), hooks `use-guided-practice-admin-give-answer.ts`, `homework-matrix-admin-fill.ts`, `use-homework-matrix-setup.ts`, `use-three-var-homework-session.ts`.

**student-portal**: `UnguidedPracticeProblemNav.tsx`, `GuidedPracticeHomeworkWorkspace.tsx` (refs/enabled sync/handler; `syncAdminGiveAnswerEnabled` effect must stay declared AFTER its `useCallback`, a hook-order crash happened once), `GuidedPracticeHomeworkView.tsx` (`workingProblemNumber`, `openProblem` focus), `homeworkProblemNavStatus.ts` (+ test), `src/styles/guided-practice.css`, `src/types/matrix-app.d.ts`, frame gallery: `FrameStage.tsx` (new), `FrameGalleryHomeworkNav.tsx` (new), `frameGalleryHomeworkProblemNumber.ts` (new), `FrameSolver.tsx`, `FrameThumb.tsx`, `FrameGalleryView.tsx`, `frameBot.tsx`, `frameTransitions.test.tsx`, `FrameSolver.test.tsx`.

**Macro App** (`School Scrips/Macro App`): Teacher Console preview reliability: `useTeacherConsolePreviewRefresh.ts`, `useTeacherConsolePreviewBoundsRecovery.ts`, `useTeacherConsolePreviewSlotHealth.ts`, `TeacherConsolePortalPreviewEmbed.tsx`, `browser-slot-blank-page-watchdog.js` (+ test). **Needs a full Macro App restart** to load the main-process watchdog; never verified on a cold launch.

**Verification run:** student-portal `src/features/frame-gallery` 49/49 pass; `homeworkProblemNavStatus.test.ts` 4/4; Matrix app correct-check / homework-matrix / three-var 28/28; watchdog tests 8/8. `tsc --noEmit` in student-portal shows many **pre-existing** errors (stale `matrix-app.d.ts` for gallery props, generic-quiz); not caused by this work.

## Open questions and constraints

- Chase has **not re-checked** the frame gallery after the keypad fix. Other screens may still have a state-dependent check base; from code reading only the matrix-entry phase put a keypad in the check's flex row (solution-entry keypad is outside that row).
- Gallery stage header has no Edit layout buttons (real header does); header height may differ slightly.
- Whether to move check positions to true absolute coordinates is **undecided** (loses saved offsets; needs his OK).
- Rules: never put anything on his screen without asking (he explicitly allowed Macro App preview takeover for measuring, per-run); no Netlify deploy without an explicit ask; no em dashes; small buttons; no ephemeral success text; do not commit/push mid-session.
- Measuring tip: Macro App MCP `browser_tabs` tab with `127.0.0.1:5340` is the portal preview; `browser_evaluate` is read-only measurement. Gallery thumbs may not render (IntersectionObserver in occluded view); clicking a frame holder renders the live frame.

## Exact next step

Ask nothing. First, tell Chase to refresh Teacher Console preview, open the frame gallery, open `P1.Q1.OK`, and compare against the app's problem 1 setup step (check mark position, Give answer beside the active number). If he reports another screen where the check differs, measure that frame's check base vs the app's with `browser_evaluate` (check `data-gp-correct-check-slot`, its `translate`, and the previous sibling's rect) and fix the flow-dependent sibling the same way.
