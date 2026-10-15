# Momentum handoff — Factoring GP portal: per-step prompts, error float, layout bake

**Written:** 2026-10-14 (day-valid only)
**Repos touched:** `School Scrips/Factoring Guided Practice`, `School Scrips/student-portal`, `Programs/` (session tracking, this handoff)
**Git:** nothing committed or pushed. No GitHub, no end-of-session actions.

---

## 1. Objective and phase

Chase is polishing **Factoring Guided Practice** embedded in the **student portal** (landscape,
admin **Move box** / **Copy** layout tuner, `@factoring-guided/` Vite alias). Focus this session:
**prompt card sizing per step**, **wrong-answer messaging off the blue card**, **Check answer**
placement on the bubble-products step, **layout bake** from Copy JSON, brief **Correct!** flash
after a good factorization, and **step-line** placement for the double-bubble flow.

**Phase:** Implementation and bakes are in place; **Chase should visually verify** on portal
dev (`npm run dev` in student-portal) — especially bubble step prompt height (33.2%), step 2
math line at `mathXPct: 13.4`, red error float, and 2.2s Correct flash. No Netlify deploy unless
he asks.

---

## 2. Chase's desired feel (use his words)

- **Move box** resize must **stick** when toggled off — not revert (was broken by CSS auto-grow
  on first-move choices and by re-measuring DOM on re-enable).
- **Copy** works with Move box **on or off** (admin header).
- **One prompt size does not fit all steps** — the taller first-move / old session box must **not**
  apply on the **double-bubble / bubble-products** slide; he tuned **that slide only** (33.2% h).
- **Check answer** on bubble step: **below the instruction text**, **bottom-right** of the blue
  card — not beside text, not overlapping Swap/Pick buttons, no scrolling inside half a card.
- **Wrong answers** go in a **separate red float** (lower-left), **not** inside the prompt card.
  He positioned it with Move box; bake is in config.
- **Correct!** should appear **briefly** then **disappear** while they continue solve-for-roots.
- Double-bubble **= 0** row should not have a big dead zone after the zero (removed `scale(0.9)`
  layout hack on skeleton).

---

## 3. Accepted decisions (implemented)

### Per-step prompt rects (`infoBlockRectPctByStep`)

In `Factoring Guided Practice/src/app/config/factoringPortalEmbedLayout.ts`:

| Key | Use | Rect (x, y, w, h) |
|---|---|---|
| `firstMove` | Choice list step | 59.8, 0, 25.8, **43.9** |
| `doubleBubblePrompt` | parenSkeleton, parenConstants, bubbleProducts, factoredDone | 65.3, 1.7, 24.3, **33.2** |
| `default` | GCF, inner, solveRoots, etc. | 59.8, 0, 25.8, **38** |

`resolveInfoLayoutStepKey(step)` + `resolvePortalInfoBlockRect()` pick the rect; session stores
`infoByStep` (not one global `info` for all steps). **Always pass embed layout config** (`baked` /
`FACTORING_PORTAL_EMBED_LAYOUT`) into `resolvePortalInfoBlockRect` — **never** `bakedPlaced()`
(Placed object) — that caused `undefined.xPct` crash (fixed).

Session key: **`factoring-layout-placed-v22`**.

### Latest full layout bake (Copy JSON, 2026-10-14)

Also in `factoringPortalEmbedLayout.ts`:

- `infoBlockRectPct` (Copy default / fallback): 59.8, 0, 25.8, 38
- `equationRectPct`: 18.6, 1.4, 44.7, 10
- `stepLinesPct`: step 1 — 11.5 / 8.8 / 12.8; step 2 — 28.2 / 9.1 / **13.4** (math X adjusted)
- `bubbleKnobPct`: 56, 54
- `bubbleProductsTuning`: innerLabelDy -3, outerLabelDy -43, plusDx -38, plusDy 27,
  innerArcShiftDy 0, outerArcShiftDy -45, innerArcBowDy -8, outerArcBowDy -7
- `correctFeedbackRectPct`: 36, 54, 11, 5
- `errorMessageRectPct`: **0, 63.9, 21.5, 27.7**

Copy output includes `infoBlockRectPctByStep` when present.

### Prompt / Check / errors (components + CSS)

- **`FactoringErrorMessageFloat.tsx`** — stage float; visible when `state.error` or Move box on
  (empty dashed box for tuning). Prompt card gets `error={null}` when embedded.
- **`FactoringBubbleCheckButton`** — in **`FactoringStepControls`** inside
  `factoring-gcf-bubble-check-footer`; not in prompt header.
- Portal CSS (`student-portal/src/styles/factoring-guided-embed.css`):
  - `data-portal-layout-lock` on prompt float — blocks first-move `!important` auto-grow from
    overriding baked %.
  - Bubble footer: card `height: auto`, Check **not** `flex: 1` filling a tall float.
- **`useFactoringCorrectFlash.ts`** — ~2.2s **Correct!** after `confirmedFactoredProduct` set
  (bubble check success); `FactoringCorrectFeedbackFloat` only when flash or Move box on.

### Layout hook (`useFactoringPortalLayout.ts`, ~610 lines — watch file size)

- Prefer saved `infoByStep[stepKey]` over DOM measure when enabling Move box.
- Copy ref always active (not only when tuner on).
- `formatFactoringLayoutForAgent` includes `errorMessageRectPct` and optional `infoBlockRectPctByStep`.

### Portal entry (`FactoringGuidedPracticeEntry.tsx`)

- **Copy** button visible whenever admin cheats on (not only when Move box on).

### Double-bubble CSS (`factoring-double-bubble.css`)

- Removed `transform: scale(0.9)` on `.factoring-paren-skeleton` (fixed trailing padding after `= 0`).

---

## 4. Rejected / do not redo

- **Check answer beside prompt text** in header row — squeezes text, causes scroll/overlap.
- **`overflow: visible` + inner scroll** on bubble prompt to “fit” text — Chase hates scrolling
  half a text box.
- **Single global `infoBlockRectPct`** for all steps — first-move height leaked onto bubble slide.
- **Passing `bakedPlaced()` as layout** into `resolvePortalInfoBlockRect` — crashes.
- **Persistent Correct!** for entire `solveRoots` — replaced with flash only.

---

## 5. Current implementation state

### Factoring Guided Practice (dirty, uncommitted)

Modified: layout hook, portal embed config, `FactoringPracticeView`, step controls, bubble
products/controls, session engine files, tests, `factoring-double-bubble.css`.

New untracked: `FactoringBubbleCheckButton.tsx`, `FactoringCorrectFeedbackFloat.tsx`,
`FactoringErrorMessageFloat.tsx`, `useBubbleProductsTuningDrag.ts`, `useFactoringCorrectFlash.ts`.

Build verified: `npm run build` in Factoring Guided Practice succeeds.

### student-portal (dirty, uncommitted)

Modified: `factoring-guided-embed.css`, `FactoringGuidedPracticeEntry.tsx`.

### Verification Chase should run (agent did not open GUI)

1. Portal dev — Factoring Guided Practice, admin cheats.
2. **First move** — tall prompt; **bubble products** — compact 33.2% float, Check bottom-right
   under text.
3. Wrong bubble check — message in **red lower-left float**, not blue card.
4. Good bubble check — **Correct!** ~2s then gone; stay on solve step.
5. Move box — resize bubble prompt, toggle off — size sticks; Copy includes `infoBlockRectPctByStep`.

---

## 6. Open questions / constraints

- **Per-step prompt tuning** beyond the three keys: if another step needs its own rect, add a
  key in `infoBlockRectPctByStep` + extend `resolveInfoLayoutStepKey` — do not revert to one global box.
- **`useFactoringPortalLayout.ts` ~610 lines** — over 500; extract before large additions (700
  extract rule).
- **`factoring-guided-embed.css` ~778 lines** — over 700 cap; prefer edits in FGA package CSS or
  extract before adding more portal rules.
- Chase uses **dwell + speech** — no typing-heavy flows; modals no backdrop dismiss (root AGENTS).
- **No Netlify deploy** unless explicit in message.

---

## 7. Read first (fresh agent)

| Need | Path |
|---|---|
| Root rules | `Programs/AGENTS.md` |
| Portal factoring row | `School Scrips/student-portal/AGENTS.md` (Factoring Guided Practice keyword) |
| Layout bake owner | `School Scrips/Factoring Guided Practice/src/app/config/factoringPortalEmbedLayout.ts` |
| Move box hook | `School Scrips/Factoring Guided Practice/src/app/hooks/useFactoringPortalLayout.ts` |
| Portal embed CSS | `School Scrips/student-portal/src/styles/factoring-guided-embed.css` |
| Bubble styles | `School Scrips/Factoring Guided Practice/src/styles/factoring-double-bubble.css` |

Prior handoff on same day (FOIL arcs — partially superseded by this doc for prompt/error/flash):
`agent docs/momentum-handoffs/2026-10-14_factoring-gp-portal-foil-layout.md`.

---

## 8. Exact next step

Chase visual pass on portal dev: confirm **bubble-products** prompt uses **doubleBubblePrompt**
33.2% rect and step 2 line at **mathXPct 13.4**. If anything is off, Move box → adjust → Copy →
paste into `factoringPortalEmbedLayout.ts` (right `infoBlockRectPctByStep` key or `stepLinesPct`).
If sum/arcs/FOIL still need tuning, read the 2026-10-14 FOIL handoff section — separate from
prompt/error work above.

Optional follow-up Chase may ask: additional **per-step** prompt bakes for GCF/inner slides;
**git sync** when he says put on GitHub (sister repos: Factoring GP + student-portal).
