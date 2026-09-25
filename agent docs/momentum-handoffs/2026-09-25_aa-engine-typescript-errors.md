# Momentum handoff — AA engine TypeScript errors (cleanup item 4); class-switch bug fixed

**Written:** 2026-09-25
**App:** `School Scrips/Macro App` (Assignment Assistant tab + vendored `assignment-assistant-engine/`)

## 1. Objective and current phase

Chase is finishing the Assignment Assistant (AA) cleanup. The work list is
`docs/plans/AA_ENGINE_CLEANUP_REMAINING_PLAN.md`.

- **Done this session (uncommitted):**
  - cleanup items 1–2
  - the MATH-2412 class-switch hang fix
- **Chase confirmed live:** "it switches to classes just fine."
- **Recommended next (proposal, not yet approved by Chase):** plan item 4. Get the engine's 97
  TypeScript errors to 0, then gate them in CI.

## 2. Chase's desired feel

- He wants structural cleanup: delete dead code, respect the 800-line cap (extract before 700),
  and don't change behavior while cleaning.
- He uses a dwell mouse:
  - Never launch the GUI or open windows without asking.
  - Verify headlessly, then give him a **flat statement** of what to test, never a question.
- He reports briefly via speech-to-text. Get evidence from logs and the running app (read-only CDP
  on port 9224, script `%TEMP%\aa-split\cdp.mjs <expr>`), not by asking him for more detail.

## 3. Accepted decisions (this session)

- **Class-switch fix** (renderer only):
  - `assignmentAssistantWorkflowMachine.ts` gained three helpers:
    - `d2lErrorPageCode`: detects `/d2l/error/<code>` pages.
    - `resolveCourseFolderErrorPageMessage` and `resolveCourseFolderNavigationFailureMessage`.
    - `waitForPaintOrTimeout`: two rAFs with a 250 ms fallback.
  - `useAssignmentAssistantWorkflow.navigateMacroCourseBrowser`:
    - reads the slot URL after navigating
    - on a D2L error page or a thrown/timed-out load, sets `serverStartError` ("Pick the class
      again to retry")
    - on the next good load, clears only that nav error (`navErrorRef`)
  - `useAssignmentAssistantBootstrap`:
    - the initial course nav uses `waitForPaintOrTimeout` instead of bare double-rAF
    - when its own `/api/test` loop confirms online, it calls a new `markServerOnline` option.
      That calls engine `state.setServerStatus('online')`, so "Connecting to the grading server…"
      can't stick.
  - Shim updates for `setServerStatus`:
    - added to `AssignmentAssistantOption2State` in `types/d2l-assignment-platform-shim.d.ts`
    - added to `ci-shims/.../useOption2State.ts`
  - Documented in `docs/EMBEDDED_BROWSER_AND_MODALS.md` § "Class switch lands on a D2L error page /
    spins (2026-09-25)".
- **Items 1–2** (from the previous handoff, still valid):
  - `class_manager_cli.py` is now `list`-only.
  - `import_file_handler.py` was split out into `import_file_grades.py`.
  - `extract_grades_cli.py` was split out into `extract_grades_steps.py`.
  - New guard test: `test_import_file_split.py`.

## 4. Rejected / do-not-rediscover

- **AA's URL and partition are not the cause.** AA and the Browser tab both use partition
  `persist:d2l-macro` and the same `folders_manage.d2l?ou=…` deep link. The Browser tab opens that
  link directly too.
- **The MATH-2412 500 was transient D2L.** The same URL loaded fine in AA on three later launches.
- **The Macro App window reports `document.hidden = true`** whenever another window covers it
  (Windows occlusion), even when it is maximized and not minimized. rAF does not fire then.
  Never gate startup work on bare rAF.

## 5. Current implementation state

- **Nothing committed.** Chase has not asked to commit.
- The Macro App working tree also holds **many uncommitted changes from other sessions**: settings
  redesign, diagnostics, and `electron-app/browser-slot-*`. Leave them alone.
  - One of them matters here: `electron-app/browser-slot-navigation.js` bounds `safeLoadUrl` with
    `SLOT_NAVIGATE_LOAD_TIMEOUT_MS` (45 s). The class-switch fix relies on it.
- **Verified:**
  - Full renderer vitest: 1,473 passed.
  - `tsc -p tsconfig.app.json`: clean for touched files.
  - The only remaining app tsc error is in `utils/studentProgress/studentPortalPreviewFramePrefs.ts`,
    another session's edit.
- **Chase's live test:** class switching works.

## 6. Open questions / constraints

- **Plan item 1 (confirm the GitHub CI engine steps) is unchecked.** `gh` is not authenticated on
  this machine. The next push reruns CI anyway.
- **Item 4 method** (from the plan):
  - Create a temporary `renderer/tsconfig.engine-check.tmp.json` that:
    - extends `tsconfig.json`
    - copies all of its `paths`
    - re-points `@d2l-assignment-platform/*` → `../assignment-assistant-engine/src/*`
    - includes `../assignment-assistant-engine/src`
    - excludes `src/ci-shims/d2l-assignment-platform/**`
  - Count only errors under the engine `src`. Baseline: 97.
  - Fix the `Option2State` setter mismatch first. `setServerStatus` was added to the shim today,
    so re-count.
  - At 0, add an engine typecheck step to `scripts/ci-local.cjs` and `.github/workflows/ci.yml`.
- **Watch file sizes:**
  - `useAssignmentAssistantWorkflow.ts` is 651 lines.
  - Engine `useOption2State.ts` is ~659.
  - Extract before 700.
- **Still not live-tested:**
  - The phase 1 checklist: tab switch keeps state, no browser jump, Statistics +/-, no backdrop
    dismiss, no restore flash, bigger icons.
  - One Process Quiz / Process Completion / Split PDF run.
  - Chase does these himself. Hand him a flat statement.

## 7. Exact next step

Build the temporary engine tsconfig described in §6 and get the current engine-only error count.
Then fix the `Option2State` / shim setter mismatch first.
