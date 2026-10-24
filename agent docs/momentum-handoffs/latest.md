# Momentum handoff: 11.2 Homework + frame gallery (Gauss-Jordan)

**Written:** 2026-10-24. Valid for today's continuation only.
**Nothing is committed or pushed** unless Chase says pull / put on GitHub / end of session.

## Objective and current phase

Ship **11.2 Homework** and the **frame gallery** dev preview so students get Pearson-style **three tries** on homework practice steps, correct **resume/advance/scoring**, and gallery frames that match what the live app actually shows.

**Phase:** Code and headless tests are largely in place. Chase has **not** done a full portal walkthrough of every fix in this handoff. **Supabase/Netlify deploy** is explicitly out of scope until he asks.

## Chase's desired feel

- Review in the **student portal** (and frame gallery locally), not raw MP4s or Matrix-only runs unless headless.
- **Problem 3 mode choice:** after problem 2, **walked-through steps** vs **"Just right or wrong"** — tap choice, no Continue button.
- **Just right or wrong** is **not** skipping to the pair only. It is the **same three-question shape as homework 4–6** but **2×2**: **augmented matrix → RREF → ordered pair**, each with **three attempts** (soft retry, then "One try left.", then reveal + Next).
- **Guided problem 3** stays the full Gauss–Jordan step flow; that path was already acceptable.
- **No-solution 3×3 homework** finishes after **"No solution"** on Q2; there is **no student Q3 screen**. The frame gallery must **not** invent interactive **P313.Q3** frames (that created stuck/impossible previews).
- Frame gallery: **W1 / W2 (one try left) / W3 (reveal)** for homework-practice question kinds; exit checker must not mark W2 stuck when the student can still retry.

## Accepted decisions

| Area | Decision |
|------|----------|
| Homework retries | `HOMEWORK_PRACTICE_MAX_ATTEMPTS = 3` in `homework-practice-retry.ts`; gallery reveal on **W3** for 3-try kinds, **W2** for 2-try guided kinds (e.g. operation-type). |
| Frame gallery 3×3 tabs | **P301, P305, P313** (not P101); `ThreeVarHomeworkSolver` in gallery with seed/resume hooks. |
| P313 Q3 in gallery | **Omit** `solution-none` question frames; catalog comment documents why. |
| Three-var **resume** | `buildThreeVarHomeworkResumeState` + workspace passes `initialQuestionIndex` / `initialSessionEvents` into `ThreeVarHomeworkSolver`. |
| Homework attempt **advance** | `advanceToNextProblem` **awaits save** before `applyProgress` updates UI index. |
| Solution-only **scoring** | Record **wrong** `(x,y)` attempts on `onDraftChange`; first-try credit uses first event per slot. |
| Solution-only **flow** | `prependSystemSetup` **on**; matrix answers recorded via `onRecordMatrixAnswer` → `onSessionEvent`; `homeworkSolutionOnlySessionResume` for augmented/RREF/solution resume. |
| Notation help (gallery) | Baked stage coords for row-scaling/replacement help; tests in Matrix app + portal FrameSolver. |

## Rejected directions (do not redo)

- **Skipping** augmented/RREF for "Just right or wrong" (briefly shipped; Chase corrected — restore 3-step flow).
- **Adding Submit-only Q3** for no-solution 3×3 as a fake student step when live flow completes on Q2.
- **Keeping P313.Q3 gallery tabs** that nothing in live homework can reach without cheating the flow.
- Treating frame gallery **W2** as "must have Next" for homework kinds still on soft retry (fixed via `galleryRevealWrongCountForQuestionKind`).

## Current implementation state

### Student portal (`School Scrips/student-portal`)

- **Frame gallery:** `frameCatalog.ts`, `frameExits.ts`, `frameGalleryProblemIds.ts`, `FrameSolver.tsx`, tests (exits, transitions, catalog, overlaps/bot if present).
- **Homework:** `GuidedPracticeHomeworkWorkspace.tsx`, `useGuidedPracticeHomeworkAttempt.ts`, `homeworkSolveMode.ts` (+ `.test.ts`), `guidedPracticeHomeworkActivity.test.ts`.

### Matrix app (`School Scrips/Matrix app`)

- `homework-practice-retry.ts` (3-try helpers + gallery reveal count).
- `three-var-homework-frame-gallery-seed.ts`, `three-var-homework-resume-state.ts` (+ tests).
- `use-three-var-homework-session.ts`, `ThreeVarHomeworkSolver`, `UnguidedPracticeSolver`, `use-homework-matrix-setup.ts` (phases + resume seeds + matrix answer recording).
- Notation help / help trigger fixes for gallery.

### Programs root

- `agent docs/momentum-handoffs/*`, session tracking bumps, possible recipe/scratch files dirty.

### Verification (agent-run, not Chase portal)

- `npx vitest run src/features/frame-gallery` — passed (48 tests) after 3-try + P313 omit.
- Matrix: `three-var-homework-resume-state.test.ts`, `unguided-practice-solver.test.tsx` (incl. homeworkPracticeFlow 3 tries).
- Portal: `homeworkSolveMode.test.ts`, `guidedPracticeHomeworkActivity.test.ts`.

## Open questions and constraints

1. **`GJ_HOMEWORK_MODE_CHOICE_TEMP_PREVIEW_IMMEDIATE`** — still may be `true` for admin preview on Start; **revert to `false`** before student-facing ship (see `2026-10-23_gj-homework-practice-mode-choice.md`).
2. **Portal confirm** Chase wanted before students: problem **4–6 resume**, solution-only **first-try credit**, **advance on save failure**, problem **3 right-or-wrong** three steps × three tries, frame gallery stuck badges.
3. **No Netlify deploy** unless Chase says so in the same message.
4. **GuidedPracticeSolver.tsx** may still be over 500 lines — extract before large adds (older constraint).

## Read first (fresh task)

1. This file.
2. `School Scrips/student-portal/src/features/guided-practice/GuidedPracticeHomeworkView.tsx` (mode choice, resume open).
3. `School Scrips/student-portal/src/features/guided-practice/GuidedPracticeHomeworkWorkspace.tsx` (three branches: guided / solution-only / three-var).
4. `School Scrips/student-portal/src/features/guided-practice/homeworkSolveMode.ts`.
5. `School Scrips/Matrix app/src/app/engine/homework-practice-retry.ts`.
6. Frame gallery: `student-portal/src/features/frame-gallery/frameCatalog.ts`, `frameExits.ts`.

## Exact next step

In the **student portal** (admin cheats OK): finish **problem 2** guided → mode modal → **Just right or wrong** on **problem 3**. Confirm **augmented → RREF → (x,y)** with **three** wrong submits on each step before reveal. **Resume** mid-RREF and confirm reopen on step 2. Then spot-check **P301** frame gallery for **W2 "one try left"** and no stuck thumbs on homework W2. If anything fails, fix in the listed files and re-run `npx vitest run src/features/frame-gallery` and portal `homeworkSolveMode.test.ts`.
