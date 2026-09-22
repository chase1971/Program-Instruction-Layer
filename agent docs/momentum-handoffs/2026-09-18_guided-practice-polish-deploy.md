# Momentum handoff — Guided practice polish + deploy queue

**Written:** 2026-09-18 (Friday, ~9:31 PM)

---

## 1. Objective and current phase

**Active thread:** Gauss-Jordan **guided practice** in the student portal (Matrix app embedded) —
row-entry UI, fraction-help trigger, and Q9 add/subtract tutorial copy/timing. Secondary thread:
Macro App **Settings modal freeze** fix (slim install) and **admin bypass loading** fix — both
coded but not deployed.

**Phase:** Guided-practice UI and Q9 tutorial fixes are **implemented locally and Matrix app
builds green** (`npm run build`). **Nothing has been deployed** (`student-portal` `deploy:prod`)
and **nothing committed/pushed** this session. Chase last asked to **remove fraction-help
draggability** and lock the trigger at **347, 151** with no border and no position readout —
that is done.

**Exact next step:** Deploy student portal so Chase can verify live, then commit/push Matrix app
+ student-portal when he says "put on GitHub" or end of session.

---

## 2. Chase's desired feel

- **Row-entry brackets** must line up with the row being edited (e.g. R2), not look like a third
  row sitting too low.
- **Fraction-help exclamation** should sit **on top of everything** (not clipped inside matrix
  frames), at a **fixed tuned spot** — currently **347×151** viewport coords. **No border box,
  no `pos:` debug readout, not draggable** (click-only to open help).
- **Q9 tutorial text** must match what's on screen — was **off by one step**; first caption
  must not describe content that hasn't appeared yet.
- **Step 3 Q9 copy** (approved wording): *"Both denominators need to be 3. Multiply the top and
  bottom of the first fraction by 3."*
- **Dwell/drag on the help trigger was tried and rejected** — head-mouse + tiny grip didn't
  work; viewport portal + dwell latch helped briefly, then Chase wanted it **fixed and
  click-only**.
- Student portal was **already even with `origin/main`** at session start; all changes are local
  dirty files.

---

## 3. Accepted decisions

| Decision | Why |
|---|---|
| `GuidedPracticeRowEntrySlot` measures target row vs matrix anchor (`getBoundingClientRect`) instead of CSS `marginTop` calc | Calc drifted in portal embed (`--matrix-cell-height` vs row height); measurement matches row-merge pattern |
| Entry grid class `matrix-entry-row` (not `matrix-result-matrix`) + portal CSS caps bracket height to one row | Two-row bracket styling made blank row look like a third row |
| Fraction-help trigger portaled to `document.body`, `position: fixed`, `z-index: 99999` | Escapes overflow/stacking in matrix embed; draggable across viewport was later removed |
| Fixed position in `fractionHelpButtonPosition.ts`: both slots `{ x: 347, y: 151 }` | Chase tuned placement; no localStorage persistence anymore |
| `useSegmentedHelpAnimation`: advance `stepIndex` **after** segment finishes (not before `playSegment`) | Fixed caption leading animation by one step |
| Q9 uses separate `ADD_SUBTRACT_HELP_INTRO` at step 0; pause captions use `instructions[stepIndex - 1]` | Multiply (Q5) keeps `instructions[stepIndex]` — intro already future-tense |
| Q9 segment boundaries (local, uncommitted): `0–2.2, 2.2–4.5, 4.5–11.8, 11.8–25.7, 25.7–37.7, 37.7–68.2` | Aligned to `Manim Trial/fraction_add_fractions_marks.json` pause marks |
| Student portal `App.tsx`: add `!adminBypass &&` before `guidedPracticeAccessChecked === null` loading gates | Instructors skip RPC → access stayed `null` → infinite Loading on Gauss-Jordan (and similar routes) |
| Macro App `useMacroAppShell.ts`: `flushSync(() => setShowSettingsModal(true))` after browser pre-freeze | Settings modal race in slim install — live browser over modal |
| Deleted `useDwellAttachDrag.ts` + `dwellStationary.ts` from Matrix app | Only used for rejected draggable help trigger |

---

## 4. Rejected directions — do not redo

- **Separate drag grip** (6px ⋮⋮) on fraction-help trigger — unusable with dwell/head-mouse.
- **Draggable help trigger** (mouse or dwell-latch) — Chase explicitly removed draggability;
  do not re-add without asking.
- **localStorage position tuning** for help trigger — removed with drag; use
  `FRACTION_HELP_BUTTON_DEFAULTS` only.
- **Yellow border/background shell** around exclamation icon — Chase wanted icon only, no chrome.
- **`marginTop` calc** for row-entry vertical align — replaced by measured slot; don't revert.
- **Incrementing tutorial step before playing segment** in `playCurrent` — causes off-by-one
  captions; keep post-play increment in `handleTimeUpdate`.

---

## 5. Current implementation state

### Matrix app (`School Scrips/Matrix app`) — **dirty, not committed**

| File | Change |
|---|---|
| `GuidedPracticeRowEntrySlot.tsx` | **New** — measured row-entry vertical align |
| `GuidedPracticeSolver.tsx` | Row entry slot; fraction help outside pointer-events-none layer |
| `GuidedPracticeFractionHelpButton.tsx` | Portal to body, fixed click-only trigger |
| `fractionHelpButtonPosition.ts` | Fixed defaults 347,151; no localStorage |
| `GuidedPracticeFractionHelpPanel.tsx` | Q9 intro + instruction offset; step 3 copy; segment times |
| `useSegmentedHelpAnimation.ts` | Step advances after segment completes |
| `MatrixEntryGrid.tsx` | `matrix-entry-row` class |
| `theme.css` | Trigger styling (no border, pointer cursor) |
| `fraction-add-fractions.mp4` | Modified (binary) |
| Also dirty: `GuidedPracticeOverlay.tsx`, `use-guided-practice-session.ts` | Review diff before commit — may be from earlier in session |

**Deleted:** `src/app/hooks/useDwellAttachDrag.ts`, `src/app/utils/dwellStationary.ts`

**Build:** `npm run build` passes (verified after drag removal).

**Git HEAD:** `a9938bb` — *Update Q9 help with corrected fraction animation* (remote matches; local
ahead only via uncommitted edits).

### Student portal (`School Scrips/student-portal`) — **dirty, not committed**

| File | Change |
|---|---|
| `src/app/App.tsx` | `adminBypass` guard on guided-practice loading |
| `src/styles/matrix-embed.css` | Single-row `matrix-entry-row` brackets |
| `src/styles/guided-practice-fraction-help.css` | Viewport trigger styles, no border/drag/dwell |

**Remote:** even with `origin/main` at `a96d669` at session start.

### Macro App (`School Scrips/Macro App`) — **dirty, not committed**

| File | Change |
|---|---|
| `renderer/src/hooks/shell/useMacroAppShell.ts` | Settings modal `flushSync` fix |
| `docs/EMBEDDED_BROWSER_AND_MODALS.md`, `docs/SLIM_DISTRIBUTION_BUILD.md`, `AGENTS.md` | Docs for fix + slim branch naming |
| `config/d2l-courses.json` | Machine-local dirty — **do not commit** |

**Not rebuilt/deployed:** slim installer still needs rebuild for Settings fix on install.

### Verification Chase has NOT done live

- Gauss-Jordan practice after portal deploy (loading fix, row brackets, help trigger, Q9 tutorial).
- Slim Macro App Settings modal after installer rebuild.

---

## 6. Open questions and constraints

- **Q9 step 4–7 copy** may still need tuning as Chase watches the retimed video — only step 3 was
  explicitly approved this session.
- **`op1-row-entry` vs `op2-row-entry`** both use same coords (347,151) — Q9 row-entry may need
  a different Y once Chase checks R2 placement.
- **Pre-existing `tsc` errors** in student-portal (guided practice types) — not introduced here;
  don't block deploy on them unless they fail the build script.
- **No commit/push/deploy** unless Chase asks — handoff only.
- **Never open GUI** for verification without permission; deploy is fine when asked.

---

## 7. Exact next step

1. **`npm run deploy:prod`** in `School Scrips/student-portal` (embeds Matrix app changes).
2. Chase verifies Gauss-Jordan guided practice: row brackets, fixed `!` at 347,151, Q9 tutorial
   step sync + step 3 wording.
3. On approval: commit Matrix app + student-portal (separate repos); Macro App separately if
   desired. Skip `config/d2l-courses.json`.
4. Optional: rebuild slim Macro App installer for Settings `flushSync` fix.

---

## Read first (fresh agent)

1. This file (`agent docs/momentum-handoffs/latest.md`)
2. `School Scrips/Matrix app/AGENTS.md` — step numbering note if tutorial steps come up
3. `School Scrips/Matrix app/src/app/components/guided-practice/GuidedPracticeFractionHelpPanel.tsx` — Q9 segments + copy
4. `School Scrips/student-portal/src/features/guided-practice/GuidedPracticeView.tsx` — portal embed shell
