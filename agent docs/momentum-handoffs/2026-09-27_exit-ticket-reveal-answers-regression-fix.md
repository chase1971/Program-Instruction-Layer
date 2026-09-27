# Momentum handoff — Exit ticket teacher console (reveal answers, LaTeX, regression fix)

**Written:** 2026-09-27 · **Apps:** `School Scrips/Macro App` · `School Scrips/student-portal` · `School Scrips/student-session-kit`

---

## Read first

1. **`School Scrips/Macro App/AGENTS.md`** — exit ticket keyword rows.
2. **`School Scrips/student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md`** — attempt policy, paste format (`P:`, `---`, `!`), **`reveal_correct_answers`** (migration 061).
3. **`School Scrips/student-session-kit/supabase/migrations/061_reveal_correct_answers.sql`** — column + RPC changes for reveal flow.
4. **`School Scrips/Macro App/renderer/src/utils/exit-ticket/exitTicketAiPrompt.ts`** — authoritative Give-to-AI paste template.
5. This file § Exact next step.

---

## Objective and current phase

Chase is running **graded domain/range exit tickets** and **Math Survey** through Macro App Teacher Console: paste → Parse → publish/edit → review tester/student responses and statistics.

**Phase:** Feature work is **implemented locally and largely uncommitted**. Migrations **059** and **060** are **pushed live**. Migration **061** (`reveal_correct_answers`) is **written but NOT pushed**. **Student portal not deployed.**

**Chase confirmed (this session):** Domain/range exit ticket and Math Survey **reappeared** in Manage Class and Responses after Macro App restart + list-query regression fix.

---

## Chase's desired feel

- **Two questions per slide** (domain + range) with **problem at top** (`P:`), not repeated in each prompt.
- **Five MC options:** four math answers + last line always **I don't know how to do this** — prefix with **`!`** so it never shuffles away from the bottom.
- **Parse should feel like it did something** — brief **blue border flash** on preview card when Parse runs.
- **Preview ~half width, centered** — room on sides for future content; **Save/Publish stays visible** without scrolling the whole app.
- **Statistics anonymous** — histograms only, no student names on that tab.
- **Responses grid full width** — no sidebar summary panel; charts live **only on Statistics tab**.
- **Graded results screen:** default **Scores only**; optional **Reveal correct answers** lets students tap any question row to review their pick vs the correct answer.
- **LaTeX in prompts/options** should render in Macro preview and statistics charts (KaTeX via `MathText`).
- Speech-to-text user — one focused question when ambiguous; no typing-heavy flows; **never launch GUI / open browser** without asking.

---

## Accepted decisions

| Decision | Why |
|---|---|
| `!` prefix → `locked: true` on option | "I don't know" stays last; math options still shuffle |
| Portal `shuffleChoiceOptions` respects `locked` | Student-facing order matches intent |
| Paste toolbar: Give to AI \| Parse \| Format rules | Three buttons in one row under textarea |
| Preview stage: half-width centered phone mockup | Side space reserved for later |
| Parse flash via `previewFlashKey` + CSS animation | Visible feedback without ephemeral text |
| Responses use `buildAppCompletionRosterStudents()` | Includes universal testers CHASE1 + W8K2P4 |
| Statistics: `ExitTicketChoiceStatisticsPanel` + stacked bar charts | Anonymous distribution per question |
| Scored cells: ● on green/red | Chase preference over ✓/✗ |
| **`reveal_correct_answers` column + RPC flag** | Teacher toggle in `ExitTicketPolicyControls`; submit returns `correct_option_id` when ON |
| **Removed `ExitTicketResponseSummaryPanel`** from Responses | Charts only on Statistics; Responses is full-width grid |
| **`MathText` + KaTeX** in Macro preview + statistics | LaTeX in teacher-facing views |
| **`GenericQuizQuestionReview`** in student portal | Clickable all-question rows on results when reveal ON |
| **List query backward-compatible fallback** | `fetchExitTicketActivityRows()` tries `reveal_correct_answers`, falls back without column if migration 061 not live |

---

## Rejected directions — do not rediscover

| Direction | Why |
|---|---|
| Toast / "Parsed!" confirmation text | Chase wants flash on preview, not ephemeral feedback |
| Full-width preview in edit workspace | Chase asked to shrink and center (~half) |
| Student names on Statistics tab | Anonymous histograms only |
| **`ExitTicketResponseSummaryPanel` on Responses tab** | Removed this session — statistics only |
| **`reveal_correct_answers` in REST select with no fallback** | Broke entire ticket list when migration 061 not applied — only Matrix Tutorial + Guided Practice showed |
| Portal deploy without Chase asking | Not deployed this session |
| Passing bare `onClick={openExitTicketCreate}` | Wrap `() => openExitTicketCreate()` |

---

## Current implementation state

### Regression fix (verified by Chase)

**Symptom:** Domain/range exit ticket + Math Survey vanished from Manage Class and Responses activity picker; only **2 built-in M1324 activities** visible. Students could still take tickets in portal.

**Cause:** `listExitTickets` REST select included `reveal_correct_answers` before migration **061** was applied → query failed → empty ticket list.

**Fix:** `fetchExitTicketActivityRows()` in `electron-app/student-progress-sections.js` — try full select, catch and retry without `reveal_correct_answers`; default `revealCorrectAnswers: false` on fallback rows.

### Supabase (`student-session-kit`)

| Migration | Status |
|---|---|
| 059 retakes/revision | Pushed live |
| 060 page_header | Pushed live |
| **061 reveal_correct_answers** | **File exists, NOT pushed** — required for reveal toggle save + student review + list query without fallback |

### Macro App — uncommitted dirty

**Reveal answers / policy**
- `ExitTicketPolicyControls.tsx` — Results screen: Scores only vs Reveal correct answers (graded only)
- Wired: `useExitTicketAuthoring.ts`, `useExitTicketQuizEdit.ts`, `exitTicketsService.ts`, `student-progress-sections.js` (publish/update RPC params)
- `MathText.tsx` + test; used in `ExitTicketLivePreview.tsx`, `ExitTicketChoiceStatisticsPanel.tsx`, `ExitTicketMcqDistributionChart.tsx`

**Responses / statistics**
- `ActivityResponsesPanel.tsx`, `ConsoleExitTicketResponseScreen.tsx` — **no** summary sidebar; full-width grid
- Deleted: `ExitTicketResponseSummaryPanel.tsx`, `ExitTicketResponseCountTooltip.tsx`
- Statistics unchanged: anonymous MC histograms

**Prior session work still in tree:** paste toolbar, `!` locked options, preview layout/flash, tester roster, tester Reset data, etc.

**Tests:** `MathText.test.ts` passes locally.

**Machine-local (do not commit):** `config/d2l-courses.json` if dirty.

### Student portal — uncommitted dirty, **NOT deployed**

- `GenericQuizQuestionReview.tsx`, `GenericQuizResult.tsx`, `GenericQuizView.tsx` — reveal flow
- `quizContentService.ts` — `revealCorrectAnswers`, `correctOptionId` on submit rows
- Review CSS in `portal-features.css`
- Prior: shuffle/locked, retake/revision, slide headers

**Portal vitest:** failed globally in agent environment (`Cannot read properties of undefined (reading 'config')`) — env issue, not verified locally.

---

## Open questions and constraints

- **Push migration 061** before reveal toggle / save-with-reveal / student review can work end-to-end. List works without it (fallback); publish/update RPC **does** pass `p_reveal_correct_answers` — saving with reveal ON may fail until 061 is live.
- **Portal deploy** (`npm run deploy:prod`) when Chase asks — required for student-facing reveal + shuffle/locked/retake.
- **No commit/push** unless Chase says "put on GitHub" or end-of-session.
- **Never launch GUI / open browser** without asking.
- Chase has **not** smoke-tested reveal toggle, LaTeX preview, or portal review flow after this session's changes.

---

## Exact next step

1. **Push migration 061** to Supabase (`student-session-kit/supabase/migrations/061_reveal_correct_answers.sql`).
2. **Chase reloads Macro App** → open graded domain/range ticket → confirm **Results screen** toggle (Scores only / Reveal correct answers) saves without error.
3. **Preview with LaTeX** in a prompt — confirm KaTeX renders in live preview and Statistics charts.
4. When Chase asks: **`npm run deploy:prod`** in `student-portal` → Student Tester completes graded ticket with reveal ON → tap question row on results → review shows pick vs correct answer.
5. If Chase wants GitHub sync: commit/push all three repos (Macro App, student-session-kit, student-portal) — large uncommitted surface across sessions.
