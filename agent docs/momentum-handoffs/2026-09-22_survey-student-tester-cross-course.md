# Momentum handoff — Survey publish + roster student tester portal view

**Written:** 2026-09-22 (Tuesday, ~6:08 PM)

---

## 1. Objective and current phase

**Active thread:** College-algebra **Math Survey** (exit-ticket / generic quiz) — publish, name it, grant student access, verify **student view** in the portal.

**Phase:** Survey features largely implemented; **student tester still does not see the activated survey** in the portal. Chase corrected the prior agent’s diagnosis (not universal CHASE1 testers). **Next agent should fix or verify cross-course student-tester code / section resolution.**

---

## 2. Chase's desired feel (use his language)

- Surveys get **custom names** (e.g. **Math Survey**), not auto-dated “Exit Ticket — Sep …”. “Exit ticket” is only the **tool category** for quick paste-and-publish.
- After publish, he expects to **grant access** from **Students & responses** (side panel bulk activate; **no** duplicate bulk button on the main roster table — he rejected that).
- **Student Tester** on the **Students** roster (Last **Student**, First **Tester**) is how he checks **what a real student sees** — each course has its **own code**.
- He suspects when he’s on one course tab, the portal may still be using the **M1324 student tester code** for both courses instead of switching to the **current course’s** student tester code.
- App access for Math Survey shows **On** for student tester, but portal does **not** show the survey tile (or shows “Nothing here yet”).

---

## 3. Accepted decisions

| Decision | Why |
|---|---|
| Exit tickets / surveys **opt-in** — default off until teacher activates (migration **055**) | Chase: access should not be automatic; admin preview bypasses filter |
| Custom **Name** field; no auto-date title on parse | Avoid 20 indistinguishable “Exit Ticket — date” entries |
| After publish → navigate to **Students & responses → Roster** with new survey selected | Clear grant-access path |
| Invalidate / sync **section exit ticket cache** after rename/save | App switcher was stale after edit |
| Bulk activate stays in **side panel only** | Duplicate roster button removed per Chase |

---

## 4. Rejected directions

| Rejected | Why |
|---|---|
| Diagnosis: universal **testers** (CHASE1 / Testers tab) need “Assign to course” | **Wrong persona.** Chase uses **Students** roster row **Student Tester**, not universal tester codes |
| Duplicate **Turn on for all** on main roster table | Already in side panel |
| Auto-fill **Exit Ticket — [date]** on parse | Chase wants explicit names like Math Survey |

---

## 5. Current implementation state

### student-session-kit (migrations **untracked**, **055 pushed** via `db:push` this session)

- `053_announcement_update_and_delete.sql` — past announcements update/delete
- `054_quiz_text_questions.sql` — survey mode, short-answer questions
- `055_exit_ticket_opt_in_access.sql` — exit-ticket app access defaults **false**; `set_student_app_access` updated for opt-in

### Macro App (many **uncommitted** files)

**Exit tickets / surveys:**
- `parseQuizPaste.ts`, `ConsoleExitTicketsScreen.tsx`, `useExitTicketAuthoring.ts` — survey toggle, Give to AI, custom names
- `useSectionExitTickets.ts` — cache listeners + `syncSectionExitTicketsCache`
- `useExitTicketQuizEdit.ts` — cache sync on load/save
- `TeacherConsoleWorkspaceShell.tsx` — post-publish navigation to Students roster
- `useRosterAppAccess.ts`, `resolveRosterBulkTargets.ts` — access `=== true` for opt-in
- `ConsoleRosterScreen.tsx` — exit-ticket hint; bulk button **removed**

**Announcements:** past announcements screen, manage class, migrations wired

**Key student-tester code (investigate next):**
- `renderer/src/utils/studentProgress/rosterStudentTester.ts` — `ROSTER-STUDENT-TESTER` org id; Last Student / First Tester
- `renderer/src/utils/studentProgress/portalPreviewPersona.ts` — `findRosterStudentTesterEntry(courseMap)`, `resolvePortalPreviewCode(persona, courseMap)`
- `renderer/src/hooks/teacher-console/useTeacherConsolePreviewPersona.ts` — persists `admin` vs `student` **globally**, not per course tab
- `renderer/src/utils/studentProgress/portalPreviewUrl.ts` — `previewPersona` param forces reload on admin↔student switch; **may not reload on course tab change**
- Student portal: `useStudentIdentity.ts`, `previewContext.ts`, `resolveEffectiveSectionId`, `classworkData.ts` `filterQuizzesByAppAccess`

### student-portal

- Generic quiz text questions, classwork tiles — may need **deploy:prod** if live site tested (not verified this session)

### Verification

- Unit tests run for roster bulk targets, parse quiz paste (session); **no live portal smoke test** with Student Tester after fixes
- **055** pushed to Supabase; Macro App **not committed**

---

## 6. Open questions and constraints

1. **Primary bug (Chase hypothesis):** Per-course **Student Tester** codes — switching Teacher Console course tab while in student-tester preview (or opening portal link) may still sign in / resolve section as **M1324’s** tester instead of **current course’s** tester → wrong section → no Math Survey tile or “Nothing here yet”.
2. **Secondary checks if hypothesis wrong:** Survey published to correct `section_id` for active course tab; `student_app_access` row exists with `enabled=true` for that student id + activity id; classwork localStorage cache stale; activity archived on home screen.
3. **Opt-in access:** Even with correct section, survey hidden until **Activate** (side panel or per-row). Chase says access is **On** — confirm roster row is **Student Tester** for **same course** as published survey.
4. **Do not** re-add roster bulk button. **Do not** conflate with universal testers (Testers workspace / CHASE1).
5. **AGENTS.md:** no GUI without permission; Macro App restart for renderer changes; student-portal deploy separate.

---

## 7. Exact next step

**Reproduce with Chase’s workflow:** Select course tab where Math Survey was published → **Students & responses** → **Students** (not Testers) → confirm **Student Tester** row App access **On** → note **that course’s** portal code → open portal with **that** code (preview or live) → confirm whether section / tiles match.

**Then trace code:** When course tab changes, does preview URL / stored identity switch to `findRosterStudentTesterEntry(currentCourseMap)?.code` and matching `sectionId`? Start with `portalPreviewPersona.ts`, preview URL builder, embedded browser navigation on course tab change, and portal `useStudentIdentity` + `resolveEffectiveSectionId`.

---

## Read first

1. This file
2. `School Scrips/Macro App/AGENTS.md` (keyword: teacher console / student progress)
3. `School Scrips/Macro App/renderer/src/utils/studentProgress/rosterStudentTester.ts`
4. `School Scrips/Macro App/renderer/src/utils/studentProgress/portalPreviewPersona.ts`
5. `School Scrips/student-portal/src/hooks/useStudentIdentity.ts`
6. `School Scrips/student-portal/src/services/classworkData.ts`
