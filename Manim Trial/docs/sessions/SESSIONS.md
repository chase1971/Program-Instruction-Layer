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
