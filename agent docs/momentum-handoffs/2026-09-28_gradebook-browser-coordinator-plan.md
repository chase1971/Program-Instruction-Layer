# Momentum handoff — Macro App gradebook browser coordinator (plan ready, not implemented)

**Written:** 2026-09-28 (day-valid only — if you are reading this on a later date, say so before acting)
**App:** `School Scrips/Macro App`
**Status:** Diagnosis done from Chase's two runs; fix plan written and reviewed. **No code changed
this task.** The previous task's uncommitted fixes are still in the working tree.

---

## Read first

1. This file.
2. **The plan:** `School Scrips/Macro App/docs/plans/gradebook-browser-coordinator-plan-2026-09-28.md`
   (a copy of `C:\Users\chase\.claude\plans\read-agent-docs-momentum-handoffs-latest-tidy-taco.md`).
   Read it in full, **including the "Review comments" section**. That section was added after
   the first draft; it corrects and tightens the plan, and it wins where the two disagree.
   Then read "Second review (Claude)" at the end: 8 more gaps checked against the code. It wins over both.
3. `School Scrips/Macro App/docs/BROWSER_TAB_INTEGRATION.md` § Phase 2–3.
4. `School Scrips/Macro App/docs/plans/MACRO_APP_REMAINING_WORK.md` § Track B. It already
   describes an app-wide browser coordinator; this work is its **first vertical slice**.

---

## Objective and current phase

On the Gradebook tab, **App view** (the grid), clicking a course must load that course's hidden
D2L Enter Grades page within **5 seconds**, and Pull must stay grey until the page is genuinely
loaded.

**Phase:** the plan is ready. The next task implements it, following the plan's "Recommended
implementation order".

---

## What Chase reported (his runs, `%APPDATA%\macro-app\logs\macro-app.log`)

- **Run 1, 23:35 UTC (Teacher Console first, then Gradebook):** the app froze and crashed.
  - `Maximum update depth exceeded` every ~0.4–0.6s, then `main-window unresponsive` ×3.
  - The log shows no IPC traffic, so this is a pure React render loop. It is a different loop
    from the `hide()` loop fixed last session.
- **Run 2, 23:40 UTC (Gradebook first):**
  - Pull un-greyed. The first click did nothing; the second showed *"Connect Enter Grades
    browser slot timed out after 5s"*.
  - Three loaders ran on `gradebook:COURSE_1692839` within one second, each `loadURL`
    aborting the one before (`ERR_ABORTED`, `load aborted`).
  - When Chase opened the D2L view, Enter Grades appeared instantly. The page had loaded in
    the background; nothing confirmed it or used it.

His framing: *"there's something majorly wrong… with how all these browsers are getting loaded
in… pay attention to what was changed about the macro app."* He was right. It is a regression
from commit **`52e7389` (2026-09-26)**, which did two things:

1. It serialized `activateSlot` through `runSerializedForSlot`.
2. It moved `activeSlotId`/`isBrowserEmbedded` into the whole-store `slotSessionStore`.

---

## Chase's desired feel

- *"When I click on a class, I want the browser behind it to load within five seconds."*
- Pull must never un-grey against a page that isn't loaded.
- **New requirement this task:** if the page hasn't loaded after 5s, **fail and show a
  persistent message** on the App view: *"Gradebook cannot connect — D2L Enter Grades did not
  load within 5 seconds (<reason>)"*. Pull and Push stay grey.
  - Purpose: *"so that I know it's failed instantly and I don't have to wait around."*
  - He may later change the failure action (for example, auto-retry), so keep it in one place.
  - It is an error message, not a toast. It stays until the next course click.
- He asked whether a more comprehensive browser coordinator is needed. **Answer given: yes.**
  - A main-process load arbiter owns each slot's loading (one actual load per slot and URL).
  - A thin renderer Gradebook policy (`ensureEnterGradesSlot`) owns the 5s rule and the
    message.
  - It **replaces** the competing loaders: warmup pool navigate, `primeHiddenEnterGradesSlot`,
    the preloader's gradebook job, `orchestrateHiddenGradebookSlot`, and the queue-release
    hacks. It is not added on top of them.
  - Gradebook slots first; other tabs move onto it later.

---

## Root causes (facts, with evidence in the plan)

- **A — Pull deadlock.** `ensureHiddenD2LSession` → `orchestrateHiddenGradebookSlot` holds the
  slot queue, then calls the serialized `activateGradebookCourseSlot` for the same slot. That
  call waits on itself forever.
  - This is last handoff's "hazard #1", and it is live.
  - Commit `f10c185` removed the `try/catch` that used to hide it.
  - It also poisons that slot's queue afterwards.
- **B — Five loaders, no owner.** Main's `activateSlot` re-issues `loadURL` while `getURL()`
  is still `''` mid-navigation.
- **C — `loadURLWithTimeout` misattributes events.** It uses webContents-wide `once`
  listeners, so one navigation's abort rejects another caller's promise.
- **D — `readySlots` is sticky.** `noteGradebookSlotNavigation` never clears a slot, so Pull
  stays on while the page reloads.
- **E — Render loop (run 1). Not yet pinned.** The top suspect is `useEnsureGradebookCourseLoaded`.
  - Teacher Console switches the shared course via `selectCourseTab` without loading it.
  - `selectCourse` gets a new identity every render: `useMacroAppShell` passes inline arrows
    into `useGradebook`, and `browser` is a fresh object every render.
  - The cache path runs `setDataRevision(v+1)` synchronously.
- **F — Amplifiers.** `useEmbeddedBrowser` subscribes to the whole store, and the no-op
  `applyD2LSessionEvent` / `applyBrowserSlotNavProbe` still notify.

---

## Accepted decisions

1. Main-process **generic load arbiter** in a new `electron-app/browser-slot-ensure-url.js`.
   `browser-view-slots.js` is 707 lines, so it gets wiring only.
   - Same slot and same target share one promise.
   - A different target supersedes the old attempt, with generation-safe cleanup.
   - Destroying the slot invalidates the attempt.
   - Main's `activateSlot`/`navigate` consult the arbiter, so nothing can start the abort storm.
2. Renderer **`ensureEnterGradesSlot`** lives in `enterGradesSlotService.ts`, the existing owner.
   - It is thin Gradebook policy on top of the arbiter.
   - Callers share the underlying load but keep **independent deadlines**.
3. **The 5s failure latches.** A load that finishes after the 5s failure must not flip Pull
   on. Use an attempt generation or cancel the load. The error stays until the next click.
4. **Readiness comes from one lifecycle record:** exists, URL matches, not loading, attempt
   not failed, not destroyed. `readySlots` may survive only during migration.
5. **The message reuses `gradebookEmbedLoadError`**, extended to render on the App view
   (today it shows only in the D2L view, `AppMainPanel.tsx:193`). There is no second error
   channel and no success text.
6. **Stabilize identities.** Memoize the `useEmbeddedBrowser` return (or have consumers use
   individual stable methods), and make `useGradebook`'s option callbacks stable.
   - `useMacroAppShell` is at 758/800 lines, so extract a small options hook.
   - `useEnsureGradebookCourseLoaded`: add an attempted-key guard **with a retry rule**. Clear
     the key when the attempt fails, when the course changes, and when Gradebook is left.
7. **Diagnostics are supporting telemetry, not a gate.**
   - Capture a stack when "Maximum update depth exceeded" fires. The renderer is **React
     18.3.1**, not 19; the first draft was wrong about that.
   - Log gradebook-slot load telemetry from main.

---

## Rejected directions — do not rediscover

- Routing any gradebook load through serialized `activateSlot`/`navigateInSlot` while the
  slot queue is held. That is the deadlock.
- Treating a matching URL, or a renderer `withTimeout`, as readiness. The Electron load keeps
  running for up to 45s after a renderer timeout fires.
- Adding a coordinator **alongside** the warmup pool, prime, and preloader. It replaces them.
- The old handoff's rejected items still stand:
  - No 5000ms timer hunt; the ~4.8s cadence is IPC round-trips.
  - Do not re-rename `readSlotState`.
  - Do not widen `reactEffectLoopRisk.test.ts` in this work.

---

## Current implementation state

**This task: no code edits.** It wrote two files:
- the plan: `docs/plans/gradebook-browser-coordinator-plan-2026-09-28.md` (new, untracked);
- this handoff.

**Still uncommitted from the previous task.** Keep these; they are compatible with the plan.
- Console-forward prefix guard: `electron-app/browser-slot-console-forward.js`, `main.js`.
- Stable `hide` and `getSlotState` / `activateSlotDirect`: `useEmbeddedBrowser.ts`.
- `slotSessionStore` no-op guards.
- Memoized `importContextRefs`: `useGradebookD2L.ts`.
- Warmup direct-IPC wiring and `getSlotState`-based readiness: `gradebookSlotWarmup.ts`,
  `useGradebookSlotWarmupCoordinator.ts`.
- `primeHiddenEnterGradesSlot` and the hidden-sync effect rework: `useEmbeddedBrowserGradebookNav.ts`,
  `useMacroAppGradebookBrowserEffects.ts`. **The plan replaces these.**
- `describeEnterGradesSlotBlocker`: `enterGradesSlotService.ts`.
- `config/d2l-courses.json` is machine-local. Never commit it, never mention it.

**Last verified gates** (previous task, before this plan):
- `npx tsc -p tsconfig.app.json --noEmit` clean. Plain `npx tsc --noEmit` in `renderer/` is
  **not** the gate.
- vitest: 1533 pass.
- eslint clean apart from 2 old warnings.

---

## Constraints

- **Never launch the app or open any window.** Hand Chase the test as a **flat statement**
  (the plan's "Chase's run" section), never a question.
- No commit or push unless Chase says `pull`, "put on GitHub", or end-of-session.
- File caps: extract before 700 lines, hard cap 800.
  - `useEmbeddedBrowser.ts`: 689
  - `useMacroAppShell.ts`: 758
  - `useGradebook.ts`: 756
  - `browser-view-slots.js`: 707
- Windows PowerShell 5.x: no `&&`.
- Bump session tracking after each deliverable:
  `node scripts/append-session-scorecard.js --note "…"`.

---

## Exact next step

Follow the plan's **Recommended implementation order**, step 1. Write the arbiter regression
tests first, as a `node --test` file beside the new `electron-app/browser-slot-ensure-url.js`:

1. The same target shares one load.
2. A different target supersedes the old one, and the old cleanup cannot clear the new record.
3. Destroying the slot mid-load cannot report ready.
4. A load that completes after the failure does not count.
5. Callers sharing one load get independent deadlines.

Then implement the arbiter.
