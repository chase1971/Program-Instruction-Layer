# Momentum handoff — Teacher Console preview-first redesign (implemented, uncommitted)

**Written:** 2026-09-14 (Monday, evening)

---

## 1. Objective and current phase

Chase wanted the **Teacher Console redesigned** to match the prototype at
`agent docs/scratch/teacher-console-concept.html`: Preview as the daily workspace (portal +
tester panel), left nav (Preview · Students & responses · Testers · Manage class), app switcher
without leaving the workspace, and setup tasks moved to Manage class — while preserving all real
roster, preview, response, and IPC behavior.

**Phase:** Implementation is **done and verified headlessly**. All plan to-dos completed. Macro App
was pulled at session start (+2 commits). **Nothing committed or pushed.** Chase is about to
request follow-up changes (polish, cleanup, or behavior tweaks) on top of this redesign.

## 2. Chase's desired feel

- Prototype = **layout and interaction model**, not sample data or fake codes.
- **Preserve real behavior** — roster actions, portal preview, response schemas, services/hooks;
  no parallel mechanisms.
- **Dwell-click accessibility** — `aria-pressed` selected states, 44px targets, no hover-only UI.
- **Never launch GUI** without asking; hand off live smoke tests to Chase with what to run/expect.
- Speech-to-text: "feature console" = **Teacher Console**; Student Progress tab = Teacher Console in UI.
- Do not edit the plan file (`teacher_console_redesign_*.plan.md`).

## 3. Accepted decisions

| Decision | Detail |
|---|---|
| **Default home = Preview** | Replaces dashboard-first; `DEFAULT_TEACHER_CONSOLE_VIEW = { kind: 'preview' }` |
| **Workspace nav** | `preview` · `students` · `testers` · `manage` (+ manage sub-views for logins, exit-ticket create/quiz) |
| **Unified app catalog** | `useTeacherConsoleActivityCatalog` — matrix (Gauss-Jordan) + **published** exit tickets only |
| **Preview layout** | Portal embed (left, max 812px landscape) + `PreviewTesterPanel` (roster/responses tabs) |
| **Controls row** | `TeacherConsolePreviewControlsBar` — Live/Preview · Admin/Student tester · Landscape/Portrait in main area |
| **Side panel role** | Contextual tools only — refresh all/page, dev server, admin tools (Preview); bulk roster (Roster tab); view tuning + attempt policy (Responses) |
| **Response detail** | Inline `ResponseDetailPanel` below grids in workspace contexts (not modal navigation) |
| **Students vs Testers** | Shared `ConsoleActivityWorkspaceScreen`; testers use `testersOnly` on roster + filtered response rows |
| **Removed drill-in panels** | Deleted `TeacherConsoleAppPanel.tsx`, `TeacherConsoleExitTicketPanel.tsx` (replaced by workspace model) |
| **CSS** | New `teacher-console-workspaces.css` imported via `teacherConsoleEntry.ts` |

## 4. Rejected directions

- Do **not** copy prototype demo apps, student names, tester codes, or mock portal HTML.
- Do **not** resurrect dashboard as default entry (`ConsoleDashboardScreen` still on disk but unwired).
- Do **not** deep-link portal preview to selected app — app switcher updates **tester/student panels only**; portal stays on home (existing behavior).
- Do **not** create parallel service/hook layers — extend existing `studentProgressService`, roster hooks, matrix/exit-ticket report hooks.

## 5. Current implementation state

**Repo:** `School Scrips/Macro App` — **all redesign changes uncommitted** (28 files touched).

### Navigation / shell
- `renderer/src/hooks/teacher-console/useTeacherConsoleNavigation.ts` — workspace-first views + `selectedActivityIndex` + `previewTesterPanel`
- `renderer/src/hooks/teacher-console/useTeacherConsoleActivityCatalog.ts` (+ test)
- `renderer/src/hooks/shell/useMacroAppStudentProgressShell.ts` — roster access when Preview/Students/Testers active; unified `previewSource`; first-paint gate for Preview

### New workspace UI
- `TeacherConsoleWorkspaceShell.tsx`, `TeacherConsoleWorkspaceNav.tsx`, `TeacherConsoleAppSwitcher.tsx`, `TeacherConsolePreviewControlsBar.tsx`
- `screens/ConsolePreviewWorkspaceScreen.tsx`, `PreviewTesterPanel.tsx`
- `screens/ConsoleActivityWorkspaceScreen.tsx` (Students + Testers)
- `screens/ConsoleManageClassScreen.tsx`
- `ActivityResponsesPanel.tsx`, `ResponseDetailPanel.tsx`
- `utils/teacher-console/filterTesterRows.ts`
- `styles/teacher-console-workspaces.css`

### Refactored
- `TeacherConsoleWorkspace.tsx`, `teacherConsoleWorkspaceProps.ts`
- `TeacherConsoleSidePanel.tsx`, `TeacherConsoleDashboardPanel.tsx`, `TeacherConsolePortalPreviewControls.tsx` (`hideModeAndIdentityControls`)
- `AppMainPanel.tsx`, `AppSidePanel.tsx`
- `ConsoleRosterScreen.tsx` — added `testersOnly` prop

### Dead / unused (safe to delete in a cleanup pass)
- `screens/ConsoleDashboardScreen.tsx`
- `screens/ConsoleAppLiveScreen.tsx`
- `screens/ConsoleGradesScreen.tsx` (was already unwired)

### Verification (headless, this session)
- `npm run build:renderer` — green
- vitest: portalPreviewUrl, portalPreviewPersona, useExitTicketResponseReport, matrixReportProgress, matrixReportRoster, useTeacherConsoleActivityCatalog — **43 tests pass**

### Not verified visually
Chase has not live-smoked Preview workspace, app switcher, Students/Testers grids, or Manage class flows yet.

## 6. Open questions and constraints

- **Live smoke** — Preview portal + tester panel side-by-side; app switcher updates roster access/responses; back buttons from secondary workspaces.
- **Follow-up cleanup** — remove dead screens/CSS (`teacher-console-dashboard.css` partially unused); wire or delete `ConsoleGradesScreen`.
- **`refreshPortalPreview.ts`** — still matrix-oriented for URL build; extend only if preview refresh must be activity-aware.
- **Slim build** — if shell imports new Teacher Console exports, update `ci-shims/teacher-console/teacherConsoleEntry.ts` too (`docs/SLIM_DISTRIBUTION_BUILD.md`).
- **File size** — `teacher-console.css` was over cap in prior sessions; new CSS is in separate `teacher-console-workspaces.css`.
- **No commit/push** unless Chase asks. Never launch Macro App GUI without permission.
- Machine-local dirty: `config/d2l-courses.json` — do not commit.

## 7. Read first (next agent)

1. **`agent docs/momentum-handoffs/latest.md`** (this file) — check Written date
2. **`School Scrips/Macro App/AGENTS.md`** — Teacher Console / live preview rows
3. **`agent docs/scratch/teacher-console-concept.html`** — layout reference only
4. **`renderer/src/components/teacher-console/TeacherConsoleWorkspaceShell.tsx`** — view dispatch
5. **`renderer/src/hooks/teacher-console/useTeacherConsoleNavigation.ts`** — view model

Plan (reference, do not edit): `.cursor/plans/teacher_console_redesign_3b9499eb.plan.md`

## 8. Exact next step

Wait for Chase's specific change request on the redesigned Teacher Console (polish, bug from live
smoke, dead-code cleanup, or new behavior). Read the files he names or the symptom he describes,
then implement minimally on top of the uncommitted redesign — **do not rebuild from dashboard-first
navigation**.

If he asks to verify: describe what to open (Teacher Console tab → Preview) and what to report;
do not launch Macro App yourself.
