# Momentum handoff — Factoring Guided Practice (portal GCF roots-reveal polish)

**Written:** 2026-10-15 (day-valid only)
**Repos touched:** `School Scrips/Factoring Guided Practice`, `School Scrips/student-portal` (one CSS line)
**Git:** uncommitted local work in both repos (plus unrelated rational-functions assets in the portal). **Nothing committed or pushed.** No end-of-session, no Netlify.

---

## 1. Objective and phase

Chase is polishing **Factoring Guided Practice** in the **student portal embed**. Focus: pinned GCF problem **`8x² − 18x = 0`** → solve → miss roots twice → **Next** → **worked solve animation for both step-2 factors** (`2x = 0`, `4x − 9 = 0`) like difference of squares (gold move under both sides, red strikes, divide bars, answer slide) → green solutions box + blue "next problem" prompt.

Phase: **three bugs fixed this session, layout bake just updated; Chase has NOT yet confirmed any of it in the portal.** He reviews only in the portal (hard refresh at `http://127.0.0.1:5340/#/factoring-guided-practice`; dev server already running on 5340 — do not start a second one). The agent browser MCP could not connect, so nothing was seen by the agent; every report is code + tests.

---

## 2. Chase's desired feel (his language)

- Animations "a little bit faster", factor columns "separated a little bit more, they're very close together".
- Answers must not be "lopsided": the **x's lined up with each other** (`x = 0` brought down to sit level with `x = 9/4`).
- **Green box** = solutions only ("Solutions are x = 0, 9/4"), **no Next button in it**. He positions it himself with Move box → Copy.
- **Blue box** that says to click to go to the next problem **belongs in the PROMPT box** (the blue prompt card, same slot as the roots keypad), **not** the red wrong-answer slot. He was explicit and annoyed that it was first put in the wrong-answer slot.
- **No keypad** may appear after the solve (it popped open with stale `x = 3,8`).
- When he pastes tuner JSON, he means "bake this" — apply it.

---

## 3. Accepted decisions / what was done

| Area | Change |
|---|---|
| Crash (root cause of "no animation, scattered numbers") | `useRootsRevealWalkthrough.ts`: `constBox` is `null` for monomial `2x = 0`; `constBox.left` threw, a swallowed `catch` pinned the finished state. Now null-safe; monomial detected by `solve.moveAmount === 0`; KaTeX splits `4x − 9` over **two `.base` rows**, so all `.base` rows are measured; `catch` now `console.error('[roots-reveal] animation aborted', err)`. |
| Pace | `PACE` 0.75 → **0.5** |
| Column spacing | student-portal `factoring-guided-embed.css` `.factoring-step-line-float__math-stack` gap `1.35rem` → **`2.6rem`** |
| Answer alignment | `factoring-double-bubble.css`: `.fsb__answer` fixed `height: 3.2rem` (centered); fraction `margin-left` only on `.fsb__frac--neg` (class added in `FactoringSolveBoard.tsx`) |
| Green box | `FactoringSolutionsFloat.tsx`: no action button/props; CSS `__action` rule removed |
| Blue prompt | `rootsReveal.ts`: `ROOTS_DONE_PROMPT = 'Click Next to go to the next problem.'`; `rootsRevealMessage`/`ActionLabel` back to **prompt-only** (red box only after 2nd miss). `FactoringPracticeView.tsx`: info float renders when `rootsReveal === 'off' || 'done'`; in done it shows `ROOTS_DONE_PROMPT` + a `factoring-gcf-menu-btn--compact-nav` **Next** → `session.onAdvanceAfterRootsReveal`; `outsideCheat` hidden; `hostBuilderUnderFloat` gated `!rootsDone` (kills keypad). |
| Layout bake | `factoringPortalEmbedLayout.ts` `solutionsRectPct` = **`{ xPct: 37.5, yPct: 23.1, wPct: 18, hPct: 26.7 }`** — **estimated from Chase's screenshot, not a pasted JSON** (previous paste was `39.2, 22.9, 28, 25.3`). |
| Stale session override | `useFactoringPortalLayout.ts`: `PLACED_STORAGE_KEY` bumped `v22` → **`v23`**. Session-stored layout silently overrides the bake (that is why his earlier bakes of the green box never showed — screenshot showed old `62/14/28/22`). **Always bump this key when baking new tuner JSON.** |

Tests: `npm test -- --run` in Factoring GP → **63 passed** (last run after the final edit). `npx tsc --noEmit` shows 4 **pre-existing** errors in files not touched (`FactoringGcfInfoBlock.tsx`, `FactoringParenSkeleton.tsx`, `FactoringParenSkeletonFloat.tsx`, `whatHappensNextFeedback.test.ts`).

---

## 4. Rejected / do not redo

- Blue "Click Next to go to the next problem" in the **red wrong-answer float** — wrong slot; must be the prompt box.
- A **Next problem** button inside the green solutions box.
- Global/full layout-JSON replace when only one rect was asked about — apply surgical diffs (last two pastes only differed in `solutionsRectPct`).
- Reintroducing the "Are you done factoring and ready to solve?" prompt, or a second guess on the next-step question (carried from earlier handoff).
- Do not "fix" the 4 pre-existing `tsc` errors unless asked.

---

## 5. Key files

Factoring GP (`School Scrips/Factoring Guided Practice/src/`): `app/hooks/useRootsRevealWalkthrough.ts`, `app/components/FactoringSolveBoard.tsx`, `FactoringSolutionsFloat.tsx`, `FactoringPracticeView.tsx`, `FactoringStepLineFloat.tsx`, `engine/rootsReveal.ts`, `engine/rootsWalkthrough.ts`, `app/config/factoringPortalEmbedLayout.ts`, `app/hooks/useFactoringPortalLayout.ts`, `styles/factoring-double-bubble.css`, `test/rootsReveal.test.ts`.
Student portal: `src/styles/factoring-guided-embed.css`.

---

## 6. Open questions / constraints

- **Unconfirmed in the portal:** full animation for both factors, spacing, aligned x's, green-box position, blue prompt + Next, no keypad, Move box → Copy capturing the green box. If Copy still does not capture a moved green box, the code path looked correct (`placedRef` → `formatFactoringLayoutForAgent`); reproduce with the stale-session fix first, and ask for a console check for `[roots-reveal] animation aborted`.
- `PIN_GCF_TRINOMIAL_AS_PROBLEM_1 = true` in `engine/config.ts` is **still on** — ask Chase before turning it off.
- **Never** launch GUI / open a browser without permission; hand-test = flat statement of what to refresh and what to report.
- **No commit/push** unless Chase says pull / put on GitHub / end-of-session. Do not commit the unrelated rational-functions portal assets with factoring unless he asks for a combined push.
- Root `AGENTS.md` rules still apply: modals never close on backdrop click, file-size caps (`FactoringPracticeView.tsx` is ~520 lines — extract before adding more), no ephemeral success feedback.

---

## 7. Exact next step

1. Read this file, then `School Scrips/Factoring Guided Practice/AGENTS.md`.
2. Ask Chase (flat statement, no GUI launch) to hard-refresh and run `8x² − 18x`: miss roots twice → Next → watch both solves; report spacing, x alignment, green-box spot, blue prompt + Next, and any console error.
3. If he pastes tuner JSON: diff against `FACTORING_PORTAL_EMBED_LAYOUT`, bake only what differs, **bump `PLACED_STORAGE_KEY`**, run tests.
4. If he confirms green: ask whether to turn off the GCF pin and whether to put on GitHub (Factoring GP + `factoring-guided-embed.css` only).

---

## Read first (next agent)

- `agent docs/momentum-handoffs/latest.md` (this file)
- `School Scrips/Factoring Guided Practice/AGENTS.md`
- `School Scrips/Factoring Guided Practice/src/app/hooks/useRootsRevealWalkthrough.ts`
- `School Scrips/Factoring Guided Practice/src/app/components/FactoringPracticeView.tsx`
- `School Scrips/Factoring Guided Practice/src/app/hooks/useFactoringPortalLayout.ts`
