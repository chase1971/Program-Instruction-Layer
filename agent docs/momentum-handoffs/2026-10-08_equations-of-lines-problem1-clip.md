# Momentum handoff — Equations of Lines: problem 1 clip done, problem 2 next (M1314)

**Written:** 2026-10-08

## Read first
- `School Scrips/student-portal/AGENTS.md` (portal rules; **never deploy to Netlify unless Chase says so in that message**)
- `Manim Trial/equations_of_lines.py` (the finished problem 1 clip) and `Manim Trial/ANIMATION_STYLE_RECIPE.md` ("Portal clips", "Solving an equation on screen") + `docs/LAYOUT_GUARDRAILS.md`
- `School Scrips/student-portal/src/features/equations-of-lines/` (`equationsOfLinesExamples.ts`, `EquationsOfLinesExamplePage.tsx`)
- Exemplars it copies: `solve_steps.py`, `math_notation.py`, `quadratic_domain_range.py`, `slope_intercept_form.py`

## Objective and phase
Chase is building Manim worked-example animations for the Equations of Lines portal app (source worksheet `C:\Users\chase\My Drive\M1314\Unit 2\Blank\2.5 Equations of Lines.docx`). **Problem 1 (m = 5/7; (3, 4), slope-intercept) is DONE and approved by Chase** ("that looks great"), wired into its Watch page. Next: problem 2, then 3 and 4.

## Chase's teaching method (his words, the spec for every problem)
Start in **point-slope form** and plug everything in -> **clear the fraction** by multiplying both sides by the denominator -> **distribute** -> switch to **standard** or **slope-intercept**.
- Standard form = **no fractions and the x term positive**. Slope-intercept = whatever `y = mx + b` comes out to.
- Problem 1: slope given, just plug in. **Problem 2: find the slope with the slope formula first, then use either point (it doesn't matter which)** and run the same process.
- Problems 3 (parallel) and 4 (perpendicular) not discussed yet.

## Chase's desired feel (confirmed on problem 1)
- Multiply step is done **in place**: slide the fraction and `(x - 3)` right, insert a gold 7 in front of each side, a **`·` dot between the 7 and the fraction**, strike the right-hand 7 and the denominator; the left 7 is already there.
- **Final answer in a box, all black** (no accent color on the answer).
- White paper background, portrait 4:5 frame, captions on top, pulses not boxes (the answer box is his one explicit exception), his negative style.

## Accepted decisions
- One `Problem` record (num, den, x1, y1) drives `EquationsOfLines`; scene `SlopePointSlopeIntercept` = problem 1. Clip ~51.67 s, ends on a hold with all work + boxed answer.
- Portal: `EQUATIONS_OF_LINES_EXAMPLES` maps problem id -> `VideoExampleEntry`; page autoplays via `useVideoExamplePlayer([entry], { autoPlay: true })` + `VideoExamplesPlayerStage`. Problems with no entry keep "Animation coming soon".
- Delivery: final render `-r 1080,1350 --fps 30`, copy to `student-portal/src/assets/video-examples/equations-of-lines/problem-N.mp4`, set `segmentEndSeconds` to the `hold` mark in `equations_of_lines_marks.json` (currently 51.67, in `equationsOfLinesExamples.ts`).

## Rejected / pitfalls
- Gold "×7" under both sides (my first multiply design) — replaced by the in-place insert above.
- **LaTeX in TS strings: use `String.raw` or double backslashes**; use Write/Edit (not bash heredocs) for files with LaTeX.
- `contact_sheet.py` expects `<module>_marks.json` — the marks file is per module (`equations_of_lines_marks.json`), so **a second scene in this module overwrites it**. Give each problem its own marks filename and tell the contact sheet / README, or split modules.
- Never `-p`/`--preview`; no GUI, browser, or Netlify without asking. Handoff is a statement, not a question.
- The audit passes frames that are invisible/low contrast: always read the contact sheet.

## Implementation state (all UNCOMMITTED, undeployed)
- New: `Manim Trial/equations_of_lines.py`, `equations_of_lines_marks.json`, README row; `student-portal/.../equationsOfLinesExamples.ts`, `src/assets/video-examples/equations-of-lines/problem-1.mp4`; edited `EquationsOfLinesExamplePage.tsx`, `src/test/equationsOfLines.test.ts` (5 tests pass).
- Earlier uncommitted work from this feature (static app, route/tile wiring, video aspect-ratio fix, migration 078 file in student-session-kit, 078 already `db:push`ed) is still uncommitted.
- Verification: audit clean at all 12 marks, contact sheet read, vitest 5/5; tsc clean for these files (pre-existing unrelated errors elsewhere). **Chase has not watched it in the portal yet** beyond approving the frames/description — no browser was opened.
- Session scorecard bumped for problem 1.

## Open items / constraints
- Macro App Teacher Console does not list Equations of Lines yet, so Chase can't toggle it on for students (mirror Composite: `useTeacherConsoleActivityCatalog.ts`, `teacherConsoleActivityTitle.ts`, `videoSlotCatalog.ts`, `portalPreviewRouteAspect.ts`).
- Problem numbering 1-4 and the parallel/perpendicular direction wording were my choices, not confirmed.
- The `Problem` dataclass only accepts **positive** slope/point values and a slope-intercept ending; problem 2 needs a negative slope and a standard-form ending, so generalize it (don't fork a second scene implementation).

## Exact next step
Build problem 2 (`(11, 2), (2, 8)`, standard form). Verified math: m = (8 - 2)/(2 - 11) = 6/(-9) = **-2/3** (show the slope formula first; negative goes on the top number per Chase's convention, `hanging_fraction`). Using (2, 8): `y - 8 = -2/3(x - 2)` -> x3: `3(y - 8) = -2(x - 2)` -> `3y - 24 = -2x + 4` -> add 2x and 24: `2x + 3y = 28` (standard: no fractions, x positive). Check (11, 2): 22 + 6 = 28. Reuse the problem 1 beats; add the slope-formula beat first and a standard-form ending; add `two-points` to `EQUATIONS_OF_LINES_EXAMPLES`. Confirm with Chase only if the standard-form move-the-x-term step needs a design he hasn't shown.
