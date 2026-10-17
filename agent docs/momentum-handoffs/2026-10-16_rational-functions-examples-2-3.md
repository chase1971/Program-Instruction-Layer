# Momentum handoff — Rational function graphing animations (examples 2 and 3 done)

**Written:** 2026-10-16 (day-valid only)
**Repos touched:** `Programs/` (Manim Trial, agent docs), `School Scrips/student-portal`
**Git:** nothing committed or pushed. No GitHub, no end-of-session, no Netlify deploy.
(The previous `latest.md` was the Factoring GP "roots reveal polish" handoff from a parallel
session; its dated copy `2026-10-15_factoring-gp-roots-reveal-polish.md` is intact. The
example-1 handoff `2026-10-14_rational-function-graph-example-1.md` is still the best source for
Chase's teaching method and the example-1 decisions.)

---

## 1. Objective and phase

Chase is building a **series of Manim animations on graphing rational functions** for the student
portal gallery "Graphing Rational Functions" (M1314, instructor-gated, access off by default).
**Three clips are done, rendered, wired, tests green**; Chase approved Part 2 ("That looks great")
after his tweaks and has not yet reviewed Part 3 in the portal. Remaining from his stated plan:
a **slant asymptote** example (still not built). A squared factor is explicitly NOT wanted.

| Part | f(x) | Scene (class) | Asset pair (`student-portal/src/assets/video-examples/rational-functions/`) | Hold |
|---|---|---|---|---|
| 1 | (x+2)/(x−3) | `rational_function_graph.py` (`RationalFunctionGraph`) | `graph-example-1` | 85.33 |
| 2 | (x+3)/(x²−9), hole at (−3, −1/6) | `rational_function_hole.py` (`RationalFunctionHole`) | `graph-example-2` | 102.0 |
| 3 | (2x+1)/x, no y-intercept | `rational_function_no_yint.py` (`RationalFunctionNoYInt`) | `graph-example-3` | 85.89 |

## 2. Chase's desired feel (his words / corrections this session)

Teaching order unchanged (factor + cancel check -> x-int -> y-int -> V.A. -> H.A. -> holes ->
graph; see the example-1 handoff). New this session:
- Hole example: "after you've canceled terms you use the **reduced function** for everything
  else"; at the end "bring back the term we canceled, set it equal to zero, find x, plug it into the
  **reduced** function to get the y." x-int is **"none"** when the top is just a number (no x).
- "Leaving **x + 3 canceled** on screen is fine. Once you bring it down, get rid of the word
  *Canceled* and put **Hole**, then put the −3 inside the x position of Hole with empty
  parentheses, and as you find the two ordered-pair values, plug them in."
- **Cancel = ONE animation** (both red slashes drawn together), not two with a wait between.
- **Negative to the top number: do it silently** — after "Simplify the bottom" shows 1 over −3,
  just move the negative up; no caption, no separate step.
- Label is **"Hole:"**, not "Holes:" (singular, when there is one).
- Hole graph must be **zoomed in** so the open circle and y-intercept read clearly **below** the
  y = 0 line (zoomed-out version looked like they sat on the axis). Caption is explicit that the
  curve goes **right through the hole**.
- Gallery home page must start **at the top**, never vertically centered (all gallery apps).
- Part 3: "this one won't have a y-intercept"; Chase picked (2x+1)/x himself.

## 3. Accepted decisions

- **Subclass the example-1 scene** instead of copying it. `RationalFunctionGraph` now owns the
  graph window as class attrs `graph_x, graph_y, x_unit, y_unit, graph_step` (`build_graph` reads
  them); subclasses set their own. `solve_for_x(..., on_copy=())` takes extra animations that play
  with the copy-down beat (used by the hole clip's Canceled -> Hole swap). Part 2 window
  x −8..8, y −2.5..2.5 (units .36/.72, per-axis on purpose); Part 3 x −4..4, y −3..7.
- Layout: left list column = x-int, y-int; right column = V.A., H.A., then **Hole / Canceled at
  y = 0.3** (its fraction otherwise collided with the y-int row and the graph top).
- Part 2 beat: factor bottom (difference of squares) -> cancel (strike x+3 top and bottom, copy of
  x+3 slides into "Canceled: x+3") -> reduced function 1/(x−3) -> x-int none -> y-int
  (−1/3) -> V.A. 3 -> H.A. y = 0 (bottom bigger) -> hole (Canceled becomes "Hole: ( , )", −3 copied
  in, then −1/6) -> graph.
- Part 3 beat: x-int solved in house style (−1 under both sides, strike, then divide by 2 with
  `divide_bars`) -> y-int: plug 0 -> 1/0 -> "undefined" -> "y-int: none" -> V.A. x = 0 (already
  solved) -> H.A. y = 2/1 -> "Hole: none" -> graph through the x-int, opposite diagonal curve up.
- Gallery top alignment: `justify-content: flex-start` in
  `student-portal/src/styles/video-examples.css`
  (`.portal-quiz--vector-projections .video-examples-shell--gallery`, portrait media query);
  documented in `agent docs/recipes/portal-math-video-examples.md` ("Gallery home layout").
  This also moved Conics and Vectors & Projections galleries to the top (same shared rule).
- Portal wiring: three `examples` entries in `rationalFunctionsGuide.ts` (hold constants
  `RATIONAL_GRAPH_EXAMPLE_{1,2,3}_HOLD_SECONDS`), `src/test/rationalFunctionsGuide.test.ts`
  (4 tests pass). Review pages: `build_page.py` `PAGES` rows + `PORTRAIT` slugs
  `rational-function-hole`, `rational-function-no-yint` (pages not built/opened this session).

## 4. Rejected directions

- Two separate strike animations for the cancel (too cut up). Spoken/captioned "Move the negative
  to the top number" step (replaced by a silent move). "Holes:" plural label. The zoomed-out
  x −12..12 window for the hole clip. Putting the hole row in the left column (collided).

## 5. Implementation state / verification

- All three clips: final render 1080x1350@30, layout audit clean (zero problem marks), contact
  sheet read frame by frame, steps JSON + MP4 copied, portal vitest passes (4/4).
- After the `build_graph` refactor, **Parts 1 and 2 were NOT re-rendered** (their rendered
  assets are from before; the refactor should be output-identical, Part 2 was re-rendered earlier
  with its own override which the class attrs reproduce). If a later change touches the parent,
  re-render both to be safe.
- The portal tile / gallery top-alignment were never opened in a browser (no launching without
  permission). Chase has not yet seen Part 3 or the top-aligned gallery.
- `tsc --noEmit` pre-existing errors in generic-quiz, guided-practice, logic-homework are not ours.
- Uncommitted: everything above plus session scorecard bumps (3 logged). Doc line in
  `portal-math-video-examples.md` file map updated to name examples 2 and 3.

## 6. Open questions / constraints

- Slant asymptote example: Chase has not given the function. Ask for it, then extend a subclass
  (same pattern; needs a long-division / "how to find the slant" beat per his method — not yet
  specified by him; ask rather than invent).
- Root rules: nothing on Chase's screen unasked; animation "done" = final render + portal assets +
  hold + test; never Netlify deploy unless he says so; handoff to Chase is a flat statement.
- Tile gating is instructor-only (`sectionGate: 'transformations'`, access OFF via migration 088);
  student-visible rollout never discussed.

## 7. Exact next step

Wait for Chase's feedback on Part 3 / the top-aligned gallery (he reviews in the portal). If he
asks for the slant-asymptote example, ask for the function first, then read
`rational_function_graph.py` + `rational_function_no_yint.py` (shortest subclass exemplar), add
`rational_function_slant.py` as another subclass, render, add `graph-example-4` + guide entry +
test, add a `PAGES` row.
