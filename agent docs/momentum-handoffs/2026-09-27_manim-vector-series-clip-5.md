# Momentum handoff — Manim vector series (clips 1–5 done, series page built)

**Written:** 2026-09-27 · **App:** `Manim Trial/` · **Topic:** linked series of vector teaching clips

---

## Objective and current phase

Chase is building a linked series of short Manim teaching clips on vectors, played from pages
at `http://127.0.0.1:8765/scratch/<slug>.html` (Next/Previous via `SERIES` in `build_page.py`):

1. `dot_product_directions.py` → `dot-product-directions` — accepted; do not re-cut.
2. `angle_between_vectors.py` → `angle-between-vectors` — approved.
3. `vector_projection_shadow.py` → `vector-projection-shadow` — approved.
4. `vector_decomposition.py` → `vector-decomposition` — approved; **light beam removed this session**.
5. `force_decomposition.py` → `force-decomposition` — **built this session; Chase: "Yeah, this
   is great."** Then beam removed at his request. About 2:14.

Plus **`vector-series.html`** — all five on one page (Chase chose "one page, five videos" over a
combined single video). Built at the end of this session; Chase has not reacted to it yet.

**Phase:** everything he asked for is done. No next clip has been named.

## Chase's desired feel

- **Derive, don't reveal; every step gets a *why*; say what each vector *is* and what each
  number *means*.** (Carried from clip 4, and clip 5 was built on it and approved.)
- **Vocabulary comes after the work.** His notes define u₁ = proj_v u as the **parallel
  component / projection of u onto v** and u₂ = u − u₁ as the **orthogonal component /
  rejection vector**; ‖proj_v u‖ = "how much of one vector lies in the direction of another,
  ignoring any component that's perpendicular." Clip 5 works the problem calling them u₁/u₂,
  then a closing summary card gives the names.
- **The shadow is a way of thinking, not something to keep drawing.** His words: once the
  triangle is drawn, "the shadow part doesn't actually add anything… You can still reference it,
  though. I reference it all the time." → mention the shadow in captions, never draw the beam
  again after clip 3.
- **No text under the play button** on any clip page — "I don't need it there."

## Accepted decisions

- Clip 5 beats: question (8 N v, 22 N u, 50°) → split into u₁/u₂ with a words-under-symbol
  card (u₁ "the part of u that goes in v's direction", u₂ "the part of u that has nothing to do
  with v", u = u₁ + u₂, "How much? → ‖u₁‖") → u₁ is u's shadow (caption + Indicate, no beam)
  → v resized 8→20→4→8 N, shadow never moves ("v only tells us which direction") → formula
  with clip two's u·v = ‖u‖‖v‖cos θ ≈ 113.13, ‖v‖² = 64, u₁ ≈ 1.768v → **1.768 beat**: copy of
  v *stretches* to the shadow (contrast: clip 4 shrank by 19/52) → ‖u₁‖ ≈ 14.14 N → ‖v‖'s struck
  out to leave 22 cos 50°, cos 50° ≈ 0.643 = "about 64% of u's length lies along v" → u₂ with v
  on the x-axis: u ≈ ⟨14.14, 16.85⟩, u₂ ≈ ⟨0, 16.85⟩, u₂·v = 0 → boxed answer → summary card
  in Chase's definition wording with "here: 14.14 N / 16.85 N" beside each line.
- Colors: u blue, v `V_COLOR` red, u₁/w₁ pink `SHADOW`, u₂/w₂ gold.
- Old `vector_projection_force.py` page kept as a standalone link, out of the `SERIES` chain.
- **No-text rule is rung 1:** `build()` in `build_page.py` no longer renders the blurb, pause
  list, or source line; `mark_list` deleted. `PAGES` blurbs remain as a record only (comment says so).
- **Series page loads videos from each clip page** (fetch page → slice data URI → blob URL),
  so it is 2.7 KB and never duplicates ~38 MB of base64 into git. `build_series()` walks `SERIES`.

## Rejected directions — do not rediscover

- Drawing clip three's light beam in later clips (removed from clips 4 and 5).
- A single combined ~11-min video for the vector series (Chase picked one page, five videos).
- Inlining all five videos into the series page (38 MB, git bloat).
- Carried over: clip 2 right-triangle beat; formula-first reveal; DNA/two-parents analogy;
  cheap model building clips (`Manim Trial/docs/CHEAP_MODEL_TRIAL.md`); two-column definition card.

## Current implementation state

- `force_decomposition.py` (~450 lines), 1080p30, all 10 marks clean under `MANIM_AUDIT_STRICT=1`,
  contact sheet and mid-beat frames checked by eye. Verified numbers in its docstring.
- `vector_decomposition.py` re-rendered 1080p30 without the beam, all 12 marks clean.
- `build_page.py`: new `PAGES` row, `SERIES['vector-decomposition'] = 'force-decomposition'`,
  no-text template, `SERIES_PAGE` + `build_series()`. All pages rebuilt.
- `agent docs/page-manifest.json`: `vector-series.html` filed under Math explainers; index rebuilt.
- `README.md` lists clip five and the series page.
- Series-page extraction tested headlessly with node (all five yield valid MP4s); **not viewed in
  a browser** — no one has watched it play yet.
- **All uncommitted** (this and the prior sessions' Manim work, scratch pages, tracking files,
  handoffs). Session-tracking bumps done for both deliverables.
- Gotchas: python heredocs through bash mangle `\f`/`\a` in LaTeX strings — use the Edit tool;
  `Text` at font 24 is ~0.19 units per character, so card lines over ~40 chars get shrunk by
  `fit_into`; the `answer` box needs `.shift(LEFT*.2)` room on the right; delete the 480p15
  folder before `build_page.py` (it takes the first glob hit).

## Open questions and constraints

- What comes next in the series is Chase's call — nothing proposed or approved.
- Never open a player or browser; hand Chase only `127.0.0.1:8765` links.
- Commit/push only at end of session or on "put on GitHub".

## Exact next step

Read `Manim Trial/README.md`, `Manim Trial/docs/LAYOUT_GUARDRAILS.md`, and
`Manim Trial/ANIMATION_STYLE_RECIPE.md`, then ask Chase for his reaction to
`http://127.0.0.1:8765/scratch/vector-series.html` or his next clip. Model any new clip on
`force_decomposition.py` and add it to `PAGES` and `SERIES` (`'force-decomposition': '<new slug>'`).
