# Momentum handoff — Portal link emails, Netlify deploy docs, Kristy Force link

**Written 2026-09-12.** Day-valid only: if you are reading this on a later date, say so before acting.

**Slug:** `2026-09-12_portal-link-emails-force-link`

---

## Read first

1. **`School Scrips/student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md`** — identity flow, same-device mismatch, Netlify deploy procedure.
2. **`School Scrips/student-portal/AGENTS.md`** — identity keywords, shipping (`npm run deploy:prod`).
3. **`School Scrips/Macro App/AGENTS.md`** — Teacher Console, Outlook compose.
4. **This handoff** — parked; no queued next action unless Chase names one.

---

## Objective and current phase

**Phase: parked.** This session built portal-link email drafting, fixed Netlify deploy on Windows, and added a teacher-side fix for “someone else’s link” device binding (tester **Kristy**, code `88HR4Q`). Chase asked for a momentum handoff with **nothing left for him to do** — treat as complete unless he opens a new task.

**Nothing from this work stream has been committed or pushed.**

---

## Chase's desired feel

- **Students do nothing special** when a phone is stuck on the wrong code — Chase fixes it from Teacher Console, student just opens their normal email link.
- **Kristy** is spelled with a **K** (not Christy/CH).
- Portal link emails: **one Outlook draft per student**, personalized link, **never auto-send**; full eligible roster (not test limit of 2).
- Netlify deploy on his PC: **`npm run deploy:prod` only** — plain `netlify deploy --prod` hits Windows EPERM on `npm ci`; script does local build + `--no-build`.
- Do not hand Chase keyboard steps or “go verify” prompts at handoff time.

---

## Accepted decisions

| Decision | Why |
|---|---|
| **Force link** on Teacher Console roster (per student) | Server flag `device_bind_override_until`; portal clears local binding on next open of that student’s link. Teacher-side only. |
| Migration **`030_device_bind_override.sql`** | `grant_device_bind_override` (service_role), `device_bind_override_active` (anon), override consumed on successful `log_portal_sign_in`. |
| **No student-facing “Use my link” button** | Chase rejected student self-service; removed from `PortalGate`. |
| **Revoke code** stays for spares / leaked codes | Does **not** fix same-device mismatch — different problem. |
| Portal link email copy | Subject: `Your math app portal link`; body about bookmarking class app link, Tuesday, keep code private (see `portalLinkEmailTemplate.ts`). |
| Outlook multi-draft loop | After each draft: Close compose → Inbox → wait for New mail (Favorites Inbox uses `title`, not `aria-label`). |

---

## Rejected directions

| Rejected | Why |
|---|---|
| Clearing Kristy’s code in Supabase | Mismatch is **localStorage on the phone**, not a DB lock on `88HR4Q`. |
| Student taps button / incognito / clear site data | Chase wants **zero student action** beyond opening the email link. |
| Revoking another student’s code to unstick the phone | Nuclear; hurts the other student. |
| Plain `netlify deploy --prod` on Windows | EPERM on locked `node_modules`. |

---

## Current implementation state

### Supabase (remote)

- **`030_device_bind_override.sql` applied** via `npm run db:push` in `student-session-kit` (succeeded this session).
- Migration file still **uncommitted** in git.

### Student portal (`student-portal`) — modified, **not deployed to Netlify**

- `useStudentIdentity.ts` — checks `deviceBindOverrideActive(linkCode)` before code-mismatch block.
- `portalLoginEvents.ts` — `deviceBindOverrideActive()` RPC wrapper.
- `PortalGate.tsx` — mismatch copy mentions Chase can fix from his end; no student button.
- `scripts/netlify-deploy-prod.mjs` — build locally then `netlify deploy --prod --no-build --dir=dist`.
- Docs: `AGENTS.md`, `Guidelines.md`, `README.md`.

**Live site may still run old bundle** until a deploy runs — override check won’t work on production until then.

### Macro App — modified, **not committed**

**Portal link emails (Outlook CDP):**

- `modules/outlook/outlook_compose_cdp.py` — `compose_portal_link_drafts`, `ensure_inbox_for_compose`
- `modules/outlook/outlook_compose_processor.py` — `compose-portal-link-drafts`
- `renderer/.../usePortalLinkEmailCompose.ts`, `portalLinkEmailTemplate.ts`, `portalLinkEmailRecipients.ts`
- `TeacherConsoleRosterPanel.tsx` — “Draft portal link emails (N)”
- Tests: `portalLinkEmailTemplate.test.ts`, `portalLinkEmailRecipients.test.ts`, `test_outlook_compose_helpers.py`

**Force link (Teacher Console):**

- `electron-app/student-progress-device-override.js` — `grantDeviceBindOverride`
- `RosterForceLinkButton.tsx`, wired in `RosterStudentActions.tsx` + `ConsoleRosterScreen.tsx`
- IPC: `student-progress:grant-device-bind-override`
- CSS status line in `teacher-console-grades.css`

**Other dirty Macro App files** from same session (Outlook sign-in retries, CDP target fallback, shell wiring) — see `git status` in Macro App repo.

### student-session-kit — modified, **not committed**

- `docs/STUDENT_PROGRESS_PIPELINE.md` — mismatch + Force link + Netlify deploy sections.
- `supabase/migrations/030_device_bind_override.sql`

### Verification already done

- `db:push` for migration 030 — success.
- Portal `npm run build` — failed in agent env (`vite` not on PATH); not re-run.
- Unit tests for email template/recipients and outlook compose helpers — passed earlier in session.

---

## Kristy (`88HR4Q`) — context

- Chase enabled app access; she saw “someone else’s link” on her phone.
- Likely cause: phone already had **another student’s code** in localStorage (not necessarily her link ever being used).
- Teacher Console **Logins** tab shows red `code_mismatch` cells naming both students when this happens.
- **Force link** sets server override; after portal deploy, her same email link should work with no extra student steps.

---

## Open questions / constraints

- **Kristy outcome unconfirmed** — whether Force link + deploy unblocked her not verified in chat.
- **Full-roster email draft run** — automation updated for all eligible students; full-class success not confirmed after Inbox fix.
- **Prior handoff** `2026-09-12_portal-check-survey-q3.md` — Portal Check Q3 reword still uncommitted from an **earlier** task; unrelated to this handoff unless Chase returns to it.
- **No commit/push** unless Chase asks (end-of-session or explicit).
- **No GUI launches** without permission per root `AGENTS.md`.

---

## Exact next step

**None queued.** Session parked at Chase’s request. If he continues this thread: read this file, then ask what he wants next (Kristy verification, portal deploy, portal-link email run, or git sync). Do not invent follow-up work.
