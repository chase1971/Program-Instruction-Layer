# Momentum handoff — M2413 Visual Test and reusable animations

Written: 2026-10-03 23:42 -05:00 (America/Chicago)
Workspace: C:\Users\chase\Documents\Programs
Phase: implementation complete locally; user requested handoff before final delivery/visual review.

## Read first

1. Root AGENTS.md and agent docs/INDEX.md for routing.
2. School Scrips/student-portal/AGENTS.md and src/features/visual-test/README.md.
3. School Scrips/Macro App/AGENTS.md before changes there.
4. Manim Trial/docs/ANIMATION_REUSE.md only if animation workflow work resumes.

## Objective and desired feel

Chase wants to produce many educational animations cheaply and quickly, eventually asking for five at a time. Cheap models (Cursor Composer 2.5) make spatial/clipping mistakes; premium models work but exhaust usage. Premium planning followed by cheap implementation already failed. Cheap drafting followed by premium direct cleanup was discussed as a possible workflow, not proven savings.

He requested a compact reusable-pattern catalog, not hundreds of markers that themselves consume context. Broad division/fraction families matter; niche vector geometry is less reusable, but formula display/cancellation is useful. Read a small menu, then only relevant example code.

Current task is a visual diagnostic BEFORE deciding on global font/color changes: an app button named Visual Test in the ONLINE MATH2413 course inside Teacher Console, usable without a roster. Static equations from Angle Between Vectors problem (a), whose cosine is -0.22486. Preserve exact original formula geometry/size and the navy-shell/white-stage viewer scaling used by M2412 vectors. Next changes only the ink color through eight choices. No animations or diagrams. The user wants the current too-small worst case so he can judge readability himself.

## Completed earlier deliverable

Created Manim Trial/docs/ANIMATION_REUSE.md (~281 lines) with eight broad families: equation operations, division/factoring, fractions, cancellation, formula assembly, graphing, linked motion/measurements, collections/distributions. It gives symbol pointers, distinguishes helpers/input-driven scenes/hardcoded examples, and includes batch workflow, validation, premium repair handoff and catalog refresh guidance. Linked from Manim Trial/README.md, ANIMATION_STYLE_RECIPE.md and agent docs/INDEX.md. Links and Python symbols checked; session logged.

Discussed portrait-first layout and stronger colors on white. Existing 16:9 vector player uses contain/top center; a 360px-wide frame is only 202.5px high. Existing audit does not estimate final phone pixels. Global portrait rules, palette adoption, and resizing/re-rendering vector animations have NOT been implemented or approved as this deliverable.

## Current implementation — local only

### Manim Trial

New export_visual_test.py (~53 lines) AST-reads the strings in AngleBetweenVectors.problem_a from angle_between_vectors.py and invokes the actual make_given()/make_problem_rows(). It captures the static formula objects as white ink on transparent 1920x1080 using Manim Camera, preserving the full frame and original right-side placement. It exports PNG plus geometry metadata directly into the portal feature folder. No Scene.play, new video, or changes to original animation code.

Formula contents: given u=2i-2j, v=5i+8j, w=4i+4j; u dot v=(2)(5)+(-2)(8)=-6; magnitude product=(2sqrt2)(sqrt89); cos(theta)=-6/((2sqrt2)(sqrt89))=-3/sqrt178 approximately -0.22486; theta=arccos(-0.22486) approximately 102.99 degrees. The negative decimal is the cosine, not the angle.

Sizing measured from actual objects: ordinary rows 29.428706877 Manim font units; magnitude row 27.69760647; given-vector line 34.38325497. Ordinary row derives from 48 x 1.15 x 1.30 x .68 x fitted factor .60308681875. These are NOT CSS pixel sizes. At 360 CSS pixels frame width, single-line dot-product/final-angle glyph bounds are about 7.73px high. Fraction row total heights about 18.47/17.57px include the whole stacked fraction.

### School Scrips/student-portal

New src/features/visual-test/:
- visualTestConfig.ts: activity instructor/visual-test; title; palette; pure access predicate requiring instructor and online M2413 preview course label.
- VisualTestView.tsx: existing vector viewer shell/stage classes, white frame, accessible static formulas, Exit, persistent color name/hex, Next cycling all eight and wrapping. One state value. No video element.
- visual-test.css: transparent PNG is a CSS mask filling the original frame (contain, top center); selected color supplies ink. Geometry stays fixed.
- angle-formulas.png and angle-formulas.json: generated source geometry assets.
- README.md: scope, source, sizing, regeneration, local preview and remaining review.
- src/test/visualTest.test.tsx: course/instructor gates, route, color cycle and unchanged static mask tests.

Modified src/config/portalAccess.ts, portalHomeApps.ts, src/app/components/MatrixHomeView.tsx, src/hooks/usePortalRoute.ts, src/app/App.tsx to wire access, tile and assignment-style route (hides normal header); added feature doc pointer in AGENTS.md. App.tsx was already ~475 lines. No refactor of unrelated code.

Access helper reads existing previewCourse URL service. There is a module import cycle portalAccess -> previewTeacherConsole -> classworkData -> portalAccess; reads are in functions and focused tests/build pass. Do not invent a blocker, but keep in mind if later troubleshooting initialization.

Colors in required order (all on white):
1. Near-black #1A2332
2. Dark blue #1E40AF
3. Purple #6B21A8
4. Dark teal #115E59
5. Burgundy #9D174D
6. Dark red #991B1B
7. Slate #475569
8. Burnt orange #92400E
All calculated contrast ratios exceed 7:1. This is the test palette, not an automatic global recolor.

### School Scrips/Macro App

Rosterless online selected-course Preview support:
- renderer/src/utils/studentProgress/portalPreviewUrl.ts adds optional previewCourse fallback, preserving real course-map priority for dev/live URLs.
- renderer/src/hooks/teacher-console/useTeacherConsolePreviewIdentity.ts accepts selectedCourseLabel, passes it to URL/phone label, and allows rosterless preview only for Admin persona + online M2413.
- renderer/src/hooks/shell/useMacroAppStudentProgressShell.ts passes selectedCourse label.
- renderer/src/components/teacher-console/TeacherConsolePortalPreviewEmbed.tsx allows the existing preview frame when no map but that explicit rosterless flag is true; configuration guard remains. This file already had unrelated user changes: preserve them.
- renderer/src/utils/studentProgress/portalPreviewUrl.test.ts adds fallback and map-priority coverage.

Local course configuration has MATH-2413 4W01 Online. No roster/student/section/DB activity/grade data was created. This is an ungraded instructor diagnostic in the portal home inside Teacher Console Preview as Admin, not a grade activity in Macro App's activity catalog. This interpretation was stated in commentary, but Chase has not yet visually evaluated it.

## Verification already completed — do not repeat for the handoff

- Portal focused run: visualTest.test.tsx, portalHomeApps.test.ts, portalHomeApps.logic.test.ts — 3 files, 6 tests passed.
- Macro renderer portalPreviewUrl.test.ts — 14 tests passed.
- Portal npm run build passed (2429 modules; existing chunk-size warning).
- Portal npm run type-check has 18 errors in unrelated generic quiz, guided-practice, transformations and classwork test code; no errors reported in changed files. Global type check is not clean; do not claim it is or fix unrelated areas.
- ffprobe confirms original clip-02-angle-between.mp4 is 1920x1080.
- Export mask alpha validated (0..255; nontransparent bounds 1000,479 to 1846,1040). White mask looked white on white in image viewer; no actual colored browser render was visually checked.
- Scoped git diff --check passed (line-ending warnings only).
- No GUI/browser/phone smoke test; actual paint and phone readability review are pending.
- Deliverable session scorecard bump already recorded: implementation, 20 focused tests, successful build, unrelated type-check failures.

## Constraints and decisions not to lose

- NEVER launch/show a browser, GUI, preview, player, or UI smoke test without per-run permission. Chase uses head gyro + dwell clicking; surprise windows steal control. Headless checks are allowed. Give a flat user testing handoff, not a question asking him to do keyboard work.
- NOT deployed. Portal docs require an explicit deploy request. The Live/actual phone site will not contain this feature until authorized deployment; no deployment request was made.
- Do not enlarge, recenter or reflow these formulas yet: exact original worst-case size is the point of this diagnostic.
- Do not add animation, diagrams, roster data, tracking or grades to this diagnostic.
- Do not implement global portrait/color policy or re-render vector videos merely because it was discussed.
- Many unrelated dirty changes exist in root, Macro App and portal (including vector engagement/survey/stats). Preserve them. No commits/pushes this task.
- Beginning-of-task fetch scanned 42 repos, excluded frozen Calendar 2.0, all origins up to date. No need to redo sync for handoff.
- File caps and no new parallel mechanisms apply; no subagents requested/used.

## Exact next step

Read the feature README and give Chase the short delivery/testing handoff that had not yet been sent: Visual Test is implemented locally; select the online M2413 course in Teacher Console, use local Preview as Admin, then Visual Test; Next cycles the eight colors. Explain ordinary formula size is ~29.43 Manim units and about 7.73px glyph height at 360px frame width. Let his visual feedback guide changes. Do not open anything automatically. If he expects access from the live phone portal, clarify that deployment is still needed and wait for an explicit deployment request. Do not restart the implementation or broadly retest unless a concrete new issue warrants it.

The requested momentum handoff is a continuation boundary, not session end. No GitHub/end-of-session actions were performed.
