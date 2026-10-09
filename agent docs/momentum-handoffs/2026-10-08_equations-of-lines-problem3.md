# Momentum handoff — Equations of Lines: problems 1-3 done, problem 4 (perpendicular) next (M1314)

**Written:** 2026-10-08

## Read first
- `School Scrips/student-portal/AGENTS.md` (portal rules; **never deploy to Netlify unless Chase says so in that message**)
- `Manim Trial/equations_of_lines.py` (611 lines; problems 1-3) and `Manim Trial/ANIMATION_STYLE_RECIPE.md` ("Portal clips", "Solving an equation on screen") + `docs/LAYOUT_GUARDRAILS.md`
- `School Scrips/student-portal/src/features/equations-of-lines/` (`equationsOfLinesExamples.ts`, `equationsOfLinesContent.ts`, `EquationsOfLinesExamplePage.tsx`)
- Exemplars it copies: `solve_steps.py`, `math_notation.py`, `quadratic_domain_range.py`, `slope_intercept_form.py`

## Objective and phase
Manim worked-example clips for the Equations of Lines portal app (worksheet `C:\Users\chase\My Drive\M1314\Unit 2\Blank\2.5 Equations of Lines.docx`). **Problems 1, 2 DONE and approved by Chase. Problem 3 (parallel) is rendered, audited, contact-sheet read and wired into its Watch page, but Chase has NOT yet reviewed the video.** Remaining: problem 4 (perpendicular).

## Chase's teaching method (his words, the spec for every problem)
Start in **point-slope form** and plug everything in -> **clear the fraction** by multiplying both sides by the denominator -> **distribute** -> switch to **standard** or **slope-intercept**.
- Standard form = **no fractions and the x term positive**. Slope-intercept = whatever `y = mx + b` comes out to.
- Problem 1: slope given. Problem 2: slope formula first, then either point, same process.
- **Problem 3 (his description):** write the problem out like the worksheet; say a parallel line needs the other line's slope, parallel lines have the same slope; give the line, rewrite it in slope-intercept form (animated), identify the slope, bring it up to the corner as `m = ...` with the point, then it is "just like the first problem."
- **Problem 4 (perpendicular) method NOT discussed yet** -- ask Chase ONE focused question before designing. Proposal (not approved): same opening as problem 3 (write the problem out, find the given line's slope from `8x - 4y = 8` -> m = 2), then say perpendicular slopes are negative reciprocals (-1/2), then the standard beats with (-2, 6) ending in standard form.

## Chase's desired feel
- Multiply step in place (gold multiplier inserted, `·`, strike right multiplier and denominator). Final answer in a box, all black. White paper, portrait 4:5, captions on top, pulses not boxes (answer box excepted), his negative style (short dash; negative hangs left of the top number).
- Captions one line each (wrap width 5.9, font 20): a 50+ char caption can strand a word on line 2; check frames.
- Problem 2 standard answer rides high (`STANDARD_ANSWER_Y = -1.5`).

## Accepted decisions
- One `Problem` record drives `EquationsOfLines`: `num, den, x1, y1, marks_file, first=(x,y), line=(A,B,C), relation='parallel', ending`. Scenes: `SlopePointSlopeIntercept` (51.67 s), `TwoPointsStandard` (69.44 s), `ParallelSlopeIntercept` (97.22 s, ends `y = -4/3 x`; the 12s cancel so no constant, `p.c == 0` path). `statement()` writes the problem out; `find_line_slope()` is the given-line phase; `find_slope()` is the slope-formula phase.
- Generalizations done: negative y1 (`y + 4`, "Subtract 12 from both sides"; slope-intercept only), negative slope in slope-intercept, zero constant. `signed(n)` gives a MathTex negative part (pass `NEG+digits`; a bare `'-4'` after a comma stays a full minus).
- Portal: `EQUATIONS_OF_LINES_EXAMPLES` has `slope-point`, `two-points`, `parallel` (problem-3.mp4, hold 97.22). `perpendicular` still "Animation coming soon".
- Delivery: render `-r 1080,1350 --fps 30 --disable_caching` with `$env:PATH` including `%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64`, `Manim Trial/.venv/Scripts/python.exe -m manim equations_of_lines.py <Scene>`, copy `media/videos/equations_of_lines/1350p30/<Scene>.mp4` to `student-portal/src/assets/video-examples/equations-of-lines/problem-N.mp4`, set `segmentEndSeconds` to the `hold` mark of that scene's marks file (`equations_of_lines_<name>_marks.json`).

## Rejected / pitfalls
- **Shell + backslashes:** bash heredoc python patch scripts mangle LaTeX (`\f` -> formfeed) and quotes. Use the Edit tool for anything with `\frac`/apostrophes.
- `contact_sheet.py` only knows `<folder>_marks.json`; per-scene sheets use a small script calling `contact_sheet.grab_frame`/`montage` (set `cs.THUMB_WIDTH = 420`, chunks of 8 tiles; the problem-3 script lived only in the session scratchpad). Always read the sheet; the audit passes invisible frames.
- Never `-p`/`--preview`; no GUI, browser, or Netlify without asking. Handoff is a statement, not a question.
- `Problem` limits still: x1 positive; standard form only for negative slope and positive y1; given line needs A, B > 0 and parallel. Problem 4 (`8x - 4y = 8`, (-2, 6), perpendicular, standard) needs negative x1, negative B, negative reciprocal, and standard form: extend, don't fork.

## Implementation state (all UNCOMMITTED, undeployed)
- Problem 3 new/changed: `Manim Trial/equations_of_lines.py`, `equations_of_lines_parallel_marks.json`, README row; `student-portal/.../equationsOfLinesExamples.ts` + `problem-3.mp4`.
- Earlier uncommitted feature work (static app, route/tile wiring, video aspect fix, migration 078 in student-session-kit already `db:push`ed, problems 1-2 clips) is still uncommitted.
- Verification: audit clean at all 23 marks, contact sheet read, problems 1/2 re-rendered with identical marks (regression OK), vitest 5/5, tsc clean for these files. Session scorecard bumped.

## Open items / constraints
- Macro App Teacher Console does not list Equations of Lines yet, so Chase can't toggle it on for students (mirror Composite: `useTeacherConsoleActivityCatalog.ts`, `teacherConsoleActivityTitle.ts`, `videoSlotCatalog.ts`, `portalPreviewRouteAspect.ts`).
- Problem numbering (worksheet says "5.)", portal says 3) and the parallel/perpendicular wording were my choices; the on-screen statement omits the number.
- Chase has not yet watched problem 3.

## Exact next step
Ask Chase ONE question about problem 4's method (confirm the proposal above), then generalize `Problem` and add scene `PerpendicularStandard`. If he instead wants changes to problem 3, apply them first.
