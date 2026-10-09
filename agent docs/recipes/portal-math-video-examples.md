# Portal math video examples — Manim to student portal (standard since 2026-10-08)

> **When Chase says "let's make an animation," "make a video for the portal," or "show this
> example in the student portal"** — read **this recipe end-to-end**, then
> [Manim Trial/ANIMATION_STYLE_RECIPE.md](../../Manim%20Trial/ANIMATION_STYLE_RECIPE.md)
> for frames, captions, pacing, and algebra on screen. This file owns **delivery + player
> behavior**. The style recipe owns **what the clip looks like**.

**Exemplar app (copy this shape):** Composite Examples — Manim
`composite_domain.py` / `composite_domain_2.py` / `composite_domain_3.py`; portal
`School Scrips/student-portal/src/features/video-examples/compositeExamplesGuide.ts` and
`CompositeExamplesGuideEntry.tsx`.

**Legacy:** Older portal clips (domain/range, linear inequalities, etc.) still use the shared
player but not every feature below. **Do not retrofit them** unless Chase names a guide.

**Equations of Lines (retrofit 2026-10-08):** `equationsOfLinesExamples.ts` +
`EquationsOfLinesExamplePage.tsx` — Auto/Slow, `*-steps.json`, navy player chrome on the
embedded clip only. Clips start at **0 s** (problem is in the page header; no `steps.slice(1)`).

---

## What the student gets

Each **example tab** is one portrait MP4. The shared viewer (`VideoExamplesView` +
`VideoExamplesPlayerStage` + `useVideoExamplePlayer`) provides:

| Control | Behavior |
|---|---|
| **Auto / Slow** | Same step times; switching modes **does not restart** — picks up at the current frame. |
| **Auto** | Clip **autoplays** on open. **Back / Next** jump one **caption step** (see below). **Next** keeps **playing** after the jump. **Pause** (left of Back) and **tap video** toggle pause/play. |
| **Slow** | **No autoplay** between steps. **Next** plays the animation to the next step hold; **Back** seeks to the previous hold. **Next** while playing skips to the **start of the following** step and keeps playing. **Tap video:** pause while playing; when paused, tap = **Next**. Pulsing **Next** when paused and ready. No Play/Replay row — use **Restart** in the mode row. |
| **Restart** | Mode row, after **Slow** — rewinds the **current example** to its opening frame. |
| **Full screen** | Top-right of the player column — expands the clip + controls (shared `VideoExamplesPlayerStage`). |
| **Opening frame** | First frame shows the **problem on the board** (e.g. directions caption + `f(x)` and `g(x)` written), not an empty board. Set `segmentStartSeconds` to just after that beat (Composite: **2.5 s**). |

Step boundaries come from **`_steps.json`** (caption beats), not raw audit marks.

---

## Two time files from Manim

Every `Narrated` scene that calls `write_marks('foo_marks.json')` also writes
**`foo_steps.json`** (array of seconds).

| File | Purpose |
|---|---|
| **`*_marks.json`** | Named layout-audit holds (`form`, `hold`, …). **`hold`** time = `segmentEndSeconds` for that clip. Still used for contact sheets and segment bounds. |
| **`*_steps.json`** | Portal **Back / Next / Slow** pauses — one time per **`say()`** caption (end of beat), plus final **`hold`**. Long board-only stretches (>8 s with no new caption) also insert audit mark times. Generated in `Manim Trial/scene_style.py` → `caption_step_times()`. |

Regenerate both **without a full render** (fast sanity check):

```text
cd Manim Trial
.venv\Scripts\python.exe -m manim --dry_run --disable_caching composite_domain_2.py CompositeDomainTwo
```

Copy into the portal asset folder:

- `composite_domain_2_marks.json` → optional reference; portal uses **steps** for navigation.
- `composite_domain_2_steps.json` →
  `student-portal/src/assets/video-examples/<guide-folder>/<name>-steps.json`

---

## Manim checklist (one example clip)

1. **`apply_portrait_frame()`** before other Manim imports; **PAPER** palette +
   `apply_portal_paper_background()`; **`color=INK`** on all math.
2. **`self.say(...)` before** the animation it describes; **`self.mark('name')`** after each
   teaching hold (audit + marks JSON).
3. **Problem on board** before domain work — exemplar:
   `composite_problem_intro.py` (`problem_title`, `problem_intro` marks).
4. Last beat: **full board visible**, then **`self.beat('hold', READ_LONG)`** (or equivalent).
5. End with **`self.write_marks('<scene>_marks.json')`**.
6. **Final render only:** `-r 1080,1350 --fps 30 --disable_caching` from `Manim Trial` cwd.
   Run layout audit / contact sheet per
   [LAYOUT_GUARDRAILS.md](../../Manim%20Trial/docs/LAYOUT_GUARDRAILS.md).
7. Copy **final MP4** into `student-portal/src/assets/video-examples/...`.

---

## Portal checklist (wire one example tab)

1. **Assets:** MP4 + `*-steps.json` (and keep marks in Manim Trial for re-renders).
2. **Guide config** — new `*Guide.ts` or extend an existing one (pattern:
   `compositeExamplesGuide.ts`):
   - `segmentStartSeconds` — opening frame with problem visible.
   - `segmentEndSeconds` — Manim mark **`hold`** for that clip.
   - `stepPauseSeconds` — `normalizeStepPauses(start, end, stepsFromJson)`; if the first
     step duplicates the opening frame, **`steps.slice(1)`** like Composite.
   - `aspectRatio: '1080 / 1350'`.
3. **Entry component** — `*GuideEntry.tsx` with `enableSlowMode`, `playbackMode` state, and
   `VideoExamplesView` with `autoPlay` (Auto mode only autoplays:
   `autoPlay && playbackMode === 'auto'` in the view).
4. **Route + tile** — activity id, `usePortalRoute`, `apps.ts` / home tile (see Composite +
   pipeline doc).
5. **Tests** — hold seconds and start time in a small vitest (see
   `compositeExamples.test.ts`).

Shared code (do not fork):

- `useVideoExamplePlayer.ts` — step navigation, Auto/Slow, segment end clamp (~0.08 s).
- `videoExampleStepPauses.ts` — normalize step arrays.
- `VideoExamplesPlayerStage.tsx` — mode row, step row, tap-to-pause/advance.

---

## File map (Composite exemplar)

| Layer | Path |
|---|---|
| Manim scenes | `Manim Trial/composite_domain*.py` |
| Marks / steps (generated) | `Manim Trial/composite_domain_*_marks.json`, `*_steps.json` |
| Portal MP4s | `student-portal/src/assets/video-examples/composite/*.mp4` |
| Portal steps JSON | `student-portal/src/assets/video-examples/composite/composite-domain-*-steps.json` |
| Guide | `student-portal/src/features/video-examples/compositeExamplesGuide.ts` |
| Entry | `student-portal/src/features/video-examples/CompositeExamplesGuideEntry.tsx` |

## File map (Equations of Lines — single-entry per problem)

| Layer | Path |
|---|---|
| Manim scenes | `Manim Trial/equations_of_lines.py` |
| Marks / steps (generated) | `Manim Trial/equations_of_lines*_marks.json`, `*_steps.json` |
| Portal MP4s | `student-portal/src/assets/video-examples/equations-of-lines/problem-*.mp4` |
| Portal steps JSON | `student-portal/src/assets/video-examples/equations-of-lines/problem-*-steps.json` |
| Clip config | `student-portal/src/features/equations-of-lines/equationsOfLinesExamples.ts` |
| Watch page | `student-portal/src/features/equations-of-lines/EquationsOfLinesExamplePage.tsx` |

Multi-screen apps (Equations of Lines) keep a white forms/list UI; wrap only the embedded
player in **`portal-quiz--video-examples`** (see `equations-of-lines.css`).

---

## New guide vs one-off clip

| Pattern | When |
|---|---|
| **Multi-tab guide** (`VideoExampleGuideConfig`, EX tabs) | Several related examples (Composite, Domain & Range, Equations of Lines). |
| **Single entry** (`VideoExampleEntry` on a feature page) | One clip per homework problem tile. Still use marks/`hold`, steps JSON, and
  `enableSlowMode` when the page should offer Auto/Slow. |

Equations of Lines uses the single-entry pattern on each problem's Watch page (see file map
below).

---

## Agent workflow (short)

1. Read this recipe + **ANIMATION_STYLE_RECIPE.md**.
2. Pick Manim exemplar scene closest to the math (Composite for domain/composite; quadratic
   for vertex form; `slope_intercept_form.py` for solve-on-screen).
3. Implement scene → dry-run → render → copy assets → guide TS → entry/route/tile → tests.
4. Chase reviews in the **portal**, not in `Manim Trial/media`.

Do **not** ship a draft resolution MP4. Do **not** deploy Netlify unless Chase asks in that
message.
