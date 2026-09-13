# Momentum handoff — Math App Survey retake, exit ticket Responses, portal deploys

**Written 2026-09-12.** Day-valid only: if you are reading this on a later date, say so before acting.

**Slug:** `2026-09-12_math-app-survey-retake-exit-ticket-responses`

---

## Read first

1. **`School Scrips/student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md`** — pause/resume, attempt policy, Netlify deploy.
2. **`School Scrips/student-portal/AGENTS.md`** — shipping (`npm run deploy:prod` only).
3. **`School Scrips/Macro App/AGENTS.md`** — Teacher Console, exit tickets, student progress.
4. **This handoff** — then ask Chase what he wants next if unclear.

---

## Objective and current phase

**Phase: survey retake debugging mostly resolved; one config mismatch found; Macro App teacher-console work uncommitted.**

Chase is friend-testing **Math App Survey** via spare roster links. He wanted **Best attempt / redo** behavior: reopen = fresh Q1, each full submit counts, Responses shows latest answers. A friend hit **auto-resume to Q2** and **"Attempt not found"** on submit. Portal fixes were deployed (deploys **11** and **12**). Supabase investigation showed **Math App Survey is still `once` (First attempt) in the database** — that explains resume-to-Q2 and why repeatable-only fixes did not fully match his expectation.

**Nothing committed or pushed** across the three repos (student-portal, Macro App, student-session-kit).

---

## Chase's desired feel

- **Best attempt surveys:** reopen always starts at **question 1** with blank answers — no mid-quiz auto-resume. Each completed submit is a new attempt; Responses row shows **latest** answers (ungraded survey).
- **Friend testing:** spare rows **Chris** and **Kristy** at the bottom of exit ticket **Responses** so friends can submit on tester links and show up there.
- **Kristy** spelled with a **K** (not Christy/CH on spare labels).
- **Netlify:** always **`npm run deploy:prod`** in `student-portal` — never plain `netlify deploy --prod` (Windows EPERM on `npm ci`).
- **Students do nothing special** for device-bind mismatch — Force link from Teacher Console (prior work).
- Do not hand Chase keyboard verification steps at handoff time.

---

## Accepted decisions

| Decision | Why |
|---|---|
| **`resume_attempt` only returns in-progress rows when `attempt_policy = 'once'`** (migration `031`) | Repeatable activities always start fresh; mid-quiz drafts not restored on retake. |
| **`useResumableAttempt` — `resumeEnabled` option; eager DB registration on fresh start** | Repeatable skips resume; empty attempt row created immediately so submit never races ahead of first save. |
| **`useGenericQuiz` — `await ensureProgressSaved` before submit** | Flushes pending saves before `submit_quiz_attempt`. |
| **`classworkData` — "In Progress" tile only for `once`** | Repeatable retakes don't show stale in-progress badge. |
| **Exit ticket Responses — Chris/Kristy spares at bottom** | `pickNamedTesterSpares()` in `matrixReportRoster.ts`; used by `useExitTicketResponseReport`. |
| **Responses page scroll** | Wheel scroll via `useGradebookViewportWheelScroll` in `MatrixReportScrollFrame`; CSS in `teacher-console-grades.css`. |
| **Browser slot right-click copy/paste** | `wireRendererContextMenu()` in `browser-slot-context-menu.js` + `main.js`. |
| **Deploy 10–12 live on Netlify** | Force link (10), repeatable fresh-start (11), attempt-not-found race fix (12). Live: https://mathappsclass.netlify.app |

---

## Rejected directions

| Rejected | Why |
|---|---|
| Assuming saves failed when Chase sees two answers in Responses | Answers **did** persist; three completed Math App Survey submits today in Supabase. "Attempt not found" was from an **earlier broken session** (pre-deploy-12 race), not missing saves. |
| Treating Math App Survey as `repeatable` without checking DB | Supabase `activities.attempt_policy` for Math App Survey is **`once`** — repeatable fixes don't change its resume behavior until policy is changed. |
| Plain `netlify deploy --prod` | Wipes/locks `node_modules/vite` on Windows while dev server running. |

---

## Current implementation state

### Supabase (remote)

- **`030_device_bind_override.sql`** — applied (Force link).
- **`031_resume_once_policy_only.sql`** — applied via `db:push`.
- Both migration files **uncommitted** in `student-session-kit`.

**Math App Survey** (`exit-ticket/406041a1-7d05-4dc8-925a-7e8929c00b66`):
- `attempt_policy`: **`once`** (First attempt) — **not** `repeatable`.
- **3 completed attempts today** with both Q1/Q2 answers: codes **`4VGKJ7`**, **`88HR4Q`** (Kristy), **`KQRZC6`** (~4:34 PM last).
- **No in-progress** rows on Math App Survey currently.

Separate published ticket **"Exit Ticket"** (`exit-ticket/9480d6f7-…`) is `repeatable`; **`CHASE1`** has two empty in-progress shell rows from eager registration (wrong ticket if testing survey).

### Student portal — modified, **deployed** (deploys 10–12) but **not committed**

Key survey/attempt files:
- `src/hooks/useResumableAttempt.ts` — eager register + `ensureProgressSaved`
- `src/features/generic-quiz/useGenericQuiz.ts` — `resumeEnabled: quiz.attemptPolicy === 'once'`
- `src/services/classworkData.ts` — in-progress tile for `once` only
- Also uncommitted from earlier: identity override, `PortalGate`, `netlify-deploy-prod.mjs`, docs

**Netlify counter:** 12 production deploys in 2026-09 (~180 credits). Bundle `index-CsHrljQs.js` includes fix markers.

### Macro App — modified, **not committed**, needs **reload/restart** for renderer + electron changes

Exit ticket Responses (this session):
- `matrixReportRoster.ts` — `pickNamedTesterSpares()`, `responseReportSpareStudents()`
- `useExitTicketResponseReport.ts` / tests
- `ExitTicketResponseGrid.tsx`, `ConsoleExitTicketResponseScreen.tsx`
- `MatrixReportScrollFrame.tsx`, `teacher-console-grades.css`, `teacher-console-matrix-report.css`
- `electron-app/browser-slot-context-menu.js`, `.test.js`, `main.js`

Also uncommitted from earlier session: portal link emails, Force link, Outlook CDP, etc. (see `git status` in Macro App).

### Verification already done

- Live bundle contains `resumeEnabled`, `ensureProgressSaved`.
- `resume_attempt` RPC returns empty for Math App Survey student (repeatable filter + no in_progress).
- Supabase REST queries confirmed attempt policy and completed submissions.
- Macro App unit tests passed for exit ticket response report / spare roster (earlier in session).

---

## Open questions / constraints

- **Math App Survey policy mismatch:** Teacher Console may show **Best attempt** in UI while DB has **`once`**. Chase wants redo — **flip to `repeatable` and save** in Teacher Console (or via `update_exit_ticket` RPC) unless he intentionally wants First attempt.
- **Friend retest after policy fix:** full tab close + reopen personal link; should land Q1 if `repeatable`.
- **Macro App uncommitted work** not on Netlify — spares-on-Responses, scroll, context menu require Macro App restart.
- **Kristy Force link** — portal override deployed; Force link button uncommitted in Macro App.
- **No commit/push** unless Chase asks.
- **No GUI launches** without permission per root `AGENTS.md`.

---

## Exact next step

**If Chase continues survey friend-testing:** open Teacher Console → **Math App Survey** → confirm side panel says **First attempt** vs **Best attempt**. If he wants redo, switch to **Best attempt**, save/republish, then have friend close tab completely and reopen her link. Verify Responses row updates on submit.

**If he names something else:** read this file, ask one focused question, do not invent work.
