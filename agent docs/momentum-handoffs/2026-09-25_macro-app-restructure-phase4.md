# Momentum handoff — Macro App restructure Phases 1.5–3 complete; Phase 4 next

**Written:** 2026-09-25
**App:** `School Scrips/Macro App` — embedded-browser / Teacher Console restructure

## Read first

1. `School Scrips/Macro App/docs/plans/MACRO_APP_RESTRUCTURE_RECOMMENDATIONS.md` — authoritative phase order (bottom-up).
2. `School Scrips/Macro App/AGENTS.md` — keyword row for restructure vs TC smoothness plan.
3. `School Scrips/Macro App/docs/plans/TEACHER_CONSOLE_PREVIEW_SMOOTHNESS_PLAN.md` — overlaps Phase 4 preview work; reconcile before duplicating TC-local fixes.

## 1. Objective and current phase

Chase is executing the **Macro App restructure recommendations** — harden the slot layer and automation coordination bottom-up, then thin the Teacher Console on top.

| Phase | Status |
|---|---|
| **0 / main Phase 1** (crash logging, one slot contract in main, isolation restore) | **Complete** — committed; Chase reports behavior good (`SESSIONS.md` 2026-09-25). |
| **1.5** (shell room: extract gradebook pipeline, move TC preview refresh into TC shell hook) | **Complete** — uncommitted. |
| **2** (one lane in renderer: honest adapter, store-owned active slot, queued `activateSlot`) | **Complete enough to ship** — core contract done; `activateSlotForTab` not fully rewritten through orchestrator (mechanical tail). |
| **3** (isolation lock) | **Complete** — main was Phase 1; this session added renderer lock IPC + button loading states. |
| **4** (Teacher Console thin consumer) | **Next.** |

Chase confirmed tab switches / preview refresh feel **fine** after 1.5+2. He **could not verify gradebook import** (access constraint, not a reported regression).

## 2. Chase's desired feel

- **Bottom-up, not TC-first.** Fix slot/orchestrator/isolation layers before adding Teacher-Console-local retries or guards.
- **Independently shippable phases** — each leaves the app green; headless tests then a flat handoff statement (no "want me to…").
- **No GUI from the agent** — dwell mouse; ask before launching the app. Verify headlessly; Chase live-tests when he can.
- **Structural moves without behavior change** in extraction phases (1.5, 5).
- **Deletions and new patterns need his OK** — orphaned TC screens, first-ever React context, API removals.

## 3. Accepted decisions

### Phase 1.5 (this session, uncommitted)

- **`useMacroAppShellGradebookPipeline.ts`** — gradebook warmup, bulk pull, D2L import sync, `navigateBrowserTabRef` moved out of `useMacroAppShell.ts` (800 → ~720 lines).
- **Preview refresh ownership** — `usePortalPreviewSectionId` + `useTeacherConsolePreviewRefresh` moved into `useMacroAppStudentProgressShell.ts`; returns `studentProgress.previewEmbedActions`. `AppMainPanel.tsx` no longer computes refresh (~604 → ~589 lines).

### Phase 2 (this session, uncommitted)

- **`embeddedBrowserOrchestratorAdapter.ts`** — returns real `{ ok, reason, url }`; no more always `{ ok: true }`.
- **`slotOrchestrator.ts`** — `showSlotAtUrl` returns `false` on activate failure; dropped dead `force` option; navigates when bootstrap URL ≠ target after activate.
- **`slotSessionStore.ts`** — added `isBrowserEmbedded`; `useEmbeddedBrowser.ts` reads active slot from store via `useSlotSessionStore`.
- **Queue split** — `activateSlotIpc` (raw, for orchestrator inside an already-serialized op) vs public `activateSlot` (wrapped in `runSerializedForSlot`). Gradebook nav adapter uses `activateSlotIpc`.
- **Tests:** `embeddedBrowserOrchestratorAdapter.test.ts`, updated `slotOrchestrator.test.ts`.

### Phase 3 (this session, uncommitted renderer; main already in Phase 1 commit)

- **`browser-slot-isolation-lock.js`** — `subscribeBrowserSlotIsolationOwner` + notify on acquire/release.
- **`browser-view.js` + preload** — `browserView:getIsolationLockOwner`, `browserView:isolationLock` event, `getIsolationLockOwner` / `onIsolationLockChange` in renderer.
- **`useBrowserSlotIsolationLock.ts`** — renderer hook.
- **Button states while lock held:**
  - Managing Grades **Bulk Edit** — "Restoring browser…" (disabled, not Cancel) when another module holds the lock.
  - Makeup Exam **Start Automation** — same pattern.
- **`useGradesBulkEdit`** — exports `isOwnAutomationBusy`, `isIsolationBlocked`; `isBusy` includes external lock for modal disables.

### Already accepted in main (Phase 1 commit `d7778ab` area)

- App-wide isolation lock; `runningByModuleId` until restore completes; per-slot restore deadlines; skip hidden `student-portal-preview`; makeup exam uses `captureRestore: true` (`docs/MAKEUP_EXAM_CDP_INTEGRATION.md`).

## 4. Rejected / do-not-rediscover

- **Do not fix preview jank inside TC first** — extend the slot lane (Phase 2) or isolation lock (Phase 3), not TC-local timeouts/retries.
- **Do not reintroduce `force` on orchestrator activate** — Phase 1 lean: explicit `navigate` when reload needed.
- **Do not show Cancel on Bulk Edit when only the global isolation lock is held** — that would call cancel on someone else's run. Use waiting/disabled state instead.
- **`TEACHER_CONSOLE_PREVIEW_SMOOTHNESS_PLAN.md` Phase 0/0A** — was written before restructure phases 1.5–2 landed; do not blindly run its Phase 2 behavior edits without checking what's already in the lane. Prefer `MACRO_APP_RESTRUCTURE_RECOMMENDATIONS.md` Phase 4 for TC work now.
- **Do not commit `config/d2l-courses.json`** — machine-local.

## 5. Current implementation state

**Nothing committed for Phases 1.5–3.** Last Macro App commit: `d7778ab` ("Document Phase 1 completion…").

**Uncommitted Macro App changes (restructure session):**

| Area | Files |
|---|---|
| Electron | `browser-slot-isolation-lock.js`, `browser-slot-isolation-lock.test.js`, `browser-view.js`, `preload.js` |
| Renderer shell | `useMacroAppShell.ts`, `useMacroAppShellGradebookPipeline.ts` (new), `useMacroAppStudentProgressShell.ts`, `AppMainPanel.tsx` |
| Renderer browser | `useEmbeddedBrowser.ts`, `useEmbeddedBrowserGradebookNav.ts`, `useBrowserSlotIsolationLock.ts` (new), `embeddedBrowserOrchestratorAdapter.ts`, `embeddedBrowserOrchestratorAdapter.test.ts` (new) |
| Orchestrator/store | `slotOrchestrator.ts`, `slotOrchestrator.test.ts`, `slotSessionStore.ts`, `browserView.d.ts` |
| UI | `ManageGradesSidePanel.tsx`, `MakeupExamExamConfigPanel.tsx` |
| Local only | `config/d2l-courses.json` (ignore for commit) |

**Verified headlessly this session:**

- Renderer: `slotOrchestrator.test.ts`, `embeddedBrowserOrchestratorAdapter.test.ts`, `slotSessionStore.test.ts` — pass.
- Electron: `browser-slot-isolation-lock.test.js` (3), `browser-slot-isolation-restore.test.js` (5), `makeup-exam-isolation.test.js` (1) — pass.
- No linter errors on touched renderer files.

**Not verified live:** gradebook import; back-to-back bulk scans; TC preview recreate after bulk scan while on Preview tab.

## 6. Open questions / constraints

**Phase 4 needs Chase OK before:**

1. Delete orphans: `ConsoleDashboardScreen`, `ConsoleAppLiveScreen`, `DashboardPortalPreviewCard`, related dashboard hooks, `PracticeArchivePanel`.
2. Prop drilling: plan recommends **(b) grouped pass-through** (`rosterData`, `results`, `preview`) — not React context unless Chase explicitly wants the first context in the app.

**Phase 2 tail (optional before or during Phase 4):**

- Mechanical route of remaining `browser.activateSlot` / `activateSlotForTab` shell call sites through orchestrator (grep still finds many in shell hooks — they go through queued `useEmbeddedBrowser` API, which may be sufficient).
- Full contract test: renderer orchestrator → IPC → main `activateSlot` / `navigate` for `{ ok: false }` and timeout (adapter unit tests exist; no electron integration test yet).

**File size flags:**

- `useMacroAppShell.ts` ~720 (was 800 cap — improved but not yet 650 target).
- `useMacroAppStudentProgressShell.ts` grew with preview refresh (~490+).
- `teacher-console-workspaces.css` ~829 — Phase 4 split flagged.

**Reconcile:** `AGENTS.md` still routes "Teacher Console live preview" to `ConsoleAppLiveScreen.tsx` — orphan slated for deletion in Phase 4.

## 7. Exact next step

Start **Phase 4** in `MACRO_APP_RESTRUCTURE_RECOMMENDATIONS.md`:

1. Ask Chase once: **OK to delete the orphaned TC dashboard/app-live screens** and use **grouped pass-through (b)** for prop drilling?
2. If yes: create **one preview identity owner** hook (course → section id → persona → preview URL, single in-flight cancel on course switch). Wire preview refresh/navigation through Phase 2 lane only — no new TC-local retry.
3. If deletions approved: remove orphans, update `AGENTS.md` rows + first-paint recipe exemplar that point at dead code.

Do **not** start Phase 4 deletions without explicit OK. If declined, implement only the preview identity owner and grouped props.
