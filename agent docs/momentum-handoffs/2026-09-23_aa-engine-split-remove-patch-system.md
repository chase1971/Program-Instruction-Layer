# Momentum handoff — AA engine split done → remove the old patch system

**Written:** 2026-09-23
**App:** `School Scrips/Macro App` (Assignment Assistant tab + vendored `assignment-assistant-engine/`)

## 1. Objective and current phase

Chase is cleaning up the Assignment Assistant (AA). He calls it "the most inconsistent and janky"
tab, and it sits on a vendored engine that is about two years old.

- **Phase 1** (de-jank): done, uncommitted, not live-tested.
- **Phase 2** (split the over-cap engine files): **done this session**, uncommitted.
- **Next:** Chase said *"the patch system is old and should be removed."* He wants the next agent
  to do it. This is **approved**. The earlier handoff rule "don't delete the patch plumbing
  without asking" is now resolved: he asked for removal.

## 2. Chase's desired feel

- Structural cleanup. The 800-line size rule matters to him.
- Delete dead code; don't keep legacy plumbing around "just in case."
- No behavior changes to live features while cleaning.
- Chase uses a dwell mouse, so never launch the GUI or open windows without asking.
  Verify headlessly, then hand him a flat statement of what to test.

## 3. Accepted decisions (phase 2, this session)

All splits were cut **verbatim** by line-range scripts, and dead code was deleted only after a
grep found zero callers.

- **`src/services/quizGraderService.ts`** (1,149 lines): now a 9-line `export *` barrel over
  `src/services/quizGrader/`, which holds `types`, `apiClient`, `serverConfigApi`,
  `quizProcessingApi`, `folderApi` and `classApi`.
  - Deleted 37 dead exports, including **all 6 frontend patch functions** (`getPatchStatus`,
    `selectAndImportPatch`, `importPatchFromDiskPath`, `importPatchZipUpload`, `clearPatches`,
    `rollbackPatches`) and the app-update/runtime-config functions.
  - Also removed `isExtractGradesEnabled` from both renderer shims.
- **`src/components/hooks/useOption2Actions.ts`** (1,682 → 81 lines): an orchestrator that spreads
  feature factories from `hooks/option2Actions/`: `context`, `gradeResultHelpers`,
  `processingActions`, `pdfActions`, `gradeSessionActions`, `classFolderActions`,
  `emailStatisticsActions`.
  - Deleted 9 dead handlers and removed 2 of them from the shims.
  - **Kept** the browser-mode `<input type=file>` branches and `handleSplitPdfUpload`. They are
    reachable when `electronAPI.showOpenDialog` is absent.
- **`python-modules/grading_processor.py`** (1,027 → 477 lines) keeps the three `run_*`
  orchestrators and re-exports `find_zip_file` / `format_error_message` for the CLIs.
  - New `zip_intake.py` (257): ZIP find, validate and extract.
  - New `grading_steps.py` (237): `ProcessingResult`, `_find_class_folder`, setup helpers.
  - Deleted `find_latest_zip` and `create_combined_pdf_only`.
  - New test: `python-modules/tests/test_grading_processor_split.py`.
- **`server/routes/quiz.js`** (963 → 17 lines): mounts `quiz-processing.js`, `quiz-split-pdf.js`
  and `quiz-folders.js` via `router.use`.
  - Deleted the dead endpoints `/list-classes`, `/list-processing-folders`, `/clear-archived-data`,
    and the `/api/quiz` copy of `/reset-windows-email-handler`.
  - `routes/system.js` still serves `/api/system/reset-windows-email-handler`. That endpoint is
    also dead (no frontend caller) and was left alone.
- Updated the engine README § Over-cap and `docs/ASSIGNMENT_ASSISTANT_ENGINE_VENDORING.md`:
  no engine file is over the cap any more.

## 4. Rejected / do-not-rediscover

- **Engine TS is not type-checked by the renderer `tsc`.** The alias points at `ci-shims`.
  - To check the engine, create a temporary `renderer/tsconfig.engine-check.tmp.json` that extends
    `tsconfig.json`, re-points `@d2l-assignment-platform/*` at `../assignment-assistant-engine/src/*`,
    includes that src, and excludes `src/ci-shims/d2l-assignment-platform/**`. Delete it afterward.
  - Current count is **97 errors**. All are pre-existing: missing react types resolved from the
    engine dir, `Option2State` lacking 3 setters, and exactOptionalPropertyTypes. The split added
    only duplicates of those.
- **`ci:local` builds the renderer against the CI shims, so it never bundles the real engine.**
  - For a real-engine build, run `cd renderer; npx vite build --outDir <scratchpad>` without
    `MACRO_CI_STANDALONE`.
- **The engine's pytest is not in CI** and needs a module path:
  `cd assignment-assistant-engine/python-modules; PYTHONPATH=. py -3 -m pytest tests -s --junitxml=<file>`.
  - Use `-s` plus junitxml, because a module swallows stdout so console output is empty.
  - The embedded `python/python.exe` has no pytest. Use `py -3`, which has pandas and pytest.
  - Current result: **34 tests pass**.
- **ESLint undefined/unused check for engine JS:**
  `npx eslint --no-config-lookup --rule '{"no-undef":"error","no-unused-vars":["error",{"args":"none","caughtErrors":"none"}]}' --global require,module,process,console,__dirname,Buffer <files>`.
  - Files must be inside the repo, or ESLint silently ignores them.
- **Headless server smoke test (no window):** spawn `node server.js` with `PORT=5987`, POST to
  `/api/...`, then kill it. The engine's own default port is 5000; Electron forks it on 5430.

## 5. Current implementation state

- **Everything is uncommitted.** Phase 1 and phase 2 files are all modified or untracked in
  Macro App. Several Teacher Console files and `usePortalPreviewSectionId.ts` in the tree are
  **not from this work**; leave them alone. Chase did not ask to commit.
- **Verified:**
  - `npm run ci:local` passed after every split (last run: 1,462 tests).
  - The real-engine vite build passed.
  - AST equality check (Python) and route/handler-hash equality check (JS) both passed.
  - The headless server smoke test passed.
- **Not live-tested by Chase.** He still has two checks to do:
  - The phase 1 checklist: tab switch keeps state, no browser jump, Statistics +/- works, no
    backdrop dismiss, no flash on restore, bigger icons.
  - One Process Quiz, one Process Completion and one Split PDF, which should all behave as before.

## 6. Open items / constraints for patch removal

**Known pieces of the patch system** (from earlier reads; **re-grep, since this list is not
exhaustive**):
- `assignment-assistant-engine/patch-manager.js` (756 lines).
- `assignment-assistant-engine/server/python-runner.js` around line 270: it picks the working
  directory and PYTHONPATH as the patch dir when patches exist. This is the dangerous part: a stale
  patch on one machine silently overrides the vendored scripts.
  - Remove it so Python always runs the vendored `scripts/` and `python-modules/`.
- `assignment-assistant-engine/server/app.js`: `uploadPatch` multer, about lines 41–42, used for
  `/api/patches/import`.
- The patch routes, probably `server/routes/patches.js` or inside `system.js`. `grep` for
  `patches`.
- `runtime-config.js` and app-update endpoints may be tied to patches. Their frontend callers
  were already deleted this session. Check before removing and ask if unrelated.
- The frontend patch functions are **already deleted** from `quizGraderService`. Check
  `renderer/src` and the shims for leftover patch types and UI, and `electron-app/` for patch IPC.
- Look for an on-disk `patches/` folder location (probably under the engine or userData). The
  code can go; **do not delete Chase's user data folders** without asking.

**Rules:**
- Grep first; delete only what's patch-only. If a file mixes patch code with live code, remove
  just the patch parts.
- Keep `renderer/src/ci-shims/d2l-assignment-platform/` in sync with anything the renderer imports.
- Update docs that mention patches: engine README, `ASSIGNMENT_ASSISTANT_ENGINE_VENDORING.md`,
  `docs/EMBEDDED_BROWSER_AND_MODALS.md` if relevant, and the Macro App `AGENTS.md` rows if any.
- Verify with the headless server smoke test, engine pytest, the engine tsc temp tsconfig
  (stay at 97 or fewer), and `npm run ci:local`.

## 7. Exact next step

From `School Scrips/Macro App`, grep for everything patch-related (`patch-manager`, `patches`,
`uploadPatch`, `getPatchDir`, `hasPatch`, `/api/patches`). Exclude `node_modules`, `python/` and
`dist-installer`. List what is patch-only versus mixed, then remove the patch system, starting
with the `python-runner.js` override.
