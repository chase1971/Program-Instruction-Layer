# Momentum handoff: Gauss-Jordan tutorial polish (Part 2/3)

**Written:** 2026-10-22 (night). Valid for today's continuation only.
**Nothing is committed or pushed.** Uncommitted work lives in `School Scrips/Matrix app` and `School Scrips/student-portal` (plus `Programs/` root for this handoff and session tracking). Commit only on "pull", "put on GitHub", or end of session.

This overwrites the earlier 2026-10-22 tap-or-click handoff. That copy work is already in the files; this file is the live continuation.

## Objective and phase

Chase is reviewing the **Gauss-Jordan Method tutorial** in the student portal (tester CHASE1, phone preview). He is walking Part 2 and Part 3 and fixing feel: prompt widths, the green column-rules tab, the step 3 number pad, yellow fraction-help `!` triggers, help-card buttons, and a bounce when the second matrix slides in.

Last finished change: Part 3 steps 6–7 bounce. `layout` was removed from both Part 3 matrix `motion.div`s so the slid-in matrix stays put when he taps the zero cell. He has not confirmed that bounce is gone.

## Chase's desired feel

- Head-mounted gyro mouse + dwell click + speech-to-text. Students tap; he dwells. Small buttons. No em dashes. No ephemeral success toasts. Never put a window on his screen without asking (permission is per run).
- He reviews **only in the portal**. Handoff is a statement: what to open, what he should see. Never "want me to launch / deploy?"
- Value-practice is the exemplar for the yellow `!` and the fraction mini-tutorials (multiply and add). Match that size and behavior. Do not invent a second help system.
- Speech-to-text: "plane button" = the blue primary Next on the help card. "Green pick / green box" = the Part 3 column-rules pull-down tab. "Part five of the second" = Part 2 step 5 (badge shows 5). "Box five / box six" = Part 2 prompt widths for `step === 5` and `step === 6` (the badge prints `step`, not `step + 1`, in these overlays).

## Accepted decisions

- Part 2 boxes 5 and 6 are 395px wide (100px more than 295).
- Part 3 step 3: blank + Submit are gone from the prompt. Scale factor is typed on the guided-practice **value** keypad (digits, `/`, `−`, Submit) that auto-opens on the right. Correct answer is still `2/7` (`isPart3ScaleAnswerCorrect`).
- Yellow multiply `!` on Part 2 step 4 is a **separate overlay** in the gap between the two matrices. The step 4 **instruction prompt stays** in the normal overlay under the row-op buttons. Do not put them in one column again.
- Yellow add `!` on Part 2 step 5 sits **under** the "Write the sum out in Part C" callout (only after the sum animation finishes), not in the step 4 gap.
- Both `!` triggers reuse `GuidedPracticeHelpTrigger` + `GuidedPracticeFractionHelpPanel` (multiply vs add-subtract). Same yes/no gate as value practice.
- Help-card Back / Replay / Next stay on **one row**. The blue Next was wrapping because it was too wide; portal CSS now `flex-wrap: nowrap` and smaller action buttons. Applies to EX1–EX3 and the add tutorial (same classes).
- `.gp-help-trigger__label` is excluded from `.matrix-embed button { font-size: 1rem }` so the yellow label is not forced into a tall skinny column.
- Green column-rules tab and the number pad are **not tied on x**. Pad stays right of the step 3 prompt (`PAD_OFFSET.x = 32`). Tab is 100px further left than that (`DRAWER_OFFSET.x = -68`). Expanded drawer uses `z-[60]` so it stacks above the pad and the prompt.
- Part 3 bounce: do **not** put `layout` back on those two matrix `motion.div`s. Pulse + check + step change was fighting the slide `x`.

## Rejected / corrected (do not rediscover)

- **Do not** move the Part 2 step 4 instruction prompt into the inter-matrix gap. That was wrong. He meant the `!` label ("Need help with multiplying fractions?") travels with the `!`, not the tutorial prompt.
- **Do not** use `placement="parent"` plus a shared 280px column that also holds the prompt. That is what shoved the prompt around.
- **Do not** move the number pad when he says to move the green tab, or the reverse, unless he names both. They share a file but have separate offsets now.
- Direction mix-up: he first asked the tab 50px left, then pad+tab 50px right, then "wrong direction, green box 100 left." Current tab x is the 100-left from the post-right position. If it still looks wrong, ask which way and how many pixels. Do not "also move the pad" unless he says so.
- **Do not** treat AGENTS.md "step 9 means `step === 8`" as applying to these Part 2/3 overlay badges. The badge renders `{step}`. Box five = `step === 5`.
- **Do not** launch the portal, Matrix app, or a browser to verify. No Netlify deploy unless he says deploy in the same message.
- **Do not** add lines to `matrix-solver-part-3.tsx` without extracting first (it is ~693, near 700).
- Cheat-enabled top Next (from earlier in this same evening) is already in `tutorialTopNext.ts`. Students stay gated. Do not add a second Next button.

## Current implementation state

Key files (uncommitted):

- Part 2: `matrix-tutorial-overlay-part-2.tsx` (widths; step 4 prompt restored), `part-2-step-4-multiply-help.tsx` (`Part2FractionHelpTrigger`, overlay vs flow), `matrix-solver-part-2.tsx` (help topic state, step 4 overlay `!`, step 5 add `!` under Part C).
- Part 3: `part-3-scale-value-pad.tsx`, `matrix-tutorial-overlay-part-3.tsx` (no in-prompt blank), `matrix-column-rules-drawer.tsx` (`DRAWER_OFFSET` / `PAD_OFFSET` / z-index), `matrix-solver-part-3.tsx` (`layout` removed), `use-matrix-tutorial-part-3.ts` (`isPart3ScaleAnswerCorrect`).
- Shared: `GuidedPracticeHelpTrigger.tsx` (`placement: 'viewport' | 'parent'`).
- Portal: `matrix-embed.css` (exclude help label from 1rem button font), `guided-practice-fraction-help.css` (nowrap smaller help actions), `MatrixTutorialView.tsx` (`onFractionHelpOpenChange` so the inset can go fraction-help mode).
- Tests that passed earlier: `part-3-scale-answer.test.ts`, `tutorialTopNext.test.ts`, `builder-keyboard.test.ts`, `guided-practice-wrong-recovery.test.ts`. Bounce fix was not re-tested in the browser (do not launch).

## Open questions and constraints

- He has not confirmed: bounce gone, green tab 100px left looking right, pad still clear of the step 3 prompt, add `!` under Part C, help buttons on one row.
- Portal Wide is 812×460. Measure before growing anything.
- Context in the outgoing chat is heavy. This handoff exists so the next task does not drag that transcript.

## Read first

- Matrix `AGENTS.md` (cheat-next, part 3 pad, part 2 `!` rows).
- `src/app/components/part-2-step-4-multiply-help.tsx`
- `src/app/components/matrix-column-rules-drawer.tsx`
- `src/app/tutorial/tutorialTopNext.ts` if he is still on skip/cheat.

## Exact next step

Ask what he sees on **Part 3** after the second matrix slides in and he taps the zero cell. If it still bounces, look at remaining transforms (cell pulse `scale(1.05)`, check flash scale) before putting `layout` back. If he is done with bounce, take the next screenshot or spoken tweak (green tab, pad, or Part 2 `!`) as a small isolated edit.
