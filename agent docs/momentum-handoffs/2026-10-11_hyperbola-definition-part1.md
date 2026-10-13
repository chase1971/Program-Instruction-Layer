# Momentum handoff — Definition of a Hyperbola clip (Part 1 done; Parts 2-3 next)

**Written:** 2026-10-11

## Read first
- `agent docs/recipes/portal-math-video-examples.md` (§ Conics file map, "Definition clips") and `Manim Trial/ANIMATION_STYLE_RECIPE.md`.
- Exemplar to copy: `Manim Trial/ellipse_definition.py` (Part 1) + `Manim Trial/ellipse_standard_form.py` (mixin with Parts 2-3).
- Finished Part 1: `Manim Trial/hyperbola_definition.py` (`HyperbolaDefinition`, subclasses `HyperbolaHorizontal` from `hyperbola_horizontal.py`).
- `School Scrips/student-portal/AGENTS.md`; guide file `src/features/video-examples/conicsGuide.ts`.

## Objective and phase
Chase is building the "Definition of a Hyperbola" Conics clip as the twin of "Definition of an Ellipse" (3 parts in one MP4). He asked to **start with Part 1 only**, modeled on the ellipse one. Part 1 is **rendered, wired into the portal, tests green**. Chase has not yet watched it in the player. Parts 2 and 3 are not started.

## Chase's desired feel (carried from the ellipse/parabola definition clips)
- Captions read like a **textbook**: capitalized full sentences ("Part 1. A hyperbola is the set of all points where…"), never telegraphic. Math in captions uses `$...$`, never spelled-out words.
- Students follow algebra **step by step**: slow, one caption per move; treat `x−h` / `y−k` as ONE term (the ellipse used `X`, `Y` substitutions); show distribution arrows, not FOIL on single letters.
- Part 2 drops the grid/numbers and explains the **generic figure**; Part 3 opens with the "warning, lots of algebra, you do not need to know this" joke caption, then the full derivation to standard form.
- Put the next `say()` BEFORE any board wipe, or the Slow-mode hold lands after the wipe.

## Accepted decisions
- Same hyperbola as the graphing clip: `(x-1)^2/25 - y^2/49 = 1`, center (1,0), a=5, b=7, c=√74≈8.602, foci (1±√74, 0), vertices (-4,0) and (6,0). Constant = 2a = 10.
- Part 1 beats: definition `|d1−d2| = constant` → foci → one point on right branch, d1, d2, difference 10 (`|15.80−5.80|`) → point travels the branch → same on left branch → vertex (6,0), distances 13.60 and 3.60, brace "2a=10" → `|d1−d2| = 2a`.
- Opening caption dropped "By definition," so it fits in 3 lines (audit flagged 4 lines as off-frame).
- Plane view x∈(-9,11), y∈(-6.5,6.5), center y −1.82; `T_LIMIT` 0.78 keeps the dot inside the rows.
- Portal entry has **no `parts` yet** (one part ⇒ no part buttons). Add `parts` (0 / part-two / part-three times) once Parts 2-3 exist.

## Rejected / don't rediscover
- Showing the hyperbola before the point traces it (the ellipse clip traces it too; copied).
- A second player mechanism. Reuse the shared player; no new hooks.
- No Netlify deploy unless Chase says so in that message.

## Implementation state
- Created: `Manim Trial/hyperbola_definition.py`, `hyperbola_definition_marks.json`, `hyperbola_definition_steps.json` (hold = **59.56 s**).
- Portal assets copied: `student-portal/src/assets/video-examples/conics-intro/hyperbola-definition.mp4` + `-steps.json`.
- `conicsGuide.ts`: new constants `CONICS_HYPERBOLA_DEF_START_SECONDS` (0) / `CONICS_HYPERBOLA_DEF_HOLD_SECONDS` (59.56), new entry "Definition of a Hyperbola" (examples index 8), added to the `hyperbola` group.
- `src/test/conicsGuide.test.ts` updated (group list + new test); `conicsGuide` + `useVideoExamplePlayer` tests pass (16). `tsc` errors exist only in unrelated test files (`classworkData.test.ts`, `guidedPracticeArchive.contract.test.ts`).
- Recipe doc updated with a short hyperbola-definition note. Session scorecard bumped.
- **Nothing committed or pushed** this session (root repo and `student-portal` both dirty with this work).
- Any clip change = final render `-r 1080,1350 --fps 30 --disable_caching` from `Manim Trial` (`.venv\Scripts\python.exe -m manim …`), copy MP4 + steps JSON to `conics-intro/`, update hold/part constants and the test.

## Open questions and constraints
- **Pre-existing mismatch (flagged to Chase, not fixed):** Macro App `renderer/src/utils/videoReport/conicsWatchReport.ts` `CONICS_CLIP_LABELS` puts Definition of an Ellipse at index 5, but the portal has it at 7 (and Hyperbola H/V at 5/6). The new hyperbola clip is index 8 in the portal and is missing from the Macro App list. Category headers assume contiguous groups. Needs a decision (reorder portal vs. make Macro App follow portal order) before analytics columns are trustworthy.
- Part 2/3 design for the hyperbola is a **proposal**, not approved: Part 2 generic figure with h, k, a, b, c, point moved to the vertex/co-vertex-equivalent, right triangle giving **c² = a² + b²** (plus, where the ellipse had minus); Part 3 distance formula for d1, d2, then `|d1 − d2| = 2a` squared step by step (two cases of sign collapse to one by squaring), ending at `X²/a² − Y²/b² = 1`. Chase found the ellipse algebra heavy; expect the same.
- Root rules: no GUI launch / browser without asking; handoffs are statements not questions.

## Exact next step (do this first)
Build Part 2 of the hyperbola definition: create a mixin `Manim Trial/hyperbola_standard_form.py` modeled on `ellipse_standard_form.py` (`figure_part`), call it from the end of `HyperbolaDefinition.construct` (replace the final `hold` beat with a `part-one-end` beat, as the ellipse does), dry-run for audit, then final render and wire `parts` into the guide. Confirm with Chase only if he wants Part 3's algebra in the same pass.
