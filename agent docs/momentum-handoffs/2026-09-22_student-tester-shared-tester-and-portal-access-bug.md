# Momentum handoff — Student Tester → shared multi-section tester + real portal-access bug

**Written:** 2026-09-22 (Tuesday, ~9:02 PM)

**Supersedes:** `2026-09-22_survey-student-tester-cross-course.md` (earlier today). That file's
diagnosis is now **stale/reversed** — see §4.

---

## 1. Objective and current phase

**Active thread:** Math Survey (exit-ticket) still not visible to **Student Tester** in the
student portal, despite app access being On and the course being assigned.

**Phase:** Two separate problems found and fixed this session:

1. **Student Tester migrated** from a per-course Students-roster row (two different codes,
   one per class) to a **shared multi-section tester** — same mechanism as Chris/Kristy/CHASE1.
   Lives in **Testers**, one code (`W8K2P4`) everywhere, **Assign to course / Remove from
   course**, follows the active Teacher Console course tab.
2. **Real, independent production bug found**: `student-portal/src/config/portalAccess.ts` had
   a **stale, nonexistent** section UUID for MATH-1314, so the *entire portal* — not just
   Student Tester, not just Transformations — has been showing "Nothing here yet" for anyone
   resolving to the M1314 section since the Sep 17 commit that introduced it. Fixed in code,
   build verified clean, **not yet deployed** — Chase chose to verify in Preview mode first.

**Current blocker:** Chase has not yet confirmed either fix works live. Waiting on him to
restart Macro App and test in Preview mode (Live mode still runs the old, un-deployed code and
still has the stale-UUID bug).

---

## 2. Chase's desired feel (use his language)

- Testers should work exactly like Chris/Kristy/CHASE1: **one shared code**, **Assign to
  course / Remove from course**, **one class at a time**, and it should **follow him** —
  "when I click on testing mode for a student, it'll know what class it's associated with."
- He does not want Student Tester on the Students roster anymore — "remove it from the student
  section" — Testers only.
- On the real bug: even though it's a live-affecting bug hitting real students, he explicitly
  chose **not** to deploy immediately — wants Preview-mode confirmation first. Don't deploy
  without him saying so again, even though the bug is serious.

---

## 3. Accepted decisions

| Decision | Why |
|---|---|
| Student Tester is now `SHARED_MULTI_SECTION_TESTERS` entry — id `b8c3e1a2-4f5d-6e7f-8a9b-0c1d2e3f4a5b`, code `W8K2P4`, label "Student Tester" | Matches Chris/Kristy pattern Chase asked for |
| Legacy roster Student Tester (`ROSTER-STUDENT-TESTER` org id, codes `THERKM`/`4VGKJ7`) retired — stripped from Drive `student-portal-codes.json`, DB rows set `active=false` | Old per-course mechanism replaced |
| `resolveEffectiveSectionId(claimSectionId, serverPreviewSectionId, multiSectionTester)` — new 3rd param honors URL `previewSection` for **any shared multi-section tester**, not just instructors | Student persona needs the same course-follow behavior as admin persona |
| `buildPortalAppPreviewUrl` always passes `previewSectionId` (no longer omitted for student persona) | Shared tester needs section context in the embedded preview URL |
| `RosterStudentActions` / `PreviewTesterCard`: Activate/Deactivate app-access buttons **always shown**, even when the tester isn't assigned to the active course tab ("courseAssignOnly" gray row) | Was incorrectly hidden — app access is global per tester, not per course membership |
| `useMacroAppStudentProgressShell`'s `rosterStudentIds` now includes all `buildUniversalTesterRows(...)` ids | App-access state wasn't loading for shared testers at all |
| `sync-portal-rosters.mjs`: shared testers get **inactive** membership rows per map (`ensureInactiveMembership`), not active upserts | DB has a unique-active-per-student constraint (`student_section_memberships_one_active_per_student`) — only one course can be active at a time, set via `grant_student_membership` / Assign button, not the sync script |
| **Root-cause fix:** `TRANSFORMATIONS_ENABLED_SECTION_IDS` in `portalAccess.ts` corrected from stale `e02887a8-9670-4939-bb9d-01be4de5d5f9` (matches **zero** rows in `sections`) to the real current M1314 id `14ab6eb2-f6b5-406e-bd57-8471a598401e` | This gate runs **before** classwork/exit-ticket rendering in `App.tsx` (`if (!portalAccess) { PortalNoAccess }`) — wrong id blocks the *whole* portal, explains "Nothing here yet" independent of Student Tester |
| Do **not** run `npm run deploy:prod` (student-portal) without Chase explicitly asking again | He picked "Preview only" when asked; the deploy script itself says "ONLY run when Chase explicitly asks" |

---

## 4. Rejected / superseded directions

| Rejected/superseded | Why |
|---|---|
| Per-course roster-based "Student Tester" (Students roster, Last Student/First Tester, one code per course) | Chase explicitly asked to replace this with the shared-tester mechanism this session — **do not recreate it** |
| Earlier handoff's framing that "universal CHASE1-style testers is the wrong persona for Student Tester" | **Reversed.** Chase later asked for exactly that mechanism. If you read the older dated handoff, ignore that specific conclusion |

---

## 5. Current implementation state

**All three repos have uncommitted changes.** Not all of it is from this thread — some
(portal-link email templates, exit-ticket opt-in access, announcements CRUD, generic-quiz text
questions) predates this specific Student Tester investigation. Don't assume every dirty file
belongs to this handoff's topic.

### Macro App (uncommitted — see `git status --short` for full list, ~60 files)

Directly relevant to this thread:
- `electron-app/shared-multi-section-testers.js` + `renderer/src/utils/studentProgress/sharedMultiSectionTesters.ts` — added Student Tester entry
- `renderer/src/utils/studentProgress/portalPreviewPersona.ts` — rewritten around `STUDENT_TESTER_SHARED`, no more roster-map lookup
- `renderer/src/utils/studentProgress/portalPreviewUrl.ts` — `previewSection` no longer omitted for student persona
- `renderer/src/components/teacher-console/screens/ConsoleRosterScreen.tsx`, `renderer/src/utils/studentProgress/resolveRosterBulkTargets.ts` — filter legacy roster tester out of Students list/bulk actions via `isRosterStudentTester`
- `renderer/src/components/teacher-console/RosterStudentActions.tsx`, `PreviewTesterCard.tsx` — Activate/Deactivate always rendered
- `renderer/src/hooks/shell/useMacroAppStudentProgressShell.ts` — `rosterStudentIds` includes universal tester ids
- Tests updated and passing: `portalPreviewPersona.test.ts` (rewritten), `portalPreviewUrl.test.ts`

### student-portal (uncommitted)

- **`src/config/portalAccess.ts` — the real fix.** `TRANSFORMATIONS_ENABLED_SECTION_IDS` corrected.
- `src/hooks/useStudentIdentity.ts` — added `multiSectionTester` to `StudentIdentityState`
- `src/services/announcementService.ts` — `resolveEffectiveSectionId` 3rd param
- `src/app/App.tsx`, `src/app/components/MatrixHomeView.tsx` — thread `multiSectionTester` through
- `src/services/previewTeacherConsole.ts` (new, from earlier in session — TC preview persona/course sync, not new today but still uncommitted)
- Tests passing: `announcementService.test.ts`, `portalAccess`-related tests (unaffected by the id swap, don't hardcode old id)
- `npm run build` succeeds clean (only pre-existing chunk-size warnings)
- **Not deployed.** Netlify Live still runs old code + the stale-UUID bug.

### student-session-kit (uncommitted)

- `scripts/sync-portal-rosters.mjs` — upserts shared testers (skips legacy roster-tester rows via `isRosterStudentTester`), inserts inactive memberships, explicitly upserts Student Tester even with no map membership
- Ran `npm run sync-portal-rosters` successfully — Student Tester now in Supabase, `multi_section_tester=true`, `section_id=null`
- One-off Node scripts run directly (not saved as files):
  - Checked for enabled `student_app_access` rows on legacy tester ids to migrate — found **0** (nothing needed copying)
  - Set `students.active=false` for legacy tester ids `8f91c144-...` (was M1314 code `THERKM`) and `b11fa085-...` (was M1324 code `4VGKJ7`)
  - Stripped legacy `ROSTER-STUDENT-TESTER` entries from both Drive `student-portal-codes.json` files — **not tracked in git**, no diff trail beyond this handoff
- Migrations `053_announcement_update_and_delete.sql`, `054_quiz_text_questions.sql` untracked, push status not reconfirmed this session (055 confirmed pushed in an earlier handoff)

### Verification performed (Supabase queries, this session)

- Student Tester row: `multi_section_tester=true`, `preview_section_id=14ab6eb2` (M1314), active membership on `14ab6eb2`, `student_app_access` enabled=true for `exit-ticket/aac49df9-fa8d-4037-b404-0495a2ac1d00` ("Math Survey")
- `activities` row for Math Survey: `published=true`, `section_id=14ab6eb2` — matches Student Tester's assigned course
- `sections` table has exactly 2 rows: M1314 = `14ab6eb2-f6b5-406e-bd57-8471a598401e`, M1324 = `956144f1-49be-42d6-be6b-dc46cb6845ad`
- Old `TRANSFORMATIONS_ENABLED_SECTION_IDS` value `e02887a8-9670-4939-bb9d-01be4de5d5f9` matches **zero** rows anywhere in `sections` — confirmed genuinely stale, introduced in commit `a96d669` ("Embed transformations identifying and graphing for M1314…", Sep 17)
- All DB state for Student Tester is internally consistent — the remaining blocker is purely code/deploy, not data

---

## 6. Open questions and constraints

1. **Macro App restart not yet confirmed.** Renderer + electron-app changes require a restart.
2. **Portal mode toggle defaults to Live** (`usePersistedState<PortalPreviewSource>(STORAGE_KEY, 'live')`). Chase must switch to **Preview** and hit the preview refresh button — this auto-starts the student-portal dev server on `127.0.0.1:5340` (`portalDevServer.startServer()`). Without this, none of today's code changes are visible, only the DB state (which is already correct).
3. **Do not deploy** `student-portal` (`npm run deploy:prod`) without Chase explicitly asking again — he picked Preview-first. Real M1314 students on the Live site are still hitting the stale-UUID bug until this ships; flag it, don't silently deploy.
4. **`useTeacherConsolePhonePreviewSection` pushes the ACTIVE TC course tab's section** to whichever student matches the current `previewPersona`'s code — this happens continuously while Teacher Console is open, independent of the Testers-screen "Assign to course" button. Reasoned through this session (it can't corrupt state because `set_preview_section` RPC raises before writing if there's no active membership for that section) but **not explicitly end-to-end tested**. If Student Tester's survey visibility flips depending on which TC course tab is active, start here.
5. Large uncommitted diff spans unrelated earlier work (portal-link email templates, exit-ticket opt-in access, announcements CRUD) — don't scope a commit to "everything dirty" without checking what's actually done vs. mid-flight.

---

## 7. Exact next step

Wait for Chase's test result from Preview mode (already told him: restart Macro App → switch
Portal mode to Preview on the M1314 tab → refresh → check Student Tester persona).

- **If Math Survey now shows:** ask Chase if he wants to deploy `student-portal` (`npm run
  deploy:prod`) now — this ships both the real students-affecting fix and the Student Tester
  feature together. Don't deploy without an explicit yes.
- **If it still doesn't show:** check `portalDevServer.isRunning`/`isReady` state actually
  flipped true, then re-check whether Chase was on the **M1314 tab** specifically when testing
  (see §6.4) — a mismatched active tab could push the tester's preview section to M1324 instead.

---

## Read first

1. This file
2. `School Scrips/student-portal/src/config/portalAccess.ts` (the real fix)
3. `School Scrips/Macro App/renderer/src/utils/studentProgress/sharedMultiSectionTesters.ts`
4. `School Scrips/Macro App/renderer/src/utils/studentProgress/portalPreviewPersona.ts`
5. `School Scrips/Macro App/renderer/src/hooks/teacher-console/useTeacherConsolePhonePreviewSection.ts`
6. `School Scrips/student-portal/src/hooks/useStudentIdentity.ts`
7. `School Scrips/student-portal/src/services/classworkData.ts`

---

## Copy-ready fresh-task prompt

See agent reply — same text as §7 wrapped in a paste block.
