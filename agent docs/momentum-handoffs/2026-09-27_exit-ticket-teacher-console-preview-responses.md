# Momentum handoff — Exit ticket teacher console (preview, responses, parse UX)

**Written:** 2026-09-27 · **Apps:** `School Scrips/Macro App` · `School Scrips/student-portal` · `School Scrips/student-session-kit`

---

## Read first

1. **`School Scrips/Macro App/AGENTS.md`** — exit ticket keyword rows.
2. **`School Scrips/student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md`** — attempt policy, paste format (`P:`, `---`, `!` locked options).
3. **`School Scrips/Macro App/renderer/src/utils/exit-ticket/exitTicketAiPrompt.ts`** — authoritative Give-to-AI paste template.
4. This file § Exact next step.

---

## Objective and current phase

Chase is running **graded domain/range exit tickets** (square root, quadratic vertex form, rational) through Macro App Teacher Console: **paste → Parse → publish/edit → review tester/student responses**.

**This session shipped:**

- **`!` locked last option** — `! I don't know how to do this` stays last while math options shuffle (parser, serialize, publish payload, portal shuffle).
- **Paste toolbar** — one row: **Give to AI | Parse | Format rules** (modal documents `P:`, `---`, `*`, `!`).
- **Statistics tab** — anonymous per-question MC histograms (no student names); correct answer green on graded quizzes.
- **Responses grid** — scored cells use **●** on green/red backgrounds (not ✓/✗).
- **Testers on Responses grid** — CHASE1 + Student Tester W8K2P4 now appear (uses `buildAppCompletionRosterStudents()` like app-completion grids).
- **Tester name → Reset data** — click last/first name on tester rows opens menu to clear that tester's attempts for **this activity only** (normal + transposed grids).
- **Preview layout** — phone mockup ~**half width**, **centered**, empty left/right columns reserved for future side content.
- **Preview vertical fit** — tighter padding (~75px saved), viewport-constrained column so **Save/Publish stays visible**; left builder scrolls instead of pushing buttons off screen.
- **Parse feedback** — brief **blue border flash** on preview card when Parse runs (including empty state).

**Phase:** Code is **local and largely uncommitted**. Supabase migrations **059** (retake/revision) and **060** (page_header) are **pushed live**. **Student portal not deployed** — production students do not see retake/revision/shuffle/locked-option behavior until `npm run deploy:prod`.

---

## Chase's desired feel

- **Two questions per slide** (domain + range) with **problem at top** (`P:`), not repeated in each prompt.
- **Five MC options:** four math answers + last line always **I don't know how to do this** — prefix with **`!`** so it never shuffles away from the bottom.
- **Parse should feel like it did something** — visual flash on the preview side, not a toast or "Copied!" text.
- **Preview should not eat the screen** — half-width centered phone mockup; room on the sides for things he may add later; Save button must stay on screen without scrolling the whole app.
- **Retakes for practice** unless he toggles restrict; testers redo freely; edit while live bumps `content_revision`.
- **Statistics anonymous** — histograms only, no student names on that tab.
- Speech-to-text user — one focused question when ambiguous; no typing-heavy flows; **never launch GUI / open browser** without asking.

---

## Accepted decisions

| Decision | Why |
|---|---|
| `!` prefix → `locked: true` on option | "I don't know" stays last; math options still shuffle |
| Portal `shuffleChoiceOptions` respects `locked` | Student-facing order matches intent |
| Paste toolbar: Give to AI \| Parse \| Format rules | Three buttons in one row under textarea |
| Preview stage: `1fr \| center(50%, 22rem) \| 1fr` grid | Centered half-width preview + side space for later |
| Parse flash via `previewFlashKey` counter + CSS animation | Chase asked for visible feedback without ephemeral text |
| Left builder column scrolls; preview column height-capped | Keeps Save/Publish visible |
| Responses use `buildAppCompletionRosterStudents()` | Includes universal testers CHASE1 + W8K2P4 |
| Tester name click → Reset data (this activity only) | Smoke testing without full tester wipe |
| Statistics: `ExitTicketChoiceStatisticsPanel` + stacked bar charts | Anonymous distribution per question |
| Scored cells: ● on green/red | Chase preference over ✓/✗ |
| Retake/revision/`restrict_after_submit` model (prior session) | Still in effect — see pipeline doc |
| `P:` → `page_header`; `---` → shared slide | Problem once at top, domain + range below |

---

## Rejected directions — do not rediscover

| Direction | Why |
|---|---|
| Three math options only | Quizzes use **five** lines; parser always supported 2–6 |
| Toast / "Parsed!" confirmation text | Chase wants flash on preview, not ephemeral feedback text |
| Full-width preview in edit workspace | Chase asked to shrink and center (~half) with side room |
| Re-implement five-option MC or locked shuffle | Already done end-to-end |
| Student names on Statistics tab | Anonymous histograms only |
| Passing bare `onClick={openExitTicketCreate}` | Passes event → `editActivityId?.trim is not a function`; wrap `() => openExitTicketCreate()` |
| Portal deploy without Chase asking | Not deployed this session |

---

## Current implementation state

### Supabase (`student-session-kit`) — migration files may be uncommitted, **pushed live**

- `059_exit_ticket_retakes_and_revision.sql` — `restrict_after_submit`, `content_revision`, republish RPC.
- `060_question_page_header.sql` — `page_header` column.

### Macro App — uncommitted dirty

**Parser / publish**
- `parseQuizPaste.ts`, `serializeQuizToPaste.ts`, `questionsToUpdatePayload.ts`, `exitTicketsService.ts` — `locked` on options.
- `exitTicketAiPrompt.ts`, `exitTicketPasteRules.ts` — `!` documented.
- `ExitTicketPasteToolbar.tsx`, `ExitTicketPasteRulesModal.tsx`.

**Preview / workspace**
- `ExitTicketLivePreview.tsx` — `parseFlashKey` flash animation.
- `ConsoleExitTicketsScreen.tsx` — `ExitTicketPreviewColumn` with preview stage wrapper.
- `ConsoleExitTicketQuizScreen.tsx` — same stage layout.
- `useExitTicketAuthoring.ts`, `useExitTicketQuizEdit.ts` — `previewFlashKey` bumps on Parse.
- CSS: `teacher-console-reports.css` (stage grid, compact padding, flash keyframes, scroll containment), `teacher-console-workspaces.css`.

**Responses / statistics**
- `useExitTicketResponseReport.ts` — roster via `buildAppCompletionRosterStudents()`.
- `ExitTicketResponseGrid.tsx`, `ExitTicketResponseTransposedGrid.tsx`, `ExitTicketResponseCell.tsx`.
- `ExitTicketResponseStudentRowGroup.tsx`, `ExitTicketResponseTesterNameMenuPanel.tsx`, `ExitTicketResponseTransposedStudentHeader.tsx`.
- `ExitTicketChoiceStatisticsPanel.tsx`, `ExitTicketMcqDistributionChart.tsx`.
- `ActivityResponsesPanel.tsx`, `ActivityResponseStatisticsPanel.tsx`.

**Tests passing (local):** `parseQuizPaste.test.ts` (20), `shuffleChoiceOptions.test.ts` (5), `useExitTicketResponseReport` tests updated.

**Machine-local (do not commit):** `config/d2l-courses.json` if dirty.

### Student portal — uncommitted dirty, **NOT deployed**

- `shuffleChoiceOptions.ts` (+ test) — locked options stay at original index.
- `quizContentService.ts` — passes `locked` through.
- Prior session: `exitTicketRetake.ts`, revision/restrict, slide headers, `groupQuizPages.ts`.

### Domain/range quiz paste (Chase's current shape)

Graded, 3 slides, `P:` + domain + range per slide, **5 options** each — last line **`! I don't know how to do this`**. Full example in `exitTicketAiPrompt.ts`. Parse → 3 slides, 2 questions each, A–E with last option locked.

---

## Open questions and constraints

- **Side columns** on preview stage are empty placeholders — Chase may add content later; nothing specified yet.
- **Portal deploy** when Chase asks — required for student-facing shuffle/locked/retake/revision.
- **No commit/push** unless Chase says "put on GitHub" or end-of-session.
- **Never launch GUI / open browser** without asking — hand flat reload/test steps.
- Chase has **not** smoke-tested this session's preview flash + vertical fit after reload — verification pending on his machine.

---

## Exact next step

1. **Chase reloads Macro App** → Manage Class → exit ticket edit: confirm half-width centered preview, Parse flash on click, Save/Publish visible without scrolling past the window.
2. **Re-paste domain/range quiz** with `!` on all six "I don't know" lines → Parse (watch flash) → Save.
3. **Testers → Responses:** CHASE1 + Student Tester visible; click tester name → Reset data works.
4. **Statistics tab:** six anonymous histogram charts.
5. When Chase asks: **`npm run deploy:prod`** in `student-portal` for production parity.

If continuing code: ask Chase what he wants in the preview side columns, or pick up any polish he reports after reload.
