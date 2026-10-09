# Momentum handoff — Equations of Lines: problems 1 and 2 done, problem 3 next (M1314)

**Written:** 2026-10-08

## Read first
- `School Scrips/student-portal/AGENTS.md` (portal rules; **never deploy to Netlify unless Chase says so in that message**)
- `Manim Trial/equations_of_lines.py` (problems 1 and 2 clips) and `Manim Trial/ANIMATION_STYLE_RECIPE.md` ("Portal clips", "Solving an equation on screen") + `docs/LAYOUT_GUARDRAILS.md`
- `School Scrips/student-portal/src/features/equations-of-lines/` (`equationsOfLinesExamples.ts`, `equationsOfLinesContent.ts`, `EquationsOfLinesExamplePage.tsx`)
- Exemplars it copies: `solve_steps.py`, `math_notation.py`, `quadratic_domain_range.py`, `slope_intercept_form.py`

## Objective and phase
Manim worked-example clips for the Equations of Lines portal app (worksheet `C:\Users\chase\My Drive\M1314\Unit 2\Blank\2.5 Equations of Lines.docx`). **Problems 1 and 2 are DONE and approved by Chase** ("that looks good"), wired into their Watch pages. Remaining: problem 3 (parallel) and problem 4 (perpendicular).

## Chase's teaching method (his words, the spec for every problem)
Start in **point-slope form** and plug everything in -> **clear the fraction** by multiplying both sides by the denominator -> **distribute** -> switch to **standard** or **slope-intercept**.
- Standard form = **no fractions and the x term positive**. Slope-intercept = whatever `y = mx + b` comes out to.
- Problem 1: slope given. **Problem 2: slope formula first, then either point (he used (2, 8)), same process.**
- **Problems 3 and 4 (parallel / perpendicular) method NOT discussed yet** -- ask Chase before designing.

## Chase's desired feel
- Multiply step done **in place**: slide fraction and `(x - 3)` right, insert a gold multiplier in front of each side, a `·` between it and the fraction, strike the right-hand multiplier and the denominator.
- **Final answer in a box, all black.** White paper background, portrait 4:5, captions on top, pulses not boxes (answer box is the exception), his negative style (short dash, negative hangs left of the top number).
- Problem 2 tweaks he asked for and approved: tight gap in `3 · -2/3` (no extra spacing after the dot), and the **standard-form answer rides higher** (`STANDARD_ANSWER_Y = -1.5`, just under the ops row) instead of the bottom.

## Accepted decisions
- One `Problem` record drives `EquationsOfLines`: `num, den, x1, y1, marks_file, first=(x,y) second point, ending='slope-intercept'|'standard'`. Scenes: `SlopePointSlopeIntercept` (problem 1, 51.67 s), `TwoPointsStandard` (problem 2, 69.44 s, ends on `2x + 3y = 28`). `find_slope` is the slope-formula phase.
- Standard ending: add the x term (2x) and the constant (24) to both sides, strike the cancelled terms; no dividing.
- Portal: `EQUATIONS_OF_LINES_EXAMPLES` maps problem id -> `VideoExampleEntry` (`slope-point`, `two-points` done; `parallel`, `perpendicular` still "Animation coming soon"). Page autoplays via `useVideoExamplePlayer`.
- Delivery: render `-r 1080,1350 --fps 30` with `Manim Trial/.venv/Scripts/python.exe -m manim ... --disable_caching`, copy `media/videos/equations_of_lines/1350p30/<Scene>.mp4` to `student-portal/src/assets/video-examples/equations-of-lines/problem-N.mp4`, set `segmentEndSeconds` to the `hold` mark of that scene's marks file.

## Rejected / pitfalls
- Gold "x7" under both sides (first multiply design) -- replaced by the in-place insert.
- **Shell + backslashes:** bash heredocs/sed/python -c mangle LaTeX backslashes (`\f` became a formfeed once). Put LaTeX in files via Write/Edit or a script file written with Write.
- `contact_sheet.py` only knows `<folder>_marks.json` and the first PAGES row for a folder; each scene here has its own marks file, so sheet a second scene with a small script calling `contact_sheet.grab_frame` / `montage` (done for problem 2; README notes it). Each scene needs its own marks filename.
- Never `-p`/`--preview`; no GUI, browser, or Netlify without asking. Handoff is a statement, not a question.
- The audit passes invisible/low-contrast frames: always read the contact sheet.
- `Problem` limits: positive points, falling line for the slope-formula beats, standard form only for negative slope, slope-intercept only for positive slope. Problems 3/4 (given points like (3, -4), (-2, 6); lines `8x + 6y = 15`, `8x - 4y = 8`) will need these generalized -- extend, don't fork a second scene.

## Implementation state (all UNCOMMITTED, undeployed)
- Problem 2 new/changed: `Manim Trial/equations_of_lines.py`, `equations_of_lines_two_points_marks.json`, README row; `student-portal/.../equationsOfLinesExamples.ts` (+ `problem-2.mp4`).
- Earlier uncommitted feature work (static app, route/tile wiring, video aspect fix, migration 078 file in student-session-kit, 078 already `db:push`ed, problem 1 clip) is still uncommitted.
- Verification: audit clean at all 17 marks for problem 2, contact sheet read, vitest 5/5, tsc clean for these files. Chase approved problem 2 from the rendered video. Session scorecard bumped.

## Open items / constraints
- Macro App Teacher Console does not list Equations of Lines yet, so Chase can't toggle it on for students (mirror Composite: `useTeacherConsoleActivityCatalog.ts`, `teacherConsoleActivityTitle.ts`, `videoSlotCatalog.ts`, `portalPreviewRouteAspect.ts`).
- Problem numbering and the parallel/perpendicular direction wording were my choices, not confirmed.

## Exact next step
Ask Chase ONE question about problem 3's method: given `8x + 6y = 15; (3, -4)`, parallel, slope-intercept answer. Proposal (not approved): solve the given line for y to get m = -4/3 (parallel = same slope), then run the standard beats with (3, -4) (negative y1 means the point-slope row has `y + 4`). Problem 4 (`8x - 4y = 8; (-2, 6)`, perpendicular, standard form) adds the negative reciprocal. Then generalize `Problem` for negative point coordinates and a line-given start.
