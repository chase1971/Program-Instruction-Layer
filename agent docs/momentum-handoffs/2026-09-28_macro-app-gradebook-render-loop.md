# Momentum handoff — Macro App gradebook browser slots

**Written:** 2026-09-28 (day-valid only — if you are reading this on a later date, say so before acting)
**App:** `School Scrips/Macro App`
**Status:** Root cause found and fixed in the working tree. **Not yet verified by Chase in the running app.**

---

## Read first

1. This file.
2. `School Scrips/Macro App/docs/BROWSER_TAB_INTEGRATION.md` § Phase 3.
3. `School Scrips/Macro App/docs/sessions/SESSIONS.md` (top entry) — history only, not current state.

---

## Objective and current phase

On the **Gradebook tab, App Gradebook view** (the grid — *not* the D2L Enter Grades toggle),
clicking a course must load that course's **hidden** Enter Grades browser slot immediately, so
the **Pull** button enables. Two hard requirements:

- It must not require opening the D2L Gradebook view first.
- Pull must **not** enable until the hidden page is genuinely loaded. Chase caught it
  un-greying early: *"it eventually allowed me to click pull, but it shouldn't have because the
  browser hadn't loaded in yet."*

**Phase:** three separate defects were found and fixed this session. The last one was the real
blocker. Everything is green on the automated gates; the remaining step is Chase running the app.

---

## Chase's desired feel and framing

- He suspected a **systemic** regression, not a local bug: *"take a step back and look at the
  entire structure of the browsers and do a deep dive… We did a bunch of cleanup and the browser
  interaction was hit so there has to be something wrong with the overarching process that
  happens."* **That instinct was correct** — the root cause was shell/store plumbing, not the
  gradebook slot code everyone had been staring at.
- Readiness must be **truthful**, not inferred. A slot sitting on the right URL mid-load is not ready.
- **No log floods.** He reported *"infinite lo— infinite errors"* and that was a real feedback loop.

---

## What was wrong (three defects, all fixed)

### 1. Main↔renderer console echo loop — log flood

`main.js` forwarded renderer console warnings/errors into `macro-app.log`, and the log store
broadcast every stored line back to the renderer console, which re-forwarded it with another
`[renderer] ` prefix and another source location appended. Each pass grew the line by ~69 bytes,
so the line-based dedup never matched and the log rotated through all four files.

**Fix:** `electron-app/browser-slot-console-forward.js` exports `RENDERER_FORWARD_PREFIX` and
`shouldForward()` refuses to forward a line already carrying that prefix. `main.js` uses both.
**Confirmed fixed from the log** — one clean line per occurrence, no rotation churn.

### 2. Warmup pool self-deadlock — hidden slot never navigated

`gradebookSlotWarmup.loadOneJob` holds the slot queue via `runSerializedForSlot`, then called
the **serialized** `activateSlot` for that same slot. `runSerializedForSlot` is not re-entrant:
the nested call awaits `state.tail`, which is its own holder's promise. Permanent deadlock.

**Fix:** the pool is wired through **direct IPC** — `activateSlotDirect` and
`navigateInSlotDirect` — in `useGradebookSlotWarmupCoordinator.ts`.
**Confirmed fixed from the log:** `created slot=gradebook:COURSE_1692839` → `navigate request`
→ `navigate … ok url=…/enter/user_list_view.d2l?ou=1692839` in ~3.8s.

### 3. **The real blocker — a permanent React render loop**

After the flood was silenced, the log showed `Maximum update depth exceeded` starting six
seconds after the Enter Grades page loaded and repeating every ~4.8s for the rest of the log,
with **zero further `[BrowserSlot]` activity for three minutes**. Three things formed a cycle:

1. `useEmbeddedBrowser` returned `hide` as an **inline arrow** — new identity every render.
2. An effect in `useMacroAppWorkspaceBrowserEffects` lists `browser.hide` in its deps and calls
   `void browser.hide()` in its body, so it re-ran every render.
3. `hide()` makes main detach and send `browserView:removed` → patches `slotSessionStore`.
   That store had **no equality check anywhere**: `setBrowserEmbedded(state, false)` on an
   already-false flag still built a new object, and `setSlotSessionState` notified **every**
   subscriber unconditionally — including `useEmbeddedBrowser` itself. Shell re-renders, `hide`
   gets a new identity, step 2 fires again.

The effect is gated on `!showBrowserPanel && isGradebookModule` — **exactly the App Gradebook
view, signed in**. That is why it never fired during boot on the Browser tab and only started
once Chase was on the grid.

`hide()` is **not passive**: main's hide detaches every slot and then runs cold-tier eviction.
The app was doing that continuously, which is why the warmup pool never advanced past the first
course and why Pull could un-grey against a slot that had been detached underneath it. This is
the "browser interaction was hit" Chase described.

---

## Accepted decisions (do not relitigate)

1. **The warmup pool and any code already holding a slot's queue use direct IPC**, never the
   serialized `activateSlot`/`navigateInSlot` for that same slot.
2. **Readiness requires live `{ url, isLoading }`.** `useEmbeddedBrowser.getSlotState` is the
   reader; `confirmGradebookSlotEnterGrades(courseCode, url, isLoading)` has **no default** on
   `isLoading` deliberately, so a caller cannot forget to read live state.
3. **Main never re-forwards a line it already forwarded** (prefix guard).
4. **`hide` is a stable `useCallback`** — it closes over nothing.
5. **`slotSessionStore` returns the same state object for a no-op patch**, and
   `setSlotSessionState` skips notifying when handed the state it already holds. This matters
   well beyond this bug: `slotReady` fires for every slot on every load transition, so
   redundant patches were the common case.
6. **`importContextRefs` in `useGradebookD2L` is `useMemo`'d** — it was an object literal
   wrapping two `useRef` calls, so it re-ran two `useGradebookCourseTabActivity` effects on
   every render (one re-registering the module-log IPC listener each time).

---

## Rejected directions — do not rediscover

- **Do not** route a hidden gradebook load through serialized `activateSlot` while the slot
  queue is held. That is the original `orchestrateHiddenGradebookSlot` deadlock.
- **Do not** treat a matching URL as readiness. That is what let Pull un-grey early.
- **The ~4.8s cadence is not a timer.** It is ~50 `browserView:hide` IPC round trips at ~96ms,
  which is React's nested-update limit. Time was lost hunting a 5000ms constant; there isn't one.
- **React 19 attaches no component stack** to this warning. `rendererDiagnostics.ts` already
  preserves stacks when React supplies one (`substituteConsoleFormat`), and it deliberately
  keeps "Maximum update depth exceeded" out of the log store. Nothing to fix there.
- A rename of `readSlotState` → `readEnterGradesSlotState` in `enterGradesSlotService.ts` was
  tried and **reverted**. Leave it alone.
- **Do not widen `reactEffectLoopRisk.test.ts` as part of this work** — see open questions.

---

## Current implementation state

All changes are **uncommitted** in `School Scrips/Macro App`.

**This session's fixes:**
- `electron-app/browser-slot-console-forward.js` + `.test.js` — prefix guard and its test
- `electron-app/main.js` — uses the shared prefix and guard
- `renderer/src/hooks/browser/useEmbeddedBrowser.ts` — `hide` is `useCallback`; also
  `getSlotState`, `activateSlotDirect`, `getSlotUrl` derived from `getSlotState`
- `renderer/src/services/slotSessionStore.ts` + `.test.ts` — no-op patch guards, 2 new tests
- `renderer/src/hooks/gradebook/useGradebookD2L.ts` — `importContextRefs` memoized
- `renderer/src/hooks/gradebook/useGradebookSlotWarmupCoordinator.ts` — direct-IPC wiring
- `renderer/src/services/gradebookSlotWarmup.ts` + `.test.ts` — `getSlotState`-based readiness,
  `isLoading` branch, required `isLoading` arg
- `renderer/src/hooks/browser/useEmbeddedBrowserGradebookNav.ts`,
  `renderer/src/hooks/shell/useMacroAppGradebookBrowserEffects.ts`,
  `useMacroAppShell.ts`, `useGradebookShellIntegration.ts`,
  `useBackgroundGradebookSlotLoader.ts`, `enterGradesSlotService.ts`,
  `gradebookD2LBackupSync.ts` — carried over from the prior session (hidden demand path,
  `describeEnterGradesSlotBlocker`, failed-key guard)

**Verification performed:**
- `npx tsc -p tsconfig.app.json --noEmit` — clean (this is the real gate; plain `npx tsc
  --noEmit` in `renderer/` pulls in test files and my-calendar aliases and reports ~100
  pre-existing errors — ignore it)
- `npx vitest run` in `renderer/` — 1533 pass, 4 skipped
- `npx eslint` on the changed files — clean apart from two warnings that pre-date the change
  (unused `voidBenignIpc`, one `exhaustive-deps` at an untouched `useCallback`)
- `node --test electron-app/browser-slot-console-forward.test.js` — 3 pass (note: the
  directory form `node --test electron-app/` is not how this repo runs it, and `ci:local` does
  not run electron node tests at all)

---

## Open questions and constraints

**Not verified by Chase.** The render-loop fix has only been reasoned from the log plus code;
no run has happened since.

**Standing rules that bind the next agent:**
- **Do not commit or push** unless Chase says `pull`, "put on GitHub", or end-of-session.
- **Never put anything on his screen without asking** — no launching the app, no UI smoke
  tests, no opening a browser. Hand him tests as a **flat statement**, never a question.
- `config/d2l-courses.json` is machine-local. Never commit it, never mention it in a recap.
- Windows PowerShell 5.x — `&&`/`||` are invalid; no `curl`.

**Known remaining hazards (found in the architecture map, not blocking, not yet fixed):**
1. `ensureHiddenD2LSession` still nests `runSerializedForSlot` on the same slot via
   `orchestrateHiddenGradebookSlot` → `activateGradebookCourseSlot`. Same deadlock shape that
   was just fixed in the warmup pool. Live landmine.
2. Cold-tier eviction can destroy a hidden `gradebook:<CODE>` slot **mid-load** with no
   cancellation of the in-flight renderer work — triggered by `setVisibleWorkspaceTabs` when
   the Gradebook tab is unchecked in Manage Tabs.
3. `d2l-email` unexpectedly became the **visible** slot at 22:16:30 during Gradebook use
   (`activate d2l-email — visible=true … visibleSlot=d2l-email`). Never explained. May be
   benign workspace preloading, may be a z-order bug.

**Deliberately deferred:** `reactEffectLoopRisk.test.ts` structurally cannot catch this class
of bug. It only inspects effects whose body contains a literal `setX(`, so `void browser.hide()`
is invisible even though it writes state two hops later through the store; and it treats
anything derived from `useCallback`/`useMemo`/`useRef` as safe, which is how a `useRef` inside
an object literal slipped through. Widening it will surface a batch of unrelated findings and
deserves its own pass — logged as a doc gap, not fixed mid-bug.

---

## Exact next step

**Chase runs the app and reports the log.** The test to hand him (as a statement):
launch the Macro App, sign in to D2L, open the Gradebook tab on the App view, click a course.
Pull should un-grey within a few seconds, and `macro-app.log`
(`C:\Users\chase\AppData\Roaming\macro-app\logs\macro-app.log`) should contain **no**
`Maximum update depth exceeded` lines at all.

Then branch on what he reports:

- **Loop gone, Pull behaves** → the three fixes hold. Offer hazard #1 (the
  `ensureHiddenD2LSession` nested-serialization landmine) as the next piece of work.
- **Loop gone, Pull still un-greys early or never** → the readiness path is now the only
  suspect. Trace `confirmGradebookSlotEnterGrades` and `isGradebookSlotReadyForCourse` against
  `utils/gradebook/gradebookBrowserSyncReady.ts`, which returns `isSelectedCourseSlotReady`
  when `showD2LGradebookView` is false.
- **`Maximum update depth exceeded` still present** → there is a second loop. Read
  `macro-app.log` first. Note that renderer `info` lines never reach that file (main forwards
  only `warning`/`error` console levels), so the gradebook detail timeline is **not** recoverable
  from disk — plan for that before trying to reconstruct it.
