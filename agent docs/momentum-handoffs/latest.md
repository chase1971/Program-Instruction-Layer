# Momentum handoff — Definition of a Parabola clip + video example player split

**Written:** 2026-10-11

## Read first
- `Manim Trial/ANIMATION_STYLE_RECIPE.md` (§ Solving an equation on screen), `agent docs/recipes/portal-math-video-examples.md`
- `School Scrips/student-portal/AGENTS.md`; recipes `INDEX.md` for file-size rules

## Objective and phase
Conics app (student portal) tile **"Definition of a Parabola"** (Manim `Manim Trial/parabola_directrix.py`, class `ParabolaDirectrix`). It is rendered, wired and pushed (portal + root, `main`). Chase had not yet watched the latest build in the player when this was written. Latest asks all done: two parts, Auto pauses between parts, formula chart order parabola / ellipse / hyperbola.

## Exact next step (do this first)
**Split `School Scrips/student-portal/src/features/video-examples/useVideoExamplePlayer.ts`** (now ~726 lines; extract before 700, hard cap 800). Pull the step/part navigation out into its own hook or module: `jumpToPart`, `partStops` + the `stopAtPartStart` rAF check, `stepNext` / `stepBack` / `pauseSlowAtStep`, `stepIndexAtTime`. Keep behavior identical. `src/test/useVideoExamplePlayer.test.ts` and `src/test/conicsGuide.test.ts` must stay green. One owner per concept; do not build a second player mechanism. No GUI launching without asking.

## Chase's desired feel (his words matter)
- Captions must read like a **textbook**, with capitalized sentences: "Part 1. The definition of a parabola is the set of all points…", "If the focus is at (h, k+p), then the distance … is found by applying the distance formula." Never telegraphic fragments. Math in captions uses `$...$` (LaTeX font), never spelled-out "plus/minus".
- Students must follow the algebra **step by step**: slow, one caption per move. He may make the derivation a bonus test question.
- For expansion: treat y−k as ONE term; show distribution arrows (like the in-clip `expand_left`), not FOIL on single letters.
- Generic figure beats specific numbers: Part 2 removes the grid/axes/y+4 and explains y = k − p and y − k + p with braces on the figure.

## Accepted decisions
- Two parts in one MP4. `parts` on the guide entry (`conicsGuide.ts`: `CONICS_DIRECTRIX_PART_TWO_SECONDS = 43.18`, hold 187.22); the player shows **1 / 2** buttons above Back/Next (`VideoExamplesPlayerStage.tsx`). A part's start time must be a step time (steps are the END of a beat, 0.04 s before the next caption), so Part 2 starts at the Part 1 hold.
- Auto mode **pauses at the start of each part after the first** (Chase asked); jumps (Next/Back/part buttons) never pause.
- Ordering rule learned: put the next `say()` BEFORE any board wipe or the Slow-mode hold lands after the wipe.
- Formula chart order is parabola, ellipse, hyperbola (`conicsFormulas.ts`).

## Rejected / don't rediscover
- A separate "Part 2" title slide (too brief; merged into the first Part 2 caption).
- Word-form captions ("minus", "plus"), "Definition of a parabola:" colon style.
- Do not deploy to Netlify unless Chase asks in that message.

## Implementation state
- Pushed: root repo `Programs` and `School Scrips/student-portal`; Macro App lint/typecheck blockers fixed and pushed.
- Any change to the clip means: final render `-r 1080,1350 --fps 30 --disable_caching` from `Manim Trial` (`.venv\Scripts\python.exe -m manim …`), copy MP4 + `parabola_directrix_steps.json` into `student-portal/src/assets/video-examples/conics-intro/`, update hold and part constants in `conicsGuide.ts`, update `conicsGuide.test.ts`. "Done" = rendered and playing in the portal.
- Another agent was editing `conicsGuide.ts` (clip groups: parabola / ellipse / hyperbola / definition); re-read it before editing.

## Open
- Whether Chase wants Auto-pause on other clips (only this clip has `parts`).
- Chase has not yet reviewed Part 2's figure and the auto-pause in the portal.
