# Momentum handoff: Build mode Phase 4 wired, white playground, Phase 5 next

**Written:** 2026-10-20 (night). Valid for today's continuation only.
**Nothing is committed or pushed.** Repos with Build work: Programs (docs-server route), Macro App, student-portal, canvas-kit, Math App Studio. Commit only on "pull", "put on GitHub", or end of session.

## Objective and phase

Chase is building **Build mode** in the Macro App Teacher Console: the local student portal (`127.0.0.1:5340`, Preview source) in an iframe, with a Studio-style move/resize overlay. The layout file `student-portal/src/features/build-playground/buildLayout.json` is source. Moves/resizes edit it. AI is only needed later to flip `planned` to `implemented`.

Plan: `School Scrips/Macro App/docs/plans/BUILD_MODE_LAYOUT_EDITOR_PLAN.md`.

- Phases 1–3: done (uncommitted kit + protocol).
- Phase 4 overlay: done (uncommitted).
- **Phase 4 Auto (toggle, panel, docs-server write, screen wiring): done, uncommitted.** Chase has opened Build on the real display twice and we fixed the phone-slot / empty-navy / orientation problems. The playground canvas is now **white**. `buildLayout.json` is at **revision 5** with one planned `text-1` that has been moved, so he did interact after the last visual fixes.
- **Phase 5 (AI recipe) is NEXT** unless he reports the phone still looks wrong.
- Phase 6 (formal visible trial, ask before any launch) remains.

## Chase's desired feel

- Head-mounted gyro mouse + dwell click + speech-to-text. Big targets, no hover-only UI, no typing flows. Modals never close on backdrop click. Small label-sized buttons. No ephemeral success feedback. No em dashes.
- Never show anything on his screen without asking. Permission is per run, not per session.
- Build must occupy the **same phone slot** as Preview. Same bezel, same landscape spacer, same orientation state. He said they "don't know each other's orientation" and that was a real bug, not a preference.
- The playground should feel like a **white testing page** he can play on, not a navy/blue dead phone. He asked "can we build an app that it can open" with a white background. That is the existing playground, not a new app.
- He needs to be able to **do something**: Add text box, move it, Refresh under the phone. He asked about Reset; Preview never had Reset under the phone. Panel Reload is enough. Do not add a Reset unless he asks again.

## Accepted decisions

- One shared phone chrome: `TeacherConsolePreviewPhoneChrome.tsx`. Preview embed and Build stage are both children of that bezel. Same CSS vars (`studentPortalPreviewChromeWindow` / `studentPortalPreviewFrameChromeWindow`).
- Keep the 100px landscape spacer. Hiding it was what put Build in a different screen position than Preview.
- Build forces landscape on enter and while `inBuild` is true. Portrait is disabled on the controls bar while Build is on. Leaving Build leaves aspect at landscape (synced).
- Overlay **ghosts draw from the layout file even before the iframe sends a manifest**. `stageLayerStyle` is the manifest stage box, or `{ inset: 0 }` until then. The plan's older "boxes only after the manifest arrives" line is stale.
- Drag still waits for `canEdit` (bridge live). Add text box and nudges work from the panel without the bridge.
- `isBuildPlaygroundAvailable()` is Vite DEV and (`isInstructorDevice()` or `isTeacherConsolePreviewUrl()`). The iframe is a separate webContents; instructor localStorage can be empty on first paint.
- Docs server is the only layout writer: `GET`/`POST /__layout/build/<appId>` in `scripts/serve-programs-docs.js` via `scripts/build-layout-docs-route.js`. Allowlist `build-playground`. Bumps `revision` on every write. Renderer `buildLayoutService.ts` throws if the docs server is down. Never silent.
- After a write, `useTeacherConsoleBuildMode` replaces `layout` with the server file so drafts can clear.
- Bounds sync stays `isPreviewActive && !buildMode`, plus `buildModeRef` so a delayed rAF cannot re-attach the native view.
- Refresh under the phone in Build calls `build.reload`.
- White playground: `#fff` on html/body/shell/stage/iframe fallback. Ghosts stay light blue dashed. Implemented playground text is dark-on-white.
- `teacher-console-workspaces.css` is over cap (1149). `teacher-console.css` is 866. Do not add to either. Portal `App.tsx` is over 700; do not touch it further.

## Rejected / corrected (do not rediscover)

- **Do not give Build its own bezel, holder scale, or `--build` class that hides the spacer.** That made a raw rectangle, extra vertical scroll, and a notch "inside the frame." First visual complaint.
- **Do not treat "build a white testing app" as a new portal tile or desktop app.** The playground is that app. A second implementation is how this tree decays.
- **Do not restore `buildLayout.json` to empty.** It is his live testing file (revision 5, `text-1` moved). Empty-by-design was only the initial proof seed.
- **Do not rewire `useBuildStageScale`.** It is leftover and unused after shared chrome. Preview is 1:1 chrome, not a scaled 932×360 stage.
- Tailwind in Macro: rejected. Handles are plain `ck-editor-` CSS in canvas-kit.
- "Align overlay with iframe using RectPct alone" was wrong. Manifest `stage` box exists because the portal insets for the landscape notch.
- Offscreen Electron (`webPreferences.offscreen: true`) is how hidden pointer tests work. Plain `show:false` coalesces events.

## Current implementation state (all uncommitted)

**Programs:** `scripts/build-layout-docs-route.js` + test, `serve-programs-docs.js` GET/POST `/__layout/build/<appId>`, `agent docs/rules/html-delivery.md` note.

**Macro `renderer/src`:**
- Shared chrome: `components/teacher-console/TeacherConsolePreviewPhoneChrome.tsx` (embed wraps `EmbeddedBrowserPanel` in it; Build wraps `TeacherConsoleBuildStage` in it from `ConsolePreviewWorkspaceScreen.tsx`)
- Stage: `components/teacher-console/build/` (`TeacherConsoleBuildStage`, `BuildStageElementBox`, `BuildStageStatus`, `TeacherConsoleBuildPanel` lazy)
- Hooks: `useBuildBridge`, `useBuildNativeDetach`, `useBuildStageEditing`, `useTeacherConsoleBuildMode` (public API `buildMode` / `buildAvailable`; internals `inBuild` / `canBuild` / `layoutLoadKey` for the effect-loop audit)
- Unused leftover: `useBuildStageScale.ts`
- Service + file utils: `services/buildLayoutService.ts`, `utils/buildMode/*`
- Styles: `teacher-console-build-stage.css`, `teacher-console-build-panel.css`
- Controls: Build button on `TeacherConsolePreviewControlsBar.tsx` (Preview + Admin only)
- Plan: `docs/plans/BUILD_MODE_LAYOUT_EDITOR_PLAN.md` (Phase 4 overlay result + Auto result, including shared chrome row)

**student-portal:** `src/features/build-playground/` (view, bridge, access, CSS, layout JSON, tests). Access test covers TC preview URL. Route `#/build-playground`. Also earlier Phase 2 edits in `App.tsx` and `usePortalRoute.ts`.

**canvas-kit / Math App Studio:** Phase 3–4 handle CSS and Studio re-exports, still uncommitted.

**Verification already done (headless):**
- Macro `tsc -p tsconfig.app.json` clean after shared chrome.
- ESLint clean on the Build wiring (pre-existing `skipGatedTutorials` unused warning on the screen).
- Macro Build-mode tests 51 passed; portal playground 12 passed (was 8, plus 4 access tests).
- `check-file-size.js` pass.
- Docs-server GET/POST was exercised earlier in the Auto chat.

**Not verified on the real display after the last two fixes** (shared chrome + white canvas). Chase has not said "this looks right." He also has not complained again, and the layout file moved, which is evidence he used Add/drag. Formal Phase 6 still needs permission before any agent launch.

## Open questions / constraints

- If the phone still sits wrong or the iframe is still navy, fix the shared-chrome / playground CSS path first. Do not start Phase 5 on top of a dead canvas.
- Student-portal `npx tsc --noEmit` has many unrelated pre-existing errors (logic, transformations, quiz). Ignore those; playground tests are the check.
- Macro depends on sibling `canvas-kit` at `../../canvas-kit`. No CI-standalone fallback.
- Protocol change touched portal and Macro; commit them together when he says so.
- Visible launch still requires asking first, every time.

## Exact next step

Start **Phase 5** from the plan: one recipe in `agent docs/recipes/` plus an INDEX row plus a keyword row in Macro and student-portal `AGENTS.md`, so "put this text box in the app" reads `buildLayout.json`, consumes `planned` rects as real elements, flips `status` to `implemented`, runs headless tests, and hands Chase a flat reload-and-expect statement. Never deploy. Never open a window. If Chase's first message in the fresh task is a visual complaint about Build, fix that instead and leave Phase 5.
