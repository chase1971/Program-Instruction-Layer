# Momentum handoff — student portal risk fixes

**Written 2026-09-11.** Day-valid only: if you are reading this on a later date, say so before acting.

**Slug:** `2026-09-11_portal-risk-fixes`

---

## Read first

1. **`agent docs/scratch/portal-risk-review.html`** — the review, and the live record of every
   decision. Chase's comments and the agreed answers are threaded under each point.
   Served at `http://127.0.0.1:8765/scratch/portal-risk-review.html`.
2. **`agent docs/scratch/portal-risk-review.comments.json`** — his comments as data. 23 posts
   across 16 points. **This file is the authority on what he decided**, not this handoff's summary.
3. **`School Scrips/student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md`** — how the four parts
   fit together. Parts of it are now out of date (see Corrections below).
4. **`agent docs/rules/html-delivery.md` § Reader comments** — how to answer him in the page if he
   comments again. Append to the card's `REPLIES` array; never rewrite an existing reply.

---

## Objective and current phase

**Phase: review complete and fully triaged. Zero code fixed yet.**

Chase asked for unpredictable edge cases in the student portal + teacher console, focused on
students using it and on the integrity of the data collected from that use. A 16-point review was
written, he annotated every point, and each now has an agreed disposition. **The next task is
implementation.** No portal, console, or migration code has been touched.

What *was* built this session: the review page, a comment mechanism on the docs server, and the
threaded replies. Those are done and verified.

---

## Chase's desired feel — the frame to keep

- **Nothing here is high-stakes.** Homework completion credit at most. His standing position: "if
  something happened, I would just give the student credit." Do not design for exam integrity.
- **He does not want to be the support desk.** Judge every student-facing decision by "does this
  generate an email to me." That reasoning beat mine twice this session and he was right both times.
- **Fewer doors, not more options.** He killed a code-entry box because students would have to open
  the email anyway, so the box only adds a place to get stuck.
- **He is the admin and is comfortable with that.** "My name can look at other people's apps
  without penalty." Do not treat his own access as a threat.
- **Privacy matters for the institutional conversation, not because he fears a breach.** His college
  is reluctant about technology; he wants positions that cannot be poked full of holes.
- **No em-dashes in student-facing copy.** He said this explicitly ("without using in-dashes").

---

## Accepted decisions — implement these

Ordered roughly by his priority. Every one of these he approved in writing in the comments file.

### 1. First attempt only, locked from then on
**The single most important decision, because several other items collapse into it.** Whatever a
student did the first time is the record. Later attempts are allowed but can never change it.
He accepts there may be exceptions in future apps; for now this is the rule.

- `Macro App/renderer/src/hooks/teacher-console/useExitTicketResponseReport.ts:52` —
  `latestAttemptForActivity` takes `attempts[attempts.length - 1]`. Change it to the **earliest
  completed** attempt, falling back to an in-progress one only when no completed attempt exists.
- **Correct his belief while doing it:** he said "I made it to where I only see results of the first
  attempt." That is not true anywhere in the code. He may be thinking of the publish-time
  `attempt_policy = 'once'` switch, but `useExitTicketAuthoring.ts:51` defaults the form to
  `'repeatable'`, so his existing tickets likely allow retakes and he has been seeing latest
  attempts. He has been told this; he has not yet checked his published tickets.
- This also fixes the "reopening blanks out their row" bug and makes the "0 of 0" screen moot.

### 2. Remove the 500-attempt cap, filter by section, show a row count
`Macro App/electron-app/student-progress-io.js:200` — `&limit=500`, no section filter, no paging,
ordered newest-first so the **oldest** rows fall off silently. A second cap of `limit=200` sits in
`listCompletedAttempts` just below and needs the same treatment.

He asked what the number counts and was told: **attempts** (one row per student per time they do an
activity), not students and not answers. 30 students × 10 tickets × 3 sections = 900, so he was
already on course to lose data. Decision: drop the cap, filter to the section being viewed, and put
a visible row count on screen so truncation can never hide again.

### 3. Close the score back door
Revoke the leftover wide-open writes so server marking actually means something.

- `student-session-kit/supabase/migrations/001_initial.sql:72,77` — `attempts_anon_insert` and
  `attempt_items_anon_insert` are `with check (true)`.
- `004_finish_attempt.sql:31` — `finish_attempt` is granted to anon with no ownership or score
  validation.

**Ordering matters and will break Matrix if you get it wrong:** the Matrix tutorial still submits
through the old path (`student-portal/src/services/attemptSubmission.ts` →
`useMatrixTutorialAttempt.ts:232`). Move Matrix onto the `submit_quiz_attempt` path **first**, then
close the old door.

### 4. `CHASE1` out of the published bundle
`student-portal/src/config/portalAccess.ts` — it ships in `dist/assets/index-*.js` as plain text and
bypasses both section gating and the device lock. Make it an ordinary `students` row enrolled in
every section instead. **Do this together with nothing-breaks-for-him**: his admin access must keep
working through the change. Also `Macro App/electron-app/student-progress-io.js` has
`INSTRUCTOR_REPORT_CODES = ['CHASE1']` that must stay in sync.

### 5. Duplicate answer rows on retry
`student-portal/src/services/attemptSubmission.ts:57` inserts `attempt_items` without deleting
first, so a failed `finish_attempt` followed by pressing Finish again doubles every answer inside
one attempt. Clear old answers before writing, **and** add a uniqueness rule on
`(attempt_id, slot)` so it becomes impossible rather than unlikely.

### 6. Active/inactive instead of deleting a student
`012_revoke_student_code.sql` deletes the `students` row; `attempts.student_id` is
`on delete set null`, so every score they earned becomes unattributable and their login history
cascades away. Add an `active` flag, check it in `claim_student()` / `log_portal_sign_in()`, and have
revoke flip it.

**He asked about archiving and the answer was no, don't bother:** an attempt row is a few hundred
bytes, 100k rows is well under a tenth of the 500 MB free tier, so keep everything forever.
`reset_student_attempts` (011) also deletes *all* of a student's attempts with no activity filter —
give it a per-quiz option.

### 7. Publish by section id, never invent a section
`useExitTicketAuthoring.ts:121` hardcodes `term: 'current'` while the mint path uses
`existingMap?.term ?? 'current'`, and the `(code, term)` index is case-sensitive. Any drift creates a
second empty section and publishes into it while reporting success. Publish against the section id
the roster sync already knows, and error out when no section matches.

### 8. Stop printing the bound student's code on the mismatch screen
`student-portal/src/app/components/PortalGate.tsx:30` renders `Your code: {storedCode}`.
**He pushed back on the severity and was right** — see Rejected below. Keep only: stop printing the
code, and keep a "this isn't me, sign this device out" button, which is what unsticks his own demo
device. Nothing else from the original recommendation.

### 9. The locked-out message, his wording, one destination, no code box
Replace the "you need your class link" copy. No code entry, no dashes:

> **You need your class link**
> Open the link in the email I sent you and you'll be signed straight back in. If you can't find
> that email, message me and I'll send you a new link.

Detection of "this device used to have access" is **not possible** once storage is evicted — he
asked, and the answer is no. One message serves both cases instead.

### 10. Block rewriting option *wording* after submissions
`016_update_exit_ticket.sql` lets option text change while ids stay, so stored answers silently come
to mean something different. Renaming the title and reordering stay allowed. No re-grading
machinery — he explicitly dropped that (see Rejected).

### 11. Cryptographic randomness for new codes
`student-portal/scripts/lib/roster-codes.mjs:65` uses `Math.random()`. Switch to `crypto.randomInt`.
**Changes nothing that already exists** — existing codes, spare codes and course files are
untouched, nothing to reissue. He confirmed no codes have been handed out yet.

### 12. Delete the open-time completion check
Once #1 lands, the one-attempt check in
`student-portal/src/features/generic-quiz/useGenericQuiz.ts:99` is unnecessary. It is an
unhandled promise rejection that leaves a permanent blank loading screen. **Remove the code rather
than adding a catch** — that was the agreed resolution after he questioned it closely.

---

## Rejected directions — do not rediscover or re-argue

- **Re-grading past attempts after an answer-key typo.** "This is not going to matter... I don't
  care." Only the option-wording block (#10) survives.
- **Treating the mismatch screen as a credential leak.** I overstated it and conceded. The
  detection value is low, phones are the normal case, nothing here is worth stealing. Implement only
  the one-line change in #8.
- **Fixing the code_mismatch log direction.** "It doesn't matter." The log blames the device owner
  rather than whoever arrived with a new link. No change. If anyone ever reads that column, remember
  the direction is unreliable.
- **A code-entry box anywhere in the portal.** Killed deliberately: "if that box was there, I would
  get more emails telling me what's the code." Do not reintroduce it as a convenience.
- **Archiving student data off the database.** Unnecessary at this scale; keep everything.
- **Any cap on attempts as the answer to payload size.** Filter and page instead.
- **Treating the login log as a legal problem.** It is not. Every LMS logs more. I had implied
  otherwise and corrected it: retention is a practical nicety for a nervous committee, not a legal
  requirement.
- **Rate limiting / failed-code-attempt logging.** Discussed under the randomness item; he took the
  free half only. Do not build monitoring.

---

## Open questions — his call, not yours

1. **Does the code stay visible to students?** `student-portal/src/app/components/PortalUserLabel.tsx`
   shows `User ABC123` on assignment headers so he can identify a student from a screenshot. He said
   he'd prefer they not know a code exists, but the screenshot use is real. **Flagged, not decided.**
2. **Has he checked whether his published tickets are `once` or `repeatable`?** Asked, not answered.
   #1 makes it not matter for the console, but it still determines whether students can retake today.
3. **Retention policy for `portal_login_events`.** Proposed 90 days; he did not accept or reject.
   Purely optional, practical only.
4. **Where the three instrumentation columns go** (which variant, what was chosen, when each step
   happened) — from the pipeline doc's "long game" section. Not discussed this session. Still
   unbackfillable, still worth raising before any schema change lands.

---

## Corrections to existing docs that should land with the work

`STUDENT_PROGRESS_PIPELINE.md` is now wrong in two ways that will mislead the next reader:

- It calls closing the anon insert/update policies **"optional cleanup."** It is not optional; it is
  what makes grading mode `server` mean anything. Decision #3 reverses that framing.
- Its "Deactivate dropped students, do not delete them" position contradicts shipped migration 012,
  which deletes. Decision #6 resolves it in favour of the doc.

Also worth a line there: the doc predates migrations 011–016, so its "Known gaps" list no longer
matches the schema.

---

## Current implementation state

**Nothing in the portal, console, or migrations has been modified.** All portal/console findings are
unfixed by design — this session was review and triage only.

Changed this session (all verified, none committed):

| File | Change |
|---|---|
| `agent docs/scratch/portal-risk-review.html` | The review + 16 comment threads + 23 replies. 69 KB. |
| `agent docs/scratch/portal-risk-review.comments.json` | His comments. **Do not hand-edit** — the page owns it. |
| `scripts/serve-programs-docs.js` | Added `POST /__comments/<page>`, the only write the server allows. |
| `agent docs/rules/html-delivery.md` | New § Reader comments — the mechanism and the REPLIES convention. |
| `agent docs/INDEX.md` | Row routing "read my comments on \<page\>" to that section. |
| `agent docs/page-manifest.json` | Filed the review page under App & pipeline maps. |

**Verified:** save endpoint returns 200 and round-trips; unknown page, path traversal and GET all
rejected (404/404/405); page and index serve 200; every one of his 23 posts has a reply at the
matching index; his comments file is byte-identical to what he typed (it was backed up before
testing and restored). Page script passes `node --check`.

**The docs server was restarted this session** to pick up the endpoint, and is running.

---

## Exact next step

Start with **decision #1** (`useExitTicketResponseReport.ts:52` → earliest completed attempt),
because it is one small change, it is the decision the other items lean on, and it immediately makes
his teacher console tell the truth. Then #2 in the same file's data path.

Do **not** start with #3 — it needs the Matrix submit-path migration first and is the one item that
can break something he uses today.

Four repos are in play: `student-portal`, `student-session-kit` (migrations), `Macro App`, and the
sibling Matrix app. Per the pipeline doc, **migrations are pushed automatically by the agent**
(`npm run db:push` in `student-session-kit`) while **Netlify deploys happen only when Chase asks**.
