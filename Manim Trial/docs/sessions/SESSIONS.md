## 2026-10-19 - FTC series: clip 3 proof reworked, theorem clip rebuilt, squeeze proof moved to clip 4

**Repos touched:** `Programs/` root (Manim Trial, agent docs), `School Scrips/student-portal`

**Files changed:** `Manim Trial/fundamental_theorem_calculus.py` (squeeze proof rebuilt on v=t(10-t): strip beats then squeeze, slowed ending; old position clip removed; ~480 lines), `Manim Trial/ftc_theorem_statement.py` (new, ~265 lines: full Part 1 and Part 2 statements, piece-by-piece breakdown incl. bar notation, then the car solved with F(b)-F(a), summary with shaded graph), `Manim Trial/build_ftc_series_page.py`, portal `fundamentalTheoremGuide.ts` (tabs: 1 Area and position, 2 Riemann sums, 3 The theorem hold 152.39 / 24 steps, 4 Proof hold 44.24 / 10 steps), `src/test/fundamentalTheoremGuide.test.ts`, assets `theorem-statement.*` and `squeeze-proof.*` (position-connection assets deleted).

**What worked:** Chase's four-clip order is now: area = position, Riemann sums to integral, the theorem explained (Part 1, Part 2, shorthand notation, worked car), the squeeze proof. Clip 3 uses his Word-doc wording and small text; the car example is directions only (find F, evaluate with the bar from 0 to 10, plug in) ending on "total distance = area under the curve". Heredoc Python edits mangled backslashes again (`` became backspace); use Edit or chr(92).

**Current state:** Green - all four clips rendered, wired, vitest 3/3, layout audit clean. Chase had not watched the final clip 3 or the slowed squeeze ending in the portal. Not deployed to Netlify.

**File size flag:** None.

**Next session:** Chase reviews tabs 3 and 4. Open questions: trim clip 2's own s(10)-s(0) ending now that clip 3 solves the car; convert clip 4's proof from v/A/t to the f/x/a notation used in clip 3; optionally add the blue-area/orange-strip pictures to clip 3.

## 2026-10-11 — Definition of an Ellipse (3 parts): foci, a/b/c figure, full derivation

**Repos touched:** `Programs/` root (Manim Trial, agent docs), `School Scrips/student-portal`, `School Scrips/student-session-kit`

**Files changed:** `Manim Trial/ellipse_definition.py` (new, ~215 lines, Part 1), `Manim Trial/ellipse_standard_form.py` (new mixin, ~265 lines, Parts 2-3), portal `conicsGuide.ts` (new "Definition of an Ellipse" entry, parts 0 / 51.4 / 103.52, hold 226.89; definition group lists parabola then ellipse), `src/test/conicsGuide.test.ts`, `conics-intro/ellipse-definition.mp4` + `-steps.json`, `agent docs/recipes/portal-math-video-examples.md`.

**What worked:** Part 1: definition d1 + d2 = constant, two foci, a point with live d1/d2/sum readouts (sum stays 6.00 around the whole ellipse), string-drawing caption, vertex check, constant = 2a. Part 2: grid and numbers go, generic figure with center (h,k), vertex a, focus c, co-vertex b; point moves to the co-vertex so each distance is a; right triangle gives b^2 + c^2 = a^2 then a^2 - c^2 = b^2 (used in Part 3 at the "factor" step). Part 3 opens on a joke warning caption ("a lot of algebra ahead, you do not need to know this"), then the distance formulas and the full derivation with X = x - h, Y = y - k as single terms. Chase found the derivation heavy; a hyperbola definition would be equally heavy (two squarings), so he may want it without the algebra.

**Current state:** Green — rendered at 1080x1350, wired, conicsGuide and player tests pass, layout audit clean. Chase had not yet watched it in the portal. Not deployed to Netlify.

**File size flag:** None.

**Next session:** Chase reviews the ellipse definition in the portal. Possible follow-ups: move a^2 - c^2 = b^2 from the end of Part 2 to where Part 3 needs it; a Definition of a Hyperbola clip (consider dropping the algebra); vertical-major-axis variant not done.
﻿## 2026-10-11 — Definition of a Parabola: focus triangle, set-equal, Part 3, ending; Conics Exit button; Drive HTML refresh

**Repos touched:** `Programs/` root (Manim Trial), `School Scrips/student-portal`, `School Scrips/student-session-kit`. Outside git: `My Drive/M2412/Unit 3 (10.2 - 10.7)/Conics/` (`index.html`, `player.html`, `Conic Sections.html`, `videos/`).

**Files changed:** `Manim Trial/parabola_directrix.py` (new `zoom_figure`, `focus_triangle`, `equate_distances`; derive reworked; ending trimmed; ~640 lines), portal `conicsGuide.ts` (Part 3 at 119.18, hold 216.22), `src/test/conicsGuide.test.ts` (3 parts), `conics-intro/parabola-directrix.mp4` + `-steps.json`, `ConicsGuideEntry.tsx` (header Exit button via `PortalQuizHeaderExitButton`, hidden on the menu).

**What worked:** The "If the focus is at (h, k+p)" slide keeps the figure (zoomed, curve and directrix redrawn so they stay on screen), writes the distance formula over it, then draws a point, the segment to the focus, horizontal and vertical legs, braces x-h and y-(k+p), and the Pythagorean beat, with leg colors matching the formula terms. The "set equal" slide clears the legs and draws the drop to the directrix, both segments get tick marks, and the equation sits on ONE line (sqrt(...) = y-(k-p), size 29 so it fits). Part 3 ("Part 3. Deriving the formula. Distribute...") cuts at the end of the set-equal hold (a step time, never mid-animation) and opens on a ~5 s hold. Ending now stops on the standard form with "The derivation for the other directions is similar" (example and purpose beats removed). Drive Conics HTML: re-copied directrix and hyperbola MP4s, directrix stops/3 parts, hyperbola tile and clip; Next no longer grays out mid-step (skips to the start of the next step and keeps playing) in `player.html` and `Conic Sections.html`.

**Current state:** Green — rendered, wired, conicsGuide + player tests pass, audit clean on the new marks; Chase had not yet watched the final Part 3 / ending in the portal. Not deployed to Netlify, nothing committed.

**File size flag:** None.

**Next session:** Chase reviews the focus triangle, set-equal, and Part 3 in the portal. Known: in Slow mode a part button shows the end of the previous slide (shared player convention, left alone). Later steps after set-equal still use the two-row equation layout; make them one line if he asks.
## 2026-10-11 — Hyperbola: Vertical clip (divide-by-4 opener)

**Repos touched:** `Programs/` root (Manim Trial, agent docs), `School Scrips/student-portal`, `School Scrips/student-session-kit`

**Files changed:** `Manim Trial/hyperbola_vertical.py` (new, ~440 lines; imports helpers from `hyperbola_horizontal.py`), portal `conicsGuide.ts` (new "Hyperbola: Vertical" entry, hold 179.11, Part 2 at 93.74, hyperbola group list), `src/test/conicsGuide.test.ts` (new test; ellipse-definition index 6 -> 7), `conics-intro/hyperbola-vertical.mp4` + `-steps.json`, `agent docs/recipes/portal-math-video-examples.md` (Conics row: all six graphing clips done).

**What worked:** Worksheet problem 2, (y+3)^2 - (x+2)^2 = 4. Opens with the divide step (`divide_bars`: bars and 4s morph into the fractions and the 1). Then the same beats as the horizontal clip with y in front: up/down first, vertical transverse axis, c triangle at the lower-right corner so the diagonal pivots down once (other focus only appears). Slope 2/2 -> 1 beat; c = sqrt(8) simplified to 2 sqrt(2) (added, not asked). Layout audit clean on all 42 marks; final frames checked. Draft 10 fps frames drift from the marks, so check frames from the 30 fps render only.

**Current state:** Green — rendered, wired, conicsGuide test passes; Chase has not yet watched it in the portal. Another agent was editing `conicsGuide.ts` at the same time; nothing committed.

**File size flag:** None.

**Next session:** Chase reviews Hyperbola: Vertical in the portal (Conics > Hyperbola > Vertical); drop the 2 sqrt(2) simplify beat if he wants it unsimplified.
## 2026-10-11 — Definition clip Part 2 figure, Auto pause between parts, formula chart order, Macro App lint fixes

**Repos touched:** `Programs/` root (Manim Trial, agent docs), `School Scrips/student-portal`, `School Scrips/Macro App`

**Files changed:** `parabola_directrix.py` (new `explain_figure`; Part 1 now ends on the vertex/p slide; wipe moved after the next caption), portal `conicsGuide.ts` (Part 2 at 43.18, hold 187.22), `useVideoExamplePlayer.ts` (`partStops`: Auto pauses at each part start; now ~726 lines), `conicsFormulas.ts` (parabola, ellipse, hyperbola), `conics-intro/parabola-directrix.mp4` + steps; Macro App `gradebookRestoreService.ts` (prefer-const), `macroAppStudentProgress.d.ts` (`multi`), `electron-app/gradebook-file-arbiter.js` (JSDoc types) so its pre-commit and pre-push pass; `agent docs/momentum-handoffs/latest.md`.

**What worked:** Part 2 drops the grid and numbers, shows y = k - p on the directrix, then braces y - k, p and the whole y - k + p on a generic figure. Found why Slow-mode holds landed after a wipe: a step time is just before the NEXT say(), so the board change must come after that say(). Macro App was blocked by one eslint error, one typing gap and one JS typecheck error; all fixed and pushed.

**Current state:** Green — rendered, wired, tests green, pushed; Chase has not yet watched Part 2 or the Auto pause in the portal.

**File size flag:** `useVideoExamplePlayer.ts` ~726 lines (cap 800, extract before 700).

**Next session:** Split `useVideoExamplePlayer.ts` (step/part navigation into its own module) per the momentum handoff, then Chase's review of the clip.

## 2026-10-10 — "Definition of a Parabola" clip: textbook captions, step-by-step expansion, Part 1 / Part 2 buttons

**Repos touched:** `Programs/` root (Manim Trial), `School Scrips/student-portal`

**Files changed:** `parabola_directrix.py` (~440 lines; new `derive`, `expand_left`, `arrows`, `stage`, `strike`), `parabola_directrix_{marks,steps}.json`; portal `conicsGuide.ts` (tile renamed "Definition of a Parabola", hold 162.67, `parts`), `conics-intro/parabola-directrix.mp4` + steps, `videoExamplesTypes.ts` (`parts`), `useVideoExamplePlayer.ts` (`jumpToPart`, exposes `stepTimes`), `VideoExamplesPlayerStage.tsx` (1 / 2 part row above Back/Next), `video-examples.css`, `conicsGuide.test.ts`.

**What worked:** Opens on the formal definition; the graph, focus and definition row clear when the derivation starts. The left-side expansion is worked below the equation: (y-k-p)^2 -> two factors with y-k kept as one term -> gold arrows distributing -> like terms combined -> substituted back; the right side just shows its answer. All captions rewritten in textbook voice with `$...$` math instead of spelled-out plus/minus. Part buttons jump to a step time; Part 2 must be the step time of the beat BEFORE the Part 2 caption (a step time is the END of a beat, so the part's own first step skips its caption).

**Current state:** Green — rendered 1080x1350, wired, vitest green; Chase has not yet used the 1/2 buttons in the portal; no Netlify deploy.

**File size flag:** `useVideoExamplePlayer.ts` ~690 lines (cap 800; extract before 700).

**Next session:** Chase's review of the Definition clip and the Part buttons; if he wants the buttons on other clips, add `parts` to those entries. Extract part/step navigation from `useVideoExamplePlayer.ts` before adding more.

## 2026-10-09 (late) — Parabola: Opens Left clip, "multiply both sides" recipe, always-wire-into-portal rule, Auto-mode Back fix

**Repos touched:** `Programs/` root (Manim Trial, agent docs), `School Scrips/student-portal`

**Files changed:** new `parabola_opens_left.py` (~300 lines; `LeftProblem`, class `ParabolaOpensLeft` extends `ParabolaOpensUp`), `parabola_opens_left_{marks,steps}.json`, `ANIMATION_STYLE_RECIPE.md` (new "Multiply both sides" entry), `solve_steps.py` docstring, `scene_audit.py` (a `DecimalNumber` is one readout, not per-digit text); portal `conicsGuide.ts` (entry 4, hold 99.78), `conics-intro/parabola-opens-left.mp4` + steps, `conicsGuide.test.ts`, `portalHomeApps.ts` ("4 clips"), `useVideoExamplePlayer.ts` (Auto-mode Back now keeps playing) + `src/test/useVideoExamplePlayer.test.ts`; root `AGENTS.md` + `portal-math-video-examples.md` (animations are always wired into the portal; Chase never views an MP4).

**What worked:** Worksheet problem 2, `-(1/4)y^2 = x - 2`: multiply both sides by -4 with the gold multiplier on each side and only the two 4s struck (negatives never mentioned), then the vertex with a "be careful, the order is flipped, (2, 0) not (0, 2)" beat, p = -1 opens left, focus (1, 0), focal width 4, vertical directrix x = 3, horizontal axis y = 0. Rendered 1080x1350, audit clean at 23 marks, wired in. Found the "stuck in Auto" report was the shared player: Back paused and disabled Pause/Resume; fixed with a failing-then-passing test.

**Current state:** Green — Chase has not yet watched Opens Left or the Back fix in the portal; no Netlify deploy.

**File size flag:** None.

**Next session:** Chase's review of Opens Left. Remaining parabola variants if wanted: opens down, opens right, equation from focus and directrix; `LeftProblem` only handles k = 0, h > 0, opening left.

## 2026-10-09 — Parabola directrix clip redone: definition + equation derivation, portal button labels, render-and-wire rule

**Repos touched:** `Programs/` root (Manim Trial, agent docs), `School Scrips/student-portal`, `School Scrips/student-session-kit`

**Files changed:** `parabola_directrix.py` (rewritten, ~230 lines), `parabola_directrix_steps.json`/`_marks.json`, `conicsGuide.ts` (directrix hold 57.44), portal assets `conics-intro/parabola-directrix.mp4` + `-steps.json`, `VideoExamplesPlayerStage.tsx` (clip nav buttons relabelled "Previous clip"/"Next clip"), root `AGENTS.md` + `portal-math-video-examples.md` (an animation is not done until rendered and playing in the portal, including edits).

**What worked:** Directrix clip is now ~57 s: one point, blue length to the focus, gold length straight down to the directrix, equal; slide the point keeping them equal and the parabola traces (3.5 s); state the definition; derive (x-2)^2 = 12(y+1) from sqrt((x-2)^2+(y-2)^2) = y+4; closing "why we care" captions. Rendered and copied into the portal; conicsGuide test passes 5/5. The two Back/Next pairs were step nav vs clip nav, now labelled differently (shared component, so Vectors & Projections picks it up too).

**Current state:** Green — rendered and in the portal; Chase has not yet watched it. No Netlify deploy.

**File size flag:** None.

**Next session:** If Chase wants the eccentricity (focus/directrix ratio) idea or the (x, y) label nudged off the curve, edit `parabola_directrix.py`, re-render, re-copy, update the hold constant. Portal needs `npm run deploy:prod` only when Chase asks.

## 2026-10-08 — Equations of Lines problem 4 (perpendicular), negative-plug animation, Slow-mode Back

**Repos touched:** `Programs/` root (Manim Trial, agent docs), `School Scrips/student-portal`

**Files changed:** `equations_of_lines.py` (589 -> 671: `PerpendicularStandard`, `Problem` accepts negative x / perpendicular / negative B, `coef()`, raw `y - (-4)` / `x - (-2)` plug row morphing to the plus), `equations_of_lines_perpendicular_{marks,steps}.json`, re-rendered problem 3; portal `equationsOfLinesExamples.ts` (+ problem 4, holds 93.56 / 93.22), `problem-3/4.mp4` + steps, `equationsOfLines.test.ts`, `equations-of-lines.css` (Back to problems label left-aligned), `useVideoExamplePlayer.ts` (Slow-mode Back stays enabled while playing; Back mid-animation returns to the hold just left).

**What worked:** Problem 4 (`8x - 4y = 8`, (-2, 6), standard form): given line -> y = 2x - 2 (m = 2) -> write 2/1, flip and change sign -> m = -1/2 -> the problem 3 beats -> `x + 2y = 10`. Plugging a negative point now shows the minus-negative first, then converges to the plus (problems 3 and 4). Audit clean, contact sheets read, vitest green.

**Current state:** Green — Chase has not yet watched problems 3-4 in the portal; no Netlify deploy.

**File size flag:** None (`equations_of_lines.py` under 700).

**Next session:** Chase's review of problems 3-4; Teacher Console still does not list Equations of Lines.

## 2026-09-28 — Slope-intercept inequality clips (three), white background, short style

**Files changed:** `slope_intercept_form.py` (new, 471), `math_notation.py` (new),
`test_math_notation.py` (new), `scene_style.py` (PAPER palette + `caption_color`),
`build_page.py` (3 `PAGES` rows, `SERIES` form → y-first → move-constant),
`ANIMATION_STYLE_RECIPE.md` (Chase's notation for negatives; white background), `README.md`,
marks JSONs, scratch pages `slope-intercept-form.html`, `slope-intercept-y-first.html`,
`slope-intercept-move-constant.html`.

**What worked:** Three clips from one data-driven module (a `Problem` record + two-line
subclass each): −2x − 3y < 6 (flip, negative moved to the top), −2y + 5x ≥ −8 (x term second,
flip), and 2y + 8 > −6x (x already across, so step 1 moves the 8; no swap, no flip). Chase then
asked for a short style: `brief=True` skips the goal/plan panel, captions only the steps
("Step 1: move the 8 by subtracting 8 from both sides", "Step 2: divide each term by 2"), and
plays cancel / bring-down / swap / simplify silently; the flip and "move the negative to the top
number" keep their captions, and the caption returns to Step 2 after a flip. `intro=True` keeps
the panel on clip 1 only. A `None` caption means the beat is silent. All three render 1080p30
with every audit mark clean.

**Current state:** Green — three clips linked Previous/Next; Chase reviewed the short style.

**File size flag:** `slope_intercept_form.py` 471 (new, under cap).

**Next session:** Wait for Chase's next variation; add it as a `Problem` with `brief=True`.

## 2026-09-27 — Vector series clips six and seven: ramp force and work

**Files changed:** `ramp_force.py` (new, 426), `work_wagon.py` (new, 418), `build_page.py`
(+2 `PAGES` rows, `SERIES` extended to `ramp-force` then `work-wagon`), `README.md` (+2 lines),
`agent docs/page-manifest.json` (series page now seven clips), new scratch pages
`ramp-force.html` and `work-wagon.html`, rebuilt `vector-series.html` and `pages.html`.

**What worked:** Both clips were modeled on `force_decomposition.py` from Chase's worksheet
screenshots. Clip six (problem 7) splits a 100 lb wagon's weight on a 20° hill into w₁ along the
ramp and w₂ into it, projects onto the unit vector r = ⟨cos 20°, sin 20°⟩, reads the minus sign in
w·r ≈ −34.20 as "down the hill", answers 34.2 lb up the hill, and closes on Force to remain
stationary = Weight × sin θ. Chase: "That looks good." Clip seven (problem 9) opens on what work
means (level pull: 5000 ft·lb), tilts the handle to 30°, keeps only F₁ = proj_PQ F, and reaches
W = ‖F‖‖PQ‖cos θ = 2500√3 ≈ 4330.13 ft·lb, checked as F · PQ, with a closing card on work.
Both clips render 1080p30 with every mark clean under `MANIM_AUDIT_STRICT=1`, and their contact
sheets were checked by eye. Gotcha hit again: Python heredocs mangle backslash escapes like `\t` in LaTeX strings,
so use the Edit tool. `Text` also drops the `·` in "ft·lb", so on-screen text says "foot-pounds".

**Current state:** Green — seven clips linked Previous/Next and on the series page.

**File size flag:** `work_wagon.py` 418, `ramp_force.py` 426 (new, under cap).

**Next session:** Chase called clip seven the last one; wait for his reaction to `work-wagon`
and `vector-series`.

## 2026-09-26 — Layout guardrails, and the cheap-model trial that failed review

**Files changed:** `scene_audit.py` (new, 438), `scene_layout.py` (new, 94),
`contact_sheet.py` (new, 173), `test_scene_audit.py` (new, 126), `test_scene_layout.py`
(new, 136), `scene_style.py` (+13), `docs/LAYOUT_GUARDRAILS.md` (new, 145),
`docs/CHEAP_MODEL_TRIAL.md` (new, 128), `ANGLE_BETWEEN_PLAN.md` (new, 87),
`angle_between_vectors.py` (new, 465 — by composer-2.5-fast, not accepted),
`build_page.py` (+1 `PAGES` row), `README.md` + `ANIMATION_STYLE_RECIPE.md` (pointers),
`agent docs/recipes/INDEX.md` (+2 rows), `agent docs/INDEX.md` (+1 row)

**What worked:** Built the layout guardrails so frame correctness stops depending on someone
looking at frames. `scene_audit.py` hangs off `Narrated.mark()` — a mark is already the moment
a frame must be readable, so every beat of every existing scene got checked for free, no new
mechanism. It checks text-vs-text overlap, off-frame margin, the caption band and minimum
readable type, and deliberately **not** text-vs-shape (an `Arrow`'s box spans its diagonal, a
`SurroundingRectangle` overlaps its contents by design — those pairs are pure noise). Every
finding carries a number to act on: which element, how far it overlaps, and the target center
coordinate or `.scale()` value. Proven both directions on `dot_product_directions.py` — clean
on all six marks with times unchanged, and flagging the pre-fix `east_dot_northeast` collision
when those two values are restored, which `test_scene_audit.py` now asserts without rendering.
Clean with zero false positives on `fraction_times_whole` (13 marks) and `dice_stats` (dense
chart, 24-25 elements). `scene_layout.py` declares `DIAGRAM`/`WORK`/`GAUGE`/`CENTER` measured
from clip one rather than guessed; `contact_sheet.py` montages one frame per mark with the
per-beat problem count burned in, reusing `build_page.PAGES` instead of a second registry.

Then the validation run: **composer-2.5-fast built clip two from a verified spec and failed
review.** It cleared ten real layout findings to nine clean marks in three renders, got every
number right, avoided the inverted-cosine trap and the textbook's part-(c) typo — and still
produced a slideshow of correct equations with no teaching motion and imprecise construction.
Chase rejected it and is out of tokens, so the clip is left as-is for another tool. Two honest
findings recorded in `docs/CHEAP_MODEL_TRIAL.md`: a cheap model can be trusted with spatial
*correctness* but not storyboard *taste*, and my spec deliberately left motion unspecified, so
what actually got tested was content-spec-only. Also: **the audit cannot see a missing
element** — composer resolved one overlap by deleting the gauge legend and that reports clean.

**Current state:** Green — guardrails working and both test files passing;
`angle_between_vectors.py` renders clean but is **not accepted** and is marked so in its
docstring. Clip one (`dot_product_directions.py`) is untouched and still awaiting review.

**File size flag:** `angle_between_vectors.py` 465 · `dot_product_directions.py` 453 ·
`scene_audit.py` 438 — all under the 700 extract threshold. `scene_style.py` now 108.

**Next session:** Clip two needs re-cutting for choreography and precision, not mathematics —
reuse the verified numbers in `ANGLE_BETWEEN_PLAN.md` as-is. Untested options are specifying
choreography transform-by-transform, or a higher-tier model writing `construct()` and the
`play()` calls while a cheap model writes only the `make_*` factories. Do not re-cut clip one
before Chase reviews it.

---

## 2026-09-22 — Rocket and lighthouse related-rates clips (worksheet #8/#9)

**Files changed:** `related_rates_lighthouse.py` (new, ~155 lines), `related_rates_rocket.py`
(new, ~140 lines), `build_page.py` (+2 `PAGES` rows)

**What worked:** Built the two "angle" problems from `3.11 Related Rates` — lighthouse (#9) and
rocket (#8) — matching the established square/ladder/drain/cone style: same navy/gold/blue/muted
palette, same flash/pulse-on-whole-unit mechanism, same threshold-triggered "the question" marker,
same render → `build_page.py` → verify-200 → link pipeline. Lighthouse went through one revision:
initially the light started at P and swept only rightward; Chase asked for the lighthouse centered
in frame with the beam sweeping the full range so negative values (left of P) are visible too —
redone with a symmetric sweep and signed (`+`/`-`) distance/angle readouts. Rocket is a genuinely
new pattern: its question is framed by **elapsed time** ("after 12 mins"), not a spatial value, so
the marker fires on a time threshold instead of a position tick, and it introduces a live `Angle`
mobject arc at the observer's vertex to visualize the elevation angle directly (first use of
`Angle` in this folder — cone's live relationship visual was an `Arrow`, not an arc). Rocket is
also the first "decelerating" clip since cone (dtheta/dt shrinks as the rocket climbs), while
lighthouse joined square/ladder in the "accelerating" family.

**Current state:** Green — both scenes render at 1080p30, are wired into `PAGES`, and their pages
return 200 at `http://127.0.0.1:8765/scratch/related-rates-lighthouse.html` and
`.../related-rates-rocket.html`.

**File size flag:** None — both scene files are ~140-155 lines, consistent with the other
self-contained `related_rates_*.py` files.

**Next session:** All worksheet problems with a natural related-rates animation are now covered
(square #1, drain #5, cone #6, ladder #7, rocket #8, lighthouse #9). Problems #2-4 (circle,
sphere-melting, sphere-surface-area) and #10-11 (business/demand) remain unbuilt if Chase asks for
more; nothing pending was requested this session.

## 2026-10-09 — Conics intro clip + Conics portal app (M2412)

**Repos touched:** Programs (Manim Trial, agent docs), School Scrips/student-portal, School Scrips/student-session-kit, School Scrips/Macro App

**Done:** `conics_intro.py` — 3D double cone, one slice tilting circle -> ellipse -> parabola (parallel to side, red generator) -> hyperbola (both nappes), ends on a four-curve board; ~42.6 s, 1080x1350. `scene_style.Narrated` gained a `caption_ready` hook so 3D scenes pin captions. New Conics gallery app in the portal (`conicsGuide.ts`, `ConicsGuideEntry.tsx`, route `conics`, precalc tile, `precalc/conics`), migration `079` pushed, Macro App teacher-console toggle + catalog + preview aspect. Not deployed to Netlify.

**Next session:** More conics clips = one more `examples` entry in `conicsGuide.ts` (update the tile subtitle count in `portalHomeApps.ts`). Degenerate cases (point/line/two lines) not built. Portal needs `npm run deploy:prod` when Chase asks.

