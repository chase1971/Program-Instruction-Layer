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
| React, student portal | `School Scrips/student-portal/src/features/frame-gallery/ViewportScrollFrame.tsx` (+ its `useViewportSmoothScroll.ts`, `scrollSpeed.ts`, `viewport-scroll-frame.css`). A verbatim port of the Macro App one. |
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
   **Never add `onPointerDown` / `onPointerUp` / `onPointerCancel` handlers** (an attempt to
   "support touch"). A dwell click is a pointer down and up while already hovering, so
   `onPointerUp → stop` kills the hover scroll right after the click. Only
   `onMouseEnter`, `onMouseLeave`, `onClick`.
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

## Student portal in the Teacher Console preview: the rail is Macro App's, not the page's

The preview is a native `BrowserView` with **phone emulation** (`browser-slot-phone-emulation.js`):
mouse becomes touch taps and the page reports `hover: none`. A rail built **inside the portal
page** can never hover there, and a tap fires an emulated `mouseenter` with no `mouseleave`, so it
scrolls forever. Don't try to fix that in the page. Put the rail **outside** it, like the Browser
tab: `BrowserVerticalScrollRail` (IPC `scrollBy`) beside the phone frame, already in
`Macro App/renderer/src/components/teacher-console/TeacherConsolePreviewPhoneChrome.tsx`. It finds
the page's inner `overflow-y: auto` container on its own, so a portal view needs no code for it.
In-page rails stay for real browsers and hide under `@media (hover: none)`.

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
