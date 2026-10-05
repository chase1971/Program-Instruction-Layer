# Momentum handoff — quadratic domain/range clip is shipped; next is the sibling clips and the Composer retry

Written: 2026-10-04 (America/Chicago)
Workspace: C:\Users\chase\Documents\Programs
Phase: The Composer 2.5 quadratic domain/range clip (about 2.9M tokens, "unusable") was rebuilt, reworked
twice on Chase's feedback, delivered into the student portal, and its lessons written into the Manim docs.
Chase called the final result "amazing." Nothing is committed or pushed. His stated next move: **try Composer
again on another domain/range problem** (square root or rational are the siblings on the chart), now that the
exemplar and protocol exist. He may also ask this agent to build one.

## Read first

1. Root `AGENTS.md` — no GUI/browser without per-run permission; no commit/push mid-session.
2. **`Manim Trial/ANIMATION_STYLE_RECIPE.md` § "Portal clips" and § "Delivery"** — the protocol written this session.
3. **`Manim Trial/quadratic_domain_range.py`** — the exemplar (docstring has the beat order). Compare
   `angle_between_vectors.py` + `portrait_frame.py` for a figure-plus-formulas clip.
4. `Manim Trial/docs/ANIMATION_REUSE.md` (domain/range paragraph under Formula assembly).

## What shipped

- **Clip:** `quadratic_domain_range.py`, portrait 4:5 (1080x1350, 30 fps), ~70 s, two examples
  (`2(x-1)^2+3` and `-2(x-1)^2+3`), 21 marks, audit 0 problems, one frame per mark read by eye.
  Beats per example: squared term pulses (no box), domain, general vertex form written above, `a` and the
  example's 2 pulse, the 2 drops into `2 > 0` and morphs to `a > 0`, range `[k,∞)` written, `k` and 3 pulse,
  the 3 replaces `k`. Every caption is said *before* its visual and held ~1-1.5 s.
- **Portal:** final MP4 copied to `School Scrips/student-portal/src/assets/video-examples/domain-range/quadratic-domain-range.mp4`;
  `domainRangeQuadraticExample.ts` Example 2 start = **35.72 s** (marks `ex2_start`). Chart tests pass.
  Composer had already built the route, the "Show example" button, `DomainRangeQuadraticExampleView`.
- **Autoplay:** `useVideoExamplePlayer(examples, { autoPlay })` option added (opt-in); the quadratic view passes it.
  Chase's rule: *every portal animation example autoplays when opened* — other example views do not yet.
- **Linear block fix:** the "(Vertical and horizontal lines are excluded.)" sentence lived inside the aligned
  KaTeX block and shifted Domain/Range; it is now a `footnote` field rendered as its own centered line.
- **Shared code changes (`Manim Trial/scene_style.py`):** wrapped captions are set at 4x and scaled down
  (`CAPTION_SUPERSAMPLE`, fixes uneven word gaps) and accept Pango markup for italic/colored variables;
  `wrap_words` splits outside `<...>`. Only the quadratic clip has been re-rendered with this; the angle clip
  will pick it up on its next render.
- **Docs:** "Portal clips" + "Delivery" sections in the style recipe; REUSE paragraph replaced; trigger words
  added to `agent docs/INDEX.md`; capture skill run; session scorecard bumped once.

## Why Composer's cut failed (for the retry)

`mathtex` text defaults to **white**, invisible on the paper background; only pieces given an accent color
showed. The layout audit does not check contrast, so it reported 0 problems. It was also landscape, built
the Domain/Range rows invisibly, and showed captions after the visuals. The protocol now covers each.

## Token comparison Chase asked for

Composer 2.5: ~2.9M tokens (Chase's Cursor figure). This agent: the first fix (diagnose, rebuild, verify,
report) was about **0.12M** of context at that point; the session then continued with three feedback rounds,
the portal wiring and the docs, so the **whole session total is higher** — read it from the session scorecard
rather than quoting 0.12M as the final cost. Input/cached/output split was not available from the usage tool.

## Chase's standards (this session)

- Phone first; use vertical space; stack steps one per line; type large.
- Never hand him draft-size video ("I don't want draft sizes, ever"); only final 1080x1350 in the portal.
  A clip is not delivered until it is in the student portal and replaces the old version.
- Captions: dark ink, one line, variables as italic + colored letters or LaTeX, read before shown, held long
  enough but "not too much longer." Pulse parts of a formula; no boxes.
- Handoffs are statements, not questions. No ephemeral "Copied!" feedback. Modals never close on backdrop click.

## Rejected directions (do not rediscover)

- Judging a clip by the audit alone.
- Draft-then-upscale to save tokens: a render costs no tokens; only reading frames and editing does.
- Boxing the squared term with `SurroundingRectangle`.
- Slow-everything pacing: a first slowed cut was 88 s and too slow; 35 s per example is right.

## Open / not done

- No `AGENTS.md`/keyword row exists inside `Manim Trial/`; routing is via root `agent docs/INDEX.md` only.
- Square-root and rational domain/range clips and their portal tabs are not built.
- The Composer retry has not started; the lessons are documented but untested on a fresh model.
- Pre-existing TypeScript errors in unrelated test files (`classworkData.test.ts`, `guidedPracticeArchive.contract.test.ts`) were seen and not touched.
- Uncommitted: all the above in `Manim Trial/`, `School Scrips/student-portal/` (Composer's portal work plus this session's edits), `agent docs/`.

## Constraints

- No GUI, browser or dev server without asking per run. Headless renders are fine.
- No commit/push unless Chase says "pull", "put on GitHub" or end-of-session.
- Files under 800 lines; check size before editing.

## Exact next step

If Chase asks for another domain/range clip (square root or rational), copy `quadratic_domain_range.py`
(same portrait frame, `build_rows`/`teach_example` structure), render at `-r 1080,1350 --fps 30`, read a frame per
mark, copy the MP4 into the portal and set the second-example start from the marks JSON. If he says Composer
is doing it, he may come back to review: render its scene and check frames **before** trusting the audit.

This handoff is a continuation boundary only — no GitHub or end-of-session actions were performed.
