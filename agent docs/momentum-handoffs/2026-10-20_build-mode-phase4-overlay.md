# Momentum handoff: Build mode, Phase 4 overlay done, Auto chat next

**Written:** 2026-10-20 (evening). Valid for today's continuation only.
**Nothing is committed or pushed in any repo** (Programs, canvas-kit, Math App Studio, Solving Quadratics, Macro App, student-portal). Commit only on "pull", "put on GitHub", or end of session.

## Objective and phase

Chase is building a **Build mode** for the Macro App Teacher Console: the real local student portal (`127.0.0.1:5340`, Preview source) in an iframe with a Studio-style move/resize overlay. The layout file (`student-portal/src/features/build-playground/buildLayout.json`) is source code the portal reads; moves and resizes edit it directly, AI is only needed to flip `planned` to `implemented`.

Plan: `School Scrips/Macro App/docs/plans/BUILD_MODE_LAYOUT_EDITOR_PLAN.md` (the "Phase 4 overlay result" section is the authoritative state).

- Phases 1, 2, 3: done.
- **Phase 4 overlay (Frontier chat): done.** This handoff.
- **Phase 4 Auto chat: NEXT.** Build toggle, Build panel, nudges, docs-server write route + renderer service.
- Phase 5 (AI recipe) and Phase 6 (visible trial, ask permission first, then stop and record Chase's judgment) remain.

Chase cannot see anything in the app yet. He asked "how am I supposed to look at this"; the answer is: not until the Auto chat wires the toggle. Visible trial is Phase 6 and needs his permission each run.

## Chase's desired feel and working constraints

- Head-mounted gyro mouse + dwell click + speech-to-text. Big targets, no hover-only UI, no typing flows. Modals never close on backdrop click. Small label-sized buttons. No ephemeral success feedback (errors and loading are fine). No em dashes anywhere.
- Never show anything on his screen without asking. All verification so far was hidden/offscreen Electron. Offscreen mode (`webPreferences.offscreen: true`) is the way to drive synthetic input; plain `show:false` coalesces/delays pointer events and breaks dwell timing.
- He chose **no Tailwind in Macro**: "let's just do it the way you suggest." Plain `ck-editor-` CSS.
- Model switching is manual per chat: Phase 4 Auto chat can be an Auto model.

## Accepted decisions

- Handles are plain CSS (`canvas-kit/src/editor/handles.css`), shared with Studio. Pixel-identical to old Tailwind (0 differing pixels, Studio-like and no-reset pages).
- canvas-kit is wired into Macro via vite alias `@canvas-kit`, tsconfig paths in `tsconfig.json` and `tsconfig.app.json` (also maps `react` and `react/jsx-runtime` to Macro's `@types/react`, because canvas-kit's own react copy has no types).
- Ghost vs live comes from the **manifest**, not file status. Rects always come from the file (or the in-progress draft), never the measured rect, so a ghost turning real never moves its handles (key unit test exists).
- Both ghosts and live elements get handles when selected (placing a planned ghost is part of the workflow). Only the selected element shows handles.
- Boxes are drawn only after the manifest arrives, on the app's **stage box** (see below). Editing needs `live` phase. 20 s timeout gives a persistent error with Reload.
- Saved drafts clear (and the portal override is cleared with `rect: null`) only when the file holds that rect and the manifest revision >= layout revision. Failed save keeps the draft and shows Retry.
- Build only works on Preview (local) source; the stage shows a persistent error on Live and never frames production.

## Rejected / corrected (do not rediscover)

- **"Overlay aligns with iframe using RectPct alone" was WRONG.** The portal shell insets its stage in landscape (about 47 px notch space on the left; stage about 812 wide in a 932 viewport). Fix: manifest carries `stage: {left, top, width, height}` (protocol addition in portal `buildBridgeProtocol.ts`, `useBuildPlaygroundBridge.ts`, tests updated; Macro parser defaults to full viewport if missing). Plan text corrected.
- Tailwind in Macro: rejected.
- Studio's `@source` for canvas-kit in `tailwind.css` is one folder too short (`../../../canvas-kit` resolves to `Math App Studio/canvas-kit`). Plain CSS made it moot; left alone, not fixed.

## Current implementation state (all uncommitted)

Macro `renderer/src`:
- `components/teacher-console/build/`: `TeacherConsoleBuildStage.tsx`, `BuildStageElementBox.tsx`, `BuildStageStatus.tsx`
- `hooks/teacher-console/`: `useBuildNativeDetach.ts`, `useBuildBridge.ts`, `useBuildStageEditing.ts`, `useBuildStageScale.ts`
- `utils/buildMode/`: `buildLayoutTypes.ts`, `buildBridgeProtocol.ts`, `buildBridgeState.ts`, `buildStageModel.ts` + 3 test files (40 tests)
- `styles/teacher-console-build-stage.css`
- Config: `renderer/vite.config.ts`, `renderer/tsconfig.json`, `renderer/tsconfig.app.json`
- Plan doc updated.

Other repos: `canvas-kit/src/editor/` (handles.css, editorHandles.tsx, useDwellRectEdit.ts type tweaks for `exactOptionalPropertyTypes`, README/AGENTS), Math App Studio (re-exports, tests, recipe notes), `student-portal/src/features/build-playground/` (protocol + manifest stage box), root `usePortalRoute.ts` and `App.tsx` edits from Phase 2.

Verification done: Macro `tsc -p tsconfig.app.json` clean, eslint clean on new files, full vitest 316 files pass, `check-file-size.js` pass; Studio 113 tests/lint/build; Solving Quadratics build with no editor code in bundle; student-portal build-playground 8 tests. Live headless run against the real portal from a `file://` parent: handshake, manifest, origin/source checks, inert iframe, mouse-grab move exact, dwell resize exact, real element follows via `build-preview-rect`.

Not verified: real display dwell feel, scaling when holder narrower than 932, real native-view detach (stub `hide` used).

Portal `buildLayout.json` is restored to its empty original (revision 0, elements []). No dev server running.

## The seam the Auto chat must use

`TeacherConsoleBuildStage` props: `appId`, `previewIdentity`, `browser` (needs `hide`), `layout: BuildStageLayout | null`, `layoutError: string | null`, `selectedId`, `onSelect`, `onRectCommit(id, rect): Promise<void>` (must reject on failure), `reloadNonce`. It does no layout I/O.

To turn Build on, `ConsolePreviewWorkspaceScreen.tsx` renders the stage **instead of** `TeacherConsolePortalPreviewEmbed` (the embed's unmount hides the native view; the stage also hides and waits a paint before mounting the iframe). Requirements:
1. Pass `isPreviewActive && !buildMode` into the screen's `syncPreviewBrowserBounds` guard so bounds sync cannot re-attach the native view over the iframe.
2. Build toggle only in Preview mode and Admin persona (`TeacherConsolePreviewControlsBar.tsx`); Build stays landscape.
3. Swap `PreviewTesterPanelTray` for the Build panel (lazy-loaded, new files): Add text box, selected readout, compact x/y/w/h nudges, Reload (bump `reloadNonce`), persistent error area.
4. Docs-server Build route: extend `scripts/serve-programs-docs.js` (it already owns `/__layout/factoring-guided-portal`); do not add a second write mechanism. Renderer service, never inline `fetch()`. Must not fail silently (unlike `factoringLayoutAgentSync.ts`). Bump `revision` on every write. After a write, the service must update the `layout` prop (new rect + revision) so drafts can clear.
5. Screen file is 266 lines; keep it orchestrating only.

## Open questions / constraints

- Student-portal `App.tsx` is over 700 lines (extract threshold); not touched further.
- Macro now depends on the sibling `canvas-kit` repo existing at `../../canvas-kit` (same relationship Studio has). No CI-standalone fallback was added; mention if CI for Macro alone matters.
- Protocol change touched portal and Macro; both repos need committing together when Chase says so.

## Exact next step

Start the Phase 4 Auto chat: read the plan's "Phase 4 overlay result" section, then build the docs-server Build route + renderer service first (it defines `onRectCommit` and the layout loader), then the Build toggle and panel in `TeacherConsolePreviewControlsBar.tsx` / `ConsolePreviewWorkspaceScreen.tsx`. Verify headlessly (unit tests for the service; reuse the offscreen Electron harness approach if needed). Never open a window for Chase without asking.
