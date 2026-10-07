# Momentum handoff — portal instruction box, composite clip, TC preview dock

Written: 2026-10-06 (America/Chicago)
Workspace: C:\Users\chase\Documents\Programs
Phase: **Logic Homework** first-problem hint now uses the shared **portal instruction text box**
(not a full-width banner). Recipe **`portal-instruction-box.md`** + INDEX + student-portal
`AGENTS.md` row. **Composite Examples** Manim clip re-authored and copied into portal assets;
**Teacher Console** middle red notice dock beside phone preview **removed** (Macro App, uncommitted).
**Nothing committed or pushed** unless Chase says pull / end-of-session.

## Read first

1. Root `AGENTS.md` — momentum ≠ end-of-session; no GUI without per-run permission; student
   portal UI is **phone/student** (do not over-apply Chase dwell rules to portal hints).
2. **`agent docs/recipes/portal-instruction-box.md`** — `PortalInstructionBox`, CSS in
   `portal-features.css`, exemplars Logic hint + Practice intro.
3. **`School Scrips/student-portal/src/features/logic-homework/LogicHomeworkView.tsx`** — hint
   shows on first problem; dismisses on click `.table-header-flash` in embed (`onClickCapture`).
4. Composite clip chain: **`Manim Trial/composite_domain.py`**, `composite_domain_marks.json`,
   **`student-portal/.../compositeExamplesGuide.ts`**, asset MP4 under `video-examples/composite/`.
5. TC preview: **`Macro App/renderer/.../TeacherConsolePortalPreviewEmbed.tsx`**,
   **`ConsolePreviewWorkspaceScreen.tsx`** — errors go to side panel / diagnostics, not middle dock.

## Objective and current phase

Chase wants **student portal** apps to follow the same **blue bordered instruction box** pattern
as Matrix guided practice / Practice intro — **no numbered step badges** for one-line hints like
Logic problem 1. Separately: composite domain **video example** aligned with teaching notes;
Teacher Console preview workspace should not show a **red notice dock** in the middle of the phone
embed (warnings still in **Console warnings & errors** side panel and Settings → Diagnostics).

## Chase's desired feel (use his language)

- Instruction / tutorial tips = **instruction box**, not a striped banner or plain status line.
- **Not numbered** unless it is a real multi-step tutorial.
- Portal apps are for **students on phones** — different from Macro App / dwell density for Chase.
- Composite animation: domains beside **f** / **g**; build composite from **x²**; caption **“Solve
  for x.”**; composite-domain explanation **before** simplify; tag slides from **g**’s domain.
- TC preview: do not steal focus with a middle red dock; logging is fine elsewhere.

## Accepted decisions

| Area | Decision |
|---|---|
| Portal instruction UI | Shared **`PortalInstructionBox`** + `.portal-instruction-box*` in `portal-features.css`; slot wrapper for in-flow hints. |
| Logic problem 1 hint | Centered box under navy header; copy points at **?** header (no “flashing” in text); dismiss when student taps flashing **?** in embed. |
| Practice intro | Refactored to same component; Okay uses `portal-instruction-box__okay-btn`. |
| Matrix in portal | Embedded Matrix still uses **`GuidedPracticeOverlay`** Tailwind box — visual twin, not duplicated in every feature. |
| TC preview middle | Removed **`portalPreviewWorkspaceIssues`** UI + module; nav/refresh errors → **`logPortalPreviewError`**. |
| Composite render | Portrait **1080×1350** → portal asset; hold seconds from regenerated marks JSON. |

## Rejected directions (do not rediscover)

- Full-width **`.logic-first-problem-hint`** strip under header — wrong pattern.
- Numbered tutorial badge on Logic’s one-line first-problem hint.
- Showing TC preview errors in the **middle red dock** beside the phone (removed intentionally).
- Treating student-portal hint sizing as Macro App head-mouse / dwell target rules.

## Current implementation state

**Programs root (dirty):** `Manim Trial/composite_domain.py`, `composite_domain_marks.json`;
`agent docs/recipes/portal-instruction-box.md` (new), `INDEX.md`; session tracking logs.

**student-portal (dirty, separate repo):**
- New: `src/app/components/PortalInstructionBox.tsx`, `LogicFirstProblemHint.tsx`.
- Modified: `LogicHomeworkView.tsx`, logic home/entry/attempt, `UnguidedPracticeSessionIntro.tsx`,
  `portal-features.css`, `guided-practice.css`, `logic-embed.css` (flash keyframes for **?** header),
  `compositeExamplesGuide.ts`, composite MP4, minor `PortalMenu` / `MatrixTutorialNav` comment edits.
- Tests: **`npm run test -- --run`** — **49 files, 158 passed** (after instruction box work).

**Macro App (dirty, separate repo):**
- TC preview embed + workspace screen + `teacher-console-preview-notices.css`.
- **Deleted:** `portalPreviewWorkspaceIssues.ts` + test.
- Chase must **restart Macro App** to see dock removal locally.

**Earlier session work (may still be dirty / uncommitted):** domain/range Manim + portal clips,
video player segment end-frame behavior — see dated archive
`2026-10-04_domain-range-player-end-frames.md` if continuing that thread.

**Git sync blocker (unchanged):** `qud-mods` — push denied to upstream (not Chase’s repo).

**Editor context:** `Manim Trial/dot_product_directions.py` open — unrelated unless Chase pivots.

## Open questions / next work

- **Visual verify:** Logic Homework problem 1 — instruction box under header; **?** still flashes;
  hint dismisses on **?** tap. Ask before opening browser / launching portal dev server.
- **Macro App:** restart to confirm TC preview has no middle red dock; side panel still shows
  `[PortalPreview]` messages.
- **GitHub:** large uncommitted surface across Programs, student-portal, Macro App — Chase has not
  asked for **pull** or end-of-session this handoff.
- **Netlify deploy** — not requested.

## Constraints

- File size cap 800; orchestrators thin; modals no backdrop dismiss.
- Frozen: Calendar 2.0.
- No commit/push/metrics finalize as part of this handoff.

## Exact next step

If continuing portal polish: open Logic Homework in portal (instructor preview or dev — **ask
Chase first** if a window is needed) and confirm the **blue instruction box** matches Practice
intro styling; fix copy/layout only if it regressed.

If continuing TC: restart Macro App and spot-check preview workspace — no middle notice dock,
errors still logged in side panel.

If syncing: Chase says **pull** or **end of session protocol** → full multi-repo sync per root
`AGENTS.md` (include student-portal + Macro App + student-session-kit pair).
