# Momentum handoff: frame gallery stuck-screen tests done, overlap checker is next

**Written:** 2026-10-24
**Slot note:** this overwrote `latest.md`, which held the 2026-10-23 "11.2 three-var / practice retries"
handoff. That one is still saved as `2026-10-23_11-2-homework-three-var-retries.md`.

## Objective and current phase

Chase reviews the 11.2 homework screens in the **frame gallery** (student portal, `#/frame-gallery`,
Teacher Console preview). He wants to be sure no student can land on a screen they cannot leave, and
now wants the gallery to **flag elements that overlap each other**.

Phase: stuck-screen testing is **finished and green**. The overlap checker is **not started**
(only discussed and approved in principle).

## Chase's desired feel

- He reviews by eye and decides himself. He wants a **flag**, not an auto-fix and not a hard failure:
  "I could always look at them and then decide if that's okay or not. That's how I do it."
- **Rule he asked to record: any element that overlaps any other element should be flagged, at least
  in this app, and it is probably a good default rule everywhere.** No allow-list that hides things;
  he decides which flags are fine. (My earlier idea of an allow-list for legitimate overlaps, such as a
  number inside its own cell, conflicts with this. Do not silently suppress. If noise is a problem,
  group or label flags, or let him mark one as "ok" himself, but ask first.)
- The green check mark in particular should not overlap anything.
- Head-mouse and dwell: no keyboard-driven steps, small buttons, no ephemeral toasts, never open a
  window or browser without asking (root `AGENTS.md`). He verifies visually; state what to open and
  what to see, never "want me to...".
- No em dashes anywhere.

## Accepted decisions

| Area | Decision |
|---|---|
| Naming | "Transition testing" (state-machine testing). Recipe: `agent docs/recipes/transition-testing-bot.md`, indexed in `recipes/INDEX.md` and student-portal `AGENTS.md`. |
| Bot cost | Plain test code, no tokens to run (about 7 s). Per-app driver; the method ports. |
| Exit badges | Every gallery thumbnail shows `Exit: ...` or red `STUCK: no way out`; header shows a count. |
| Overlap flag rule | Flag **every** element-vs-element overlap (Chase, this chat). |

## Rejected directions (do not rediscover)

- **Overlap detection in jsdom**: jsdom has no layout, so bounding boxes are all zero. It needs a real
  browser engine.
- **Allow-listing legitimate overlaps up front**: conflicts with Chase's "flag everything, I decide".
- **Matching keypad keys by button text**: matrix cells show numbers as button text and get clicked by
  mistake. Match `aria-label` first (see the recipe's lessons).
- **Treating the solution keypad's own "Next" as an exit**: stop once the next prompt is on screen.

## Current implementation state

**student-portal** (`School Scrips/student-portal`, uncommitted new files; check `git status`):
- `src/features/frame-gallery/frameExits.ts` + `frameExits.test.tsx`: level 0, exit present.
- `frameTransitions.test.tsx`: levels 1 and 2, click the exit and assert the next question lands.
- `frameBot.tsx` + `frameBot.test.tsx`: level 3 playthrough bot, modes `right`, `retry`, `giveup`.
  Drives matrix entry, row entry, solution entry, parametric entry (`3-2t` style), solution type,
  pick-cell, operation type, row notation, and the row-notation recovery quiz (all-wrong run).
- `FrameThumb.tsx` (exit badge) and `FrameGalleryView.tsx` (stuck count in header) edited.
- `src/types/matrix-app.d.ts`: added `formatRowOpNotation` and `RowOp` to the question-script shim.
- Run: `npx vitest run src/features/frame-gallery` (from `student-portal`).

**Docs:** `agent docs/recipes/transition-testing-bot.md` (new), `recipes/INDEX.md` and
`student-portal/AGENTS.md` (one row each).

**Verification:** all 35 frame-gallery tests pass (~7.5 s). `tsc` shows no errors in the touched files.
Every new test was falsified (changed the expectation, confirmed failure). Nothing viewed on screen.
Not committed or pushed. Not deployed.

**Known gaps in the stuck-screen tests:** math correctness (bot trusts the engine's `expected`),
correct-answer variant of the recovery quiz, finish screen after the last question, fractional
parametric answers (pad has no `/`), the 3-var homework flow (not in the gallery).

## Open questions and constraints

- **Browser engine for overlap detection**: none is installed (`package.json` has no Playwright or
  Puppeteer). Proposal, not yet approved: add Playwright (dev dependency) with headless Chromium so no
  window appears. Confirm with Chase before adding a dependency or launching anything visible.
- How should flags be shown? Proposal: a red `OVERLAP` badge next to the `Exit` badge on each
  thumbnail, plus a header list, naming the two elements. Not yet approved.
- What counts as an element? Proposal: buttons, text boxes, prompt, matrix, keypad, check mark, help
  triggers, reveal blocks. Define it by probing real frames first.
- Layouts moved in the layout editor are saved (`gp-correct-check-offsets` JSON via
  `127.0.0.1:8765`); the checker must measure the saved positions.
- Files over cap? `frameBot.tsx` is about 330 lines; fine. `GuidedPracticeSolver.tsx` is about 752 in
  Matrix (extract before adding).
- Context was very large at handoff (about 260k per reply). Start fresh.

## Exact next step

Read `agent docs/recipes/transition-testing-bot.md` for the pattern, then probe a few frames in a
**headless** browser to learn the element list and how many natural overlaps there are. Ask Chase one
question: OK to add Playwright as a dev dependency? Then build a measurement test that loads each
gallery frame, lists every pair of intersecting element boxes (all of them, per Chase's rule), and
surfaces them as an `OVERLAP` badge in the gallery. Hand him the visual check as a statement: open the
frame gallery and look at the red badges.
