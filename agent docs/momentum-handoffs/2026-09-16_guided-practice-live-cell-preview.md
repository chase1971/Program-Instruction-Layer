# Momentum handoff — Gauss-Jordan guided practice builders

**Written:** 2026-09-16 (Wednesday, afternoon)

---

## 1. Objective and current phase

Chase is polishing **Gauss-Jordan Method Practice** in the **Student Portal**
(`matrix/guided-practice`), embedded from **Matrix app** via `@matrix` alias.

**Phase:** Step 4 row-op builder and row-entry number calculator are largely **done to
Chase's satisfaction** for layout, sizing, and flow. **Next priority:** **live preview** —
digits typed on the number keypad must appear **in the active matrix cell in real time**
(before Next/Enter).

---

## 2. Chase's desired feel

### Step 4 row-op builder (DONE — do not redo unless asked)
- Click-to-open; Enter saves draft only; Submit validates
- Builder locked at `{ x: 201, y: -9 }` in `GuidedPracticeOverlay.tsx`
- Expression bar: large text, ⌫ inside field, red × close; row keys without × multiply
- Enter bottom-right on keypad; ↔ SVG glyph sized down; → longer in expression field
- Tutorial box step 4: 200px narrower than Part 3 default (350px total via trim constant)

### Row-entry number calculator (DONE except live preview)
- Same horizontal width as tuned (`13rem` in portal CSS) — **horizontally good**
- **Taller keys** (`2.1rem` min-height) — Chase asked for ~50px more height
- **No text field** — numbers only appear in matrix on commit today (Chase wants this changed)
- Keypad: 5 columns, 3 rows — `1–9`, `0`, then `/ − ⌫` + **Next** or **Enter**
- **Next** on cells 1–2; **Enter** on last cell (3rd) — closes builder when row complete
- Only **active** matrix cell pulses (not all empty cells)
- Row-entry step **auto-opens** builder on cell 0
- Small red **×** top-right closes builder; **⌫** deletes last typed digit (internal draft)

### Testing aid (step 4 only)
- Click on empty row-notation slot **pre-fills correct answer** in row builder
  (`openRowOpBuilder` in `use-guided-practice-session.ts`)

### Chase's explicit next requirement
> *"When I press a number, it should appear in the matrix cell that we are trying to enter
> in. In real time."*

Today `builderExpression` is internal — `MatrixEntryGrid` only shows committed
`matrixDraft` values. Next agent should wire **live preview** into the active cell display
(partial string like `1/3` or `−2` before parse/commit). Backspace should update preview
live. Next/Enter still commits parsed rational via `parseRational`.

---

## 3. Accepted decisions

| Decision | Detail |
|---|---|
| Portal embed CSS beats Tailwind on buttons | Use `guided-practice.css` rules with higher specificity for key font sizes |
| Row builder horizontal | 6-col grids; value keys + row-op row; Enter col 6 |
| Number builder horizontal | 5-col grid; no expression bar; `--value` modifier class |
| Enter advances cells | `commitBuilder` fills cell, moves `activeMatrixCell`, keeps builder open |
| Last cell label | `Enter`; earlier cells `Next` |
| Active cell pulse only | `MatrixEntryGrid` pulses `activeCellIndex === cellIndex` |
| Popover width trim | `GUIDED_PRACTICE_POPOVER_WIDTH_TRIM = 200` from Part 3 bases |
| Step 4 test pre-fill | Empty slot + row-notation → `formatRowOpNotation(expected)` |

---

## 4. Rejected directions

- **Do not** restore multiply (×) on row-op keypad
- **Do not** restore Clear (C) on row builder expression bar (accidental mis-clicks)
- **Do not** pulse all empty matrix cells
- **Do not** use 3-column number keypad (Chase wanted 5 columns, not 6-wide shrink)
- **Do not** widen number calculator horizontally — height only when sizing
- **Do not** redo step 4 flow, builder position, or symbol SVG work unless Chase asks
- **Do not** assume Tailwind `text-[*px]` works in portal without checking `matrix-embed.css`

---

## 5. Current implementation state

### Matrix app (`School Scrips/Matrix app`)

| File | State |
|---|---|
| `use-guided-practice-session.ts` | Enter→next cell; row-entry auto-open cell 0; step 4 pre-fill |
| `BuilderPanel.tsx` | `HorizontalValueBuilder`, `HorizontalTransformationBuilder`, `valueSubmitLabel` |
| `builder-key-styles.ts` | Value/row horizontal key tiers; value keys `2.1rem` |
| `builder-arrow-glyphs.tsx` | ↔ keypad SVG; → expression SVG; `BuilderExpressionText` |
| `MatrixEntryGrid.tsx` | Active-cell-only pulse; no live draft display yet |
| `GuidedPracticeSolver.tsx` | Passes `valueSubmitLabel`, matrix + inline builders |
| `GuidedPracticeOverlay.tsx` | Popover width trim; builder position constants |

### Student portal (`School Scrips/student-portal`)

| File | State |
|---|---|
| `src/styles/guided-practice.css` | Builder widths; value key font-size overrides; arrow symbol overrides |

### Tests
Matrix app: `npm test -- --run` — **38 passed** (last run this session).

### Uncommitted
Both **Matrix app** and **student-portal** have local edits. **Not committed or pushed.**

---

## 6. Open questions, blockers, constraints

### PRIMARY NEXT TASK: Live matrix cell preview

**Problem:** `builderExpression` updates on each keypress but `MatrixEntryGrid` reads only
`matrixDraft` (committed rationals). Active cell shows `·` while typing.

**Likely approach:**
1. Pass `builderExpression` (or `draftPreview: string | null`) + `activeCellIndex` into
   `MatrixEntryGrid`.
2. When `cellIndex === activeCellIndex && builderOpen`, render `builderExpression` (or formatted
   partial) instead of `·` / committed value.
3. On Next/Enter, existing `parseRational` + commit unchanged.
4. On ⌫, preview updates via existing `backspaceBuilder`.
5. Invalid partials (e.g. lone `−`, trailing `/`) — show raw string; parse only on commit.

**Touch minimally:** `MatrixEntryGrid.tsx`, `GuidedPracticeSolver.tsx` (props), possibly
`use-guided-practice-session.ts` if exposing a derived preview helper.

### Constraints
- **Never launch GUI** without asking Chase
- **Do not commit** unless Chase asks
- Row builder expression field stays as-is (row-op has text field); only **number builder**
  omits it

---

## 7. Exact next step

1. Read this file, then `MatrixEntryGrid.tsx` and `use-guided-practice-session.ts`
   (`builderExpression`, `activeMatrixCell`, `commitBuilder`).
2. **Show `builderExpression` live in the pulsing active matrix cell** as keys are pressed.
3. Verify: row-entry step → type `1` `/` `3` → cell shows `1/3` before Next; Next commits and
   advances; last cell shows Enter.

---

## Read first (next agent)

1. **`agent docs/momentum-handoffs/latest.md`** (this file)
2. `School Scrips/student-portal/AGENTS.md`
3. `School Scrips/Matrix app/AGENTS.md`
4. `Matrix app/src/app/components/builders/MatrixEntryGrid.tsx`
5. `Matrix app/src/app/hooks/use-guided-practice-session.ts`
6. `Matrix app/src/app/components/guided-practice/GuidedPracticeSolver.tsx`

---

## Verification handoff (Chase)

Reload student portal → Gauss-Jordan guided practice → row-entry step → type digits on
calculator → **active matrix cell should update on every keypress** (not only after Next).
