# Momentum handoff — Exit ticket edit, retake policy, unified workspace

**Written:** 2026-09-27 · **Apps:** `School Scrips/Macro App` · `School Scrips/student-portal` · `School Scrips/student-session-kit`

## Read first

1. **`School Scrips/Macro App/AGENTS.md`** — exit ticket keyword rows (edit/retake, paste format).
2. **`School Scrips/student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md`** — § Attempt policy, § Paste-to-create (P:, ---, five-option MC).
3. **`School Scrips/Macro App/renderer/src/utils/exit-ticket/exitTicketAiPrompt.ts`** — Give to AI template (authoritative paste rules).
4. This file § 7 for the exact next step.

## 1. Objective and current phase

Chase is running **graded domain/range exit tickets** (square root, quadratic vertex form, rational) via Macro App Teacher Console **paste → parse → publish/edit**. Session shipped:

- **Retake model:** retakes default ON; optional **Restrict to one submission**; testers + CHASE1 always redo; **content_revision** bump on save starts a fresh round.
- **Unified workspace:** side dropdown picker, inline edit while published, Save / Unpublish / Republish.
- **`P:` slide headers:** equation once at top of slide; domain + range questions below on same slide.
- **Layout fixes:** full-width two-column builder/preview; back button width fix (was stretched by flex `align-items: stretch`).

**Phase:** Code is **local and largely uncommitted**. Supabase migrations **059** (retake/revision) and **060** (page_header) are **pushed live**. **Student portal not deployed** — production students do not see retake/revision/P: behavior until `npm run deploy:prod`.

## 2. Chase's desired feel

- **Two questions per slide** (domain + range) with **problem at top** (`P:`), not repeated in each question prompt.
- **Five multiple-choice options:** four math answers + last line always **I don't know how to do this** (never starred). Chase corrected agent that shortening to three options was wrong — parser always supported 2–6; only the **paste text** was wrong.
- **Retakes for practice** unless he toggles restrict; **First attempt counts** = first completed attempt at **current content_revision**.
- **Testers redo freely** for smoke tests without Teacher Console reset.
- **Edit while live** — no unpublish required; Save bumps revision.
- **Manage activities screen** — equal-width edit + preview columns; **Back to manage class** button compact (content-width), not full-bleed.
- Speech-to-text user — one focused question when ambiguous; no typing-heavy flows; never launch GUI without asking.

## 3. Accepted decisions

| Decision | Why |
|---|---|
| `restrict_after_submit` default **false** | Retakes allowed unless Chase restricts |
| `content_revision` increment on every **update_exit_ticket** save | Edit = fresh round; old attempts kept in DB |
| Testers + `is_instructor` bypass restrict + tile hide | Smoke testing without manual reset |
| `---` page break; questions before next `---` share one slide | Two related questions per panel |
| `P:` line → `page_header` on first question of slide | Problem shown once at top |
| Remove migration 057 post-submit edit locks | Chase chose edit > protecting in-flight attempts |
| Side dropdown ticket picker (not full-width list above builder) | Less crushing the builder |
| Republish RPC + button | Unpublish is not a dead end |
| Graded MC: rotate `*` among math lines; reject all-correct = A | Anti pattern-matching |
| Last option: `- I don't know how to do this` on graded math quizzes | Chase's standard five-option shape |

## 4. Rejected / do not rediscover

| Direction | Why |
|---|---|
| Three math options only | Chase's quizzes use **five** lines; agent error in handoff sample, not app limit |
| Treat `once` attempt_policy as UI lockout by default | Split into recording vs `restrict_after_submit` |
| Full-width **Back to manage class** button | Caused by `align-items: stretch` on flex shell — use `flex-start` + `width: 100%` on screen only |
| Outer `teacher-console-exit-layout` 2-col grid with one child | Squished layout to half width — builder-row is the grid now |
| Passing `onClick={openExitTicketCreate}` bare | Passes click **event** → `editActivityId?.trim is not a function`; wrap `() => openExitTicketCreate()` |
| Code changes to "enable" five options | Parser already supported them |

## 5. Current implementation state

### Supabase (`student-session-kit`) — migration files uncommitted, **pushed live**

- `059_exit_ticket_retakes_and_revision.sql` — `restrict_after_submit`, `content_revision`, RPC updates, republish.
- `060_question_page_header.sql` — `page_header` column; get/publish/update RPCs.

### Macro App — uncommitted dirty

**Navigation / workspace**
- `useTeacherConsoleNavigation.ts` — merge edit into create screen; safe string normalize for `editActivityId`.
- `ConsoleManageClassScreen.tsx` — `onClick={() => onOpenExitTicketCreate()}`.
- `ConsoleExitTicketsScreen.tsx` — unified workspace; direct `teacher-console-exit-builder-row` (no broken outer grid).
- CSS: `teacher-console-reports.css`, `teacher-console-grades.css`, `teacher-console-workspaces.css` (layout + back button).

**Parser / publish**
- `parseQuizPaste.ts` — `P:` → `pageHeader`; `---` → `pageGroup`.
- `exitTicketAiPrompt.ts` — P:, ---, five-option + I don't know convention.
- `ExitTicketLivePreview.tsx`, portal `GenericQuizQuestionCard.tsx` — render slide header.
- Hooks: `useExitTicketAuthoring`, `useExitTicketQuizEdit`, policy controls, ticket picker.

**Tests:** Macro renderer vitest pass; portal 97 tests pass (local).

**Machine-local (do not commit):** `config/d2l-courses.json` if dirty.

### Student portal — uncommitted dirty, **NOT deployed**

- `exitTicketRetake.ts`, `classworkData.ts`, `GenericQuizView.tsx`, `formatAttemptScore.ts`, `quizContentService.ts` — revision + restrict + tester bypass.
- `groupQuizPages.ts`, slide header display.

### Docs touched (uncommitted)

- `STUDENT_PROGRESS_PIPELINE.md` § Attempt policy + paste slide table.
- `Macro App/AGENTS.md` keyword rows.

### Domain/range quiz paste (Chase's current shape)

Graded, 3 slides, `P:` + domain + range per slide, **5 options** each (last = I don't know how to do this). Full paste is in `exitTicketAiPrompt.ts` example block — or Chase's last chat copy. Parse → **3 slides**, 2 questions each, **A–E**.

## 6. Open questions and constraints

- **Portal deploy** when Chase asks — required for student-facing retake/revision/P: headers/shuffle.
- **Macro App reload** after CSS/navigation fixes (back button, layout).
- **No commit/push** unless Chase says "put on GitHub" or end-of-session.
- **Never launch GUI / open browser** without asking — hand flat test steps.
- Chase wants to **document paste conventions** — started in pipeline + exitTicketAiPrompt; not a separate doc file unless he asks.

## 7. Exact next step

1. **Chase reloads Macro App** — confirm **Back to manage class** is compact and exit-ticket workspace is full-width two columns.
2. **Paste corrected five-option domain/range quiz** (with `P:` and `---`) → Parse → Save on existing ticket or Publish new → smoke as Student Tester (`/?s=W8K2P4`): retake visible, 3 slides, 5 options, problem at top.
3. When ready: **`npm run deploy:prod`** in `student-portal` so production matches local retake/revision behavior.

If continuing code work: verify portal deploy status first; do not re-implement five-option support (already works).
