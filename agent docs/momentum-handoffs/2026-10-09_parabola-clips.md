# Momentum handoff — Parabola clips for the Conics gallery

**Written:** 2026-10-09

## Read first
- `agent docs/recipes/portal-math-video-examples.md` (delivery standard) and `Manim Trial/ANIMATION_STYLE_RECIPE.md`.
- `Manim Trial/parabola_walkthrough.py` (the exemplar for the rest of the parabola set).
- Plan file: `C:\Users\chase\.claude\plans\i-want-to-make-merry-lighthouse.md`.

## Objective and phase
Chase is building the pre-calc Conics video set (intro clip exists; ellipse formula chart exists in the portal). Parabolas come next. Clip 1 of the parabola set, `(x − 2)² = 12(y + 1)` (worksheet problem 1), is **done and in the portal** as Conics gallery entry 2, "Parabola: Opens Up". Next is more parabola clips.

## Chase's desired feel
He teaches a **process, not formulas**. He does not recite the formula; he explains how to do it. Order for the clip: x squared → opens up/down; vertex (h, k) and why the signs are opposite; p from 4p ÷ 4; positive → up; plot vertex; focus is p up; focal width |4p| → left/right half of it from the focus; draw curve; directrix p the other way (dashed); axis of symmetry splits the middle; vertical lines are `x =`, horizontal are `y =`.

## Accepted decisions
- New file `parabola_walkthrough.py`, class `ParabolaOpensUp(Narrated, Scene)` with a `Problem` dataclass (h, k, c; verifies with Fraction). Currently built only for h > 0 > k, opens up, c divisible by 4. Reuses `tex`/`var`/`signed` from `equations_of_lines.py`.
- Phase 1 is algebra on the full board; phase 2 keeps the answers as a two-column list above the graph, filled in as the graph finds each one. Graph = `NumberPlane` x −5..9, y −5..3, centered y = −2.05.
- Colors: vertex/curve/end dots red, focus dot and dashed lines blue, arrows gold, h/k gold.
- Vertex reasoning (Chase's correction, applied): caption "The vertex is (h, k)." → "The h and k values come out as the opposite of the numbers you see." → "So (h, k) equals (2, −1)." → "Plug these values in, and you get the original expression." The 2 and −1 fly up and **replace h and k in the general-form equation already on screen**; then `y − (−1)` becomes `y + 1` in place.

## Rejected directions
- Do **not** write a second equation underneath for the plug-in demo. Chase explicitly rejected that.
- Do not state the vertex as "For this one the vertex is (2, −1). Here is why."

## Current implementation state
- Final render done at 1080x1350/30fps, audit clean at all 19 marks. Hold = **86.56 s**, 19 Slow-mode steps.
- Portal: `src/features/video-examples/conicsGuide.ts` (entry 2 + `CONICS_PARABOLA_START_SECONDS`/`HOLD_SECONDS`), `src/config/portalHomeApps.ts` (tile says "2 clips"), `src/test/conicsGuide.test.ts` (3 tests pass). Assets: `src/assets/video-examples/conics-intro/parabola-opens-up.mp4` and `-steps.json`.
- Everything is **uncommitted and unpushed**. No Netlify deploy. Chase has **not yet watched** the final render in the portal (never launch a window without asking). Scorecard bump for the clip was logged before the vertex rework; no bump yet for the rework.
- Pre-existing tsc errors in `classworkData.test.ts` and `guidedPracticeArchive.contract.test.ts` are not from this work.

## Open questions and constraints
- Which clip is next is unconfirmed (proposals only): opens down, opens left/right (y squared), writing the equation from focus/directrix. `Problem` currently rejects those cases, so extend it or add subclasses.
- Whether a parabola formula chart page (ready: false in `conicsFormulas.ts`) is wanted is unconfirmed and separate.
- Clip is 86.6 s, longer than the ~35 s recipe norm; Chase has not complained.
- Rules: no GUI/browser/preview without asking; handoffs are statements, not questions; final render is `-r 1080,1350 --fps 30 --disable_caching` from `Manim Trial` with MiKTeX on PATH; draft with `-ql`; `contact_sheet.py parabola_walkthrough` works because the marks file name matches the module (per-scene marks files need a wrapper); per-file cap 800 lines.

## Exact next step
Tell Chase (flat statement) to watch Parabola: Opens Up in the Conics tile, then ask one question: which parabola variant is next. Do not build until he answers.
