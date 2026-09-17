# Momentum handoff — Teacher Console Students & Responses (layout done, follow-up planned)

**Written:** 2026-09-15 (Tuesday, evening)

---

## 1. Objective and current phase

Chase is redesigning the **Teacher Console → Students & responses** workspace (Macro App) so
the main panel is tighter and the side panel owns navigation chrome. The **first layout pass is
implemented and Chase said it looks good.** The session then scoped a **follow-up batch** (arrow
centering, side-panel cleanup, cell colors, response detail modals, statistics view) — **plan
written, not implemented yet.**

**Phase:** Implement follow-up from the approved plan (`responses_follow-up_polish` in Cursor
plans). Do **not** redo the completed layout work unless something regressed.

---

## 2. Chase's desired feel

- **Less vertical chrome** in the main panel — app switcher and grid start near the top; no
  redundant "Students & responses" heading or inline back button.
- **Back to preview** lives on the **same line as "Teacher Console"** in the side panel, far
  right (all non-preview workspaces: Students, Testers, Manage class).
- **Arrow pad** beside the response grid: **minimal left gutter** (~one arrow-pad wide), **vertically
  centered halfway down the visible roster/grid** — not stuck at the top.
- **Dwell-friendly** — big click targets; collapsible side-panel sections (not hover-only).
- **Students vs Testers split** — spares (Chris, Kristy, Michelle, Ashley) belong in **Testers
  only**; remove from Students responses grid (they already live in Testers).
- **Checkmarks green, X's red** — should pop on the activity workspace grid.
- **Response detail** — centered **modal** (max-w-md), not a wide bar at the bottom of the page.
- **Statistics** — button in the **center** of the head row (app switcher | Statistics | Roster/
  Responses tabs). Clicking **replaces the grid** with a "TV wall" of stat tiles:
  - Bar chart: which **response** questions were missed most (not Part 1–3 completion).
  - Ranking: students who missed the most → fewest; **ties show "N students"** with click to
    expand names.
- **Completion vs response** — new distinction: Part 1/2/3 = completion; Q1–Q7 = responses.
  Statistics care about **responses only**. Future ported apps will designate column kinds.
- **Statistics scope (Chase confirmed):** matrix apps **and** exit tickets (exit ticket questions
  all count as responses).

---

## 3. Accepted decisions

| Decision | Detail |
|---|---|
| Back button placement | Side panel header row, right of "Teacher Console"; removed from main Students/Testers/Manage screens |
| Page title removed | No "Students & responses" + course subheading in main panel |
| Side-panel back scope | All non-preview workspaces; manage sub-screens keep inline "Back to manage class" |
| Compact scroll rail CSS | Activity-workspace block in `teacher-console-matrix-report.css` (not `teacher-console-workspaces.css` — over 800 lines) |
| Remove "Reset my scores" | Stop rendering `TeacherConsoleMatrixGradesPanel` in responses side panel (do not delete the component file) |
| Collapsible tuning | One `GradebookFilteringPanelCollapsibleSection` wrapping tuning + attempt policy + refresh; default **closed** |
| Detail UI split | `ResponseDetailPanel` inline only for **compact** preview-tester; full workspace uses existing modals |
| Statistics toggle | Local state in activity workspace; matrix + exit ticket stats |

---

## 4. Rejected directions

- Do **not** put "Back to preview" back in the main panel.
- Do **not** show spare tester rows on **Students** responses (Testers workspace keeps them).
- Do **not** include Part 1/2/3 completion columns in statistics charts.
- Do **not** use inline bottom detail panel for full Students & responses workspace (regression from layout flex changes).
- Do **not** add attempt-count ranking for matrix tutorial (Chase noted single attempt makes it useless); use **miss-count ranking** instead.
- Do **not** edit the Cursor plan file itself — implement from it.

---

## 5. Current implementation state

### Completed (first layout pass — uncommitted)

| File | Change |
|---|---|
| `TeacherConsoleSidePanel.tsx` | Header flex row + conditional "← Back to preview" |
| `ConsoleActivityWorkspaceScreen.tsx` | Removed back button, heading, unused props |
| `ConsoleManageClassScreen.tsx` | Removed inline back button |
| `TeacherConsoleWorkspaceShell.tsx` | Dropped back/title/courseLabel props |
| `teacher-console.css` | `.teacher-console-side-panel__header-back` |
| `teacher-console-neumorphic.css` | Neumorphic styling for header back |
| `teacher-console-matrix-report.css` | Activity-workspace flex chain + compact rail CSS (~85 lines) |
| `teacher-console-workspaces.css` | `:has(.teacher-console-screen--activity-workspace)` padding tweak |

Chase verified: **layout looks good**; arrows still at top; follow-up items remain.

### Not started (follow-up plan — all todos pending)

1. Arrow `gradebook-filtering-panel__center` wrapper in `MatrixReportScrollFrame.tsx`
2. Green/red cell colors scoped to `--activity-workspace`
3. Modals instead of `ResponseDetailPanel` in full `ActivityResponsesPanel`
4. Remove `TeacherConsoleMatrixGradesPanel` from side panel; collapsible tuning
5. `filterMatrixRowsToStudents` / exit-ticket equivalent
6. `columnKind` on `matrixSlotCatalog.ts` columns
7. `buildActivityResponseStatistics.ts` + tests + `ActivityResponseStatisticsPanel.tsx` + head-row Statistics button

### Git (Macro App)

**Dirty, nothing committed or pushed** for this work. `git status` also shows unrelated dirty
files (`config/d2l-courses.json`, `d2lService.ts`, `slotSessionStore.ts`, etc.) — **commit TC
redesign separately** from machine-local / unrelated changes per `agent docs/rules/multi-repo-git-push.md`.

### Verification

- Typecheck run during first pass — no errors in changed TC files (repo may have pre-existing tsc noise elsewhere).
- **No GUI smoke test** performed by agent — Chase verified layout visually.

---

## 6. Open questions and constraints

1. **Arrow centering** — CSS `align-items: center` on rail may be insufficient; plan uses
   gradebook `__center` absolute positioning exemplar — try that first.
2. **Exit ticket statistics** — completion-only tickets should show empty state, not crash.
3. **Mixed dirty tree** — don't commit `d2l-courses.json` or unrelated service edits with TC work.
4. **Never launch GUI** without asking Chase; hand off visible verification steps.
5. **Modal rule** — modals must not dismiss on backdrop click (root AGENTS.md).
6. **File size** — `teacher-console-workspaces.css` at ~829 lines; add new CSS to
   `teacher-console-matrix-report.css` or new `teacher-console-response-statistics.css`.

---

## 7. Exact next step

**Phase 1 quick fixes first** (single focused pass before statistics):

1. Read follow-up plan: Cursor plan `responses_follow-up_polish` (or this handoff §5 not-started list).
2. Edit `MatrixReportScrollFrame.tsx` — wrap arrow pad in `gradebook-filtering-panel__center`.
3. Add activity-workspace cell color CSS + rail height fixes in `teacher-console-matrix-report.css`.
4. In `ActivityResponsesPanel.tsx` — swap full-mode detail to `MatrixReportDetailModal` /
   `ExitTicketResponseDetailModal`.
5. In `TeacherConsoleSidePanel.tsx` — remove matrix grades panel; wrap tuning in collapsible section.
6. Add student spare filters in `filterTesterRows.ts` + wire in `ActivityResponsesPanel`.

Then **Phase 2–3:** columnKind metadata, statistics util + panel, Statistics button in head row.

---

## Read first (fresh task)

1. This file (`agent docs/momentum-handoffs/latest.md`)
2. Follow-up plan todos (Cursor: `responses_follow-up_polish`)
3. `agent docs/recipes/report-grid-layout.md` — scroll frame / arrow rail exemplar
4. `School Scrips/Macro App/renderer/src/components/teacher-console/MatrixReportScrollFrame.tsx`
5. `School Scrips/Macro App/renderer/src/components/teacher-console/ActivityResponsesPanel.tsx`
6. `School Scrips/Macro App/renderer/src/components/side-panels/teacher-console/TeacherConsoleSidePanel.tsx`
7. `School Scrips/Macro App/renderer/src/utils/matrixReport/matrixSlotCatalog.ts` — Part vs Q columns

**App AGENTS:** `School Scrips/Macro App/AGENTS.md` (keyword: report grid, Teacher Console live preview)
