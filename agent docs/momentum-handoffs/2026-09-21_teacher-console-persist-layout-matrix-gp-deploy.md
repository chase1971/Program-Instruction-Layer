# Momentum handoff — Matrix GP deploy + Teacher Console persistence/layout

**Written:** 2026-09-21 (Monday, ~8:20 PM)

---

## 1. Objective and current phase

**Active thread (this chat):** Two deliverable tracks:

1. **Matrix guided practice (student portal)** — crash fix, Enter/submit flow, R1/R2 typing, help triggers, cell font scaling → **committed, pushed, Netlify production deployed.**
2. **Teacher Console Students & responses** — remember last app + Roster/Responses tab + workspace; stop Practice archive / Statistics from shifting header tabs → **implemented, unit tests green, NOT live-smoke-tested, NOT committed.**

**Phase:** Teacher Console work is code-complete pending Chase verification in Macro App. Macro App repo has **additional uncommitted changes** beyond the persistence/layout patch (GP completion dots, preview console error forwarding — see §5).

**Prior handoff (2026-09-20)** covered GP post-survey + page error button polish (Submit button layout on survey step 4). That thread may still have dirty files in Macro App / student-portal from before this chat — do not assume everything on disk is from §5 only.

---

## 2. Chase's desired feel (use his language)

### Teacher Console (latest ask)
- **Remember** which **app** he had selected, whether **Roster** or **Responses** was active, and which workspace (**Students** vs **Testers** vs **Preview**) when he reopens.
- **Roster / Responses tabs stay top right always** — switching to Responses and showing **Practice archive** or **Statistics** must **not** push those tabs down. Extra buttons sit beside them, not in a separate grid row that shifts layout.
- Side panel **Students & responses** should reopen to his **last tab**, not always Responses.

### Matrix guided practice (shipped this chat)
- **Enter:** consistent two-step — first Enter commits/closes builder; second Enter or Submit submits (row entry + row notation).
- **R1/R2:** keyboard types R and digit separately; **button** R1/R2 still deletes as one unit on backspace.
- **Help:** `Need help with [topic]? Click or tap here.` — icon and label both tappable; space after `?`.
- **Cells:** 6+ character values shrink font so they don't overflow.
- **Rejected:** full-width expanded Submit on number pad (phone app, not dwell UI).

### Standing constraints
- No surprise windows — ask before launching Macro App GUI.
- Modals never dismiss on backdrop click.
- `config/d2l-courses.json` is machine-local — **never commit**.

---

## 3. Accepted decisions (do not re-litigate)

| Decision | Why |
|---|---|
| Workspace persistence via `usePersistedState` (ADR-001 exemplar: `useTeacherConsolePreviewActivityIndex`) | Matches existing preview app index pattern |
| Keys: `macro-app-teacher-console-workspace-activity-index:{course}` and `macro-app-teacher-console-workspace-view:{course}` | Per-course, like preview index |
| Persist `{ kind, panel }` for preview / students / testers only | Manage screens do not overwrite last workspace snapshot |
| `openStudents()` / `openTesters()` with no arg restore last panel for that audience | Side panel was hardcoding `'responses'` — fixed in `AppSidePanel.tsx` |
| Header layout: `__toolbar` flex row — `[stats toggle?] [Roster] [Responses]` right-aligned | Replaces 3-column `--with-stats` grid that shifted tabs |
| Matrix GP + portal embed fixes deployed to **https://mathappsclass.netlify.app** (deploy #36) | Chase asked deploy everything for session work |

---

## 4. Rejected directions

| Rejected | Why |
|---|---|
| 3-column grid `__head--with-stats` for statistics/archive toggle | Pushed Roster/Responses down when Responses active |
| Reset workspace activity index to 0 on every course change | Replaced with persisted index per course |
| Auto-submit on first Enter for row entry / notation | Chase wanted two-step flow matching each other |
| Full-width Submit on builder number pad | Wrong interaction model for dwell UI |

---

## 5. Current implementation state

### Shipped — Matrix app (`School Scrips/Matrix app`)
- **Git:** clean (committed `fe8f950`, pushed).
- Key files: `GuidedPracticeSolver.tsx`, `guided-practice-builder-commit.ts`, `use-guided-practice-session-submit.ts`, `use-builder-keyboard.ts`, `GuidedPracticeHelpTrigger.tsx`, `matrixCellButtonClasses.ts`, tests.
- **141 tests** passing at deploy time.

### Shipped — student-portal embed
- **Git:** only `docs/netlify-deploy-counter.json` dirty locally (counter bump from deploy).
- Commit `d3b542b` pushed; production Netlify deploy succeeded.

### Teacher Console persistence + layout — **uncommitted, needs smoke test**

| File | Change |
|---|---|
| `renderer/src/hooks/teacher-console/useTeacherConsoleWorkspacePersistence.ts` | **New** — read/write view + activity index |
| `renderer/src/hooks/teacher-console/useTeacherConsoleWorkspacePersistence.test.ts` | **New** — storage key test |
| `renderer/src/hooks/teacher-console/useTeacherConsoleNavigation.ts` | Restore/persist view; workspace activity index hook |
| `renderer/src/components/teacher-console/screens/ConsoleActivityWorkspaceScreen.tsx` | `__toolbar` wrapper; removed `--with-stats` head class |
| `renderer/src/components/shell/AppSidePanel.tsx` | `openStudents()` / `openTesters()` without forced panel |
| `renderer/src/styles/teacher-console-workspaces.css` | `__toolbar` styles; head grid 2-col |
| `renderer/src/styles/teacher-console-response-statistics.css` | Removed `--with-stats` grid rules |

**Tests run:** `npm test -- useTeacherConsoleWorkspacePersistence` — pass (renderer).

**Not tested:** Live Macro App — tabs stay top-right on Responses; persistence survives close/reopen and course switch.

### Other uncommitted Macro App work on disk (same repo — verify before commit)

These were **not** part of the persistence/layout patch; may be from earlier session work:

- `guidedPracticeCompletionReport.ts` (+ test) — GP Problem 1/2/Survey completion dots in Responses
- `electron-app/browser-slot-console-forward.js` (+ test) — forward portal preview console to log
- `TeacherConsolePreviewConsoleErrorsPanel.tsx`, `portalPreviewConsoleErrorDisplay.ts` (+ test)
- `TeacherConsolePreviewAdminTools.tsx`, `TeacherConsoleSidePanel.tsx`, `ConsolePreviewWorkspaceScreen.tsx`, `TeacherConsolePortalPreviewEmbed.tsx`
- `StatusLogBox.tsx`, `buttons-status.css`, `teacher-console.css`
- `config/d2l-courses.json` — **do not commit**

---

## 6. Open questions and constraints

- **Live smoke:** Chase has not confirmed Teacher Console persistence/layout in running Macro App — **exact next step** is hand him a verification checklist (do not launch without permission).
- **Optional (not requested):** persist Practice archive / Statistics toggle open state.
- **File size:** `teacher-console-workspaces.css` is large (~1070+ lines) — extract before adding more (SESSIONS.md flag).
- **Session scorecard bump** failed (`collectIndexFailures is not a function` in `session-tracking-html.js`) — not blocking handoff.
- **No commit/push/deploy** unless Chase asks ("put on GitHub" / end-of-session).
- Read root `AGENTS.md`, `School Scrips/Macro App/AGENTS.md`, `cursor-patterns/CODING_STANDARDS.md`.

---

## 7. Exact next step

1. Read this file, then **`ConsoleActivityWorkspaceScreen.tsx`** and **`useTeacherConsoleWorkspacePersistence.ts`** to confirm layout + persistence match §3.
2. **Hand Chase a smoke checklist** (no auto-launch): Macro App → Teacher Console → Students & responses → pick app → Roster → close/reopen → same app + tab; switch Responses → Practice archive/Statistics visible **without** tabs moving down.
3. If smoke passes and Chase wants sync: commit Teacher Console persistence/layout files (§5 table) — **separately** from other dirty Macro App work unless he wants one bundle.
4. If smoke fails: fix layout (toolbar CSS) or persistence (localStorage keys / `isActive` restore timing in `useTeacherConsoleNavigation.ts`).

---

## Read first (fresh agent)

1. This file (`agent docs/momentum-handoffs/latest.md`)
2. Root `AGENTS.md` (never display without permission, modal rules, multi-repo git)
3. `School Scrips/Macro App/AGENTS.md`
4. `useTeacherConsoleNavigation.ts`, `useTeacherConsoleWorkspacePersistence.ts`, `ConsoleActivityWorkspaceScreen.tsx`
5. `teacher-console-workspaces.css`, `teacher-console-response-statistics.css` (toolbar section)

---

## Verification Chase should run (when ready)

- Teacher Console → **Students & responses**
- Select a non-default app in switcher → **Roster** → quit Macro App or switch module → return → same app + Roster
- **Responses** → confirm **Practice archive** (guided practice) or **Statistics** (other apps) sits **left of** Roster/Responses; tabs **stay top right**
- Side panel **Students & responses** after using **Roster** should not force **Responses**
