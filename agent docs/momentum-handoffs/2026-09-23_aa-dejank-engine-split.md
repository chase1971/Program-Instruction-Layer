# Momentum handoff — Assignment Assistant de-jank → engine file split

**Written:** 2026-09-23
**App:** `School Scrips/Macro App` (Assignment Assistant tab + vendored `assignment-assistant-engine/`)

## 1. Objective and current phase

Chase: Assignment Assistant (AA) is "the most inconsistent and janky" of the Macro App's
embedded-browser tabs, because it sits on a roughly two-year-old vendored engine. Goal: improve it structurally.

- **Phase 1 (done, uncommitted, not live-tested):** fixed the jank Chase can see.
- **Phase 2 (next, approved in spirit, not yet planned):** split the over-cap files in the
  vendored engine. Chase asked about the ">1,000 line files" right after phase 1, so this is next.

## 2. Chase's desired feel

- "Fix what you feel": user-visible jank first, i.e. flashes, stuck browser, buttons that do nothing,
  layout jumps.
- Dwell-mouse accessibility: big targets, no backdrop-dismiss, no hover-only info.
- The size rule matters to him. He noticed the 1,000+ line engine files weren't touched.

## 3. Accepted decisions (phase 1)

- **Keep-alive instead of remount:** `AssignmentAssistantWorkspaceSlot.tsx` is mounted from
  `TabbedAppShell` on the first visit. It follows the MyCalendar/Calendar keeper pattern.
  - While hidden, the view renders no `EmbeddedBrowserPanel`, because that panel owns the shared
    holder ref. It also renders no sidebar portal and no overlays.
- **Startup logic extracted** to `renderer/src/hooks/assignment-assistant/useAssignmentAssistantBootstrap.ts`.
  - This took `useAssignmentAssistantWorkflow.ts` from 831 to 631 lines.
  - It runs once per app session. Its refs are **not** reset when the tab is deactivated.
- **Freeze after the data loads, not on click:** the engine's email, statistics and workspace picker
  handlers call `prepareHostBrowserOverlay` right before `flushSync(setShow…)`.
  - The host wrappers in `buildAssignmentAssistantActions.ts` now pass straight through.
  - Statistics +/- and notes edits use `refreshStatistics` and no longer re-open the modal.
- **Log dedupe:** `addLog` only drops a line that echoes the same line within 3 s
  (`LOG_ECHO_WINDOW_MS`). HTTP replay dedupes against the live log via
  `registerActivityLogReader` (in `quizGraderService.ts`).
- **Engine server-status poller** (`useOption2State.ts`):
  - A visibility change no longer sets `'checking'`.
  - It never reports `'offline'` before the server has been online once.
  - `computeIsTabBootstrapping` now ignores `'checking'` when there is a `serverStartError`.
- **No backdrop dismiss:** removed from `ModalShell.tsx` (the prop is kept but ignored) and from
  `StudentDetailModal.tsx`.
  - Deliberately did **not** add `courses-modal-overlay` to StudentDetail. That class sets
    `pointer-events: none`, so clicks would fall through to the Statistics panel underneath.
- **Sidebar:**
  - The portal target is resolved in `useLayoutEffect`.
  - The MutationObserver now watches the slot's parent, not the whole body.
  - Only the functional rules in `compact-sidebar.css` were re-scoped to
    `.macro-embed-side-panel-slot`: header toggle, split-PDF source, download progress.
  - The `.da-btn` shrink and tiny-font rules were deliberately **not** re-scoped, so targets
    don't shrink.
  - Icon buttons went from 28 to 36 px.
- **"Linking class…"** moved from the banner above the browser into the class picker's loading label.
- **Grade review modal:** `useLayoutEffect` seeds rows from the session when it opens and clears them on close.
  Blank-line padding was collapsed to stay net-neutral; the file is now 715 lines.
- **`electron-app/d2l-assignment-host.js`:** the pandas probes are now async (`execFile`) instead of
  `spawnSync` on the main process. Concurrent starts share a `startPromise` guard.

## 4. Rejected / do-not-rediscover

- **Engine code is not type-checked by the renderer's `tsc`.** The alias points at `ci-shims`.
  - To check the engine, use a temporary tsconfig that re-points `@d2l-assignment-platform/*` at
    `../assignment-assistant-engine/src/*`, and compare error counts before and after.
  - Baseline is about 97 pre-existing errors.
- **Engine tests would break CI**, because CI uses the shims. Keep new tests on renderer-side pure
  functions (the precedent is `assignmentAssistantWorkflowMachine.test.ts`).
- **`reactEffectLoopRisk.test.ts`** flags callback props used as effect deps. Use a ref instead.

## 5. Current implementation state

- **Uncommitted.** Macro App working tree has about 20 modified files and 2 new ones (see `git status`).
  Chase did not ask to commit.
- **Verified:**
  - Renderer `tsc` is clean.
  - The full vitest suite passes: 1,460 tests, including a new `computeIsTabBootstrapping` case.
  - `npm run ci:local` passed: electron lint, checkJs, pytest.
- **Not live-tested.** Chase has the handoff checklist:
  1. Switch tabs and come back: no "Starting…" screen, and the log and class are kept.
  2. Switching class doesn't make the browser jump.
  3. Statistics +/- works without the window reopening.
  4. Clicking outside the student detail doesn't close it.
  5. Minimize and restore: no flash.
  6. The icons are bigger.
- `docs/EMBEDDED_BROWSER_AND_MODALS.md` got two new AA subsections, and the modal table was
  updated to show where each open handler lives.

## 6. Open items / constraints (phase 2)

**Over-cap files.** All engine files are vendored and exempt via `VENDORED_PREFIXES` in
`scripts/check-file-size.js`.

| File | Lines |
|---|---|
| `src/components/hooks/useOption2Actions.ts` | 1,682 |
| `src/services/quizGraderService.ts` | 1,149 |
| `python-modules/grading_processor.py` | 1,027 |
| `server/routes/quiz.js` | 963 |
| `scripts/extract_grades_cli.py` | 774 |
| `patch-manager.js` | 756 |
| `renderer/.../assignment-assistant-host/grade-review.css` | 842 |
| `renderer/.../assignment-assistant-host/process-wizard.css` | 721 |

**Dead code found by audit.** These are the "unused" findings only. Verify with grep before deleting.

- **`quizGraderService.ts`:** about 27 exports with no callers, about 450 lines around lines 634–1141:
  - `listClasses`, `listProcessingFolders`, `clearArchivedData`, `killProcesses`
  - `openStudentPdf`, `openCombinedPdf`, `openImportFile`, `isExtractGradesEnabled`
  - the Windows-email helpers
  - class add/edit/delete, `selectFolder`
  - the window/version/runtime-config/app-update functions
  - all 6 patch functions
- **`useOption2Actions.ts`:**
  - the legacy clear flow: `handleAssignmentSelection`, `executeClearForAssignments`,
    `handleToggleAssignment`, `handleSelectAll`, `handleDeselectAll`, `handleAssignmentModalClose`
    (around lines 1348–1487)
  - `handleZipModalSelect`, `handleOpenClassRosterFolder`, `handleSaveGradesReview`
  - the browser-mode `<input type=file>` branches
- **Stale shim declarations:** `renderer/src/types/d2l-assignment-platform-shim.d.ts:200-240`.

**Risk / rule notes:**
- The `patches/` PYTHONPATH override in `server/python-runner.js` means a stale patch on one machine
  silently overrides the vendored scripts. Don't delete the patch plumbing without asking.
- Rule: the engine README calls the over-cap files "no-edit-until-split". Split verbatim, with no
  behavior change, then delete the dead code.
- Keep `renderer/src/ci-shims/d2l-assignment-platform/` exports in sync for anything the renderer imports.
- `grading_processor.py` and `quiz.js` do the real grading. Split them carefully and have pytest cover them.

## 7. Exact next step

Plan (plan mode) the phase-2 split, starting with `quizGraderService.ts`:
1. Grep each of its exports for callers across `assignment-assistant-engine/src` and `renderer/src`.
2. Delete the dead exports.
3. Split what's left by domain (quiz/process, grades, files/folders, config/server) behind a barrel,
   so imports don't change.

Then do `useOption2Actions.ts` the same way (by feature, with dead handlers removed). Verify with the
temporary engine tsconfig error-count comparison plus `npm run ci:local`.
