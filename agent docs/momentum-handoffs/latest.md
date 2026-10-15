# Momentum handoff — Rational function graphing animation (example 1 done)

**Written:** 2026-10-14 (day-valid only)
**Repos touched:** `Programs/` (Manim Trial, agent docs), `School Scrips/student-portal`
**Git:** nothing committed or pushed. No GitHub, no end-of-session, no Netlify deploy.
(The previous `latest.md` was the Factoring GP handoff; its dated copy
`2026-10-14_factoring-gp-portal-animations-layout.md` is intact.)

---

## 1. Objective and phase

Chase is building a **series of Manim animations on graphing rational functions** for the student
portal. **Example 1, f(x) = (x+2)/(x-3), is finished and approved ("Perfect")**: final render done,
in the portal, and a review page exists. Next is the next example in the series (Chase has said
the next ones introduce a **slant asymptote**, then a **hole**; a squared factor is explicitly NOT
wanted yet).

## 2. Chase's desired feel / his teaching method (use his words)

His order, every problem: **everything must be factored first, check whether anything cancels** ->
**x-intercept** (set top = 0) -> **y-intercept** (plug in 0) -> **vertical asymptote** (set bottom
= 0) -> **horizontal asymptote** (compare degrees: equal -> divide leading coefficients; bigger on
top -> none, but potentially a slant; bottom bigger -> always y = 0) -> **holes** (if something
cancels) -> graph.
- Example 1 only says the equal-degree rule. "We'll explain [slant / holes] more when we have one."
- Graph: "graph all the asymptotes and plot all the points." Then **"look for points where you have to
  cross to draw the first curve"** (the side with the intercepts); **"since this one's going down,
  on the opposite side it will be going up"**; then **sketch** the other curve. Curves "want to ride
  to the horizontal asymptote." The caption says **"sketch"** but the drawn curve is accurate.
- He does NOT teach the squared-factor case (both sides same direction); don't mention it.
- Don't mention that a curve can cross the horizontal asymptote.
- He wanted the graph **zoomed out** so students see the curves settling onto the asymptotes
  (done: x -12..12, y -8..8).

## 3. Accepted decisions

- Scene: `Manim Trial/rational_function_graph.py`, class `RationalFunctionGraph`. Portrait 4:5,
  house solving style (op under both sides in gold, strike, copy_into), answers collect in a
  two-column list under the function (x-int, y-int, Holes | V.A., H.A.), graph fills the area below.
  Negatives use Chase's short dash; y-int shows "negative to the top number" as its own beat.
- Wired as an **instructor-preview tile** (`sectionGate: 'calculus-instructor'`, copy of the
  Fundamental Theorem pattern): `student-portal/src/features/video-examples/rationalFunctionsGuide.ts`
  (+ `RationalFunctionsGuideEntry.tsx`, route `rational-functions`, activity
  `precalc/rational-functions`, App.tsx / portalHomeApps.ts / MatrixHomeView.tsx / usePortalRoute.ts
  edits, `src/test/rationalFunctionsGuide.test.ts`). Assets in
  `src/assets/video-examples/rational-functions/graph-example-1{.mp4,-steps.json}`.
  Hold = **85.33 s**. Adding example 2 = a new entry in `examples` there + new asset pair + test.
- Review page for Chase: `http://127.0.0.1:8765/scratch/rational-function-graph.html` built by
  `Manim Trial/build_page.py` (row in `PAGES`, slug in `PORTRAIT`) -> `portal_clip_page.py`
  (fits one screen; Auto / Slow / Restart / Pause / Back / Next driven by the steps JSON).
  Chase said it was "really good" and "perfect". New clips: add a `PAGES` row + `PORTRAIT` slug.

## 4. Rejected directions

- Arrows showing "this side goes down / up" beside the vertical asymptote: removed; after zooming
  out the gap between curve and asymptote is too thin. The pulse on the drawn curve replaces them.
- Full-width review page: Chase's monitor could not see it on one screen -> height-fitted.
- Old explanation "the y-intercept is below the x-axis so it goes down" replaced by Chase's
  points-you-must-cross reasoning.

## 5. Implementation state / verification

- Final render 1080x1350@30, layout audit: all 22 marks clean; contact sheet checked for the
  graph beats; portal vitest for the new guide passes (2 tests). Page script syntax-checked with
  `node --check`; **the page's buttons and the portal tile were never opened/clicked** (no browser
  launch without permission) -- Chase has used the page and approved.
- `tsc --noEmit` shows pre-existing errors in generic-quiz, guided-practice, logic-homework (not
  from this work).
- Uncommitted: all of the above plus Manim Trial README line and the session scorecard bumps.
- The `700p15` draft folder under `media/videos/rational_function_graph/` is deleted before page
  builds (build_page.py globs the first mp4 it finds).

## 6. Open questions / constraints

- Not built: slant asymptote, hole (cancelling factor), bottom-degree-bigger case. Each should
  be its own example clip; extend `rational_function_graph.py` (the scene hard-codes example 1's
  numbers -- turn `TOP`/`BOTTOM`/answer rows into a small `Problem` record like
  `parabola_walkthrough.py` when example 2 needs it).
- Root rules: nothing on Chase's screen unasked; animation "done" = final render + portal assets +
  hold seconds + test; never Netlify deploy unless he says so; handoff to Chase is a flat
  statement, never "want me to...".
- Tile gating is instructor-only; making it student-visible (course bucket, migration) was never
  discussed.

## 7. Exact next step

Ask Chase for example 2's function (he said a slant asymptote example is next), then read
`rational_function_graph.py`, add a `Problem`-style input, add the slant-asymptote beat (long
division / "how to find the slant" per his method), render, wire as a second `examples` entry,
rebuild the review page.
