# Momentum handoff — Macro App slim build prep: splash fix, Makeup Exam class + calculator

**Written:** 2026-09-13 (Sunday, evening)

---

## 1. Objective and current phase

Chase is getting the **Macro App slim hand-off build** ready to install on a laptop (a separate
machine, installed build, not dev). The flow he set: **fix code first → more changes → then he
asks for an installer build**. Three code fixes are done and verified headless/live; nothing is
built or committed since. He is about to name more changes.

## 2. Chase's desired feel

- **Don't build unless asked.** I started an installer build after the splash fix; he said
  "I did not say to build the installer." Each build / copy-to-USB needs its own explicit request.
  (Memory: `feedback_no_unrequested_builds.md`.)
- He wants code changed and explained plainly; he verifies in the app himself.
- Speech-to-text: "feature console" = **Teacher Console**; "slim bill" = slim build.
- "Take over the browser" = inspect Macro App's embedded browser read-only via CDP
  (it's already on the right page — don't navigate).

## 3. Accepted decisions

- **Teacher Console stripped from slim build** (committed earlier in session by an end sync):
  `@teacher-console` Vite alias → `renderer/src/ci-shims/teacher-console/teacherConsoleEntry.ts`
  when `student-progress: false`; `main.js` gates student-progress requires/IPC on
  `isTabEnabled('student-progress')`; `electron-builder.config.cjs` excludes student-progress
  files. Documented in `docs/SLIM_DISTRIBUTION_BUILD.md`. **Anything the shell imports from
  Teacher Console must be added to both the entry and the shim** (another session already added
  CSS imports to the entry — fine).
- **Slim installer 0.1.27** is on USB `H:\Macro App Setup 0.1.27 (slim).exe` (built without the
  pip step because `python-runtime` was locked by the running dev app; runtime verified importable).
  It does NOT contain the three fixes below.
- **Blank launch splash on laptop** (square empty ~10s, content appears at the end): cause is a
  blocked main process during synchronous `require()` of subsystem trees on a cold/AV-scanned
  install. Fix: `loadSubsystems()` is now async and yields a macrotask between each of 34 requires;
  `waitForLaunchSplashPaint` waits `SPLASH_PRESENT_SETTLE_MS = 120` after ready-to-show; boot
  stall watch logs `[boot] main thread stalled Xs` until reveal. Symptom row in
  `docs/LAPTOP_LAUNCH.md`.
- **Makeup Exam tab opens on a class**: last used (persisted key
  `macro-app-makeup-exam-last-course-code` via `usePersistedState`), else first course; re-picks
  if selected course disappears. Reset keeps the class (log says "Pick students again").
- **Makeup Exam calculator**: live form `#LSC_TCRFORMS_LSC_TCCALCULATOR` (frame `TargetContent`)
  now has S=Scientific, N=None, A=Any, F=Four Function, G/C/T graphing. Side panel choice maps
  straight: Scientific → `S`, anything else → `A` (no class-code heuristic — that produced
  "None"). Selected by value, read back, raises if not kept. Side panel label "Default (any
  calculator)" → "Any" (persisted value still `'default'`).

## 4. Rejected directions

- Don't kill Chase's running dev Macro App to unlock `python-runtime` for builds.
- Don't guess the splash cause from this PC's log — the slow machine is the laptop (installed);
  this PC boots in ~1s.
- Don't restore the calculator class-code heuristic (1314/1324).

## 5. Current implementation state (all uncommitted in Macro App)

Mine from this stretch:
- `electron-app/main.js` (async `loadSubsystems` w/ `loadYielding`, stall watch start/stop),
  `electron-app/launch-splash-window.js` (settle delay, `splash shown` mark),
  `electron-app/boot-timing.js` (`startStallWatch`/`stopStallWatch`), `docs/LAPTOP_LAUNCH.md`
- `renderer/src/hooks/makeup-exam/useMakeupExam.ts`, `useMakeupExamAutomation.ts` (reset msg)
- `modules/makeup-exam/backend/automation_actions.py` (`calculator_option_for_mode`,
  `select_calculator`), `automation_core.py` (uses it; now 733 lines — over 700, don't add to it),
  `tests/test_pure_helpers.py`, `renderer/src/components/makeup-exam/MakeupExamExamConfigPanel.tsx`
- `package.json` version 0.1.27 (bumped by the approved installer build).

Not mine (another session's in-progress work — leave alone): Teacher Console components/services
splits, `teacher-console*.css`, `browser-view-slots.js`, `browser-slot-phone-emulation*.js`,
`browser-slot-wire-webcontents.js`, `AGENTS.md`, `AppMainPanel.tsx`.

Verification: renderer `tsc` + eslint clean; electron lint + typecheck clean; vitest 753 passed;
makeup-exam pytest passed (run from app root with system `python`); calculator helper exercised
live on the open form (Any/Scientific kept, restored to None, nothing submitted). Splash fix not
observed visually — needs the laptop install.

## 6. Open questions and constraints

- Makeup Exam Python process must restart (restart Macro App) to pick up calculator change.
- Splash fix effectiveness unproven until a new slim installer runs on the laptop; if still slow,
  read that machine's `%APPDATA%\macro-app-slim\logs\macro-app.log` `[boot]` stall lines.
- Building while dev app runs: `build:python` fails (locked `.pyd`); build without pip step only
  after verifying runtime imports, and only when Chase asks.
- Never launch GUI / open windows without asking. Don't commit/push mid-session.

## 7. Exact next step

Ask nothing — wait for Chase's next requested change for the slim build and implement it (code
only, headless verification). Build the installer only when he says to.
