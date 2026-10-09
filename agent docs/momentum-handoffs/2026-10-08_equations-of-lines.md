# Momentum handoff — Equations of Lines portal app (M1314)

**Written:** 2026-10-08

## Read first
- `School Scrips/student-portal/AGENTS.md` (portal rules; **never deploy to Netlify unless Chase says so in that message**)
- `School Scrips/student-portal/src/features/equations-of-lines/` (the app)
- Exemplar for wiring a reference app: Composite Examples (`features/video-examples/compositeExamplesGuide.ts`, routes in `hooks/usePortalRoute.ts`)
- Animations are Manim: see `Manim Trial/` and the portal pause/resume + video-examples recipes in `agent docs/recipes/INDEX.md`

## Objective and phase
Chase is building animations for the M1314 course. **Equations of Lines** (source: `C:\Users\chase\My Drive\M1314\Unit 2\Blank\2.5 Equations of Lines.docx`) is built as a static portal app, **no animations yet**. Next phase: Chase said "let's build the ..." (sentence cut off by the handoff request) — **ask him what he wants built next**; most likely the Manim worked-example animations for the 4 problems.

## Chase's desired feel
- Click the tile -> screen 1 shows the three forms (slope-intercept, point-slope, standard) with their rules, plus a **Show examples** button.
- Screen 2: four problems written like the worksheet. Problems 1+2 share one bold direction; the parallel and perpendicular problems each get their **own bold direction**. Each problem has a separate **Watch** button next to it (the problem itself is not a button, and is not boxed).
- Watch opens a per-problem page that will hold the animation. That page shows the problem as plain text, **no box**.

## Accepted decisions
- Problems numbered 1-4 (worksheet's 1, 2, 5, 6) — my choice, **not confirmed** by Chase.
- Parallel/perpendicular direction wording was written by me from his description — not confirmed.
- App is white-background, KaTeX via the existing `DomainRangeLatex`; navigation is internal state (forms -> problems -> example), no extra routes.
- Activity id `reference/equations-of-lines`, route `equations-of-lines`, section gate `transformations`, access off for students by default.

## Rejected / pitfalls
- Whole-problem-as-button and boxed problem on the example page: rejected by Chase.
- **LaTeX in TS strings: use `String.raw\`...\`` or double backslashes.** Single-quoted `'\tfrac'` became a tab and `'\,'` became `,` (caused `frac57` and `,,` bugs). Heredocs through bash also mangle backslashes — use the Write/Edit tools for files containing LaTeX.
- docx text extraction drops fractions; problem values were confirmed from Chase's words (m = 5/7; (3,4)) plus the doc text.

## Implementation state (all UNCOMMITTED, undeployed)
- New: `student-portal/src/features/equations-of-lines/` (Activity, Content, View, Forms, Problems, ProblemText, ExamplePage, css), `src/test/equationsOfLines.test.ts` (4 tests pass).
- Wired in: `hooks/usePortalRoute.ts`, `config/portalHomeApps.ts`, `hooks/portalFirstPaintAccess.ts` (+ test), `app/App.tsx` (now ~642 lines; 700 is the extract line), `app/components/MatrixHomeView.tsx`.
- Also uncommitted in student-portal: video aspect-ratio fix (`aspectRatio` on clip entries in `videoExamplesTypes.ts`, `VideoExamplesPlayerStage.tsx`, composite + domain-range guide files) — fixes the half-height-then-expand first load on Composite Examples / Domain & Range.
- Supabase: migrations 076, 077, **078_equations_of_lines_activity.sql** applied to remote via `npm run db:push` (078 file is uncommitted in student-session-kit).
- Machine pulled/synced earlier today; Programs root + Macro App pushed.
- Verification: tsc clean for these files; pre-existing unrelated tsc errors (generic-quiz, guided-practice, classworkData tests); `compositeExamples.test.ts` fails because it expects 1 example (guide has 3) — stale, not ours. **Never visually verified** (GUI rule: ask before opening a browser).

## Open items / constraints
- Macro App Teacher Console does not list Equations of Lines yet, so Chase can't toggle it on for students (mirror Composite: `useTeacherConsoleActivityCatalog.ts`, `teacherConsoleActivityTitle.ts`, `videoSlotCatalog.ts`, `portalPreviewRouteAspect.ts`).
- Chase has not yet looked at the final layout after the Watch-button/LaTeX fixes.
- No GUI/browser launches without asking; never deploy Netlify unprompted; handoff is a statement, not a question.

## Exact next step
Ask Chase what to build next (his message was cut off). If it's the animations: pick problem 1 (m = 5/7; (3,4), slope-intercept) and model on the Composite Examples Manim flow, replacing "Animation coming soon" in `EquationsOfLinesExamplePage.tsx`.
