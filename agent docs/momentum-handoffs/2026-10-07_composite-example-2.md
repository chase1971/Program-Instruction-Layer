# Momentum handoff — Composite Examples clip: Example 1 redesign shipped, Example 2 built

Written: 2026-10-07 (America/Chicago)
Workspace: C:\Users\chase\Documents\Programs
Phase: Both Composite Examples clips are rendered at final quality and copied into the
student-portal assets; the guide has an Example 2 tab. **Chase has not yet reviewed Example 2**
(or the final Example 1 tweak) in the Teacher Console preview. **Nothing committed, pushed or
deployed** (not asked).

## Read first

1. Root `AGENTS.md` — no GUI/browser launches without per-run permission; **never deploy to
   Netlify unless Chase says so in that message**; handoff is a statement, not a question;
   file cap 800 / extract before 700.
2. `Manim Trial/ANIMATION_STYLE_RECIPE.md` — house style (white `PAPER_*`, `mathtex`, LaTeX captions).
3. `Manim Trial/composite_domain.py` (Example 1), `composite_domain_2.py` (Example 2, imports
   `row`, `domain_row`, `pair`, sizes and `ROW_Y` from Example 1), `tick_number_line.py`,
   `math_caption.py`.
4. Portal: `School Scrips/student-portal/src/features/video-examples/compositeExamplesGuide.ts`
   and `src/assets/video-examples/composite/` (`composite-examples.mp4`, `composite-examples-2.mp4`).

## Objective

Teach composite-function domains in the portal's "Composite Examples" clip (portrait 4:5, phones).
Chase reviews in the Macro App Teacher Console preview (embedded portal, dev origin reads local
`src/assets`; re-render + copy shows up after **his** Refresh — state it, don't ask).

## Chase's desired feel (his language)

- Math in captions is **LaTeX**, never plain text. Domains **beside** functions with a real gap;
  work centered. Solve steps tight; proper number lines (ticks, integer labels, arrows, dot).
- **Number lines build left to right** (−7 … 7 placed in order, axis extending) — applies to all lines.
- Don't mislead: never put a domain beside `(f∘g)(x)` that belongs to a different expression.
- At the end the composite must **still be on screen** with its answer domain.
- Example 2: "same structure"; it's `g(f(x))`, explain that you're plugging f in; **no merge panel**
  because the composite's domain equals the plugged-in function's domain.

## Accepted decisions / what is built

**Example 1** — f(x)=x²+6, g(x)=√(x−2), (f∘g)(x)=x+4, domain [2,∞). Closing board: top shows
`(f∘g)(x) = x+4`; underneath `y = x+4` with its own domain `(−∞,∞)` beside it ("this isn't the
actual domain of the composite"); all-reals line; g returns with domain and line; both merge onto a
third line; cleanup removes `y=x+4`, g and their lines, merged line moves up under the composite;
blue ray pulses twice, gold fades, `Domain: [2,∞)` below. Hold 98.44 s (const in guide), md5 of
asset == render (`087d3ab3…`).

**Example 2** — f(x)=√x, g(x)=4x+2, g(f(x))=4√x+2, domain [0,∞). Solve `x ≥ 0` on a number line
(dot on 0) → f's domain; g linear → all reals; build `4x+2` → `4(x)+2` → f flies in (blue) → drop
parentheses; clear; composite at top; "any function plugged into another brings its domain with
it"; f returns with domain + line; composite keeps f's domain; final `Domain: [0,∞)` under the
line, composite still on top. Hold 61.89 s (`COMPOSITE_EXAMPLES_2_HOLD_SECONDS`), asset md5
`6de7a323…` == render. 15 audit marks clean; frames reviewed (draft). Caption wording was my
choice (e.g. "A line has no restrictions, so g's domain is all real numbers.", "Drop the
parentheses.") — Chase hasn't seen it.

## Rejected / do not rediscover

- `Domain: (−∞,∞)` next to `(f∘g)(x)` (wrong math). `x ≥ 2` tag beside the result. Italic-markup
  variables in captions. Stacked domains. Left drift in composite rows (rows share a left head
  position on purpose so the head swaps without double print — don't "fix").

## Pitfalls that cost time

- **`play()` without `run_time` counts as 1.0 s in the marks clock** (`Narrated.play`) even if the
  animation is longer → marks drift from video. Always pass `run_time=` (builds:
  `self.play(nl.build(), run_time=3.0)`).
- `manim -qh` writes to `media/videos/<scene_file>/1350p60/`, not `1350p30`; always `md5sum` the
  copy. Render with `Manim Trial/.venv/Scripts/python.exe -m manim` and MiKTeX on PATH
  (`%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64`); system python has no manim.
- After a final render set the hold const to the last mark in `*_marks.json`.
- Write Python with Write/Edit (or a python heredoc script), not shell heredocs with quotes.
- `tsc --noEmit` in student-portal shows pre-existing generic-quiz type errors; none in composite files.

## Other uncommitted work (Macro App, separate repo, from earlier this day)

Teacher Console preview auto-flip portrait/landscape (`portalPreviewRouteAspect.ts`,
`useTeacherConsolePreviewRouteAspect.ts`); route→aspect mapping partly **guessed** (matrix and
logic routes unconfirmed). Macro App must be restarted to try it.

## Git / constraints

Programs root, student-portal (2 mp4s + guide) and Macro App are dirty. No commit/push/deploy
requested. Netlify never unless asked in that message. Don't open windows/browsers uninvited.

## Exact next step

Wait for Chase's feedback on Example 2 (and the Example 1 top line `(f∘g)(x)=x+4`) after he
refreshes the preview; apply tweaks in `composite_domain_2.py`, re-render `-qh`, re-copy from
`media/videos/composite_domain_2/1350p60/`, verify md5, update `COMPOSITE_EXAMPLES_2_HOLD_SECONDS`.
