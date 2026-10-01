# Momentum handoff — Macro App Track B (browser + Teacher Console preview)

**Written:** 2026-09-30 · **Valid:** today's continuation only · **Not** an end-of-session; nothing pushed by this task.

## Read first
1. `School Scrips/Macro App/docs/plans/MACRO_APP_REMAINING_WORK.md` — the one open plan. § Track B has checkboxes with dated notes of everything done below.
2. `School Scrips/Macro App/docs/BROWSER_TAB_INTEGRATION.md` (Phase 2–3 load-arbiter contract) only if touching slot loading.

## Objective and phase
Chase asked me to work through the plan's Track B in order, "just do it" each step. Done: B0, B1 (all but its "one result shape" audit), B2 (all but the optional default-to-Live item), B3, B4. Track D marked complete on Chase's word (CI/live test not re-verified by an agent). Track A and C untouched. Chase says the preview "has seemed okay so far" — so B is hardening, not firefighting.

## Chase's desired feel
Predictable, not "seamless": Refresh visibly reloads or visibly fails; a course switch never leaves the old class on the phone. Fix the app-wide lifecycle, don't bend TC to a flawed shared abstraction. Dwell-click user: no hover-only UI, no timed-dismiss errors, no ephemeral "Copied!" feedback.

## Accepted decisions (Chase said go ahead)
- Removed legacy `browserView.show()` + `ensureSessionVisible/Hidden` IPC; Pearson tab now uses `activateSlot('pearson')`. **Behavior change:** revisiting Pearson no longer resets it to the portal home URL (only bootstraps a blank slot). Not yet called out as a question — mention if Chase notices.
- Failed navigates now throw (`navigateViaIpc` retired); callers catch.
- Slot's actual URL is the only navigation truth (no `lastNavigatedUrlRef` / external-nav event).
- Toolbar Reload = big Refresh; Reset = `restartSlotAtUrl` at canonical preview URL.
- "Switching class…" is label text above the frame, NOT an overlay — the native view paints over any HTML overlay (honest limit). B4's bezel dim is the visual cue.

## Rejected / don't rediscover
- Plan's "~40 direct slot-command sites bypass the queue" was stale: all callers already use the facade's per-slot queue; gradebook course slots skip it on purpose (arbiter coalesces; queue deadlocked Pull). Guard test exists.
- Don't re-read `getSlotNavState` after activate — activate's returned URL is already the actual URL.
- Don't add hook-render tests without asking: repo has no `@testing-library/react`; untested by design: course A resolution finishing after switch to B, and the Refresh/Reset hook itself.

## Implementation state
- **All this work is already committed, but on branch `cursor/work-it-out-ink-pad-fbfc`, NOT `main`** (another session's "Sync work in progress." commit swept it in). Macro App rule is main-only (`AGENTS.md` § Git). Needs merging to main — ask Chase / follow `agent docs/rules/multi-repo-git-push.md` § Main only. Only uncommitted Macro App file: `renderer/src/hooks/teacher-console/useWorkItOutInkPad.ts` (not mine).
- Verification at B4: renderer vitest 1600 pass; electron-app `node --test electron-app/*.test.js` 153 pass; `lint:electron` clean; `tsc` = 135 errors, all pre-existing test-file errors (baseline — none in non-test files). `ci:local` NOT run. App never launched (Chase rule: never launch GUI without asking).
- Key files: `electron-app/browser-slot-navigation.js` (`loadUrlDetached`), `browser-slot-ensure-url.js` (arbiter), `browser-slot-phone-emulation.js` (returns on/failed/skipped; `phoneEmulationField`), `renderer/src/services/slotOrchestrator.ts`, `slotSessionStore.ts` (`phoneEmulation`), `hooks/browser/useEmbeddedBrowser.ts` (685 lines; `restartSlotAtUrl`, `currentSlotView`), `hooks/teacher-console/useTeacherConsolePortalPreview.ts` / `…PreviewIdentity.ts` (`ready`, `grantError`) / `…PreviewRefresh.ts` (`refreshError`, `onReset`), `utils/studentProgress/previewSectionGrant.ts`, `utils/browser/navigateSlotViaIpc.ts`, `__tests__/slotCommandContract.test.ts`.
- Over-cap flag: `hooks/shell/useMacroAppShell.ts` is 749 lines (hard cap 800, extract line 700). Split before anyone adds to it. `styles/teacher-console-workspaces.css` is 1186 lines — don't edit; I put new TC styles in `teacher-console.css` (781 lines, near cap).
- Session scorecard bumped for each step.

## Open questions / constraints
- Decision 1 (plan): default preview source to Live when dev server isn't running — optional B2 item, needs Chase.
- Hand-tests Chase still owes (plan § Verification): rows 3,4 (course switch), 10 (stop dev server → Refresh → error line), 12 (Reset keeps source/course/persona), 6 (rotate). Also Track A1 sandbox restore test. State these flatly; never ask to launch.
- B0A (shared browser contract design/ADR) is still unwritten — plan says design before further behavior edits; B6/B7 are small enough to proceed, but the "one coordinator" vision needs B0A first.

## Exact next step
**B6 — roster mutations → preview reload:** one debounced preview-invalidation callback above the roster/tester components (not scattered through `useRosterAppAccess`, `RosterStudentActions`, cards); reload only when the mutation affects the active preview persona/activity or its effective section (hand-test rows 11, 13). Reuse `onRefresh` from `useTeacherConsolePreviewRefresh` (via `previewEmbedActions`). Then B5 verify (Chase), B7 optional, B0A ADR.
