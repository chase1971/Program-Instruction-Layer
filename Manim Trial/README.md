# Manim Trial

Local experiment for AI-directed mathematical animation, separate from Math App Studio.

Reusable style guidance: [ANIMATION_STYLE_RECIPE.md](ANIMATION_STYLE_RECIPE.md).
Keeping frames from colliding: [docs/LAYOUT_GUARDRAILS.md](docs/LAYOUT_GUARDRAILS.md) — the
audit that runs at every pause mark, the layout regions, and the contact sheet.

## Animation examples

- `slope_intercept_form.py`: the first **white-background** clip (`PAPER_*` palette in
  `scene_style.py`). Goal y = mx + b; x and y go on opposite sides, so move the x term
  first, then divide by the number next to y. −2x − 3y < 6 (an inequality — the sign is kept, and flips
  when dividing by −3): add 2x (it cancels on the
  left), 6 and 2x are not like terms so the right side is written 2x + 6, divide every
  term by −3, simplify to y > −2/3 x − 2, then move the negative to the top number (−2 over 3; Chase's graphing convention, stated without a reason). Meant as the first of several "ways to get to
  slope-intercept form" clips. `http://127.0.0.1:8765/scratch/slope-intercept-form.html`.
  Same module, second scene `SlopeInterceptYFirst`: −2y + 5x ≥ −8 → flips to
  y ≤ 5/2 x + 4; solid line, shade below (x term second, slope positive, so no
  negative-on-top beat) →
  `http://127.0.0.1:8765/scratch/slope-intercept-y-first.html`. Each clip is one `Problem`
  record at the top of the file; a new equation is a new record plus a two-line subclass.
- `fraction_times_whole.py`: multiply a fraction by whole numbers — write as n/1,
  cancel first, then multiply tops. Each product is two factors only (e.g. 1/3 × 15
  separately), then `2/7` with a negative and `2/7 × 3/8` simplified.
  `http://127.0.0.1:8765/scratch/fraction-times-whole.html`.
- `angle_between_vectors.py`: clip two — derives the angle formula: shrink u and v onto the unit circle, dot the unit vectors, combine into (u·v)/(‖u‖‖v‖) = cos θ. Then works (a)-(c) by swinging one arrow while the gauge follows. `http://127.0.0.1:8765/scratch/angle-between-vectors.html`.
- `vector_projection_shadow.py`: clip three — the projection as the shadow u casts on v's line under light perpendicular to v. u longer than v (shadow runs past v), then v longer (shadow inside v), then only v's length changes and the shadow stays put. Builds proj_v u = (u·v/‖v‖²) v. `http://127.0.0.1:8765/scratch/vector-projection-shadow.html`. Clips one → two → three → four are linked with Next/Previous buttons (`SERIES` in `build_page.py`).
- `vector_decomposition.py`: clip four — what decomposing means (3i + 4j is u split along the axes), a perpendicular reference swinging around u and settling on v, why only w₁ acts along v, w₁ as clip three's shadow, then the worksheet problem u = 3i + 4j, v = 10i + 2j: project, subtract, check. Verified fractions are in the module docstring. `http://127.0.0.1:8765/scratch/vector-decomposition.html`.
- `force_decomposition.py`: clip five, replacing the standalone `vector_projection_force.py` — the 8 N / 22 N at 50° problem worked as a decomposition: u₁ along v (the shadow, what the question asks for) and u₂ across it; v's size never moves the shadow; u₁ ≈ 1.768v (v stretched to the shadow); the ‖v‖'s cancel to 22 cos 50° ≈ 14.14 N; u₂ = u − u₁ ≈ ⟨0, 16.85⟩; closing card with Chase's names (parallel component / projection, orthogonal component / rejection vector). `http://127.0.0.1:8765/scratch/force-decomposition.html`.
- `ramp_force.py`: clip six — worksheet problem 7, the 100 lb wagon on a 20° hill. w = ⟨0, −100⟩ splits into w₁ along the ramp and w₂ into the hill; w₁ is the projection onto the unit ramp vector r = ⟨cos 20°, sin 20°⟩; w·r ≈ −34.20 (the minus sign means down the hill), so it takes about 34.2 lb up the hill. Closes on Force to remain stationary = Weight × sin θ. `http://127.0.0.1:8765/scratch/ramp-force.html`.
- `work_wagon.py`: clip seven — worksheet problem 9, what work means. A level 50 lb pull over 100 ft is 5000 ft·lb; tilt the handle to 30° and only F₁ (F's shadow on PQ) does work, F₂ lifts and does none. W = ‖proj_PQ F‖‖PQ‖ = ‖F‖‖PQ‖cos θ = 2500√3 ≈ 4330.13 ft·lb, checked as F · PQ. `http://127.0.0.1:8765/scratch/work-wagon.html`.
- **The whole vector series on one page:** `http://127.0.0.1:8765/scratch/vector-series.html` — `build_series()` in `build_page.py` walks `SERIES` and stacks one player per clip. Each player borrows its video from that clip's own page, so the series page is a few KB and follows every re-render. Clip pages show no text under the player (Chase's rule) — the `PAGES` blurb is a record only.
- `dot_product_directions.py`: the dot product as shared direction, taught before it is
  calculated — you travel east at 1 mph and a friend travels north, so the similarity gauge
  sits empty and only then does the arithmetic produce the zero that says the same thing. The
  friend turns northeast and the gauge fills to √2/2 ≈ 0.707. Closes on the limit of that
  reading: `u·v = ‖u‖‖v‖cos θ` collapses to `cos θ` only because both magnitudes are 1.
  `http://127.0.0.1:8765/scratch/dot-product-directions.html`.
- `gcf_division.py` and `solve_factors.py`: factor and solve a quadratic.
- `two_step_equation.py`: solve `3x + 7 = 22` by undoing the addition, then the
  multiplication, with each operation written beneath both sides. Delivered at
  `http://127.0.0.1:8765/scratch/two-step-equation.html`.
- `dice_sums.py`: part 1 of the two-dice series — every ordered roll behind each sum
  from 2 to 12, ending on 36. `http://127.0.0.1:8765/scratch/dice-sums.html`.
- `dice_stats.py`: part 2 — the chart tips into a histogram, a normal curve lays over it,
  then mu = 7 and sigma = 2.42. `http://127.0.0.1:8765/scratch/dice-stats.html`.
  Reconstructs part 1's final frame from `dice_sums`, so the two cut together.
- `dice_sampling.py`: part 3 — opens on a definition card, then four rolls of the pair
  make one sample; 100 sample means rain onto part 2's axis, the bell pulls in to
  sigma / root n = 1.21, and the closing beat runs it backwards to recover mu and sigma
  from the samples. Ends on the part 4 hook: a non-normal population whose sampling
  distribution goes normal anyway. `http://127.0.0.1:8765/scratch/dice-sampling.html`.
  Seeded at 132 so the draw always looks bell-shaped; it borrows `hx`, `BASE_Y` and
  `HOLD` from `dice_stats` so all three parts share one x-axis.

- `dice_products.py`: part 4 — the **product** of two dice, a spiky population with
  eighteen values that never occur (no 7, no 11, no 13). Its sampling distribution still
  goes bell-shaped, mu = 12.25 carries across, the naive sigma = 8.94 is struck through,
  and sigma / root n = 4.47 matches the observed 4.482. Ends on the Central Limit Theorem.
  `http://127.0.0.1:8765/scratch/dice-products.html`. Seeded at 429 — `PART4_PLAN.md`
  records how that seed was chosen, so re-run that search before changing it.

- `combine_parts.py`: stitches parts 1-4 into one 4:27 video, `DiceSeries.mp4`. All four
  render 1920x1080 at 30 fps from the same pipeline, so the streams are copied, not
  re-encoded — lossless and quick. Straight cuts, no transitions: part 2 reconstructs
  part 1's final frame, so that seam is invisible. Also merges the parts' pause marks into
  `dice_series_marks.json`, offset into the combined timeline.
  `http://127.0.0.1:8765/scratch/dice-series.html` (17.9 MB page — a few seconds to load).
  Re-run it after re-rendering any part, then re-run `build_page.py`.

American spellings on screen — "center", never "centre".

**`PART4_PLAN.md`** is the handoff doc part 4 was built from — verified numbers, the seed
search, the beats and the pitfalls. Kept as the record of why the clip is shaped this way.

`build_page.py` inlines a rendered MP4 into a page under `agent docs/scratch/`. Add a row
to its `PAGES` table and run it; Chase gets the `127.0.0.1:8765` link, never a file path.

Shared helpers: `math_notation.py` (`mathtex()` — Chase's negatives and negative fractions;
see the recipe's "Chase's notation"), `scene_style.py` (palette, caption line, `PACE`, pause marks),
`scene_audit.py` + `scene_layout.py` + `contact_sheet.py` (layout guardrails — see the doc
above) and `dice.py` (die faces, white first die / blue second die).

## Pace and pause marks

`scene_style.PACE` scales every explicit `run_time` and every `wait` — 1.2 plays the
clip 20% faster. Scenes call `self.mark('name')` on a hold, and `write_marks()` drops
a JSON sidecar so an embedding app knows where it may pause without hand-transcribed
timestamps going stale on the next render. A mark is also where the **layout audit** runs,
so the render log says whether every held frame is readable.
- `ellipse_definition.py`: centered ellipse, focal distances, fixed-sum meter,
  inside/outside comparison, and string-based tracing. Source references are linked
  in `ellipse-player.html`; rendered video is embedded in the delivered page at
  `http://127.0.0.1:8765/scratch/ellipse-definition.html`.

## Setup

The project lives in Programs at `Manim Trial/` (same repo as the instruction layer).
Pull Programs on the laptop if this folder is missing.

### First time on a new laptop

**Toolbar tile (separate from install):** dwell **`Wire Manim Toolbar.vbs`** once. That
patches the sibling `electron-toolbar` repo and adds **Manim Setup** to the 📚 Launcher Panel.
Log: `wire-launcher.log`. Restart electron-toolbar if the tile does not appear.

**Install Manim deps:** dwell **`Setup Manim Trial.vbs`** (no console). Log: `setup.log`.
Setup also runs the toolbar wire step when it finishes successfully.

Or run **`setup.ps1`** directly. It installs or verifies:

| Tool | Purpose |
|---|---|
| Python 3.12+ | runtime |
| uv (`python -m uv`) | virtualenv + locked deps from `uv.lock` |
| FFmpeg | encodes frames to MP4 |
| MiKTeX | LaTeX for `MathTex` equations |
| Manim Community 0.21.0 | Python package in `.venv` |

`setup.ps1` uses winget for FFmpeg and MiKTeX when they are missing. After winget
installs, you may need a **new terminal** before PATH updates; rerun setup if checkhealth
still fails.

Manual fallback if winget is unavailable:

- Python: https://www.python.org/downloads/ (check **Add to PATH**)
- FFmpeg: `winget install Gyan.FFmpeg` or https://www.gyan.dev/ffmpeg/builds/
- MiKTeX: https://miktex.org/download (per-user install under
  `%LOCALAPPDATA%/Programs/MiKTeX`)
- Then: `python -m pip install uv` and `python -m uv sync` in this folder

### Already set up

- Python 3.12: existing per-user Python installation.
- uv: invoke as `python -m uv`.
- Manim Community 0.21.0: project `.venv`; dependencies pinned in `uv.lock`.
- MiKTeX: per-user installation under `%LOCALAPPDATA%/Programs/MiKTeX`.

## Agent rendering

Use `render.ps1` from this directory for the installation-check scene. It sets the
MiKTeX path for that process and renders an MP4 without opening a player.
The output is `media/videos/verify_render/480p15/DivisionCheck.mp4`.

The check scene is deliberately minimal: fraction/exponent typesetting and a
transition to a simplified expression. It is not the finished teaching animation.

Chase directs changes through speech. Do not hand him terminal commands.
Never use Manim's `-p`/`--preview` or open a player without per-run permission.
