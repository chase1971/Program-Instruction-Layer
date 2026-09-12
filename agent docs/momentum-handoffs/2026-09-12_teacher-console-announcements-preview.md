# Momentum handoff — Teacher Console dashboard, announcements, preview server

**Written 2026-09-12.** Day-valid only: if you are reading this on a later date, say so before acting.

**Slug:** `2026-09-12_teacher-console-announcements-preview`

---

## Read first

1. **`School Scrips/Macro App/AGENTS.md`** — Teacher Console / student progress keywords.
2. **`School Scrips/student-portal/AGENTS.md`** — portal shipping and preview dev port.
3. **`School Scrips/student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md`** — schema + RPC context.
4. **This handoff** — current state and what Chase has not verified yet.

---

## Objective and current phase

**Phase: feature-complete in local/preview; Chase has not fully verified the latest UX.**

Chase wanted the Teacher Console dashboard redesigned to match his mockup, class announcements
(teacher publish, student dismiss/view history), Live vs Preview for the student portal, in-app
preview server start, and sensible launch behavior (last class, dashboard on open).

All of that is implemented in code. Migration **028** was applied to Supabase (`npm run db:push`
ran successfully this session). **Nothing has been committed or pushed to GitHub.**

---

## Chase's desired feel

- **Dashboard is home.** On Macro App launch, Teacher Console opens to the **last selected class's
  dashboard**, not wherever he left off mid-drill-in. While the app stays open, tab switches
  preserve position.
- **Preview is local code; Live is Netlify.** Preview tab = `http://127.0.0.1:5340`. Live tab =
  deployed portal. He should not have to run `npm run dev` manually — Macro App starts the Vite
  server headlessly when he opens Preview.
- **Announcements are teacher-authored, not auto-seeded.** He publishes from Teacher Console →
  Dashboard → Announcements. Students see cards on the portal home; dismiss removes the card.
- **Past announcements belong on their own page**, not a big collapsible on home. After dismiss,
  a **small "Past announcements" link** on home goes to `#/announcements` with dated history.
- **Dwell-friendly UI.** Big click targets; no typing-heavy flows; modals don't dismiss on backdrop
  click (Macro App rules).

---

## Accepted decisions

| Decision | Why |
|---|---|
| Session-only Teacher Console navigation (`useState`, not localStorage) | Launch → dashboard; in-session tab switches keep drill-in position |
| Last course still persisted (`macro-app-student-progress-last-course-code`) | Separate from navigation |
| `previewSection` URL param on preview URLs | Fixes instructor (CHASE1) seeing wrong section's announcements |
| `student-portal-host.js` spawns Vite on port **5340** | Matches `student-portal/vite.config.ts`; reuses external server if already running |
| Past announcements page at `#/announcements` | Replaces home collapsible; grouped by publish date like classwork |
| Migration **028** adds `p_section_id` to `dismiss_announcement` | Fixes "Announcement not found" when dismissing during instructor preview |
| Migrations **026–028** applied via `db:push` | 028 confirmed applied this session |

---

## Rejected / superseded

- **Persisting Teacher Console drill-in across launches** — removed; Chase wanted dashboard on open.
- **Collapsible "Past announcements" on portal home** — replaced by tiny link + dedicated page.
- **Telling Chase to "apply the migration" himself** — he asked the agent to run `db:push`; that is done.

---

## Current implementation state

### student-session-kit (schema — **pushed to Supabase, not committed**)

| Migration | Purpose |
|---|---|
| `026_class_announcements.sql` | Tables + RPCs: publish/unpublish/list/dismiss |
| `027_announcements_preview_section.sql` | `p_section_id` on `list_student_announcements` |
| `028_dismiss_announcement_preview_section.sql` | `p_section_id` on `dismiss_announcement` — **live on remote** |

### student-portal (**uncommitted**)

- `ClassAnnouncementCard.tsx`, `StudentAnnouncementsPanel.tsx` — active cards + past link on home
- `PastAnnouncementsView.tsx` — `#/announcements` dated history + Back to home
- `useStudentAnnouncements.ts`, `announcementService.ts` — RPC calls + date formatting
- `App.tsx` + `usePortalRoute.ts` — `ANNOUNCEMENTS_ROUTE`
- `MatrixHomeView.tsx` — wires announcements above classwork tiles

### Macro App (**uncommitted**)

**Dashboard redesign**

- `ConsoleDashboardScreen.tsx`, `teacher-console-dashboard.css`
- `dashboard/DashboardSectionCard.tsx`, `DashboardLoginsPreview.tsx`, `DashboardAnnouncementsPanel.tsx`

**Announcements (teacher side)**

- IPC in `student-progress-io.js` — list/publish/unpublish/resolve-section
- `useSectionAnnouncements.ts`, service + types in `studentProgressService.ts` / `macroAppStudentProgress.d.ts`

**Live / Preview**

- `portalPreviewUrl.ts` — Live = Netlify, Preview = `127.0.0.1:5340`, `previewSection` param
- `useTeacherConsolePortalPreview.ts`, `TeacherConsoleAppPanel.tsx` — Live / Preview / Grades / Roster nav
- `student-portal-host.js` — start/stop/status IPC; registered in `main.js`; stops on app quit
- `useStudentPortalDevServer.ts` — auto-start on Preview tab + side panel controls

**Navigation**

- `useTeacherConsoleNavigation.ts` — session-only view state (dashboard default each launch)

### Verification done this session

- `student-portal-host.js` syntax check passed
- Integration test: detected already-running server on 5340
- `npm run db:push` — migration 028 applied successfully
- student-portal type-check has pre-existing `supabase` possibly-null warnings (not introduced here)

### Not verified by Chase

- Dismiss announcement → past link → past page flow in Preview after restart
- In-app preview server auto-start from Macro App Preview tab
- Dashboard mockup match to his eye
- Live tab (Netlify) still won't show new announcement UI until portal is deployed

---

## Open questions and constraints

1. **Netlify deploy** — Live tab uses deployed portal; preview/local changes need `deploy:prod` in
   student-portal when Chase wants Live to match (see student-portal AGENTS.md).
2. **Macro App restart** required after electron/preload changes (preview server IPC).
3. **Preview server restart** — Chase said he can restart; after code changes, reload Preview tab.
4. **Git** — three repos dirty; no commit this session unless Chase asks or end-of-session protocol.
5. **config/d2l-courses.json** in Macro App is machine-local dirty — do not commit.

---

## Exact next step

**Verify the announcement dismiss + past-announcements flow in Macro App Preview:**

1. Restart Macro App (electron changes).
2. Teacher Console → pick class → open an app → **Preview** tab (server should auto-start).
3. Dismiss the class announcement → home should show **Past announcements** link (no red error).
4. Click link → `#/announcements` shows dismissed message with date → **Back to home** works.

If anything fails, check browser console + Macro App module logs for `student-progress` / `student-portal-dev`.

**After verification passes:** Chase may want end-of-session protocol to commit/push all three repos
(Macro App, student-portal, student-session-kit migrations).

---

## Key file paths (quick grep targets)

```
Macro App/electron-app/student-portal-host.js
Macro App/renderer/src/hooks/teacher-console/useTeacherConsoleNavigation.ts
Macro App/renderer/src/hooks/teacher-console/useStudentPortalDevServer.ts
Macro App/renderer/src/components/teacher-console/dashboard/DashboardAnnouncementsPanel.tsx
student-portal/src/app/components/PastAnnouncementsView.tsx
student-portal/src/app/components/StudentAnnouncementsPanel.tsx
student-session-kit/supabase/migrations/026_class_announcements.sql
student-session-kit/supabase/migrations/028_dismiss_announcement_preview_section.sql
```
