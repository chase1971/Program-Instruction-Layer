# Momentum handoff — Gradebook hidden browser load on course click

**Written:** 2026-09-28 (Monday afternoon, Central)  
**Repo:** `School Scrips/Macro App` (uncommitted — PC desktop, post-laptop pull)  
**Status:** Fix implemented, **not yet verified by Chase** after the deadlock/bootstrap rewrite.

---

## Objective and current phase

Chase wants: on the **Gradebook tab**, when he clicks a **course** (App Gradebook view, not D2L toggle), the **hidden Enter Grades browser for that course must load immediately** so Pull is enabled. On his **laptop (16 GB)** other background browser warmups must not starve the selected course; on **PC (32 GB)** same behavior but less pressure.

**Phase:** Root-cause fix landed in working tree; **next agent must verify in running app** and finish if still broken.

---

## Chase's desired feel (his words / intent)

- Click gradebook → click course → **that** browser loads **right then**, not only after opening D2L Gradebook view.
- Pull correctly stays **disabled until the browser is actually loaded** — he confirmed that gating is correct; the bug is the browser **never** loading hidden.
- Laptop should **prioritize** the selected course over staggered preload/warmup of other tabs.
- If browser doesn't load within **~5 seconds** of course click → **`console.error`** saying **"Browser did not load in"** with **why** (blank URL, sign-in page, still loading, wrong page, etc.).
- Opening D2L Gradebook currently **does** eventually load Enter Grades (~5–10s) — acceptable as fallback path but **must not be required**.

---

## Accepted decisions

| Decision | Why |
|---|---|
| **Demand path = `activateSlotIpc(slot, { visible: false, bootstrapUrl })`** — same as `useWorkspaceBrowserPreloader` | Visible Enter Grades already worked via direct IPC + bootstrap; hidden path through `orchestrateHiddenGradebookSlot` **deadlocked** (see Rejected). |
| **`clearGradebookWarmupQueueExcept(courseCode)`** on course select | Suspends queued warmup for other courses when user picks one. |
| **`GRADEBOOK_COURSE_CLICK_LOAD_TIMEOUT_MS = 5000`** + `describeEnterGradesSlotBlocker()` | User-requested timeout + explanatory console error. |
| **In-flight refs** (`hiddenSyncInFlightKeyRef`, `gradebookD2LViewInFlightKeyRef`) | Stops "Maximum update depth exceeded" loop when log lines re-render during D2L view activation. |
| **`confirmGradebookSlotEnterGrades()`** after successful load | Marks warmup ready set so `isGradebookBrowserReadyForSync` / Pull gate can open (secondary to actually loading URL). |

---

## Rejected directions (do not redo)

| Tried | Why wrong |
|---|---|
| **`ensureHiddenD2LSession` / `orchestrateHiddenGradebookSlot` for demand load** | **Deadlock:** `runSerializedForSlot('hidden-attach')` holds the slot queue, then `activate()` calls `runSerializedForSlot` on the **same slot** → activate waits forever → **no navigation, blank slot**. |
| **`attachOnly: true` on hidden course select** | Only attaches webview; **does not navigate** to Enter Grades — Pull stays disabled correctly but browser never loads. |
| **Assuming Pull grey = ready-flag bug only** | Chase corrected: browser **genuinely** not loaded until D2L view opened. |
| **Setting `gradebookD2LViewPrimedKeyRef` only on success (f10c185)** without in-flight guard | Log-driven re-renders re-triggered visible activation → max update depth. Fixed with in-flight key, not by restoring early primedKey alone. |

---

## Current implementation state

### Uncommitted files (Macro App)

```
renderer/src/hooks/browser/useEmbeddedBrowserGradebookNav.ts   — primeHiddenEnterGradesSlot rewrite (bootstrap)
renderer/src/hooks/browser/useEmbeddedBrowser.ts               — export primeHiddenEnterGradesSlot
renderer/src/hooks/shell/useMacroAppGradebookBrowserEffects.ts   — demand load on course click, 5s error, in-flight guards
renderer/src/hooks/shell/useMacroAppShell.ts                     — clearGradebookWarmupQueueExcept on course activate
renderer/src/services/enterGradesSlotService.ts                  — describeEnterGradesSlotBlocker()
renderer/src/services/gradebookD2LBackupSync.ts                — GRADEBOOK_COURSE_CLICK_LOAD_TIMEOUT_MS
renderer/src/services/gradebookSlotWarmup.ts                     — clearGradebookWarmupQueueExcept, confirmGradebookSlotEnterGrades
renderer/src/services/gradebookSlotWarmup.test.ts                — tests (5 pass)
config/d2l-courses.json                                          — machine-local (do not commit)
```

### Key code paths

| Path | File | Behavior |
|---|---|---|
| Course click (App view) | `useMacroAppGradebookBrowserEffects.ts` hidden-sync effect | Calls `primeHiddenEnterGradesSlot`; logs `[Gradebook] COURSE — loading Enter Grades now` |
| Demand hidden load | `useEmbeddedBrowserGradebookNav.ts` → `primeHiddenEnterGradesSlot` | Clear warmup queue → `activateSlotIpc({ visible: false, bootstrapUrl })` → `waitForEnterGradesSlotReady(5s)` → throw with blocker text if fail |
| Visible D2L toggle | same file → `showGradebookCourseSlotVisible` | Works today; bypasses warmup queue |
| Background warmup | `gradebookSlotWarmup.ts` | `WARMUP_MAX_CONCURRENT = 2`; on-demand tiering |
| Workspace preload | `useWorkspaceBrowserPreloader.ts` | Stagger 650ms; also uses hidden `bootstrapUrl` |
| Pull gate | `gradebookBrowserSyncReady.ts` + `useMacroAppShell.ts` | Grey until D2L live + slot ready (hidden) or embedded (visible D2L view) |

### Session context (already on PC)

- Pulled laptop pushes: Macro App `f10c185` (gradebook sync + CI), Programs root doc updates.
- Prior laptop commit `f10c185` added pull grey-until-ready, visible bypass, log pause, loop fixes — **SESSIONS.md** entry dated 2026-09-28 describes mid-refactor state **before** this session's deadlock fix.

### Verification

- **Unit:** `gradebookSlotWarmup.test.ts` — 5 passed (renderer).
- **Runtime:** Chase reported **same behavior** after first fix attempt (ready-flag + prioritize); **not retested** after deadlock/bootstrap rewrite (latest commit in working tree only).

---

## Open questions and constraints

1. **Does the bootstrap fix work on Chase's machine?** Must verify: Gradebook → course click → Pull enables within ~5s **without** D2L toggle.
2. **`ensureHiddenD2LSession` still uses orchestrateHiddenGradebookSlot** for import/sync/other callers — may still deadlock on those paths; demand path bypasses it. Do not route course-click through orchestrateHidden again.
3. **16 GB laptop:** If still slow, consider pausing `useWorkspaceBrowserPreloader` while Gradebook module active + course loading (not implemented).
4. **No GUI launch without permission** — hand off test steps to Chase; do not open Macro App unprompted.
5. **No commit/push** unless Chase asks — working tree is dirty, uncommitted.

---

## Read first (next agent)

1. This file.
2. `School Scrips/Macro App/docs/sessions/SESSIONS.md` — top entry (2026-09-28) for prior context.
3. `School Scrips/Macro App/docs/BROWSER_TAB_INTEGRATION.md` — Phase 3 warmup / demand priority.
4. Code: `useEmbeddedBrowserGradebookNav.ts` (`primeHiddenEnterGradesSlot`), `useMacroAppGradebookBrowserEffects.ts` (hidden-sync effect), `electron-app/browser-view-slots.js` (`activateSlot` bootstrap rules: hidden passes bootstrap to `ensureSlot`).

---

## Exact next step

**Verify the bootstrap fix in Macro App (dev or installed build):**

1. D2L logged in → Gradebook tab → **App Gradebook view** (not D2L toggle).
2. Click a course.
3. Expect within ~5s: log `[Gradebook] … Enter Grades ready` and **Pull un-greys**.
4. If fail: console should show `[Gradebook] COURSE — Browser did not load in — <reason>` from `describeEnterGradesSlotBlocker`. Check `macro-app.log` for `[BrowserSlot] activate gradebook:COURSE … bootstrap=…`.

If still broken after verification, compare hidden demand path to working visible path line-by-line in `browser-view-slots.js` (`activateSlot` lines ~418–487) and confirm `bootstrapUrl` reaches `safeLoadUrl` for `visible: false`.
