# Momentum handoff — Factoring Guided Practice (portal GCF flow + layout)

**Written:** 2026-10-13 · Topic: Factoring Guided Practice in student portal

## Read first

1. This file.
2. Root `Programs/AGENTS.md` (never display without permission, no ephemeral toasts unless asked, modal rules N/A here).
3. Portal host: `School Scrips/student-portal/src/features/factoring-guided-practice/FactoringGuidedPracticeEntry.tsx`
4. Portal CSS: `School Scrips/student-portal/src/styles/factoring-guided-embed.css`
5. Practice UI (Vite alias `@factoring-guided/`): `School Scrips/Factoring Guided Practice/src/app/components/` + `src/engine/` + `src/app/hooks/`
6. Baked layout: `School Scrips/Factoring Guided Practice/src/app/config/factoringPortalEmbedLayout.ts`
7. Exemplars Chase named: Matrix horizontal **value builder**; Transformations problem label; GCF tutorial info card; animation notation for **small negative vs full minus** (`Manim Trial/ANIMATION_STYLE_RECIPE.md` § negatives).

## 1. Objective and current phase

Bring **Factoring Guided Practice** into the **student portal** with Matrix-like guided feel: floating prompt box, equation placement, and a step-by-step GCF→factor→“what happens next” flow. Chase is **testing the solvable GCF binomial path** on a pinned problem 1. Phase: **UI/flow working through “What happens next?”**; solve-for-roots steps after that still use the older ExpressionKeypad (not yet rebuilt as Matrix builder). Layout is baked; tuner still available for instructors.

## 2. Chase's desired feel

- Prompt lives in a **blue GCF-style info card** (not a bottom instruction bar); Yes/No and prompts should stay **compact** — do **not** widen the baked box globally just to fit a later step.
- Instructor layout tuner: **Move box** + tiny **Copy** in the **navy header** (not problem nav). Whole box drags; corner grip resizes. No giant green JSON panel. Copy flashes **Copied** on the button (he asked for that).
- Turning Move box on must **not** jump layout; turning off must **lock** placement. Coordinates are **% of padding-free `.factoring-gcf-stage`**, not viewport/`fixed`.
- GCF / inner answers: **answer cell** + **builder under the card** (Matrix value-builder look). Vertical space is premium — **compact keys**.
- Minus (subtract) = full-size key; **negative = smaller shorter dash**.
- Partial factoring line: `1.)` with clear spacing from the math, dropped a bit under the original equation; incomplete inner uses **`?` inside slightly larger parens**, not `\cdots`. No “Your factoring so far” label.
- After inner is correct: show `1.) 3x(x+4)=0`, then ask **What happens next?** with **numbered 1/2/3 rows** (small number buttons + label text), not giant blue menu buttons. Box may widen **only on that step**.

## 3. Accepted decisions

| Decision | Why |
|---|---|
| Portal shell + floating info/equation via baked `%` on `.factoring-gcf-stage` | Stable coordinate space after padding mismatch bugs |
| `PIN_SOLVABLE_GCF_AS_PROBLEM_1 = true` → always `3x^2 + 12x = 0` as problem 1 | Predictable test path (GCF + solve) |
| Builder for `gcfEntry` + `innerEntry`; Enter commits + checks | Same interaction as Matrix cell builder |
| `doneQuestion` → “What happens next?” with `setBothZero` / `setParenOnly` / `factorMore` | Replaces yes/no “completely factored”; for AB binomial correct = set both = 0 |
| Info float grows/widens only `:has(.factoring-gcf-next-choices)` | Keep Yes/No box at Chase’s tuned size |
| Baked layout (restore): info `{39.3, 0, 28.7, 28.8}`, equation `{18.6, 1.4, 44.7, 18.8}` | From Chase’s Copy after tuner fixes |
| Session placed key `factoring-layout-placed-v6` | Stale drag sessions must not override bake |

## 4. Rejected / do not redo

- **Giant green “Copy layout for agent” panel** + blue Move handle bar on the card.
- **URL-only layout mode** without a visible Move box control.
- Widening baked `infoBlockRectPct` for all steps (made GCF Yes/No box too big) — only expand on next-step choices.
- Treating tuner `%` as viewport/`fixed` coordinates.
- Letting equation stay in flex underlay while info floats (equation looked “way off”).
- “Your factoring so far” caption; `\cdots` inside parens.

## 5. Current implementation state

### Uncommitted — `School Scrips/Factoring Guided Practice`

- Layout: `factoringPortalEmbedLayout.ts`, `useFloatingRectTuner.ts`, `useFactoringPortalLayout.ts`, `useFactoringExpressionBuilder.ts`
- UI: `FactoringPracticeView.tsx`, `FactoringGcfInfoBlock.tsx`, `FactoringAnswerCell.tsx`, `FactoringExpressionBuilder.tsx`, `FactoringNextStepChoices.tsx`, `FactoringStepControls.tsx`, `FactoringEquationPanel.tsx`
- Engine: `practiceSession.ts` (`submitWhatHappensNext`, inner/GCF draft overrides), `buildSet.ts` pin, `config.ts` pin flag, `generators.ts` fixed AB problem, `answerCheck.ts` (− normalize)
- Tests updated: `buildSet.test.ts`, `practiceSession.test.ts`
- Deleted: `FactoringLayoutTunerBar.tsx`, `useFactoringGcfBuilder.ts`

### Uncommitted — `School Scrips/student-portal` (factoring-related only)

- `FactoringGuidedPracticeEntry.tsx` — Move box + Copy in header; `layoutCopyRef`
- `useFactoringLayoutTuner.ts` — starts **off** by default
- `factoring-guided-embed.css` — floating stage, compact builder, partial line, next-choices, grow-on-choices
- `factoring-guided-practice.d.ts`, `UnguidedPracticeProblemNav.tsx` (totalProblems / endControls)
- `factoringGuidedPracticeActivity.ts` — enabled flag (verify before prod)

**Also dirty in student-portal (unrelated):** logic-homework files — **do not bundle** into a factoring-only commit unless Chase asks for broader sync.

### Verification

- Factoring Guided Practice `npm run build` + vitest practice/buildSet tests — last run green this session.
- Chase has been reviewing in portal / Teacher Console; latest ask was reverting accidental Yes/No box growth (fixed).

### Git

- **Not committed or pushed** (momentum handoff — no sync).

## 6. Open questions / constraints

- **Solve roots UI** (`solveGcfRoot` / `solveInnerRoot`) still uses `ExpressionKeypad` — not Matrix builder yet; Chase stopped at “get to What happens next.”
- After correct `setBothZero`, flow goes to `solveGcfRoot` — transition/presentation of “set equal to zero” may still need polish when he continues.
- `PIN_SOLVABLE_GCF_AS_PROBLEM_1` is temporary — turn off when full randomization wanted.
- Netlify deploy only if Chase explicitly asks.
- Never launch GUI / portal window without asking.

## 7. Exact next step

1. Confirm GCF Yes/No box is back to the small tuned size after reload.
2. Continue the AB binomial path past **What happens next? → (1) set both equal to zero**: build the next UI beat (show factors set to zero / root entry) in Matrix-builder style if Chase wants parity with GCF/inner.
3. Do not commit unrelated logic-homework dirt with factoring work.
