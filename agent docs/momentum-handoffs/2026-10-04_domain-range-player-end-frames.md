# Momentum handoff — domain/range portal clips + video player end frames

Written: 2026-10-04 (America/Chicago)
Workspace: C:\Users\chase\Documents\Programs
Phase: Quadratic, square-root, and rational **domain & range** Manim clips are built, rendered
portrait 1080×1350 @ 30 fps, copied into the student portal, and wired with **Show example**
(Example 1 / Example 2 tabs, autoplay). Shared **video examples player** fixes: switch tabs while
playing, readable active tab styling, segments **stop on the last content frame** (not blank).
Animation docs now require every example to end with work still on screen. **Nothing committed or
pushed** unless Chase says pull / end-of-session.

## Read first

1. Root `AGENTS.md` — no GUI/browser without per-run permission; momentum ≠ end-of-session.
2. **`Manim Trial/ANIMATION_STYLE_RECIPE.md`** — § Portal clips (including **“When playback stops”**),
   § Delivery (`ex1_hold` / `ex2_form` segment convention).
3. **`School Scrips/student-portal/src/features/video-examples/useVideoExamplePlayer.ts`** —
   `SEGMENT_END_EPSILON`, `segmentHoldTime`, segment end / skip / `handleEnded` behavior.
4. Exemplars: **`quadratic_domain_range.py`**, **`sqrt_domain_range.py`**, **`rational_domain_range.py`**
   + matching `*_marks.json` and `domainRange*Example.ts` in student-portal.

## Objective and current phase

Chase wants **phone-readable** math explanation clips in the **student portal** for the domain &
range chart (quadratic, square root, rational), with the same teaching feel as the quadratic
exemplar. Playback UX: autoplay on open, **dwell-friendly** tab switching, and **never end an
example on a blank frame** — freeze on the finished board (or a summary), not after a fade-out.

## Chase's desired feel (use his language)

- Phone first; large type; captions **before** the visual; hold ~1–1.5 s; pulse with `Indicate`, no boxes.
- White **PAPER** palette; every `MathTex`/`mathtex` gets `color=INK` (white default is invisible).
- **No draft renders** in the portal — only final 1080×1350.
- When an example **ends in the player**, he should see **all the math still there**, not white.
- If a blank transition between two examples in one MP4 is needed, that's fine **between**
  segments only; each tab's stop time must be **before** that fade.

## Accepted decisions

| Area | Decision |
|---|---|
| Multi-example MP4 segments | Example 1 `segmentEndSeconds` = **`ex1_hold`**; Example 2 `segmentStartSeconds` = **`ex2_form`**. Not `ex2_start` (usually after fade). |
| Player safety net | Seek to `end - 0.08s` at segment end, skip-to-end, and near EOF when no segment end — pauses on content even if marks drift slightly. |
| Rational range teaching | No “horizontal asymptote” wording; “fraction never zero” → `y ≠ d` then numeric `d`. |
| Tab UX | Tabs not disabled while playing; `selectExample` pauses then switches; `autoPlay` restarts segment. |
| Documentation | Rule in style recipe + REUSE verify step: **stop frame must not be blank**; optional summary slide if that's the natural ending. |

## Rejected directions (do not rediscover)

- Ending Example 1 at **`ex2_start`** — includes inter-example **FadeOut** → blank ending.
- Trusting layout audit alone for contrast or “does the student see math?”
- Ephemeral success toasts; modals that dismiss on backdrop click.
- Visible `cmd.exe` launchers; interactive terminal prompts for Chase.

## Current implementation state

**Manim (uncommitted / new files):** `quadratic_domain_range.py`, `sqrt_domain_range.py`,
`rational_domain_range.py`, marks JSONs, helpers (`portrait_frame.py`, `solve_steps.py`, etc.),
`ANIMATION_STYLE_RECIPE.md`, `docs/ANIMATION_REUSE.md`.

**Portal (`School Scrips/student-portal`, separate git repo, dirty):**
- Assets: `src/assets/video-examples/domain-range/*.mp4` (three clips).
- Config: `domainRangeQuadraticExample.ts`, `domainRangeSqrtExample.ts`, `domainRangeRationalExample.ts`
  with hold/form segment times from marks JSON (e.g. rational ex1 **52.17**, ex2 start **56.11**).
- Views/routes/chart **Show example** buttons; tests **`domainRangeChart.test.tsx`** + **`useVideoExamplePlayer.test.ts`** — **8 passed** last run.
- Player: `useVideoExamplePlayer.ts`, `videoExamplesTypes.ts` comment on segment convention, tab CSS.

**Programs root repo:** also dirty (Manim, agent docs, momentum handoffs, session logs).

**Optional cleanup (not done):** Move `mark('ex2_start')` to **before** `FadeOut(first example)` in
Manim scenes so marks JSON isn't misleading; portal already uses hold/form.

**Other portal guides:** `linearInequalitiesGuide.ts` Intro segment — confirm intro doesn't end on
blank if Chase reports it; vector projection uses separate MP4s per clip.

## Open questions / next work

- **GitHub sync:** large uncommitted surface across Programs + student-portal; Chase has not asked
  for pull / put on GitHub this session.
- **Composer retry** on another domain/range problem (from earlier handoff) — exemplar + siblings
  now exist; may be lower priority.
- **Netlify deploy** — not requested; local `npm run dev` for review (ask before opening browser).
- **`dot_product_directions.py`** open in editor — unrelated to domain/range unless Chase pivots.

## Constraints

- File size cap 800 lines; orchestrators stay thin.
- Frozen: Calendar 2.0 — do not touch.
- Session is **context-heavy**; prefer fresh task for unrelated major work after this handoff.

## Exact next step

If continuing domain/range: spot-check all three **Show example** tabs in the portal — each example
should **pause on the full final frame**. If any clip still fades to blank at tab end, add/fix
`ex1_hold` in Manim and re-render, then refresh segment constants from `*_marks.json`.

If syncing: Chase says **pull** or **end of session protocol** → full multi-repo sync per root `AGENTS.md`.
