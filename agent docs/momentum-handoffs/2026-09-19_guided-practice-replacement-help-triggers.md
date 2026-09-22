# Momentum handoff — Guided practice row-replacement + help triggers

**Written:** 2026-09-19 (Saturday, ~3:21 PM)

---

## 1. Objective and current phase

**Active thread:** Gauss-Jordan **guided practice** in Matrix app + student portal — full **row-replacement** wrong-answer parity with row-scaling (notation recovery, row-entry reveal, help panels), unified **help triggers** (yellow **!** + “Need help with …?” label), and **column-two** skip buttons + layout polish.

**Phase:** Implementation **complete locally** — **89 vitest tests pass** in Matrix app. Chase has **not device-verified** the latest round (help trigger on replacement animation, compact label shrink, `!` vs `?` fix). **Nothing committed** in Matrix app or student-portal.

---

## 2. Chase's desired feel

- **Help triggers:** Yellow **!** badge (exclamation — **not** a question-mark icon) beside a **small yellow text box** that **asks a question**: *Need help with multiplying fractions?* (question mark **in the text only**).
- Help triggers are **draggable** (grab label or area; icon click opens help).
- **Row-entry fraction help** uses **compact** label; **column-two** slots (`op3-*`, `op4-*`) get **wide** variant (+30px over compact).
- **Replace row-entry wrong reveal (step 16):** Short tip *Incorrect. Look at the animation to see how to do it.* — **Next inline** beside text (wider popover ~370px). **Adding-fractions help** sits **above the animation** inside the same `MovablePanel` (not portaled beside matrix — avoids overlapping the sum).
- **Row-scaling row-entry wrong reveal:** Keeps full `wrongHint` + inline Next.
- **Operation-type wrong (step 14 etc.):** Popover **~350px wide** so feedback isn’t a tall narrow stack. After wrong **Row Swap** on a **replacement** step, **Row Scaling must stay clickable** (only the wrong pick grays out) — student can still try scaling even though it’s wrong.
- **Row-notation recovery reciprocal prompt:** Popover **270px** (80px trim) so keypad/matrix don’t collide.
- **Never launch GUI / open browser** without asking. Handoff statements only for device checks.

---

## 3. Accepted decisions

| Decision | Why |
|---|---|
| Row-replacement notation recovery | Mirror scale flow: opposite → pivot row → target row → retry → give answer |
| Row-entry replacement reveal | `DynamicRowReplacementAnimation` in `MovablePanel`; fraction help embedded above animation |
| `GuidedPracticeHelpTrigger` | Replaces deleted `GuidedPracticeFractionHelpButton` + `GuidedPracticeRowNotationHelpButton` |
| `helpTriggerCopy.ts` | Central “Need help with {topic}?” strings |
| Replacement reveal opens **add-subtract** fraction help | Not row-replacement notation help |
| Column-two home skip buttons | Col 1 · Scale/Replace help/Replace entry + Col 2 · same (op3/op4 indices) |
| `operationButtonPulse` fix for `row-replacement` expected | Wrong row-swap → pulse scaling **and** replacement; wrong row-scaling → pulse replacement only |
| `OPERATION_TYPE_WRONG_POPOVER_WIDTH_EXTRA = 150` | Steps like 14 — wide wrong-operation feedback |
| Icon = **!**, label text ends with **?** | Chase corrected agent that changed icon to `?` |

---

## 4. Rejected directions — do not redo

- **Question-mark icon** on yellow badge — Chase wants **!** only; **?** belongs in the label text.
- **Long row-replacement hint** on replace row-entry reveal — use short “Look at the animation…” only.
- **Row-replacement notation help** during replace row-entry reveal — use adding-fractions tutorial instead.
- **Portaled fraction help at x:380** during replacement reveal — overlaps animation; now embedded in panel.
- **Changing replacement animation** to show common-denominator fraction conversion — explicitly left as-is.
- **Auto-commit / push** — not done; Chase drives git at end of session.

---

## 5. Current implementation state

### Matrix app — **dirty, not committed** (89 tests pass)

| Area | Key files |
|---|---|
| Help trigger | `GuidedPracticeHelpTrigger.tsx`, `helpTriggerCopy.ts`, `helpTriggerLabelWidth.ts`, `FractionHelpAlertIcon.tsx` |
| Positions | `fractionHelpButtonPosition.ts` — row entry x:327; row notation x:280 |
| Replace flows | `guided-practice-row-replacement-notation-recovery.ts`, `DynamicRowReplacementAnimation.tsx`, `GuidedPracticeRowEntryReplacementReveal.tsx`, `GuidedPracticeRowReplacementNotationHelpPanel.tsx`, `rowReplacementNotationHelpSteps.ts` |
| Scale flows | `DynamicRowScalingAnimation.tsx`, `GuidedPracticeRowEntryScalingReveal.tsx`, row-scaling help panel |
| Session hooks | `use-guided-practice-wrong-flows.ts`, `use-guided-practice-session-help.ts`, `use-guided-practice-row-entry-reveal.ts` |
| Overlay / layout | `GuidedPracticeOverlay.tsx` — inline Next on row-entry reveal; `guided-practice-wrong-recovery.ts` — popover widths, `operationButtonPulse` |
| Catalog | `guided-practice-catalog.ts` — `OP3_*`, `OP4_*` indices |
| CSS | `src/styles/theme.css` — help trigger + label compact/wide sizes |

### Student portal — **dirty, not committed**

| Area | Key files |
|---|---|
| Skip buttons | `GuidedPracticeView.tsx` — 6 buttons (Col 1 + Col 2) |
| Exports | `guidedPracticeActivity.ts`, `matrix-app.d.ts` |
| Help trigger CSS | `guided-practice-fraction-help.css` — must keep `gp-fraction-help-trigger` classes for icon sizing |

### Verification

- `npm test -- --run` in Matrix app → **89 passed**
- **No GUI smoke test** this session (Chase dwell-clicks; agent must not launch)

---

## 6. Open questions and constraints

- **Device pass needed:** Col 2 skip paths, step 12 compact help label, step 16 embedded help above animation, step 14 wide popover + row scaling still clickable after wrong swap.
- **Fine-tune positions:** Help triggers are draggable but defaults may still need nudging per screen.
- **File size:** `use-guided-practice-session.ts` was extracted but verify still under 800 before adding more.
- **Frozen:** Calendar 2.0 — do not touch.
- **Git:** Do not commit until Chase says “put on GitHub” or end-of-session protocol.

---

## 7. Read first (fresh agent)

1. This file (`agent docs/momentum-handoffs/latest.md`)
2. `School Scrips/Matrix app/src/app/components/guided-practice/GuidedPracticeHelpTrigger.tsx`
3. `School Scrips/Matrix app/src/app/components/guided-practice/GuidedPracticeSolver.tsx` — help trigger wiring
4. `School Scrips/Matrix app/src/app/hooks/guided-practice-wrong-recovery.ts` — popover + operation buttons
5. `School Scrips/student-portal/src/features/guided-practice/GuidedPracticeView.tsx` — skip buttons

---

## 8. Exact next step

**Wait for Chase’s device feedback** on the latest help-trigger + step 16 layout. If he reports overlap or wrong behavior, adjust `GuidedPracticeRowEntryReplacementReveal.tsx` / compact label CSS in `guided-practice-fraction-help.css` (portal) and `theme.css` (Matrix standalone). If everything looks good, ask whether to run **end-of-session protocol** (commit both repos).

**Skip-button smoke path for Chase (statement, not a question):** Home → **Col 2 · Replace entry** → wrong row → confirm embedded *Need help with adding fractions?* above animation, **!** icon, inline Next on wrong tip.
