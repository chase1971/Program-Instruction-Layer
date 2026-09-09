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

The project lives in Programs at `Manim Trial/` (same repo as the instruction layer).
Pull Programs on the laptop if this folder is missing.

### First time on a new laptop

Dwell-click **`Setup Manim Trial.vbs`** in this folder (no console, no typing).
Progress and errors go to `setup.log`. Setup also adds a **Manim Setup** tile to the
electron-toolbar Launcher Panel (📚 grid) when `electron-toolbar` is present as a sibling
folder under Programs.

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
