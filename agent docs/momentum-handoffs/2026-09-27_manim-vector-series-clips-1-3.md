# Momentum handoff — Manim dot-product series (clips 1–3 done)

**Written:** 2026-09-27 · **App:** `Manim Trial/` · **Topic:** linked series of vector teaching clips

---

## Objective and current phase

Chase is building a linked series of short Manim teaching clips on vectors, played in order
from pages at `http://127.0.0.1:8765/scratch/<slug>.html` (Next/Previous buttons join them):

1. `dot_product_directions.py` → `dot-product-directions` — dot product as shared direction (accepted earlier; do not re-cut).
2. `angle_between_vectors.py` → `angle-between-vectors` — **done this session, Chase approved.**
3. `vector_projection_shadow.py` → `vector-projection-shadow` — **new this session, Chase: "that looks really good."**

Chase will say what the **next clip** is. His words were ambiguous ("the next one would be …
this one, we haven't done this one yet"). Plausibly it relates to the older standalone
projection clips, `vector_projection_force.py` (the 8 N / 22 N force at 50° worked problem)
or `dot_product_projection.py`, but **do not assume. Wait for his instruction.**

## Chase's desired feel

- **Derive, don't reveal.** He wants a formula built on screen from the picture: "show that by
  scaling it down all you're really doing is taking the unit vector of both and then that's
  what generates that formula." Build each result in front of the student, never state it.
- **Intuition first, arithmetic confirms.** The gauge stays empty until the computation fills it.
- **Spell out SOH CAH TOA literally**: `cos θ = ADJ / HYP`, then ADJ → the projection and
  HYP → ‖u‖, *as an animation* (the labels on the diagram and in the equation change together).
- **Two panels** when a derivation has two ideas: length first, then direction/vector.
- He cares that each step has a *why*, e.g. how the magnitude-of-projection formula becomes
  the projection *vector*.
- Interpretation he approved for a negative cosine: **"About 22% of v's direction points against u."**

## Accepted decisions

- Every diagram object is built from one state/view (origin + scale, or u/v lengths) and animated
  with `rebuild(mob, lambda alpha: build(...))` from `angle_between_vectors.py`. Nothing is
  positioned after it is built. This is what fixed the cheap-model draft's detached arrows.
- Clip 2 order: long vectors → `u·v` → "clip one only worked at length 1" → û = u/‖u‖, v̂ = v/‖v‖
  (arrows shrink onto the unit circle, zoom in) → û·v̂ = (u/‖u‖)·(v/‖v‖) → combine → "= cos θ" →
  θ = arccos → gauge → problems (a)–(c), each swinging one arrow while the gauge follows it.
- Clip 3: light perpendicular to a **tilted** v, and the shadow is proj_v u. Cases: u longer than v
  (shadow past v's tip), then v longer (shadow inside), then only v's length changes and the
  shadow stays put ("v only supplies the direction"). Then the two panels described above.
- Pages chain through the `SERIES` dict in `build_page.py` (slug → next slug).

## Rejected directions — do not rediscover

- **Right-triangle / adjacent-side beat in clip 2**: Chase removed it ("doesn't make sense for
  the problem you do"). The gauge must not be filled before part (a)'s arithmetic.
- **Showing the formula first and rearranging it** (clip 2's first re-cut): rejected in favour of deriving it from unit vectors.
- **DNA / two-parents analogy for projection**: Chase proposed it. I left it out and explained
  why: a projection of u onto v is always a copy of v, so the "child" would carry none of the
  father's own direction, which teaches the wrong idea. He did not ask for it back.
- A cheap model (`composer-2.5-fast`) building a clip: rejected, see `Manim Trial/docs/CHEAP_MODEL_TRIAL.md`.

## Current implementation state

- All three clips are rendered at 1080p30. Every pause mark audits clean under
  `MANIM_AUDIT_STRICT=1`, and the frames were checked by eye with contact sheets.
- Changed or new this session, **all uncommitted**:
  - `angle_between_vectors.py`
  - `vector_projection_shadow.py` (new, ~400 lines)
  - `vector_projection_shadow_marks.json`
  - `angle_between_vectors_marks.json`
  - `build_page.py` (the `SERIES` Next/Previous buttons, new `PAGES` row, blurbs)
  - `README.md`
  - `docs/CHEAP_MODEL_TRIAL.md` (a re-cut section explaining the three placement bugs)
  - `docs/LAYOUT_GUARDRAILS.md` (the `TransformFromCopy` gotcha)
  - The regenerated `agent docs/scratch/*.html` pages
- **Gotchas learned:**
  - `TransformFromCopy` leaves the padded *copy* on screen. Use `ReplacementTransform(src.copy(), dst)`
    (`copy_into` in `vector_projection_shadow.py`).
  - Gold fill under ~.25 opacity reads gray on navy.
  - FadeIn adds on top, so give background shapes `set_z_index(-1)`.
  - `build_page.py` rebuilds every page. One page can fail to write if it is open or locked; rerun it.
  - Python heredocs with `\` escapes via bash silently fail to replace. Use the Edit tool or a script file.

## Open questions and constraints

- Which clip is next: Chase will say.
- Never open a player or browser (no `-p`). Hand Chase the `127.0.0.1:8765` link only.
- The verified numbers for clip 2 live in `ANGLE_BETWEEN_PLAN.md`. Don't recompute them.
- Commit and push only at end of session or on "put on GitHub".

## Exact next step

Ask nothing. Wait for Chase's description of the next clip. Then read `Manim Trial/README.md`,
`Manim Trial/docs/LAYOUT_GUARDRAILS.md` and `Manim Trial/ANIMATION_STYLE_RECIPE.md`, and model the
new scene on `vector_projection_shadow.py`: state-built parts, `rebuild`, `copy_into`, and
hand-built `fraction()` rows. When it's done, add it to `PAGES` and `SERIES` in `build_page.py`.
