# Momentum handoff — Row-scaling notation + wrong-answer recovery

**Written:** 2026-09-19 (Saturday, ~1:42 PM)

---

## 1. Objective and current phase

**Active thread:** Gauss-Jordan **guided practice** — row-scaling **row-notation step** (op1,
`1/3R1→R1`), **wrong-answer mini-tutorial**, **row-scaling notation help** (5-step panel),
and Part 3 parity for pick-cell / operation-type recovery.

**Phase:** Most features are **implemented locally and headless tests pass (70)**. Chase
**still blocked on device**: typing **`1/3R1→R2`** (wrong but structurally complete) **does
not submit / does not start the reciprocal mini-tutorial** — no clear error either. **Nothing
committed.** Next agent should **fix submit → wrong-answer recovery on device**, then Chase
re-verifies.

---

## 2. Chase's desired feel

- **Wrong row notation must always be submittable** when it looks like real notation (e.g.
  `1/3R1→R2`) — even when rows don't match. That should **start the mini-tutorial** (reciprocal
  → which row → which row changes → retry → give answer), not silently fail or show only a
  format error.
- **Row transformation builder:** Enter commits; **Submit** on the overlay is the answer. (Enter
  used to auto-submit; removed to fix × cancel — may be why Submit feels broken — verify.)
- **× on row builder** = abandon, back to empty **Tab or click** — must **not** count as wrong.
- **Backspace** on row builder deletes whole **R1 / R2 / →** tokens, not one digit at a time.
- **Row-scaling help tutorial (5 steps):** **Back to question** on the **left** of the tip on
  steps 1–4 (absolute position — **tutorial box must not shift** when step 5 drops the side
  exit). Step 5 keeps **Back to question** in the bottom actions row → feedback modal → resume.
- **Help step 5 example** must **not** be the problem answer — use **`2/7 R2 → R2`**, not `1/3 R1 → R1`.
- **Never launch GUI / deploy / commit** without asking.

---

## 3. Accepted decisions

| Decision | Why |
|---|---|
| Scale-only **row-notation recovery** state machine | Reciprocal keypad → R1/R2 picks → retry notation → give answer |
| `isStructurallyCompleteRowOp` accepts wrong rows | `1/3R1→R2` parse fails but shape is valid — must submit as wrong |
| `backspaceRowOpExpression` | Whole row labels/symbols delete as one token |
| `closeBuilder` vs `cancelBuilder` | Enter commit uses close; × cancel restores slot snapshot — no wrong answer |
| Row-scaling help exit **absolutely positioned** left of panel | Prevents layout jump on step 5 |
| Skip home button → **Skip to row scaling help** | Lands on op1 row-notation + opens help |
| Extract session hook pieces | `guided-practice-answer-flow.ts`, `use-guided-practice-row-notation-recovery.ts`, etc. |
| Part 3 parity | RREF reference, pick-cell pulse, operation wrong messages, row notation help `!` button |

---

## 4. Rejected directions — do not redo

- **Pre-fill row-op builder with correct answer** on open (testing aid) — removed; confuses QA.
- **Auto-submit on Enter** after commit — removed when fixing × cancel; may need **targeted**
  restore (submit on Enter **only**, never on ×) if two-step Enter+Submit is too opaque.
- **Side exit button in flex layout** next to tutorial panel — caused **step 5 layout jump**;
  use absolute positioning instead.
- **Row builder × = wrong answer** — explicitly wrong; fixed with snapshot restore.
- **Help example `1/3 R1 → R1`** on step 5 — same as op1 answer; changed to `2/7 R2 → R2`.

---

## 5. Current implementation state

### Matrix app — **dirty, not committed**

| Area | Key files |
|---|---|
| Row-op parser | `parse-row-op-expression.ts` — `isStructurallyCompleteRowOp`, `backspaceRowOpExpression`, `validateRowOpDraft` |
| Wrong recovery core | `guided-practice-row-notation-recovery.ts`, `use-guided-practice-row-notation-recovery.ts` |
| Recovery UI | `GuidedPracticeRowNotationRecovery.tsx`, `GuidedPracticeOverlay.tsx` |
| Session | `use-guided-practice-session.ts` (~820 lines — over cap; further extract if adding more) |
| Builder commit | `guided-practice-builder-commit.ts` — `closeBuilder` on Enter, not `cancelBuilder` |
| Row-scaling help | `GuidedPracticeRowNotationHelpPanel.tsx`, `rowNotationHelpSteps.ts`, `ReciprocalFlipAnimation.tsx` |
| Wrong recovery Part 3 | `guided-practice-wrong-recovery.ts`, `RrefReferenceMatrix.tsx`, matrix display flash |
| Tests | `parse-row-op-expression.test.ts`, `guided-practice-row-notation-recovery.test.ts`, `guided-practice-wrong-recovery.test.ts`, `rowNotationHelpSteps.test.ts` — **70 tests pass** |

### Student portal — **dirty, not committed**

| File | Role |
|---|---|
| `guided-practice-fraction-help.css` | Row notation help layout + `__exit` absolute left |
| `matrix-embed.css` | Exclude `gp-row-notation-help-screen__exit` from base button styles |
| `GuidedPracticeHomePanel.tsx` | Skip to row scaling help |
| `GuidedPracticeView.tsx`, `guidedPracticeActivity.ts`, `matrix-app.d.ts` | skip + `rowNotationHelpOpen` |

### Expected wrong-answer flow (op1 scale)

1. Skip to row scaling help or reach op1 row-notation step.
2. Tab or click blank slot → row-op builder (starts **empty**).
3. Type `1/3R1→R2` → **Enter** → value appears in slot, builder closes.
4. **Submit** → mini-tutorial: "What's the reciprocal of **3**?" …

### Chase's report (unverified fix)

- Types `1/3 R1 → R2`, **cannot submit**, no message, mini-tutorial does not start.
- **Likely causes to check first:**
  1. **Two-step flow** — Enter only stages to slot; Submit disabled or not clicked?
  2. **`submitSlotDraft` not wired** or `slotDraft` empty after Enter (snapshot/cancel bug)?
  3. **Portal embed stale** — needs hard refresh after Matrix bundle rebuild?
  4. **Regression** — remove auto-submit broke the path Chase expects (Enter = submit wrong answer)?

### Verification done this session

- `npm test -- --run` in Matrix app — **70 pass**
- No device GUI run (Chase verifies)

---

## 6. Open questions and constraints

- **Primary fix:** Wrong structurally complete notation (`1/3R1→R2`) must **Submit** (or Enter
  if restored) → **start recovery** without silent failure.
- Consider **Enter = commit + submit** again, with **`closeBuilder` only on Enter** and
  **`cancelBuilder` on ×** (already split) so × never submits.
- **`use-guided-practice-session.ts` is ~820 lines** — extract before large adds (hard cap 800).
- **No commit/push/deploy** unless Chase asks.
- Read `School Scrips/Matrix app/AGENTS.md` — Portal Wide ~812×460; row-notation is op1 step 4 in UI (~question index 2).

---

## 7. Exact next step

1. Read this file, then `School Scrips/Matrix app/AGENTS.md`.
2. Reproduce on device: **Skip to row scaling help** → close help → type **`1/3R1→R2`** → Enter → Submit.
3. **Fix** until wrong answer reliably starts mini-tutorial (reciprocal of 3 → row picks → retry).
4. If Enter+Submit is too many steps for Chase, restore **Enter = submit** without breaking × cancel.
5. Report what broke and what Chase should re-test — **do not commit** unless asked.

---

## Read first (fresh agent)

1. `agent docs/momentum-handoffs/latest.md` (this file)
2. `School Scrips/Matrix app/AGENTS.md`
3. `use-guided-practice-row-notation-recovery.ts` — submit + recovery start
4. `use-guided-practice-session.ts` — `commitBuilder`, `openRowOpBuilder`, `cancelBuilder` / `closeBuilder`
5. `parse-row-op-expression.ts` — structural validation
6. `GuidedPracticeRowNotationHelpPanel.tsx` — tutorial exit layout
