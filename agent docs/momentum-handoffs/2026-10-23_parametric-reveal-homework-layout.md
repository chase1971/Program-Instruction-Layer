# Momentum handoff: 11.2 Homework parametric reveal + layout

**Written:** 2026-10-23. Valid for today's continuation only.
**Nothing is committed or pushed.** Dirty repos include `School Scrips/Matrix app`, `School Scrips/student-portal`, and related `Programs/` root docs. Commit only on "pull", "put on GitHub", or end of session.

## Objective and current phase

Chase is shipping **11.2 Homework** in the student portal: infinite-solution systems (parametric **t**), guided wrong-answer recovery, optional **walked through** vs **just right or wrong** after problem 2, and layout polish (solution-type panel position, layout preview).

**Phase:** Headless tests are green for the latest Matrix work; **portal UI verify** is the gap. Chase reviews in the app only (no MP4 in `Manim Trial/media/`).

## Chase's desired feel

- Review in **student portal** and Matrix homework embed. No GUI launch, browser open, or Netlify unless he asks in the same message.
- **Dwell-friendly:** no backdrop-dismiss modals; small buttons; no ephemeral "Copied!" toasts.
- Parametric second wrong try: show **The answer is …** + **Next**, **no pulse** on augmented constants (2 and 0), plus a **draggable** solve animation (equation → `y = t` → substitute → subtract/strike → `x = …`) with **Play / Pause / Replay** like row-entry reveals.
- Solution-type MCQ (Infinitely many / No solution): Factoring Guided Practice pattern; panel sits **right of matrix**; raised **40px** (`y: -12` from `28`).
- Instruction box: **shrink = width only**, not moving `left`.

## Accepted decisions

**Parametric wrong-answer reveal (implemented this session):**

- `solutionConstantPulseForQuestion` returns `[]` when `expected.type === 'parametric'`; plain `(x, y)` keeps constant-column pulse.
- `getParametricRevealContext(question, workingMatrix)` in `guided-practice-parametric-reveal.ts` drives copy from reduced row `[1, a | b]` and expected parametric **x**.
- `DynamicParametricSolveAnimation` + `GuidedPracticeParametricSolveReveal` in `MovablePanel` at `{ x: 400, y: 70 }` when `solutionGiveAnswer && parametricEntry`.
- `GuidedPracticeFloatingBuilders.tsx` extracted from `GuidedPracticeSolver.tsx` (~785 lines after extract).
- Tests: `guided-practice-parametric-reveal.test.ts` (six `INFINITE_SOLUTION_PROBLEMS` + edge cases), extended `guided-practice-infinite-solution.test.tsx` (panel + Play control).

**Solution-type panel position (implemented this session):**

- `GUIDED_PRACTICE_SOLUTION_TYPE_PANEL_POSITION` and `HOMEWORK_THREE_VAR_SOLUTION_TYPE_PANEL_POSITION`: **`y: -12`** (was `28`).

**Still in flight from earlier homework work (uncommitted, see portal repo):**

- Mid-homework **mode choice** after problem 2: guided vs solution-only on problem 3; `GJ_HOMEWORK_MODE_CHOICE_TEMP_PREVIEW_IMMEDIATE = true` for admin **Start → pick mode** (revert before student ship).
- Problem **1** always guided (infinite-solution); `homeworkEffectiveSolveMode` guards unique-solution-only for practice mode.
- Parametric help tutorial wired to yellow trigger; MP4 in Matrix assets.

## Rejected / do not rediscover

- **Out of scope** for parametric reveal animation: three-variable parametric homework (problems 4–6 hint-only path); re-render Manim help video for this task.
- **Do not** pulse augmented constants on parametric give-answer.
- **Do not** fix "shrink box" by shifting **`left`** on row-notation popovers.
- **Do not** re-add **Continue** on mode choice or **Submit** on solution-type MCQ.
- Dev **HMR** may reset homework; use **Resume** after reload.

## Current implementation state

**Matrix app (key new/changed paths):**

- `GuidedPracticeSolver.tsx` — parametric reveal wiring, pulse guard, floating builders extract.
- `guided-practice-parametric-reveal.ts`, `DynamicParametricSolveAnimation.tsx`, `GuidedPracticeParametricSolveReveal.tsx`, `GuidedPracticeFloatingBuilders.tsx`.
- `guided-practice-wrong-recovery.ts` — `solutionConstantPulseForQuestion`.
- `GuidedPracticeSolutionTypePanel.tsx` — `y: -12`.
- Vitest: `guided-practice-parametric-reveal`, `guided-practice-infinite-solution`, `guided-practice-wrong-recovery` passing (last run 2026-10-23).

**Student portal:**

- Embeds Matrix guided practice; homework title **11.2 Homework**; layout preview available to admin.
- Mode choice + workspace changes dirty alongside Matrix (see prior files in `GuidedPracticeHomeworkView.tsx`, `homeworkSolveMode.ts`).

**Not verified by Chase:**

- Problem **2** (infinite): wrong parametric answer **twice** → no constant flash, animation right of popover, **Next** advances.
- Solution-type step: MCQ panel vertical position after **40px** raise.
- Mode choice → problem **3** unguided if that thread is still active.

## Open questions and constraints

- Animation panel position `{ x: 400, y: 70 }` is a guess; drag or one-number nudge after portal look.
- `GuidedPracticeSolver.tsx` still large (~785 lines); extract before major new features.
- Revert **`GJ_HOMEWORK_MODE_CHOICE_TEMP_PREVIEW_IMMEDIATE`** before student-facing ship when mode choice is confirmed.

## Read first

1. This file.
2. `School Scrips/Matrix app/src/app/hooks/guided-practice-parametric-reveal.ts` and `GuidedPracticeParametricSolveReveal.tsx`.
3. `School Scrips/Matrix app/src/app/components/guided-practice/GuidedPracticeSolutionTypePanel.tsx` (position constant).
4. For mode choice: `School Scrips/student-portal/src/features/guided-practice/GuidedPracticeHomeworkView.tsx`, `homeworkSolveMode.ts`, `GuidedPracticeHomeworkWorkspace.tsx`.

## Exact next step

In the portal, open **11.2 Homework**, problem **2**, reach **solution-type** and confirm the MCQ panel sits where Chase wants after the **40px** raise. Finish reduction, answer parametric **wrong twice**, confirm **no** highlight on augmented **2/0**, the **Parametric solve demo** panel with playback controls, and **Next** still works. If animation position is off, adjust `GUIDED_PRACTICE_PARAMETRIC_SOLVE_REVEAL_POSITION` or report direction to nudge.
