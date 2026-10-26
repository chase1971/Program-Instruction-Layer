# Momentum handoff: Frame gallery overlaps, notation help anchor, homework 4–6 finish flow

**Written:** 2026-10-25. Valid for today's continuation only.
**Nothing is committed or pushed.** No Netlify deploy was run.

## Objective and current phase

One long session on **11.2 homework** and the **frame gallery** (`#/frame-gallery`, `?s=CHASE1` for headless). Code is in place and **headless tests pass**; Chase has **not** walked through the latest homework finish modal / nav fixes in the live portal after the last edits.

## Chase's desired feel

- Frame gallery must match the **real student app** for layout work (check marks, prompts, yellow help triggers). False overlaps (especially sr-only) are noise; **real** overlaps need **red boxes** so he can see them.
- Gallery should **refresh** when he moves things in Edit layout, and **check all frames without scrolling** (staggered thumb mount).
- Content shifted **right** to clear the Teacher Console preview notch (black pill).
- Yellow **notation** help triggers must not sit in the top banner where he cannot drag them; anchored to the matrix with a minimum offset below the anchor (~50px).
- **"Use a calculator"** bold in the three-var RREF instruction everywhere that prompt appears.
- Solution-type pick (3 choices) gets **two tries**, not three (three tries would always succeed).
- After problems **4–6**, if credit is **yellow or red**, a **modal**: redo, similar (later), or next; pulse the problem number; he must be able to **click a finished problem** and **stay** on it (no auto-advance bounce).

## Accepted decisions

**Frame gallery (student-portal `src/features/frame-gallery/`)**
- Overlap detector skips `.sr-only`; reports intersection **region**; merges **cut-offs** from `frameClipping.ts`.
- Red overlay boxes via `FrameOverlapBoxes.tsx`; live poll via `useLiveFrameOverlaps.ts`; status bar with **Show only problems**.
- Upfront checks: staggered `FrameThumb` mount (`MOUNT_STAGGER_MS`), collapsed off-screen measure, `refreshKey` from parent.
- Notch clearance: `NOTCH_CLEARANCE_PX` on section + live modal (`?previewNotch=1` awareness elsewhere).
- `frameCatalog`: solution-type wrong frames use **2** steps (reveal at W2), not W3.

**Notation help (Matrix app guided-practice)**
- `NOTATION_HELP_REFERENCE_MATRIX`, `matrixAnchorRef`, `notationHelpOffsetFromMatrix`, layout keys `notation:${kind}:v2`.
- `useViewportAnchorPosition`: rAF retry when anchor ref null; container-pixel conversion for scaled gallery.
- `GuidedPracticeHelpTrigger`: `MIN_BELOW_ANCHOR_TOP_PX = 30` on layout offset Y when anchored.
- **Fraction** help triggers: same gallery-vs-app coordinate mismatch **not** fixed (Chase approved notation-only).

**Copy / retries**
- `promptEmphasis.tsx` bolds **Use a calculator** in overlay via `EditableText` children; plain string unchanged for overrides/logs.
- `HOMEWORK_SOLUTION_TYPE_MAX_ATTEMPTS = 2`; gallery seed + session + resume use it.

**Homework finish / nav (student-portal)**
- Problems 4–6: **no** generic `useHomeworkAutoAdvance`; green credit waits `HOMEWORK_NEXT_PROBLEM_HOLD_MS` then advances via `useHomeworkThreeVarFinish.ts`.
- Yellow/red: `HomeworkThreeVarFinishModal.tsx` (similar disabled); **Redo** clears events via `resetHomeworkProblem`.
- Strip click sets `allowAutoAdvance: false` so finished problems do not auto-jump.
- **Prompt flash fix:** `homeworkResumeQuestionIndex` returns **0** when problem has **no answer events** (stale `stepIndexByProblem` from cross-problem race). Snapshots include `problemId`; `recordQuestionIndex` ignores wrong problem. Overlay `key` on slot+prompt in `ThreeVarHomeworkSolver`.
- `ThreeVarHomeworkSolver` `onComplete` wired to portal (was noop).

## Rejected / do not rediscover

- Counting sr-only duplicate text as overlap.
- Fixing fraction-help gallery positions without Chase asking (notation was the approved scope).
- Three tries on solution-type pick.
- Auto-advance when student clicks back to a finished problem on the strip.

## Current implementation state

**Matrix app:** `homework-practice-retry.ts`, `use-three-var-homework-session.ts`, `three-var-homework-resume-state.ts`, `three-var-homework-frame-gallery-seed.ts`, `GuidedPracticeOverlay.tsx`, `promptEmphasis.tsx`, `GuidedPracticeHelpTrigger.tsx`, `useViewportAnchorPosition.ts`, `fractionHelpButtonPosition.ts`, `guided-practice-notation-help-trigger.tsx`, `GuidedPracticeSolver.tsx`, `ThreeVarHomeworkSolver.tsx`, `threeVarHomeworkSolverTypes.ts`, tests updated (264 Matrix tests passed last full run; three-var subset 23/23).

**student-portal:** frame-gallery overlap/clipping/checks/nav/notch files; `homeworkProblemNavStatus.ts` (`homeworkThreeVarProblemCreditStatus` exported); `guidedPracticeHomeworkActivity.ts` (three-var excluded from auto-advance helper); `useGuidedPracticeHomeworkAttempt.ts` (`resetHomeworkProblem`, resume index guard, snapshot problem id on record); `useHomeworkAutoAdvance.ts` (`enabled` flag); `GuidedPracticeHomeworkView.tsx`, `GuidedPracticeHomeworkWorkspace.tsx`, `HomeworkThreeVarFinishModal.tsx`, `useHomeworkThreeVarFinish.ts`, `UnguidedPracticeProblemNav.tsx`, `guided-practice.css` (pulse animation), `frameCatalog.ts`. Guided-practice tests **37/37**; frame-gallery **54/54** last run.

**Still noisy in gallery:** default notation trigger position may overlap keypad on many frames (~22 flagged); Chase adjusts in Edit layout.

**Not verified by agent in real student UI:** notation anchor after final clamp; homework finish modal end-to-end; yellow vs red strip after partial credit (logic matches tests).

## Open questions and constraints

- **Similar problem** button is disabled ("coming soon"); no backend yet.
- Chase may still see **yellow then red** on strip if saved events differ from what he expects; if it persists after refresh, inspect `eventsByProblem` for that problem id and `firstAnswerPerSlot` per slot (`setup-rref-matrix`, `solution-type-homework`, `solution`).
- Rules unchanged: no GUI/browser without ask; no Netlify unless explicit; no em dashes; modals no backdrop dismiss; no commit/push unless pull/end-of-session.
- This chat is **context-heavy**; prefer fresh task for unrelated work.

## Read first

- `agent docs/momentum-handoffs/latest.md` (this file) then app rows in `agent docs/INDEX.md` for homework / frame gallery if extending.
- `School Scrips/student-portal/AGENTS.md` for portal dev URL and gallery gate.

## Exact next step

Refresh the homework at `http://127.0.0.1:5340` (or Teacher Console preview). On problem 4, finish with **partial credit** (miss one part on first try): confirm strip stays **yellow**, modal appears, problem number **pulses**, **Redo** restarts problem 4, clicking **4** on the strip **stays** on 4. Then complete problem 4 and move to 5; confirm no half-second **parametric** prompt flash on first RREF step. If anything fails, fix that path before new features.
