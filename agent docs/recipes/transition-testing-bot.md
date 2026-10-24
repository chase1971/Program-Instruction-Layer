# Transition testing bot: prove a student can never get stuck

> **You might say:** "make sure they can't get stuck" · "does every wrong screen have a way out" ·
> "does the Next button actually work" · "test every path through the problem" · "a bot that plays
> the homework" · "do this for the other app too" · dead end · stuck screen · frame gallery exits
> **What it is:** a test-only bot that plays an app through its real screens in a simulated
> browser, clicks every exit, and checks the student lands where they should. It costs no tokens
> to run (plain test code, about 7 seconds). Tokens are only spent writing it.

**Exemplar (read these first, the code is the truth, this file is the map):**

| Piece | File (all under `School Scrips/student-portal/src/features/frame-gallery/`) |
|---|---|
| Frame catalog (every screen, with stable IDs like `P3.Q4.W2`) | `frameCatalog.ts` |
| Level 0: does each screen have an exit control (also drawn as badges on the gallery) | `frameExits.ts`, `frameExits.test.tsx`, badge in `FrameThumb.tsx` |
| Levels 1 and 2: click the exit, check where the student lands | `frameTransitions.test.tsx` |
| Level 3: a bot that plays a whole problem three ways | `frameBot.tsx`, `frameBot.test.tsx` |

Run it:

```bash
npx vitest run src/features/frame-gallery
```

(from `School Scrips/student-portal`). It fails with the screen ID and what went wrong.

---

## Vocabulary (so you can name it to an agent)

- **Transition testing** (part of **state-machine testing**): each screen is a *state*, each
  button or timer is a *transition*. You test that every transition lands on the right next state.
- **Dead-end detection**: the cheap check that a screen has *an* exit control. It never clicks,
  so a Next button that does nothing still passes. That is why transition tests exist.
- **Playthrough bot**: the end-to-end version. It answers every question, right and wrong,
  and fails if it ever cannot reach the next question.

## The levels (build in this order, each reuses the one before)

| Level | What it checks | Cost |
|---|---|---|
| 0. Exit present | Normal and Wrong 1 have an enabled answer control. Wrong 2 has Next, Continue or Enter. Correct is labeled "Auto-advances". | Smallest. Reads the rendered DOM, never clicks. |
| 1. Exit works | Wrong 2: click Next (repeat if a timed reveal needs a second Next), assert the next question's prompt shows. Correct: answer right, run the timer, assert the next prompt shows. | Small. No typed answers needed. |
| 2. Retry loop | Wrong then right advances. Wrong twice shows the answer with a Next that advances. Wrong screen shows the red text. | Small. Same machinery as 1. |
| 3. Full playthrough | A bot plays every question of a whole problem in three modes: `right`, `retry` (wrong then right), `giveup` (wrong twice, then Next or the recovery quiz). | Biggest. Needs a driver for every input widget. |

## How it works (the mechanism)

1. **Render the real screen** with testing-library in jsdom (`// @vitest-environment jsdom`). No
   window opens, so it respects the "never put anything on Chase's screen" rule.
2. **Never hardcode answers.** The bot reads `question.expected`, the same field the solver
   grades against, from the engine (`buildGuidedPracticeQuestions`). Any generated problem that
   yields a matrix plays the same way. Wrong answers are invented (7 in every cell, the wrong
   operation, a wrong factor in the notation).
3. **Fake timers.** `vi.useFakeTimers()`, then `act(() => vi.advanceTimersByTime(500))` in a loop
   (up to 60 s of fake time) until the next prompt appears. Correct-answer flashes and reveal
   animations are skipped instantly.
4. **"Landed" means the next question's prompt text is on screen** (`page.has(next.prompt)`).
   Exact full-text equality is too strict (portaled help triggers appear later). Assert on the
   prompt text only.
5. **Three modes, one loop.** For each question: optionally answer wrong 0, 1 or 2 times, then
   either answer right or click through to the Next, then wait for the next prompt.
6. **Report, do not throw.** `playProblem` returns `{ played, total, failures, unsupported }`.
   `failures` are real stuck states. `unsupported` are question kinds the bot cannot answer yet,
   so a gap in the bot never looks like a bug in the app.

## Hard-won lessons (each one cost a debugging round, do not rediscover)

- **Match buttons by aria-label first, then text.** The matrix cells show numbers as button text
  ("7"), so matching text alone clicks a cell instead of the keypad key. Keypad keys carry
  `aria-label`; cells do not. Also `Enter` can have `aria-label="Submit row values"`: read
  visible text first when deciding if a button is a forward button.
- **Index matrix cells over all buttons, not only enabled ones.** Disabled cells still occupy
  their slot in the DOM order.
- **After a wrong submit the cells keep their wrong values.** A student taps each cell, clears
  it with backspace, retypes, and submits only on the last cell (committing a cell with nothing
  empty sends the whole answer). The bot finds the cells as the unlabeled buttons still showing
  the wrong value (`retypeCells`). This applies to matrix entry, row entry and solution entry.
- **A keypad "Next" is not an exit.** The solution keypad has its own Next key. Stop clicking
  once the next prompt is on screen, otherwise you click keypad keys by mistake.
- **Reveal screens are timed animations.** A Next can start an animation that needs fake time
  and then a second Next. Loop: click Next, advance timers, check, repeat (cap at about 6).
- **jsdom has no `ResizeObserver`.** Stub it in `beforeAll` (the anchored help triggers need it
  after a question change).
- **Row-notation Wrong 2 has no Next.** It opens a mini tutorial (reciprocal or opposite, which
  row to multiply, which row changes, full notation, then the answer with Next). Drive it from
  the on-screen text, answering wrong at every step so every reveal and Continue runs
  (`playRecovery`). The Enter key is that screen's forward control, not Next.
- **Parametric answers use a pad with `t`, `+`, minus and no `/`.** The bot formats them as
  `3-2t` and reports fractional answers as unsupported rather than failing.
- **Falsify every new test.** Temporarily change the expected text to something impossible and
  confirm it fails. A test that cannot fail proves nothing.

## What it does not prove (say this plainly when reporting)

- **Math correctness.** The bot trusts the engine's `expected`. A wrong answer key passes. That
  needs a separate check (for example plug the solution back into the equations).
- **Correct-answer variants of the recovery quiz** (it answers wrong at every step).
- **The last question's finish screen** (nothing follows it to assert on).
- **Looks.** Layout and overlap are checked by eye in the gallery, not here.

## Applying it to another app (the checklist)

The *method* ports as is. The *driver* is per app, because every app has its own screens.

1. **List the screens** as a catalog with stable IDs (question, correct, wrong 1, wrong 2). If the
   app has no gallery, a list is enough. Seed wrong screens by replaying wrong-answer events
   through the app's own resume path if it has one.
2. **Level 0 first.** Copy `frameExits.ts`. It looks for enabled buttons and a Next, so it needs
   little change. Add the badge to the gallery if there is one.
3. **Find the source of truth for answers.** Where does the app grade from? (`expected`, an
   answer key, a generator.) The bot must read that, never hardcode.
4. **Write a one-page note of each question type**: how it is answered (click, keypad, drag),
   what a wrong answer does to the screen, and what its exits look like. Probe with a throwaway
   test that dumps `container.textContent` and every button's label after each action. This is
   how every lesson above was found, and it is quicker than reading the source.
5. **Build levels 1 and 2** on the simple question types. Then add one question type at a time
   to the bot, running it after each, until `unsupported` is empty.
6. **Keep the three modes and the `{ played, total, failures, unsupported }` result.**
7. **For generated problems** (a generator instead of a fixed list), run the bot over hundreds
   of generated problems per test run. That is where it finds odd cases a hand-picked list never
   would (a zero pivot, an unusual fraction).
8. **Shared core, only if a second app really needs it.** Split the loop, the modes and the
   reporting (shared) from a per-app adapter that says how to answer each question kind. Do not
   build the shared version before a second app exists.

## Rules this recipe obeys

- Headless only, never opens a window (root `AGENTS.md`).
- No new app UI. The only on-screen piece is the exit badge, and it appears in the gallery.
- No em dashes in anything student-facing; none were added.
