# Momentum handoff — Gauss-Jordan guided practice step 4 builder polish

**Written:** 2026-09-16 (Wednesday, afternoon)

---

## 1. Objective and current phase

Chase is polishing **Gauss-Jordan Method Practice** in the **Student Portal**
(`matrix/guided-practice`), embedded from **Matrix app** via `@matrix` alias. Focus this session
was **step 4 (row-notation)**: click-to-open builder flow, locked builder position, and
expression-bar / keypad UI polish.

**Phase:** Step 4 interaction flow is **done**. Builder is **locked at left 201px, top -9px**.
Expression bar layout (C/× above Enter on the right, ⌫ inside field, large expression text) is
**done to Chase's satisfaction**. **Symbol sizing on row-op keys (+ × → ↔) is NOT done** —
Chase confirms prior font-size tweaks had **zero visible effect**.

**Deferred:** Auto-formatting fractions in the expression field (Chase asked briefly, did not
specify desired display — not started). Full column beyond first-column cap still deferred.

---

## 2. Chase's desired feel

- **Step 4 flow:** Tutorial shows prompt + **Click** placeholder → builder opens (tutorial
  hides) → student builds row op → **Enter** closes builder and fills slot → **Submit** validates
  (no auto-advance on Enter).
- **Builder placement:** Fixed; no drag HUD in production. Locked coords from Chase's tuning:
  **`GUIDED_PRACTICE_BUILDER_POSITION = { x: 201, y: -9 }`** in
  `GuidedPracticeOverlay.tsx`.
- **Expression bar:** C and × on a **row above Enter** (right column); typing field uses most
  width; **⌫** is borderless symbol inside the field; expression text should be **large and
  readable** (`text-lg`, vertically centered — Chase approved this).
- **Row-op keypad symbols:** **+ × → ↔** should look **bigger inside the same button size** —
  especially **→** and **↔**. Chase: *"they only use about half of the space"* / *"did not
  actually increase size in any way whatsoever"*.
- **Utility styling:** C = blue flush; × = red; no gray orphan buttons; no nudge arrows; no
  separate "Drag to move" bar.
- **Dwell-click** — keypad is primary interaction; utility buttons can be smaller.
- **Never launch GUI** without asking; hand off visible checks to Chase.

---

## 3. Accepted decisions

| Decision | Detail |
|---|---|
| Click-to-open builder | No auto-open on step 4; Enter saves draft only; Submit validates |
| Builder position | `{ x: 201, y: -9 }` — constant in `GuidedPracticeOverlay.tsx` |
| Expression bar layout | `[expression + ⌫] \| [C× row] [Enter col]` |
| Delete control | ⌫ inside field, no border — symbol only |
| Clear label | **C** not Clr |
| Close | Red **×** |
| Expression text | `text-lg`, centered in field |
| Draggable tuning tooling | Removed after lock-in |
| Engine / first column | Unchanged — Matrix app `use-guided-practice-session.ts` |

---

## 4. Rejected directions

- **Do not** auto-open builder on row-notation step entry.
- **Do not** validate or advance on Enter in builder — Submit only.
- **Do not** use nudge arrow buttons for placement tuning.
- **Do not** use separate "Drag to move" bar or debug coordinate HUD in student UI.
- **Do not** put C/× in a left column beside the field (tried — Chase wanted them above Enter).
- **Do not** assume Tailwind `text-[22px]` on builder keys works in portal embed without checking CSS overrides (see §6 — it doesn't today).

---

## 5. Current implementation state

### Matrix app (`School Scrips/Matrix app`)

| File | State |
|---|---|
| `src/app/hooks/use-guided-practice-session.ts` | Step 4 click-flow; Enter → `setSlotDraft` + close |
| `src/app/components/guided-practice/GuidedPracticeSolver.tsx` | Fixed-position builder; tutorial hides when builder open |
| `src/app/components/guided-practice/GuidedPracticeOverlay.tsx` | `GUIDED_PRACTICE_BUILDER_POSITION`, `GUIDED_PRACTICE_POPOVER_POSITION` |
| `src/app/components/builders/BuilderPanel.tsx` | Horizontal builder UI; `horizontalRowOpKeyClass()` for symbol tiers |
| `src/app/components/builders/builder-key-styles.ts` | `SYMBOL` 17px, `ARROW` 22px classes ( **not visible in portal** ) |
| `src/app/components/builders/BlankSlot.tsx` | `emptyLabel="Click"` for step 4 |
| `DraggablePlacementFrame.tsx` | **Deleted** |

### Student portal (`School Scrips/student-portal`)

| File | State |
|---|---|
| `src/styles/guided-practice.css` | Builder width `min(18rem, 38vw)` |
| `src/styles/matrix-embed.css` | **Likely blocker** — see below |

### Tests

Matrix app: `npm test -- --run` — **38 passed** (last run this session).

### Uncommitted

Both Matrix app and student-portal have local edits from this session. **Not committed or pushed**
(handoff boundary — no end-of-session).

---

## 6. Open questions, blockers, constraints

### BLOCKER: Symbol font-size changes have no visible effect

Code sets tiered classes in `builder-key-styles.ts`:
- `BUILDER_KEY_HORIZONTAL_SYMBOL_CLASS` — `text-[17px]` for + ×
- `BUILDER_KEY_HORIZONTAL_ARROW_CLASS` — `text-[22px]` for → ↔

Chase verified on device: **no visible change** from earlier 15px attempt either.

**Likely root cause (not yet fixed):** `student-portal/src/styles/matrix-embed.css` ~lines 352–356:

```css
.matrix-embed button:not(.matrix-tutorial-nav__part-btn):not(.matrix-tutorial-nav__step-btn),
.matrix-embed input {
  font-size: 1rem;
  line-height: 1.5;
}
```

This blanket rule probably **overrides** Tailwind arbitrary `text-[*px]` on builder keypad
buttons inside `.matrix-guided-practice-inset`. Specificity: `.matrix-embed button:not(...)` beats
single utility class.

**Fix directions for next agent (pick one, verify in portal):**
1. Exempt builder keys: e.g. `.guided-practice-builder button { font-size: inherit; line-height: inherit; }` or scoped reset after the global rule.
2. Use inline `style={{ fontSize: '22px' }}` on arrow keys ( ugly but proves the theory ).
3. Add a dedicated class e.g. `.matrix-builder-key--arrow` with `font-size: 22px !important` in `guided-practice.css` (prefer structural fix over !important if possible).
4. Confirm in DevTools on Chase's preview that computed font-size on → button is 16px not 22px.

Also check `portal-compact-layout.css` landscape `--quiz-*` scale if testing on phone landscape.

### Open: fraction auto-format

Chase asked whether typing `1/3` could auto-format in the expression field. **Not specified** —
ask one question if pursuing (stacked display? KaTeX? keep raw string for parser?).

---

## 7. Exact next step

1. Read this file, then `School Scrips/student-portal/src/styles/matrix-embed.css` (button
   font-size block) and `Matrix app/src/app/components/builders/BuilderPanel.tsx`.
2. **Fix arrow/symbol sizing so it actually renders** in portal embed — confirm with computed
   styles or Chase screenshot; → ↔ should visibly fill more of the key cap.
3. Do **not** redo step 4 flow or builder position unless Chase asks.

---

## Read first (next agent)

1. **`agent docs/momentum-handoffs/latest.md`** (this file)
2. `School Scrips/student-portal/AGENTS.md` — portal embed, landscape, never launch without ask
3. `School Scrips/Matrix app/AGENTS.md` — dwell targets, step numbering note
4. `School Scrips/student-portal/src/styles/matrix-embed.css` — embed overrides
5. `School Scrips/Matrix app/src/app/components/builders/BuilderPanel.tsx` + `builder-key-styles.ts`

---

## Verification handoff (Chase)

Reload student portal dev server → Gauss-Jordan guided practice → step 4 → Click → compare
**→** and **↔** key glyph size to **R1/R2**. Should be noticeably larger when fix lands.
