# Momentum handoff: frame gallery + layout editor (11.2 homework)

**Written:** 2026-10-23
**Slot note:** `latest.md` still holds a live, different handoff from today (11.2 three-var / RREF /
Pearson retries). It was NOT overwritten. To resume this topic, say
"read the momentum handoff agent docs/momentum-handoffs/2026-10-23_frame-gallery-layout-editor.md".

## Objective and current phase

Chase wants to stop triggering events by hand to see what each screen looks like. Two linked tools
for the 11.2 Gauss-Jordan homework (student portal, Matrix embed):

1. **Frame gallery**: a dev/instructor page that lays out every student-interactive frame of a
   problem as thumbnails (normal gray, correct green, wrong red), each with a stable ID
   (`P3.Q4.OK`, `P3.Q4.W1`, `P3.Q4.W2`), click for full size with Back/Next to cycle.
2. **Layout editor** (inside layout preview): move and resize text boxes visually, Save locks the
   layout per step, Undo reverts to last saved.

Phase: gallery done and working. Layout editor works for **prompt boxes only** (the blue
instruction box). Chase just said it "feels good" and asked to **apply it to all the other text
boxes**. That is the next job; the handoff was requested instead of starting it.

## Chase's desired feel

- Head-mouse + dwell + presenter mouse. Big, always-visible controls; no hover-only paths.
- "I want to see it, grab it, move it, hit save, and if I mess up, undo." Buttons are named
  **Show layout / Save / Undo** (his words), reachable from the real problem banner and from the
  gallery without a separate "Enter" step.
- A drag must behave like a drag box: grab, move, release. It must never keep growing, and the
  handles must never be lost after dragging out.
- He wants to enter a frame **at that exact point** to interact with it (play the animation,
  check the exclamation point overlap), not on a randomly picked problem.
- No em dashes anywhere. Small buttons. No ephemeral success toasts. Never open a window or
  browser without asking (see root AGENTS.md). He verifies visually himself; do not ask him
  "want me to...", state what to open and what to see.

## Accepted decisions

| Area | Decision |
|---|---|
| Frame source | Frames come from the real `PracticeQuestion` list. Wrong frames are seeded by replaying fake wrong-answer events through the solver's existing resume path (`initialSessionEvents`), so no hook change was needed for them. Catalog: `student-portal/src/features/frame-gallery/frameCatalog.ts`. |
| Problems shown | Fixed, not random: first 3 regular problems + first infinite-solution problem. |
| Route and gate | `#/frame-gallery`, same instructor/DEV gate as Build (`isBuildPlaygroundAvailable`). Menu entry: "Frame gallery / Open" under the 11.2 Homework Start/Resume card. |
| Green frames | Use the solver's existing `correctCheckPreviewMode` (+ admin cheats), so the check sits where he placed it. |
| Layout storage | Reuse the existing per-slot mechanism: localStorage + POST to `127.0.0.1:8765/__layout/gp-correct-check-offsets` (the server writes the whole JSON, so the new `promptBoxLayouts` field persists). Baked shipping table: `PROMPT_BOX_LAYOUT_BY_SLOT` (empty so far). |
| Undo vs Reset | The old Reset (wrote defaults over saved layout) became **Undo** (revert to last saved, writes nothing). The same token plumbing is reused (`correctCheckResetToken`). No "restore defaults" button exists now; offer it only if Chase asks. |
| Scope of layout editor v1 | Chase chose "prompt boxes only (recommended)" first, then asked for the rest after approving the feel. |
| Move cap | Offsets limited to +/-220px (same guard as check mark); sizes 120..1200 wide, 44..1200 high. Raise only if Chase asks. |

## Rejected directions (do not rediscover)

- **A fixed right-side scroll strip with a drag thumb and smooth paging**: wrong. The Macro App
  recipe is hover-to-scroll, two large arrow buttons, `behavior: 'auto'`, left side. Read
  `agent docs/recipes/vertical-scroll-rail.md` first. A port lives in
  `frame-gallery/ViewportScrollFrame.tsx`.
- **In-page hover rail inside the Teacher Console preview**: cannot work. The preview emulates
  touch (`hover: none`, mouse becomes taps). Macro App draws its own rail beside the preview
  (`BrowserVerticalScrollRail` in `TeacherConsolePreviewPhoneChrome.tsx`). Someone (Chase or an
  agent) already changed the CSS to hide the in-page rail under `@media (hover: none)` and
  recorded it in student-portal `AGENTS.md`. Do not add pointer handlers back.
- **Portaled help triggers inside thumbnails**: they portal to `document.body` at fixed viewport
  coordinates and floated over the gallery. Fixed with `HelpTriggerContainerContext`
  (Matrix `helpTriggerContainerContext.ts`) and a host wrapper in `FrameSolver`.
- **Re-reading the live box size on every pointer move** caused runaway resize. Size is captured
  once at pointerdown (`usePromptBoxLayoutEditing.ts`).
- **Resize handles as children of the scrolling dialog**: they scrolled/clipped with the text.
  Handles now sit on the outer wrapper; only the text div scrolls.
- A seeded `showCorrectCheck` flag in the session hook: dropped; preview mode does the job.

## Current implementation state

**student-portal** (`School Scrips/student-portal`, uncommitted):
- New `src/features/frame-gallery/`: `frameCatalog.ts`, `FrameSolver.tsx`, `FrameThumb.tsx`,
  `FrameGalleryView.tsx`, `ViewportScrollFrame.tsx` (+ `viewport-scroll-frame.css`),
  `useViewportSmoothScroll.ts`, `scrollSpeed.ts`, tests (`frameCatalog.test.ts`,
  `FrameSolver.test.tsx`).
- Edited: `App.tsx` (route branch), `usePortalRoute.ts` (`FRAME_GALLERY_ROUTE`, assignment route),
  `GuidedPracticeHomeworkHomePanel.tsx` (menu), `GuidedPracticeCheckLayoutBannerControls.tsx`
  (Show layout / Save / Undo, prop `onUndo`), `GuidedPracticeView.tsx` and
  `GuidedPracticeHomeworkView.tsx` (`onUndo`), `src/types/matrix-app.d.ts` (type shim: question
  kinds, matrix answer, container context module).
- `AGENTS.md` and `frame-gallery` CSS/scroll files were also edited by someone else mid-chat
  (scroll rail note, `hover: none` rule). Treat as current.

**Matrix app** (`School Scrips/Matrix app`, uncommitted):
- New: `helpTriggerContainerContext.ts`, `promptBoxLayoutPosition.ts`,
  `usePromptBoxLayoutEditing.ts`, `useGuidedPracticeSolverNotifications.ts` (extracted from the
  solver to get it under the 800 cap; solver now ~752 lines), `src/test/prompt-box-layout.test.tsx`.
- Edited: `GuidedPracticeOverlay.tsx` (layout/layoutPreview/onLayoutChange props, corner handles
  on the outer wrapper, ~440 lines), `GuidedPracticeSolver.tsx` (passes layout to overlay),
  `useGuidedPracticeLayoutPreview.ts` (prompt box state, save, undo), `gpLayoutPreviewPublish.ts`
  (`promptBoxLayouts`), `GuidedPracticeHelpTrigger.tsx` (container context),
  `guided-practice-answer-flow.ts` (give-answer no longer wiped on mount; real resume bug).
- **Mixed worktree:** many other modified Matrix files (three-var, RREF, retries) belong to the
  other 11.2 chat, not this one. Do not revert or fold them in.

**Verification done:** `tsc` clean for all new/edited files; portal `vitest src/features` 31 files
pass; Matrix vitest 242 pass, 1 fail. The failing test
(`guided-practice-infinite-solution.test.tsx` "reveals the parametric answer...") fails **without**
these changes too (comes from other uncommitted work). Portal `tsc` still shows unrelated errors
(`three-var-homework-problems` module, `solutionOnlyActive`, logic-homework). **Nothing has been
viewed on screen by the agent**, only by Chase (he confirmed the prompt-box editor feels good).

## Open questions and constraints

- **Which text boxes count as "all the other text boxes"?** Not yet enumerated. Candidates seen:
  yellow help labels ("Need help with...?" triggers, already draggable by offset, no resize),
  row-entry scaling/replacement reveal text, parametric solve reveal block
  (`PARAMETRIC_REVEAL_LAYOUT_KEY`), row-notation recovery panels, solution-type panel, fraction
  help prompt, floating builders. Propose a list to Chase; ask ONE question if scope is unclear.
- `GuidedPracticeOverlay` is shared with `ThreeVarHomeworkSolver` and `UnguidedPracticeSolver`;
  those do not pass `layout` props yet (defaults leave behavior unchanged). Stacked layout
  (practice) intentionally ignores the layout.
- Size caps: `GuidedPracticeSolver.tsx` ~752, `use-guided-practice-session.ts` ~714,
  `use-three-var-homework-session.ts` ~617. Extract before adding. Overlay ~440.
- Do not deploy to Netlify, do not commit or push unless Chase asks. Do not open a browser/window
  unasked.
- Frame gallery covers 2-var homework only; the 3-var flow and practice/other wrong branches
  (parametric reveal animation, setup step wrong variants) are not in the catalog.

## Exact next step

Generalize the layout editor from "prompt box" to a reusable wrapper, then apply it to the next
text boxes. Concretely: (1) read `usePromptBoxLayoutEditing.ts` and `promptBoxLayoutPosition.ts`;
(2) extract a small generic `LayoutEditableBox` (keyed layout store `boxId:slot`, same
move/resize/handles-on-outer-wrapper, same Save/Undo through
`useGuidedPracticeLayoutPreview`); (3) propose to Chase the exact list of text boxes to cover and
get one confirmation; (4) wire them in one at a time, adding a test per box like
`prompt-box-layout.test.tsx`. Hand him the visual check as a statement (open the frame gallery
full-size view, Show layout, drag a corner), never as a question.
