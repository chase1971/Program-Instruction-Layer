# Momentum handoff — Composite Examples player + portal video standard doc

**Written:** 2026-10-08 (Thursday)

---

## Objective and current phase

**Composite Examples** (M1314 student portal) is the **reference implementation** for how Manim
math clips ship in the portal: caption-based **Auto / Slow** steps, shared Back/Next marks,
opening frame with the problem on board, and documented end-to-end in
`agent docs/recipes/portal-math-video-examples.md`.

**Current phase:** Player and UX work from this session are **implemented and unit-tested**.
Chase has **not** given final sign-off on every control after the last round (Auto **Next**
continues playing, mode switch without restart, control layout, tap-on-video). **Documentation
for “let’s make an animation” is done.** Next product work is either **Chase’s review feedback**
on Composite only, or **retrofit Writing Equations of Lines** to the new standard (Chase said
that is the one old guide to fix — **not** other legacy clips).

---

## Chase's desired feel

- **Caption bar only** — never duplicate “Find …” on the board under `f(x)` / `g(x)`.
- **Say before you show** in Manim (`READ_LONG` / read waits after notation).
- **Opening frame:** directions caption + **f(x) and g(x) already written** (portal starts at
  **2.5 s**, not 0).
- **Auto / Slow share the same step times** (`*_steps.json` from caption beats, not raw audit
  marks). Switching modes **continues from the current frame**, does not restart.
- **Slow:** step on **Next**; **Back** to previous hold; **Restart** in mode row; no Play/Replay
  row; **Next** pulses when paused and ready; **tap video:** pause while playing, advance when
  paused.
- **Auto:** autoplays on open; **Back/Next** jump by step; **Next** must **keep playing** after
  the jump; **Pause** left of **Back** in the step row; **tap video** = pause/play.
- **Control layout (do not rearrange without asking):** mode row = **Auto | Slow | Restart**
  (unchanged Auto/Slow positions); step row = **[Pause if Auto] Back | Next** (Back/Next stay
  where they were).

---

## Accepted decisions (shipped this session)

| Area | Decision |
|---|---|
| Step data | `Narrated.caption_step_times()` → `<scene>_steps.json`; portal imports `*-steps.json`; first step dropped when opening frame already shows that caption (`steps.slice(1)`). |
| Ex2 hold | **73.61 s** — `composite-examples-2.mp4` + guide |
| Segment start | `COMPOSITE_EXAMPLES_START_SECONDS = 2.5` for all three Composite tabs |
| Auto **Next** | Seek to next step mark, then **`play()`** (except final hold) |
| Mode toggle | No restart on Auto/Slow click; active mode click is no-op |
| Docs | **`agent docs/recipes/portal-math-video-examples.md`** owns portal delivery + player; **`ANIMATION_STYLE_RECIPE.md`** owns visuals; INDEX + student-portal `AGENTS.md` route “let’s make an animation” there |
| Legacy clips | No retrofit except **Equations of Lines** when Chase asks |

Prior (still true): Ex2 domain narration order; Composite-only Auto/Slow scope; no Netlify
without explicit ask; no GUI launch without permission.

---

## Rejected directions (do not redo)

- Single merged control bar (Chase: put controls back — only move Restart + Pause).
- Restart/Auto/Slow/Back/Next repositioning beyond Restart-after-Slow and Pause-before-Back.
- Slow mode using raw audit marks only for steps (caption `*_steps.json` is the standard).
- Auto **Next** pausing at each mark (regression fixed this session).
- Replay label (use **Restart**).

---

## Current implementation state

**Manim:** `scene_style.py` — `caption_starts`, `caption_step_times()`, `write_marks` writes
steps JSON. Exemplar scenes `composite_domain*.py`; dry-run regenerates steps.

**Portal — player:** `useVideoExamplePlayer.ts` — `stepNavigationActive`, Auto vs Slow
`stepNext`/`stepBack`, mode-switch effect, RAF step stops in Slow.

**Portal — UI:** `VideoExamplesPlayerStage.tsx` — layout above; video wrap tap handler.

**Portal — guide:** `compositeExamplesGuide.ts`, assets under
`src/assets/video-examples/composite/` (`*-steps.json`, MP4s).

**Docs:** `portal-math-video-examples.md`, pointers in `INDEX.md`, `recipes/INDEX.md`,
`ANIMATION_STYLE_RECIPE.md`, `student-portal/AGENTS.md`.

**Verification:** `videoExampleStepPauses.test.ts` + `compositeExamples.test.ts` pass (8 tests).

**Likely uncommitted:** Manim `scene_style.py`, composite scenes/marks/steps, portal MP4s,
player/stage/CSS, guide, agent docs, equations-of-lines work from **other sessions** may also
be dirty on disk.

**Note:** Previous `latest.md` described **Equations of Lines problem 4**; archived copy:
`2026-10-08_equations-of-lines-problem3.md`. That thread is **separate** until Chase
prioritizes it.

---

## Open questions

- Final **Composite** UX sign-off after Chase uses Auto/Slow, Restart, tap-on-video, and Ex2
  domain copy on device.
- **Equations of Lines retrofit:** steps JSON, `enableSlowMode`, opening frame — follow
  `portal-math-video-examples.md` when Chase says go (problem 3 review / problem 4 still open
  in parallel handoff archive).
- Persist Auto/Slow in `localStorage` — out of scope unless asked.

---

## Constraints

- Re-render: `Manim Trial/.venv/Scripts/python.exe -m manim -r 1080,1350 --fps 30
  --disable_caching …` from `Manim Trial`; sync MP4 + steps + hold in guide.
- Modals / portal rules unchanged. **Calendar 2.0** frozen.

---

## Read first

1. This file.
2. [`agent docs/recipes/portal-math-video-examples.md`](../recipes/portal-math-video-examples.md)
3. [`Manim Trial/ANIMATION_STYLE_RECIPE.md`](../../Manim%20Trial/ANIMATION_STYLE_RECIPE.md)
4. [`School Scrips/student-portal/src/features/video-examples/useVideoExamplePlayer.ts`](../../School%20Scrips/student-portal/src/features/video-examples/useVideoExamplePlayer.ts)
5. [`School Scrips/student-portal/src/features/video-examples/VideoExamplesPlayerStage.tsx`](../../School%20Scrips/student-portal/src/features/video-examples/VideoExamplesPlayerStage.tsx)

---

## Exact next step

Chase chooses one path:

- **A — Composite polish:** Review Composite Examples in the portal (Auto, Slow, Restart, tap
  video, Ex2 domain). Report only wording/pacing/step issues; apply **only** that feedback in
  Manim copy or step data — **do not** move control buttons.
- **B — Equations of Lines retrofit:** Read archived handoff
  `2026-10-08_equations-of-lines-problem3.md` for problem 3/4 state, then upgrade the Equations
  guide to `portal-math-video-examples.md` (steps JSON, Auto/Slow, opening frame) after Chase
  confirms priority.
