# Teacher Console — exit-ticket survey statistics (instructor view)

> **Exemplar:** M2412 **Portal Check** / **Math App Survey** (ungraded exit ticket in the
> student portal). Chase approved this layout 2026-10-12 for reading class survey results in
> Macro App, not for anonymous “share with the class” slides.

---

## Why this exists

Exit-ticket activities double as **class surveys**. The old Statistics view squeezed every
question into a 3-column grid with **stacked horizontal bars** and (for text) **lumped
identical answers** — hard to scan and useless when Chase needs **names** for follow-up.

This recipe is the **template** for future portal surveys: one full-width card per question,
visualization chosen by **question type** and **sort order**, roster names where instructor
action is needed.

---

## Where the text lives

| Layer | What it holds |
|---|---|
| **Supabase `questions` table** | Live copy students see — edited in **Teacher Console → Exit Tickets**. |
| **Git snapshot (exit tickets only)** | `School Scrips/Macro App/content/exit-tickets/*.txt` — written automatically on every successful **Save** or **Publish**. Exemplar: `exit-ticket__2403341a-e212-4677-b4be-9afc7448e521.txt` (**Studying Survey**, M2412). |
| **Built-in portal surveys** | TypeScript `*Copy.ts` files in student-portal — see [portal-survey-copy-index.md](./portal-survey-copy-index.md). |

Backfill snapshots for a section: `node scripts/snapshot-exit-tickets-for-section.js "MATH-2412 4101 1"` from Macro App root.

---

## Where to open it

1. Macro App → **Teacher Console** → course (e.g. M2412).
2. Activity: **Portal Check** / **Math App Survey** (exit-ticket kind).
3. **Responses** workspace → toggle **Statistics** (not the side “Response summary” panel on
   Responses — that still uses the older horizontal bar layout for quick glance).

Entry component: `ActivityResponseStatisticsPanel` → `ExitTicketChoiceStatisticsPanel`.

---

## Data pipeline (do not duplicate)

| Step | Owner |
|---|---|
| Load attempts + per-slot answers | `useExitTicketResponseReport` |
| Aggregate counts + `respondents[]` per option | `buildExitTicketResponseSummary` |
| Per-student text for free-response | `exitTicketSurveyTextRows` |
| Render | `ExitTicketChoiceStatisticsPanel` |

**Non-negotiable:** extend this pipeline — do not add a second Supabase read or parallel
summary builder for the same activity.

---

## Visualization rules (template)

Questions are **`sortOrder` 0-based** (displayed as Q1 = `sortOrder 0`, Q5 = `sortOrder 4`).

| Condition | View | Component |
|---|---|---|
| `questionType === 'text'` | Each answer + **student name** (separate cards, `pre-wrap`) | `ExitTicketSurveyTextResponses` |
| `questionType === 'select'` **or** `sortOrder === 1` | Options **ranked by count** (high → low), label + number | `ExitTicketChoiceRankList` |
| `choice` / `multi`, not rank slot | **Vertical bar chart** — columns **A, B, C…**, counts on top; full option text in side legend | `ExitTicketMcqVerticalBarChart` |
| Same as above + **`sortOrder === 4`** (Q5) | Vertical bars **plus** name lists for options whose labels match **Strongly disagree** / **Disagree** (Likert follow-up) | `ExitTicketSurveyNegativeFollowUp` |
| Anything else (fallback) | Legacy stacked horizontal bar | `ExitTicketMcqDistributionChart` |

**M2412 Portal Check mapping (as designed 2026-10-12):**

| Q# | `sortOrder` | Intended shape |
|---|---|---|
| Q1 | 0 | Vertical MCQ bars + A/B/C/D legend |
| Q2 | 1 | Ranked list |
| Q3 | 2 | Text (must be `questionType: text` in editor) |
| Q4 | 3 | Vertical MCQ bars |
| Q5 | 4 | Vertical MCQ bars + disagree / strongly disagree name lists |

If a future survey uses a **different** slot for rank or Likert follow-up, adjust the
`sortOrder` checks in `ExitTicketChoiceStatisticsPanel` (`useRankedMcqView`, Q5 follow-up)
or introduce a small config map keyed by `activityId` — **one** place, not a second chart
component.

---

## Layout and CSS

- **Full width:** stacked cards (`.exit-ticket-choice-statistics__stack`), not the old
  `max-width: 840px` three-column grid.
- Styles: `School Scrips/Macro App/renderer/src/styles/exit-ticket-survey-statistics.css`
  (imported from `teacherConsoleEntry.ts`).
- Shared MCQ tokens still live in `teacher-console-response-statistics.css` for other tabs.

---

## Exemplar files (copy this shape)

| File | Role |
|---|---|
| `renderer/src/components/teacher-console/exit-tickets/ExitTicketChoiceStatisticsPanel.tsx` | Orchestrates per-question view |
| `renderer/src/components/teacher-console/exit-tickets/ExitTicketMcqVerticalBarChart.tsx` | Q1/Q4/Q5-style MCQ |
| `renderer/src/components/teacher-console/exit-tickets/ExitTicketChoiceRankList.tsx` | Q2-style rank |
| `renderer/src/components/teacher-console/exit-tickets/ExitTicketSurveyTextResponses.tsx` | Q3-style text + names |
| `renderer/src/components/teacher-console/exit-tickets/ExitTicketSurveyNegativeFollowUp.tsx` | Q5 disagree lists |
| `renderer/src/utils/exit-ticket/exitTicketSurveyTextRows.ts` | Text rows from attempt cells |
| `renderer/src/utils/exit-ticket/buildExitTicketResponseSummary.ts` | Counts + respondents |

Tests: `buildExitTicketResponseSummary.test.ts` (aggregates); add tests if you change rank or
text row behavior.

---

## Anti-patterns

- **Anonymous header on instructor Statistics** — this view is for Chase’s roster follow-up;
  do not revert to “safe to share with the class” unless building a separate export view.
- **Second chart system** for the same exit ticket — extend the panel/components above.
- **Hardcoding survey prompts in React** — prompts render from loaded `questions`; only
  `sortOrder` / `questionType` drive layout.
- **Text question as choice with “Other”** — use `text` type so Q3 gets one row per student.

---

## Adding a new class survey

1. Publish exit ticket in TC (ungraded if it is a survey).
2. Order questions in the editor — **`sortOrder` matches the table above** if you want the
   same visuals without code changes.
3. Use **`text`** for free response; **`select`** or slot 2 (`sortOrder 1`) for “pick one,
   show me rank”; **`choice`** for A/B/C/D vertical bars.
4. For Likert Q5-style follow-up, use option labels that include **Disagree** / **Strongly
   disagree** (matcher in `ExitTicketSurveyNegativeFollowUp.tsx`) or extend that matcher once.

---

## Related

- Exit ticket authoring paste format: `renderer/src/utils/exit-ticket/exitTicketAiPrompt.ts`
- Pipeline overview: `School Scrips/student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md`
- Response grid layout: [report-grid-layout.md](./report-grid-layout.md)
