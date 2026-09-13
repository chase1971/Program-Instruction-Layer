# Portal assignment gate — blocking errors inside an app

> **When Chase says:** "access turned off but they still see the tile", "error in the
> header is cut off", "deactivated student opened the quiz", "show a full page instead
> of overlaying the app", "assignment isn't available".

## The failure mode

A student opens an assignment (exit ticket, Matrix tutorial, future apps). Something
**hard-stops** progress — app access off, database refused the attempt, quiz not
published for them. If the app still renders questions behind a red line in the navy
header (`.portal-quiz__header-status` is absolute and clips on phones), the message is
unreadable and the UI looks broken.

**Never overlay a blocking error on assignment chrome.** Replace the assignment body
with a full-page gate.

## Three layers — pick the right one

| Layer | When | Component | Student actions |
|---|---|---|---|
| **Sign-in gate** | No code, wrong link, offline before identity | `PortalGate.tsx` | Try again (offline only); no Go home |
| **Portal home gate** | Signed in but section has no pilot apps | `PortalNoAccess.tsx` | Email instructor only |
| **Assignment gate** | Inside `#/quiz/…`, Matrix tutorial, etc. | `PortalAssignmentGate.tsx` | **Refresh** + **Go home** |

Gate-level screens are **not** assignment gates. Assignment gates are **not** modals
and **not** header status lines.

## Blocking vs header-only errors

Copy lives in `student-portal/src/config/studentMessages.ts`. Helpers:
`isBlockingAssignmentMessage()`, `isHeaderAssignmentError()`.

| Situation | Blocking (full page) | Header only (keep working) |
|---|---|---|
| App access off / `save_attempt_progress` refused at start | Yes — `START_REFUSED_MESSAGE` | |
| Network down at open | Yes — `START_FAILED_MESSAGE` | |
| Save refused mid-session (DB says no) | Yes — `SAVE_BLOCKED_MESSAGE` | |
| Quiz not published for class | Yes — `QUIZ_LOAD_FAILED_MESSAGE` | |
| Transient save retry | | `SAVE_RETRY_HINT` |
| Submit failed, can retry Finish | | `FINISH_FAILED_MESSAGE` |

When in doubt: if the student **cannot** safely continue the assignment, use the
assignment gate. If they can tap the same button again, keep it in the header.

## Assignment gate UI

**Exemplar:** `student-portal/src/app/components/PortalAssignmentGate.tsx`

- Same visual language as `PortalGate` (`.portal-gate`, centered title, `max-w-md` body).
- **Two buttons always:** Refresh (`window.location.reload()`) and Go home
  (`navigatePortalRoute('classwork')`). Do not pick one — Chase cannot know every edge
  case (offline mid-submit vs deactivated vs wrong class). Refresh retries the same URL;
  Go home exits the assignment.
- Dwell-friendly: `min-h-12`, side-by-side with wrap on narrow screens.
- No backdrop dismiss (not a modal).

## Hide tiles before the gate

Students should not click into an assignment they cannot use.

1. **Home / classwork list** — filter published activities with
   `checkStudentAppAccess(studentId, activityId)` before showing tiles.
   Exemplar: `student-portal/src/services/classworkData.ts` → `filterQuizzesByAppAccess`.
   Instructor devices skip the filter (`isInstructorDevice()`).
2. **Route entry** — check access before fetching content or mounting the runner.
   Exemplar: `GenericQuizView.tsx` uses `useStudentAppAccess` then
   `PortalAssignmentGate` when denied.
3. **Attempt start** — `useResumableAttempt` may set `status: 'error'`. The feature
   hook must **not** render the assignment UI on error. Exemplar: `useGenericQuiz.ts`
   sets `phase: 'blocked'` and `GenericQuizRunner` returns `PortalAssignmentGate`.

Matrix tutorial: `MatrixTutorialView` returns the gate when
`attempt.blockingMessage` is set (`useMatrixTutorialAttempt.ts`).

## Adding a new portal app — checklist

1. Register activity in Supabase + Teacher Console app access toggles.
2. **Classwork or home tiles:** filter with `student_has_app_access` (or equivalent).
3. **Route/view:** gate on access before loading assignment content.
4. **Resume hook:** on `useResumableAttempt` error or `saveState === 'blocked'`, show
   `PortalAssignmentGate` — do not pass blocking text to `PortalQuizHeaderCenter`.
5. **Messages:** add new copy to `studentMessages.ts`; if blocking, add to
   `BLOCKING_ASSIGNMENT_MESSAGES` set.
6. **Header:** only transient errors via `PortalQuizHeaderCenter` +
   `isHeaderAssignmentError()`.

## Anti-patterns

- Red error string in `.portal-quiz__header-status` for access denied or start failure.
- Rendering the quiz/matrix while `resumeStatus === 'error'`.
- Listing every published quiz on home without an access check.
- Assignment gate with only Go home (no Refresh) — bad for connection blips.
- Modal with backdrop click dismiss (dwell unsafe).

## Related

- First paint (separate concern): [first-paint-gate.md](./first-paint-gate.md)
- Student progress pipeline: `student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md`
- Per-student app access: migration `013_student_app_access.sql`
