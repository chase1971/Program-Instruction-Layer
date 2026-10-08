# Momentum handoff — Assignment grade-crop loading hang

Written: 2026-10-07 16:40 America/Chicago
Workspace: C:\Users\chase\Documents\Programs\School Scripts\Macro-App
Phase: A third transport implementation has been completed and verified headlessly, but Chase
has not yet live-tested it. Nothing committed or pushed.

## Read first

1. Root `AGENTS.md` and this app's `AGENTS.md`.
2. `docs/EMBEDDED_BROWSER_AND_MODALS.md` — Chase also observed Settings failing to freeze the
   browser while the crop hang was active.
3. `docs/LOGGING.md`.
4. Relevant code:
   - `assignment-assistant-engine/server/helpers/grade-crop-file.js`
   - `electron-app/assignment-assistant-ipc.js`
   - `electron-app/preload.js`
   - `assignment-assistant-engine/src/services/quizGrader/quizProcessingApi.ts`
   - `renderer/src/modules/d2l-assignment-assistant/modals/AssignmentGradeCropOverlay.tsx`
   - `renderer/src/modules/d2l-assignment-assistant/modals/AssignmentGradesReviewModal.tsx`

## Objective and Chase's desired feel

In Assignment Assistant's extracted-grade results, clicking a student's name must display that
student's saved crop immediately and repeatedly. Chase may inspect many students in sequence.
The first crop must not work while later crops slow down, hang the app, delay Settings, interfere
with browser freeze, or make Close ineffective. Progress/failure must not be silent. Large,
dwell-friendly controls and no backdrop dismissal remain mandatory.

## Accepted decisions

- Grade extraction crop is centered and small:
  `top=0`, `bottom=0.0682`, `left=0.3855`, `right=0.6145`; 292×112 px for Letter at 150 DPI.
- Red-text isolation is temporarily disabled with `USE_RED_TEXT_ISOLATION = False`.
- In extraction review mode, clicking a student name opens the crop overlay. Other review modes
  retain the existing feedback-comment behavior.
- Crop reads now bypass Chromium HTTP entirely in Macro App. The Electron Assignment Assistant
  IPC bridge validates and reads the local file, returning a data URL.

## Evidence and diagnosis

- Deanna Allen's and Timothy Baines's PNG files both exist and are valid.
- The old Express endpoint was tested directly with Deanna, Timothy, William, and Avery; all
  reads completed in milliseconds.
- During Chase's most recent live test, persisted logs showed:
  - request 1: server 12 ms
  - request 2: server 34 ms
  - request 3: server 20 ms
  - request 4: server 23 ms
- Despite that, Chromium issued/displayed later requests progressively later; the fourth took
  more than 30 seconds from Chase's click. Settings also became delayed/unusable and failed to
  freeze the browser. Therefore Google Drive and the crop endpoint were not the bottleneck.
- The latest implementation removes browser networking from the Macro App crop path.

## Rejected directions — do not rediscover

1. Missing crop files were not the explanation for the reported students.
2. Restarting only the stale Express server fixed an earlier 404 but not sequential loading.
3. Prioritizing Electron's direct port 5430 over Vite's proxy did not fix the cumulative hang.
4. Replacing fetch/Blob URLs with direct `<img src>` plus buffered HTTP responses and
   `Connection: close` improved behavior but produced progressively longer delays.
5. A timeout alone is not a fix; Chase explicitly rejected masking the underlying hang.

## Current implementation state

Uncommitted work includes the requested feature plus unrelated pre-existing changes. Do not
discard or rewrite unrelated dirty files.

Crop pipeline:
- `grade_parser.py`: smaller centered crop and red filtering disabled.
- `extract_grades_simple.py`: respects disabled red filtering.
- `AssignmentGradesReviewModal.tsx` / `AssignmentGradesReviewRow.tsx`: extraction-name clicks
  open crop overlay.
- `AssignmentGradeCropOverlay.tsx`: asynchronously requests a data URL; no Blob URL creation,
  revoke lifecycle, or browser image HTTP request in Macro App.
- New `server/helpers/grade-crop-file.js`: single validated path resolver/reader shared by
  Express fallback and Electron IPC.
- `assignment-assistant-ipc.js`: `assignment-assistant:read-grade-crop` handler with safe
  start/completion timing logs and no student names.
- `preload.js` + `macroAppAssignmentAssistant.d.ts`: expose/type `readGradeCrop`.
- `quizProcessingApi.ts`: uses the IPC bridge in Macro App; keeps an HTTP URL only as a
  standalone-engine fallback.
- Express route still works through the shared reader and remains useful outside Macro App.

Unrelated dirty files include config JSON, makeup-exam history, and browser-slot isolation files.
Do not include them in a crop-specific cleanup.

## Verification completed

- Four sequential real file reads through the shared IPC-owned helper:
  - Deanna 26 ms
  - Timothy 16 ms
  - William 14 ms
  - Avery 9 ms
- `npm run build:renderer` passed.
- `npm run typecheck:aa-engine` passed.
- `npm run typecheck:electron` passed.
- `npm run lint:electron` passed.
- Targeted renderer lint passed.
- `git diff --check` passed (only unrelated line-ending warnings).
- No GUI was launched by the agent.

## Open questions and constraints

- The IPC implementation needs a real repeated-click test after a full app restart because
  preload and IPC changes do not hot-reload.
- If it still slows, compare `[GradeCrop] IPC request N started/completed` timestamps. If the
  IPC start itself is delayed after the click, the remaining issue is renderer/main-thread
  scheduling or modal lifecycle, not file I/O.
- The earlier non-instant Close behavior is a separate defect: `main.js` intercepts close,
  waits for gradebook flush, then calls unbounded sequential auth snapshot saves. Do not claim
  this has been fixed.
- Never launch Macro App or any visible browser/window without Chase's permission for that run.
- Momentum handoff is not permission to commit, push, or run end-of-session protocol.

## Exact next step

Review the IPC crop bridge and current diff first. Then wait for or collect Chase's live
repeated-click result after a full restart. If it still hangs, inspect persisted
`[GradeCrop] IPC request` timing immediately and trace the renderer/modal lifecycle; do not
return to HTTP transport or add a timeout as the primary fix.
