# Momentum handoff — Macro diagnostics checkpoint done → safe browser-slot restore

**Written:** 2026-09-24
**App:** `School Scrips/Macro App`
**Primary plan:** `docs/plans/TEACHER_CONSOLE_PREVIEW_SMOOTHNESS_PLAN.md`

## 1. Objective and current phase

Chase wants the Teacher Console embedded preview to feel smooth and predictable, but does not
want it forced into a flawed Macro App framework. If the correct Teacher Console design requires
an app-wide embedded-browser restructure, change the framework. The combined plan therefore uses
Teacher Console as the first migration toward one coherent browser-slot system.

Implementation has started in small checkpoints so Chase can test between behavior changes.

Completed in this task:

1. **Crash-evidence checkpoint:** durable main/renderer/child failure diagnostics.
2. **Visible logging checkpoint:** an app-wide, current-session Diagnostics view with
   warnings/errors separated from ordinary activity.

No navigation, isolation-restore, or Teacher Console URL behavior has been changed yet.
The next browser reliability work is still pending.

## 2. Chase's desired feel

- He wants to know that an actual warning or error happened without opening DevTools or hunting
  through a long ordinary log.
- The Teacher Console's small console-error panel is the model he likes: visible, copyable, and
  focused on problems.
- He still wants ordinary operational logs when useful, so the chosen design has two views over
  one event stream: **Warnings & errors** and **All activity**.
- He wants this capability app-wide and permanent as part of the architecture, not a one-off
  Teacher Console patch.
- Browser smoothness should be predictable rather than promising impossible zero latency:
  no stale-class flashes, silent failures, or stranded slots; unavoidable waits should have
  visible state and recovery.
- Chase uses a dwell mouse. Never launch the GUI, open windows, or run visible UI smoke tests
  without per-run permission. Modals must not dismiss on backdrop click.

## 3. Read first

From Programs root, read:

1. `AGENTS.md`
2. `agent docs/INDEX.md`
3. `School Scrips/Macro App/AGENTS.md`
4. `School Scrips/Macro App/docs/plans/TEACHER_CONSOLE_PREVIEW_SMOOTHNESS_PLAN.md`
5. `School Scrips/Macro App/docs/LOGGING.md`

Use `docs/plans/MACRO_APP_RESTRUCTURE_RECOMMENDATIONS.md` as the independent app-wide review,
not as a competing implementation plan.

## 4. Accepted decisions

### Embedded-browser architecture

The plan now targets:

- one explicit slot state machine;
- a desired-state coordinator;
- structured results instead of mixed booleans/null/fire-and-forget success;
- one event-backed renderer store;
- one bounds owner;
- one app-wide isolation transaction;
- slot profiles for feature-specific policy;
- Teacher Console first, simple slots next, Gradebook last.

Do not preserve an existing abstraction merely because Macro App already uses it.

### Logging and diagnostics

- There is **one logging mechanism**, not a separate error-log system.
- Electron severity (`debug`, `info`, `warn`, `error`) is now preserved in
  `moduleLogStore`.
- Settings has a **Diagnostics** section with:
  - Warnings & errors
  - All activity
  - copy, clear, pause-scroll, and follow-latest controls
- The always-visible Settings control shows a red issue count. If issues exist when Settings is
  opened, it starts on Diagnostics.
- Renderer `console.warn`, `console.error`, uncaught errors, and unhandled rejections are
  captured into the shared in-memory store while still appearing in DevTools.
- The Teacher Console preview forwards both console warnings and console errors.
- `createFeatureLogger` now has `warn()` and `error()`; routine progress remains `log()`.
- The visible panel is intentionally **current-session only** for now.
- Durable crash history remains in the existing redacted rotating `macro-app.log`.
- Prior-session issue recovery is a planned follow-up: add severity to that existing file format
  and read a bounded recent slice. Do not create a second file or unbounded history.
- Do not indiscriminately forward every D2L/Pearson page warning. Third-party embedded-console
  capture should become a slot-profile policy so noisy vendor pages cannot drown first-party
  failures.

## 5. Rejected directions / do not rediscover

- Do not add a second errors-only store or error log. The two views are selectors over the shared
  store.
- Do not make the Teacher Console conform to current Macro inconsistencies. The app-wide contract
  can change.
- Do not claim the 2026-09-22 full-app crash cause is known. It remains unconfirmed; the point of
  crash diagnostics is to gather evidence.
- Do not add another timeout wrapper directly inside the 758-line
  `browser-view-slots.js`. It is already over the 700-line extraction threshold.
- Do not add toast/ephemeral success feedback.
- Phone emulation is already bounded at 750 ms; do not re-plan a redundant 5-second wrapper.
- Slot detach-without-destroy already exists; do not present it as new work.
- An already queued D2L run waits for restore, but a newly submitted run can start because
  `runningByModuleId` is cleared before restore settles. Preserve this corrected understanding.
- Makeup Exam is a second isolation entry point; do not design the isolation lock only around
  `d2l-bridge.js`.

## 6. Current implementation state

Everything is uncommitted. Do not commit or push unless Chase explicitly requests GitHub or runs
the end-of-session protocol. The Macro App worktree was already heavily dirty with unrelated
Assignment Assistant cleanup, settings redesign, config, and other user/agent changes. Preserve
all of it.

### Crash diagnostics

- `electron-app/crash-diagnostics.js` — new helper for uncaught exceptions, unhandled
  rejections, Electron child-process failures, main-window renderer failure/unresponsive events.
- `electron-app/crash-diagnostics.test.js` — new focused tests.
- `electron-app/macro-log-file.js` — added crash-only synchronous append using the same
  file, format, and redaction boundary.
- `electron-app/main.js` — wiring only; now 659 lines.

### Visible diagnostics

- `renderer/src/services/moduleLogStore.ts` — entries now retain severity; filters support
  levels; entry snapshots are exposed.
- `renderer/src/hooks/shared/useModuleLogLines.ts` — added entry selector hook.
- `renderer/src/services/rendererDiagnostics.ts` and test — capture otherwise
  DevTools-only renderer warnings/errors and unhandled failures.
- `renderer/src/main.tsx` — installs renderer diagnostics outside modal-catalog mode.
- `renderer/src/utils/shared/createFeatureLogger.ts` — added `warn` and `error`.
- `renderer/src/components/AppErrorBoundary.tsx` — emits a real error-level entry.
- `renderer/src/components/settings/AppSettingsDiagnosticsPanel.tsx` — new dual-view panel.
- `renderer/src/components/AppSettingsModal.tsx`,
  `components/settings/AppSettingsSidebar.tsx`, and
  `components/settings/appSettingsTabs.ts` — Diagnostics integration.
- `renderer/src/components/chrome/SettingsButton.tsx` — red issue-count badge.
- `renderer/src/styles/app-settings.css` and `styles/shell-tabs.css` — diagnostics/badge styles.
- `electron-app/browser-slot-console-forward.js` — Teacher Console preview now forwards
  warnings and errors.
- `TeacherConsolePreviewConsoleErrorsPanel.tsx` — label and empty state now say
  warnings & errors.
- `renderer/src/types/macroApp.d.ts` and log-discipline allowlist updated.

Important dirty-tree detail: several settings redesign files, including
`AppSettingsSidebar.tsx`, `appSettingsTabs.ts`, and `app-settings.css`, were already
untracked changes before this work; the diagnostics integration legitimately extends them.
Do not replace them with versions from HEAD.

### Documentation

- `docs/LOGGING.md` documents the crash-durable path, severity rules, Diagnostics UI, and
  current-session boundary.
- `docs/plans/TEACHER_CONSOLE_PREVIEW_SMOOTHNESS_PLAN.md` is the merged working plan and records
  both completed logging checkpoints plus prior-session recovery.
- `AGENTS.md` routes app-wide diagnostics requests to `docs/LOGGING.md`.
- `docs/plans/MACRO_APP_RESTRUCTURE_RECOMMENDATIONS.md` remains the independent comparison.

## 7. Verification already completed

Headless checks passed:

- 7 focused crash/isolation/phone-emulation Node tests at the first checkpoint.
- Latest focused set: 7 Vitest tests and 5 Node tests passed.
- Renderer TypeScript check passed.
- Electron TypeScript check passed.
- Renderer lint passed.
- Electron lint passed.
- Production renderer build passed (only existing Vite chunk/dynamic-import warnings).
- Documentation checker passed with 0 dead links; unrelated existing warnings remain.
- `git diff --check` passed.

No GUI was launched. Chase has not live-tested the new Settings Diagnostics UI.

Expected visible checkpoint when Chase next launches normally:

- Settings contains **Diagnostics**.
- A new warning/error creates a red count on Settings.
- Opening Settings while the count exists lands on Diagnostics.
- Diagnostics can switch between issues-only and all activity.
- Teacher Console Preview's panel says **Console warnings & errors**.

## 8. Open questions and constraints

- Current-session diagnostics disappear on restart; durable logs remain on disk. Prior-session
  recovery is planned but not implemented.
- The persisted log record currently omits severity as a separate field. Change that format
  carefully because audit-log examples and any parsers may depend on it; grep before editing.
- Many renderer call sites still emit problem-sounding text through `log()`. Migrate only real
  warnings/errors as their features are touched; do not use broad keyword inference that turns
  “no errors” into an error.
- The Teacher Console navigation bugs and isolation restore failures are still confirmed and
  unfixed.
- `browser-view-slots.js` is 758 lines. Extract before editing it.
- No visible testing without Chase's explicit permission.

## 9. Exact next step

First, report the live-test checkpoint from section 7 and incorporate any result Chase gives.
If he proceeds without reporting a UI problem, implement **Phase 1 task 2** from the Teacher
Console smoothness plan: make `browser-slot-isolation-restore.js` restore each captured slot
inside its own try/catch, continue after one failure, restore the previously visible slot last,
and return a structured `{ restored, failed }` result. Add focused headless tests and stop at
that next phase boundary. Do not touch the over-cap `browser-view-slots.js` yet.

