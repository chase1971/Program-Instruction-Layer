# Dwell & Head-Mouse — single source of truth

> **Read this before writing any hover-, dwell-, or drag-activated UI anywhere in
> the Programs tree.** Chase drives every app with a **gyro head-mounted mouse
> plus dwell click**. There is no reliable "just click it" fallback and no
> reliable "hold perfectly still" either.
>
> **This file is the source of truth for dwell timing.** Four implementations
> exist (below). They are allowed to differ — but only for the reasons recorded
> here. If you are about to invent a fifth, stop and read § Grep before you build.

---

## The interaction model (why any of this exists)

| Fact about the hardware | Consequence for UI code |
|---|---|
| Cursor wobbles several px even when "held still" | Tight (2–5px) stationary thresholds **never latch**. Use ≥12px. |
| `mouseleave` / `pointerleave` fire constantly from wobble | **Never** cancel an armed interaction on leave. Poll and hit-test instead. |
| A dwell click fires automatically wherever the cursor rests | Any element that is hovered **will be clicked**. There is no hover-without-click. |
| Precise small targets are slow and error-prone | Large targets; no hover-only affordances; no backdrop-dismiss. |
| Typing is expensive (VoiceAttack / on-screen) | No typing-heavy flows; prefer selection over entry. |

**The one rule that subsumes most of the others:** *every hover affordance must
also have a click path, and every click target must survive being clicked
accidentally.*

---

## The four implementations

| Where | Timing source | Arms at | Releases after | Move threshold |
|---|---|---|---|---|
| **electron-toolbar** (OS-level dwell click) | `modules/dwell/backend/dwell_constants.py` + `dwell_persisted_settings.json` | **250 ms** *(persisted; the constants-file default of 300 is not what runs)* | 300 ms | 15 px |
| **Math App Studio** (in-app latch-to-drag) | `renderer/src/utils/dwellStationary.ts` | **450 ms** | 280 ms idle | 12 px |
| **Macro App** (tooltips only) | `renderer/src/hooks/gradebook/useGradebookDelayedHover.ts` | **1000 ms** (headers 400) | 150 ms grace | — |
| **`accessibility-patterns.md`** (React drawer prose) | *documentation only* | 500 ms | 500 ms | — |

### Why they legitimately differ

- **Toolbar (250 ms)** is the *system* dwell click. It must be fast because it
  replaces every physical click you make all day. It is tuned for throughput.
- **Studio (450 ms)** is a *latch to drag*, layered on top of a surface that the
  toolbar is already dwell-clicking. It is deliberately **slower than the toolbar**
  so that a normal dwell-click on a handle is not mistaken for a drag intent.
- **Macro App (1000 ms)** is a *tooltip*, i.e. purely informational. Long delay
  is correct for "I paused to read", wrong for "I want to act".

### What is NOT legitimate

The `accessibility-patterns.md` 500 ms figures match nothing that ships. They were
written as illustrative prose, not measured. **Do not copy them into new code** —
use the table above.

---

## ⚠️ The cross-layer coupling (open question — verify before relying on it)

**The toolbar's dwell click and every app-level hover delay run at the same time,
on the same cursor, and neither system knows the other exists.**

Timeline when you rest the cursor on a dwell-draggable handle in Math App Studio:

```
t=0ms     cursor arrives, Studio arms its 450ms latch
t=250ms   ← toolbar fires a REAL OS-level left click here
t=450ms   Studio latch would attach
```

The OS click lands **200 ms before** the in-app latch. In the Studio that click
most likely enters the *mouse-grab* path (`onPointerDown → grabMove`) rather than
the dwell-latch path — which may be why drag "just works" there. In the Macro App,
the same click lands **750 ms before** a tooltip appears, so a tooltip-only hover
target is being clicked every single time it is read.

**Status: unverified.** Chase does not currently know whether toolbar dwell stays
live while working in Studio. It is documented here because *no doc in either repo
mentioned that the other system was running*, which is the actual defect.

### How to settle it

1. Check the pause state: `modules/dwell/backend/dwell_pause_audit.py` records a
   reason for every pause. Watch the `DWELL` logger while using the Studio.
2. Dwell has pause reasons for **typing**, **scroll zones**, **hotkey**, and
   **manual** — see `dwell_typing_pause.py`, `dwell_scroll_zone_pause.py`. There
   is **no app-window or per-application exclusion**. If Studio work needs one,
   that is a new pause reason, modeled on `dwell_scroll_zone_pause.py`.
3. `electron-app/patterns/overlay-exclusion-zones.md` documents a position-based
   exclusion pattern, but **no implementation of it exists in the dwell backend**
   (no `exclusion` or `tabletop` reference in `modules/dwell/backend/*.py`).
   Treat that doc as a design sketch, not a description of running code.

**Until this is settled:** when adding a hover affordance, assume the element
**will be clicked at 250 ms**. Design so that click is harmless or is the intended
action.

---

## Grep before you build

There are already four dwell/hover mechanisms. Before adding a fifth, search for
the one that already covers your case:

| You need… | Use | Exemplar consumer |
|---|---|---|
| Move/resize a canvas element (`rectPct`) | `useDwellRectEdit` | `DesignCanvas.tsx` (Math App Studio) |
| Move a floating panel (px) | `useDwellAttachDrag` | `FloatingToolbar.tsx` (Math App Studio) |
| Shared latch geometry / hit-test / Esc-release | `utils/dwellStationary.ts` | Math App Studio |
| Delayed tooltip on hover | `useGradebookDelayedHover` | `GradebookScorecardTooltip.tsx` (Macro App) |
| Region hover/dwell in a click-through overlay | `createOverlayHoverPoll` | `electron-app/src/overlay-hover-poll.js` (toolbar) |
| OS-level dwell click / drag behavior | `modules/dwell/backend/` | toolbar (do not reimplement in an app) |

**If you would create a second implementation of one of these, STOP and surface it
for a decision** (root `AGENTS.md` rule 7).

---

## Non-negotiable behaviors

These each exist because a specific bug bit. Do not "clean them up".

- **Leave handlers are no-ops on dwell surfaces.** Wobble fires `pointerleave`
  constantly. A **poll loop** owns hit-testing (`isPointerOverRect`).
- **Re-arm requires a physical exit.** After release, the same handle must not
  re-arm until the cursor actually leaves it (`needsExitHandleRef` in the Studio),
  or it instantly re-latches.
- **Release only starts after the cursor has moved.** Holding still after a latch
  keeps the grab alive — otherwise the grab drops the moment you stop to aim.
- **Hit-tests get padding.** `DWELL_HIT_PADDING_PX = 8`; prefer a rect test over
  `elementFromPoint`, which a wobbly cursor frequently misses.
- **Escape cancels; right-click releases.** See `bindHoldReleaseShortcuts`.
- **Never dismiss a modal on overlay/backdrop click.** A wobble onto the backdrop
  must not cancel a multi-step flow. See `modal-pattern.md`.
- **Post-pause cooldowns are load-bearing.** e.g. `HOTKEY_PAUSE_JIGGLE_COOLDOWN = 3.0`
  exists so a head wobble right after an intentional pause does not undo it before
  the overlay has even rendered the paused state.

---

## Anti-patterns

- Tight (2–5 px) stationary thresholds — never latch for a head-mouse.
- Using `onPointerLeave` / `onMouseLeave` to cancel arming.
- Hover-only actions with **no click path**.
- A second drag/hover implementation "just for this one overlay".
- Copying the 500 ms figures from `accessibility-patterns.md` — they ship nowhere.
- Assuming a hovered element is not also being clicked (see § coupling).

---

## Where the code lives

| Layer | Path |
|---|---|
| OS dwell engine (Python) | `electron-toolbar/modules/dwell/backend/` |
| Dwell timing constants + *reasons* | `electron-toolbar/modules/dwell/backend/dwell_constants.py` |
| Live persisted overrides | `electron-toolbar/modules/dwell/backend/dwell_persisted_settings.json` |
| Overlay hover/dwell factory (JS) | `electron-toolbar/electron-app/src/overlay-hover-poll.js` |
| 16 toolbar interaction patterns | `electron-toolbar/electron-app/patterns/` (indexed by its `README.md`) |
| React latch-to-drag | `School Scrips/Math App Studio/renderer/src/app/hooks/useDwell*.ts` |
| React shared geometry | `School Scrips/Math App Studio/renderer/src/utils/dwellStationary.ts` |
| React tooltip hover | `School Scrips/Macro App/renderer/src/hooks/gradebook/useGradebookDelayedHover.ts` |

## Related

- `.cursor/rules/25-dwell-accessibility.mdc` — the always-relevant short form
- `School Scrips/Math App Studio/.cursor/rules/studio-dwell-mechanics.mdc` — **the exemplar rule**; model new app rules on its shape
- `cursor-patterns/accessibility-patterns.md` — React drawer/keyboard/ARIA detail
- `cursor-patterns/modal-pattern.md` — no-backdrop-dismiss
