# Momentum handoff — Macro App launch regression + gradebook/hooks work (uncommitted, startup worse)

**Written:** 2026-09-26
**App:** `School Scrips/Macro App`

> Previous `latest.md` (2026-09-25 gradebook remediation Phase 3 next) is preserved at
> `agent docs/momentum-handoffs/2026-09-25_gradebook-remediation-phase3.md`.

## Read first

1. **`School Scrips/Macro App/docs/plans/GRADEBOOK_REMEDIATION_PLAN.md`** — gradebook restore work (Phases 0–4 largely implemented, uncommitted).
2. **`School Scrips/Macro App/launch.bat`** — comment explains stale Vite on port 5328 causes hook-signature mismatches; full quit + `launch.bat` required for dev testing.
3. **`C:\Users\chase\AppData\Roaming\macro-app\logs\macro-app.log`** — main-process boot/reveal lines; `[renderer]` console forward added this session (may be empty on older launches).
4. **`electron-app/main.js`** § `createMainWindow` — splash/reveal logic (`revealOnce`, `SPLASH_SLOT_GRACE_MS`, `browserView.hide()` before show).

Do **not** treat restructure session files as in-scope unless Chase names them — large uncommitted diff includes restructure Phase 4 + gradebook remediation mixed together.

## 1. Objective and current phase

Two parallel threads got tangled in one uncommitted diff:

| Thread | Intent | Status |
|---|---|---|
| **Gradebook remediation** (Phases 0–4) | Snapshot restore points, history UX, contract tests, flush-on-close | Largely coded; **544+ vitest tests passed** at last headless check; **not committed** |
| **Launch + hooks crash** | Fix compressed-then-expands flash, Rules-of-Hooks crash on every launch, `render-process-gone` | **Multiple fix rounds; Chase reports startup is now significantly worse than before any of this** |

**Current phase for the next agent:** **Stop making launch worse — diagnose and revert or fix launch/splash/browser-reveal sequencing.** Gradebook remediation can wait until the app opens cleanly again.

## 2. Chase's desired feel (his words / STT)

- Every launch: app looked **compressed then expanded** to correct size (original complaint).
- **React hooks error** every launch (MacroAppRoot chain through gradebook hooks) — still reported after attempted fix.
- After latest launch changes: **browser visible ~5 seconds before tabs and side panels** — "startup has become significantly worse than what it was."
- Before momentum handoff: **"this current change has made it worse"** — wants next agent informed, not more blind tweaks.
- Headless verification only unless he explicitly permits GUI launch.
- **No commit/push** unless he asks.

## 3. Accepted decisions (still valid)

- Gradebook restore architecture: **snapshot-based restore points** per `GRADEBOOK_REMEDIATION_PLAN.md` (not seq-only restore).
- `useGradebookEditSession`: merged `restoreFromSnapshotBatch` + `undoSnapshotRestore` into single **`runSnapshotRestore`**; **`useGradebookFlushOnAppClose`** at end of hook list.
- `useGradebook.ts`: single **`applyHistoryRestore`** API wired from `AppSidePanel.tsx`.
- Launch: **`revealOnce` guard** — only one main-window reveal per boot (log at 9:13 PM showed single reveal; double-reveal shrink-expand was real in earlier logs).
- **`launch.bat` kills port 5328** before dev start — stale Vite bundle can cause hook-order crashes that look like code bugs.

## 4. Rejected / failed directions (do not rediscover)

| Attempt | Why it failed / made things worse |
|---|---|
| **Double `revealOnce` fix alone** | Stopped second resize flash in log, but Chase still saw flash + hooks error |
| **Create window at full launch-monitor work area + pre-show maximize** (`launch-monitor.js` hidden path) | BrowserView bounds synced while window hidden, then maximize on reveal → **native browser covered full window for ~5s until bounds resync** |
| **Initial `activateSlot('browser', { visible: true })` on boot** | Fires before chrome mounted; splash `fireFirstVisibleActivation` interacts badly with reveal timing |
| **3s display-scale boot grace blocking focus/resize refresh** | Removed in last round; may have delayed layout recovery |
| Assuming **renderer errors appear in macro-app.log** without `[renderer]` forward | They did not until `main.js` added `console-message` → `moduleLog` this session |
| Treating **`render-process-gone exitCode=-36861`** as every-launch | Log showed it **once** (8:43 PM); later launches had no crash line |

**Latest round (still unverified, Chase says worse):**
- Reverted window create to **1440×900**
- Removed pre-show full-area maximize path
- Boot browser **`visible: false`** in `useEmbeddedBrowser.ts`
- **`browserView.hide()`** before `mainWindow.show()` in `revealMainWindow`
- Kept `revealOnce`, skip redundant `applyMonitorScales` if unchanged

## 5. Current implementation state

### Launch / electron (touched this session)

| File | Changes |
|---|---|
| `electron-app/main.js` | `revealOnce` + `mainWindowRevealed`; `ensureWindowOnLaunchDisplay` before `show()`; `browserView.hide()` before reveal; `[renderer]` console forward; gradebook flush on close |
| `electron-app/launch-monitor.js` | Skip `setBounds` when already visible+maximized; pre-show hidden path **added then removed** |
| `electron-app/launch-monitor.test.js` | Test for maximized skip |
| `renderer/src/utils/shared/displayZoom.ts` | Sync apply on init; single async hydrate; skip if scale unchanged; boot grace **added then removed** |
| `renderer/src/hooks/browser/useEmbeddedBrowser.ts` | Initial boot **`visible: false`** (was `true`) |

### Hooks / gradebook (earlier in same diff)

| File | Changes |
|---|---|
| `useGradebookEditSession.ts` | `runSnapshotRestore`, `useGradebookChangeLogWriter`, `useGradebookFlushOnAppClose`, `flushAndResetSession` |
| `useGradebook.ts` | `applyHistoryRestore`; moved `useGradebookStartupPrehydrate` to end of hook list |
| `SettingsButton.tsx` | Import order fix (setState-during-render warning was suspected) |
| Many Phase 3–4 gradebook/history/restore files | See `git status` — large uncommitted tree |

### Git

- **Macro App repo:** large dirty working tree; **nothing committed this session** for launch/hooks/gradebook bundle.
- **Do not commit** unless Chase asks.

### Verification already run (headless)

- `npx tsc -p tsconfig.app.json --noEmit` — clean after hook-order move
- `npx vitest run src/__tests__/gradebook-restore-contract.test.ts` — passed (earlier in session)
- `node --test electron-app/launch-monitor.test.js` — 6 pass
- `npx vitest run src/utils/shared/displayZoomProfiles.test.ts` — 4 pass

### Log evidence (macro-app.log)

- **9:13 PM launch:** single `window revealed (no visible slot within grace window)` — double-reveal fix worked in main process.
- Browser slot `visible=true` activate ~same second as reveal.
- **No `[renderer]` / `[AppError]` lines** in file before console forward — hooks error likely only in dev terminal or error boundary UI.

## 6. Open questions and constraints

1. **Exact hooks error text** — not captured on disk; need from error boundary UI or devtools after launch with `[renderer]` forward enabled.
2. **Revert launch changes wholesale?** — Chase says current state is worse than baseline; next agent may need to `git checkout -- electron-app/main.js electron-app/launch-monitor.js renderer/src/hooks/browser/useEmbeddedBrowser.ts renderer/src/utils/shared/displayZoom.ts` and re-apply only `revealOnce` if that was the only net win.
3. **Original splash design** (from `main.js` comments): wait for first **visible** slot activation OR grace timer — booting browser hidden means grace always wins (~6s); may be OK if chrome+ browser appear together after fix.
4. **Stale Vite** — always test via **`launch.bat`**, not relaunching Electron alone.
5. **Frozen / permissions:** no GUI launch without Chase; no commit/push; file size caps apply (`useGradebook.ts` ~750 lines).

## 7. Exact next step

1. Read this file and **`electron-app/main.js`** `createMainWindow` + **`useEmbeddedBrowser.ts`** initial boot effect (~line 508).
2. **Compare launch behavior to last committed `main.js`** (`git show HEAD:electron-app/main.js`) — consider reverting all launch-touched files to HEAD, then re-introducing **only** `revealOnce` (proven in log) with a test plan Chase can describe.
3. Capture **first line of error boundary** or new **`[renderer]`** lines from `macro-app.log` after one `launch.bat` run (Chase reports back — do not launch yourself unless permitted).
4. **Do not** continue gradebook Phase 5 or sandbox testing until startup is acceptable again.

## Copy-ready context for gradebook work (when launch is fixed)

Phases 0–4 of `GRADEBOOK_REMEDIATION_PLAN.md` are implemented in working tree; Phase 5 (backup "newest" across New Year) and sandbox manual test remain. Contract tests in `gradebook-restore-contract.test.ts` should stay green.
