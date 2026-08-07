# Electron Shell: Display Scaling

> **Required for every Electron desktop app** Chase builds: the manual **Display** button +
> slider + Fit-to-window, scaling the whole app via `#app-scale-frame`. This solves a
> real, confirmed bug — UI clipping at high Windows display scaling — and Chase actively
> uses it (open Display, drag slider until it looks right).
>
> **Optional, not required: automatic per-monitor memory** — detecting which monitor the
> window is on and auto-restoring a distinct remembered scale per monitor (Phase 3 below).
> **Downgraded 2026-08-07** — Chase confirmed that even in Macro App, the exemplar for this
> half of the spec, it isn't reliably saving him the manual re-adjustment it's meant to save,
> and physically different monitors can't be made to "look the same" through zoom alone
> regardless. Manual-only (one remembered scale, no per-monitor auto-switch) is a fully
> legitimate implementation. Build Phase 3 only if Chase specifically asks for it.
>
> **AI:** Implement Phases 1–2 (manual Display button + slider) for every Electron shell.
> Skip Phase 3 (automatic per-monitor detection/memory) unless asked. Read this file and
> copy/adapt from the **exemplar** below.
>
> **Exemplars:**
> - Calendar 2.0 — display scale only (`School Scrips/Calendar 2.0`)
> - Macro App — display scale + embedded `BrowserView` / `WebContentsView` (`School Scrips/Macro App`)
>
> **Last verified:** 2026-08-07

---

## Policy (one line)

**Every Electron app gets:** `#app-scale-frame` + transform scale + title-bar **Display**
button (slider + fit). **Optional:** per-monitor `localStorage` + main-process monitor IPC,
so the remembered scale is per-monitor instead of one global value.

---

## Problem this solves

On Windows with high display scaling (e.g. 225%), UI can be **clipped** with no scroll — layout stays full size while the window is smaller.

| Requirement | Notes |
|-------------|--------|
| Scale the **whole app** | Real controls, not a bitmap shrink |
| **Simple control** | **Display** button, slider 35–100%, **Fit to this window** |
| **Accessibility** | Large targets; **no backdrop-click** to close Display modal |
| Modals scale too | Portal roots inside `#app-scale-frame` |
| *(Optional)* **Per-monitor memory** | Dragging between monitors restores each monitor's own last scale — build only if asked; see banner above |

---

## Do NOT use

| Approach | Why |
|----------|-----|
| CSS `zoom` on `#root` | Layout stays full size → clipping and gray margins |
| Auto-scale on startup | Fights user intent; wrong feel on first load |
| Long DPI/resolution preset lists | Too much re-tuning when switching monitors |

---

## Architecture

```
Electron main: screen.getDisplayNearestPoint(window center)
  → IPC: get-active-monitor-info, active-display-changed
Renderer: displayZoom.ts
  → localStorage: { monitorId: scale }
  → transform on #app-scale-frame
UI: Display button → DisplayScaleModal (slider, fit, Done)
Optional: manualZoom.ts (Ctrl+±/0)
```

**Scale math:** `transform: scale(z)` on `#app-scale-frame` with `width/height: (100/z)vw/vh`, `transform-origin: top left`. At `z === 1`, clear transform.

**Fit to window:** `min(innerWidth/DESIGN_W, innerHeight/DESIGN_H)` clamped (default design size `1920×1080`).

---

## Per-app constants (change on every new app)

| Constant | Pattern | Example |
|----------|---------|---------|
| `STORAGE_KEY` | `{appSlug}-display-by-monitor` | `calendar20-display-by-monitor` |
| Portal ids in `ensureScaleFrame()` | Match `index.html` | `root`, `modal-portal`, `alert-portal` |
| Display modal path | App-specific folder | `src/components/.../DisplayScaleModal.tsx` |
| Title bar button | Custom chrome / shell component | Label: **Display** |

---

## Files to create or port (from exemplar)

Copy from Calendar 2.0 and adapt names/paths/storage key:

| Exemplar file | Purpose |
|---------------|---------|
| `src/utils/displayZoom.ts` | Frame, apply zoom, storage, init watcher |
| `src/utils/manualZoom.ts` | Ctrl+±/0 shortcuts (optional but recommended) |
| `src/components/.../DisplayScaleModal.tsx` | Slider UI (move to your shell/components folder) |
| `src/electron.css` | `#app-scale-frame`, `html/body overflow` |
| `src/main.tsx` | Call `initPerMonitorDisplayZoom()` + `initManualZoom()` **before** `createRoot` |
| `src/types/electron.d.ts` | `getActiveMonitorInfo`, `onActiveDisplayChanged` |
| `electron/main.js` | `getMainWindowMonitorInfo`, `notifyActiveDisplayChanged`, IPC, screen events |
| `electron/preload.js` | Bridge methods |
| Shell component (e.g. title bar) | **Display** button + modal `open` state |

`index.html` must include portal mount nodes if the app uses modals (`modal-portal`, `alert-portal`).

---

## Electron main (required IPC)

**Monitor under window:** center of `mainWindow.getBounds()` → `screen.getDisplayNearestPoint(center)`.

**Invoke:** `get-active-monitor-info` → `{ id, label, width, height, scaleFactor }`.

**Push event:** `active-display-changed` when monitor id changes.

**Subscribe in main:**

- `mainWindow`: `move`, `resize`, `focus`
- `screen`: `display-metrics-changed`, `display-added`, `display-removed`

Dedupe notifications with `lastNotifiedDisplayId`.

**Restart Electron** after changing main/preload (HMR is not enough).

---

## Preload bridge

```js
getActiveMonitorInfo: () => ipcRenderer.invoke('get-active-monitor-info'),
onActiveDisplayChanged: (callback) => {
  const handler = (_event, info) => callback(info);
  ipcRenderer.on('active-display-changed', handler);
  return () => ipcRenderer.removeListener('active-display-changed', handler);
}
```

---

## Renderer bootstrap

```ts
import { initPerMonitorDisplayZoom } from "./utils/displayZoom";
import { initManualZoom } from "./utils/manualZoom";

initPerMonitorDisplayZoom();
initManualZoom();

createRoot(document.getElementById("root")!).render(<App />);
```

Import `./electron.css` in `main.tsx` (or equivalent entry).

---

## Embedded browser + modal freeze snapshots (REQUIRED WARNING)

Many Electron shells embed a native browser (`BrowserView` / `WebContentsView`) in a React “hole.” When a modal opens, the live browser is often **detached** and a **PNG snapshot** of the page is shown in the hole so the transition is less jarring.

**Do not use snapshots if this app has per-monitor Display scaling.**

| Why | What goes wrong |
|-----|-----------------|
| Snapshot is a **frozen image** | Resizing the app (Display slider, monitor switch, Fit) scales the **bitmap**, not the live page |
| Looks like a bug | User drags scale and the “browser” appears unchanged — it is still the old screenshot |

### Required behavior

1. **`freezeForModal({ snapshot: false })`** whenever the browser is hidden because a modal is open **and** the user can change Display scale during that flow (always true if Display scaling exists).
2. **Display modal:** while Display is open, freeze with **`snapshot: false`** (Macro App `App.tsx` already does this).
3. **Other modals** over the embedded browser (settings, wizards, pickers): also use **`snapshot: false`** unless Chase explicitly wants snapshots **and** Display scaling is disabled for that session.
4. **Default in `freezeForModal`:** treat snapshot as **opt-in** (`snapshot: true`), not opt-out — so new call sites do not forget.

```ts
// freezeForModal in useEmbeddedBrowser (or equivalent)
const useSnapshot = options?.snapshot === true; // NOT !== false

// Opening Display scale modal
void browser.freezeForModal({ snapshot: false });

// Any modal while Display scaling is enabled
await browserModal?.freeze({ snapshot: false });
```

### Exemplar code (Macro App)

| File | Pattern |
|------|---------|
| `renderer/src/hooks/useEmbeddedBrowser.ts` | `freezeForModal`, `captureSnapshot`, `snapshotDataUrl` overlay |
| `renderer/src/App.tsx` | `freezeForModal({ snapshot: false })` when `showDisplayScaleModal` |
| `renderer/src/components/browser/EmbeddedBrowserPanel.tsx` | Shows `browser-snapshot` img when `snapshotDataUrl` set |
| `electron-app/browser-view.js` | `captureSnapshot()` → `capturePage()` PNG data URL |

Snapshot freeze is fine for **non-scaling** shells or modals where scale cannot change; it is **incompatible** with live Display rescaling.

---

## Display modal UX (required)

- Slider **35–100%**, live preview on `onChange`
- **Save** on slider commit (`mouseup` / `touchend` / `keyup`), not only Done
- **Fit to this window** — saves for current monitor
- **Done** closes; **no overlay backdrop dismiss** (dwell-mouse)
- Min button height ~**48px**; slider height ~**32px**
- Show monitor label + window size

---

## Init checklist (AI — use in order)

### Phase 1 — Mechanics
- [ ] `#app-scale-frame` CSS
- [ ] `ensureScaleFrame()` — move `#root` + portal ids
- [ ] `applyDisplayZoom(z)` — transform + inverse vw/vh; never `zoom` on `#root`
- [ ] Init before React render

### Phase 2 — UI + storage
- [ ] `STORAGE_KEY` for this app
- [ ] **Display** in title bar → modal with slider + Fit + Done
- [ ] Save on slider commit

### Phase 3 — Per-monitor Electron
- [ ] Main + preload + `electron.d.ts` as above
- [ ] `initPerMonitorDisplayZoom()` listens for display-changed + resize/focus

### Phase 4 — Embedded browser (if applicable)

**Electron version (check first):** Read `School Scrips/Macro App/package.json` and use the same **`electron`** version in the new app. Macro’s `WebContentsView` / bounds / `navigationHistory` patterns require that generation (42.x today). Older apps (Video Player, Calendar 2.0, toolbar) still on Electron 28 are valid for **non-embedded** shells only — do not copy their `package.json` Electron pin when copying Macro browser code.
- [ ] `package.json` `electron` matches Macro App (Step 4c in `INIT_NEW_APP.md`)
- [ ] `freezeForModal` defaults to **no snapshot** (`snapshot` opt-in only)
- [ ] Display modal uses `freezeForModal({ snapshot: false })`
- [ ] All other modals over the browser use `{ snapshot: false }` while Display scaling is enabled

### Phase 5 — Verify
- [ ] 100% and 70% — no clip, no page scroll
- [ ] Move window to second monitor — auto switch
- [ ] Persist after restart
- [ ] With embedded browser: open Display, drag slider — browser area should **not** look like a frozen screenshot

---

## New app bootstrap (INIT_NEW_APP)

When `INIT_NEW_APP.md` scaffolds any variant that includes **`electron/`** + a React (or HTML) renderer:

1. Read this file.
2. Port files from Calendar 2.0 exemplar (table above).
3. Set `STORAGE_KEY` to `{appSlug}-display-by-monitor`.
4. Wire **Display** into the app’s title bar / shell.
5. Add to the app’s `CLAUDE.md`: “Electron shell includes per-monitor Display scaling — see cursor-patterns/electron-per-monitor-display-scaling.md.”

---

## Adding to an existing Electron app

1. Implement Phases 1–3 above.
2. Do not remove user’s layout — only add frame + button.
3. Confirm all `createPortal` targets live inside moved portal nodes.
4. Report storage key and that Electron restart is needed after IPC changes.

---

## Known limitations

- Monitor = display under **window center** (not span across two monitors).
- Vite-only browser dev: single `browser-default` scale until Electron runs.
- IPC/preload changes need full Electron restart.

---

## Summary for agents

1. No `zoom` on `#root`.
2. `#app-scale-frame` + `transform: scale(z)` + `(100/z)vw/vh`.
3. `localStorage` map by `display.id`.
4. Main process notifies on monitor change.
5. **Display** button: slider + fit; no backdrop dismiss; save on slider release.
6. Init before `createRoot`.
7. **Embedded browser modals:** `freezeForModal({ snapshot: false })` — snapshots break when Display scale changes.

**Exemplar:** Calendar 2.0 (`School Scrips/Calendar 2.0`). App-specific copy also at `Calendar 2.0/docs/guides/PER_MONITOR_DISPLAY_SCALING.md` (points here).
