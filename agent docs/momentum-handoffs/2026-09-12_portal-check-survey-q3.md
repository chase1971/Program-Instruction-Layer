# Momentum handoff — Portal Check survey Q3 + preview/quiz fixes

**Written 2026-09-12.** Day-valid only: if you are reading this on a later date, say so before acting.

**Slug:** `2026-09-12_portal-check-survey-q3`

---

## Read first

1. **`agent docs/momentum-handoffs/2026-09-12_teacher-console-announcements-preview.md`** — prior dashboard/announcements/preview work (still uncommitted).
2. **`School Scrips/Macro App/AGENTS.md`** — Teacher Console keywords; exit ticket / preview server.
3. **`School Scrips/student-portal/AGENTS.md`** — portal dev port 5340, deploy.
4. **This handoff** — exact next step is updating **Portal Check** question 3 in Teacher Console.

---

## Objective and current phase

**Phase: preview and quiz flow work; survey copy needs one publish.**

Chase has **Portal Check** — a three-question exit ticket (feedback only, no grading) published
via Teacher Console for his M1324 classes. The portal preview on the Teacher Console dashboard
now loads and surveys open. Chase reviewed question 3 and wants it **reworded** so students are
not asked to judge features of *his specific apps* before they have used them. The next agent
should **update the live published ticket** (Supabase via Teacher Console quiz editor), not only
suggest copy in chat.

**Nothing from this extended session has been committed or pushed.**

---

## Chase's desired feel (survey Q3)

- Students **do not yet know** what apps Chase will assign. Q3 must ask what they **would want**
  from a class app in general — not “does this app help you learn” as if they already know the product.
- Keep the question plain and student-friendly. Chase’s framing: **best feature for using an app** /
  **what would help most**.
- Options should be **concrete things a student can picture**, not meta lines like “easy to use as
  apps I already use” or “helps my instructor know where I need help” (those were **rejected** for Q3).
- **Approved option themes for Q3:**
  - Tells me right away if I got something right or wrong
  - Explains things in guided practice (step-by-step while practicing)
  - Easy to use and quick to do
  - Offers tutorials I can follow
- Q1 and Q2 can stay as published unless Chase asks for a consistency pass (they still say “class app
  like this” — only Q3 was flagged this session).

---

## Accepted survey copy — question 3 (Chase-approved direction)

**Publish this in Teacher Console** (replace question 3 only; keep Q1 and Q2 unchanged unless Chase says otherwise):

```
Q: What would be the most helpful feature for you in a class app?
- It tells me right away if I got something right or wrong
- It explains things while I practice step by step
- It is easy to use and quick to do
- It offers tutorials I can follow
```

**Tile title:** Portal Check (unchanged).

**Intro inside the ticket** (already short): “Please answer all three questions. There is no wrong answer. This does not affect your grade.”

**Home screen intro** (not inside the ticket): `student-portal/src/config/portalHomeIntro.ts`

---

## Full Portal Check paste (all three questions — reference)

Use when republishing or if the editor is easier with full paste. **Q3 is the only intentional change from what students saw earlier.**

```
Q: Which of these would be most helpful to you in a class app like this?
- Short questions at the end of class so I can tell if I understood the lesson
- Extra practice problems I can redo anytime
- Short tutorials that walk me through new topics step by step
- Step-by-step help when I'm stuck on a homework problem

Q: When would you most likely use a class app like this?
- Right after class while the lesson is still fresh in my mind
- While I'm doing homework later that day
- When I'm studying for a quiz or test
- When I have a few free minutes between classes or on the bus

Q: What would be the most helpful feature for you in a class app?
- It tells me right away if I got something right or wrong
- It explains things while I practice step by step
- It is easy to use and quick to do
- It offers tutorials I can follow
```

**How to update:** Macro App → Teacher Console → Exit Tickets → open **Portal Check** → Quiz
subview → edit paste / save via existing `useExitTicketQuizEdit` flow. Refresh preview after save.

---

## Rejected directions (Q3)

| Rejected | Why |
|---|---|
| “It is as easy to use as apps I already use every day” | Too vague; assumes comparison to unknown apps |
| “What I do here helps my instructor know where I need help” | Students don’t know the app’s purpose yet |
| “What would make you feel like an app like this is actually helping you learn?” (original Q3 prompt) | Implies they already understand Chase’s apps |

---

## Current implementation state (this session — uncommitted)

### student-portal

| Area | What changed |
|---|---|
| `src/hooks/usePortalRoute.ts` | Quiz routes (`quiz/...`) no longer map to home |
| `src/app/App.tsx` | Renders `GenericQuizView` for quiz routes |
| `src/styles/index.css` | Assignment quiz full-bleed layout, smaller text, fixed header/footer curves; removed inner `portal-section-light` box on quiz body |
| `src/features/generic-quiz/GenericQuizQuestionCard.tsx` | Dropped `portal-section-light` on body |
| `src/features/generic-quiz/GenericQuizResult.tsx` | Same |
| `vite.config.ts` | `optimizeDeps.include` for katex etc. |

### Macro App

| Area | What changed |
|---|---|
| `TeacherConsolePortalPreviewControls.tsx` | Refresh button (fixed missing `STUDENT_PORTAL_DEV_ORIGIN` crash) |
| `refreshPortalPreview.ts` | Re-activate preview slot + navigate/reload |
| `AppSidePanel.tsx` | Refresh restarts dev server in Preview mode then reloads embed |
| `student-portal-host.js` | Kill port 5340 on stop/start; clear `.vite` cache **after** port free; `restartServer` IPC |
| `browser-slot-console-forward.js` | Forward `[PortalPreview]` warnings/errors to module log |
| `portalPreviewUrl.ts` | Dev origin `http://127.0.0.1:5340` (matches Vite host) |
| `useTeacherConsolePortalPreview.ts` | Removed hide-on-unmount that broke embed |
| `useStudentPortalDevServer.ts` | Exposes `refreshStatus` |

### Verification

- Preview white screen traced to stale Vite on 5340 + `504 Outdated Optimize Dep` on katex; fixed by killing port and clean restart.
- Chase confirmed **app working** after fixes; quiz UI spacing improved; survey Q3 copy still **not** updated in Supabase.

---

## Open questions / constraints

- **Live survey text is in Supabase**, not in repo — must edit via Teacher Console (or RPC if agent has a scripted path; UI is the intended path).
- **Full Macro App restart** required after electron/preload changes; Preview **Refresh** restarts Vite + reloads embed.
- **Do not commit/push** unless Chase asks or end-of-session protocol.
- Prior handoff **`2026-09-12_teacher-console-announcements-preview`** still describes large uncommitted dashboard/announcements work — same dirty tree.

---

## Exact next step

1. Read **`School Scrips/Macro App/renderer/src/hooks/teacher-console/useExitTicketQuizEdit.ts`** and **`ConsoleExitTicketQuizScreen.tsx`** — confirm edit/save path.
2. Open Teacher Console → **Portal Check** → Quiz editor.
3. Replace **question 3** with the approved copy above (or full three-question paste if easier).
4. Save/publish update.
5. Preview mode → **Refresh** → confirm Q3 wording and options on question 3 of 3.
6. *(Optional)* Add `student-portal/src/config/portalCheckSurvey.ts` with `PORTAL_CHECK_SURVEY_PASTE` constant so future edits have one code owner — **only if Chase wants repo source of truth**; not required for this task.
