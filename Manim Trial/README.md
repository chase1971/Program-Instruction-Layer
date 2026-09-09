# Manim Trial

Local experiment for AI-directed mathematical animation, separate from Math App Studio.

Reusable style guidance: [ANIMATION_STYLE_RECIPE.md](ANIMATION_STYLE_RECIPE.md).

## Animation examples

- `gcf_division.py` and `solve_factors.py`: factor and solve a quadratic.
- `two_step_equation.py`: solve `3x + 7 = 22` by undoing the addition, then the
  multiplication, with each operation written beneath both sides. Delivered at
  `http://127.0.0.1:8765/scratch/two-step-equation.html`.
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
