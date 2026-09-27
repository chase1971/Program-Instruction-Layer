# Momentum handoff — Manim vector series (clips 1–4 done)

**Written:** 2026-09-27 · **App:** `Manim Trial/` · **Topic:** linked series of vector teaching clips

---

## Objective and current phase

Chase is building a linked series of short Manim teaching clips on vectors, played in order
from pages at `http://127.0.0.1:8765/scratch/<slug>.html` (Next/Previous buttons join them via
`SERIES` in `build_page.py`):

1. `dot_product_directions.py` → `dot-product-directions` — accepted earlier; do not re-cut.
2. `angle_between_vectors.py` → `angle-between-vectors` — approved.
3. `vector_projection_shadow.py` → `vector-projection-shadow` — approved ("that looks really good").
4. `vector_decomposition.py` → `vector-decomposition` — **built this session; Chase: "All right,
   that's good"** after two requested additions (below). About 2:35.

**Next clip (Chase named it, not yet started):** redo the **force problem** that uses
decomposition. It is "one we already did" — the older standalone `vector_projection_force.py`
(8 N / 22 N forces at 50°) — but done "differently, based on how we've started trying to piece
by piece explain everything that's going on." He has not described the new version's beats yet.

## Chase's desired feel

- **Derive, don't reveal; every step gets a *why*.** Build each result from the picture.
- **Say what things *are*, in plain words, not just show them.** His correction on clip 4: the
  clip showed w₁ and w₂ but never said what they were. His words: w₁ is "all the parts of the
  vector that's going in the direction that V is going," w₂ is "the part of the vector that
  absolutely [has] nothing to do with V."
- **Name what every number means.** His second correction: say what 19/52 *is* — "the scale
  factor … to make the size of V the size of the shadow," compared to making a unit vector
  ("here we're not making a unit vector").
- Intuition first, arithmetic confirms. Two panels when a derivation has two ideas.
- Interpretation approved in clip 2 for a negative cosine: "About 22% of v's direction points against u."

## Accepted decisions (clip 4)

- Beats: what decompose means (u = 3i + 4j is already u split along the axes, pink 3i + gold 4j)
  → a dashed perpendicular reference swings around u ("any perpendicular pair works") → zoom
  out, v grows, reference settles on v → **define the pieces** (card on the right: w₁ "the part
  of u that goes in v's direction", w₂ "the part of u that has nothing to do with v", u = w₁ + w₂
  "every bit of u is in one or the other"; a copy of v slides out, shrinks and lands on w₁; a dot
  slides along w₁ and its shadow ring moves, climbs w₂ and the ring stays put) → **why: a ramp
  along v** (only w₁ moves you along it; w₂ presses into it — sets up the force problem) →
  clip three's light: w₁ is the shadow → plan card (project, subtract, check) → Step 1 with the
  **19/52 beat** (copy of v shrinks by 19/52 onto w₁; note under diagram
  19/52 = ‖w₁‖/‖v‖ ≈ 3.73/10.20 ≈ 0.37; "like a unit vector … here, to the shadow's length")
  → Step 2 (3 and 4 written over 26) → Step 3 (w₂·v = 0, w₁ + w₂ = ⟨3,4⟩) → boxed i/j answer.
- Colors: u blue, v `V_COLOR` red, w₁ = clip three's pink `SHADOW`, w₂ gold.
- Verified fractions are in the `vector_decomposition.py` docstring; don't recompute.

## Rejected directions — do not rediscover

- Clip 2: right-triangle beat removed; formula-first-then-rearrange rejected.
- DNA / two-parents analogy for projection: left out (a projection is always a copy of v).
- Cheap model (`composer-2.5-fast`) building clips: rejected, `Manim Trial/docs/CHEAP_MODEL_TRIAL.md`.
- Definition card laid out as two columns (symbol | words) was too wide and shrank below the
  type floor; words now sit under each symbol like the plan card.

## Current implementation state

- `vector_decomposition.py` (~590 lines; cap 800, extract before 700), rendered 1080p30, all
  12 marks clean under `MANIM_AUDIT_STRICT=1`, frames checked by eye (contact sheet + mid-beat
  ffmpeg grabs under `media/audit/`).
- Helpers inside it worth reusing: state-dict diagram (`to_screen`, `frame`, `pieces`), `morph`
  rebuilding only shown parts, `rebuild_now`, `shrink_copy_of_v` / `land_on_w1`, `m()` colored
  rows keyed by 'u','v','w1','w2', `settle()` into `BELOW_GIVEN`.
- `build_page.py`: new `PAGES` row + `SERIES['vector-projection-shadow'] = 'vector-decomposition'`.
  `README.md` lists clip four.
- **All uncommitted** (this session's plus the prior session's clips 2–3 work): `Manim Trial/*`,
  regenerated `agent docs/scratch/*.html`, session-tracking files, handoffs.
- Gotchas: `TransformFromCopy` leaves the padded copy — use `copy_into`. Gold fill <.25 reads gray.
  `build_page.py` can fail on a locked page (e.g. `dice-series.html`) — rerun. Python heredocs
  via bash mangle `\f`/`\a` in LaTeX strings (`\frac` → form feed) — use raw strings in a
  quoted `<<'EOF'` script file, or the Edit tool.

## Open questions and constraints

- The force clip's shape is Chase's to describe. Plausible (proposal, not approved): rebuild
  `vector_projection_force.py` on clip 4's machinery — decompose the force along/across a
  ramp or the other force, define each piece in words, name what each number means.
- Never open a player or browser (no `-p`). Hand Chase only the `127.0.0.1:8765` link.
- Commit/push only at end of session or on "put on GitHub".

## Exact next step

Read `Manim Trial/README.md`, `Manim Trial/docs/LAYOUT_GUARDRAILS.md`,
`Manim Trial/ANIMATION_STYLE_RECIPE.md`, then `vector_projection_force.py` (the old version)
and `vector_decomposition.py` (the model). Wait for Chase's description of the redone force
clip; when he gives it, build it as clip five and add it to `PAGES` and `SERIES`
(`'vector-decomposition': '<new slug>'`).
