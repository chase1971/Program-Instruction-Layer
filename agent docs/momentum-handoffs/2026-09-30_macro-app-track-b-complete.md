# Momentum handoff — Macro App Track B (browser + Teacher Console preview): B done, hardening complete

**Written:** 2026-09-30 (second handoff today; replaces the earlier "B6 next" one) · **Valid:** today's continuation only.

## Read first
1. `School Scrips/Macro App/docs/plans/MACRO_APP_REMAINING_WORK.md` — the one open plan. § Track B is now fully checked except the optional items below. Tracks A and C untouched; D marked complete on Chase's word.

## Objective and phase
Track B (make the embedded browser + Teacher Console phone preview predictable) is **finished and on `main`**. Chase hand-tested: course switch, rotate, Reset, tester access toggle (reload) and unrelated-student toggle (no reload) all pass. He could NOT test "stop the dev server -> Refresh -> error line" (can't turn the dev server off) — that one is unverified by a human.

## Chase's desired feel
Predictable, not "seamless": Refresh visibly reloads or visibly fails; a course switch never leaves the old class on the phone. Dwell-click user: no hover-only UI, no timed errors, no ephemeral "Copied!". He said the stale-announcement flash on launch is "not that big a deal" — don't chase it.

## Accepted decisions
- B6: one `onRosterMutation(change)` (shell hook `useMacroAppStudentProgressShell`) -> `useTeacherConsolePreviewRosterSync` (500 ms debounce) -> existing `onRefresh`. Rule in `utils/studentProgress/rosterMutationAffectsPreview.ts` (preview student + previewed activity for access; + previewed section for membership). Covers access toggle and tester course assign/remove. Progress Reset does NOT reload the phone (deliberate).
- Return-to-Preview bug fixed (`1d45e47`): `useTeacherConsolePortalPreview` skipped activation when the slot URL already matched, leaving "Loading embedded browser…" after leaving Preview and returning to the same class. Now calls `activateSlot(STUDENT_PORTAL_PREVIEW_SLOT, {visible:true})` on a match.
- Admin preview persona bypasses app-access checks by design (`isInstructorDevice()` in student-portal). To test deactivation use **Student tester**.

## Rejected / don't rediscover
- Stale announcement on fresh launch = portal's own localStorage cache (`student-portal/src/services/announcementData.ts`) painting before the fetch. By design; Chase declined a change.
- Don't add hook-render tests without asking (no `@testing-library/react`). Untested by design: the Refresh/Reset hook, the roster-sync hook, course A resolving after switch to B.
- Plan's "~40 slot-command sites bypass the queue" was stale; don't re-audit.

## Implementation state
- Macro App `main` has B6 (`17caa8e`) and the return-to-Preview fix (`1d45e47`); Chase asked to push them — check `git rev-list --left-right --count main...origin/main` (0 0 = pushed). Branch `cursor/work-it-out-ink-pad-fbfc` was already merged; ignore it.
- Verification: renderer vitest 1614 pass; non-test `tsc` clean; eslint 0 errors. `ci:local` NOT run by an agent. App never launched by an agent (Chase rule).
- Over-cap flags: `hooks/shell/useMacroAppStudentProgressShell.ts` ~508 lines (ok); `useMacroAppShell.ts` 749 (split before adding); `styles/teacher-console-workspaces.css` 1186 (don't edit).

## Open questions / optional leftovers (none required)
- B0A (shared browser contract ADR) unwritten — only needed before more big browser-behavior changes.
- B7 bounds-sync cleanup (optional); B1 "one result shape" audit; B2 default-to-Live when dev server is down (needs Chase's decision).
- Untested by a human: stop dev server -> Refresh -> error line under the embed.

## Exact next step
Nothing in Track B is blocking. Ask Chase which to do next: Track A (gradebook hardening + sandbox restore test), Track C opportunistic restructure, or an optional B item. Don't start any without his pick.
