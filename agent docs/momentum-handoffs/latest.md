# Momentum handoff — Car position/area animation: Part 2 fixed, Parts 3 and 4 need the same treatment

**Written:** 2026-10-12

## Read first
- This file, then the animation itself: `C:\Users\chase\My Drive\M2413\Unit 4 Integration\car-position-area-animation.html` (single self-contained file, outside git, ~480 lines). Read the whole `<script>` before editing.
- Sibling, older and **not** updated to the new controls: `fundamental-theorem-animation.html` (same folder; F(x)=x²+3x beside f(x)=2x+3). Leave it alone unless Chase asks.
- Style exemplar for the page shell: `My Drive\M2413\Unit 3 Derivative Applications\Blank\linear-approximation-animation.html`.
- Root `AGENTS.md` rules that bite here: never open a browser/GUI on Chase's screen without asking (verify headlessly, then hand off as a flat statement, never "want me to…?"); no commit/push mid-session.

## Objective and phase
Chase teaches M2413 Unit 4 (integration). His worksheet has three cars: constant v=20, linear v=2t, non-linear v(t)=t(10−t). Goal of the animation: let him **grasp and explain why plugging into the position function p gives the area under the velocity graph**. He can do the mechanics; the gap is the *why*. The page has 4 part buttons: 1 constant speed, 2 changing speed, 3 why p equals the area, 4 a curve geometry can't handle.

**Part 1 and Part 2 are done and Chase approved Part 2 ("That looks good").** Parts 3 and 4 are first drafts Chase has **not reviewed yet**. The job: restructure them the way Part 2 was restructured (below).

## The core explanation (accepted — keep it)
Bucket / odometer idea: the total-distance bucket **is** the odometer p(t). A sliver of area v·dt is one tick of the odometer because p′=v (in time dt the odometer rises p′·dt = v·dt). Adding slivers = adding ticks = total rise of the odometer = p(b)−p(a). So p(5)=25 is not a shortcut around the sum; the odometer had been adding the whole time. Any antiderivative works since a constant cancels in p(10)−p(0). Also true here: p(0)=0, so p(t) *is* "area from 0".

## Chase's desired feel (his words matter)
- **Small, discrete, readable screens.** He wants each idea on its own screen, built up one piece at a time, then the pieces shown together. Not a sweep he has to catch.
- **Start from zero**, not from an arbitrary t (he rejected "t=3" and "t=1 to 2" first slivers: "start from zero to one… then one to two, then two to three, then show all the results together").
- Show the **actual numbers** being multiplied (speed × time = distance) and drop them into the **bucket**; he wants units to make sense.
- Show what a chunk **misses** (speed changes inside the chunk) and that it only becomes exact as dt→0 (limit). He wants: chunks 1 s → 0.5 s → 0.1 s, "better the closer we get".
- **No clutter**: he rejected a one-line note `dt = 1 → 90   dt = 0.5 → 95 …` as "too clustered, hard to follow"; a small table was accepted instead.
- **Write the integral the way the lesson argues it**: `lim_{dt→0} Σ v(t)dt = ∫ … = 100` (limit of the sum first), not "integral = limit".
- **No auto-play, no fades.** Everything on a step prints at once. Only genuinely moving things animate, and then he wants a visible indicator.

## What was done to Part 2 (the pattern to repeat)
Old Part 2 had a 0.1 s sliver at t=3 and an auto-cycling chunk sweep. Replaced by 8 static steps: setup → chunk 0→1 (speed 0, adds 0 m, misses everything) → chunk 1→2 (2 m) → chunk 2→3 (4 m, bucket 6 m) → all ten 1 s chunks (90 m, off by 10) → 0.5 s chunks (95) → 0.1 s chunks (99) → limit table + limit-first integral → "why does p(10)=100 work instantly?".
Mechanics worth reusing:
- `kind:'p2one'` with `c` (chunk start) draws previous chunks blue, current chunk orange + pink "missed" triangle, connector lines to the zoom box, bucket = cumulative.
- `zoom(vtxt, prodtxt, o, dtxt, miss)` — `miss={v0,v1}` scales the schematic (17.5 px per m/s) and puts `speed × 1 = distance` above it.
- `kind:'p2chunk'` with `dt` draws all chunks, bucket total, missed amount.
- `p2limit` draws a 3-column table (chunk size / total / off by) in the empty right half.

## Controls and engine (accepted; don't redesign)
- No Auto. **Each step plays once then stops.** Real motion is declared in the `DUR` map (seconds) near the top of the script; **a step not in `DUR` is static**: no bar, Next flashes immediately, everything visible at once. Currently animated: `p1bucket`, `p1repeat`, `both5`, `stack`, `slope`.
- Real Pause/Play (resumes instantly), progress bar **only for animated steps** and it is a **draggable scrubber** with a knob (click/drag = jump within the step); dots are clickable (jump to step, replay from start). Next flashes (`.ready`) when the step is done; disabled on the last step.
- Layout fits one window height (flex column, SVG shrinks), controls never scroll off. Everything is drawn as a pure function of `ts` (time in step), which is what makes scrubbing work. `p` is forced to 1 (no fades).
- `?part=2&step=3` (0-based) freezes a frame for checking.

## Next step: do Part 3 and Part 4 "the Part-2 way"
Treat these as **proposals** (Chase has not seen them, so confirm direction by showing him the result, not by asking a menu):

**Part 3 (why p equals the area), v=2t, p=t².** Current steps: `both5` (animated sweep to t=5, "area so far" vs "p(t)" readouts), `ticks` (two callouts using the t=3, dt=0.1 sliver — the same arbitrary-start problem Chase rejected in Part 2), `stack` (animated 10 slivers stacking into the odometer rise), `slope` (animated slide), `concl`.
- Replace the sweeps with **discrete static screens at chosen times** (e.g. t=1, 2, 3, then 5): each shows area so far = p(t) side by side, built one at a time, then "all together". Use exact numbers (area ½·t·2t = t²: 1, 4, 9, 25).
- Redo the sliver/tick explanation **starting from zero**: one small piece from 0, then the next, etc., each showing its area (v·dt) *and* the odometer tick (p′·dt) as the same number, then show the ticks stacking into p(5)−p(0)=25 one piece at a time (static steps, or keep `stack` animated only if it stays clear — add a table/readout, not a long note line).
- Keep the slope step as stops (slide to t=2, pause and explain: height of v = slope of p; then t=4), the way Chase liked in the earlier fundamental-theorem file: "when it gets to two and four, stop and explain".
- Keep the conclusion: p(10)−p(0)=100−0=100 is the sum of every sliver.

**Part 4 (v=t(10−t), p=5t²−t³/3, p(10)=500/3≈166.7).** Current: setup, geom ("no formula"), slope, plug. Make it the payoff of Parts 2–3: geometry is stuck → chunks approach the answer → p(10) gives it exactly.
- Verified chunk totals (left-endpoint, same method as Part 2): **dt=1 → 165; dt=0.5 → 166.25; dt=0.1 → 166.65; limit 166.67 (=500/3)**. A table like Part 2's limit table fits.
- **Caution:** the curve rises then falls, so left-endpoint chunks overshoot on the falling half and undershoot on the rising half; the Part 2 "missed (orange)" shading and "off by" wording are **one-sided there and would be wrong**. Show over/under honestly or just show totals vs the true 166.67.
- Then the slope step (stops, not a continuous slide) and the plug step.

**Conventions to follow while doing it:**
- Captions: textbook sentences, `$…$` math, step by step. LaTeX backslashes must be **doubled inside JS strings** (`\\cdot`, `\\lim`). **Gotcha:** Bash/Python heredocs silently collapsed backslashes this session (captions rendered as "2cdot1"). Edit captions with the Edit/Write tools, then scan the file for single backslashes (build the char with `chr(92)`; the only legitimate singles are in the regex inside `renderMath`).
- Headless check before handing off: syntax-check the extracted `<script>`, and run a stub-DOM Node harness that calls `draw()` for every part × step × several `ts` values (the harness exposes `draw/cur/setPart` via a `window.__t` shim). Don't launch a browser unasked.
- Handoff to Chase is a flat statement: what changed, what to look at (e.g. "open it, check Part 3 steps X–Y"), no "want me to…".

## Open questions
- None blocking. Whether the older `fundamental-theorem-animation.html` should get the new controls/layout is undecided (Chase hasn't asked).

## State
- Files changed this session (all outside git, in `My Drive\M2413\Unit 4 Integration\`): `fundamental-theorem-animation.html`, `car-position-area-animation.html` (new). Nothing committed or pushed; repo changes are only these handoff docs.
- Verification so far: `<script>` syntax OK and all 4 parts × all steps draw without exceptions headlessly. **Chase has watched Parts 1–2 and approved Part 2; Parts 3–4 unreviewed.**
