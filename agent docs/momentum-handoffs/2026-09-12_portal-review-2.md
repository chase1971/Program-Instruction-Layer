# Momentum handoff: second portal risk review

**Written 2026-09-12.** Day-valid only. If you are reading this on a later date, say so before acting.

**Slug:** `2026-09-12_portal-review-2`

---

## Read first

1. **`agent docs/scratch/portal-risk-review-2.html`** is the review, served at
   `http://127.0.0.1:8765/scratch/portal-risk-review-2.html`. It has 7 commentable cards. Chase has
   not commented yet. When he says "read my comments on the second portal review", read
   `agent docs/scratch/portal-risk-review-2.comments.json` and answer by appending to that page's
   `REPLIES` object (see `agent docs/rules/html-delivery.md` § Reader comments).
2. **`agent docs/momentum-handoffs/2026-09-11_portal-risk-fixes.md`** covers the first review: his
   frame, what he accepted, and what he rejected. **Do not re-raise rejected items** (rate limiting,
   code-entry box, re-grading, archiving, mismatch log direction, legal framing of login logs).
3. **`School Scrips/student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md`** explains the whole chain
   and the shipping rules. Migrations are pushed by the agent automatically. Netlify deploys happen
   only when Chase asks. Tightening migrations wait in `supabase/pending/`.

---

## Objective and current phase

Chase asked for a second look at the student portal and the Teacher Console (Macro App) for critical
issues he may have missed. **The review is written, re-verified, and published as HTML. No fixes have
been made.** He has not yet approved any fix. The next phase is implementation, once he says which items.

---

## Chase's desired feel (carried from the first review, still true)

- Low stakes: homework completion credit at most. Do not design for exam integrity.
- "Does this generate an email to me" is the test for student-facing decisions.
- Fewer doors, not more options.
- He turns things off on purpose. **This session he corrected me:** I said the Matrix tutorial was
  "broken right now for every student", but he has Matrix access switched off for 30 M1324 students
  deliberately and wants it off. **Always check live toggles (`student_app_access`) before calling
  something student-facing urgent.**

---

## Findings (all verified live unless marked)

Supabase project `xdpegfmsauxwspswlmmj`. Read-only checks went through the Management API
(`POST https://api.supabase.com/v1/projects/<ref>/database/query`, with `SUPABASE_ACCESS_TOKEN` from
`student-session-kit/.env`). Never print the token.

1. **Matrix save/submit broken by migration 033. Fix before Matrix is turned back on.**
   033's `save_attempt_progress` now raises "Activity not available for this class" when
   `activities.section_id` does not match `effective_student_section_id`. `matrix/gauss-jordan`
   has `section_id` null, so every save fails. `submitCompletedAttempt` saves first, so Finish fails too.
   Students have Matrix off, so today only CHASE1 and the testers `kqrzc6` / `88hr4q` hit it (they
   bypass the per-student toggle). Proposed fix: a new migration that only enforces the match when the
   activity names a section, the same rule `submit_tutorial_attempt` (022) uses. Check whether
   `submit_quiz_attempt` or `get_quiz_questions` need the same care for section-less activities.
2. **Teacher-only functions can be executed by `anon`.** `revoke all ... from public` does not remove
   Supabase's default direct grant to `anon` and `authenticated`. `has_function_privilege('anon', ...)`
   is true for every function. With only the anon key I confirmed that the `activities` select exposes
   section ids and that `list_portal_login_events` returns student ids. Exposed functions:
   reset_student_attempts, revoke_student_code, publish_exit_ticket, update_exit_ticket,
   unpublish_exit_ticket, publish_class_announcement (needs only the section code
   `MATH-1324 4202 1` + term `current`), unpublish_class_announcement, set_student_app_access,
   set_students_app_access, list_student_app_access, list_portal_login_events,
   grant_device_bind_override (030), set_preview_section and revoke_student_membership (033), and
   finish_attempt. Proposed fix: a migration that revokes execute from anon and authenticated on
   these, plus `alter default privileges in schema public revoke execute on functions from anon,
   authenticated`. After that, any function the portal needs must be granted to anon explicitly. The
   portal never calls these functions (grep confirmed) and Macro App uses the service role, so no
   deploy is needed. Verify with `has_function_privilege` after pushing.
3. **`supabase/pending/023_close_anon_writes.sql` can now be pushed.** The portal was deployed on
   2026-09-12. The live bundle `index-DLCvqFnu.js` contains `submit_tutorial_attempt` and no longer
   contains `finish_attempt` or `CHASE1`. The anon insert/update policies are still live. Also
   proposed: rotate the CHASE1 code, because it sat in the public bundle about a week. Its link is used
   by Macro App's Teacher Console preview and App Dashboard.
4. **Term-turnover device lock.** Old-term codes are never deactivated, so a returning student's new
   link shows the mismatch screen, and Force link (030) needs an email first. Proposal: deactivate a
   course's codes in Macro App's course-retire flow.
5. **The save retry loop has no delay.** In `student-portal/src/hooks/useResumableAttempt.ts`,
   `flushSaveNow` re-awaits itself in `finally` immediately and forever. It is a hot loop offline and
   endless on server refusals. Proposal: backoff (1, 2, 4 ... 30 s), stop on server errors, stop on
   unmount. Needs a Netlify deploy (Chase's call).
6. **No backups on Free, and a 7-day inactivity pause.** Proposal: a scheduled `supabase db dump` to
   his PC.
7. **Deactivate and the section gate are browser-only.** `localStorage mathapps.isInstructor` and
   `?previewSection=` bypass them. Low stakes, nothing proposed.

Already fixed by other sessions today: once-policy retakes (032), the old live bundle (deployed),
Force link (030). There are 11 orphaned attempts (student_id null) left over from old revoke deletes,
which is harmless.

---

## Current implementation state

- Created `agent docs/scratch/portal-risk-review-2.html` and added it to
  `agent docs/page-manifest.json` (match list + description). Comment save endpoint tested (200); the
  test comments file was deleted afterwards.
- Session-tracking bumps were logged for both deliverables.
- **Nothing committed.** Other sessions have uncommitted work in student-portal,
  student-session-kit and Macro App (migrations 030–033 and more). Do not commit unless asked.

---

## Open questions (his call)

- Which fixes to do, and in what order. The page's top three are: Matrix section check, lock the
  teacher functions, push 023.
- Whether to rotate CHASE1.
- Whether he wants a backup job, and the term-end code deactivation.

---

## Exact next step

Wait for Chase to say which items to fix, or to comment on the page. If he says "fix them" without
specifics, start with **#2 (lock teacher functions)** as a new migration in
`student-session-kit/supabase/migrations/` (next free number after 033), `npm run db:push`, then
verify with `has_function_privilege` that anon lost those and kept the portal-facing ones.
