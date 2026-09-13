# Momentum handoff — CHASE1 grades missing + portal polish

**Written:** 2026-09-13 (Sunday)

---

## Objective and current phase

Chase is finishing the Matrix Gauss-Jordan tutorial for M1324 pilot: landscape phone UX, Teacher Console admin preview tools, auto-solve fix, and teacher-grade visibility. **Current phase:** portal/Macro App changes are built locally; one production Netlify deploy happened earlier today (deploy #16). **Next priority:** investigate why **CHASE1 completed the full tutorial (Auto Solve unlocked) but the Matrix grades report shows nothing** for that row.

---

## Chase's desired feel

- Status messages belong in the **navy header, red, centered** — never in the light-blue footer tile inside the assignment.
- Misleading copy is unacceptable: if a save cannot retry, tell the student **what to do** (close other sessions, go back, reopen).
- Skip-gated tutorial testing: instructor on phone (admin link) should skip part gates **without** needing Teacher Console URL hacks; TC preview toggle Off should still simulate the real student path (`previewSkipGated=0`).
- Teacher Console Matrix **Grades** needs a **Refresh grades** control (added locally).
- Chase uses phone + Teacher Console preview **at the same time** to compare spots — expect session overlap, not "bad mobile Wi‑Fi."

---

## Accepted decisions

| Decision | Why |
|---|---|
| Fullscreen button — phones only, landscape, in quiz header | Hides mobile URL bar; hidden on desktop (fine pointer) |
| Admin preview skip-gated via URL + instructor check | Students cannot bypass gates with a query param |
| Instructor phone (no `previewSkipGated` param) **defaults to skip gates** | Admin link should not force full tutorial every time |
| TC preview sends `previewSkipGated=1` or `=0` explicitly | Toggle Off must mean real gated path |
| Auto-solve fix: mid-animation Next finishes current step only | Prevents matrix jumping two operations ahead |
| Save status: `retrying` vs `blocked` with different student messages | "Trying again" only when retries are actually happening |
| Matrix grades side panel: Refresh + auto-refresh on Grades tab | Stale Supabase cache was plausible; Chase asked for it |

---

## Rejected directions

- **Do not** reintroduce Part 3 fraction-answer template (reverted intentionally).
- **Do not** treat save failures as mobile connectivity by default when TC preview + phone are open together.
- **Do not** assume empty grades = wrong student row — Chase confirms **CHASE1**, not student tester, full completion, Auto Solve unlocked, **still empty**.
- **Do not** deploy or commit unless Chase asks (handoff boundary).

---

## Current implementation state

### Deployed to production (Netlify, earlier session)

- Auto-solve checkpoint fix (via Matrix source at build time)
- Fullscreen button, tutorial-complete copy, previewAdminTools URL support (skip-gated **only** with param at deploy time — instructor phone default skip **not** deployed yet)
- Part 1–3 portal CSS from prior commit

### student-portal — uncommitted

- `PortalQuizHeaderCenter.tsx` — red header status (not blue footer)
- `useDocumentFullscreen.ts`, `MatrixTutorialFullscreenButton.tsx`
- `previewAdminTools.ts` — instructor phone default skip; `previewSkipGated=0/1` semantics
- `studentMessages.ts` — `SAVE_BLOCKED_MESSAGE`; save states `retrying` / `blocked`
- `useResumableAttempt.ts` — blocked vs retrying
- `matrixTutorialLandscape.ts` — touch device check for fullscreen
- `matrixTutorialActivity.ts` — em dash removed from complete copy
- `MatrixTutorialView.tsx` — header status, fullscreen, skip-gated wiring

### Macro App — uncommitted

- Teacher Console admin tools (skip gated toggle, reset progress) — preview only
- `TeacherConsoleAppPanel.tsx` — **Refresh grades** + auto-refresh on Grades tab
- `portalPreviewUrl.ts` — always sets `previewSkipGated=0|1`
- Wired through shell, side panel, preview embed, refresh

### Matrix app — uncommitted

- `matrix-auto-solver.tsx` — checkpoint fix
- Part 3 overlay copy / fraction template revert

### Verification

- student-portal `npm run type-check` — pass (after save-state change)
- Macro App `portalPreviewUrl.test.ts` — 5 tests pass
- Matrix app `npm run test` — 27 tests pass (earlier in session)

---

## Open bug — CHASE1 grades empty (Chase-confirmed)

**Report:** Chase used code **CHASE1** (not student tester), completed **all three parts**, answered Part 3 questions, **Auto Solve unlocked** (implies `completedParts.length === 3` in UI). Teacher Console → Gauss-Jordan → **Grades** shows **no data** for CHASE1 as if never attempted.

**Chase rejects stale-cache / wrong-row explanation** — he was on CHASE1 the whole time.

**Leading hypotheses for next agent (investigate in order):**

1. **Local UI complete but Supabase never got final submit** — `handleComplete` calls `handleExitToHome()` then `await finish()`. If mid-session saves failed (TC preview + phone overlap → `SaveRefusedError` or retries), local `completedParts` can unlock Auto Solve while DB has no `completed` attempt or empty `attempt_items`. **Check Supabase** for CHASE1 student id: `attempts` where `activity_id = 'matrix/gauss-jordan'` (status, progress jsonb, completed_at).

2. **Finish/submit failed silently** — `finish()` sets `FINISH_FAILED_MESSAGE` on catch but user may not have noticed if already on home. Verify `submitCompletedAttempt` / `submit_tutorial_attempt` RPC for instructor row.

3. **Skip-gated UI false completion** — If `previewSkipGated` was active, `effectiveCompletedParts` fakes all parts complete **without** Supabase writes; Auto Solve unlocks without grades. Chase says he did the work, but confirm whether skip toggle was On in TC preview during that run.

4. **Macro App results query gap** — `listStudentProgressResults` in `electron-app/student-progress-io.js` — confirm CHASE1 attempts returned, activity id filter in `useMatrixReportData` / `isMatrixActivityId`, instructor row pinned via `INSTRUCTOR_PIN_CODES`.

5. **Concurrent sessions corrupting attempt** — two browsers same CHASE1: "Attempt belongs to another student" / "Attempt already completed" → blocked saves; UI still advanced.

**No portal logging for save failures** — only Supabase rows and header messages.

---

## Exact next step

1. Read `School Scrips/student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md` § Matrix / attempts.
2. Resolve CHASE1's `students.id` for code CHASE1; query Supabase (or Macro App service role) for all `matrix/gauss-jordan` attempts — compare in_progress vs completed, `progress.completedParts`, `attempt_items`.
3. If DB empty or in_progress only: trace `useMatrixTutorialAttempt.finish()` and whether failed saves left UI ahead of DB; fix so Auto Solve cannot unlock unless progress persisted OR submission succeeded.
4. If DB has completed attempt but TC grid empty: trace `listStudentProgressResults` → `useMatrixReportData` for CHASE1 row id mismatch.
5. Deploy portal + restart Macro App when fixes verified (Chase has not asked to commit yet).

---

## Read first

| Doc / file | Why |
|---|---|
| `agent docs/momentum-handoffs/latest.md` | This file |
| `School Scrips/student-portal/src/features/matrix-tutorial/useMatrixTutorialAttempt.ts` | finish + save flow |
| `School Scrips/student-portal/src/hooks/useResumableAttempt.ts` | save retry vs blocked |
| `School Scrips/Macro App/renderer/src/hooks/teacher-console/useMatrixReportData.ts` | grades grid data |
| `School Scrips/Macro App/electron-app/student-progress-io.js` | listStudentProgressResults |
| `School Scrips/student-session-kit/supabase/migrations/034_section_less_tutorials_and_teacher_locks.sql` | save_attempt_progress rules |

---

## Copy-ready fresh-task prompt

See agent reply to Chase.
