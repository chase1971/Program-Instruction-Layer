# canvas-kit click targets

> **You might say:** "the button is too small to click", "target size", "rectPct minimum"
> **What it is:** canvas-kit click targets — rectPct minimum size for head-mouse + dwell
> **Source:** converted from `School Scrips/canvas-kit/.cursor/rules/canvas-kit-target-size.mdc` on 2026-08-02 (was a Cursor glob rule that almost never fired).

**Exemplar files — read these before writing new code:**

- `School Scrips/canvas-kit/src/**`
- `School Scrips/**/screens.json`
- `School Scrips/**/prototype.json`

---

Chase drives these apps with a **gyro head-mouse + dwell click**. Target size is an
accessibility constraint here, not a style preference.
Background: `cursor-patterns/dwell-and-head-mouse.md`.

## The hole this closes

`CanvasStage` locks content to a fixed design box (e.g. **812×460**) and scales it
to fit. Interactive elements are placed with **`rectPct`** — percentages of that box.

`MenuButton` in **fill mode** (`h-full min-h-0 w-full min-w-0`, used by
`CanvasButtonLayer`) takes its size **entirely from `rectPct`**. Nothing in the code
enforces a floor, so a Studio-authored button can render too small to dwell on.

## Minimum target size

Against an **812×460** design box, a **44×44 px** rendered minimum is:

| Axis | Minimum `rectPct` |
|---|---|
| Height | **≥ 9.6%** of 460 |
| Width | **≥ 5.4%** of 812 |

**Round up in practice: use ≥ 10% height.** 44px is a floor, not a goal — prefer
the ~48px that standalone `MenuButton` (`px-4 py-3`) already produces.

For a different design box, recompute: `44 / designHeight` and `44 / designWidth`.

## Rules

- **Never author a button `rectPct` below the floor above** in `screens.json` /
  `prototype.json`. If a design needs a smaller visual, keep the *hit area* at the
  floor and inset the visual.
- **Adjacent targets need a gap.** Two buttons flush against each other invite a
  wrong dwell click. Leave ≥2% of the design box between interactive rects.
- **No hover-only affordances.** Anything revealed on hover must also be reachable
  by a click path — the dwell click fires on its own timer whether or not you
  wanted it (timing: `cursor-patterns/dwell-and-head-mouse.md`).
- **Scale down, not up.** Because `CanvasStage` letterboxes, a target that is
  borderline at design size is *smaller* on a narrower viewport. Check the smallest
  viewport the app ships to, not the Studio canvas.
- **Don't cancel interactions on `pointerleave`** in any canvas layer — head-mouse
  wobble fires it constantly. See `25-dwell-accessibility.mdc`.

## Changing shared components

canvas-kit is consumed **as source** by Math App Studio *and* live math apps. A
change to `MenuButton`, `CanvasButtonLayer`, or `rectPctStyle` ships to all of
them at once. Verify in the Studio **and** one live app before calling it done.

## Related

- `recipes/info-block-nav-buttons.md` — Back/Next MenuButton wiring
- `recipes/canvas-info-block-design.md` — info block visual design
- `cursor-patterns/dwell-and-head-mouse.md` — timing + coupling
