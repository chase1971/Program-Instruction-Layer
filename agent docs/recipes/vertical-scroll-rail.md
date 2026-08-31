# Vertical scroll rail — hover to scroll, click to nudge

> **The dwell-mouse replacement for a scrollbar.** A thin column of two large arrow
> buttons pinned to the **left** edge of a scrollable region. Hovering a button scrolls
> continuously; clicking it moves one step.

**Why it exists:** Chase drives the cursor with a head-mounted gyro mouse and dwell click.
A scrollbar thumb is too small to grab and dragging it is a sustained precision hold — the
two things that interaction is worst at. Wheel events don't reach him at all. So **any
region that scrolls and that Chase operates needs a rail**, not a scrollbar.

**It is on the left** because the dwell toolbar and its own scroll zones live on the right;
a rail on the right competes with them.

---

## Copy the exemplar — do not write a fifth one

| Context | Exemplar |
|---|---|
| **React (canonical)** | `School Scrips/Macro App/renderer/src/components/LocalVerticalScrollRail.tsx` + `renderer/src/hooks/browser/useViewportSmoothScroll.ts` |
| React, wrapping a whole scroll region | `School Scrips/Macro App/renderer/src/components/ViewportScrollFrame.tsx` |
| React, non-Macro-App | `School Scrips/Math App Studio/renderer/src/app/components/LocalVerticalScrollRail.tsx` |
| Scrolling an Electron `BrowserView` (no DOM to scroll) | `School Scrips/Macro App/renderer/src/components/browser/BrowserVerticalScrollRail.tsx` — same hook, `onScroll` → IPC |
| **Plain HTML/JS, no framework** | `Guildrun Stats/grstats/render.py` → `RAIL_JS` + `_rail()` |
| Same shape, zoom instead of scroll | `School Scrips/Macro App/my-calendar/src/components/shared/LocalCalendarZoomRail.tsx` |

In React, **`useViewportSmoothScroll` is the mechanism** — the rail is just two buttons
wired to it. It already handles scrolling a DOM element (`viewportRef`) *and* scrolling
something else (`onScroll` override). Do not write a second scroll loop; extend that hook.

**CSS:** `browser-scroll-rail`, `browser-scroll-rail__btn`, `browser-scroll-rail__icon`,
`browser-scroll-rail--compact` — defined in `Macro App/renderer/src/styles/browser-panel.css`
and reused by every consumer. Non-React ports mirror the same shape.

---

## The contract

1. **`onMouseEnter` starts continuous scroll. `onMouseLeave` stops. `onClick` nudges once.**
   Hover is the primary gesture — dwell produces a long hover before it produces a click.
2. **Fire once immediately on hover**, then start the interval. Otherwise the first tick of
   delay reads as a dead button.
3. **Always stop on unmount**, and on `window` blur for a standalone page. A rail that keeps
   scrolling after the pointer leaves is the failure mode Chase actually hits.
4. **`behavior: 'auto'`, never `'smooth'`.** Smooth scrolling queues animations behind a
   fast repeating interval and the region overshoots.
5. **Buttons are large.** Rail width and button size follow
   [canvas-kit-target-size.md](./canvas-kit-target-size.md) — a rail button that needs
   aiming defeats the point.
6. **Never `pointer-events: none` the rail** while its region is scrollable, and never hide
   it behind a hover reveal. It must be there before the pointer arrives.

## Timing

**Don't write a number into this file or into new code.** Step amount and interval are
`DEFAULT_BROWSER_SCROLL_SPEED` and `BROWSER_SCROLL_DELAY_MS` in
`Macro App/renderer/src/utils/browser/browserScrollSpeed.ts`, which mirror
`electron-toolbar/modules/scroll/backend/scroll_constants.py`. That Python file is the owner.
A port to another app imports or mirrors those names — it does not re-pick values.

## When *not* to use a rail

A region short enough that it never scrolls doesn't get one. A modal that scrolls should
wrap in `ViewportScrollFrame` rather than hand-rolling a rail —
see [modal-shell.md](./modal-shell.md).
