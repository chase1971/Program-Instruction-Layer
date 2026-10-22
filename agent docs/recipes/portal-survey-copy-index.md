# Portal survey copy — where question text lives

Students see survey prompts from **two different systems**. This index is the single map so
agents and Chase know where to read or archive wording.

---

## 1. Teacher Console exit tickets (Supabase + git snapshot)

**Examples:** Studying Survey, Portal Check / Math App Survey, exit tickets, ungraded class surveys.

| Layer | Location |
|---|---|
| **Live (what students get)** | Supabase `questions` rows for `activity_id` like `exit-ticket/…` |
| **Edit UI** | Macro App → Teacher Console → Exit Tickets |
| **Git copy (after Save/Publish)** | `School Scrips/Macro App/content/exit-tickets/*.txt` — auto-written on successful save |
| **Backfill all tickets in a section** | `node scripts/snapshot-exit-tickets-for-section.js "<section code>"` from Macro App root |
| **Statistics layout recipe** | [teacher-console-exit-ticket-survey-statistics.md](./teacher-console-exit-ticket-survey-statistics.md) |

Implementation: `electron-app/exit-ticket-content-snapshot.js` (called from `updateExitTicket` /
`publishExitTicket` in `student-progress-sections.js`).

---

## 2. Code-owned surveys (student-portal TypeScript)

**Examples:** Logic homework post-survey, Transformations identifying/graphing post-surveys,
Guided Practice post-survey, one-question “helpful?” surveys on video galleries.

| Survey | Copy owner file | Activity id (Supabase) |
|---|---|---|
| Logic post-survey | `student-portal/src/features/logic-homework/logicPostSurvey/logicPostSurveyCopy.ts` | `logic/post-survey` |
| Transformations identifying | `…/identifyingPostSurvey/identifyingPostSurveyCopy.ts` | `transformations/identifying-post-survey` |
| Transformations graphing | `…/graphingPostSurvey/graphingPostSurveyCopy.ts` | `transformations/graphing-post-survey` |
| Guided Practice | `…/guided-practice/guidedPracticePostSurveyCopy.ts` | `matrix/guided-practice-survey` |
| Gauss-Jordan homework | `…/guided-practice/guidedPracticeHomeworkSurveyCopy.ts` | `matrix/gauss-jordan-homework-survey` |
| Vector projections helpful | `…/video-examples/VectorProjectionsHelpfulSurvey.tsx` (inline options) | `precalc/vector-projections-helpful-survey` |
| Conics helpful | `…/ConicsHelpfulSurvey.tsx` | `precalc/conics-helpful-survey` |
| Domain & range examples helpful | `…/DomainRangeExamplesHelpfulSurvey.tsx` | `reference/domain-range-examples-helpful-survey` |
| Logic Gates extra credit enjoy | `…/logic-homework/logicGatesEnjoySurveyCopy.ts` | `logic/gates-extra-credit-enjoy-survey` |

To change wording: edit the **copy file**, ship portal (+ kit migration if RPC/options change).
Macro App statistics for those apps read attempts from Supabase but **labels** often come from
the same copy files or report utils under `Macro App/renderer/src/utils/…Report/`.

---

## Anti-pattern

Do not duplicate exit-ticket prompts in markdown “for convenience” without syncing — use
`content/exit-tickets/*.txt` after save, or the code-owned `*Copy.ts` file for built-in surveys.
