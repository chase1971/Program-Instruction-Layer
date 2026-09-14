# Momentum handoff — Refactor pass: Matrix done, Teacher Console next

**Written:** 2026-09-13 (Sunday, evening)

---

## 1. Objective and current phase

Chase asked for a refactoring survey of **Teacher Console** (Macro App), **student portal**, and
the **matrix tutorial** (Matrix app + portal `features/matrix-tutorial`), then to work through the
low-risk items. **Matrix app + portal matrix tutorial work is finished.** Next phase: the Teacher
Console / portal CSS items that were paused because another session was editing those files.
Chase says that other session is no longer working on anything.

## 2. Chase's desired feel

- "Not the risky one" — do the safe, behavior-preserving cleanups; **skip the Part 1–3 solver merge**.
- Go one step at a time; he asks "what's the next thing" and wants a plain-language answer
  before approving ("give it its own code" = extract into its own file/hook).
- Wants proof nothing visible changed (tests/builds, identical output), not UI launches.

## 3. Accepted decisions

- Survey order (approved): 1) Matrix dead code + helpers ✅ 2) remove blank-line padding + split
  over-cap CSS 3) split `studentProgressService.ts` + trim Teacher Console prop drilling
  4) portal auto-solve hook ✅ 5) Part 1–3 merge — **rejected for now (risky)**.
- CSS splits must preserve cascade order exactly:
  - Macro App: split a file into consecutive halves; import the new half **immediately after**
    the original in `renderer/src/modules/teacher-console/teacherConsoleEntry.ts`.
    Planned split points: `teacher-console.css` at line 457 (`/* ---- Reports screen` → new
    `teacher-console-reports.css`); `teacher-console-grades.css` at line 518
    (`.teacher-console-screen--logins` → new `teacher-console-logins.css`). Re-check line
    numbers first — files may have changed. **Update** `agent docs/recipes/report-grid-layout.md`
    (it points at `teacher-console-grades.css § logins`).
  - Portal `src/styles/index.css` (1103 lines) already `@import`s `matrix-embed.css` and
    `portal-layout-debug.css` at the top. Keep order by making index.css the import list
    (tailwind, existing imports, `@source`) and moving its body into consecutive files imported
    in original order. Landscape compact block is at the bottom (~line 1001+); update
    `student-portal/AGENTS.md` rows that say "bottom of `src/styles/index.css`" / "§ Compact layout".
- Blank-line padding: files double-spaced (a blank after every line). Remove only whitespace
  lines; verify with `git diff -w --ignore-blank-lines` showing nothing else. Candidates:
  `ConsoleDashboardScreen.tsx` (685→~347 real), `ConsoleRosterScreen.tsx`, `RosterStudentActions.tsx`,
  `ConsoleAppLiveScreen.tsx`, `useGradesScreenData.ts` (Macro App TC); portal
  `MatrixTutorialView.tsx`, `useStudentIdentity.ts`, `studentIdentity.ts`, `usePortalRoute.ts`,
  `StudentAnnouncementsPanel.tsx`. Scope is these three areas only.

## 4. Rejected directions / don't rediscover

- Swapping the row-scaling animations onto `shared/animation-cells.tsx` — different API and
  sizes; a new `shared/scaling-cells.tsx` was made instead.
- `MultiplyingCell` in `row-multiply-then-add-animation(-part-3).tsx` looks duplicated but
  differs (multiplier content, offsets) — belongs to the risky Part 1–3 merge.
- Editing files another live session is touching: check `find <dir> -mmin -30` mtimes before
  editing TC/portal files. A CSS split was done and **reverted** earlier for this reason.
- Don't open a browser/app to verify (root AGENTS.md) — headless checks, then state what Chase will see.

## 5. Current implementation state (all uncommitted — Chase has not asked to commit)

**Matrix app** (`School Scrips/Matrix app`):
- Deleted 53 unused files (`git rm`, staged): 45 shadcn `components/ui/*` (kept `button`, `input`,
  `utils.ts`), 6 dead notation/swap files, `figma/ImageWithFallback`, `shared/matrix-brackets`.
- `cloneMatrix` + `Matrix` type now imported from `utils/matrix-display.ts` / `types/matrix.ts`
  in `use-matrix-tutorial.ts`, `-part-2.ts`, `-part-3.ts`, `matrix-auto-solver.tsx`.
- New `components/shared/scaling-cells.tsx`; `row-scaling-animation`, `row-scaling-part-three-animation`,
  `row-multiplication-animation`, `row-multiplication-animation-part-2` use it. Verified identical
  rendered markup (incl. all motion props) via a temp test, since deleted.
- `npm uninstall` of 46 unused packages (package.json + lock); 4 root demo files deleted.
  Build output hash unchanged.
- Docs updated: `docs/MATRIX_APP_GUIDE.md`, `ANIMATIONS.md`, `TERMINOLOGY.md`, `README.md`.
- Pre-existing uncommitted Matrix work from an earlier session also present (auto-solver, part-3
  overlay, deleted fraction-answer files).

**Student portal** (`School Scrips/student-portal`):
- New `src/features/matrix-tutorial/useMatrixAutoSolveNav.ts`; `MatrixTutorialView.tsx` uses it (7→3 useState).
- Fixed hook-order crash: `MatrixTutorialView` is now a thin wrapper that shows
  `PortalAssignmentGate` when `attempt.blockingMessage`, else renders inner `MatrixTutorialScreen`.
- Lots of other uncommitted portal work from other sessions (assignment gate, quiz header, styles).

**Programs root:** `APP_LOCATIONS.md` gained Teacher Console + matrix tutorial alias rows.

**Verification last run:** Matrix vitest 27 pass + vite build OK; portal `tsc --noEmit` OK,
vitest 20 pass, vite build OK. Macro App not built/tested this session.

## 6. Open questions and constraints

- Macro App TC files still carry another session's uncommitted edits — preserve them.
- File cap 800: `teacher-console.css` 907, `teacher-console-grades.css` ~917, portal `index.css` 1103.
- Step 3 ideas (proposals, not approved in detail): split `studentProgressService.ts` (570 lines,
  48 exports) by domain — attempts/access, tester codes & sections, announcements, exit tickets,
  portal dev server; group `TeacherConsoleWorkspace`'s ~50 props into objects; `useTesterRename`
  hook out of `ConsoleRosterScreen`; dedupe the two identical `ConsoleRosterScreen` renders.
- Macro App CI before any push: `npm run ci:local` (only if Chase asks).
- Mojibake in `TeacherConsoleWorkspace.tsx` header comment ("â€”") — trivial.

## 7. Exact next step

Check recent mtimes in `Macro App/renderer/src` and `student-portal/src` to confirm nothing is
being edited, then do **step 2a**: split `teacher-console.css` and `teacher-console-grades.css`
with order-preserving imports in `teacherConsoleEntry.ts`, and run Macro App renderer lint/test/build.
