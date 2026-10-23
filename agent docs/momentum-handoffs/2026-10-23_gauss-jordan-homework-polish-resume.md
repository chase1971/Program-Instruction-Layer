# Momentum handoff: 11.2 Homework polish, resume, row-notation box

**Written:** 2026-10-23. Valid for today's continuation only.
**Nothing is committed or pushed.** Dirty repos: `School Scrips/Matrix app`, `School Scrips/student-portal`, plus earlier session work in `Programs/` root, `School Scrips/student-session-kit`, `School Scrips/Macro App`. Commit only on "pull", "put on GitHub", or end of session.

## Objective and phase

Chase is polishing **11.2 Homework** (Gauss-Jordan guided practice in the student portal): help triggers, correct-check placement, infinite-solution flow (solution-type MCQ + parametric entry), tester **Next** / **Resume**, and instruction box sizing.

Phase: **visual confirm in portal** after a batch of UX fixes. No deploy unless he asks in the same message.

## Chase's desired feel

- Review in **student portal only** (homework embed). No GUI launch or Netlify without explicit ask.
- **Factoring Guided Practice** is the UI reference for MCQ rows (numbered choices, no separate Submit).
- Yellow help: **"Need help with …? Tap or click here."** must actually show on the step (not crushed or stuck at 0,0).
- Instruction boxes: when he says **shrink** or **cut empty space on the right**, change **width only** — **do not** change `left` / anchor. When he says **move**, that is position.
- **Layout preview** + **Save** for green check and draggable help offsets when code defaults are wrong.
- **Resume** must return to the **same step**, including after tester **Next** skips (not only after correct answers).
- Number pads: **no close button** (dwell-friendly).

## Accepted decisions

- **Solution-type panel** (`GuidedPracticeSolutionTypePanel`): Factoring-style numbered rows; **tap choice to grade** (no Submit). Top line: **"Tap or click a choice to answer."** Wider card (~16rem).
- **Parametric step:** yellow trigger opens `GuidedPracticeParametricHelpPanel` (left instruction, center "Click to watch how to do this" placeholder until MP4 wired). `placement="parent"` under solution pair.
- **Row-entry multiply fractions help:** normal play uses **`placement="parent"`** in-flow under row entry; layout preview still uses viewport + anchor for drag tuning.
- **Homework resume:** `stepIndexByProblem` on progress blob + `recordQuestionIndex` on solver snapshot and before back-home; resume index = max(correct-answer slot index, saved farthest step, DB `currentIndex`). See `useGuidedPracticeHomeworkAttempt.ts` / `homeworkResumeQuestionIndex`.
- **Builder panels:** `showCloseButton` default false on horizontal/vertical value builders and row-op panel.
- **Idle row-notation** prompt ("Write the row … operation"): **`ROW_NOTATION_IDLE_POPOVER_WIDTH_TRIM = 50`** — width 350→300, **left unchanged** (`guided-practice-wrong-recovery.ts`).

## Rejected / corrected (do not rediscover)

- **Do not** fix "shrink box from the left" by adding **`popoverLeftInset`** / shifting `left` — Chase reverted that; he wanted **width trim from the right** only.
- **Do not** re-add **Submit** on solution-type MCQ.
- **Do not** viewport-portal row-entry fraction help in normal play without verifying anchor (was invisible until parent placement).
- Dev **HMR** on Matrix `.tsx` still resets homework to **home**; **Resume** after reload. CSS-only portal edits may hot-update in place.

## Current implementation state

**Matrix app (guided practice):**

- `GuidedPracticeSolver.tsx` (~760+ lines, **near cap — extract before big adds**).
- `GuidedPracticeSolutionTypePanel.tsx`, `GuidedPracticeParametricHelpPanel.tsx`.
- `use-guided-practice-session-submit.ts` — `selectSolutionType` grades on click.
- `guided-practice-wrong-recovery.ts` — popover widths including row-notation idle trim.
- Layout preview: `useGuidedPracticeLayoutPreview.ts`, `layoutPreviewOffsetGuard.ts`, `correctCheckPosition.ts`, `helpTriggerLayoutPosition.ts`.
- Tests passing headless: `guided-practice-infinite-solution.test.tsx`, `guided-practice-wrong-recovery.test.ts`, layout offset tests.

**Student portal:**

- `useGuidedPracticeHomeworkAttempt.ts` — resume index logic + `recordQuestionIndex`.
- `GuidedPracticeHomeworkView.tsx` — snapshot → `recordQuestionIndex`.
- `guided-practice.css`, `guided-practice-fraction-help.css` — solution-type + embed styles.

**Not done / placeholder:**

- Parametric help **MP4** not wired (same pattern as `GuidedPracticeFractionHelpPanel` / segmented animation when ready).

## Open questions and constraints

- Chase should confirm: **step 4 / `op1-row-entry`** yellow multiply-fractions alert visible after bundle reload.
- **Green check** beside matrix after correct row-entry (offset guard + slot placement) — retest if layout preview saved bad offsets.
- `GuidedPracticeSolver.tsx` file size: next feature work should **extract**, not inline.

## Read first

- `agent docs/momentum-handoffs/latest.md` (this file) then grep, do not read all of `GuidedPracticeSolver.tsx`.
- `School Scrips/student-portal/src/features/guided-practice/useGuidedPracticeHomeworkAttempt.ts` (resume).
- `School Scrips/Matrix app/src/app/components/guided-practice/GuidedPracticeSolutionTypePanel.tsx`.
- `School Scrips/Matrix app/src/app/hooks/guided-practice-wrong-recovery.ts` (popover width rules).
- `School Scrips/Matrix app/src/app/components/guided-practice/GuidedPracticeHelpTrigger.tsx` (placement).

## Exact next step

Open **11.2 Homework**, **Resume** problem 1. Walk one path Chase cares about: (1) row-entry step with **multiplying fractions** help visible, (2) **solution-type** MCQ after zero row (two choices, no Submit), (3) **Resume** after using tester **Next** mid-problem lands on same step. If row-notation box (step 3) still has too much empty space, adjust **`ROW_NOTATION_IDLE_POPOVER_WIDTH_TRIM`** only (width), never `left`, unless he asks to move it.
