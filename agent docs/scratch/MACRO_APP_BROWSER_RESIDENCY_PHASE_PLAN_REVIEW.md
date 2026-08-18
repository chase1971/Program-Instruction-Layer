# Review: MACRO_APP_BROWSER_RESIDENCY_PHASE_PLAN.md

## Context

Chase asked for a review of the draft plan
(`agent docs/scratch/MACRO_APP_BROWSER_RESIDENCY_PHASE_PLAN.md`) that proposes changing Macro
App's embedded-browser tab lifecycle from "destroy most inactive slots to save RAM" toward
"keep tabs loaded so switching doesn't reset them," with a settings UI so RAM usage stays
user-controllable. This is a review, not an implementation — the output below is a verdict plus
fact-checking against the current code, not new code.

## Verdict: Agree, with two real gaps to close before Phase 0 starts

The plan's architecture is sound and its instincts are the right ones for this codebase:

- Correctly treats cold-tier eviction, the gradebook LRU cap, and Playwright isolation as
  **three separate policies**, not one mechanism to gut — this matches how the code is
  actually split (`browser-slot-cold-tier.js`, `browser-slot-gradebook-lru.js`, `d2l-bridge.js`
  are genuinely independent files with independent purposes).
- Correctly refuses to touch Playwright isolation first. `d2l-bridge.js:209-212` documents a
  real, specific failure mode (D2L Home's cross-origin iframes stall full-browser CDP attach) —
  this isn't a hypothetical risk, it's a known bug the plan is right to fence off.
- Uses the codebase's actual conventions instead of inventing new ones: `createUserDataStore`
  for the new prefs store (ADR-002-compliant), the existing `AppSettingsModal.tsx` section
  pattern for the new UI, and it explicitly defers doc/index updates to the end (matches the
  capture-ladder discipline in root `AGENTS.md`).
- "Recommended First PR Scope" (prefs store + dynamic cap + policy-driven cold-tier + settings
  UI + tests, deferring hidden-tab release / staggered warmup / explicit release / Playwright
  changes) is the right size for a first slice — it answers "do tabs stop resetting" without
  touching the highest-risk area.
- Rollback story is present at every phase and the safety invariants (never destroy the visible
  slot, save auth cookies before destruction, keep `destroySlotsExcept` unchanged) are the
  correct ones — they match what the code already protects.

## Fact-check results (verified against current code, not just the plan's claims)

All verified via three parallel Explore passes over `electron-app/`, `renderer/src/`, and
`docs/`. Everything below is TRUE unless flagged.

| # | Claim | Result |
|---|---|---|
| Cold-tier eviction destroys non-warm slots, Pearson exempt | TRUE — `browser-slot-cold-tier.js:9-10`, hardcoded `Set(['pearson'])` |
| `GRADEBOOK_LIVE_COURSE_CAP = 2`, course-based LRU eviction | TRUE — `browser-slot-gradebook-lru.js:13,75`. Minor precision note: eviction is keyed off `listLiveCourseKeys(slots).length >= 2` via a `touchOrder` recency array, not literally "when a 3rd course needs a slot," but functionally equivalent |
| Playwright isolation (`destroySlotsExcept` + restore) exists for CDP-stall reasons | TRUE — `d2l-bridge.js:214`, restore lives in `browser-slot-isolation-restore.js`, stall rationale in `d2l-bridge.js:209-212` |
| `browser-view-slots.js` / `browser-view.js` split (primitives vs IPC facade) | TRUE |
| `app-memory-ipc.js` reports `gradebookCourseCap` for the memory pill | TRUE — line 44 |
| `userDataStore.js` / `createUserDataStore` is the right persistence primitive | TRUE — ADR-002, 10 existing callers follow this pattern |
| Gradebook LRU test hardcodes cap=2, needs updating | TRUE — `electron-browser-slot-gradebook-lru.test.ts:79` |
| `D2L_TAB_BROWSER_SLOT` mapping confirms which tabs own slots | TRUE — `renderer/src/modules/moduleContracts.ts:102-114` (plan's tab-id spelling is slightly off: `d2l-discussion-grading` / `d2l-email`, not `discussion-grading` / `email`) |
| `WARMUP_MAX_CONCURRENT = 2` | TRUE — `renderer/src/services/gradebookSlotWarmup.ts:17` |
| Hiding a tab in Manage Tabs currently leaves its slot loading (no release exists) | TRUE — confirms the plan's premise for Phase 4; modal's own copy says so (`ManageWorkspaceTabsModal.tsx:50`) |
| `AppSettingsModal.tsx` already has a section-component pattern to follow | TRUE |
| Proposed `useBrowserResidencyPrefs.ts` + `browserResidencyPrefsService.ts` pairing matches existing convention exactly | PARTIAL — no single existing pair matches both halves; it's a reasonable synthesis of two different real precedents (`gradebookFilteringPrefsService.ts` for service naming, `useFirstDayHandoutPrefs.ts` for hook naming), not a fabricated pattern |
| "Pearson exempt because MyLab SPA breaks on recreate" is documented | PARTIAL — true only as a **code comment** (`browser-slot-cold-tier.js:9`); `docs/EMBEDDED_BROWSER_AND_MODALS.md` never states this rationale |
| Doc-update targets (`EMBEDDED_BROWSER_AND_MODALS.md`, `BROWSER_TAB_INTEGRATION.md`) are correctly indexed, not orphaned | TRUE — both are live rows in Macro App `AGENTS.md` |

## Two real gaps — recommend closing these before Phase 0

**1. The plan doesn't reference a prior plan in the exact same area that already shipped a
first slice.** `docs/archive/plans/gradebook-slot-memory-tiering.md` (confirmed by direct read)
describes the hot/warm/cold tier + LRU-cap design and is marked "✅ First slice landed
(2026-06-12) — on-demand warmup, tab unblock, LRU cap 2 in main process." It is the origin of
both `GRADEBOOK_LIVE_COURSE_CAP = 2` and the cold-tier mechanism this new plan proposes to make
configurable. Critically, it also gives the **reason the cap is 2**, which the new plan never
states: a measured RAM table — "16 GB is comfortable for 6 courses with all slots live. 8 GB is
tight unless we cap how many Chromium views stay resident." The new plan's presets (`Keep
loaded`, `Balanced`, `Conserve RAM`) should be defined against that same kind of machine-spec
reasoning (e.g., which preset is safe on Chase's 8 GB machine vs his higher-RAM one) rather than
being freestanding labels. Before Phase 0 starts, read that archived plan and carry its RAM
budget data forward into the new plan's default choices.

**2. `docs/EMBEDDED_BROWSER_AND_MODALS.md` is stale relative to the code it's supposed to
describe.** It currently describes tab switching as "no forced navigation home" with no mention
of cold-tier eviction at all — but `browser-slot-cold-tier.js` demonstrably destroys inactive
slots today. Phase 9 of the plan proposes *adding* residency-policy language to this doc's
"Per-tab browser slots" section, but as written it would be layering new text on top of an
already-inaccurate baseline description. The doc update in Phase 9 needs to also correct the
existing "slots are just kept warm, nothing gets destroyed" framing, not just append the new
policy.

## Minor notes (not blockers)

- Default-promotion gate is implicit: the plan lists a "conservative" default set for early
  testing and a "better" default set "after testing," but doesn't say who signs off on flipping
  the shipped default. Recommend making that explicit: the switch happens only after Chase runs
  the Phase 8 manual test script and confirms it, not automatically once Phase 2 code lands.
- Phase 4's open question ("should gradebook auto-sync still run when Gradebook is hidden?") is
  reasonable to leave open, but flag it as a thing to re-check against any existing periodic/
  background D2L sync job before implementing — that wasn't verified in this review and could
  change the answer.

## If/when this moves to implementation

The plan's own "Recommended First PR Scope" is the right unit to execute first: prefs store +
preload bridge (Phase 1), dynamic gradebook cap (part of Phase 2), policy-driven cold-tier
eviction (part of Phase 2), settings UI with presets/cap (Phase 3), and the associated tests —
explicitly deferring hidden-tab release, expanded warmup, the explicit release button, and any
Playwright isolation changes to later PRs, exactly as the plan already recommends.

No app launch, browser preview, or visible test is proposed here — this review was entirely
code/doc reading. If/when implementation starts, Phase 8's rule stands: no GUI testing without
asking first, and any manual verification gets handed to Chase as a flat "run this, expect this"
statement, not a request for permission to proceed.
