# Momentum handoff — Exit ticket quiz: multi-question slides, shuffled choices, graded authoring fixes

**Written:** 2026-09-27
**Apps:** `School Scrips/Macro App` · `School Scrips/student-portal` · `School Scrips/student-session-kit`

## Read first

1. **`School Scrips/Macro App/AGENTS.md`** — Teacher Console / exit tickets keyword row if present; else grep `exit-ticket`.
2. **`School Scrips/student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md`** — deploy order when schema + portal both change.
3. This file § 7 for the exact next step.

## 1. Objective and current phase

Chase is building **graded math review exit tickets** (domain + range for square root, quadratic vertex form, rational function) via the **AI → paste → parse → publish** workflow in Macro App Teacher Console, with **LaTeX** (`$...$`) in prompts and options.

**Phase:** Feature code is **implemented locally** across Macro App, student portal, and Supabase migration 058. **Not yet committed or deployed.** Chase needs to reload Macro App, republish the quiz with the new paste format, and deploy the student portal before students see slides/shuffle/left-align.

## 2. Chase's desired feel

- **Two related questions on one slide** (domain + range per function) — not one question per screen when there's room.
- **Question text left-aligned** with **numbers on the left edge** (1., 2., …). Header "N of M" (pages) is fine.
- **Same problems and question order for everyone**; only **multiple-choice option order** may differ per student.
- When they **open** the quiz, they get a personal option order that **stays fixed** if they resume mid-quiz.
- **Do not** author graded quizzes where every correct answer is choice **A** (first line) — students pattern-match. Parser should reject that; AI prompt should rotate `*` positions.
- Publish flow must work without mystery failures (empty Name was blocking publish silently before).

Speech-to-text user — ask one focused question when ambiguous; no typing-heavy flows.

## 3. Accepted decisions

| Decision | Why |
|---|---|
| **`---` page break in paste format** | Questions before the next `---` share one slide; break starts a new slide. No `---` = legacy one question per slide. |
| **`page_group` column on `questions`** (nullable) | NULL = one question per step (backward compat). Same non-null group = one slide. |
| **Left-align prompts + per-question numbers** | Portal + teacher live preview CSS; numbered heading row. |
| **Reject graded parse when all `*` on same option letter** | Prevents all-A quizzes at parse time (2+ choice questions, one correct position). |
| **Per-student MC shuffle client-side** | Shuffle `choice` options only; store `choiceOptionOrder` in attempt progress blob; submit still uses stable option ids (`a`,`b`,…). Seed = attempt id. |
| **Teacher preview stays author order** | No shuffle in `ExitTicketLivePreview` — easier to edit. |
| **Auto-activate Chase (CHASE1) + Student Tester on publish** | `sharedMultiSectionTesters.ts` / `useExitTicketAuthoring.ts`. |
| **Migration 058 pushed to Supabase** | `npm run db:push` succeeded in session (058 adds `page_group`, updates `get_quiz_questions`, `publish_exit_ticket`, `update_exit_ticket`). |

## 4. Rejected / do not rediscover

| Direction | Why |
|---|---|
| All correct answers as choice A in paste | Chase explicitly rejected; parser error + AI prompt rotation. |
| Shuffling **question** order | Chase wants identical problem sequence for all students. |
| Shuffling dropdown / short-answer options | Multiple choice only. |
| DB-side shuffle | Client + progress blob is enough; grading uses option ids not display letters. |
| Fixed letter "E" rule | Chase started "Although E should probably always be…" but did not finish — **no special E rule implemented**. Display letters A/B/C/D follow on-screen position after shuffle. |

## 5. Current implementation state

### Supabase (`student-session-kit`) — uncommitted, **pushed live**

- `supabase/migrations/058_question_page_group.sql` — `page_group` column; RPC updates.

### Macro App — uncommitted dirty

**Parser / publish**
- `renderer/src/utils/exit-ticket/parseQuizPaste.ts` — `---` breaks, `pageGroup`, all-same-letter rejection, `page_group` in publish payload.
- `renderer/src/utils/exit-ticket/groupQuizPages.ts` — group for preview.
- `renderer/src/utils/exit-ticket/serializeQuizToPaste.ts` — emits `---` between groups.
- `renderer/src/utils/exit-ticket/exitTicketAiPrompt.ts` — page breaks, rotated `*` examples, anti-all-A note.
- `renderer/src/utils/exit-ticket/questionsToUpdatePayload.ts` — `page_group` on edits.
- `electron-app/student-progress-sections.js` — `page_group` in list questions.

**Teacher UI**
- `ConsoleExitTicketsScreen.tsx`, `useExitTicketAuthoring.ts` — publish when Name empty fixed/disabled, Graded label, auto-activate testers, message slot.
- `ConsoleExitTicketQuizScreen.tsx`, `ExitTicketLivePreview.tsx` — multi-question preview, left numbers.
- `teacher-console-reports.css` — left-align preview prompts.
- `sharedMultiSectionTesters.ts`, `portalPreviewPersona.test.ts` — default access IDs.

**Tests:** `parseQuizPaste.test.ts` (17 pass), related payload tests updated.

**Machine-local (do not commit):** `config/d2l-courses.json` modified — stash per git rules.

### Student portal — uncommitted dirty

- `groupQuizPages.ts` — page grouping for quiz runner.
- `shuffleChoiceOptions.ts` + `.test.ts` — seeded per-student MC order (4 tests pass).
- `useGenericQuiz.ts` — pages + shuffle + progress persist `choiceOptionOrder`.
- `GenericQuizQuestionCard.tsx`, `GenericQuizView.tsx` — multi-question slides, numbered prompts.
- `quizContentService.ts` — `pageGroup` from RPC.
- `portal-base.css` — left-align, question number layout.

**Not deployed to Netlify** — students on production portal won't see changes until `deploy:prod` (only if Chase asks).

### Verification already done

- Macro App: `parseQuizPaste.test.ts` 17/17 pass.
- Student portal: `shuffleChoiceOptions.test.ts` + `quizAnswerState.test.ts` 7/7 pass.
- Supabase: migration 058 applied via `db:push`.

### Sample paste for Chase's domain/range quiz

Six questions, **Graded**, `---` between each function pair. Rotate `*` across lines (not all first):

```
Q: What is the domain of $y = -\sqrt{x - 2} - 4$?
* $[2,\infty)$
- $(-\infty,2]$
- $(2,\infty)$
Q: What is the range of $y = -\sqrt{x - 2} - 4$?
- $(-\infty,-4]$
* $[-4,\infty)$
- $(-\infty,\infty)$
---
Q: What is the domain of $y = 2(x - 4)^2 + 3$?
- $(-\infty,\infty)$
- $[3,\infty)$
* $[4,\infty)$
Q: What is the range of $y = 2(x - 4)^2 + 3$?
- $(-\\infty,3]$
* $[3,\infty)$
- $(4,\infty)$
---
Q: What is the domain of $y = \frac{-4}{x + 3} - 1$?
* $(-\infty,-3)\cup(-3,\infty)$
- $(-\infty,-3]$
- $[-3,\infty)$
Q: What is the range of $y = \frac{-4}{x + 3} - 1$?
- $(-\infty,-1)\cup(-1,\infty)$
* $(-\infty,-1]$
- $[-1,\infty)$
```

(Adjust `*` rotation as needed so parser accepts — not all on first line.)

**Publish checklist:** Name filled → Parse (no errors) → Preview shows **3 slides**, 2 questions each → Publish → Activate roster or rely on auto-activate for testers.

**Student access:** Exit tickets are opt-in (`055_exit_ticket_opt_in_access.sql`); preview bypasses access for instructor device.

## 6. Open questions and constraints

- **Portal deploy:** Required for student-facing slides, left-align, shuffle. Schema already live.
- **Macro App reload/rebuild:** Required for Teacher Console parse/publish/preview changes.
- **"E should always be…"** — unfinished thought; no implementation. Ask Chase if he meant a fixed last option (e.g. "None of the above").
- **No commit/push** unless Chase says "put on GitHub" or end-of-session.
- **Never launch GUI without asking** — hand Chase test steps instead.
- **Context-heavy session** — fresh task recommended for unrelated work.

## 7. Exact next step

1. **Deploy student portal** (`student-portal`, production deploy per pipeline doc) so shuffle + multi-question slides work for students.
2. **Chase reloads Macro App**, pastes the domain/range quiz (with `---` and rotated `*`), Parse → Publish with a name.
3. **Smoke test as Student Tester** in portal: 3 slides, left numbers, different MC order than teacher preview, submit grades correctly.

If deploy is out of scope for the fresh agent, start with: confirm portal deploy status, then walk Chase through republish + student preview verification.
