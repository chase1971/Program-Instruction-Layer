# Momentum handoff: FTC animation series (portal)

**Written:** 2026-10-19

## Read first
- `Manim Trial/fundamental_theorem_calculus.py` (4 scenes: FtcTriangleSquare, FtcAddedArea, FtcSqueezeProof, FtcPositionConnection)
- `Manim Trial/build_ftc_series_page.py` (builds the review page, see below)
- `agent docs/recipes/portal-math-video-examples.md` (render + wiring recipe), `Manim Trial/ANIMATION_STYLE_RECIPE.md`
- Portal: `School Scrips/student-portal/src/features/video-examples/fundamentalTheoremGuide.ts`, test `src/test/fundamentalTheoremGuide.test.ts`

## Objective and phase
Chase is reworking the four-clip Fundamental Theorem of Calculus animation so the logic builds
the way he teaches it (his Word-doc narrative: displacement = area under v(t); Riemann sum
approximates it; limit = definite integral; FTC links integral to antiderivatives).
**Clips 1 and 2 are done, rendered, wired, tests green. Clips 3 (proof) and 4 are next.**
Review page: http://127.0.0.1:8765/scratch/fundamental-theorem-calculus.html (also the portal
tile "Fundamental Theorem of Calculus"). Chase approved clip 1 ("looks good"); clip 2 ending was
just revised and he has not yet reviewed the final render.

## Accepted decisions
- Use **s(t)** for position (not p). Never show the position function/graph before it is derived.
- Clip 1 (done, approved): v(t)=2t only -> triangle (base T, height 2T) -> A(T)=∫0^T 2t dt ->
  =½(T)(2T)=T² -> then slide left, draw s(t)=t² graph -> at T=10 both give 100 m. No duplicate
  area formula on top.
- Clip 2 (done, awaiting review): v(t)=t(10-t), no geometry formula -> left-Riemann rectangles
  n=5,10,20,40 with readout (160.00 ... 166.56) -> limit -> ∫0^10 v dt -> "displacement = final
  position minus initial position" = s(10)-s(0) -> "need s(t)" (s(t)=?) -> antiderivative
  s'(t)=v(t) -> s(t)=5t²-t³/3, s(10)-s(0)=166.67-0 matches sums. 11 steps, hold 40.71 s.
- Clip 3 = the proof. Plan (proposal Chase accepted in outline): the strip beats (A(t+h)-A(t) ≈
  v(t)h, divide by h, A'(t)=v(t)) that were REMOVED from old clip 2 move to the start of clip 3,
  ahead of the squeeze (lower/upper rectangles). Old strip code is in git history
  (`git log -p -- "Manim Trial/fundamental_theorem_calculus.py"`, the pre-2026-10-19 FtcAddedArea).
  Clip 4 ties it together: s and A both have derivative v, differ by a constant, so area = position
  change; position is an antiderivative of velocity. Chase has NOT yet reviewed/approved the exact
  clip 3 and 4 content; confirm with him or show the plan before big rewrites.

## Rejected
- Showing the position graph or formula in clip 2 before deriving it ("if you don't know the
  position function you can't draw it").
- The "sums approached 166.67 ... why? that is the proof" ending (replaced by displacement/antiderivative).
- Formulas duplicated in two places on the board (clip 1).

## Implementation state
- Both clips rendered (`-r 1080,1350 --fps 30`), MP4 + steps JSON copied to
  `student-portal/src/assets/video-examples/fundamental-theorem-calculus/`, guide hold constants
  updated (triangle 26.25, added-area 40.71), clip 2 tab label "2 · Riemann sums to integral",
  test pause counts [6, 11, 6, 9], vitest 3/3 green. Layout audit clean on both.
- Scratch page rebuilt via `Manim Trial/.venv/Scripts/python.exe build_ftc_series_page.py`
  (CLIPS list in that file holds hold seconds + labels; update when clips 3/4 change). A
  transient write error occurred once; retry fixed it.
- Nothing committed or pushed. Scorecard bumps logged for both clips.
- Squeeze and position clips still the old versions (hold 20.27 / 28.48; test counts 6 and 9).

## Constraints
- Done = rendered + copied into portal + guide holds + test passes (no handoff of "go render").
- No GUI launches, no Netlify deploy, no em dashes, ask-before-assume (one question).
- Python edits through bash heredocs mangled backslashes (`\D`, `\t`); use the Edit tool or raw strings.
- Layout audit gotchas: keep tall integral lines separated (~0.8 units), axis label `t` placed RIGHT of axis end.

## Exact next step
Ask Chase (or propose briefly) whether clip 3 should open with the moved strip beats then the
squeeze, then rework `FtcSqueezeProof` accordingly (final render, assets, guide hold, test, rebuild page).
