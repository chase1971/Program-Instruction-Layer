# Momentum handoff — AA class switch hangs on MATH-2412 (plus cleanup items 1–2 done)

**Written:** 2026-09-25
**App:** `School Scrips/Macro App` (Assignment Assistant tab + vendored `assignment-assistant-engine/`)

## 1. Objective and current phase

Chase is cleaning up the Assignment Assistant (AA). The remaining work is listed in
`docs/plans/AA_ENGINE_CLEANUP_REMAINING_PLAN.md`.

- **Items 1–2 are done this session and uncommitted.** Details are in §5.
- **New live bug (the current focus):** Chase switched AA to **MATH-2412 4101 MW 8-10:20**
  (`COURSE_1692794`, ou=1692794). The class picker spins and the class "never actually loads."
- **Key fact from Chase:** the same course loads fine in Macro App's **Browser tab**. So D2L is not
  down for that course; the problem is in AA's path.

## 2. Chase's desired feel

- Structural cleanup. The 800-line rule matters to him. Delete dead code; no behavior changes
  while cleaning.
- He uses a dwell mouse:
  - Never launch the GUI or open windows without asking.
  - Verify headlessly, then hand him a flat statement of what to test, not a question.
- He reports through speech-to-text, briefly ("it just spins… never actually loads"). Evidence has
  to come from logs and the running app, not from asking him to describe more.

## 3. Accepted decisions (this session)

- **Item 1:** `scripts/class_manager_cli.py` is now `list`-only. `add`, `edit`, `delete` and
  `deleteAll` had no caller.
- **Item 2:** two files were split verbatim by line range. An AST check confirmed all 30 functions
  are identical, with none missing.
  - `python-modules/import_file_handler.py` (752 → 375):
    - New `import_file_grades.py` holds grade-column setup, `update_import_file`,
      `build_grade_preview_rows`, `_is_eol_row`, `_save_import_file` and `_close_excel_for_file`.
    - `import_file_handler` re-exports those names.
    - `load_import_file` and `apply_grade_edits` stayed in `import_file_handler`, because a test
      monkeypatches `import_file_handler.log`.
    - The dead `_find_import_file` alias was deleted.
  - `scripts/extract_grades_cli.py` (774 → 355): the five helpers moved to
    `python-modules/extract_grades_steps.py`. `main()` stays in the script.
  - New guard test: `python-modules/tests/test_import_file_split.py` (5 tests).
- The docs were updated:
  - engine `README.md` § Over-cap
  - the cleanup plan (items 2–3 marked done)
  - `ASSIGNMENT_ASSISTANT_ENGINE_VENDORING.md`
  - `ROSTER_PIPELINE_INTEGRATION.md`: fixed the nonexistent `load_working_gradebook` → `load_import_file`
  - Macro App `AGENTS.md` row

## 4. Rejected / do-not-rediscover

- **The class switch does not touch the Python changed today.** The switch path is:
  - `commitMacroCourseSelection` in `renderer/src/hooks/assignment-assistant/useAssignmentAssistantWorkflow.ts:294`
  - → `navigateMacroCourseBrowser`, which calls `browser.navigateAssignmentAssistant(folders_manage URL)`
  - → `syncPlatformClassForCourse`, which calls IPC `assignment-assistant:sync-courses`.
    That is pure JS in `electron-app/assignment-assistant-sync-courses.js` and writes `classes.json`.
  - Don't revert items 1–2 to chase this bug.
- **The engine server is fine.** `/api/test` returned 200 on 5430 and through the Vite proxy
  `localhost:5328/api/test`, both from the shell and from inside the page.
- **Read-only live inspection works through CDP port 9224.** The script is
  `%TEMP%\aa-split\cdp.mjs <expr>`: it runs `Runtime.evaluate` with `awaitPromise` on the
  `localhost:5328` page.
  - It touches no windows. Keep it read-only.
  - 9224 was **not listening** after Chase's 01:25Z restart. The log says "CDP endpoint 9224 not
    reachable — a leftover Macro App process is likely holding it." A full quit and relaunch fixes it.
- Before this session, "D2L is down for that course" was a plausible explanation. **Chase ruled it
  out**: the Browser tab loads MATH-2412.

## 5. Current implementation state

- **Uncommitted in Macro App:**
  - Modified: `AGENTS.md`, engine `README.md`, `import_file_handler.py`, `class_manager_cli.py`,
    `extract_grades_cli.py`, two docs, and the cleanup plan.
  - New: `extract_grades_steps.py`, `import_file_grades.py`, `test_import_file_split.py`.
  - `docs/plans/TEACHER_CONSOLE_PREVIEW_SMOOTHNESS_PLAN.md` (untracked) and machine-local
    `config/d2l-courses.json` are **not from this work**.
  - Chase did not ask to commit.
- **Verified:**
  - `npm run ci:local` passed: 1,463 renderer tests, plus engine pytest (39) and the helper tests.
  - Both CLIs were smoke-run with the bundled `python/python.exe`.
- **Evidence for the MATH-2412 hang** (`%APPDATA%\macro-app\logs\macro-app.log`):
  - `01:22:09Z`: navigate `d2l-assignment-assistant` → `folders_manage.d2l?ou=1692794`.
  - `01:22:39Z`: "ok" but url=`https://d2l.lonestar.edu/d2l/error/500`. The page title was
    "Internal Error - LSCS". It took 30 s.
  - Other D2L slots were fine at the same time, so the session was live.
  - `ou=1692723` (MATH-1324) had loaded fine in the AA slot earlier.
  - After the restart, `01:25:18Z`: AA bootstraps straight to the same ou=1692794 URL. No
    completion line was logged after it.
- **Also seen live, cause unknown:** after the picker finished, the AA
  `.aa-bootstrap-overlay` stayed up saying "Connecting to the Assignment Assistant grading server…".
  - That message means the engine `serverStatus === 'checking'`. The only place that sets it is the
    initial `useState` in `assignment-assistant-engine/src/components/hooks/useOption2State.ts:393`.
  - The page's `/api/test` fetch succeeded at the same moment, and `document.hidden` was true.
  - Suspect the phase-1 keep-alive (`AssignmentAssistantWorkspaceSlot.tsx`) or a remount leaving the
    poller in a fresh instance that never reports online. **Unverified.**

## 6. Open questions / constraints

- **Why does the AA slot get D2L's 500 on a direct `folders_manage.d2l?ou=1692794` load when the
  Browser tab loads the course fine?** Candidates, all unverified:
  - The Browser tab enters through course home, so D2L has the org-unit context. A cold deep link
    to Manage Assignments for that ou errors.
  - The AA slot partition or cookies differ from the Browser tab's.
  - That course's dropbox admin page specifically errors on direct load.
- Compare the Browser tab's actual URL for MATH-2412 Assignments with AA's target URL. The URL is
  built by `evaluateAssignmentsFolderNavigation`; grep it.
- Check what happens after navigation lands on `/d2l/error/500`. AA should surface an error, not an
  endless spinner or overlay.
- Don't open windows or launch the app without asking. Chase re-tests live.

## 7. Exact next step

Find `evaluateAssignmentsFolderNavigation` and `navigateAssignmentAssistant` (renderer plus
`electron-app` BrowserSlot navigate). Confirm the exact URL and partition AA uses for ou=1692794.
Once 9224 is back, use the read-only CDP script to read the Browser tab's URL when Chase is on
MATH-2412 Assignments, then compare the two.
