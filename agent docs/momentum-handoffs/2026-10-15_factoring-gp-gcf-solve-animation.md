# Momentum handoff — Factoring Guided Practice (portal GCF path)

**Written:** 2026-10-15 (day-valid only)
**Repos touched:** `School Scrips/Factoring Guided Practice`, `School Scrips/student-portal` (embed CSS + layout bake lives in GP app config)
**Git:** uncommitted local work in both repos above. **Nothing committed or pushed.** No end-of-session, no Netlify.

---

## 1. Objective and phase

Chase is polishing **Factoring Guided Practice** in the **student portal embed** (floating blue prompt, step lines, zero-product drop, roots keypad, wrong-answer walkthrough). Current focus: **GCF → linear inner → “what do you want to do next?” → set equal to zero → solve**, with the **same worked solve animation** as difference-of-squares / double-bubble (gold move under both sides, red strikes, divide bars, answer slide).

Phase: **feature-complete for the pinned test problem; portal QA still owed** on roots-reveal animation after two wrong root attempts.

---

## 2. Chase's desired feel (his language)

- **“What do you want to do next?”** with three choices that all start from **done factoring** wording on options 1–2:
  1. Done factoring — set the GCF and what's inside equal to zero
  2. Done factoring — only set what's inside equal to zero
  3. Factor what's still inside the parentheses
- **One wrong pick on that step → teach immediately** (no second guess, no red “Try again”). Show **specific** why that choice is wrong, then **auto-advance on the correct path** (blue teaching note in the lower-left float, not error red).
- **Move box / layout tuner** must not show fake future UI (empty tuner rects for ghosts).
- **Solve animation** must match the existing diff-squares board: cancel, move, divide — **per factor** on GCF paths (`2x = 0` and `4x − 9 = 0`), not jump straight to green solutions.
- Default **info block height** for `default` step key ~**64.9%** (tuner paste 2026-10-15); **solveRoots** info block stays **24%** so keypad isn’t pushed down.

---

## 3. Accepted decisions

| Area | Decision |
|---|---|
| Grading “next step” | `innerNeedsFurtherFactoring()` (inner has `x²`) → **factor more**; else GCF → **set GCF + inside**; else **inside only**. Not `canMarkDone` / AB-binomial only. |
| Wrong “next step” | `submitWhatHappensNext` → `wrongWhatHappensNextFeedback` + `applyWhatHappensNextChoice(correct)` + `teachingNote` on state. |
| Zero-product step 2 | `useFactorSplitTransition` all paths; GCF skips bubble shrink, drops from step 1. Triple line when inner splits to two binomials. |
| Roots after 2 misses | `buildRootsWalkthroughForSolve` from GCF/inner/`zeroFactors`, not only `confirmedFactoredProduct`. |
| Roots reveal animation | `useRootsRevealWalkthrough` + `FactoringSolveBoard`; **wait for board refs** before animating; **force factor-column layout** during `rootsReveal` solving/done. |
| Test pin | `PIN_GCF_TRINOMIAL_AS_PROBLEM_1 = true` → problem 1 = **`8x² − 18x = 0`** (`fixedGcfTrinomialPracticeProblem`). Diff-squares pin **off**. |
| Portal layout bake | `FACTORING_PORTAL_EMBED_LAYOUT` in `factoringPortalEmbedLayout.ts` — Chase pasted tuner JSON 2026-10-15 (`default` hPct 64.9). |

---

## 4. Rejected / do not redo

- **“Are you done factoring and ready to solve?”** prompt — replaced with **“What do you want to do next?”**
- **Second guess** on the next-step question with generic red try-again.
- **Marking “set GCF and parentheses = 0” wrong** on linear inner after GCF (fixed via `whatHappensNext` grading).
- **Global layout JSON** when Chase only wanted **default info height** — apply surgical diff to bake, not whole-tree replace without ask.
- **Move box mounting real future components** (solutions, elongated prompt) — use `FactoringLayoutTunerRect` ghosts only.

---

## 5. Implementation state (key files)

**Factoring Guided Practice** (`School Scrips/Factoring Guided Practice/`):

| Topic | Files |
|---|---|
| Next-step copy + one-strike teach | `src/engine/whatHappensNext.ts`, `practiceSession.ts` (`teachingNote`), `FactoringNextStepChoices.tsx`, `FactoringPracticeView.tsx` (teach tone on error float), `FactoringErrorMessageFloat.tsx` |
| Layout / tuner | `factoringPortalEmbedLayout.ts`, `FactoringLayoutTunerRect.tsx`, `FactoringPracticeView.tsx`, `useFactoringPortalLayout.ts` |
| Zero-product + split | `useFactorSplitTransition.ts`, `practiceRules.ts` (`setEqualZeroLatexLines`, `splitSetEqualZeroLine`) |
| Roots walkthrough data | `rootsWalkthrough.ts`, `useFactoringPracticeSession.ts` |
| Roots reveal animation | `useRootsRevealWalkthrough.ts` (**board wait loop**, KaTeX base selector), `FactoringSolveBoard.tsx`, `FactoringStepLineFloat.tsx` |
| Keypad | `FactoringExpressionBuilder.tsx`, `expressionMinus.ts`, `useFactoringExpressionBuilder.ts` |
| Pin / generators | `config.ts`, `generators.ts`, `buildSet.ts` |

**Student portal:** `src/styles/factoring-guided-embed.css` — teach-tone error float, **`.factor-col`** stack for factor + solve board under each step-2 factor.

**Tests:** `npm test -- --run` in Factoring GP — **63 passed** (last run this session).

**Uncommitted** in Factoring GP + student-portal (see git status); includes unrelated rational-functions assets in portal — **do not commit portal video work with factoring unless Chase asks for a combined push**.

---

## 6. Open questions / constraints

- **Portal QA not confirmed by Chase** after roots-reveal fix: wrong roots twice → Next → full cancel/divide for **both** `2x = 0` and `4x − 9 = 0`. If still broken, debug `useRootsRevealWalkthrough` DOM measure on monomial `2x` (monomial branch skips cancel when `b = 0` but should still divide).
- **`PIN_GCF_TRINOMIAL_AS_PROBLEM_1`** still on — turn off before shipping mixed sets.
- **No commit/push** unless Chase says pull / put on GitHub / end-of-session.
- **Never launch GUI / open browser** without permission; handoff test = tell Chase what to refresh and what to report.
- Read **`School Scrips/Factoring Guided Practice/AGENTS.md`** + root **`Programs/AGENTS.md`** for modal, file size, session tracking.

---

## 7. Exact next step

1. Read this file, then `School Scrips/Factoring Guided Practice/AGENTS.md`.
2. In **student portal** Factoring Guided Practice embed (refresh after dev build): pinned **`8x² − 18x`**, complete to **solve**, intentionally miss roots **twice**, tap **Next**, confirm **both** factors get the **full** Manim-style solve board animation (same feel as diff squares).
3. If animation fails or skips: fix `useRootsRevealWalkthrough` / factor-column DOM for GCF lines; re-run `npm test -- --run` in Factoring GP.
4. If Chase confirms green: ask whether to **turn off GCF pin** and whether to **put on GitHub** (Factoring GP + portal CSS only, not unrelated rational video files unless he wants them).

---

## Read first (next agent)

- `agent docs/momentum-handoffs/latest.md` (this file)
- `School Scrips/Factoring Guided Practice/AGENTS.md`
- `School Scrips/Factoring Guided Practice/src/engine/whatHappensNext.ts`
- `School Scrips/Factoring Guided Practice/src/app/hooks/useRootsRevealWalkthrough.ts`
