# Momentum handoff: 11.2 Homework Matrix (parametric, 3-var, layout, UI polish)

**Written:** 2026-10-23. Valid for today's continuation only.
**Nothing is committed or pushed.** Dirty work spans `School Scrips/Matrix app`, `School Scrips/student-portal`, and `Programs/` (agent docs). Commit only on "pull", "put on GitHub", or end of session.

## Objective and current phase

Chase is polishing **11.2 Homework** in the student portal (Matrix embed): infinite-solution **2-var** parametric recovery, **three-variable** homework problems (RREF → solution type → answer), layout preview for animation/check positions, and button press feedback.

**Phase:** Most recent work is **implemented and headless-green**; Chase has **portal-verified** layout-preview drag and button click feedback, but not re-checked every animation/layout tweak from this long session. No Netlify deploy unless explicitly asked.

## Chase's desired feel

- Review in **student portal** only for student-facing UI (hard refresh Ctrl+Shift+R after changes).
- **Plain drag** for layout preview (no dwell hooks). Grab anywhere on the animation block; Save persists offset.
- Animations match **Factoring Guided Practice** solve-board house style: gold op under both sides, **one red diagonal** cancel through `3t` and `- 3t` (negative slope), answers in **yellow boxes** side by side (`x = …` then `y = t`). **No loop**; Replay only.
- Buttons must **look clickable** and **animate press** on dwell click (global Web Animations helper).
- Solution-type MCQ: **Exactly one solution** / **Infinitely many solutions** / **No solution** (not "ordered triple" on the choice row).
- After correct **RREF** on 3-var homework, keep the **student's reduced matrix** on the left (replaces original system), not augmented initial form.
- Correct **solution type** choice gets **green check flash** like RREF before advancing.
- Parametric step prompt: **Enter the solution in parametric form. Let z = t.** (dynamic free variable from answer key; all current 3-var parametric problems use **z = t**).

## Accepted decisions

**2-var parametric wrong-answer reveal (`DynamicParametricSolveAnimation.tsx`, `GuidedPracticeParametricSolveReveal.tsx`):**

- Pacing: `PARAMETRIC_SPEEDUP = 1.15` on step/hold/fade constants.
- Sequence: equation + `y = t` beside it → y→t swap → gold ops under `3t` and `2` → single measured **CancelLine** → fade ops → `x` answer box, then `y = t` box **beside** x.
- Layout preview: pointer-capture drag, scale-aware, `PARAMETRIC_REVEAL_LAYOUT_KEY`; Reset via portal banner + `useGuidedPracticeLayoutPreview` `layoutResetToken`.
- Wrong solution entry **kept** on first wrong (not cleared).

**Portal / Matrix shared UI:**

- `buttonClickFeedback.ts` installed in `student-portal/src/main.tsx` and `Matrix app/src/main.tsx`. Banner buttons restyled in `guided-practice.css`.
- `pressable-buttons.md` extended with dwell-proof animation section; recipes INDEX row for Factoring solve-board cancel pattern.

**Three-var homework (`ThreeVarHomeworkSolver`, `use-three-var-homework-session.ts`, `use-homework-matrix-setup.ts`):**

- `onSuccess(matrix)` passes submitted RREF into `displayMatrix`; post-RREF phases show **only** reduced matrix (no duplicate augmented copy).
- `showTypeCorrectCheck` + `CORRECT_CHECK_MS` delay before solution phase.
- `parametric3EntryPrompt()` in `parametric.ts` for step-3 overlay text.

**Solution-type labels (`solution-type-labels.ts`):**

- Single source for MCQ copy in `HomeworkThreeVarSolutionTypePanel`, `GuidedPracticeSolutionTypePanel`, and wrong-answer reveal hint in `use-three-var-homework-session`.

## Rejected / do not rediscover

- **Dwell-based drag** for layout preview (Chase wants Word-style pointer drag).
- **`:active` only** for click feedback (invisible on dwell).
- **Separate `y = t` row** below equation in parametric animation (must be beside equation, then beside answer boxes).
- **Two red strikes** for cancel (Chase wanted **one** diagonal through both terms; may still want spacing tweaks).
- **Auto-loop** on parametric solve animation.
- **"Saved!"** toast after layout Save (no-ephemeral-feedback still applies).
- Revert **`GJ_HOMEWORK_MODE_CHOICE_TEMP_PREVIEW_IMMEDIATE`** before student ship when mode-choice thread is done (from earlier homework work).

## Current implementation state

**Matrix app (high-signal paths):**

- `DynamicParametricSolveAnimation.tsx` — full solve walkthrough; tests in `guided-practice-infinite-solution.test.tsx`, `parametric-reveal-layout-drag.test.tsx`, `button-click-feedback.test.ts`.
- `GuidedPracticeParametricSolveReveal.tsx`, `layoutPreviewOffsetGuard.ts`, `helpTriggerLayoutPosition.ts` (`PARAMETRIC_REVEAL_LAYOUT_KEY`).
- `use-three-var-homework-session.ts`, `ThreeVarHomeworkSolver.tsx`, `HomeworkThreeVarSolutionTypePanel.tsx`.
- `solution-type-labels.ts`, `three-var-homework-questions.ts`, `parametric.ts` (`parametric3EntryPrompt`, `parametric3FreeVariable`).
- `GuidedPracticeSolver.tsx` still **~793 lines** (cap 800); do not grow without extract.

**Student portal:**

- `GuidedPracticeCheckLayoutBannerControls.tsx` (Layout preview / Save / Reset).
- `GuidedPracticeHomeworkView.tsx` / `GuidedPracticeView.tsx` — `checkResetToken`, layout banner wiring.
- `main.tsx` — `installButtonClickFeedback()`.

**Verification (agent):** Vitest green on infinite-solution, three-var questions, parametric reveal, layout drag, button feedback, unguided solver. **Not** full portal visual pass on latest cancel-line geometry or 3-var check placement.

## Open questions and constraints

- Layout preview **placeholder** box for animation may still be taller than the shortened 3-row animation; shrink preview box if Chase cares.
- **Check mark** position for 3-var solution-type step is beside matrix (not layout-preview slot yet); may need `GuidedPracticeCorrectCheckSlot` parity with 2-var guided practice.
- Animation timing still tunable via `PARAMETRIC_SPEEDUP` only.
- Parallel older handoff topics (mode choice after problem 2, MCQ `y: -12`) may still matter; confirm with Chase which homework path is active (problem 2 infinite vs problem 4+ three-var).

## Read first

1. This file.
2. `School Scrips/Matrix app/src/app/components/guided-practice/DynamicParametricSolveAnimation.tsx` (animation exemplar).
3. Factoring reference: `School Scrips/Factoring Guided Practice/src/app/hooks/useRootsRevealWalkthrough.ts`, `FactoringSolveBoard.tsx`.
4. Three-var flow: `use-three-var-homework-session.ts`, `ThreeVarHomeworkSolver.tsx`.
5. Labels: `solution-type-labels.ts`.
6. Layout preview: `useGuidedPracticeLayoutPreview.ts`, `GuidedPracticeParametricSolveReveal.tsx`.

## Exact next step

Hard refresh portal. On **11.2 Homework problem 4** (three-var): complete RREF, confirm **reduced matrix stays** on step 2, pick **Exactly one solution** / **Infinitely many** / **No solution** and confirm **check flash**, then read parametric prompt (**Let z = t** on parametric problems). Separately on **problem 2** (infinite): wrong parametric twice, confirm animation cancel line and side-by-side yellow answers; use **Layout preview** if animation position still needs Save. Report any misaligned gold ops or cancel line only (numbers for nudge).
