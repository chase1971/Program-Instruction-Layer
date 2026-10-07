# Momentum handoff — Composite clip closing redesign (NOT yet built) + TC preview auto-flip

Written: 2026-10-06 (America/Chicago)
Workspace: C:\Users\chase\Documents\Programs
Phase: The **Composite Examples** Manim clip is built and shipped to the portal asset through
the "overlap" ending. Chase has now dictated a **redesign of the closing board** (domain-of-the-
composite section). **Nothing of that redesign is implemented — he said "don't actually do
this, put it in a note."** The next agent builds it.
**Nothing committed or pushed** (not asked; this is a momentum handoff, not end-of-session).

## Read first

1. Root `AGENTS.md` — no GUI/browser launches without per-run permission; **never deploy to
   Netlify unless Chase says so in that message**; handoff is a statement, not a question;
   file cap 800 / extract before 700.
2. **`Manim Trial/ANIMATION_STYLE_RECIPE.md`** — house solve style, Chase's negative notation
   (`mathtex`), white `PAPER_*` palette.
3. **`Manim Trial/composite_domain.py`** (~350 lines) — the clip. Helpers it uses:
   `math_caption.py` (captions with real LaTeX), `tick_number_line.py` (numbered number line),
   `scene_style.py`, `solve_steps.py`.
4. Portal side: `School Scrips/student-portal/src/features/video-examples/compositeExamplesGuide.ts`
   (hold-seconds constant) and the asset
   `School Scrips/student-portal/src/assets/video-examples/composite/composite-examples.mp4`.

## Objective

Teach composite-function domains in one clip: f(x)=x²+6, g(x)=√(x−2) → (f∘g)(x)=x+4, domain
[2,∞). Audience: students on phones (portrait 4:5 clip). Chase reviews it in the Macro App
**Teacher Console preview** (embedded portal, dev origin `127.0.0.1:5340` reads the portal's
local `src/assets`, so a re-render + copy shows up after the preview's Refresh).

## Chase's desired feel (his language)

- Math in captions must be **LaTeX** (variables, numbers, intervals) — never plain text.
- Domains sit **next to** the function (not stacked below), but with a real gap; work is
  **centered**, not drifting down-left.
- Solving steps tight together; show a **proper number line** (ticks + integer labels, arrows,
  dot on 2, arrow right) like `sqrt_domain_range.py`'s, then interval notation.
- Show **cancelling**: red slash through the √ and the ² ("Squaring cancels the square root").
- He likes the composite build animation (x² → (x)² → g flies in) — **do not change it**.
- Wants each screen readable: when merging, **clear clutter**.

## What is built and working now (all in `composite_domain.py`)

Two functions each with domain beside; solve `x−2≥0` (+2 under both sides, strikes) → `x≥2`;
number line (ticks −7..7, dot on 2, ray right, −∞/∞ labels under the arrow ends) → `Domain:
[2,∞)` beside g; composite build; slash-cancel; `x−2+6` → `x+4`; then the current (to be
replaced) closing board: board cleared, `(f∘g)(x)=x+4` at top with `Domain: (−∞,∞)` beside it,
all-reals number line drawn from zero outward, "Any function plugged into another brings its
domain with it", g + its domain + its number line back underneath, a third merged line, caption
"The domain of the composite is where the two lines overlap.", gold arrow fades, final
`Domain: [2,∞)`. Latest render: 22 audit marks clean, hold = 84.78 s (already in the guide
file), asset copied and byte-identical to the render.

## THE NEXT JOB — Chase's dictated redesign (not started)

His reasons, in his words: putting `Domain: (−∞,∞)` next to **(f∘g)(x)** is **wrong** — that is
the domain of just `x+4`, not of the composite, so the current screen teaches a falsehood.
"It's hard to read everything" once the lines merge.

Intended flow (build exactly this; label gaps as proposals if unsure):

1. After simplifying to `(f∘g)(x) = x+4`: clear the board. Show `(f∘g)(x)` at the top, and
   **underneath it `y = x + 4`** (the standalone linear function). Caption: now the domain of
   the composite; start with the result `x+4`; **`x+4` is linear, so by itself its domain is
   all real numbers.**
2. Put the `Domain:` for **`y = x+4`** next to *that* line (not next to `(f∘g)(x)`), then
   say **this isn't the actual domain of the composite** (exact wording his; keep it short).
3. **Number-line build fix — apply to ALL number lines in the clip:** it must **build itself
   left to right, as if being written**: −7, −6, −5, −4, −3, −2, −1, 0, 1, 2, 3, 4, 5, 6, 7
   placed down in order, the axis line extending as the ticks go down. (Current version starts
   at 0 and fans outward — Chase called it "weird".) Then the gold all-reals arrow on top.
4. Caption: that is not the domain of the composite, because **any function plugged into
   another brings its domain with it.** Then bring **g** back with its domain and its number
   line (same length/values/tick spacing as the first line), as now.
5. Merge: third line, both highlights slide onto it, as now.
6. **Then clean up so it reads:** get rid of `y = x+4`, its domain, its number line, **and g
   with its domain and number line.** Keep only **`(f∘g)(x)`** (no domain next to it) and the
   **merged number line moved up** underneath it.
7. Caption: **"The domain of the composite is where the two lines overlap."** **Pulse just the
   overlapping part on the line itself** (the blue ray from 2 on). Then the gold/orange part
   goes away. Then show the answer: **`Domain: [2, ∞)`** (interval notation), hold, end.

Open choice for the next agent (not discussed): whether to keep the final caption
"The domain of the composite is $[2,\infty)$." — Chase approved it earlier; keep unless he
objects.

## Rejected / do not rediscover

- `Domain: (−∞,∞)` beside `(f∘g)(x)` (above) — wrong math, now rejected.
- `x ≥ 2` tag sliding beside the result — replaced by interval notation only.
- Captions with italic-markup variables instead of LaTeX.
- Domains stacked under functions (he wants them beside, just not cramped).
- Left-aligned drift in composite rows; keep rows centered (the composite build rows share a
  left head position *on purpose* so the head can swap without a double print — don't "fix").
- Explaining the overlap as "all real numbers has no restrictions, so the only restriction is
  from g" — he replaced it with the single overlap sentence.

## Pitfalls that already cost time

- **`manim -qh` writes to `media/videos/composite_domain/1350p60/`**, NOT `1350p30`. The
  `1350p30` file is a stale old render; copying it made the portal show the old video twice.
  Always `md5sum` the render against the portal asset after copying.
- After a final render, set `COMPOSITE_EXAMPLES_HOLD_SECONDS` in `compositeExamplesGuide.ts`
  to the last mark's time in `composite_domain_marks.json` (render script `sed` pattern:
  `HOLD_SECONDS = [0-9.]*`).
- **Bash heredocs with quotes/backslashes broke repeatedly** in this harness; write Python
  files with the Write/Edit tools, not `cat <<EOF`. In Python source, `\infty` needs `\\infty`
  in normal strings (a single `\i` is an invalid-escape warning, not a failure).
- Loop: draft `-ql` render (no window), read the `[audit]` block, pull frames with ffmpeg at
  each mark (`media/audit/cf/` holds scratch frames), then `-qh` render + copy. Mid-animation
  frames matter: check the number-line build and the merge at intermediate times.
- Captions: any caption containing `$…$` goes through `math_caption.py` (blue g is `$@b g$`).
  `scene_audit.py` was changed to treat a VGroup caption as the caption.
- Number lines: `tick_number_line(y)` returns ticks (dict by integer), `axis_left/right`,
  `all_reals()` (gold double arrow), `from_two()` (blue dot + arrow). Its UNIT/HALF were tuned
  so labels (size 24 = audit floor) don't overlap; the left-to-right build needs a new
  reveal (e.g. ticks −7…7 in order with the axis drawn along), likely a helper in that file
  so all three lines share it.

## Other uncommitted work this session (Macro App, separate repo)

**Teacher Console preview auto-flip + no "backs out" bug** — done, tests pass, not run in the
app:
- Cause of the old bug: portrait/landscape was encoded in the preview URL (`previewNotch`), so
  flipping reloaded the portal to home. Fixed in `renderer/src/hooks/teacher-console/
  useTeacherConsolePreviewIdentity.ts` (notch param constant; the portal draws the notch only
  when its viewport is landscape).
- New: `renderer/src/utils/studentProgress/portalPreviewRouteAspect.ts` (+ `.test.ts`) maps
  portal hash routes to portrait/landscape; new hook
  `renderer/src/hooks/teacher-console/useTeacherConsolePreviewRouteAspect.ts` listens to the
  preview slot's `onNavState` and flips; wired in `useMacroAppStudentProgressShell.ts`.
- Mapping was **guessed**: landscape = transformations-homework, matrix-tutorial,
  matrix-guided-practice, matrix-part-3; portrait = home, composite/domain-range clips,
  vector-projections, graphing-linear-inequalities; Logic Homework unlisted (left as is).
  Chase has not confirmed the matrix/logic choices. Macro App must be restarted to try it.

## Verification state

Composite clip: 22 marks clean in the layout audit; contact-sheet frames reviewed by eye for
the shipped version. Chase said "looks good" to the number-line closing version, then asked for
this redesign. Macro App: `npx vitest run src/utils/studentProgress` → 19 files / 74 tests pass.

## Git / constraints

Programs root dirty (Manim Trial + agent docs), student-portal dirty (asset + guide const),
Macro App dirty. No commit/push/deploy requested. Netlify: never unless asked in that message.
Chase's cursor is a head-mounted gyro mouse; don't open windows/browsers uninvited — the
Teacher Console preview Refresh is **his** step (state it as a statement, no question).

## Exact next step

Implement the 7-step closing redesign in `Manim Trial/composite_domain.py`, starting with the
shared **left-to-right number-line build** in `tick_number_line.py`, then re-render (`-ql`
audit + frames, then `-qh`), copy from the **1350p60** folder, verify md5, update the hold
seconds, and tell Chase to refresh the preview.
