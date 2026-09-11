# Momentum handoff — 2026-09-11 — Per-app roster access (Supabase + wiring)

> **Written:** 2026-09-11 · **Topic:** Teacher Console roster **Deactivate/Activate** = toggle **this app only**, not portal code kill

## Objective and current phase

Wire **per-student, per-activity app access** so when Chase is in **Gauss-Jordan Method → Roster**, **Deactivate** hides Matrix for that student on the portal while their **sign-in code stays valid**. **Activate** turns the app back on. **Reset** clears attempts only (unchanged).

**Phase:** Supabase migration **written, not yet pushed**. Macro App roster UI **safe-stubbed** (no more `revoke_student_code`). Portal + IPC + roster toggle wiring **not started**.

## Chase's desired feel

- **Deactivate ≠ revoke code** — student can still open the portal; only **the app you're viewing in Teacher Console** goes off for them.
- **Activate ↔ Deactivate toggle** — not a one-way delete; button flips after each action.
- **Bulk:** "Turn off {app name} for all" in the side panel — same semantics, whole roster at once.
- **Tester spares (Chris/Christy)** — all-apps access; no per-app deactivate on spares (Copy link only).
- **Dwell-friendly** roster table — compact Last/First/Code/App access/Actions; side panel for bulk actions.
- **No student-facing fix flows** — instructor toggles access; students just see the app gone or back.

## Accepted decisions

| Decision | Why |
|---|---|
| **`student_app_access` table** — sparse rows, only when disabled | No row = enabled (existing students unchanged after migration) |
| **`set_student_app_access`** — `enabled=true` deletes row | Keeps table small |
| **`student_has_app_access`** — anon RPC for portal | No direct table access for anon key |
| Activity id for Matrix = **`matrix/gauss-jordan`** | Matches `010_matrix_tutorial.sql` and `matrixSlotCatalog.ts` |
| **`revoke_student_code` stays** for spare-code rotation | Separate from roster Deactivate; do not call it from roster Deactivate |
| Roster **App access** column (not "code status") | Shows On/Off for **this app** |

## Rejected directions

| Rejected | Why |
|---|---|
| Roster Deactivate calling **`revoke_student_code`** | Deletes student row — kills portal sign-in entirely |
| Section-wide **`students.active`** flag for this feature | Turns off everything, not one app |
| Local-only `revokedStudentIds` UI state | Not persisted; lied about real access |
| Re-activate via "re-run portal SQL" | Wrong UX; must be a toggle |

## Current implementation state

### student-session-kit (new, uncommitted, **not pushed to Supabase**)

| File | Status |
|---|---|
| `supabase/migrations/013_student_app_access.sql` | **NEW** — table + 4 RPCs (see below) |

**RPCs in 013:**

| Function | Caller | Purpose |
|---|---|---|
| `student_has_app_access(student_id, activity_id)` | Portal (anon) | `true` when no row or row enabled |
| `set_student_app_access(student_id, activity_id, enabled)` | Macro App (service role) | Per-row toggle |
| `set_students_app_access(student_ids[], activity_id, enabled)` | Macro App | Bulk deactivate/activate all |
| `list_student_app_access(activity_id, student_ids[])` | Macro App | Roster load — map id → enabled |

**First step for fresh agent:** from `student-session-kit`, run `npm run db:push` (or paste SQL in Supabase editor). Confirm 013 applied before wiring callers.

### Macro App (dirty, uncommitted)

| Area | Files | Status |
|---|---|---|
| Roster UI safe-stub | `RosterStudentActions.tsx`, `ConsoleRosterScreen.tsx`, `TeacherConsoleRosterPanel.tsx` | Deactivate/Activate **disabled**; tooltips say not wired; **no revoke calls** |
| App title passed to roster | `TeacherConsoleWorkspace.tsx`, `TeacherConsoleAppPanel.tsx` | Done |
| Activity id constant | `utils/matrixReport/matrixSlotCatalog.ts` → `MATRIX_TUTORIAL_ACTIVITY_ID` | Use for Matrix |
| Revoke still exists | `student-progress-io.js`, `RosterSpareRevokeButton.tsx` | For spare rotation only — **not** roster Deactivate |

**Still to wire (Macro App):**

1. `electron-app/student-progress-io.js` — `listStudentAppAccess`, `setStudentAppAccess`, `setStudentsAppAccess` RPC wrappers + IPC handlers
2. `preload.js` + `macroApp.d.ts` + `studentProgressService.ts` — expose to renderer
3. `resolveTeacherConsoleActivityId(appId)` — map `matrix` → `matrix/gauss-jordan` (mirror `resolveTeacherConsoleAppTitle`)
4. Hook `useRosterAppAccess(activityId, studentIds)` — load on roster open, refresh after toggle
5. **`RosterStudentActions`** — call `setStudentAppAccess`; toggle Deactivate ↔ Activate
6. **`TeacherConsoleRosterPanel`** — wire "Turn off {appTitle} for all" via `setStudentsAppAccess`
7. **`ConsoleRosterScreen`** — read real `enabled` from hook, not hardcoded `On`

### student-portal (not started)

1. Service: `checkStudentAppAccess(studentId, activityId)` → RPC `student_has_app_access`
2. **`App.tsx`** — before Matrix routes, if `!hasAccess` show blocked state (reuse or extend `PortalNoAccess`)
3. **`MatrixHomeView`** — hide Matrix entry if disabled (if home shows app tile)
4. Optional: re-check on route change

Read first: `student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md` § privacy + § where the doors are.

### Teacher Console context (prior session, still valid)

- Dashboard-first nav, matrix grades in main area, tuning in side panel
- Side panel header: Back (← Grades from Roster), Home (house)
- Matrix report header row height tuning works (`categoryRowPaddingY`)

## Open questions

| Question | Default if Chase doesn't answer |
|---|---|
| Disabled student already **in** Matrix mid-session | Block on next navigation / refresh (check RPC at route entry) — don't kill in-flight attempt mid-step unless easy |
| **Spares** (Chris/Christy) | No per-app toggle in UI — bypass or all-apps (PORTAL_BYPASS_CODES) |
| Exit tickets later | Same `student_app_access` pattern with exit-ticket `activity_id` |

## Constraints

- **No PII in Supabase** — access table is ids + activity_id only
- **Do not use `revoke_student_code` for roster Deactivate**
- PowerShell: no `&&`
- Don't launch GUI without asking Chase
- Migration must be **pushed** before portal/Macro App calls will work

## Exact next step

1. **Push migration 013** (`student-session-kit`: `npm run db:push`).
2. **Macro App IPC** — add the three RPC wrappers in `student-progress-io.js` following `resetStudentAttempts` pattern.
3. **Wire `RosterStudentActions`** — one student toggle end-to-end; verify in Supabase table row appears/disappears.
4. Then portal `student_has_app_access` check so a deactivated student can't open Matrix.

## Verification checklist (when wired)

- [ ] Deactivate one student → row in `student_app_access` with `enabled=false`
- [ ] Activate same student → row deleted
- [ ] Student portal: deactivated student sees no Matrix (or blocked message); code still signs in
- [ ] Reset progress still works when app access On
- [ ] Bulk "Turn off for all" sets all roster ids
- [ ] `npm run build` passes in Macro App + student-portal

## Read first (fresh task)

1. This file
2. `School Scrips/student-session-kit/supabase/migrations/013_student_app_access.sql`
3. `School Scrips/student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md`
4. Macro App exemplars: `011`/`012` migrations usage in `electron-app/student-progress-io.js`; roster UI in `RosterStudentActions.tsx`, `ConsoleRosterScreen.tsx`, `TeacherConsoleRosterPanel.tsx`
