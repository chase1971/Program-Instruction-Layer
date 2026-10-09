# Momentum handoff — Composite Examples (Ex2 domain copy + Slow mode)

**Written:** 2026-10-08 (Thursday)

---

## Objective and current phase

Chase is polishing **Composite Examples** (M1314 student portal): three Manim clips with notation captions, domain teaching, and a new **Auto / Slow** viewer mode on the Composite route only.

**Current phase:** **Ex2 domain wording + re-render** and **Slow mode (portal)** are implemented and unit-tested. Chase has **not** yet signed off on Slow mode or re-watched all three tabs after the Ex2 domain fix. Next work is **portal review feedback** (wording, pacing, step density) — not new features unless something is broken.

---

## Chase's desired feel

- **Caption bar only** — never duplicate “Find …” on the board under `f(x)` / `g(x)`.
- **Say before you show** in Manim (`READ_LONG` / `READ_CAPTION_EXTRA` after notation lines).
- **Example 2 domain (composite section):** Do **not** jump straight to “any function brings its domain.” Start from the **composite written alone** (`4√x+2` / `y = …`), find its domain (square root → `[0,∞)`), say it matches **f**, **then** the plug-in rule and bring **f** back; **g** accepts all reals so domains **match** (not a merge overlap like Ex1).
- **Slow mode:** Students **click Next** to advance; **no autoplay** between steps. **Back** goes to previous held frame (seek, no reverse animation). **Full animation** plays between step pauses. Mode toggles **Auto | Slow** under the video (left); switching mode **restarts** the current example; clicking the active mode again **replays**. **Play** disabled while paused in Slow (use **Next**); **Pause** still works mid-step animation.
- **Step granularity (v1):** Pause at **Manim audit mark times** bundled in portal JSON — not caption-only yet. If steps feel too dense, follow-up is Manim marks after each `say()` + read wait.

---

## Accepted decisions (shipped)

| Area | Decision |
|---|---|
| Ex2 domain beats | `Now the domain of the composite. Start with $4\sqrt{x}+2$.` → radicand → domain same as **f** + number line → “Any function plugged…” → bring **f** → “domains match” → final Domain line. Number line at `ROW_Y['nl_g']` (audit clean). |
| Ex2 hold | **73.61 s** — `composite-examples-2.mp4` + `compositeExamplesGuide.ts` |
| Slow mode scope | **Composite Examples route only** (`CompositeExamplesGuideEntry`) — not Domain & Range / Vector / Equations yet |
| Step data | Three JSON files in `student-portal/src/assets/video-examples/composite/composite-domain*-marks.json`; `stepPauseSeconds` on each guide entry via `normalizeStepPauses` |
| Slow UI | Mode row under video (left); in Slow, ±5 row becomes **Back** / **Next** |
| Auto mode | Unchanged for Composite (`autoPlay` when mode is Auto) |

Prior round (still true): Ex1/Ex3 notation two-beat captions; fast `NL_*` constants; no em-dash captions; no third “substitute …” line after notation beat 2.

---

## Rejected directions (do not redo)

- Ex2 domain section opening with only “Any function plugged into another…” before establishing standalone composite domain (Chase: sentence order made no sense).
- Graying out Auto/Slow while playing (scrapped — restart on mode click instead).
- Free-run playback in Slow when paused (Play disabled at step holds; only **Next** advances).
- Slow mode on all portal video viewers in v1 (Chase chose Composite-only).

---

## Current implementation state

**Manim — Example 2:** [`Manim Trial/composite_domain_2.py`](Manim Trial/composite_domain_2.py) — closing domain block with `y_row`, `y_domain`, then plug-in beats. Marks: [`Manim Trial/composite_domain_2_marks.json`](Manim Trial/composite_domain_2_marks.json) (includes `y_inside`, `y_domain`).

**Portal — Slow mode:**

- Hook: [`School Scrips/student-portal/src/features/video-examples/useVideoExamplePlayer.ts`](School Scrips/student-portal/src/features/video-examples/useVideoExamplePlayer.ts) — `playbackMode`, `stepNext` / `stepBack`, `slowModeActive`
- Helper: `videoExampleStepPauses.ts`
- UI: `VideoExamplesPlayerStage.tsx`, `VideoExamplesView.tsx`, `CompositeExamplesGuideEntry.tsx`, `video-examples.css` (`.video-examples-controls--mode`)
- Guide: `compositeExamplesGuide.ts` + mark JSON assets

**Verification:** `videoExampleStepPauses.test.ts` + `compositeExamples.test.ts` pass (8 tests). Manim Ex2 re-render audit: all marks clean.

**Likely uncommitted:** Manim `composite_domain_2.py`, marks JSON (Trial + portal assets), portal MP4, slow-mode TS/CSS, agent docs.

---

## Open questions

- Does **Slow** step pacing feel right on phone (too many audit marks vs caption rhythm)?
- Any remaining **wording** on Ex1/Ex3 after Chase watches domain + composite sections?
- If steps too dense: **caption-only pause marks** in Manim (`Narrated.say` + read wait) — not started.
- Persist Slow/Auto in `localStorage` — out of scope unless Chase asks.

---

## Constraints

- No GUI launch without permission. Re-render: `Manim Trial/.venv/Scripts/python.exe -m manim -r 1080,1350 --fps 30 --disable_caching …` from `Manim Trial` cwd; copy MP4 + sync marks + hold in guide.
- Modals / portal rules unchanged. No Netlify deploy unless Chase asks in that message.

---

## Read first

1. This file.
2. [`Manim Trial/ANIMATION_STYLE_RECIPE.md`](Manim Trial/ANIMATION_STYLE_RECIPE.md) — captions, say-before-show, portal delivery.
3. [`School Scrips/student-portal/src/features/video-examples/useVideoExamplePlayer.ts`](School Scrips/student-portal/src/features/video-examples/useVideoExamplePlayer.ts) — slow vs auto behavior.
4. [`Manim Trial/composite_domain_2.py`](Manim Trial/composite_domain_2.py) — Ex2 domain exemplar after review fix.

---

## Exact next step

Chase reviews **Composite Examples** in the portal: try **Slow** on Example 2 (and spot-check Ex1/Ex3), confirm **Auto** still runs through, confirm Ex2 domain narration order feels right. Report any caption timing, step density, or wording issues. Apply **only** his feedback — Manim copy in the relevant `composite_domain*.py`, or portal slow-step data/UI if the problem is step boundaries not copy.
