# Momentum handoff — Factoring GP portal: layout tuner + FOIL product stack

**Written:** 2026-10-14 (day-valid only)
**Repos touched:** `School Scrips/Factoring Guided Practice`, `School Scrips/student-portal`, `Programs/` (session tracking only)
**Git:** nothing committed or pushed. No GitHub, no end-of-session actions.

---

## 1. Objective and phase

Chase is polishing **Factoring Guided Practice** in the **student portal** embed (landscape,
Move box tuner, `@factoring-guided/` alias). The double-bubble / sign-flip step should match his
standalone **factoring-app** FOIL visuals: arcs below the binomials, vertical addition of middle
terms with **x**, sum under a line, prompt + Check in the blue card, adjustment buttons stacked
and clickable-looking.

**Phase:** Implementation done through baked layout + product UI; **needs Chase visual pass**
on device (sum line alignment, arc endpoints near 11 and 5, prompt box scroll on first move).
No Netlify deploy unless he asks.

---

## 2. Chase's desired feel (use his words)

- Layout tuner (**Move box**) must **not change box size on toggle** — only when he drags/resizes.
  Resized layout must **stick when Move box turns off** (not revert to choice-list CSS).
- First-step prompt (**"What should we do first?"**) uses the **same baked float rect** as later
  steps — no special width/height override fighting inline %.
- FOIL products: **not** horizontal `55 + 55`; **vertical stack** with **+** between; labels
  show **`55x`** (coefficient of middle term), not bare `55`.
- Outer arc should sit **under** the binomials like factoring-app, endpoints **closer to 11 and 5**
  (translate whole arc up/down), **separate from** bending the curve.
- **Check answer** lives **inside** the blue prompt box on `bubbleProducts`; float row is only
  Swap / Pick new last / Pick new first terms — real buttons (press + hover where supported).
- Product number boxes ~**15% smaller**; sum box under a **line** below the bottom addend.
- Prompt on sign step: *"Click the operations to toggle between + and −. Use the buttons below
  to adjust if needed."*

---

## 3. Accepted decisions (implemented)

### Portal embed CSS (`student-portal/src/styles/factoring-guided-embed.css`)

- Removed first-move `!important` width/height overrides (baked rect owns the prompt box).
- `data-custom-layout` on prompt float when tuned rects differ from bake — keeps resize after
  Move box off.
- Compact **Check answer** (`factoring-gcf-menu-btn--compact-check`); bubble action buttons use
  `factoring-gcf-menu-btn--bubble-action` (gradient, active, hover).
- Move box outlines for bubble product tuner targets.

### Layout bake (`Factoring Guided Practice/src/app/config/factoringPortalEmbedLayout.ts`)

Latest Chase **Copy** baked (2026-10-14):

- `infoBlockRectPct`: 59.8, 0, 25.8 × **43.9**
- `equationRectPct`, `stepLinesPct` (step 1 `yPct: 8`), `bubbleKnobPct` 56 / 54
- `bubbleProductsTuning`:
  - `innerLabelDy: -3`, `outerLabelDy: -43`, `plusDx: -38`, `plusDy: 27`
  - `innerArcShiftDy: 0`, **`outerArcShiftDy: -45`**
  - `innerArcBowDy: -8`, `outerArcBowDy: -7`

Session storage key: **`factoring-layout-placed-v16`**; custom layout flag
`factoring-layout-custom-v1`.

### Move box behavior (`useFactoringPortalLayout.ts`, ~467 lines)

- Snapshot visible rects before Move box on; seed `placed` from snapshot (no snap to bake).
- Persist custom layout to sessionStorage when rects differ from bake.
- **`useBubbleProductsTuningDrag.ts`** (new): drag inner/outer labels (Y only), plus (XY),
  arc **shift** (whole arc Y) vs arc **bow** (control point only).
- Copy JSON includes `bubbleProductsTuning` with `*ShiftDy` / `*BowDy` (legacy `*ArcDy` → bow).

### FOIL UI (`FactoringBubbleProducts.tsx`, `doubleBubble.ts`)

- Arcs curve **downward**; outer below inner span.
- **`formatBubbleXTerm`**: displays `55x`, sum `110x`.
- Vertical stack + **sum line** + **sum box** under outer addend; after Check, sum box green/red
  + ✓/✗ (removed duplicate sum from float controls).
- Move box: blue circle = arc **shift**, small red circle = arc **bow**.

### Copy / controls

- `practiceSession.ts` bubble prompt text updated (no "check your answer" in prose).
- `FactoringStepControls`: Check in card on `bubbleProducts`.
- `FactoringBubbleKnob`: renamed labels, `portalStyled`, `hideCheck` on portal float.

**Verification:** `npm test -- --run` in Factoring Guided Practice → **26 pass**.

---

## 4. Rejected directions

- Outer arc **above** the binomials (old guided-practice bug) — wrong; must match factoring-app
  below.
- Horizontal `55 + 55` row for addends — wrong; vertical addition column.
- Arc tuner handle that only changed **bow** when Chase needed **whole arc translate** — split into
  shift vs bow handles.
- Re-adding first-move `!important` auto-size CSS — breaks baked/tuned prompt rect.

---

## 5. Uncommitted files (summary)

**Factoring Guided Practice:** components (BubbleProducts, Knob, ControlsFloat, ParenSkeletonFloat,
PracticeView, StepControls, DoubleBubbleStage), `factoringPortalEmbedLayout.ts`,
`useFactoringPortalLayout.ts`, `useFloatingRectTuner.ts`, `useBubbleProductsTuningDrag.ts` (new),
`doubleBubble.ts`, `practiceSession.ts`, `factoring-double-bubble.css`.

**student-portal:** `factoring-guided-embed.css` only.

**Programs root:** session tracking HTML/JSONL only (not app code).

---

## 6. Open questions / constraints

- **Sum stack position** is computed from label tops + fixed `PRODUCT_BOX_H` (28px) — if line/sum
  misaligns after Chase reviews, add tuner offsets for sum line/box or measure box height.
- **Pick new first terms** intentionally returns to `parenSkeleton` (clears bubble fields) — not
  a bug; tooltip on button explains.
- **`useFactoringPortalLayout.ts`** ~467 lines — extract before adding more tuner logic (700+ rule).
- **`FactoringPracticeView.tsx`** — keep orchestrator-only; don't grow past 300 without extract.
- No GUI launch without permission; Chase reviews in portal/Macro preview himself.
- **No Netlify deploy** unless explicit in message.

---

## 7. Read first (fresh agent)

| Need | Path |
|---|---|
| Portal factoring embed | `School Scrips/student-portal/AGENTS.md` |
| Sister app | `School Scrips/Factoring Guided Practice/AGENTS.md` |
| Baked layout | `Factoring Guided Practice/src/app/config/factoringPortalEmbedLayout.ts` |
| Product arrows UI | `Factoring Guided Practice/src/app/components/FactoringBubbleProducts.tsx` |
| Move box hook | `Factoring Guided Practice/src/app/hooks/useFactoringPortalLayout.ts` |
| FOIL math | `Factoring Guided Practice/src/engine/doubleBubble.ts` |
| Standalone reference | `School Scrips/factoring-app/src/app/components/ProductArrows.tsx` |

---

## 8. Exact next step

Chase opens **Factoring Guided Practice** in the portal (landscape), problem 1 through **Set up
parentheses** → coefficients/constants → **bubbleProducts**. Confirm:

1. Arc endpoints feel close enough to outer terms (else tweak baked `outerArcShiftDy` or Move box
   → Copy → bake).
2. Vertical **`55x` / + / `55x` / line / sum** reads like factoring-app.
3. First-move prompt has **no scrollbar** at baked `hPct: 43.9` (overflow visible on choices).

If anything is off, prefer **Move box + Copy → paste into `factoringPortalEmbedLayout.ts`** and
bump `factoring-layout-placed-v*` — do not reintroduce CSS overrides that fight inline %.

If green, next product chunk is **`factoredDone` → solving roots** (still stubbed after correct
Check) — confirm with Chase before building.
