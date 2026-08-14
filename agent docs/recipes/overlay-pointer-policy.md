# Overlay pointer policy (click-through vs block background)

> **You might say:** "click through the overlay", "block clicks in the game", "pointer policy", "don't register clicks under the pill"
> **What it is:** Per-overlay setting for poll-based overlays (key pills, tabletop R/2) — orthogonal to the four behavior modes.

**Exemplar files:**

- `electron-toolbar/overlay-creator/lib/overlay-pointer-policy.js`
- `electron-toolbar/electron-app/src/window-helpers.js` — `createOverlayBlockGate`
- `electron-toolbar/overlay-creator/frontend/key-overlay-host-runtime.js`
- `electron-toolbar/electron-app/src/tabletop-overlay-runtime.js`

Cross-link: scroll zones use a **different** mechanism — [scroll-zone-click-block.md](./scroll-zone-click-block.md).

---

## Two policies

| Policy | Value | Behavior |
|---|---|---|
| Click through | `through` (default) | Window uses `setIgnoreMouseEvents(true, { forward: true })`. Dwell/hover via cursor poll. Clicks reach the app below. |
| Block background | `block` | While cursor is inside the overlay hit region, main process sets `setIgnoreMouseEvents(false)` **without** `forward` — clicks are absorbed. Window stays `focusable: false` + focus-stealing prevention. Renderer does **not** treat mouse down as overlay activation; dwell still runs via central cursor poll. |

---

## Not the toolbar/arrow pattern

`click-through-windows.md` (in `electron-toolbar/docs/recipes/`) describes **interactive regions** — temporarily disabling click-through so buttons receive clicks.

**Block background** is the opposite intent: the overlay never becomes clickable; it only **stops** clicks from reaching the game.

---

## Storage

- Per overlay: `overlayRegistry.behaviorOverrides[id].pointerPolicy` via `overlay-registry-service.js`
- Saved setups: each preset item carries `pointerPolicy` alongside `mode` and optional key `bounds`

---

## When to use which

- **Through:** You want to click the game/UI under the overlay while the overlay is visible (current default).
- **Block:** Accidental clicks under a pill would fire in-game actions; you still activate the overlay via dwell hover, not direct click.

---

## Implementation checklist

1. Add policy to registry + preset snapshot.
2. Pass `pointerPolicy` in pill specs / tabletop query params.
3. Renderer tracks cursor over block-policy regions → IPC `overlay-block-enter` / `overlay-block-leave`.
4. Main process ref-counts via `createOverlayBlockGate(win)`.

Timing values live in dwell settings — do not copy numbers from this doc.
