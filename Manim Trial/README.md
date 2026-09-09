# Manim Trial

Local experiment for AI-directed mathematical animation, separate from Math App Studio.

Reusable style guidance: [ANIMATION_STYLE_RECIPE.md](ANIMATION_STYLE_RECIPE.md).

## Animation examples

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

Shared helpers: `scene_style.py` (palette, caption line, `PACE`, pause marks) and
`dice.py` (die faces, white first die / blue second die).

## Pace and pause marks

`scene_style.PACE` scales every explicit `run_time` and every `wait` — 1.2 plays the
clip 20% faster. Scenes call `self.mark('name')` on a hold, and `write_marks()` drops
a JSON sidecar so an embedding app knows where it may pause without hand-transcribed
timestamps going stale on the next render.
- `ellipse_definition.py`: centered ellipse, focal distances, fixed-sum meter,
  inside/outside comparison, and string-based tracing. Source references are linked
  in `ellipse-player.html`; rendered video is embedded in the delivered page at
  `http://127.0.0.1:8765/scratch/ellipse-definition.html`.

## Setup

- Python 3.12: existing per-user Python installation.
- uv 0.12.10: installed with Python pip; invoke as `python -m uv`.
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
