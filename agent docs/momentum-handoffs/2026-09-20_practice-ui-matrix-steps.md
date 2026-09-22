# Momentum handoff — Practice mode UI polish + matrix steps viewer

**Written:** 2026-09-20 (Sunday, ~2:12 PM)

---

## 1. Objective and current phase

**Active thread:** Gauss-Jordan **Method Practice** in student portal — one tile (`#/matrix/guided-practice`), two home modes (**Guided Practice** + **Practice**), shared 20-problem bank.

**Phase:** **Practice UI substantially reworked; device verify NOT done.** Layout, two-try flow, builder UX, instruction overlay placement, and matrix-steps recovery screen were all implemented this session. Headless tests + portal build pass. Chase has **not** confirmed on phone after the latest layout/matrix-steps changes.

**Next focus:** Phone verify, then any pixel tweaks Chase reports (screenshots in chat work well for layout issues).

---

## 2. Chase's desired feel (use his language)

### Main practice screen
- Should **look like guided mode at the solution step**: matrix + ordered pair side by side, horizontal number builder.
- **X cell pulses** on start so it’s obvious where to type — not static/dashed with no motion.
- **Auto-open** number builder on **x** when a problem loads — no tap-first.
- Builder keys: **Next** on x → moves to y; **Submit** on y → checks answer. **No separate Submit button** outside the builder.
- **First wrong:** amber “Try again”, **clear (x,y)**, reopen builder on x.
- **Second wrong:** show revealed answer, **stay on screen** (no auto-advance). **Next problem** and **Matrix steps** as **short buttons inside the blue instruction box** — not full-width buttons below the answer row.
- Instruction box **directly under the matrix** — must **not cover matrix numbers** and must **not push the answer row / builder to the right** (that was a regression when the box was in a flex column with the matrix).
- Problem label: **Problem 1, 2, 3…** (session ordinal), in nav row — not bank id.
- **Correct answer:** green message + check flash, then auto next problem.

### Matrix steps screen (after 2nd wrong → Matrix steps)
- **Start** matrix **separate** on the left, raised up.
- **Vertical wall/divider** between Start and the four steps.
- Steps in **2×2 grid** to the right: Step 1 TL, Step 2 TR, Step 3 BL, Step 4 BR.
- **No** intro text (“Each row operation in order…”).
- **No “Answer correctly”** dev button on this screen.
- **Back** button: **small**, at the **bottom** (not top header row).

### Layout feedback for agents
- Chase attaches **screenshots** — agents can read them. Best way to catch overlap without pixel-by-pixel back-and-forth.

---

## 3. Accepted decisions (do not re-litigate)

| Decision | Detail |
|---|---|
| One portal tile | `#/matrix/guided-practice` |
| Two Supabase activity IDs | Guided: `matrix/guided-practice` · Practice: `matrix/unguided-practice` |
| Shared problem pool | `problemBank.ts` localStorage |
| Practice defer initial save | `useResumableAttempt({ deferInitialSave: true })` |
| Second wrong: manual advance | `onNextProblem` fires `finish('incorrect')` — not auto |
| Matrix steps optional | Separate screen toggled by `showStepViewer` in `UnguidedPracticeView.tsx` |
| Step matrices source | `practiceStepMatrices()` in `guided-practice-questions.ts` — Start + 4 ops same as guided |
| Instruction overlay placement | Absolute under matrix column (`top-full`), not in document flow beside matrix (that widened column and shifted answer row) |
| Dev “Answer correctly” | Still on main practice nav; **hidden** when `showStepViewer` — remove before production when Chase says |

---

## 4. Rejected directions — do not redo

- **Auto-advance on 2nd wrong** — too fast; Chase couldn’t read feedback.
- **Next problem / Matrix steps as full-width buttons** below the ordered pair — belong **inside** instruction overlay.
- **Instruction box in flex column with matrix** if it widens the column and shifts answer/builder right — use absolute under matrix instead.
- **Floating overlay at y:72 overlapping matrix cells** — covers numbers.
- **Separate Submit button** in practice — builder Submit handles it.
- **Opening builder clears pulse** without active-cell pulse — empty active cell must still pulse.
- **Matrix steps 2×2 including Start** — Start is separate with a wall; only Steps 1–4 in grid.
- **Intro paragraph on matrix steps screen** — removed per Chase.

---

## 5. Current implementation state

### Key files (Practice)

| Area | File |
|---|---|
| Solver + flow | `Matrix app/.../UnguidedPracticeSolver.tsx` (~830 lines — **watch size**) |
| Instruction overlay | `Matrix app/.../GuidedPracticeOverlay.tsx` — `instructionLayout="stacked"`, `practiceRevealActions` |
| Pulse active cell | `Matrix app/.../SolutionEntryGrid.tsx` — `showPulse = !hasDisplay && (pulseEmptyCells \|\| active)` |
| Builder Submit label | `Matrix app/.../BuilderPanel.tsx` — `'Next' \| 'Enter' \| 'Submit'` |
| Step matrices | `Matrix app/.../UnguidedPracticeMatrixStepsPanel.tsx` |
| Portal workspace | `student-portal/.../UnguidedPracticeView.tsx` |
| Steps screen shell | `student-portal/.../UnguidedPracticeMatrixStepsView.tsx` — back at bottom |
| Problem nav + dev btn | `student-portal/.../UnguidedPracticeProblemNav.tsx` |
| CSS | `student-portal/src/styles/guided-practice.css` |

### Behavior summary
- Mount: `initialPracticeBuilderState()` opens x builder immediately; active empty x **pulses**.
- `commitBuilder`: x → Next opens y; y → Submit calls `submitSolution`.
- First wrong: clears draft, soft retry message, reopens x builder.
- Second wrong: `revealedAnswer`, buttons in overlay, builder closes.
- `key={problemId}` remounts solver per problem.

### Tests / build (last run this session)
- Matrix app: **103** vitest tests pass (`unguided-practice-solver.test.tsx` included)
- student-portal: **`npm run build`** succeeds
- **No phone verify** after: instruction box reposition, x pulse, matrix steps layout, back-at-bottom

### Git
- **Uncommitted** across Matrix app + student-portal (+ related kit/migration from prior work). Do **not** commit until Chase says “put on GitHub” or end-of-session protocol.

---

## 6. Open questions and constraints

- **Phone verify** is the gate — Chase has not signed off on latest practice + matrix steps layouts.
- **Guided mode** still uses **Another problem?** modal; Practice uses inline **Next problem** — confirm if guided should match (not asked this session).
- **Resume mid-reveal:** student leaves after 2nd wrong before Next — resume with revealed state may be incomplete (not explicitly handled).
- **Remove dev “Answer correctly”** before production when Chase wants.
- **UnguidedPracticeSolver.tsx** approaching size watch — extract only if adding more; hard cap 800.
- **Frozen:** Calendar 2.0 — do not touch.
- **Never launch GUI** without Chase’s permission — handoff checklists as flat statements.

---

## 7. Exact next step (for fresh agent)

**Phone-verify Practice + matrix steps; fix any layout issues Chase reports.**

1. Read `agent docs/momentum-handoffs/latest.md` (this file) — then skim exemplar `GuidedPracticeSolver.tsx` solution branch if tweaking layout.
2. Ask Chase for **screenshots** if overlap or spacing looks wrong — do not guess pixel nudges.
3. Verify checklist (statement for Chase — do not run GUI yourself):
   - New problem: x **pulses**, builder open, **Next** → y, **Submit** → grade.
   - Wrong once: cleared fields, retry builder on x.
   - Wrong twice: answer in blue box, **Next problem** + **Matrix steps** inside box; no auto-advance.
   - Matrix steps: Start | wall | 2×2 steps; small **Back** at bottom; no green Answer correctly.
   - Correct: celebration then auto next; Problem N label in nav.
4. If all green and Chase asks, run end-of-session / put on GitHub.

**Do NOT** redo problem bank, attempt wiring, or home panel unless a verify bug requires it.

---

## 8. Phone verify checklist (flat statement for Chase)

1. Practice layout: matrix + corner ordered pair + builder — answer row **not shifted right**.
2. X pulses on load; builder auto-open on x.
3. Next on x → y; Submit on y — no separate Submit button.
4. Wrong once → clear + retry; wrong twice → reveal in instruction box with short buttons.
5. Matrix steps → Start left, wall, 2×2 steps; Back small at bottom.
6. Correct → green flash → next problem.

---

## Copy-ready navigation path

`latest.md` → `UnguidedPracticeSolver.tsx` → `GuidedPracticeOverlay.tsx` → `UnguidedPracticeMatrixStepsPanel.tsx` → `UnguidedPracticeMatrixStepsView.tsx` → `guided-practice.css`
