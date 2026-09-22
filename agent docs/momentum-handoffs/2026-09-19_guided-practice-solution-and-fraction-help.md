# Momentum handoff — Guided practice polish (fraction help + solution entry)

**Written:** 2026-09-19 (Saturday, ~12:56 PM)

---

## 1. Objective and current phase

**Active thread:** Gauss-Jordan **guided practice** in the student portal — multiply/add
fraction help tutorials (Q5/Q9), solution entry (Q17), skip shortcuts, and prompt wording.

**Phase:** Feature work is **locally complete and Chase-verified in pieces** — multiply EX1/2
and add/subtract EX1/2 flows tuned; EX3 multiply timed on old MP4; solution entry reworked.
**Nothing committed.** Next agent should **live-verify step 17 on device** after refresh, then
Chase decides deploy / Manim re-render.

---

## 2. Chase's desired feel

- **Multiply intro:** Describes EX1/2/3 by numeral; pick example — no auto-play through all.
- **Add/subtract intro:** Simple — **"Tab or click on an example to begin."** (no per-clip copy yet).
- **EX2 add/subtract:** Same combine text as EX1 — *"Put it all over the same denominator and
  add the numerators together."* — one clip through finish (not a separate simplify step before sum).
- **EX3 multiply:** Simplify-first pedagogy like EX2 — *"Simplify the 2 and 8 first."* then multiply new numbers.
- **Prompts:** User-facing **"tab or click"** (not "click" alone) on pick-cell and related copy.
- **Solution (Q17):** Instruction — *"What is the solution? Tab or click on the ordered pair
  to enter your answer."* Both `(x, y)` cells **pulse together** until first tab/click; then
  pulse stops, keypad opens, enter **either order**, values must **persist** when switching cells.
- **Home skip buttons:** Skip to multiply help, add/subtract help, column 2, **step 17** (solution).
- **No video scrub UI** in production — timing buttons were dev-only and **removed** per Chase.
- **Never launch GUI / deploy** without asking.

---

## 3. Accepted decisions

| Decision | Why |
|---|---|
| Per-example intro + hold/play segments (`useSegmentedHelpAnimation`) | Independent EX1/2/3; Next on hold plays motion |
| EX3 multiply: hold 44s, simplify 44–46.7s, multiply 46.7–49s | Chase live-tuned on old 6-example MP4 |
| EX2 add combine: single segment 20.65–24.65 with ADD_COMBINE text | Matches EX1; plays through sum + finish |
| Add EX3: hold 29.1, match steps from Manim marks (estimates) | Same structure as multiply; tune on device if needed |
| `solutionPairPulse` — pulse until first field pick, then off | Cues without animating while typing |
| Live-sync `solutionDraft` on keypad append/backspace | Fixes vanishing digits when switching x/y |
| Skip-to-help at row-entry: pause snapshot after draft init | Fixes malformed row grid (empty `matrixDraft`) |
| `GUIDED_PRACTICE_SOLUTION_ENTRY_INDEX` + home **Skip to step 17** | Fast path to solution QA |
| Overshoot guard in `handleTimeUpdate` (no snap unless >40ms past end) | Reduces flash at segment end |

---

## 4. Rejected directions — do not redo

- **Video scrub controls (−0.5s / +0.5s + time display)** — helped tuning; Chase asked removal from both tutorials.
- **EX3 multiply instruction** *"Multiply numerators and denominators together, then simplify"* at start — wrong; simplify-first like EX2.
- **Separate EX2 add "Simplify if necessary" step before playing the sum** — broke flow; merged into one combine segment.
- **Auto-advance solution x → y on Enter** — Chase wants any order; pick either cell.
- **Pulse on filled solution cells while typing** — caused glitchy text; pulse only on empty cells before first pick.
- **Solution effect depending on `workingMatrix`** — reset draft repeatedly; removed from deps.

---

## 5. Current implementation state

### Matrix app — **dirty, not committed**

| Area | Key files |
|---|---|
| Multiply tutorial | `fractionHelpTutorialConfigs.ts` — EX3 @ 44s, simplify-first steps |
| Add/subtract tutorial | same — intro, holds, EX2 single combine segment |
| Fraction help UI | `GuidedPracticeFractionHelpPanel.tsx`, `useSegmentedHelpAnimation.ts` |
| Solution entry | `SolutionEntryGrid.tsx`, `use-guided-practice-session.ts`, `guided-practice-builder-commit.ts` |
| Prompts | `question-script.ts` (tab or click), `guided-practice-questions.ts` (solution prompt) |
| Skip index | `guided-practice-catalog.ts` — `GUIDED_PRACTICE_SOLUTION_ENTRY_INDEX` |
| Row-entry skip bug | `guided-practice-fraction-help.ts`, `use-guided-practice-session.ts` |
| Tests | `fractionHelpTutorialConfigs.test.ts` (16 pass), `guided-practice-engine.test.ts` (9 pass) |

### Student portal — **dirty, not committed**

| File | Role |
|---|---|
| `GuidedPracticeHomePanel.tsx` | Skip to step 17 button |
| `GuidedPracticeView.tsx` | `skipToSolution` handler |
| `guidedPracticeActivity.ts` | exports solution index |
| `matrix-app.d.ts` | types for solution index |
| `guided-practice-fraction-help.css` | layout (scrub CSS removed) |

### Macro App — **dirty, not committed**

| File | Role |
|---|---|
| `matrixSlotCatalog.ts` | tab-or-click prompts + solution prompt (sync with Matrix app) |
| `matrixSlotCatalog.test.ts` | prompt assertion updated |
| `config/d2l-courses.json`, `d2l-homework-order.json` | machine-local — **do not commit** |

### Manim Trial — **dirty, not committed**

`fraction_times_whole.py` — 3-example scene trimmed; **MP4 not copied** to Matrix assets.
`fraction-times-whole.mp4` in Matrix app is still **old ~50s / 6-example** render.

### Verification

- `npm test -- --run fractionHelpTutorialConfigs` — pass
- `npm test -- --run guided-practice-engine` — pass
- Chase live-verified: multiply EX1/2/3 timing (EX3 @ 44–49s), add EX2 combine flow, scrub removal.
- **Solution step 17:** logic fixed in session; Chase should re-verify pulse → pick → type both → Submit on device.

---

## 6. Open questions and constraints

- **Solution entry on device:** Confirm pulse stops on first pick, digits persist switching x/y, Submit works — after refresh via Skip to step 17.
- **Add/subtract EX1/EX3 segment times:** Estimated from marks json; may need device tuning (no scrub UI — adjust `fractionHelpTutorialConfigs.ts` from Chase's timestamps).
- **Permanent multiply fix:** Re-render `fraction_times_whole.py`, copy MP4 to `Matrix app/src/assets/guided-practice/fraction-times-whole.mp4`, sync all segment times from new marks json.
- **Deploy:** Not done; ask before `npm run deploy:prod` or launching portal GUI.
- **No commit/push** unless Chase asks.
- Read `School Scrips/Matrix app/AGENTS.md` for viewport budget + step numbering (UI step 17 = question index 16).

---

## 7. Exact next step

1. Refresh portal → **Skip to step 17**.
2. Confirm: both cells pulse → tab/click one → pulse stops → enter x and y in either order → values stay → Submit.
3. If good, Chase may ask deploy or Manim re-render; if add/subtract times off, tune `ADD_SUBTRACT_HELP_TUTORIAL` in `fractionHelpTutorialConfigs.ts`.

---

## Read first (fresh agent)

1. This file (`agent docs/momentum-handoffs/latest.md`)
2. `School Scrips/Matrix app/AGENTS.md`
3. `School Scrips/Matrix app/src/app/components/guided-practice/fractionHelpTutorialConfigs.ts`
4. `School Scrips/Matrix app/src/app/hooks/use-guided-practice-session.ts`
5. `School Scrips/Matrix app/src/app/components/guided-practice/SolutionEntryGrid.tsx`

Prior handoff (multiply-only, partially superseded): `2026-09-19_multiply-fraction-help-polish.md`
