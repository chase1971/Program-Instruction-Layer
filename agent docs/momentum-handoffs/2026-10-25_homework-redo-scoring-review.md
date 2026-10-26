# Momentum handoff: 11.2 homework redo, 17-point scoring, grade screen, test buttons, solved recap

**Written:** 2026-10-25 (evening). Valid for today's continuation only.
**Nothing is committed or pushed.** No Netlify deploy was run. Chase has **not** yet walked through any of this in the live portal; everything below is headless-verified only.

Still live from the earlier same-day handoff (`2026-10-25_homework-gallery-finish-flow.md`): the frame gallery overlap work and notation help anchor. This handoff covers only the homework behavior changes made after it.

## Objective and current phase

Polishing **11.2 Homework** (Gauss-Jordan method, six problems) in the student portal (`School Scrips/student-portal`) and the Matrix app solvers it imports (`School Scrips/Matrix app`, alias `@matrix/app/...`). Phase: all requested changes are coded and unit-tested; waiting on Chase to click through them.

## Chase's desired feel

- A student must never be stuck on a screen with no way out. After any wrong answer there is always a clear next step.
- Redoing a problem means a **different problem of the same solution type** (exactly one, infinitely many, none). Never the same problem, never a stale answer pre-selected.
- Strip colours must be truthful: green full credit, yellow partial, red none.
- Grading is **17 points**: problems 1-3 are 3 points each (all or nothing at 70% first-try), problems 4-6 are 1 point per scored step (3, or 2 for the no-solution problem). "Full credit" wording only at 17/17.
- Grade screen copy is plain: no "Keep practicing!", no "you missed N", just the score and percent.
- "Give answer" (tester cheat) should be a one-button way to keep moving: first click shows and types the answer, second click presses Enter/Next/Submit.
- Small buttons for cheats (like the Logic app's margin teleports). Head-mouse user: no typing flows, no tiny targets, modals never close on backdrop click.
- Problem 3 (practice mode, ordered pair only): out of tries means redo via guided practice, no bypass.
- Row notation: a wrong first try keeps what was typed on the number pad.
- Reopening a problem with full credit shows a recap, not the solver.

## Accepted decisions (all built)

**Finish flow, problems 4-6** (`useHomeworkThreeVarFinish.ts`, `HomeworkThreeVarFinishModal.tsx`)
- Modal buttons: "Try a similar problem" and "Come back later" (becomes "Continue" when no open problems remain, leading to survey then grade). "Redo this problem" was removed.
- Completion is deferred with a pending-state plus effect, because `onComplete` fires in the same tick as the last `recordEvent` (stale-closure race that caused the earlier stuck screen). Green advances immediately (no hold lag).
- `replaceHomeworkProblemWithSimilar` swaps the id for a same-kind id, excluding ids already in the attempt, and deletes that problem's events/step index/solve mode.
- `wrongTypeChoice` restore only when the type is still unanswered (Matrix `three-var-homework-resume-state.ts`).

**Scoring** (`guidedPracticeHomeworkActivity.ts`): `homeworkProblemPoints`, `scoreHomeworkProblems`, `HOMEWORK_GUIDED_BLOCK_POINTS = 3`; `homeworkScoringSlots` drops the automatic `solution` slot on no-solution 3x3 problems. Tests assert perfect 17/17 passed, one miss 16, 94%, not passed.

**Redo missed problems from grade screen**: `homeworkRedoMissed.ts` (`missedThreeVarIndexes`, `buildRedoMissedProgress`), `startRedoMissedHomework` in the attempt hook (new attempt row, kept problems keep events). Button "Redo missed problems" via `extraActionLabel`/`onExtraAction` on `TransformationsResult`. `advanceToNextProblem` skips complete problems. Only problems 4-6 can be redone this way.

**Give answer, two stage**: `use-guided-practice-admin-give-answer.ts` (new), `use-homework-matrix-setup.ts`, `use-three-var-homework-session.ts`, `UnguidedPracticeSolver.tsx`, wired through `use-guided-practice-session.ts`.

**Grade screen copy** (`guidedPracticeHomeworkResultCopy.ts`, `GuidedPracticeHomeworkResult.tsx`, `TransformationsResult.tsx`): `heading={null}` hides the tier title; `scoreLine` = "You got 16 out of 17 correct (94%)."; message when not perfect = "You may keep this score, or redo the missed problems to earn a higher grade." Perfect keeps the full credit message. Confetti tier logic untouched (confetti at 70%+, storm and rain below 70).

**Home page test buttons** (`homeworkGuidedPctTest.ts`, `useHomeworkGuidedPctTest.ts`, `GuidedPracticeHomeworkHomePanel.tsx`): two margin buttons "Guided <70%" and "Guided 73%", only when `hasAdminCheats()`. Each starts a fresh homework and opens problem 1 with every step answered except the last, scored so the final correct answer lands just under or over 70%. Chase said he would do the problem 3 case himself.

**Problem 3 practice-mode miss** (`homeworkSolveMode.ts`, `HomeworkGuidedRetryModal.tsx`, attempt hook `restartHomeworkProblemGuided`): `homeworkProblemFinishedForAdvance` now means a correct last step only (a wrong answer no longer auto-advances). `homeworkSolutionOnlyExhausted` (three wrong on the last slot, no correct) shows a no-backdrop modal "Try number N again through the guided practice process." with one Okay button. Okay swaps problem 3 for a **different unique-solution problem** (random from the bank, excluding ids in the attempt), clears its events, switches it to guided, and opens it.

**Row notation pad** (`use-guided-practice-row-notation-recovery.ts`): first wrong submit reopens the pad with `setBuilderExpression(trimmed)` instead of clearing it. Matrix row-entry cells already kept their draft.

**Solved recap** (`HomeworkSolvedReview.tsx`, `homeworkSolvedSummary.ts`, `useHomeworkStripState.ts`, workspace `reviewMode`): clicking a **green** problem on the strip shows Original system, an arrow, Row reduced, an arrow, then the solution (pair, parametric pair, triple, three parametric lines, or "No solution"). Strip stays visible. Yellow/red problems and the Resume button still open the solver. `reviewProblemId` state in the View is cleared by `openProblem`. Problems 1-3 count as green at 70%+, not only perfect.

**Strip colours**: three-class `:disabled` overrides in `guided-practice.css` so `--active/--green/--yellow/--red` keep colour on disabled buttons; removed the stale `initialEvents` merge in the strip memo.

## Rejected directions

- "Redo this problem" (same problem, same type pre-selected): rejected, you cannot redo a problem; redo means a similar one.
- Old per-step score ("36 out of 39", "full credit" for anything): replaced by the 17-point scheme.
- Auto-advance after any answer on the practice-mode last step: rejected, it advanced on wrong answers and skipped the guided-retry requirement.
- Same problem 3 on the guided retry: rejected, must be a different problem.
- New `.cursor/rules/*.mdc` or new pattern docs: retired / not wanted.

## Current implementation state

Uncommitted in **student-portal** (all under `src/features/guided-practice/` unless noted): `GuidedPracticeHomeworkHomePanel`, `GuidedPracticeHomeworkResult`, `GuidedPracticeHomeworkView`, `GuidedPracticeHomeworkWorkspace`, `guidedPracticeHomeworkActivity(.test)`, `guidedPracticeHomeworkResultCopy`, `homeworkSolveMode`, `useGuidedPracticeHomeworkAttempt`, `useHomeworkAutoAdvance`, `homeworkProblemNavStatus(.test)`, `../transformations/TransformationsResult.tsx`, `../../styles/guided-practice.css`, `../../types/matrix-app.d.ts`; new files `HomeworkGuidedRetryModal.tsx`, `HomeworkSolvedReview.tsx`, `HomeworkThreeVarFinishModal.tsx`, `homeworkGuidedPctTest(.test).ts`, `homeworkProgress.ts`, `homeworkRedoMissed(.test).ts`, `homeworkSolvedSummary(.test).ts`, `useHomeworkGuidedPctTest.ts`, `useHomeworkStripState.ts`, `useHomeworkThreeVarFinish(.test).ts`. Plus frame-gallery files from the earlier handoff.

Uncommitted in **Matrix app**: `use-guided-practice-row-notation-recovery.ts`, `use-homework-matrix-setup.ts`, `use-three-var-homework-session.ts`, `use-guided-practice-session.ts`, `UnguidedPracticeSolver.tsx`, `three-var-homework-resume-state.ts`, new `use-guided-practice-admin-give-answer.ts`, plus earlier-handoff files.

Verification: portal `npx vitest run src/features/guided-practice src/features/frame-gallery src/features/transformations` green (last full guided-practice run 13 files, 49 tests); Matrix `npx vitest run` 53 files, 265 tests green (run after the notation-pad change). Portal `tsc` still reports **pre-existing** noise: missing `@matrix/app/...` module stubs in `src/types/matrix-app.d.ts`, `solutionOnlyActive` unused and an arg-count error in `GuidedPracticeHomeworkView.tsx`, `Workspace` unused vars. None were introduced by this work; Vitest resolves the alias fine.

File sizes: `GuidedPracticeHomeworkView.tsx` is **702** lines (over the 700 extract mark, under the 800 cap); `useGuidedPracticeHomeworkAttempt.ts` 639; Matrix `use-guided-practice-session.ts` about **748** (over 700, only minimal wiring added). Extract before adding to any of these.

## Open questions and constraints

- Should clicking a **yellow or red** problem on the strip re-offer the finish modal ("Try a similar problem")? Today "Come back later" then clicking N reopens the old finished state with no way to ask for a similar problem. Redo missed problems on the grade screen is the clean path. Proposal only, not approved.
- Confetti below 70% still shows storm and rain; Chase has not said whether to remove it.
- Recap threshold for problems 1-3 is 70%+; Chase may prefer perfect-only.
- The give-answer and test-button behavior depends on `hasAdminCheats()`; verify with the CHASE1 cheat account.
- Root rules: never launch a GUI or open a browser without asking; handoffs to Chase are statements, not prompts; no em dashes; modals never dismiss on backdrop; small buttons; no commit/push/deploy unless he says so.

## Exact next step

Hand Chase a short live test list as a statement (do not launch anything): (1) home page "Guided <70%" and "Guided 73%" buttons, then click Give answer on the last step and confirm red/locked vs green/advance; (2) finish 4-6 with a miss, press Redo missed problems on the grade screen, confirm similar problems and kept greens; (3) problem 3 practice mode, miss three times, confirm the guided-retry popup and a different problem; (4) click a green problem on the strip and confirm the three-part recap; (5) wrong row notation keeps text on the pad. Then fix whatever he reports, starting with the open strip-click question if he wants it.
