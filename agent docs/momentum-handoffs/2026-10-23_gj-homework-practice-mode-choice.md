# Momentum handoff: 11.2 Homework mid-mode choice + practice mode

**Written:** 2026-10-23. Valid for today's continuation only.
**Nothing is committed or pushed.** Dirty repos include `School Scrips/student-portal`, `School Scrips/Matrix app`, and earlier session work under `Programs/` root and other School Scrips apps. Commit only on "pull", "put on GitHub", or end of session.

## Objective and phase

Chase is shipping **11.2 Homework** (Gauss-Jordan in the student portal): prior UX polish (help, resume, infinite-solution MCQ, layout preview) **plus** a **mid-homework mode choice** after problem 2 (or on Start for admin temp preview): **walked through each step** vs **just right or wrong** (same unguided practice as Gauss-Jordan Method Practice).

Phase: **portal verify** that choosing **Just right or wrong** actually opens **`UnguidedPracticeSolver`** (matrix + ordered pair, two tries), not guided steps. Then revert temp flags before students see it.

## Chase's desired feel

- Review in **student portal only**. No GUI launch or Netlify unless he asks in the same message.
- Mode prompt: **one left-aligned paragraph** (main question + "You can switch back later if you change your mind" in the same flow). **No** "Pick one to continue." **No Continue button** — tap a choice and go straight to the problem.
- **Just right or wrong** must feel like **practice mode**: type `(x, y)`, submit, correct / try again. Not guided MCQ steps.
- Factoring Guided Practice remains the reference for other MCQ rows (numbered, tap to answer).
- Instruction box rules from earlier polish still apply: **shrink = width only**, not moving `left`.

## Accepted decisions

- **When choice applies (production):** After **problem 2** is finished (`GJ_HOMEWORK_MODE_CHOICE_AFTER_PROBLEMS = 2`), show modal **before problem 3** opens. Homework has **3 problems**; only problem 3 gets the chosen mode in normal flow.
- **Problem 1 is always infinite-solution** (`HOMEWORK_INFINITE_SOLUTION_PROBLEM_NUMBER = 1`). Practice mode **cannot** run there (no single `(x, y)`). **`homeworkEffectiveSolveMode`** forces **guided** when there is no unique solution.
- **Solution-only UI:** `GuidedPracticeHomeworkWorkspace` branches to **`UnguidedPracticeSolver`** when mode is `solution_only` and `homeworkUniqueSolution(problemId)` is set. Outcomes recorded via `createHomeworkSolutionOnlyAnswerEvent` / `recordHomeworkSolutionOnlyOutcome(problemId, ...)`.
- **Progress:** `solveModeByProblem` on homework progress blob; scoring/advance use `homeworkSolveMode.ts` helpers.
- **Admin temp preview:** `GJ_HOMEWORK_MODE_CHOICE_TEMP_PREVIEW_IMMEDIATE = true` shows the modal on **Start/Resume** (with admin cheats). If user picks **right_or_wrong** while pending problem 1 would open, **jump to problem 3** (`homeworkPracticeModePreviewProblemId`) so Chase can test practice mode without doing problems 1–2. **`focusHomeworkProblem`** syncs `currentIndex`.
- **`solveModeOverride`** in `GuidedPracticeHomeworkView` avoids one-frame guided flash before persisted mode applies.
- Mode choice UI: `GuidedPracticeHomeworkModeChoice` — `onChoose`, class `gp-homework-mode-choice` for left-aligned prompt.

## Rejected / corrected (do not rediscover)

- **Do not** expect practice mode on **homework problem 1** — infinite system by design.
- **Do not** re-add **Continue** or centered two-line hint on the mode modal.
- **Do not** fix "shrink box" by shifting **`left`** on row-notation popovers (width trim only).
- **Do not** re-add **Submit** on solution-type MCQ.
- Dev **HMR** on Matrix `.tsx` may reset homework to home; use **Resume** after reload.

## Current implementation state

**Student portal (mode choice + practice — this thread):**

- `guidedPracticeHomeworkSurveyCopy.ts` — mode copy; **`GJ_HOMEWORK_MODE_CHOICE_TEMP_PREVIEW_IMMEDIATE = true`** (revert before ship).
- `GuidedPracticeHomeworkModeChoice.tsx`, `GuidedPracticeHomeworkView.tsx`, `GuidedPracticeHomeworkWorkspace.tsx`.
- `homeworkSolveMode.ts` (new), `useGuidedPracticeHomeworkAttempt.ts` (`setHomeworkSolveModeForProblem`, `focusHomeworkProblem`, `solveModeForProblem`, `recordHomeworkSolutionOnlyOutcome`).
- `useGuidedPracticeHomeworkCloseout.ts`, `useHomeworkAutoAdvance.ts`, `guidedPracticeHomeworkActivity.ts` — advance/scoring aware of mode.
- `guided-practice.css` — `.gp-homework-mode-choice` left align, wider card.
- **Build + `guidedPracticeHomework` vitest:** passing (last run this session).

**Still not done:**

- **"Switch back later"** is copy only — no in-assignment mode toggle UI.
- **Revert** `GJ_HOMEWORK_MODE_CHOICE_TEMP_PREVIEW_IMMEDIATE` to `false` before student-facing ship.
- Chase **portal confirm** that after **Just right or wrong** he sees unguided solver on **problem 3** (temp preview or after finishing 1–2).

**Matrix app + earlier homework polish (prior handoff, still dirty):**

- `GuidedPracticeSolver.tsx` (~760+ lines — **extract before big adds**).
- Solution-type panel, parametric help shell (MP4 placeholder), layout preview, resume `stepIndexByProblem`, row-notation width trim, fraction help placement.
- Headless tests on infinite-solution / wrong-recovery / layout offsets were green in prior work.

## Open questions and constraints

- After reload, confirm **no guided flash** on problem 3 when mode was saved as solution-only.
- Infinite-solution **problem 1** stays guided even if student somehow had solution_only stored for that id (effective mode guard).
- `GuidedPracticeSolver.tsx` file size: extract before more Matrix features.

## Read first

1. This file.
2. `School Scrips/student-portal/src/features/guided-practice/GuidedPracticeHomeworkView.tsx` (mode modal, `dismissModeChoice`, preview jump).
3. `School Scrips/student-portal/src/features/guided-practice/homeworkSolveMode.ts`.
4. `School Scrips/student-portal/src/features/guided-practice/GuidedPracticeHomeworkWorkspace.tsx`.
5. For polish regressions: `useGuidedPracticeHomeworkAttempt.ts`, Matrix `GuidedPracticeSolver.tsx` (grep, do not read whole file).

## Exact next step

In the portal with **admin cheats**, open **11.2 Homework**, **Start** → tap **Just right or wrong** (no Continue). Expect **problem 3 of 3** with **unguided** entry (not step-by-step). Submit a pair and confirm correct/try-again feedback. If still guided, trace `workingSolveMode` / `homeworkEffectiveSolveMode` on `workingProblemId` in the workspace. When satisfied, set **`GJ_HOMEWORK_MODE_CHOICE_TEMP_PREVIEW_IMMEDIATE = false`** and verify production path: finish problems **1 and 2** guided → modal → problem **3** practice.
