# recipes/ — how we've built it before

> **The single place to look before building an interaction.** Drag, dwell, hover,
> overlay, scroll, toggle, modal, canvas element, animation.
>
> **Chase points here by saying:** *"check the recipes folder"* / *"how did we do the
> drag handle on an overlay?"* — but an agent should read this table **without being
> asked**, any time it is about to build something in one of these categories.
> Root `AGENTS.md` § Recipes says so.

---

## How to use this

1. **Match his words to a row** in the table below. Read **that one recipe**.
2. **Open the exemplar files** the recipe names. The code is the truth; the recipe
   is the map.
3. **Extend the exemplar.** Do not write a parallel implementation. If no recipe
   matches, build it, then **add a recipe** (see § Adding a recipe).

**Never copy a timing value out of a recipe.** Every dwell, hover, and drag
threshold lives in **`cursor-patterns/dwell-and-head-mouse.md`** and in
`electron-toolbar/modules/dwell/backend/dwell_constants.py`. Recipes describe
*shape and order*; those two files own the *numbers*.

---

## Dwell and click

| You might say | Recipe | Status |
|---|---|---|
| "click by holding still", "dwell mode 1" | [dwell-click.md](./dwell-click.md) | ✅ |
| "drag by dwelling", "the drag state machine", "dwell mode 2" | [dwell-drag.md](./dwell-drag.md) | ✅ |
| "hover a button to fire it", "toolbar button activation" | [dwell-activation.md](./dwell-activation.md) | ✅ |
| "count down before it does the thing" | [dwell-countdown.md](./dwell-countdown.md) | ✅ |
| "dwell in the Studio", "the React dwell hook", "it clicks before I'm ready" | [studio-dwell-latch.md](./studio-dwell-latch.md) | ✅ |

## Drag, move, position

| You might say | Recipe | Status |
|---|---|---|
| "drag handle on an overlay", "hover the handle then it follows", "ghost overlay" | [hover-to-lock-drag.md](./hover-to-lock-drag.md) | ⚠️ see note |
| "move or resize a canvas element", "carry mode", "resize handles" | [canvas-move-resize.md](./canvas-move-resize.md) | ✅ |
| "send the overlay to my cursor", "F14 / F23 reposition" | [move-to-cursor.md](./move-to-cursor.md) | ✅ |
| "keep the window on the right monitor", "it opened off-screen" | [window-positioning.md](./window-positioning.md) | ✅ |

## Overlays and windows

| You might say | Recipe | Status |
|---|---|---|
| "the overlay eats my clicks", "click-through window", "only hot regions clickable" | [click-through-windows.md](./click-through-windows.md) | ✅ |
| "toggle the overlay on and off", "it flickers when I press the hotkey twice" | [toggle-pattern.md](./toggle-pattern.md) | ✅ |
| "build a toolbar", "add a button to the toolbar" | [toolbar-system.md](./toolbar-system.md) | ✅ |

## Hover and scroll

| You might say | Recipe | Status |
|---|---|---|
| "detect when the cursor is over a region", "polling vs events" | [mouse-hover-detection.md](./mouse-hover-detection.md) | ✅ |
| "scroll faster near the edge", "region to scroll speed" | [scroll-calculation.md](./scroll-calculation.md) | ✅ |

> **No key-press recipe right now.** `hover-to-key-press.md` and `continuous-key-press.md`
> were deleted 2026-08-02 — they documented `modules/arrow_module.py`, which commit
> `e98301b "Interface 2.0"` removed. Arrow lives in `coordinator/arrow_handlers.py` +
> `electron-app/src/window-managers/arrow-manager.js` now. **Write the replacement from
> that code**, not from memory of the old docs.

## Building UI (React / canvas apps)

| You might say | Recipe | Status |
|---|---|---|
| "new modal", "make it look like that modal", "the modal scrolls wrong" | [modal-shell.md](./modal-shell.md) | ✅ |
| "the blue instruction box", "info block", "step badge" | [canvas-info-block-design.md](./canvas-info-block-design.md) | ✅ |
| "Back / Next buttons on the info block", "tutorial nav" | [info-block-nav-buttons.md](./info-block-nav-buttons.md) | ✅ |
| "the element vanishes when I click it in edit mode" | [edit-underlay-layer-contract.md](./edit-underlay-layer-contract.md) | ✅ |
| "make the word flash", "blue pulse", "vocabulary highlight" | [tutorial-flash-vocabulary.md](./tutorial-flash-vocabulary.md) | ✅ |
| "the button is too small to click", "target size", "rectPct minimum" | [canvas-kit-target-size.md](./canvas-kit-target-size.md) | ✅ |

## Animation

| You might say | Recipe | Status |
|---|---|---|
| "reuse an animation", "animation template", "port that animation over" | [animation-library.md](./animation-library.md) | ✅ |
| "implement the director notes", "the pending animation file" | [animation-director-notes.md](./animation-director-notes.md) | ✅ |

## Architecture and handoff

| You might say | Recipe | Status |
|---|---|---|
| "manage the states", "it gets stuck between modes" | [state-machine.md](./state-machine.md) | ✅ |
| "Studio and the AI are fighting over screens.json", "design handoff" | [studio-design-propagation.md](./studio-design-propagation.md) | ✅ |
| "embed VLC", "the video rectangle", "VlcStage" | [vlc-embed-contract.md](./vlc-embed-contract.md) | ✅ |

---

## Accuracy notes — read before trusting a detail

**Audited 2026-08-02 against the live code.** Every recipe above names exemplar files
that were confirmed to exist, and the three that described deleted code were removed:

| Removed | Why |
|---|---|
| `overlay-exclusion-zones.md` | Design sketch — no implementation ever existed. For dwell suppression, add a **pause reason** modeled on `dwell_scroll_zone_pause.py` |
| `hover-to-key-press.md` · `continuous-key-press.md` | Documented the deleted `modules/arrow_module.py`. Every class they named (`ArrowKeyHandler`, `ContinuousKeyPressHandler`, `poll_key_press`, `verify_key`) returned zero hits |

**Timing values were wrong and are now removed from every recipe.** The dwell recipes
carried `DWELL_TIME = 600` where the real constant is `0.3` and the persisted override
is `250 ms`; `DRAG_RELEASE_TIME = 1.0` against a real `0.75`; `MOVEMENT_THRESHOLD = 10`
against a real `15`. Recipes now write the **constant's name** and point at its owner.
`scripts/check-docs.js` has a `RECIPE VALUES` check that fails if a number comes back.

**Still worth a second look:** the toolbar recipes were last substantively revised
**2025-12-22** and the dwell backend has moved since. They are anchored to real files
now, but **open the exemplar before relying on a specific detail.**

**Known gap:** nothing here covers the `coordinator/` layer (`module_registry.py`,
`module_supervisor.py`, `module_lifecycle.py`, `hotkey_supervisor.py`). Modules are
registered and supervised now; the recipes still describe standalone backends talking
over signals. *How to add a new toolbar module* has no recipe yet.

---

## Where things live

| Kind | Home | Example |
|---|---|---|
| **Recipe** — how to build one interaction | **this folder** | `dwell-drag.md` |
| **Standard** — shape all code must have | `cursor-patterns/` | `CODING_STANDARDS.md`, `file-headers.md` |
| **Values** — timings, thresholds, sizes | `cursor-patterns/dwell-and-head-mouse.md` + `dwell_constants.py` | never restated in a recipe |
| **Integration doc** — why this subsystem is like this | the app's `docs/` | `EMBEDDED_BROWSER_AND_MODALS.md` |

That split is what keeps this folder from becoming a dumping ground. If a
document explains *one app's history*, it is not a recipe.

---

## Adding a recipe

When you build an interaction that has no recipe — **before the session ends**:

1. Create `recipes/<name>.md`.
2. Header block, in this order:
   - `> **You might say:** ` — the words **Chase** would use, not the technical name
   - `> **What it is:** ` — one line
   - `**Exemplar files**` — real paths to the working code
3. Body: mental model, step order, gotchas. **No bare timing numbers.**
4. **Add a row to the matching table above**, with a status mark.

Size discipline, same as `PEARSON_BROWSER_AUTOMATION.md`:

| Layer | Budget |
|---|---|
| Each table above | ~12 rows — always safe to read whole |
| Each recipe | aim for under ~300 lines |
| This index | keep under ~150 lines; split a category out if it outgrows that |

**A recipe no table names is invisible.** Adding the file is half the job.

## Promoting an app pattern into a recipe

Not every pattern starts here. Something built inside one app stays in that app's
`docs/` — until it gets built **a second time somewhere else**. That is the signal.

| Where it is | Move it here when |
|---|---|
| `<app>/docs/*.md` | The same interaction has now been built in **two or more apps** |
| A recipe here | — it never moves back; if only one app still uses it, leave it and note that |

When promoting: move the file, generalize the exemplar list to name **every** app that
uses it, add the index row, and leave a one-line pointer in the app doc it came from.

The reverse also holds — if something in here turns out to be true of exactly one app
and unlikely to spread, it is an app doc wearing the wrong hat. Move it out.

---

*Created 2026-08-02 by consolidating three scattered libraries: `electron-toolbar/electron-app/patterns/` (16), `School Scrips/Math App Studio/.cursor/rules/` (9), and single rules from `canvas-kit` and `Video Player`. The `.mdc` originals were Cursor glob rules that only fired when a matching file happened to be open in an editor tab — which is not how Chase works.*
