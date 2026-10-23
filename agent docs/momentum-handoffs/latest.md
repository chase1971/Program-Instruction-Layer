# Momentum handoff: Gauss-Jordan guided practice / homework polish

**Written:** 2026-10-22 (late night). Valid for today's continuation only.
**Nothing is committed or pushed.** Uncommitted work lives in `School Scrips/Matrix app`, `School Scrips/student-portal`, and a prompt string in `School Scrips/Macro App` (`matrixSlotCatalog.ts`). Handoff + session tracking live in `Programs/` root. Commit only on "pull", "put on GitHub", or end of session.

This overwrites the earlier 2026-10-22 Part 2/3 tutorial handoff. That Part 2/3 work is already in the files. This file is the live continuation: Chase moved on to **guided practice / Gauss-Jordan Method Homework** (tester CHASE1, phone preview) and iterated the yellow `!`, row-scaling help card, row-entry, and the solution pair.

## Objective and phase

Chase is walking homework as a student (with tester cheats) and fixing feel on each screen: yellow help labels, the row-scaling tutorial card, row-entry (scale then replace), row-notation format errors, and the final ordered-pair step.

Last finished change: solution step (Q17). Pad auto-opens on x. Prompt is only "What is the solution?" with no Submit. First pad button is Next; second is Submit and that grades the pair. He has not confirmed that screen.

## Chase's desired feel

- Head-mounted gyro mouse + dwell click + speech-to-text. Students tap; he dwells. Small buttons. No em dashes. No ephemeral success toasts. Never put a window on his screen without asking (permission is per run).
- He reviews **only in the portal**. Handoff is a statement: what to open, what he should see. Never "want me to launch / deploy?"
- Yellow `!` + "Need help with…?" is one system (`GuidedPracticeHelpTrigger`). Same compact size everywhere. Do not invent a second help widget.
- "Explanation point" = the yellow `!`. "Text box from the yellow" = the small bordered label beside it. "The matrix that's being typed" = the blank row-entry grid, not the original matrix.
- Tester Back/Next in the top nav stay for him. Students never see those. Do not put the tutorial title in that nav slot.
- Incomplete-notation warning belongs on the **pad only**, not in the blue instruction card.

## Accepted decisions

- Compact yellow labels are all the wider size (portal compact `max-width: 8.125rem`). Notation, multiplying, adding, reveals, Part 2/3. `wideLabel` defaults true on `GuidedPracticeHelpTrigger`.
- Row-scaling help card: ~500px, higher on the page (not full-stretch), smaller type, **Row scaling tutorial** centered at the top of the card, **Back to question** inside the card (bottom-left of the actions). In-card Step N of M stays. Top-nav **1 of 3** hides while help is open (`hideLabel={fractionHelpOpen}`). Cheat Back/Next stay.
- Row-entry (scale and replace): no Use answer, no Submit row in the prompt. Prompt is 50px narrower (idle 200px). Compact `!` sits **under the typed row**, parent-placed, not the old viewport coords. Filling the last cell submits the row.
- Row-notation format error ("Enter the full row transformation before submitting.") stays on the pad. Blue prompt keeps "Write the row replacement operation."
- Solution pair: pad opens on x (`use-guided-practice-question-init.ts`). No Submit in the prompt. x pad = Next (advances to y). y pad = Submit (`commitGuidedPracticeBuilder` already returns `submit-solution`). Prompt copy is "What is the solution?"
- Guided practice cheat Back sits next to cheat Next (`UnguidedPracticeProblemNav`). Students stay gated.
- Row-notation pad still auto-opens; pad Submit grades the transformation. Compact `!` beside the matrix (`guided-practice-notation-help-trigger.tsx`).
- Green correct-check flash in guided practice is `translate-y-[30px]` so it clears the `!` label.

## Rejected / corrected (do not rediscover)

- **Do not** put "Row scaling tutorial" in the top-nav cheat Back/Next slot. That slot is his, not the student's title.
- **Do not** leave **Back to question** floating at the viewport corner. It lives inside the help card.
- **Do not** put the multiplying/adding `!` back at the old fixed viewport coords beside the prompt (`fractionHelpButtonPosition` idle numbers). Those stay unused for first-try row-entry. Help goes under the typed row.
- **Do not** bring Use answer or Submit row back into the instruction card. Last cell / last solution field submits.
- **Do not** duplicate the format-error banner into the blue prompt. Pad only.
- **Do not** treat AGENTS.md "step 9 means `step === 8`" as applying to Part 2/3 overlay badges. The badge renders `{step}`.
- **Do not** add lines to `use-guided-practice-session.ts` (at the 700 cap). Init, submit, and resume hydration live in the extracted hooks.
- **Do not** add lines to `matrix-solver-part-3.tsx` without extracting first (still near 700).
- **Do not** launch the portal, Matrix app, or a browser. No Netlify unless he says deploy in the same message.
- Part 2 step 4: the instruction prompt stays under the row-op buttons. Only the `!` label travels with the `!` in the matrix gap. Do not merge them into one column.

## Current implementation state

Key files (uncommitted):

- Help labels: `GuidedPracticeHelpTrigger.tsx` (`wideLabel` default true), `guided-practice-notation-help-trigger.tsx` (always wide), portal `guided-practice-fraction-help.css` and Matrix `theme.css` (compact 8.125rem / 8.625rem).
- Row-scaling / replacement help: `GuidedPracticeRowNotationHelpPanel.tsx` (topic + in-card exit), `GuidedPracticeRowReplacementNotationHelpPanel.tsx` (exit inside card), portal `.gp-row-notation-help-screen*` (smaller type, top-aligned 500px card).
- Nav: portal `UnguidedPracticeProblemNav.tsx` (`hideLabel`), wired from `GuidedPracticeView.tsx` and `GuidedPracticeHomeworkWorkspace.tsx`.
- Row-entry / solution: `GuidedPracticeSolver.tsx` (help under typed row, check +30px y, no overlay submit props), `GuidedPracticeOverlay.tsx` (no Use answer / Submit row / solution Submit; no row-notation format banner), `use-guided-practice-question-init.ts` (solution pad on x), `guided-practice-builder-commit.ts` (`submit-matrix-row` on last cell), `use-guided-practice-session-submit.ts`, `guided-practice-wrong-recovery.ts` (`ROW_ENTRY_IDLE_POPOVER_WIDTH_TRIM = 50`), `guided-practice-questions.ts` (solution prompt), `guided-practice-resume-state.ts` (solution-field hydration).
- Macro catalog prompt sync: `Macro App/renderer/src/utils/matrixReport/matrixSlotCatalog.ts`.
- Matrix `AGENTS.md` tap-or-click / submit-row / ordered-pair row is the lookup.

Tests that passed this continuation (headless): row-notation help panel, builder-commit, wrong-recovery widths, builder-keyboard, resume-state, solution-entry commit, unguided solver, engine. No browser confirmation (do not launch).

## Open questions and constraints

- He has not confirmed: solution Q17 pad-on-arrival, adding-fractions `!` under the typed row after refresh, or the latest compact label width on every `!`.
- If he still sees Use answer / Submit row on replace row-entry, that screenshot was from before the overlay removal. Source no longer has those buttons. Ask him to refresh before editing again.
- Portal Wide is 812×460. Measure before growing anything.
- Context in the outgoing chat is heavy. This handoff exists so the next task does not drag that transcript.

## Read first

- Matrix `AGENTS.md` (tap-or-click / submit row / ordered pair row, plus cheat-next and part 2 `!` rows).
- `src/app/hooks/use-guided-practice-question-init.ts`
- `src/app/components/guided-practice/GuidedPracticeOverlay.tsx`
- `src/app/components/guided-practice/guided-practice-notation-help-trigger.tsx`

## Exact next step

Wait for his next homework screenshot or spoken tweak. If he is still on Q17, the expected screen is: pad already open on the first blank, prompt "What is the solution?" only, Next then Submit. If he names another yellow `!` or a collision, treat it as a 30px / placement edit on the existing trigger, not a new help system.
