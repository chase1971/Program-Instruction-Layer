# Scroll zone click block (dwell pause)

> **You might say:** "block clicks under scroll zone", "scroll zone doesn't click through", "dwell pause over zone"
> **What it is:** Global scroll-zone setting — **not** the same as overlay pointer policy.

**Exemplar files:**

- `electron-toolbar/modules/scroll/backend/scroll_zone_dwell_pause.py`
- `electron-toolbar/modules/scroll/backend/scroll_zone_visual_settings.py`
- `electron-toolbar/electron-app/src/scroll-zone-settings-panel.js` — **Block clicks under zone** toggle

Cross-link: Electron overlay pills/tabletop use [overlay-pointer-policy.md](./overlay-pointer-policy.md).

---

## How scroll zones work

Scroll zone capsules stay **fully click-through** (`WS_EX_TRANSPARENT` in Python/Tk). Wheel scroll is detected by cursor polling, not by receiving mouse events on the overlay window.

**Block clicks under zone** (`blockClicksUnderOverlay`):

1. Cursor enters a locked scroll zone capsule.
2. `scroll_zone_dwell_pause.py` broadcasts `dwell_scroll_zone_pause` with `{ active: true }`.
3. Dwell-click cannot fire while paused — accidental dwell activation is suppressed.
4. The zone window **remains transparent**; wheel events still reach the page under the cursor.

When the setting is off, dwell is not paused over zones.

---

## Settings path

Toolbar **Settings** → scroll zone section → **Block clicks under zone** (or scroll profiles setup UI).

Persisted in `scroll_zone_visual_settings.json` via `scroll-visual-settings.js`.

---

## vs overlay pointer block

| | Scroll zone block | Overlay `block` policy |
|---|---|---|
| Window | Always transparent | Electron overlay window |
| Mechanism | Pause dwell system | Absorb mouse events (no forward) |
| Scope | All scroll zones globally | Per key pill / tabletop overlay |
| Wheel scroll | Still works | N/A (not a scroll zone) |

Use scroll-zone block when accidental **dwell** fires through a scroll capsule. Use overlay block when **any** click under a pill would hit the game.
