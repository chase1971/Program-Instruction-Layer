# Momentum handoff — 2026-09-10 — Matrix tutorial + portal identity + Teacher Console roster tools

> **Written:** 2026-09-10 (late evening) · **Repos:** student-portal, Matrix app, Macro App, App Dashboard, electron-toolbar, student-session-kit (all uncommitted except migrations pushed to Supabase)

## Objective and current phase

Ship the **Gauss-Jordan Matrix tutorial** in **Student Portal** (M1324, **Portal Wide** 812×460). Parallel work this session: **device code-lock** UX, **instructor revoke-code** so a new spare link replaces a dead code without any student action, and **Teacher Console roster** polish (per-spare Copy link, scroll rails).

Phase: **locally green, QA partially done** — Chase revoked **NAJPJK** (M1314 SPARE-2) and sent a friend a **new M1324 spare link**; **not confirmed working yet**. Matrix tutorial Auto Solve / full walkthrough QA still outstanding. **Seven repos dirty; nothing committed.**

## Chase's desired feel

- **Students only click links** — never ask them to clear storage, reset, or use a student-facing “switch code” flow.
- **Instructor fixes device lock** — revoke old code in Supabase, send new spare link; portal auto-clears dead code when they open the new URL.
- **Shaped window** — **Portal Wide** or **Portal Debug** launchers only; never raw localhost URLs to Chase.
- **Matrix tutorial** — home completion message (no flash of intro on re-entry), Auto Solve two-mode Next, completion lands on home not result screen, etc. (see prior handoff — still valid).
- **Teacher Console** — spare **Copy** per row (full URL); **Revoke code** per spare; scroll rails on Roster, Grades student list, Matrix report.

## Accepted decisions

| Decision | Why |
|---|---|
| Device code-lock stays (link ≠ stored code → block) | Prevents account sharing on same device |
| **No student-facing reset** | Chase explicit — instructor-only revoke |
| `revoke_student_code(p_student_id)` deletes student row in Supabase | `claim_student` fails → portal clears localStorage on next new link (existing hook logic) |
| Mismatch gate shows stored code + **Open my link** | Helps stuck students return to *their* code — not for switching |
| `progressKnown` in `useMatrixTutorialAttempt` | Avoid intro flash before “Tutorial complete” on home |
| Roster spares: **Copy** + **Revoke code** buttons | Per-spare link handout + instructor reset |
| `ViewportScrollFrame` scroll rails on TC roster/grades/matrix | Dwell-friendly; exemplar pattern |

## Rejected directions

- **Student-facing “use new link” / clear device button** on mismatch screen — rejected this session.
- Pinning old codes (NAJPJK) like CHASE1 — Chase prefers revoke + new spare link.
- Student instructions to clear browser data or use InPrivate — instructor path only.

## Current implementation state

### student-portal (dirty)

| Area | Files |
|---|---|
| Matrix tutorial / home / completion | `MatrixTutorialView.tsx`, `MatrixTutorialHomePanel.tsx`, `MatrixAutoSolveNav.tsx`, `useMatrixTutorialAttempt.ts`, … |
| **Code mismatch UI** | `PortalGate.tsx`, `useStudentIdentity.ts` (`storedCode`), `studentIdentity.ts` (`buildStudentPortalLink`) |
| **Completion hydration** | `useMatrixTutorialAttempt.ts` — `progressKnown` + `useLayoutEffect` |
| Layout debug (remove when done) | `useLayoutDebug.ts`, `LayoutDebugLegend.tsx`, `portal-layout-debug.css`, `launch-horizontal-debug.bat` |
| Orphan | `MatrixTutorialResult.tsx` (unused) |

Build: **passes** (`npm run build`).

### Matrix app (dirty)

Auto Solve ref (`jumpToStepResting`, two-mode Next), portal props, popover tweaks, sum-step `timingScale` — unchanged from earlier handoff.

### Macro App (dirty)

| Area | Files |
|---|---|
| **Revoke code** | `RosterSpareRevokeButton.tsx`, `ConsoleRosterScreen.tsx`, `student-progress-io.js`, `preload.js`, `studentProgressService.ts` |
| **Spare Copy** | `RosterSpareCopyButton.tsx` |
| **Scroll rails** | `ConsoleRosterScreen.tsx`, `ConsoleGradesScreen.tsx`, `ConsoleMatrixReportScreen.tsx`, `teacher-console-grades.css`, … |
| Copy actions split | `StudentProgressCopyActions.tsx` — roster vs spare codes/links |
| Matrix report | Reset scores (011 RPC) — existing |

Skip on commit unless asked: `config/d2l-courses.json`.

Build: **passes** (renderer).

### student-session-kit (dirty files, **migrations live**)

| Migration | Status |
|---|---|
| `011_reset_student_attempts.sql` | Applied via `db:push` |
| `012_revoke_student_code.sql` | Applied via `db:push` this session |

### Other dirty

| Repo | Change |
|---|---|
| App Dashboard | `apps.json` — Portal Wide + Portal Debug |
| electron-toolbar | `scripts-panel.html` — Portal Debug tile |

### Verification

- Chase **revoked NAJPJK** and sent friend a **new M1324 spare link** — **outcome unknown**
- Matrix tutorial full QA / Auto Solve re-QA — **not confirmed this session**
- Code mismatch + revoke flow — **not formally tested by agent**

## Open questions and constraints

- **Friend link after revoke** — Did new spare link bind and show Matrix app? Report back to next agent.
- **NAJPJK revoke** was on **M1314** roster; new link from **M1324** spares — correct cross-course workflow.
- **Remove layout-debug** launcher/CSS when Matrix QA done?
- **Commit/push** — wait for “put on GitHub” or end-of-session; six+ repos.
- **Never open GUI without permission** — QA is Chase’s launchers.
- **Future:** teacher alert when someone hits code-mismatch (deferred).

## Exact next step

1. **Chase (or agent after report):** Confirm friend’s **new spare link** works after NAJPJK revoke — Matrix home loads, grades appear on M1324 Matrix report under new spare.
2. **Chase:** Matrix tutorial QA on **Portal Wide** (Auto Solve, Parts 1–3, Finish → home completion).
3. **Agent:** Fix any QA findings; then ask about removing layout-debug, deleting `MatrixTutorialResult.tsx`, committing all repos.

## Read first (fresh agent)

1. This file
2. `School Scrips/student-portal/AGENTS.md`
3. `School Scrips/student-portal/src/hooks/useStudentIdentity.ts` — mismatch + auto-clear on dead code
4. `School Scrips/Macro App/renderer/src/components/teacher-console/screens/ConsoleRosterScreen.tsx` — Copy / Revoke
5. `School Scrips/student-session-kit/supabase/migrations/012_revoke_student_code.sql`
6. `School Scrips/student-portal/src/features/matrix-tutorial/MatrixTutorialView.tsx`
