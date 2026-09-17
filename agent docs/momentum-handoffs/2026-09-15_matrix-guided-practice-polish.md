# Momentum handoff — Gauss-Jordan Guided Practice (first-column UI done, recording next)

**Written:** 2026-09-15 (Tuesday, evening)

---

## 1. Objective and current phase

Chase is building **Gauss-Jordan Method Practice** as a **separate Student Portal activity**
(`matrix/guided-practice`) — not a modification of the existing Matrix Tutorial. Students walk
through row reduction with guided questions at each step, using **token keypads** (not OS
keyboard) for numbers/fractions and row-op notation.

**Phase:** **First-column practice UI is working in portal preview** (2 operations → 10
questions). Headless engine + tests pass. **Attempt recording to Supabase is not wired yet.**
Full RREF (columns 2+) is intentionally deferred — session hook caps at
`FIRST_COLUMN_OPERATION_COUNT = 2`.

**Fixed test problem** (engine default):
```
[3  -1 | 7]
[2   1 | 3]
```
Solution x=2, y=−1. First pivot 3 → scale by 1/3 immediately.

---

## 2. Chase's desired feel

- **Match Part 3 tutorial layout** — same matrix positioning, row-op buttons at y=112, tutorial
  popover at y=152, portal `matrix-guided-practice-inset` CSS (same vars as
  `matrix-tutorial-part3-inset`).
- **Dwell-click** — big targets, token keypads on the far right; no OS keyboard for inputs.
- **Tutorial box** — same spot as Part 3; wrong answers show **Incorrect.** inline with reasoning
  (no line break after "Incorrect."); **never flash/highlight the correct cell** on wrong pick —
  all cells keep pulsing for retry.
- **Correct answers** — green check flash beside matrix (`CorrectCheckFlash`, 700ms) then advance
  (same as tutorial Part 3).
- **Dev nav only** — Back/Next above workspace (tutorial nav chrome); **Next always unlocked**,
  auto-applies matrix state when skipping; not for student-facing final UX.
- **Brackets** — lighter Part 1/2 style (6px SVG, strokeWidth 2), not Part 3 thick brackets.
- **Separate from tutorial** — home menu card like Fractions/Logic; tutorial may get a second
  button later.
- **Never launch GUI** without asking; hand off visible tests to Chase.

---

## 3. Accepted decisions

| Decision | Detail |
|---|---|
| **New engine, not tutorial hardcode** | Pure TS under `Matrix app/src/app/engine/` — exact rationals, algorithmic steps |
| **Question script** | 5 questions per row op: pick-cell → target-value → operation-type → multiplier/notation → row-entry |
| **Builders** | `BuilderPanel` far right — value mode + row-op mode; matrix entry grid for row-entry step |
| **Activity id** | `matrix/guided-practice`; migration `041_matrix_guided_practice.sql` (20 items) |
| **Portal route** | `matrix-guided-practice` via `GuidedPracticeView` / `GuidedPracticeEntry` |
| **Wrong feedback** | `wrongHint` on each `PracticeQuestion`; overlay replaces prompt when wrong |
| **Popover width** | Part 3 bases + **50px extra** (`GUIDED_PRACTICE_POPOVER_WIDTH_EXTRA`) |
| **Scope cap** | First column only until polish + recording proven |

---

## 4. Rejected directions

- Do **not** reuse Matrix Tutorial's hardcoded `[4,1|9],[-2,3|-1]` solver — guided practice uses the new engine only.
- Do **not** pulse only the correct cell on pick-cell (Chase explicitly rejected flashing the answer on wrong try).
- Do **not** use thick Part 3 primary brackets (12px / stroke 3) — looked too dark in portal embed.
- Do **not** lock Next on dev nav — Chase needs to skip freely for testing.
- Do **not** touch frozen Calendar 2.0 or unrelated Matrix tutorial dirty files unless asked.

---

## 5. Current implementation state

### Matrix app (`School Scrips/Matrix app`) — **all guided-practice work untracked (new dirs)**

| Area | Path |
|---|---|
| Engine | `src/app/engine/` — `rational`, `matrix-ops`, `gauss-jordan`, `question-script`, `answer-check`, `problems`, `types`, `index.ts` |
| Tests | `src/test/engine/guided-practice-engine.test.ts` (8 pass), `src/test/builders/parse-row-op-expression.test.ts` |
| UI | `src/app/components/guided-practice/` — `GuidedPracticeSolver`, `GuidedPracticeOverlay`, `GuidedPracticeMatrixDisplay` |
| Builders | `src/app/components/builders/` — `BuilderPanel`, `BlankSlot`, `MatrixEntryGrid`, `parse-row-op-expression` |
| Session | `src/app/hooks/use-guided-practice-session.ts` — state machine, flash-on-correct, goBack/goNext dev nav |

### Student portal — **modified + new feature**

| Area | Path |
|---|---|
| Feature | `src/features/guided-practice/` — `GuidedPracticeView`, `GuidedPracticeHomePanel`, `GuidedPracticeEntry`, `GuidedPracticeStepNav`, `guidedPracticeActivity.ts` |
| Routing | `App.tsx`, `usePortalRoute.ts` (`GUIDED_PRACTICE_ROUTE`), `MatrixHomeView.tsx` |
| Styles | `src/styles/guided-practice.css`, `matrix-embed.css` (`.matrix-guided-practice-inset`) |
| Types | `src/types/matrix-app.d.ts` — `GuidedPracticeSolver` ref handle |

### student-session-kit — **untracked migrations**

- `supabase/migrations/041_matrix_guided_practice.sql` — activity registered (`total_items: 20`)
- Also untracked: `040_memberships_enable_rls.sql` (may be unrelated — verify before push)

### Macro App — **modified** (teacher console + catalog)

- `useTeacherConsoleActivityCatalog.ts` — guided practice tile
- `matrixSlotCatalog.ts` — `GUIDED_PRACTICE_ACTIVITY_ID`

### Verification (this session)

- `npm run test` in Matrix app — engine tests pass
- `npm run build` in student-portal — succeeds
- **No GUI smoke test** — Chase verifies in Teacher Console preview / portal dev

### Git

**Nothing committed or pushed** for guided practice across repos.

---

## 6. Open questions and constraints

1. **Attempt recording** — Wire `useGuidedPracticeAttempt` (or portal exemplar pattern) +
   Supabase submit; engine slot ids like `op1-pick-cell`. `guidedPracticeSlotLabel()` is still
   placeholder returning `null`.
2. **Label catalogs** — Update `activityQuestionLabels.ts` (portal) and `matrixSlotCatalog.ts`
   (Macro App) with human-readable slot labels for Teacher Console breakdowns.
3. **Extend beyond first column** — Remove or raise `FIRST_COLUMN_OPERATION_COUNT` once recording
   works; full RREF is 4 ops for problem 2.
4. **Row-op builder UX** — Token parsing may need polish on phone; builder on narrow landscape
   may need overlay (not implemented).
5. **Dev nav** — Back/Next should stay dev-only in final student UX (remove or hide before ship?).
6. **Migration push** — `041` may need `npm run db:push` in student-session-kit if not already
   applied on this machine.
7. **Macro App dirty state** — Many teacher-console files modified; may mix unrelated TC redesign
   work — commit per repo, don't conflate.

---

## 7. Exact next step

**Wire attempt recording for guided practice** — follow
`student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md` § Adding a new app and the generic-quiz /
matrix-tutorial attempt patterns:

1. Read pipeline doc + matrix tutorial attempt hook in student-portal.
2. Emit one attempt item per question advance (slot id from `PracticeQuestion.slot`).
3. Implement `guidedPracticeSlotLabel()` and Macro App slot catalog rows.
4. Headless test or hook test if exemplar has one; hand Chase portal preview steps for one full
   first-column run.

---

## Read first (fresh task)

1. This file (`agent docs/momentum-handoffs/latest.md`)
2. `student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md` § Adding a new app
3. `School Scrips/student-portal/src/features/guided-practice/` (current UI entry)
4. `School Scrips/Matrix app/src/app/hooks/use-guided-practice-session.ts` (advance/slot ids)
5. `School Scrips/student-portal/src/features/matrix-tutorial/` — attempt/resumable pattern exemplar

**App AGENTS:** `School Scrips/student-portal/AGENTS.md`, `School Scrips/Matrix app/AGENTS.md`
