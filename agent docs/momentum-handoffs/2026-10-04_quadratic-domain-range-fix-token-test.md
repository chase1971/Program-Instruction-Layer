# Momentum handoff — fix the Composer-made quadratic domain/range clip, and report the token cost

Written: 2026-10-04 (America/Chicago)
Workspace: C:\Users\chase\Documents\Programs
Phase: Chase had Cursor **Composer 2.5** build the quadratic domain-and-range Manim clip. It took
**about 2.9 million tokens** (Chase's figure from Cursor billing) and the result is, in his words,
**"complete garbage, actually unusable."** The next agent's job is to redo or fix it and report what
that cost. The earlier portal-chart handoff (same topic, before the clip existed) is archived at
`agent docs/momentum-handoffs/2026-10-04_domain-range-quadratic-plan.md` and still holds the plan context.

## Read first

1. Root `AGENTS.md` — never open a GUI/browser/preview without per-run permission; handoff is not end-of-session (no commit/push unless asked).
2. **`Manim Trial/quadratic_domain_range.py`** (144 lines) + `quadratic_domain_range_marks.json` — the Composer-made clip to judge.
3. **`C:SERSASE.CURSORPLANSQUADRATIC_RANGE_ANIMATION_A341B6EA.PLAN.MD` (IN THE HOME FOLDER, NOT UNDER PROGRAMS)** — the plan Composer was given (the authoritative beats). The clip is todo 2 of 6; the portal pieces are the other todos.
4. `Manim Trial/ANIMATION_STYLE_RECIPE.md`, `Manim Trial/docs/LAYOUT_GUARDRAILS.md`, `Manim Trial/docs/ANIMATION_REUSE.md`.
5. **`Manim Trial/angle_between_vectors.py` + `portrait_frame.py`** — the clip redone earlier this session in the phone-shaped frame. It is the working exemplar for the approach below.

## What Chase wants

- Look at the finished clip, find what is wrong with it, and **redo it or fix it** — your call, but say which and why.
- The clip shows the domain and range of a quadratic with two examples on one MP4: `f(x)=2(x-1)^2+3` (a>0, range [3,∞)) and `f(x)=-2(x-1)^2+3` (a<0, range (-∞,3]). Beats: highlight `(x-h)^2` as the quadratic part, domain all reals, `a` grows, a copy of `a` sits beside `a>0`/`a<0`, `k` pops, the interval builds. Mark `ex2_start` splits the two portal tabs.
- **Then tell Chase how many tokens the fix took.** He is comparing models by token cost: Composer 2.5 spent ~2.9M and produced something unusable, so this is the "stronger agent smooths it out" half of the test. Report input, cached input and output separately if you can see them (`mcp__ccd_session_mgmt__get_usage` is available in this app; the session scorecard also records tokens). State the number plainly at the end, next to the 2.9M baseline.

## Feel and standards (from this session)

- **Phone first.** The portal shows video about 375 px wide. In a 14.2-unit landscape frame, type is drawn about 2.2× too small for that. We built `portrait_frame.py` (4:5, 6.4 x 8 units, `apply_portrait_frame()` called **before any other project import**) and redid the angle clip in it. At that frame, math font 26 lands about 11 px tall on a phone, roughly 16 px body text. **Proposal, not a decision for this clip:** use the same portrait frame, since the quadratic clip also plays in the portal player; confirm with Chase only if it matters.
- Use the vertical space: the frame is taller than it is wide. Keep figures modest and give formulas the room; stack steps one per line rather than running equations sideways.
- Captions wrap at full size: set `caption_wraps = True` on the scene (added to `scene_style.py`).
- Colors: the PAPER palette in `scene_style.py`. No ephemeral "Copied!" style feedback.

## Important finding to act on

The audit says the Composer clip is **clean: 0 problems across all 14 marks** (`media/audit/QuadraticDomainRange_audit.json`). Chase still finds it unusable. So the audit only catches text-on-text collisions, off-frame, and tiny type; it does **not** judge whether the teaching reads. **Look at the frames before trusting it** — render a draft (`-ql`, no window opens) and montage one frame per mark. The helper used this session lives in the Claude Code session scratchpad and will not exist; write a ~15-line one with `av` + PIL, or use `contact_sheet.py`. The clip may also be landscape and small-type for the phone.

## Current implementation state

- `Manim Trial/quadratic_domain_range.py` (Composer-made, uncommitted, untracked) and `quadratic_domain_range_marks.json`; a rendered `media/videos/quadratic_domain_range/.../QuadraticDomainRange.mp4` exists.
- `Manim Trial/build_page.py` has a new `quadratic_domain_range` row (scratch preview page, `agent docs/scratch/quadratic-domain-range.html`); `Manim Trial/docs/ANIMATION_REUSE.md` has 5 added lines (Composer's). Both uncommitted — review before keeping.
- The portal side (example route, player, "Show example") is **not** part of this task unless Chase asks; only the clip is.
- Angle clip: rewritten in portrait this session, all 9 marks audit clean, draft rendered only (not final, not copied into the portal). Changed files: `angle_between_vectors.py`, `portrait_frame.py` (new), `scene_style.py` (opt-in caption wrap). Leave them alone.
- Nothing committed or pushed this session.

## Rejected directions (do not rediscover)

- Judging a clip by the audit alone: it passed a clip Chase calls garbage.
- Designing for the desktop and letting the phone shrink it: the 42/48-font landscape floor idea was replaced by the portrait frame.
- Putting the quadratic video inline in the chart: Chase chose a full-screen example route (later work).

## Constraints

- No GUI, browser, or portal dev server without asking per run. Headless renders and frame images are fine.
- No commit, push, or deploy unless Chase asks.
- Files stay under 800 lines; Manim scene target under 500.
- Chase talks through speech-to-text; ask only if the literal reading would be clearly wrong.

## Exact next step

Draft-render `quadratic_domain_range.py`, look at one frame per mark, and write down in two or three lines what is actually wrong. Then fix or rebuild it (likely in the portrait frame, modeled on `angle_between_vectors.py`) until every mark passes the audit **and** the frames read. Finish by stating the token total.

This handoff is a continuation boundary only — no GitHub or end-of-session actions were performed.
