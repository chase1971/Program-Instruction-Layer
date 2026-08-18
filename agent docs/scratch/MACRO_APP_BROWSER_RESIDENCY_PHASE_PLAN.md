# Macro App Browser Residency Phase Plan

Status: first implementation slice landed 2026-08-11; later phases remain open
Created: 2026-08-11
Scope: `C:\Users\chase\Documents\Programs\School Scrips\Macro App`

## Goal

Change Macro App from "destroy most inactive embedded browsers to save RAM" toward "keep browser tabs loaded so tab switches preserve state," while adding settings that let the user reduce RAM usage when needed.

The preferred end state:

- Browser-backed tabs stay alive after they have been opened.
- Gradebook course browser slots can stay warm beyond the current two-course cap.
- Browser warmup is staggered, not all-at-once.
- Users can choose a lower-memory policy without a code change.
- Hidden workspace tabs do not keep browser resources alive.
- Existing modal freeze behavior and automation safety are preserved.

## Current Behavior Summary

The current browser lifecycle has three separate mechanisms.

1. Cold-tier workspace eviction
   - Owner: `electron-app/browser-slot-cold-tier.js`
   - Most non-gradebook slots are considered cold-tier and are destroyed when they are no longer visible.
   - Pearson is currently exempt because the MyLab SPA breaks badly on recreate.

2. Gradebook live-course cap
   - Owner: `electron-app/browser-slot-gradebook-lru.js`
   - `GRADEBOOK_LIVE_COURSE_CAP = 2`
   - The cap counts courses, not raw slots. One course may own both `gradebook:{code}` and `manage-grades:{code}`.
   - When a third course needs a slot, the oldest course's gradebook slots are destroyed.

3. Playwright isolation
   - Owner: `electron-app/d2l-bridge.js`
   - Some Playwright commands call `destroySlotsExcept(slotId, { captureRestore: true })`.
   - This is not just a RAM policy. It prevents CDP attach stalls caused by too many Chromium targets.
   - Destroyed slots are restored afterward by `browser-slot-isolation-restore.js`.

The change should treat these as separate policies, not one big removal.

## Guiding Decisions

- Do not remove modal freeze/snapshot behavior. Native `WebContentsView` still paints above React modals.
- Do not disable Playwright isolation in the first implementation. It protects against a known automation timeout path.
- Make the low-RAM behavior available through settings before removing the hard-coded safety.
- Use a single policy owner in Electron main process. Avoid scattering cap checks across renderer hooks.
- Let raising the residency limit apply immediately where safe.
- Do not silently destroy active work when lowering the limit. Lower caps should take effect on restart or through an explicit "release inactive browsers" action.
- Hidden workspace tabs should not warm or remain resident.

## Proposed User Settings

Add a new `Browser residency` section to the app settings modal.

### Presets

`Keep loaded`
- Default target behavior for Chase's main machine.
- Keep browser-backed workspace tabs alive after first open.
- Keep gradebook course slots up to the selected gradebook cap.
- Stagger warmup after sign-in.

`Balanced`
- Keep important/problematic tabs loaded.
- Cap gradebook courses.
- Release lower-value workspace tabs after tab switches.

`Conserve RAM`
- Approximate current behavior.
- Destroy inactive cold-tier workspace tabs.
- Keep a small gradebook cap, default `2`.

### Advanced Controls

`Max live gradebook courses`
- Values: `2`, `4`, `6`, `All`
- Implemented first-slice default: `All`.
- Default for rollback/safety: `2`.

`Warm gradebook courses after sign-in`
- Values:
  - `Selected course only`
  - `Visible courses, staggered`
  - `All courses, staggered`
- Recommended initial default: `Selected course only`, then test `Visible courses`.

`Workspace browser tabs`
- Per-tab keep-loaded toggles for browser-backed tabs:
  - Browser
  - Managing Dates
  - D2L Course
  - Assignment Assistant
  - Discussion Grading
  - Email
  - Makeup Exam
  - Pearson
- Non-browser app tabs should not appear here:
  - Calendar
  - My Calendar
  - My Due Dates
  - First Day Handout
  - Student Progress

`Release inactive browsers now`
- Optional button.
- Applies current policy immediately.
- Should never release the visible slot.
- Should warn via button text/status, not a scary confirmation modal unless destructive active work is possible.

## Phase 0 - Baseline and Guardrails

Purpose: make sure the implementation is measurable and reversible.

Tasks:

- Record current slot behavior from code:
  - `browser-slot-cold-tier.js`
  - `browser-slot-cold-ui.js`
  - `browser-slot-gradebook-lru.js`
  - `browser-view-slots.js`
  - `d2l-bridge.js`
- Confirm which workspace tabs are hidden through Manage tabs.
- Confirm which tabs actually own browser slots through `D2L_TAB_BROWSER_SLOT`.
- Keep Playwright isolation out of the first behavior change.
- Preserve existing memory pill behavior, then extend it later.

Deliverable:

- No app behavior change yet.
- Clear file list and test list before code changes.

Risk:

- Low. This is planning and inspection.

Rollback:

- None needed.

## Phase 1 - Add a Browser Residency Policy Owner

Purpose: introduce one main-process owner for browser lifetime preferences.

New files:

- `electron-app/browser-residency-prefs-io.js`
- `renderer/src/services/browserResidencyPrefsService.ts`
- `renderer/src/hooks/shared/useBrowserResidencyPrefs.ts`
- `renderer/src/types/macroAppBrowserResidency.d.ts` or add compact types to `macroApp.d.ts`

Electron data shape:

```ts
type BrowserResidencyMode = 'keep-loaded' | 'balanced' | 'conserve-ram' | 'custom';

type GradebookCourseCap = number | 'all';

type BrowserResidencyPrefs = {
  mode: BrowserResidencyMode;
  gradebookCourseCap: GradebookCourseCap;
  keepLoadedTabIds: string[];
};
```

Implementation notes:

- Use `createUserDataStore` from `electron-app/shared/userDataStore.js`.
- Store as profile-scoped if the right setting may differ between laptop and desktop.
- Register IPC in `main.js` near the other settings/prefs registration.
- Expose preload bridge as `window.macroApp.browserResidencyPrefs`.
- Normalize unknown values back to safe defaults.
Implemented first-slice default:

- `mode: 'keep-loaded'`
- `gradebookCourseCap: 'all'`
- `keepLoadedTabIds`: every enabled browser-backed workspace tab

Tests:

- Unit test normalization:
  - invalid mode falls back
  - invalid cap falls back
  - unknown tab ids are ignored
  - Pearson remains included by default unless explicitly removed by a valid low-RAM preset

Risk:

- Low to medium. IPC/preload/type plumbing touches several files but does not yet change eviction.

Rollback:

- Remove the new prefs bridge, or leave it unused.

## Phase 2 - Make Eviction Policy-Driven

Purpose: replace hard-coded slot destruction rules with the new policy.

Files to change:

- `electron-app/browser-slot-cold-tier.js`
- `electron-app/browser-slot-cold-ui.js`
- `electron-app/browser-slot-gradebook-lru.js`
- `electron-app/browser-view-slots.js`
- `electron-app/app-memory-ipc.js`
- Existing tests:
  - `renderer/src/__tests__/electron-browser-slot-gradebook-lru.test.ts`
  - Add a new cold-tier policy test if practical.

Cold-tier policy behavior:

- `keep-loaded`:
  - Do not evict workspace browser slots just because the user switched tabs.
  - Still allow explicit release for hidden tabs or "release inactive browsers now."

- `balanced`:
  - Keep configured tabs alive.
  - Default keep list should include Pearson and likely Assignment Assistant.
  - Evict tabs not in the keep list.

- `conserve-ram`:
  - Match the current cold-tier behavior as closely as possible.
  - Pearson may remain exempt unless the user explicitly chooses a strict release option.

Gradebook cap behavior:

- Change `GRADEBOOK_LIVE_COURSE_CAP` from a hard constant to a default plus policy argument.
- Keep a default export for tests and memory display.
- `evictExcessGradebookSlots(...)` should accept a cap option:

```js
evictExcessGradebookSlots(slots, destroySlot, keepSlotIds, {
  incomingSlotId,
  courseCap,
});
```

- `courseCap === 'all'` means do not evict gradebook course slots for cap reasons.
- Existing tests should be updated from "expect cap is 2" to "default cap is 2" and add tests for `4` and `all`.

Memory pill:

- Update `app-memory-ipc.js` so `gradebookCourseCap` reflects the active policy.
- Consider adding `browserResidencyMode` and `inactiveReleaseAvailable`.

Tests:

- Hard cap `2` still evicts oldest course.
- Cap `4` permits four live courses.
- Cap `all` does not evict.
- Keep-list protects visible/active/incoming slots.
- Cold-tier policy in `keep-loaded` destroys nothing on tab switch.
- Cold-tier policy in `conserve-ram` matches current behavior.

Risk:

- Medium. This is the behavior-changing phase.
- Main risk is accidentally preserving slots that automation isolation expects to remove. Avoid by leaving `destroySlotsExcept` unchanged.

Rollback:

- Set policy to `conserve-ram` and gradebook cap `2`.
- If needed, revert Phase 2 files only; prefs UI can remain harmless.

## Phase 3 - Add Settings UI Safety Valve

Purpose: give Chase and future users control over browser RAM behavior.

Files to change:

- `renderer/src/components/AppSettingsModal.tsx`
- New: `renderer/src/components/BrowserResidencySection.tsx`
- New: `renderer/src/hooks/shared/useBrowserResidencyPrefs.ts`
- New: `renderer/src/services/browserResidencyPrefsService.ts`
- Preload/types from Phase 1.
- Possibly `renderer/src/styles/shell-tabs.css`, unless the section can reuse existing settings classes.

UI behavior:

- Add a `Browser residency` section.
- Use a segmented or radio-style control for the preset.
- Use a select/segmented control for `Max live gradebook courses`.
- Use checkboxes/toggles for per-tab keep-loaded options.
- Add a small status line:
  - "New tabs use this immediately."
  - "Lower limits release inactive browsers after restart or when you press Release inactive browsers now."
- Do not add hover-only controls.
- Do not require typing.

Apply behavior:

- Saving settings should update Electron prefs immediately.
- Raising limits applies immediately for future slot activations.
- Lowering limits should not instantly destroy active browser work.
- Optional explicit button can call `browserView:releaseInactiveSlots` later.

Tests:

- Hook loads defaults.
- Saving a preset updates prefs.
- Invalid preload bridge absence fails gracefully with a status message.

Risk:

- Low to medium. UI and IPC typing surface.

Rollback:

- Hide the settings section.
- Keep the default policy at `conserve-ram`.

## Phase 4 - Make Manage Tabs Release Browser Resources

Purpose: when a tab is hidden in Manage tabs, it should not keep loading in the background.

Current issue:

- `ManageWorkspaceTabsModal.tsx` says hidden tabs still load in the background.
- Chase wants the opposite for hidden/unused tabs.

Files to change:

- `renderer/src/components/shell/ManageWorkspaceTabsModal.tsx`
- `renderer/src/hooks/shell/useManageWorkspaceTabsModal.ts`
- `renderer/src/hooks/shell/useWorkspaceTabLayout.ts`
- `renderer/src/hooks/shell/useMacroAppShellWorkspaceTabGuard.ts`
- `renderer/src/hooks/gradebook/useGradebookSlotWarmupCoordinator.ts`
- `renderer/src/hooks/gradebook/useBackgroundGradebookSlotLoader.ts`
- Electron IPC in `browser-view.js` / `browser-view-slots.js` if adding release commands.

Needed main-process helper:

```js
releaseSlotsForHiddenTabs(hiddenTabIds, options)
```

Slot release mapping:

- `browser` -> `browser` should probably never be hidden.
- `d2l` -> `d2l`
- `d2l-course` -> `d2l-course`
- `d2l-assignment-assistant` -> `d2l-assignment-assistant`
- `d2l-discussion-grading` -> `d2l-discussion-grading`
- `d2l-email` -> `d2l-email`
- `makeup-exam` -> `makeup-exam`
- `pearson` -> `pearson`
- `gradebook` hidden -> release `gradebook:*` slots if no background gradebook behavior is allowed.
- `manage-grades` hidden -> release `manage-grades:*` slots.

Important policy question:

- If Gradebook is hidden, should auto-sync/push still run in the background?
- Recommendation: hidden Gradebook means no gradebook browser warmup. App-file gradebook data can still exist, but browser-backed D2L sync should not run automatically.

Renderer changes:

- Pass visible tab ids into warmup coordinator.
- Do not queue warmup for hidden Gradebook/Manage Grades tabs.
- On save from Manage tabs, if a browser-backed tab became hidden, call main-process release helper.
- Update modal copy to:
  - "Hidden tabs are removed from the header and their inactive browser pages can be released to save RAM."

Tests:

- Hiding Manage Grades releases `manage-grades:*`.
- Hiding Gradebook stops startup warmup.
- Browser tab cannot be hidden.
- Active hidden tab guard moves the user back to Browser before release.

Risk:

- Medium. Hidden tab behavior intersects with gradebook background sync.

Rollback:

- Keep Manage tabs as display-only by disabling the release call.

## Phase 5 - Add Staggered Warmup for Keep-Loaded Mode

Purpose: get the "tabs are ready when I click them" benefit without loading everything at once.

Files to change:

- `renderer/src/services/gradebookSlotWarmup.ts`
- `renderer/src/hooks/gradebook/useBackgroundGradebookSlotLoader.ts`
- `renderer/src/hooks/gradebook/useGradebookSlotWarmupCoordinator.ts`
- `renderer/src/hooks/shell/useMacroAppWorkspaceBrowserEffects.ts`
- Possibly new `renderer/src/services/workspaceSlotWarmup.ts`

Gradebook warmup:

- Existing `WARMUP_MAX_CONCURRENT = 2` is a good starting point.
- Change `startupCourseCodes` based on policy:
  - `selected-only`: selected course only.
  - `visible-courses`: all visible courses in the gradebook course tab list, if such a subset exists.
  - `all-courses`: every configured course.
- If `gradebookCourseCap` is smaller than the startup warmup list, either:
  - only queue up to the cap, or
  - allow warmup but cap will evict old courses. This wastes work, so prefer queue up to cap unless cap is `all`.

Workspace tab warmup:

- Only warm tabs that:
  - are visible in Manage tabs,
  - are allowed by residency policy,
  - have a safe bootstrap URL,
  - and will not cause sign-in redirects or intrusive auth loops.

Suggested first warmup list after D2L sign-in:

- `browser` at D2L home
- `d2l-course` at D2L home
- `d2l` only when selected course has a Manage Dates URL
- `d2l-assignment-assistant` as attach-only or workflow-controlled, not forced navigation
- `d2l-email` only if the user has enabled keep-loaded for Email
- `pearson` only after Pearson auth/session is available or user opens it

Avoid at first:

- Aggressively opening Outlook.
- Aggressively opening Pearson assignment manager.
- Aggressively opening every course-specific Manage Grades page.

Tests:

- Queue respects policy.
- Queue respects hidden tabs.
- Queue respects cap.
- Queue remains concurrency-limited.

Risk:

- Medium. Warmup can accidentally fight user navigation if not serialized.

Rollback:

- Set warmup mode to `selected-only`.
- Keep slot preservation without aggressive preloading.

## Phase 6 - Keep Playwright Isolation, Then Revisit

Purpose: avoid reintroducing known CDP attach timeouts.

Do not change first:

- `PLAYWRIGHT_ISOLATION_COMMANDS`
- `destroySlotsExcept(slotId, { captureRestore: true })`
- `restoreSlotsAfterPlaywrightIsolation()`

Why:

- This path is about automation reliability, not just RAM.
- The comments say D2L Home cross-origin iframes in other slots caused Playwright `connect_over_cdp` stalls.

Later experiment:

- Add a developer-only policy flag:
  - `playwrightIsolation: 'always' | 'restore' | 'off-experimental'`
- Test whether Python automation can consistently attach by target ID without full-browser enumeration.
- If raw CDP replacements exist for more commands, reduce isolation command list.

Tests before disabling:

- Bulk scan uncategorized.
- Bulk set category.
- Reorder scan.
- Reorder fix categories.
- Reorder fix category sequence.
- Run with many live tabs and multiple gradebook course slots.

Risk:

- High if disabled too early.

Rollback:

- Keep current isolation behavior.

## Phase 7 - Add Explicit Release and Recovery Tools

Purpose: make low-RAM recovery easy without requiring restart.

Potential IPC:

```js
browserView:releaseInactiveSlots
browserView:releaseSlotsForTabs
browserView:getResidencyState
```

Rules:

- Never destroy visible slot.
- Never destroy active modal-suppressed pending slot.
- Never destroy a slot with known running automation.
- Save auth cookies before destruction, as `destroySlot` already does.
- Notify renderer through existing `browserView:slotDestroyed`.

UI:

- Settings button: `Release inactive browsers now`.
- Status text:
  - "Released 4 inactive browser pages."
  - "Nothing to release."
  - "Skipped active automation slot."

Memory pill:

- Keep current RAM display.
- Add active policy to tooltip, not necessarily visible text.

Tests:

- Releasing inactive slots skips visible slot.
- Releasing hidden tabs clears gradebook warmup ready state through existing `slotDestroyed`.
- Release result reports destroyed slot ids.

Risk:

- Medium. Explicit release is destructive to unsaved browser-page state, so active/visible slot protection matters.

Rollback:

- Remove the button, keep restart-based policy application.

## Phase 8 - Verification Plan

Headless checks:

- `npm run lint` for renderer/electron if available.
- Targeted unit tests:
  - gradebook LRU policy tests
  - cold-tier policy tests
  - prefs normalization tests
  - warmup queue tests
  - settings hook/service tests
- `npm run ci:local` before final push, if Chase asks for full verification.

No unapproved GUI testing:

- Do not launch Macro App or browser windows without asking first.
- If visible testing is needed, ask Chase first and describe what appears and how it closes.

Manual test script for Chase:

1. Open Macro App.
2. Sign in on Browser.
3. Set Browser residency to `Keep loaded`.
4. Visit Assignment Assistant, Managing Dates, Course, Email/Pearson as desired.
5. Switch away and back.
6. Confirm pages do not reset.
7. Open two or more gradebook courses.
8. Confirm the RAM pill shows more live slots/courses.
9. Change setting to `Conserve RAM`, restart or press release button.
10. Confirm inactive tabs reload again, matching old behavior.

Specific bug checks:

- Assignment Assistant modal opens over browser without pop/regression.
- Gradebook sync does not time out because the target slot is still blank.
- D2L sign-in redirect still goes to Browser tab.
- Pearson does not blank after tab switch.
- Makeup Exam form remains stable when its tab is active.
- Bulk edit/reorder automations still restore browser slots after Playwright isolation.

## Phase 9 - Documentation Updates

App docs to update:

- `docs/EMBEDDED_BROWSER_AND_MODALS.md`
  - Update "Per-tab browser slots" section with policy.
  - Mention hidden tabs release slots.
  - Mention Playwright isolation remains separate.

- `docs/BROWSER_TAB_INTEGRATION.md`
  - Update warmup and readiness section.
  - Explain staggered warmup policy.

- `School Scrips/Macro App/AGENTS.md`
  - Add a keyword row only if Chase is likely to ask for "browser residency", "tabs reload", "RAM cap", or "keep browsers loaded" later.

Do not:

- Add root always-on rules for this.
- Add `.cursor/rules/*.mdc`.

## Expected File Touch List

Likely Electron files: `browser-residency-prefs-io.js`, `browser-slot-cold-tier.js`, `browser-slot-cold-ui.js`, `browser-slot-gradebook-lru.js`, `browser-view-slots.js`, `browser-view.js`, `preload.js`, `main.js`, and `app-memory-ipc.js`.

Likely renderer files: `AppSettingsModal.tsx`, new `BrowserResidencySection.tsx`, `ManageWorkspaceTabsModal.tsx`, `useBrowserResidencyPrefs.ts`, `browserResidencyPrefsService.ts`, workspace tab layout hooks, workspace browser effects, gradebook warmup hooks, `gradebookSlotWarmup.ts`, and preload typings.

Likely tests: gradebook LRU tests, cold-tier policy tests, `gradebookSlotWarmup.test.ts`, prefs normalization tests, and renderer service/hook tests.

Likely docs: `docs/EMBEDDED_BROWSER_AND_MODALS.md`, `docs/BROWSER_TAB_INTEGRATION.md`, and maybe the Macro App `AGENTS.md` keyword table if "browser residency" becomes a recurring phrase.

## Suggested Implementation Order

1. Add prefs storage and IPC with tests.
2. Make gradebook cap dynamic with tests.
3. Make cold-tier eviction policy-driven with tests.
4. Add settings UI.
5. Add hidden-tab release behavior.
6. Add staggered warmup expansion.
7. Add explicit release button/state.
8. Update docs.
9. Run targeted tests.
10. Ask Chase before any visible app test.

## Complexity Estimate

Basic experiment:

- Keep workspace slots loaded and raise gradebook cap.
- Difficulty: low to medium.
- Touches roughly 4 to 6 implementation files plus tests.
- Revert path: restore hard cap and cold-tier behavior, or set policy to `conserve-ram`.

Full configurable version:

- Settings, policy store, dynamic cap, per-tab release, hidden-tab behavior, staggered warmup.
- Difficulty: medium.
- Touches roughly 12 to 18 files.
- Revert path: policy default `conserve-ram`, cap `2`, warmup `selected-only`.

Highest-risk area:

- Automation commands that use Playwright isolation.
- Recommendation: leave isolation unchanged until after the browser residency change has been tested.

## Recommended First PR Scope

The safest first PR should not try to solve every RAM preference at once.

Include:

- Browser residency prefs store and preload bridge.
- Dynamic gradebook course cap.
- Policy-driven cold-tier eviction.
- Staggered workspace tab preloading for kept-loaded tabs.
- Settings UI with presets and cap.
- Tests for cap, cold-tier behavior, and preload job planning.

Defer:

- Hidden-tab release.
- Expanded all-course gradebook warmup.
- Explicit release button.
- Playwright isolation changes.

That first PR lets Chase test the main experience quickly: "Do tabs stop resetting when I switch around?" Then the safety valve can get richer in the next pass.
