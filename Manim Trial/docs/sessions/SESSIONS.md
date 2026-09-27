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
