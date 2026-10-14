# Momentum handoff — Factoring Guided Practice: double bubble

**Written:** 2026-10-13 (day-valid only)
**Repos touched:** `School Scrips/Factoring Guided Practice`, `School Scrips/student-portal`
**Git:** nothing committed or pushed. No GitHub, no end-of-session actions.
(Logic-homework files in `student-portal` are dirty from a different chat — not this work.)

---

## 1. Objective and phase

Chase is building out **Factoring Guided Practice**, used in the student portal (`@factoring-guided/`
alias) and the Macro App preview. The "Double bubble products" plan
(`C:\Users\chase\.cursor\plans\double_bubble_products_3b7e2795.plan.md` — do **not** edit it) was
fully implemented this session. **Phase: built and headless-verified, not yet seen by Chase.**
Next is his visual review: he drags the new layout with Move box and pastes the tuner JSON back.

## 2. Chase's desired feel

- Mirrors his standalone `factoring-app` "double bubble" (Bubble / ProductArrows): red arrows,
  inner product below, outer product above. His words: "this will be an animation… it's gonna do
  what the inner product and the outer product does in the other app."
- Bigger bubble, "make the parentheses bigger even." Arrows, product boxes and the control row
  must move **with** the bubble when he uses Move box.
- Student flow: coefficients (Enter after each) → left constant, right constant (Enter after
  each) → products animate → the `+` signs **flash** and he clicks them to flip to `−` → products
  update live → Check answer. **No sum before Check.** Check shows the sum with ✓ / ✗.
- A "control knob" row directly under the bubble: **Check answer, Swap last, New last, New first.**
  "Just do the best you can. I just need to see something on there so I can evaluate."
- "Set up parentheses" choice: only two empty, bigger parentheses plus `= 0`. Nothing inside.

## 3. Accepted decisions (all implemented)

- Problem 1 is pinned: `121x^2 - 25 = 0` (no GCF). Opening question "What should we do first?"
  (Factor out the GCF / Set up parentheses). Matrix-style **Use answer** cheat sits outside the
  blue card.
- Formulas as in the standalone app: inner = signed B × C, outer = A × signed D, for
  `(Ax + B)(Cx + D)`. Correct = inner + outer equals the middle term **and** B×D equals the last
  term (and A×C the first).
- Coefficients accept any pair multiplying to the first term (121 → 11/11, 121/1, …).
  Constants graded as positive whole numbers multiplying to |c|; signs start `+`.
- Swap last swaps constants **with** their signs. New last → back to constant entry.
  New first → back to coefficients.
- Correct Check → step `factoredDone`: "Factored! Solving comes next." + Next problem button
  (stub; solving the roots after the bubble is not built).
- Layout is baked in percentages of `.factoring-gcf-stage` (`factoringPortalEmbedLayout.ts`,
  info block `xPct` 50.6, storage key `factoring-layout-placed-v10`).

## 4. Rejected directions

- First skeleton with dashed answer cells — "not it." Restyled to the standalone Bubble look.
- Cheat button inside the text box / inside the blue card — rejected; it hangs outside the card.
- Yes/No GCF opener replaced by the two-choice first move.
- Do not add a parallel mechanism: the bubble extends `practiceSession.ts`; no second session
  engine.

## 5. Implementation state

Factoring Guided Practice (`src/`):
- `engine/doubleBubble.ts` (new, pure): `parseFactoredBubbles`, validators, `computeBubbleProducts`,
  `bubbleSum`, `isBubbleCorrect`, `problemQuad`.
- `engine/practiceSession.ts` (483 lines): steps `parenSkeleton → parenConstants → bubbleProducts →
  factoredDone`; state `bubbleConstants / bubbleSigns / bubbleSignsTouched / bubbleChecked`;
  transitions `setBubbleActiveBlank`, `submitSkeletonCoeff`, `submitBubbleConstant`,
  `toggleBubbleSign`, `swapLastNumbers`, `resetLastNumbers`, `resetFirstNumbers`,
  `checkBubbleAnswer`, `isDoubleBubbleStep`; Use answer covers the new steps.
  Removed `expectedSkeletonLeadCoeffs` and `matchesSkeletonLeadCoeff`.
- `app/hooks/useBubbleAnchors.ts` (new): measures A/B/C/D field centers so arrows follow the bubble.
- `app/components/`: `FactoringParenSkeleton` (enlarged bubble, tappable flashing signs),
  `FactoringParenSkeletonFloat` (one host: bubble + products + sum + knob),
  `FactoringBubbleProducts` (arrows, boxes, sum), `FactoringBubbleKnob` (new),
  `FactoringExpressionBuilder` (new `digits` mode), `FactoringFirstMoveChoices` (empty-paren
  sublabel), `FactoringUseAnswerButton` (cheat steps), `FactoringStepControls`.
- `FactoringPracticeView.tsx` is **349 lines** (over the 300 line mark; this change shrank it).
  Do not grow it — extract instead.
- Tests: `practiceSession.test.ts`, `doubleBubble.test.ts` → **26 pass** (`npx vitest run`).
  `npx tsc --noEmit` clean in this package.

student-portal:
- `styles/factoring-double-bubble.css` (new, imported in `styles/index.css`); the bubble block was
  moved out of `factoring-guided-embed.css`. Portal's own `tsc` shows unrelated pre-existing errors
  in `generic-quiz`; `npx vitest run factoring` passes.

Session scorecard already bumped for this deliverable.

## 6. Open questions and constraints

- **Nothing has been viewed on screen.** Geometry is untested visually: outer product box height
  above the bubble row, `margin-top: 4.6rem` reserved for the inner product box, the arrow
  depths (`INNER_DEPTH 30`, `OUTER_DEPTH 40`), the knob wrapping to two rows, and the outer box
  possibly overlapping the equation. Expect tweaks after Chase's look.
- Never launch a GUI or open a browser without asking (his head-mount mouse + dwell click).
  Verify headlessly, then state what to run/expect — as a statement, not a question.
- Modals never dismiss on backdrop click. No ephemeral "Copied!"-style feedback.
- Never deploy to Netlify unless Chase says so in that message.
- `+`/`−` stays inside each bubble for now (Chase said he may change that later).

## 7. Exact next step

Tell Chase (flat statement): open Factoring Guided Practice in the portal, problem 1, pick
"Set up parentheses", go through coefficients → constants → watch the arrows → click a flashing
sign → Check answer; then drag with Move box and paste the tuner JSON. When he sends the JSON,
bake it into `factoringPortalEmbedLayout.ts` and bump the `factoring-layout-placed-vN` key.
Fix any visual problems he reports (anchor geometry is in `FactoringBubbleProducts.tsx`; styles
in `factoring-double-bubble.css`).
