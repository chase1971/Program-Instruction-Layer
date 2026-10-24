# Momentum handoff — 11.2 Gauss-Jordan homework (three-var + practice retries)

**Written:** 2026-10-23

## Objective and current phase

Chase is shipping **11.2 Homework** in the student portal (Matrix embed): six problems (1–3 guided 2×2, 4–6 three-variable calculator-RREF flow). This chat finished UX, validation, and Pearson-style retries on **practice-style** steps. **Not deployed to Netlify** unless Chase asks. Verify in portal with hard refresh after local Matrix + portal builds.

## Chase's desired feel

- Head-mouse / dwell: no mystery dead ends after wrong tries; number pad stays usable.
- **Calculator RREF** means full reduction on the **whole augmented matrix** (pivot in constant column clears entries above it).
- **No-solution** systems: no extra "confirm" step; say correct and move on.
- **Parametric triple:** `t` prefilled in the free variable (usually z); only type x and y; minus appends in parametric mode; Submit on y.
- Finishing problem 6: **no** "matrix is in RREF" modal; brief hold then survey (once) or grade screen. **Admin:** skip survey entirely.
- Practice homework steps: **three tries**, then show answer + **Next** (never auto-advance past reveal). Guided problems 1–3 unchanged.

## Accepted decisions

| Area | Decision |
|---|---|
| RREF validation | `gauss-jordan.ts` loops all columns including augmented (`colCount`), not `colCount - 1`. Problem 317 expects `[1,0,1,0; 0,1,1,0; 0,0,0,1]`. |
| First wrong RREF | `use-homework-matrix-setup.ts`: keep draft, focus cell 0, builder open (`reopenMatrixBuilderOnFirstCell`). |
| None (problem 6) | Choosing **No solution** on type step finishes problem (records solution slot, `THREE_VAR_NONE_TYPE_SUCCESS_PROMPT`). No third confirm button. |
| Last problem closeout | Removed `GuidedPracticeHomeworkCompleteCard` overlay; `GuidedPracticeHomeworkView` auto `continueFromLastProblem` after hold for all modes. |
| Parametric minus | `use-three-var-homework-session` uses `appendParametricBuilderToken` (not sign-toggle). |
| Parametric UX | `initialTripleDraftForSolution` prefills `t`; commit on y submits with free var; `solutionBuilderSubmitLabel` Next on x, Submit on y/z. |
| Admin nav (3-var) | `adminGoBack` / `adminSubmitCorrectSolution`; workspace wires Back/Next for three-var step index. |
| Admin survey | `useGuidedPracticeHomeworkCloseout`: `hasAdminCheats()` → `finishHomework()` + result, skip survey. |
| Practice retries | Shared `homework-practice-retry.ts`: 3 attempts, messages on 1 and 2, reveal on 3. Used in matrix entry, three-var type/solution, unguided 2×2. Overlay `homeworkPracticeReveal` with **Next** in prompt. |

## Rejected directions

- Treating partial RREF (constants 2,3,1 with `[0,0,0|1]` bottom row) as correct: wrong for calculator RREF on full augmented matrix.
- Closing builder and clearing focus on first wrong RREF try.
- Separate "Confirm no solution" step and last-problem Continue modal copy about RREF.
- Two-try only on practice mode (expanded to three to match Pearson ask).
- Auto-advancing immediately after answer reveal without **Next**.

## Current implementation state (uncommitted)

**Repos with dirty work:** `School Scrips/Matrix app`, `School Scrips/student-portal`

**Matrix app (high signal paths):**

- `src/app/engine/gauss-jordan.ts` — full augmented RREF
- `src/app/engine/homework-practice-retry.ts` — new
- `src/app/hooks/use-homework-matrix-setup.ts` — 3-try + first-wrong reopen
- `src/app/hooks/use-three-var-homework-session.ts` — none-on-type, parametric, 3-try reveal, admin skip/back (~600+ lines; watch cap)
- `src/app/components/guided-practice/ThreeVarHomeworkSolver.tsx`, `GuidedPracticeOverlay.tsx`, `UnguidedPracticeSolver.tsx`
- Tests: `three-var-homework-*`, `homework-practice-retry`, `three-var-none-flow`, `three-var-parametric-solution-entry`, `append-parametric-builder-token`, `unguided-practice-solver` (updated for 3 tries)

**Student portal:**

- `GuidedPracticeHomeworkWorkspace.tsx` — three-var snapshot, no complete card, admin back
- `GuidedPracticeHomeworkView.tsx` — auto closeout all modes
- `useGuidedPracticeHomeworkCloseout.ts` — admin skips survey
- `src/types/matrix-app.d.ts` — `ThreeVarHomeworkSolverHandle` adminBack

**Verification:** Matrix app vitest passed for retry, unguided, three-var tests run in session. No Netlify deploy. Chase should portal-smoke: problem 4 parametric (3 wrong → answer + Next), problem 6 none + full RREF, admin finish without survey.

## Open questions / constraints

- `ThreeVarHomeworkSolver` `onComplete` in workspace is still `() => undefined`; advancement is **event-driven** via `onSessionEvent` / homework complete slots. OK if last slot gets recorded (including reveal **Next** path which records `correct: true` on solution after reveal for progression).
- `GuidedPracticeHomeworkCompleteCard.tsx` still exists but is unused in workspace; safe to delete later if desired.
- `GJ_HOMEWORK_MODE_CHOICE_TEMP_PREVIEW_IMMEDIATE` and related homework mode choice flags from prior sessions: confirm before prod ship.
- File size: `use-three-var-homework-session.ts` growing; extract if adding more phases.
- Never deploy Netlify prod unless Chase says so in that message.

## Read first (fresh agent)

1. This file (date check).
2. `School Scrips/Matrix app/src/app/hooks/use-three-var-homework-session.ts`
3. `School Scrips/Matrix app/src/app/engine/homework-practice-retry.ts`
4. `School Scrips/student-portal/src/features/guided-practice/GuidedPracticeHomeworkView.tsx`
5. Bank: `School Scrips/Matrix app/src/app/engine/three-var-homework-problems.ts` (ids 301–317)

## Exact next step

Hard-refresh portal, run through **problem 4** (parametric: prefilled `t`, 3 wrong submits → answer in blue prompt + **Next** → next phase) and **problem 6** (RREF `[0,0,1]` aug column, **No solution** on type, no survey as admin). If anything fails, fix the specific phase hook before adding features. If all green and Chase wants sync: **put on GitHub** (Matrix app + student-portal repos).
