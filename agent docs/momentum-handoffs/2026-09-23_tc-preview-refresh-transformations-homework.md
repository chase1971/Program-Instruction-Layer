# Momentum handoff — TC Preview Refresh broken + Transformations Homework (local)

**Written:** 2026-09-23 (Wednesday, ~7:35 PM)

**Supersedes:** `2026-09-22_student-tester-shared-tester-and-portal-access-bug.md` (different thread; M1314 UUID fix may still be undeployed on Live).

---

## 1. Objective and current phase

**Two threads in this session:**

### A. Transformations Homework (student-portal) — **code complete locally, not deployed**

Chase wanted a unified **Transformations Homework** shell (Matrix GP-style home with Start/Resume for Identifying and Graphing), resume without intro/badge popups, legacy route redirects, separate Supabase activity IDs unchanged for grading.

**Phase:** Implementation done; **84/84** student-portal tests pass. All changes **uncommitted**. Preview still shows **old two-tile layout** when Macro App serves **Live/Netlify** or when Refresh does not reload local Vite.

Also added: hide `transformations/identifying` and `transformations/graphing` from **ClassworkView** (published Supabase duplicates); redirect `quiz/transformations/...` to homework route.

### B. Teacher Console Preview Refresh — **broken; Chase blocked**

Chase reports the **Refresh** button under the embedded Student Portal preview **does nothing** (no visible reload). He also rejects the **Preview log** side panel — activity lines are useless there and **disappear**; he wants logging in **DevTools console only** (like the rest of Macro App), and the side panel should stay **errors-only**.

**Phase:** Prior agent refactored refresh into `useTeacherConsolePreviewRefresh` + `portalPreviewActivityLog.ts` and renamed side panel to "Preview log". Chase says this made things worse. **Fix refresh + revert logging UX is the immediate next step.**

---

## 2. Chase's desired feel

- **Refresh must visibly reload the portal preview** — he uses it to pick up local student-portal code in Preview mode and to recover from blank/hung preview.
- **No activity logging in the side panel.** That panel is for **embedded portal console errors**, not Macro App narration. DevTools `console.info` (via `createFeatureLogger` / `moduleLogStore`) is where refresh diagnostics belong — same as Gradebook, Browser slots, etc.
- **Preview mode = local code** (`127.0.0.1:5340`); **Live = Netlify**. He expects Preview Refresh to show uncommitted homework work without deploying.
- Unified **one** "Transformations Homework" tile — not separate Identifying/Graphing built-ins or classwork duplicates.
- Resume flows: no intro popup, no badge hint on resume, manual Next on correct screens (transformations-app fixes landed).

---

## 3. Accepted decisions

| Decision | Why |
|---|---|
| Unified homework shell with GP-style home | One student entry; separate grading IDs preserved |
| Hide published `transformations/*` from classwork list | Avoid duplicate tiles; homework built-in is the entry |
| Legacy hash routes + `quiz/transformations/*` → homework | Old links still work |
| Preview first-paint gate only waits **first maps load** (`useTeacherConsolePreviewFirstPaint`) | Dashboard gate caused blank preview on map refresh |
| `[PortalPreview]` prefix in side panel = **embedded webview console errors only** (electron `browser-slot-console-forward.js`, `level === 'error'`) | Pre-existing design — do not hijack for activity logs |

---

## 4. Rejected directions — do not rediscover

| Rejected | Why wrong |
|---|---|
| **"Preview log" side panel for refresh narration** | Chase: useless, disappears, not what the panel is for |
| **`logPortalPreviewActivity` → `[PortalPreview]` moduleLogStore lines** | **Collides** with embedded console-error prefix; pollutes errors panel |
| **Tying Refresh button `isRefreshing` to global `isLoading \|\| isLoadingMaps \|\| isLoadingResults`** | Hung forever when roster reload stalled; button stuck "Refreshing…" |
| **`refreshAll()` before browser reload** (old inline handler) | Blocked visible reload on slow/hung roster fetch — felt broken |
| **Assuming screenshot's two transformation tiles mean code was reverted** | They match **committed** `portalHomeApps.ts` (Netlify / stale embed), not local homework code |
| **Deploying student-portal mid-debug** | Chase testing in Preview first; Live still old until deploy |

---

## 5. Current implementation state

### student-portal (uncommitted — `School Scrips/student-portal`)

| Area | Key files |
|---|---|
| Homework shell | `TransformationsHomeworkEntry/View/HomePanel.tsx` |
| Routing | `portalHomeApps.ts`, `usePortalRoute.ts`, `App.tsx`, `MatrixHomeView.tsx` |
| Classwork filter | `classworkData.ts` — excludes `transformations/identifying`, `transformations/graphing` |
| Resume/popup fixes | `transformations-app` (separate repo folder): `useIdentifyingTransformations.ts`, badge hint |

**Tests:** 84/84 pass.

**What Preview should show after a working Refresh (local dev):** Math Survey in In Progress (classwork); **one** built-in tile **Transformations Homework** below (`Identifying + Graphing · Guided practice`).

### Macro App (partial uncommitted — `School Scrips/Macro App`)

**Refresh-related (untracked unless noted):**

| File | Status | Notes |
|---|---|---|
| `useTeacherConsolePreviewRefresh.ts` | **Untracked (new)** | Replaced inline handler in `AppMainPanel.tsx` |
| `portalPreviewActivityLog.ts` | **Untracked (new)** | Uses `[PortalPreview]` → **pollutes errors panel** |
| `refreshPortalPreview.ts` | Modified | Added activity logging; reload path unchanged |
| `useTeacherConsolePreviewFirstPaint.ts` | **Untracked (new)** | Good — keep |
| `useStudentProgressPortalMaps.ts` | Modified | Added `hasResolvedMapsOnce` — good — keep |
| `AppMainPanel.tsx` | Modified | Wires `previewEmbedRefresh` hook |
| `TeacherConsolePreviewConsoleErrorsPanel.tsx` | Modified | Renamed to "Preview log" — **revert labels** |
| `ConsolePreviewWorkspaceScreen.tsx` | Modified | First-paint wait logs via `logPortalPreviewActivity` — **remove** |

**Other dirty Macro App files** (exit-ticket stats, browser modal, etc.) are **same session tree** but **not** the refresh complaint — don't scope-creep unless Chase asks.

### Likely root cause — Refresh "does nothing"

1. **`refreshPortalPreview`**: when preview URL unchanged, `navigate` returns `{ skipped: true }` → calls `browser.reloadSlot()` via **`voidLoggedIpc` (not awaited)** → async refresh **resolves immediately**; reload may not run or may fail silently if slot inactive.
2. **No cache-bust** on dev refresh — even a successful reload might serve cached bundle (less likely with Vite HMR, but navigate-skip path is suspicious).
3. **Prior "working" feel** may have been **`refreshAll()` blocking** before navigate — slow but sometimes masked timing issues.

**Read for fix:** `refreshPortalPreview.ts`, `useTeacherConsolePreviewRefresh.ts`, `AppMainPanel.tsx` (git diff vs HEAD), `electron-app/browser-view-slots.js` navigate skip + reload, `useTeacherConsolePortalPreview.ts` (auto-nav on mount — compare patterns).

---

## 6. Open questions and constraints

- **Chase has not confirmed** whether Preview dev server (`127.0.0.1:5340`) is running when he hits Refresh — hook tries `portalDevServer.startServer()` if not.
- **Live Netlify** will show old two-tile portal until student-portal deploy — expected.
- **Do not commit/push** unless Chase asks (end-of-session / "put on GitHub").
- **Do not launch GUI** without permission (AGENTS.md).
- M1314 portal-access UUID fix from 2026-09-22 handoff — verify whether still undeployed on Live; separate from homework.

---

## 7. Exact next step (start here)

**Fix Teacher Console Preview Refresh button** in Macro App:

1. **Revert side panel UX:** `TeacherConsolePreviewConsoleErrorsPanel.tsx` → title **"Console errors"** again; empty message **"No console errors."** Panel keeps filtering `linePrefix: '[PortalPreview]'` — **errors only** from embedded webview forwarder.

2. **Remove or repurpose `portalPreviewActivityLog.ts`:** Delete activity lines from `[PortalPreview]` store prefix. If refresh needs logging, use **`createFeatureLogger('[PortalPreviewRefresh]', 'student-progress')`** or `[BrowserSlot]` — a prefix **not** wired to the side panel. Logs already mirror to DevTools via `moduleLogStore` → `console.info`.

3. **Make Refresh actually reload:**
   - **Always** force reload on manual Refresh — e.g. `await` IPC `browserView.reload(student-portal-preview slot)`, **or** append `&_tcRefresh=<timestamp>` to dev preview URL so navigate is not skipped.
   - Do **not** block on `refreshAll()` before reload (Chase's original hang).
   - Optional: run `refreshAll()` in background after reload succeeds (current hook intent — keep if reload works).

4. **Verify headlessly:** unit test for refresh hook if feasible; otherwise document hand-test: Preview mode → Refresh → portal visibly reloads → local homework tile appears.

5. **Then** (if Chase wants): deploy student-portal for Live.

**Read first:** this file → `Macro App/renderer/src/utils/studentProgress/refreshPortalPreview.ts` → `Macro App/docs/EMBEDDED_BROWSER_AND_MODALS.md` (if activateSlot blocks) → `agent docs/recipes/` only if stuck.

---

## Copy-ready verification (Chase — after fix)

Macro App Teacher Console → course tab with portal map → **Preview** (not Live) → Admin → Refresh → embedded portal reloads; DevTools shows `[PortalPreviewRefresh]` lines; side panel **Console errors** stays empty unless the portal page throws; scroll home → **Transformations Homework** single tile.
