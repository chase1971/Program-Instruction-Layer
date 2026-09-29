# Momentum handoff — Manim slope-intercept inequality clips (two done, Chase approved)

**Written:** 2026-09-28 (day-valid only — if you are reading this on a later date, say so before acting)
**App:** `Manim Trial/`
**Status:** Two clips finished, rendered 1080p30, pages built. Chase: *"it looked perfect."*
Nothing committed yet (mid-session rule — wait for "put on GitHub" / end of session).

> The previous `latest.md` (Macro App gradebook browser coordinator plan, also written today by
> another task) is preserved at `2026-09-28_gradebook-browser-coordinator-plan.md`.

---

## Read first

1. This file.
2. `Manim Trial/ANIMATION_STYLE_RECIPE.md` — especially **"Chase's notation — negatives and
   dividing by a negative"** (new today) and the **white background** bullet in Visual style.
3. `Manim Trial/slope_intercept_form.py` — the exemplar. Every clip is a `Problem` record +
   a two-line subclass; the beats are shared.
4. `Manim Trial/docs/LAYOUT_GUARDRAILS.md` — the audit/render loop.

---

## Objective and current phase

Chase is building a set of short clips on **getting a line (now: a linear inequality) into
slope-intercept form**, "different ways you have to get a line into slope-intercept form."
Headed for the classroom projector and eventually the **student portal**.

Done:
- `SlopeInterceptForm` — **−2x − 3y < 6** → y > (−2/3)x − 2 → negative moved to the top →
  graph: intercept −2, down 2 right 3, **dashed**, **shade above**.
  `http://127.0.0.1:8765/scratch/slope-intercept-form.html`
- `SlopeInterceptYFirst` — **−2y + 5x ≥ −8** (x term second) → y ≤ (5/2)x + 4 → graph:
  intercept 4, up 5 right 2, **solid**, **shade below**.
  `http://127.0.0.1:8765/scratch/slope-intercept-y-first.html`
- Linked Previous/Next (`SERIES` in `build_page.py`).

Phase: waiting for Chase's next equation / variation.

---

## Chase's desired feel (his words where they matter)

- **White background** from now on — navy clips were "hard to see" on the projector; clips go
  to the student portal. `PAPER_*` palette in `scene_style.py`, `caption_color = PAPER_MUTED`.
- Teaching script he dictated: goal is y = mx + b; "the x's and y's need to be on opposite
  sides"; **move the x over first**, then **divide every term** by the number next to y;
  constant and x term "are not like terms" so write them **x term first** (2x + 6);
  simplify. Plain classroom captions.
- **Negative on top of the fraction**: caption says only *"Move the negative to the top
  number."* — **no reason on screen** ("they'll understand when they see it"). His reason
  (graphing: top number goes up/down, bottom always right) is in the recipe, not the clip.
- **Negatives are a short dash**, not a full minus ("it just looks too big"). Subtraction
  keeps the full minus.
- **A negative never widens a fraction bar** — "the negative can just hang off."
- Inequality: keep the sign in slope-intercept form; **flip when dividing by a negative** —
  its own beat, sign pulses red and comes down flipped.
- Loves the graph beat ("I love the graph").

## Accepted decisions

- One module, data-driven: `Problem` dataclass (captions, tokens, divisor, answer, top_answer,
  rise_run, intercept, graph window). New clip = new record + `class X(SlopeInterceptForm):
  problem = X_DATA`.
- `math_notation.py` owns the notation: `mathtex()` (swaps negatives for `NEG`),
  `hanging_fraction()`, `unsigned()` (what a drawn division bar spans). `test_math_notation.py`
  passes. **Always build math via `mathtex()`/the scene's `tex()`**, never raw `MathTex`.
- Negative vs subtraction is decided by position: a `-` opening the expression or following
  `= < > + -` (or `\leq \geq`) is a negative. Write a subtraction as its own `'-'` part.
- Graph: same unit on both axes (`GRAPH_HEIGHT` / y-span), anchored at `GRAPH_RIGHT`; line and
  shading clipped to the window (`line_through_box`, `half_plane`). Pick `window` per problem so
  the rise fits (clip 2 uses `(-7, 5, -3, 11)`). Run label goes on the side outside the
  rise/run triangle.
- The "move the negative to the top" beat runs only when `top_answer` is set (negative slope).

## Rejected directions — don't rediscover

- **Shading "below" for clip 1.** Chase said "less than … shade below," but the sign flips to
  `>`; shading **above** is correct. Told him; he accepted.
- A *scaled-down* minus as the negative — replaced by a `\rule` dash (`NEG`).
- `\frac{\llap{-}\,2\,}{3}` padding the numerator — detached the dash from the 2. Padding goes
  on the **denominator**.
- `TransformFromCopy` — use `copy_into` (from `vector_projection_shadow.py`).

## Current implementation state

New/changed (uncommitted): `Manim Trial/slope_intercept_form.py` (415 lines),
`math_notation.py`, `test_math_notation.py`, `scene_style.py` (PAPER palette +
`caption_color`), `build_page.py` (2 PAGES rows + SERIES link), `README.md`,
`ANIMATION_STYLE_RECIPE.md`, `agent docs/INDEX.md` + `agent docs/recipes/INDEX.md` (trigger
words: "how I write negatives · dividing by a negative · fraction bar too long"), marks JSONs,
two scratch pages. Both scenes: audit all marks clean (13 / 14), final 1080p30 rendered.

Gotchas hit this session:
- **`contact_sheet.py` looks up by folder** and takes the first `PAGES` row — with two scenes
  in one module it sheets the wrong clip. Grab frames with ffmpeg from the marks JSON instead.
- Contact-sheet frames at 480p15 lag the marks by ~1 s (frame rounding); a mid-animation
  thumbnail is not a bug — check a frame 1 s later.
- Python patch scripts: use raw strings for anything with `\frac`, `\leq`, `\llap`
  (`\f` became a form feed twice).
- Delete `media/videos/slope_intercept_form/480p15` before `build_page.py` so it takes 1080p.

## Open questions / constraints

- Chase framed these as "some different ways" — more variations likely (e.g. y term already
  positive, fractions in the original, x term on the right, ≤ / > cases, no flip). None
  specified yet — ask which equation, don't invent.
- Subtraction signs stay full minus; Chase hasn't objected. If he says the minus before a term
  also looks too big, that's a one-line `negatives()` change — ask first.
- Never open a player/browser; hand Chase `127.0.0.1:8765` links only.

## Exact next step

Wait for Chase's next equation. To add it: write a `Problem` record in
`slope_intercept_form.py` (verify the algebra and a test point in the docstring first), add a
subclass, draft-render (`-ql`), read the `[audit]` lines, eyeball frames via ffmpeg, final
render `-qh --fps 30`, add a `PAGES` row + extend `SERIES`, run `build_page.py`, give the link.
