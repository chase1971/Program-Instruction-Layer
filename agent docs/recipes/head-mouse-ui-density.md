# Head-mouse UI density — slim by default

> **You might say:** "buttons are too big", "too bulky", "slim and condensed", "normal button size", "dwell doesn't mean huge", "I'm accurate with my mouse"
> **What it is:** How dense Macro App / Programs UI should be for Chase's head-mouse + dwell setup — **not** oversized touch-target padding everywhere.

**Exemplar files — read these before writing new code:**

- `School Scrips/Macro App/renderer/src/components/LocalVerticalScrollRail.tsx` — large targets **where scroll replaces a tiny scrollbar**
- `School Scrips/Macro App/renderer/src/styles/buttons-status.css` — standard `da-btn` sizing (use this, don't inflate)
- `agent docs/recipes/vertical-scroll-rail.md` — when large hit areas *are* required
- `agent docs/recipes/canvas-kit-target-size.md` — **canvas-kit only** floor for tiny `rectPct` buttons

---

## Why it exists

Chase uses a head-mounted gyro mouse with dwell click and is **highly accurate** with the
cursor. Older guidance ("min 44px, prefer 60px+ on everything") was written as a safe
default and got over-applied — settings screens, mockups, and modals ballooned into chunky
touch-style UI that he finds ugly and wasteful.

**Dwell accessibility is not the same as mobile touch accessibility.** What actually helps:

| Need | Mechanism | Not this |
|---|---|---|
| Scroll long content | [Vertical scroll rail](./vertical-scroll-rail.md) on the left | Giant padding so everything scrolls off-screen |
| Drag / resize | Hover-to-latch drag (Studio, toolbar recipes) | Huge buttons on every row |
| Accidental dismiss | No backdrop click on modals | — |
| Hover-only UI | Forbidden — always a click path | — |
| Ordinary buttons | **Normal desktop density** — standard `da-btn`, compact rows | 48px+ everything "for dwell" |

A **slightly** larger target is fine when a control is genuinely hard to hit (tiny icon-only
actions, scrollbar replacement). Default to **slim, condensed, standard web/desktop scale**.

## Rules

- **Default UI density:** normal desktop — tight sections, standard button classes, no
  inflating min-height "because dwell".
- **Do not** scale up an entire settings panel or modal to touch-target guidelines.
- **Do** add scroll rails when content can overflow and Chase needs to scroll it.
- **Do** use drag-latch patterns for move/resize instead of click-then-position precision.
- **44px floor** applies to **canvas-kit `rectPct` hit areas** and similarly tiny targets —
  see [canvas-kit-target-size.md](./canvas-kit-target-size.md). It is **not** a mandate for
  every `<button>` in React modals.
- **Mockups and redesigns:** show compact layouts first. Never default mockups to oversized
  "accessibility" buttons unless the control is a scroll-rail or drag handle.

## Anti-patterns

| Wrong | Bug it produces |
|---|---|
| Every settings control min-height 48px+ | Scrollbar, bulky screens, wasted space |
| Sliders with huge padded track blocks | Display tab feels like a touch kiosk |
| "Dwell-friendly" as excuse for low information density | Chase rejects the whole design |
| Shrinking content to fit giant chrome | Still scrolls; still ugly |

## Related

- [vertical-scroll-rail.md](./vertical-scroll-rail.md) — where large controls are correct
- [modal-shell.md](./modal-shell.md) — fit content without scrolling when possible
- [INIT_NEW_APP.md](./INIT_NEW_APP.md) § Accessibility — points here for density
