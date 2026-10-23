# Momentum handoff: Gauss-Jordan "tap or click" copy

**Written:** 2026-10-22 (evening). Valid for today's continuation only.
**Nothing is committed or pushed.** Repos with uncommitted copy work: `School Scrips/Matrix app`, `School Scrips/student-portal`, `School Scrips/Macro App`, `Programs/` root (handoff + scratch catalog + session tracking). Commit only on "pull", "put on GitHub", or end of session.

## Objective and phase

Chase is reviewing the **Gauss-Jordan Method tutorial** in the student portal (tester CHASE1). He wants student directions to work for phones, so "click" became **"tap or click"**. After that landed, he screenshotted the yellow row-swap notation box and asked to **bold** "do not write this down."

Both copy changes are in the files. He has not said the bold looks right. The **live Netlify site is unchanged**.

This chat also did a **full pull** at the start (session set empty → every `pull: true` repo). Macro App (3 commits), student-portal (Probability on M1324 home), and student-session-kit (migration `097_probability_app.sql`) fast-forwarded. `npm run db:push` applied 097. Probability App is `pull: false` and was already current; do not mention it in a pull recap.

## Chase's desired feel

- Head-mounted gyro mouse + dwell click + speech-to-text. Students on phones **tap**; desktop users **click**. Directions must say both.
- No em dashes. Small buttons. No ephemeral success feedback. Never put a window on his screen without asking. Permission is per run.
- He reviews in the **portal**, not a standalone Matrix window. Handoff is a statement, never "want me to deploy?"
- Speech-to-text: "tab or click" in older practice copy was almost certainly meant to be "tap or click." Treat leftover "Tab or click" the same way if any remains.

## Accepted decisions

- Phrase is **"tap or click"** (tap first), not "click or tap."
- Scope was the tutorial first, then **all student-facing Gauss-Jordan click verbs** in Matrix tutorial + guided/unguided practice + fraction-help intros + portal Auto Solve wrap-up + portal page-error button + Macro `matrixSlotCatalog` prompts (gradebook labels stay in sync).
- Already-correct "Tap or click" strings were left alone so they did not become "tap or tap or click."
- "Click or tap" was rewritten to **"Tap or click"** (same meaning, requested order).
- Bold in the yellow box is `<strong>Do not write this down</strong>` only. Rest of the sentence stays normal.
- Headless Matrix tests for the changed copy files passed (47 tests). No GUI launch. No Netlify deploy.

## Rejected / corrected (do not rediscover)

- **Do not** change `onClick`, comments, `fireEvent.click`, or "clickable" in code. Student-facing words only.
- **Do not** change Logic homework / gate copy (`Click the ?`, `Click or tap an output`). That is a different app. Chase named Gauss-Jordan.
- **Do not** deploy the portal unless he says deploy / ship live / Netlify in the same message.
- **Do not** launch Macro App, the portal, or a browser to "check" the bold.
- **Do not** add lines to `matrix-solver.tsx` (791, near the 800 cap). The bold is a wrap of existing text. Extract before any real add.
- **Do not** treat "Tab or click" as a keyboard instruction. It was leftover phrasing.

## Current implementation state

**Matrix app (student copy):**
- Tutorial part 1: `src/app/components/matrix-tutorial-overlay.tsx` — indicated cell, Row Scaling button, continue button.
- Tutorial part 3: `src/app/components/matrix-tutorial-overlay-part-3.tsx` — next-pivot cell, wrong-cell follow-up, Row Scaling / Row Replacement, zero cell.
- Yellow row-swap box: `src/app/components/matrix-solver.tsx` ~647 — `<strong>Do not write this down</strong>`.
- Practice: `question-script.ts`, `guided-practice-questions.ts`, `guided-practice-wrong-recovery.ts`, `helpTriggerCopy.ts`, `GuidedPracticeOverlay.tsx` emptyLabel, `GuidedPracticeRowNotationRecovery.tsx` emptyLabels, `fractionHelpTutorialConfigs.ts`.
- Tests updated: `guided-practice-wrong-recovery.test.ts`, `fractionHelpTutorialConfigs.test.ts`. Engine tests already expected "Tap or click" on the first two pivot prompts.
- Catalog regenerated: `scripts/instruction-copy-catalog.json` and `Programs/agent docs/scratch/instruction-copy-catalog.json` via `npm run extract:copy` (446 strings).

**student-portal:**
- `src/features/matrix-tutorial/matrixTutorialActivity.ts` — complete-screen Auto Solve line now "tap or click Auto Solve."
- `src/features/guided-practice/GuidedPracticePageErrorButton.tsx` — "Tap or click if you see an error..."

**Macro App:**
- `renderer/src/utils/matrixReport/matrixSlotCatalog.ts` — remaining "Tab or click" prompts → "Tap or click." Existing test already asserted the first tap-or-click pivot line.

**Verification:** Matrix vitest on the three copy test files, 47 passed. Bold not visually verified after the edit.

## Open questions / constraints

- Chase has not confirmed the bold on the real display after the last edit. If the next message is another screenshot, fix that copy. Do not invent more wording.
- Live students still see "click" until he asks for a Netlify deploy.
- This chat was context-heavy (pull + copy sweep). Do not reopen the full click-search unless he asks for another pass.

## Exact next step

Wait for Chase's next review note on the Gauss-Jordan tutorial (next screenshot or "looks good"). If he wants it live, deploy only after he says so. Do not start a new feature and do not relaunch the tutorial to check the bold.
