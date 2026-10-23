# Programs workspace — session log

Instruction-layer and cross-app work at `Programs/` root (not inside a single School Scrips app).

## 2026-10-23 — Matrix 11.2 homework polish (momentum handoff)

**Repos touched:** `Programs/` root, `School Scrips/Matrix app`, `School Scrips/student-portal`

**What worked:** Parametric solve animation (Factoring-style cancel, layout preview drag, no loop); global button press feedback; 3-var RREF retained + type check flash + dynamic parametric prompt; solution-type MCQ labels ("Exactly one solution").

**Current state:** Green vitest — portal spot-check still open on cancel-line alignment and 3-var flows.

**File size flag:** `GuidedPracticeSolver.tsx` ~793 lines (cap 800).

**Next session:** see `agent docs/momentum-handoffs/latest.md` (2026-10-23)

## 2026-10-23 — Parametric reveal animation + solution-type layout (momentum handoff)

**Repos touched:** `Programs/` root, `School Scrips/Matrix app`, `School Scrips/student-portal`

**What worked:** Parametric second-wrong reveal: no constant-column pulse, problem-driven solve animation with Play/Pause/Replay in movable panel; `getParametricRevealContext` + vitest; floating builders extract from solver. Solution-type MCQ panel raised 40px (`y: -12`).

**Current state:** Green headless tests — Chase has not portal-verified animation placement or MCQ position.

**File size flag:** `GuidedPracticeSolver.tsx` ~785 lines.

**Next session:** see `agent docs/momentum-handoffs/latest.md` (2026-10-23)

## 2026-10-23 — Homework practice mode choice (momentum handoff)

**Repos touched:** `Programs/` root, `School Scrips/student-portal`, `School Scrips/Matrix app`

**What worked:** Mid-homework mode modal (left-aligned copy, tap choice, no Continue); wired **Just right or wrong** to `UnguidedPracticeSolver` on homework; `homeworkSolveMode.ts` + progress `solveModeByProblem`; admin temp preview jumps to problem 3 for practice test (problem 1 is infinite-solution).

**Current state:** Green build/tests — pending Chase portal confirm on unguided problem 3; revert `GJ_HOMEWORK_MODE_CHOICE_TEMP_PREVIEW_IMMEDIATE` before ship.

**File size flag:** `GuidedPracticeSolver.tsx` ~760+ lines (extract before more features).

**Next session:** see `agent docs/momentum-handoffs/latest.md` (2026-10-23)

## 2026-10-23 — 11.2 Homework UX, resume, momentum handoff

**Repos touched:** `Programs/` root, `School Scrips/Matrix app`, `School Scrips/student-portal`

**What worked:** Solution-type MCQ like Factoring (tap choice, no Submit); parametric help shell; row-entry fraction help in-flow; homework resume saves farthest step (tester Next); row-notation box 50px narrower without moving left; number pad close buttons off.

**Current state:** Green — pending Chase portal pass on fraction help, green check, resume, row-notation width.

**File size flag:** `GuidedPracticeSolver.tsx` ~760+ lines (extract before more features).

**Next session:** see `agent docs/momentum-handoffs/latest.md` (2026-10-23)

## 2026-10-23 — 11.2 Homework layout preview and help triggers (momentum handoff)

**Repos touched:** `Programs/` root, `School Scrips/Matrix app`, `School Scrips/student-portal`, `School Scrips/student-session-kit`, `School Scrips/Macro App`

**What worked:** Homework title **11.2 Homework**; solution-type MCQ in right panel; yellow help viewport-anchored; **Layout preview** for green check + help triggers with Save; fixed `currentSlot` ReferenceError in solver.

**Current state:** Green — pending Chase visual confirm on row-entry fraction help and saved check/help offsets.

**File size flag:** `GuidedPracticeSolver.tsx` ~740 lines (extract before more features).

**Next session:** see `agent docs/momentum-handoffs/latest.md` (2026-10-23)

## 2026-10-21 — Fine-tune pipeline docs built (Cursor)

**Repos touched:** `Programs/` root, `School Scrips/student-portal`, `School Scrips/student-session-kit`, `School Scrips/Macro App`

**Files changed:** `Manim Trial/docs/FINE_TUNE_BRIEF.md`, `FINE_TUNER.md`, updates to `FINE_TUNE_PIPELINE.md` (Cursor CSV usage, cost weighting, pointer-only spec), `.cursor/.claude/.codex` `manim-fine-tuner` stubs, `.gitignore` allowlist for those agent folders, `agent docs/INDEX.md`.

**What worked:** Reviewed the plan from Cursor's side. Local Cursor DB has no token counts; the dashboard `usage-events` CSV is the source, with no chat ID, so benchmark runs cannot overlap other Cursor chats. Built the builder brief, the short fine-tuner spec, and the three tool stubs. Cursor stub pins `claude-opus-5-5[effort=medium]` (exact ID unverified until first run).

**Current state:** Green — docs built, never run on a clip. Same-night save also includes Gauss-Jordan Method Homework in portal, session-kit, and Macro (see those SESSIONS).

**File size flag:** None.

**Next session:** Read-only baseline scan of past Manim transcripts, then one real clip through arm B. First Cursor fine-tune: confirm the subagent card names Opus.

## 2026-10-21 — Fine-tune pipeline plan, handoff and tracking cleanup

**Repos touched:** `Programs/` root (other agents this day also touched `School Scrips/student-portal` and `School Scrips/Macro App` for the Gauss-Jordan homework; see their SESSIONS)

**Files changed:** `Manim Trial/docs/FINE_TUNE_PIPELINE.md` (plan; `FINE_TUNER.md`, `FINE_TUNE_BRIEF.md` and the `.cursor/.claude/.codex` `agents/` stubs were built by Cursor), `agent docs/MOMENTUM_HANDOFF.md`, `WRAP_UP.md`, `SESSION_TRACKING.md`, `SESSION_METRICS.md`, `INDEX.md`, root `AGENTS.md`, `scripts/scorecard-enforce.js`, `scorecard-hook-tally.js`, `session-tracking-store.js`, `session-token-cost.js`, `session-scorecard-ops.js`, `append-session-scorecard.js`; new `scripts/context-growth-estimate.js`, `scripts/session-context-jumps.js`.

**What worked:** Plan for cheap-model build then premium-model fine-tune of Manim clips, with a benchmark that only records what a platform reports. Momentum handoff is tool-neutral, has no pasted prompt, and writes the short wrap-up entry too. Cursor/Codex context warning now estimates growth from tool calls and words written (tool calls explained 87% of context growth across 128 sessions; messages 22%). Tracking now records per-turn models (`modelTurns`), the five biggest context jumps per task (`topJumps`), and the Stop hook writes an `autoBump` row instead of blocking.

**Current state:** Green — scripts syntax-check and the new tracking paths were exercised in a throwaway copy with fake data, not in live Cursor.

**File size flag:** None.

**Next session:** Read-only baseline scan of past Manim transcripts; review the Cursor-built fine-tuner files; test whether Cursor delivers the context warning (`additionalContext`) or ignores it; decide whether to keep `--gap`; write the Cursor usage CSV reader.

## 2026-10-20 — Build mode Phase 5 recipe and proof save

**Repos touched:** `Programs/` root, `School Scrips/Macro App`, `School Scrips/student-portal`, `School Scrips/canvas-kit`, `School Scrips/Factoring Guided Practice`, `School Scrips/logic-app`

**Files changed:** `agent docs/recipes/build-mode-implement-planned.md`, `agent docs/recipes/INDEX.md`, Macro and student-portal `AGENTS.md` keyword rows, `scripts/build-layout-docs-route.js`, `serve-programs-docs.js`. App code saved in those repos (see their SESSIONS).

**What worked:** Phase 5 recipe so "put this text box in the app" reads `buildLayout.json`, consumes `planned` rects, and flips them to `implemented`. Phases 1-4 Build proof (overlay, panel, shared phone chrome, playground, canvas-kit editor) saved the same night.

**Current state:** Green — proof built and uncommitted work is this save. Phase 6 visible trial not started. Chase is not ready to try yet.

**File size flag:** student-portal `App.tsx` is 708. Macro `teacher-console-workspaces.css` and `teacher-console.css` remain over cap (not edited this save).

**Next session:** Phase 6 visible trial when Chase asks: add and place a box in Build, say put this text box in the app, reload, check Preview.

## 2026-10-13 — Factoring Guided Practice momentum + session finalize

**Repos touched:** `Programs/` root, `School Scrips/Factoring Guided Practice`, `School Scrips/student-portal` (app detail in those SESSIONS)

**Files changed:** `agent docs/momentum-handoffs/latest.md` + dated copies; session tracking/metrics logs; student-portal `AGENTS.md` Factoring keyword (matrix-embed key override / `stepLinesPct`).

**What worked:** Momentum handoff for portal GCF→solve path; end-of-session metrics finalize.

**Current state:** Green.

**File size flag:** None.

**Next session:** See Factoring Guided Practice 2026-10-13 entry.

## 2026-10-12 — Car position/area animation: Parts 3–5 rebuilt (odometer gains, cancellation, hill picture)

**Repos touched:** none for the animation itself (`C:\Users\chase\My Drive\M2413\Unit 4 Integration\car-position-area-animation.html` lives outside git); `Programs/` root for this log and session-tracking files only.

**Files changed:** `car-position-area-animation.html` (~500 lines, single file, outside git).

**What worked:** Part 3 (v=2t) rebuilt as 16 static steps: area vs p(t) at t=1,2,3,5 in a growing table → slope stops at t=2,4 → odometer readings and exact gains chunk by chunk from zero (1 s, then 0.5 s) → the rectangle guess `v·dt` vs the exact gain → all gains → a clean cancellation screen (each gain as end − start, middle readings struck, p(0) and p(10) boxed) → limit-first integral. Part 4 (v=t(10−t)) got the same treatment (22 steps), with chunk totals built from zero (165 / 166.25 / 166.65) and honest over/under wording. New Part 5, "the hill picture": steepness = height gained per second of ground, steepness × ground = climb (same as speed × time), height of v = steepness of p, sum of rectangles vs total climb, and "your height is your start plus every climb so far". The key conceptual fix for Chase: the position function does no summing; it is accumulated change, so the middle terms cancel. A tick is distance gained in a chunk, not time; the exact gain `p(b)−p(a)` is the exact area, only `v·dt` is a guess. Also fixed the `?part=&step=` regex (was `\\d`). Fixed Part 5 text clipping off the right edge.

**Current state:** Green — script syntax OK and all 5 parts × all steps draw headlessly; Chase has seen Part 5 steps 1–2 render and the clipping was fixed, other Part 3–5 steps not yet reviewed in the browser.

**File size flag:** `car-position-area-animation.html` now ~560 lines of one self-contained file (outside git; no size cap applied).

**Next session:** Chase reviews Part 3 steps 7–16, Part 4 steps 3–22 and Part 5 in the browser for crowding (decimal tables, gain brackets about 6 px tall). `fundamental-theorem-animation.html` still has the old controls; untouched.

## 2026-10-12 — Portal survey copy index + exit-ticket statistics recipe

**Repos touched:** `Programs/` root, `School Scrips/Macro App`

**Files changed:** `agent docs/recipes/portal-survey-copy-index.md`, `teacher-console-exit-ticket-survey-statistics.md`, `agent docs/recipes/INDEX.md`; Macro `AGENTS.md` keyword rows; implementation lives in Macro App (see that repo’s SESSIONS entry same date).

**What worked:** Single map for where survey wording lives (TC → `content/exit-tickets/*.txt` vs code-owned `*Copy.ts`). Not a dump of all question text in one markdown.

**Current state:** Green — local only until git push.

**File size flag:** None

**Next session:** Same as Macro App wrap-up entry 2026-10-12.

## 2026-10-11 — Hyperbola: Horizontal clip (build, full-graph foci, pivot for c)

**Repos touched:** `.` (Programs root — `Manim Trial/`, `agent docs/`), `School Scrips/student-portal`, `School Scrips/student-session-kit`

**Files changed:** `Manim Trial/hyperbola_horizontal.py` (new, ~540 lines), `hyperbola_horizontal_{marks,steps}.json`, `Manim Trial/ellipse_horizontal.py` (`ellipse_row(..., op='+')`, default unchanged), `student-portal/src/features/video-examples/conicsGuide.ts` (hyperbola entry, Part 1/2, group list), `src/test/conicsGuide.test.ts`, `src/assets/video-examples/conics-intro/hyperbola-horizontal.mp4` + `-steps.json`, `agent docs/recipes/portal-math-video-examples.md` (Conics graphing-clip note).

**What worked:** `(x-1)^2/25 - y^2/49 = 1` clip. Part 1: a² is always under the FIRST term (formula numerators swap with `Swap`, a²/b² stay put), the variable in front gives direction and vertices, center, a = 5 / b = 7, transverse and conjugate axes, graph the center and vertices, dashed box, full-length asymptotes through the box corners (graph window x -10..14, y -10..10, drawn zoomed out), curves approaching them. Part 2 on the FULL graph (no zoomed quarter, which cut the hyperbola off): box triangle a, b, c; a² + b² = c² (plus, unlike the ellipse); c = √74; the blue diagonal pivots like a clock hand onto the transverse axis (right side only) to show the focus is c from the center; left focus just appears; asymptotes via up 7 / over 5, slope ±7/5, point-slope with the center. Hold 168.56 s, Part 2 starts 94.4 s. conicsGuide test 9/9, audit clean on all 39 marks.

**Current state:** Green — rendered, in the portal, tests pass; not deployed to Netlify, nothing committed. Chase has reviewed the foci beat and approved the pivot approach; the rest of the final build is not yet re-confirmed in the player.

**File size flag:** None.

**Next session:** Build "Hyperbola: Vertical" (add its label to the `hyperbola` group in `conicsGuide.ts`, slope is ±a/b there); optionally put the hyperbola clip in the Macro App teacher console list if Chase wants it.

## 2026-10-11 — Ellipse: Horizontal clip (build, foci derivation, final-graph fix)

**Repos touched:** `.` (Programs root — `Manim Trial/`), `School Scrips/student-portal`, `School Scrips/student-session-kit`

**Files changed:** `Manim Trial/ellipse_horizontal.py` (new, ~400 lines), `ellipse_horizontal_{marks,steps}.json`, `student-portal/src/features/video-examples/conicsGuide.ts` (ellipse entry, Part 1/2 buttons), `src/test/conicsGuide.test.ts`, `src/assets/video-examples/conics-intro/ellipse-horizontal.mp4` + `-steps.json`.

**What worked:** `x^2/9 + (y-3)^2/4 = 1` clip: formula under the intro, center, a = 3 / b = 2 from the square roots, major axis, graph + answer list, then Part 2 finding c — zoom in, dashed major axis, right triangle (b² + c² = a²), 9 − 4 = 5, c = √5 exact, c follows the vertices, foci (0 ± √5, 3), all answers back on the graph. Fixed a bug where the zoom `ReplacementTransform` reshaped the original graph objects in place, so the final graph came back zoomed and off the grid (now returns to `.copy()`s). Another chat later reworded the opener and re-rendered (see the entry above).

**Current state:** Green — in the portal, test passes; not deployed to Netlify, final player view not yet confirmed by Chase.

**File size flag:** None.

**Next session:** Chase reviews Conics → Ellipse in the portal; hyperbola clips not built.

## 2026-10-11 — Ellipse: Vertical clip + ellipse form caption

**Repos touched:** `.` (Programs root — `Manim Trial/`), `School Scrips/student-portal`, `School Scrips/student-session-kit`

**Files changed:** `Manim Trial/ellipse_vertical.py` (new, mirrors `ellipse_horizontal.py`; problem `(x-2)^2/9 + (y+1)^2/16 = 1`), `Manim Trial/ellipse_horizontal.py` (opener reworded, new `form` beat), `student-portal/src/features/video-examples/conicsGuide.ts`, `src/test/conicsGuide.test.ts`, `src/assets/video-examples/conics-intro/ellipse-{horizontal,vertical}.mp4` + `-steps.json`.

**What worked:** Built and rendered the vertical ellipse clip (center (2,-1), y+1 shown as y-(-1), a = bigger half-length so a^2 sits under y, foci (2, -1 ± sqrt7)); wired as the second Ellipse clip. Per Chase, both ellipse clips now open with "Since both x and y are squared and we are adding, this is an ellipse" and get a separate caption when the formula appears ("For ellipses, a is always the bigger number..."). Re-rendered both; hold 117.78 s, Part 2 starts 62.18 s. conicsGuide test 7/7.

**Current state:** Green — clips are in the portal; not deployed to Netlify, not viewed in the player yet.

**File size flag:** None (`ellipse_vertical.py` ~440 lines).

**Next session:** Chase reviews both Ellipse clips in the portal (Conics → Ellipse). Hyperbola clips still not built.

## 2026-10-11 — Conics classroom HTML set (M2412 Drive folder)

**Repos touched:** `.` (Programs root — `Manim Trial/conics_intro.py`)

**Files changed:** `Manim Trial/conics_intro.py` (hyperbola plane now extends through both cones, camera faces it); outside the repo, in `My Drive/M2412/Unit 3 (10.2 - 10.7)/Conics/`: `index.html`, `player.html`, `Conic Sections.html`, `videos/*.mp4` (6 clips copied from the portal assets; intro re-rendered).

**What worked:** Removed my first interactive 3D page (wrong ask). Built the Conics index (intro + Parabolas/Ellipses/Hyperbolas lists) and a shared `player.html?clip=` with Back/Auto/Next/Restart/Full screen and Part buttons, styled like the M2413 linear-approximation page. No step/caption text. Next only starts the next step (disabled while playing). Re-rendered the intro so the hyperbola plane visibly cuts both cones.

**Current state:** Green — not opened in a browser; frames checked headlessly.

**File size flag:** None

**Next session:** Hyperbola clips when made (add to `index.html` + `CLIPS` in `player.html`). The portal still holds the old intro MP4; the re-rendered one lives only in the Drive folder.

## 2026-10-08 — GitHub sync workflow (wrap up, pull registry, session-guided pull)

**Repos touched:** `.` (Programs root — `agent docs/`, `scripts/serve-programs-docs.js`, `scripts/sync-pull-registry-ops.js`)

**Files changed:** `agent docs/WRAP_UP.md`, `agent docs/END_OF_SESSION.md`, `agent docs/rules/multi-repo-git-push.md`, root `AGENTS.md`, `agent docs/INDEX.md`, `agent docs/sync-pull-registry.json`, `instructional-layer-htmls/github-sync-and-app-map.html` (rewritten), `instructional-layer-htmls/sync-pull-registry.html`, `page-manifest.json`; Macro App `AGENTS.md` (pull row).

**What worked:** Split **wrap up** (document only, no git) from **put on GitHub** / end-of-session. Session-guided **pull from GitHub** + **sync-pull-registry.json** (17 Pull / 27 Skip after Chase saved toggles). Pull/skip UI with server save endpoint. Rewrote sync reference HTML to match current procedure. Clarified portal embeds (logic / transformations / Matrix) vs standalone apps.

**Current state:** Green — docs and registry on disk; **not pushed** this wrap-up (Chase pushes at end of night).

**File size flag:** None

**Next session:** **Put on GitHub** when ready so laptop gets registry + docs; then **pull from GitHub** on other machine.

## 2026-09-16 — Guided-practice fraction help and viewport tuning

**Files changed:** Matrix app guided-practice builders, session hook, fraction-help components and MP4 asset; student-portal guided-practice screens and scoped styles; `Manim Trial/fraction_times_whole.py` and pause marks; viewport-budget recipe, app routing docs, momentum handoffs, and generated session logs.

**What worked:** Completed the Q5 help path from draggable alert and blurred Yes/No prompt through a click-driven, non-interactive Manim lesson. The lesson now uses numbered tutorial cards, immediate text changes, Back/Next navigation, Replay below the animation, multiple examples, a right-side Resume button, and an unsaved Yes/Kinda/No feedback gate. Related guided-practice builder sizing, live cell previews, row-entry transitions, portal preview framing, and 812×460 layout work are included.

**Current state:** Green — Matrix app and student-portal production builds pass; Chase approved the flow through the final “Play another example” adjustment.

**File size flag:** `student-portal/src/styles/guided-practice.css` was split; fraction-help styling now lives in `guided-practice-fraction-help.css`. No changed file exceeds 500 lines.

**Next session:** Verify the final Q5 sequence and record the alert coordinates, then build the matching Q9 add/subtract lesson.

## 2026-09-13 — Recipe: portal assignment gate

**Files changed:** `agent docs/recipes/portal-assignment-gate.md` (new), `agent docs/recipes/INDEX.md` (row), `agent docs/recipes/first-paint-gate.md` (touch), momentum handoffs for grades/logo work.

**What worked:** Documented the full-page portal assignment gate pattern (blocking errors, Refresh + Go home, no backdrop dismiss). App implementation and deploy logged in `student-portal/docs/sessions/SESSIONS.md`.

**Current state:** Green.

**File size flag:** None.

**Next session:** None queued.

## 2026-09-13 — Recipe: pressable buttons

**Files changed:** `agent docs/recipes/pressable-buttons.md` (new), `agent docs/recipes/INDEX.md` (row).

**What worked:** Captured Chase's requirement that buttons look raised, sink on press, and that a chosen toggle stays pushed in (dwell clicks are too quick to see `:active`). Exemplar: Macro App `teacher-console-side-panel-buttons.css`, built this session. Main work of the session is logged in `student-portal/docs/sessions/SESSIONS.md`.

**Current state:** Green.

**File size flag:** None.

**Next session:** None queued.

## 2026-09-11 — Session tracking fixes, scorecard split, capture-ladder pages refreshed

**Files changed:** `scripts/session-token-cost.js` (count each reply once, tail context reader, `HEAVY_CONTEXT_TOKENS`),
`scripts/chat-task.js` (new — per-chat identity + message counts), `scripts/scorecard-enforce.js`,
`scripts/scorecard-hook-tally.js`, `scripts/scorecard-navigation-path.js` (+`validateNavigationPath`),
`scripts/session-tracking-store.js`, `scripts/session-tracking-html.js`, `.gitignore`; split
`scripts/append-session-scorecard.js` 926 → 101 lines into new `session-scorecard-ops.js`,
`session-metrics-store.js`, `session-metrics-html.js`, `session-metrics-card.js`;
`agent docs/SESSION_TRACKING.md`, `agent docs/SESSION_METRICS.md`; six HTML pages
(`context-engineering-*`, `rule-architecture-infographic`, `instructional-layer-htmls/head-agents-md`,
`measuring-agent-efficiency`); generated logs.

**What worked:** Audited whether session tracking and the momentum handoff produce real data. Token cost
was recorded on only 4 of 342 bumps (Claude Code only — Cursor transcripts carry no usage) and was 2–4×
high because the reader summed one transcript line per content block; fixed, and 4 logged entries recounted.
The context warning is now per chat, so a fresh task after a handoff starts at zero, and it fires on real
context size in Claude Code (message count in Cursor). Bumps with unknown step keys or no outcome are now
rejected instead of silently logged as `helpful`. Split the over-cap scorecard entry file and proved the
split byte-identical on page output and identical across all six CLI modes against a pre-split snapshot.
Refreshed the capture-ladder HTML family, which still taught the retired `.mdc` mechanism as rung 3.

**Current state:** Green — every changed script loads, bump/finalize/rebuild verified headlessly,
check-docs 0 dead links, HTML tag balance unchanged.

**File size flag:** `append-session-scorecard.js` 926 → 101. Largest new file `session-metrics-card.js` 391.
None over 500.

**Next session:** Confirm a Cursor bump records `chatUserMessages` — the Cursor transcript resolves by
conversation id but has not run through the new hook yet. Handoff-effect data is still only two days deep.

---

## 2026-09-08 — Agent measurement workbench + session-tracking trim

**Files changed:** `scripts/session-tracking-stats.js`, `session-token-cost.js`, `scorecard-hook-tally.js`,
`session-tracking-store.js`, `session-tracking-html.js`; `scripts/token-report.js`, `token-report-data.js`,
`cursor-token-scan.py`; `scripts/run-probes.js`, `probe-report.js`; `agent docs/probes/retrieval-probes.json`;
`agent docs/instructional-layer-htmls/agent-measurement-workbench.html`; `agent docs/SESSION_TRACKING.md`;
`agent docs/index.html`; generated HTML logs.

**What worked:** Removed measurement artifacts from session tracking (`indexFirst`,
`unexplainedSearches`, `pathCoverage`); added per-task token cost from transcript. Built regenerable
token usage report (Read ~34% of cost vs Edit ~8.5%). Built 20-question retrieval probe set with
baseline 20/20. Added measurement workbench landing page linking all three reports + experiment queue.
Also: Manim two-step equation animation delivered to scratch HTML.

**Current state:** Green — reports regenerate via documented commands on port 8765.

**File size flag:** None.

**Next session:** Run probe experiments from workbench queue; optional Manim index row if that tree
gets more animation work.

---

## 2026-09-07 — Stale workspace root broke Grep; APP_LOCATIONS path check added

**Files changed:** `scripts/check-docs.js` (+~45 lines — new MISSING PATHS check, `LOCATIONS_DOC`, header item 7, summary and `--strict` wiring); `APP_LOCATIONS.md` (D2L Assignment Assistant row repointed); `School Scrips/Macro App/AGENTS.md` (slim build row said four tabs, ships three).

**What worked:** A sub-agent had spun and died looking for how the app launches in prod-renderer mode. The cause was not the search — Chase deleted `Documents\D2L Assignment Assistant` today, Cursor still has it registered as a workspace root, and the `Grep` tool fails wholesale with "Path does not exist" when any root is missing, so it never searched anything. `rg` through Shell was the workaround and answered the original question immediately: `electron-app/main.js:330`, `app.isPackaged || MACRO_APP_PROD_RENDERER === '1'` chooses `loadFile` on `renderer/dist/index.html` over the dev server. The failed task's own "no references found" output was a false negative — it was killed at 46s mid-scan because `Get-ChildItem -Recurse -Exclude` enumerates `node_modules` before filtering.

Chase's separate question — a slim hand-off build with only Browser, Makeup Exam, and Email — needed no work. `build-profiles/slim/build.config.json` already excludes all three calendar tabs and sets `memoryPill: false`, and profile builds already relocate to `%APPDATA%\macro-app-<profile>`, so the shared-settings risk he was worried about was solved on 2026-09-07 in `51420e9`. Per-recipient tab configs are not warranted for two users who want the same three tabs; a fourth profile folder is ~5 minutes when someone wants something different.

The deleted folder left a stale row in `APP_LOCATIONS.md`, and Chase asked why the doc checker never flagged it. It could not have, at any point: `CODE_PATH_RE` only matches backticked names ending `.md`/`.mdc`, so a bare folder path was never examined, and even a match would have been suppressed by the `kind === 'link'` gate. The gate is right in general — backticked paths elsewhere are often prose — but `APP_LOCATIONS.md` is the one doc where a path is a claim about the disk. Added a check scoped to that file only, verified by appending two probe rows (one caught with line number, one correctly silenced by the new `<!-- path-ok: -->` hatch) and reverting.

**Current state:** Green — `check-docs.js`: 0 dead links · 0 broken chain · 0 missing paths · 90/99 unrouted. Warning-only by design: these are absolute machine paths and the laptop legitimately lacks the desktop's `My Drive` root, so a hard failure would go red on every laptop run.

**File size flag:** None. `scripts/check-docs.js` is 450 lines.

**Next session:** Nothing pending in the repo. The Cursor workspace root itself is unfixable from here — there is no `.code-workspace` file, so it lives in Cursor's own state and only Chase can remove it. Until he does, `Grep` stays broken workspace-wide and `rg` via Shell is the fallback.

> **Superseded 2026-09-09.** The stale root is gone: `C:\Users\chase\.cursor\Programs.code-workspace` now lists only `Documents/Programs` and `My Drive/Rosters etc`, both of which exist. The IO error still seen afterwards was a different bug — `Grep` fails only when the explicit `path` *is* the workspace root spelled with an uppercase `C:`, because Cursor registers it lowercase and compares case-sensitively. Omitting `path` works. `Grep` is **not** broken workspace-wide and `rg` via Shell is **not** the general fallback. Rule captured in root `AGENTS.md` § Searching this tree.

---

## 2026-09-07 — Gradebook sync fixes, Matrix tutorial, and MT2 tools

**Files changed:** Macro App gradebook pull/cache and two-decimal average calculation with regression tests; Matrix tutorial navigation/checking and Auto Solve gating; Electron Toolbar scripts panel; new local `mt2-dwell-floors` plugin; Programs routing, scratch pages, and generated session tracking.

**What worked:** Repaired six false Calculus pending grades without pushing to D2L, invalidated stale gradebook caches after successful pulls, corrected the manual-pull regression, and matched D2L's two-decimal calculated-final precision. Matrix tutorial navigation and completion gating were completed. MT2 dwell-floor and run-report tooling was added and routed.

**Current state:** Green — Macro renderer typecheck passed; gradebook precision and cache tests passed.

**File size flag:** `School Scrips/Matrix app/src/components/matrix-solver.tsx` is 753 lines and must be extracted before future edits.

**Next session:** Continue the next requested teaching-app task; extract `matrix-solver.tsx` first if Matrix work resumes.

---

## 2026-09-06 — Phone-to-desktop agent worker (My Machines)

**Files changed:** `agent docs/PHONE_AGENT_ACCESS.md` (new, ~95 lines); `agent docs/INDEX.md` (+1 row); `scripts/cursor-worker-start.ps1` (new, ~111 lines); `scripts/Start Cursor Worker.vbs` (new, ~16 lines).

**What worked:** Chase wanted to send a task from his phone and have it run here — "commit and push so I can pull at work." That's Cursor's My Machines worker, so the job was turning it on, not building anything. Two things blocked it. Build `2026.09.02-c22c1a3` ships Node 24 but a `better_sqlite3.node` compiled for Node 22, so the bundled runtime dies with `ERR_DLOPEN_FAILED` (ABI 127 vs 137) and the worker cannot start at all; the launcher now probes that exact `require` and falls back to system Node 22, which self-heals when Cursor fixes the build. And a worker started from the agent's terminal dies when that terminal is torn down — that was the `exit_code=4294967295` notification — so a `.vbs` starts it windowless and a PowerShell loop supervises it, with a `shell:startup` shortcut for login. Also passes `--idle-release-timeout 0`, since the CLI's 3600 default silently drops the machine off the phone's picker after an hour idle.

**Current state:** Green — Chase confirmed `desktop` appears under cloud/remote machines on his phone. One supervisor + one worker running after clearing duplicates and an orphan.

**File size flag:** None.

**Next session:** Nothing pending. The runtime probe reverts to bundled Node on its own once a corrected build ships.

---

## 2026-08-30 — Guildrun Stats last-battle toolbox + INDEX rows

**Files changed:** `agent docs/INDEX.md` (+12 pointer rows); `APP_LOCATIONS.md` (Guildrun row). App code is local-only under `Guildrun Stats/` — see `Guildrun Stats/docs/sessions/SESSIONS.md`.

**What worked:** Indexed trigger dropdowns, attack/ability scaling, last-battle casts, Hermit vs Poisonous Attacks, grown-this-fight, and “is end-of-combat Magic stored.”

**Current state:** Green — INDEX matches the session; Guildrun sheet is local.

**File size flag:** None in this repo.

**Next session:** Guildrun Stats work continues from that app’s `docs/sessions/SESSIONS.md`.

---

## 2026-08-30 — Modal-over-browser freeze mandatory in recipes

**Files changed:** `agent docs/recipes/modal-shell.md`, `agent docs/recipes/INDEX.md`. Macro App app work logged in `School Scrips/Macro App/docs/sessions/SESSIONS.md`.

**What worked:** Added § Macro App embedded browser to `modal-shell.md` — freeze before open, unfreeze on every close path, close modal before live D2L navigation. Indexed rows for PAUSED-stuck / snapshot / freeze. Cross-linked `EMBEDDED_BROWSER_AND_MODALS.md` ↔ modal-shell. Macro App `AGENTS.md` "new modal" row now requires both docs when Browser tab is visible.

**Current state:** Green — doc-only for this repo; Macro App bulk-pull freeze fix shipped in sibling repo.

**File size flag:** None.

**Next session:** None for docs unless another modal-over-browser feature is added without reading the checklist.

---

## 2026-08-14 — Session tracking hook verification

**Files changed:** `scripts/session-tracking-stats.js` (new), `scripts/scorecard-hook-tally.js`, `scripts/session-tracking-store.js`, `scripts/session-tracking-html.js`, `scripts/append-session-scorecard.js`, `scripts/scorecard-navigation-path.js`; `agent docs/SESSION_TRACKING.md`; generated `session-tracking-log.html`, `session-tracking.jsonl`, `session-metrics-log.html`.

**What worked:** Hook now records an ordered `toolTimeline` (search, doc-read, read, edit). Each bump reconciles self-reported `navigationPath` against hook observations — index-first rate, unexplained searches, path coverage, active tool time. Tracking page replaced misleading duration/dead-end stats with honest aggregates and a "Where the index failed" backlog. Headless smoke test confirmed coverage pills. Overlay Creator extraction logged in `electron-toolbar/docs/sessions/SESSIONS.md`; Assignment Assistant workspace paths logged in `School Scrips/Macro App/docs/sessions/SESSIONS.md`.

**Current state:** Green — headless verify passed; no GUI tests run.

**File size flag:** None (`session-tracking-html.js` ~300 lines).

**Next session:** Watch index-first and path-coverage rates over a few sessions; add index rows from the failure backlog as patterns emerge.

---

## 2026-08-11 — Capture: handoff is a statement, never a prompt

**Files changed:** `AGENTS.md` (§ Never put anything on Chase's screen without asking), `agent
docs/rules/never-display-without-permission.md`. App code work this session (Macro App online-
course calendar matching fixes) is logged in `School Scrips/Macro App/docs/sessions/SESSIONS.md`.

**What worked:** Chase rejected an AskUserQuestion call that asked "want me to do anything else,
or are you good to check it yourself?" after a safe, non-GUI text-label fix, and said to stop
asking permission or asking him to start/verify things — ever. Captured as a tightening of the
existing "never put anything on screen without asking" rule: the launch-permission half stays
unchanged, but the handoff step (when work can't be verified headlessly) must now always be a
flat, declarative statement — never an interactive question, and no exception for low-stakes
changes he'll see next time he opens the app anyway. Added the rule to both the always-on root
`AGENTS.md` summary and the detail doc, plus a matching memory file so it persists across
sessions.

**Current state:** Green — doc-only change, no code/tests affected.

**File size flag:** None.

**Next session:** None pending.

---

## 2026-08-09 — Session tracking split (metrics vs task pathing)

**Files changed:** New `scripts/session-tracking-store.js`, `scripts/session-tracking-html.js`;
`scripts/scorecard-navigation-path.js` (+ `summarizeNavigationPath`, `formatDurationMs`);
`scripts/append-session-scorecard.js` (bump → tracking JSONL + both HTML pages); `scripts/scorecard-enforce.js`,
`scripts/serve-programs-docs.js`; `agent docs/SESSION_TRACKING.md`, `SESSION_METRICS.md`, `SESSION_SCORECARD.md`
(pointer); `AGENTS.md`, `INDEX.md`, `END_OF_SESSION.md`, `index.html`, `rules/html-delivery.md`; removed
`session-scorecards-log.html`; generated `session-tracking-log.html`, `session-metrics-log.html`,
`session-tracking.jsonl`.

**What worked:** Per-request `--bump-file` now appends a collapsible task row with ordered navigation path
(✓ helpful, ~ partial, ✗ dead-end) to `session-tracking.jsonl` and regenerates tracking HTML. Metrics finalize
writes the grep/file tally card only (`session-metrics-log.html`). Primary URL for path review:
`http://127.0.0.1:8765/session-tracking-log.html`. Chase declined auto-appending missed INDEX routes — path
tracking only, thin index + grep unchanged.

**Current state:** Green headlessly — bump/finalize scripts run; no live docs-server smoke test this wrap.

**File size flag:** None.

**Next session:** Optional backfill of older finalized sessions' `taskLog` into `session-tracking.jsonl` if
historical bumps included `navigationPath`.

## 2026-08-08 (round 4) — App Dashboard conformance pass, first of the School Scrips series

**Files changed:** New `agent docs/instructional-layer-htmls/app-dashboard-docs-review.html`
(Phase 1 report, then updated in place with the outcome once Chase made his calls); added its
card to `agent docs/index.html`. Inside `School Scrips/App Dashboard` (separate repo): deleted
`docs/REBUILD-PLAN.md`, `docs/PHASES.md`, `docs/LIFECYCLE-TRACKING-NOTES.md`,
`docs/sessions/END_OF_SESSION_CHECKLIST.md`, `guidelines/Guidelines.md` (and the now-empty
`guidelines/` folder); fixed a stale toolbar-routing claim and a broken backslash-path link in
`README.md`; removed the now-dangling pointers to the deleted files from `AGENTS.md` and
`QUICK_START.md`.

**What worked:** Ran the conformance pass per `APP_CONFORMANCE_PASS.md` — all 12 markdown files
checked against live code, not just against each other's prose. Found a real, currently-unguarded
bug: Macro App's Vite dev server and D2L Platform (Personal)'s API server both hardcode port
**5328**; `npm run audit:launch-registry` doesn't catch it because only Macro App's side is
registered in `apps.json`'s `devRouting`. Also found `README.md` directly contradicting
`LAUNCHER.md` about how the toolbar sources app paths (stale `appPaths` map claim; the real
mechanism is `school-launchers.js` reading `apps.json`). Chase then reviewed every finding for
*usefulness*, not just correctness — his call was "I don't use this app much, that plan is too
old to remember, not worth the tokens to fix the lifecycle bug" — and deleted the five docs above
rather than fixing them.

**Current state:** Green. App Dashboard now has 7 markdown files, all either verified accurate
or freshly fixed. Two findings deliberately left open: the 5328 port collision (Chase hasn't
picked which side to move) and a stale `(future)` tag on the `process` log source in
`docs/LOGGING.md`.

**File size flag:** None — this was a docs-only session.

**Next session:** Decide the 5328 collision (move Macro App's `devRouting.upstreamPort` off it,
or register D2L Personal's hardcoded API port so the audit script can see the conflict). Then
continue the School Scrips conformance-pass series — Macro App, Math App Studio, and 8 others
still to review, one at a time per `APP_CONFORMANCE_PASS.md`.

## 2026-08-08 - Quasimorph routing + local Tracker/mod work

**Files changed:** `APP_LOCATIONS.md` (added Quasimorph Tracker and Quasimorph mods rows),
`agent docs/session-scorecards.jsonl`, `agent docs/session-scorecards-log.html`; local-only work
outside root git in `Quasimorph Tracker/` and `Desktop/games/Quasimorph-GoldBerg/mod-dev/`.

**What worked:** Routed future "Quasimorph Tracker" and "Quasimorph mods" requests directly.
Built/deployed `QM_StickyTooltips` v2.2.0 for dwell-click-safe hover tooltips, and added
Tracker ship material tracking with pinned two-column commodities plus centered scroll controls.

**Current state:** Green - scorecard finalized, Tracker `npm run build` passed, StickyTooltips
`dotnet build -c Release` passed and deployed. Visible app/game smoke tests were not run.

**File size flag:** None.

**Next session:** Chase smoke-tests StickyTooltips and Tracker tracking in the live app/game;
consider initializing git for Quasimorph Tracker if it should be backed up.

## 2026-08-08 (round 3) — Recipes folder split by owning app; only 3 recipes stayed shared

**Files changed:** Moved 8 files to new `School Scrips/Math App Studio/docs/recipes/`
(`studio-dwell-latch.md`, `canvas-move-resize.md`, `animation-director-notes.md`,
`studio-design-propagation.md`, `canvas-info-block-design.md`, `edit-underlay-layer-contract.md`,
`animation-library.md`, `info-block-nav-buttons.md` — fixed two stale `.mdc` cross-references
and one double-blank-line formatting issue in the same edit), `vlc-embed-contract.md` to
`Video Player/docs/`, `school-exam-map-html.md` to `School Scrips/School documents/docs/`.
Updated pointers in `Math App Studio/AGENTS.md`, `Solving Quadratics App/AGENTS.md`,
`canvas-kit/AGENTS.md`, `Video Player/AGENTS.md`, and `School documents/README.md`.
Rewrote `agent docs/recipes/INDEX.md` (shrank from documenting ~19 recipes to 3 — everything
else now lives with its owning app) and `agent docs/instructional-layer-htmls/recipes-review.html`
per Chase's request to bring the review page current (added a "where each of the 26 ended up"
destination table, marked the original findings as pre-split historical record).

**What worked:** Chase grouped the remaining "keep as-is" recipes by owning app himself
(Math App Studio, canvas-kit, Macro App, Video Player, School documents) and asked two
clarifying questions before committing — what `click-through-windows.md` does, and whether
`school-exam-map-html.md` is current — both confirmed in the prior turn. His working
assumption was "everything left besides click-through-windows is Math App Studio's, including
canvas-kit." Grepping for real consumers caught two problems with that before any file moved:
canvas-kit is consumed by Solving Quadratics App too (9 files import it, not zero), and — the
bigger catch — `modal-shell.md` and `canvas-kit-target-size.md` are referenced from **10 and 7
apps respectively** (factoring-app, transformations-app, Matrix app, Fractions-App, App
Dashboard, Seating-Chart, Agent Browser, canvas-kit, Solving Quadratics App, and either Macro
App or Math App Studio itself), not narrowly scoped at all. Moving those two under Math App
Studio would have broken 8-9 other apps' pointers and buried a genuinely universal convention
in one app's folder. Held both back in the shared folder and flagged the finding instead of
executing the move silently. The other 8 real Math-App-Studio/canvas-kit files and the 2
single-consumer files (Video Player, School documents) had no such fan-out — confirmed via the
same grep-for-consumers method before moving, not assumed.

**Current state:** All moves verified — `check-docs.js` clean, no stale references to the 10
moved/deleted filenames found tree-wide outside expected historical records (old PROJECT_SYNOPSIS.md
staleness pre-dating this session, noted but out of scope; doc-restructure-plan.html's illustrative
example, same).

**File size flag:** None. `agent docs/recipes/INDEX.md` trimmed from ~197 to ~176 lines despite
documenting three rounds of reorg — still over its own ~150 budget but judged acceptable for
a doc explaining a one-time structural change.

**Next session:** `agent docs/recipes/` is down to 3 interaction recipes + the 6 code-standards
docs. Worth a fresh look at whether "recipes" is still the right name for a folder that's mostly
`CODING_STANDARDS.md` and friends now that the interaction patterns have scattered to their
owning apps. `dwell-activation.md`'s possible rename is still deferred at Chase's own call.

---

## 2026-08-08 — Recipes review resolved: real-usage triage, not just doc accuracy

**Files changed:** Built `agent docs/instructional-layer-htmls/recipes-review.html` — a
doc-vs-code accuracy pass across all 26 interaction recipes in `agent docs/recipes/` (three
parallel agents, each opening every named exemplar file rather than trusting the recipe's own
prose). 12 of 26 came back needing a fix. Chase then walked through those 12 himself and
reclassified several by whether he actually retrieves them as recipes, not just whether they're
accurate. Outcome: `move-to-cursor.md` and `state-machine.md` deleted (`agent docs/recipes/`,
`electron-toolbar/modules/move-to-cursor.md` tombstone also removed). `scroll-calculation.md`,
`dwell-click.md`, `dwell-drag.md`, `dwell-countdown.md`, `toolbar-system.md` moved to
`electron-toolbar/docs/` with their stale numbers fixed in the same edit. `hover-to-lock-drag.md`,
`mouse-hover-detection.md`, `dwell-activation.md`, `modal-shell.md` (514→257 lines),
`canvas-kit-target-size.md` reworked in place in `agent docs/recipes/`. Updated
`agent docs/recipes/INDEX.md` (7 rows removed, pointers added to the new `electron-toolbar/docs/`
homes), `electron-toolbar/AGENTS.md` (keyword table repointed, known-gaps section updated), and
cross-references in `toggle-pattern.md` / `mouse-hover-detection.md` that pointed at deleted or
moved files. `recipes-review.html` and its `agent docs/index.html` card marked resolved.

**What worked:** Doc-accuracy triage alone would have kept all 12 in place, just fixed. Chase's
own read reframed the actual question — several of these were never "recipes" he retrieves, just
captures of how his own dwell overlay works ("I don't use them as recipes, I just captured how
they worked"). Distinguishing "accurate but never referenced" (→ move to the one app it
documents) from "accurate and heavily used" (→ keep, just fix) from "not even real" (→ delete)
required his judgment, not just the code check — the code check correctly found 0 dead exemplars
across all 26, so nothing here was catchable by `check-docs.js` or a second doc-vs-code pass
alone. One real bug caught along the way: `hover-to-lock-drag.md`'s own "mistake this recipe
exists to prevent" callout (DOM hover events never fire on click-through overlays) was
contradicted by a live `mouseenter` listener in its own third exemplar file — softened to "check
per-window, don't assume" rather than an absolute claim.

**Current state:** Round 1 verified clean — `check-docs.js` 0 dead links / 0 bare values / 0
recipe values, no stale references found tree-wide except expected historical records.

**File size flag:** None over cap. `modal-shell.md` cut from 514→257 lines;
`toolbar-system.md` cut from 652→243 lines during its move to `electron-toolbar/docs/`.

---

**Round 2, same day:** Chase started reviewing the 14 "keep as-is" recipes and immediately
found the same real-usage question applied there too — not "should this be a recipe at all"
this time, but "is this actually in the right shared folder." He grouped the remaining files
by owning app (Math App Studio, canvas-kit, Macro App, Video Player, School documents) and
asked to confirm two things: what `click-through-windows.md` actually does, and whether
`school-exam-map-html.md` is current. Both confirmed — click-through-windows.md is
electron-toolbar (overlay ignores clicks except over specific regions), and
school-exam-map-html.md's exemplars (`exam2-review-map.html`, `exam3-homework-map.html`) were
both modified today, so it's live, not stale (it's a recurring per-exam-cycle tool, not a
one-off page).

While answering, found that his assumption "everything else is Math App Studio" was wrong on
two counts: `modal-shell.md` is actually Macro App (its exemplars — `ModalContainer.tsx`,
`ModalPortal.tsx`, `ViewportScrollFrame.tsx` — are all Macro App, not Studio), and canvas-kit
turned out to be a shared library consumed by **two** apps, not one — grepped for canvas-kit
imports and found 9 files in `Solving Quadratics App` alongside the Math App Studio ones. Also
found 6 more files that were exactly like the first round's electron-toolbar batch
(`click-through-windows.md`, `dwell-activation.md`, `hover-to-lock-drag.md`,
`mouse-hover-detection.md`, `toggle-pattern.md`, `window-positioning.md`) — internal to that
app, not cross-app patterns — which Chase confirmed moving. Executed that move: files relocated
to `electron-toolbar/docs/`, cross-references between them simplified now that they're
siblings again, the dead `hover-to-key-press.md` reference in `click-through-windows.md`
removed (that file was deleted 2026-08-02), `electron-toolbar/AGENTS.md` keyword table and
known-gaps section updated, `agent docs/recipes/INDEX.md` restructured (the now-empty
"Overlays and windows" / "Hover and scroll" sections collapsed into one note), and a genuinely
stale inbound pointer fixed in `electron-toolbar/modules/overlays/README.md` (still said
`electron-app/patterns/`, a path retired 2026-08-02, predating this session entirely).

**`agent docs/recipes/` no longer has any electron-toolbar-specific recipes.** What's left:
`studio-dwell-latch.md` + `canvas-move-resize.md` (Math App Studio only),
`canvas-info-block-design.md` + `canvas-kit-target-size.md` + `edit-underlay-layer-contract.md`
+ `animation-library.md` + `info-block-nav-buttons.md` (canvas-kit, shared by Studio and
Solving Quadratics App — Chase's call: keep filed as canvas-kit's own, folded under Math App
Studio's home since that's where he thinks of it, not split further), `modal-shell.md` (Macro
App), `vlc-embed-contract.md` (Video Player), `school-exam-map-html.md` (School documents),
`tutorial-flash-vocabulary.md` (genuinely cross-app — 5 independent live math apps share the
CSS class), plus `animation-director-notes.md` + `studio-design-propagation.md` (Math App
Studio). **Not yet moved** — Chase confirmed the electron-toolbar batch only; the
Math-App-Studio/canvas-kit/Macro-App/Video-Player/School-documents moves are proposed, not
executed.

**Next session:** Execute the remaining moves once Chase confirms scope: Math App Studio's own
recipes folder (4 files, or 9 if canvas-kit folds in as he leans toward), Macro App gets
`modal-shell.md`, Video Player gets `vlc-embed-contract.md`, School documents gets
`school-exam-map-html.md` (target: `School Scrips/School documents/docs/`, which doesn't exist
yet). `tutorial-flash-vocabulary.md` — genuinely cross-app, probably the one file that should
stay in the shared `agent docs/recipes/` folder rather than move anywhere. Re-run
`check-docs.js` and the stale-reference grep after any further move, same as this round.
`dwell-activation.md`'s possible rename still deferred at Chase's own call.

---

## 2026-08-07 — Full agent docs/ + cursor-patterns/ review; cursor-patterns/ eliminated

**Files changed:** Reviewed all 12 `agent docs/` files and all 17 `cursor-patterns/` files
file-by-file (two new HTML reviews under `agent docs/instructional-layer-htmls/`, plus 7
per-file detail pages under `.../cursor-patterns/`). Built the original scorecard
Stop/PreCompact enforcement in `scripts/scorecard-enforce.js` +
`.claude/settings.json` (later extended to Cursor/Codex by the entry below). Then, at
Chase's direction, eliminated `cursor-patterns/` as a folder entirely: `accessibility-patterns.md`
(606→21 lines) and `dwell-and-head-mouse.md` (175→~25 lines) gutted to keep only what he
confirmed mattered (no-backdrop-dismiss modal rule, real overlay code pointers);
`electron-per-monitor-display-scaling.md` deleted outright, no merge, after Chase reported
its per-monitor memory never reliably worked even in Macro App; 6 dead archive stubs deleted;
`CODING_STANDARDS.md`, `INIT_NEW_APP.md`, `file-headers.md`, `react-patterns.md`,
`refactoring-checklist.md`, `anti-patterns.md` moved into `agent docs/recipes/` (which itself
moved from `Programs/recipes/`). Rewrote path references across ~60 files in Programs root
plus ~16 sibling app repos (each committed separately, see their own `SESSIONS.md`/commit log).
Fixed a real bug in `scripts/check-docs.js`: its own hardcoded `SECOND_TIER_INDEXES` and the
`RECIPE VALUES` check still pointed at the pre-move paths, silently checking nothing.

**What worked:** The review process itself caught real problems the fast way — reading each
file against what actually exists on disk rather than trusting the prose. Concrete finds:
`dwell-and-head-mouse.md` claimed an "always-on AGENTS.md short form" that was deleted
2026-08-05 (false — nothing routed to it anymore); `CODING_STANDARDS.md`'s own launcher
section, initially flagged as a duplicate of `App Dashboard/docs/LAUNCHER.md`, turned out to be
the canonical source that `LAUNCHER.md` itself defers to (caught before a wrong edit).
Chase's core objection, once he walked through `dwell-and-head-mouse.md` and
`accessibility-patterns.md` section by section: most of it was AI-generated documentation from
years ago describing needs he doesn't have (keyboard nav, screen readers, invented timing
values) rather than the one thing he actually uses (electron-toolbar's real overlay/dwell
mechanism). Used Plan mode for the folder elimination given the ~100-file blast radius across
15+ separate git repos — researched via two parallel Explore agents first (recipe inventory +
reference count), then a written plan before touching anything.

**Current state:** Green — `check-docs.js`: 0 dead links, 98/99 unrouted (at, not over, the
pre-existing ratchet), 0 recipe-values violations. All 17 doc/detail HTML pages re-verified
serving after a docs-server restart (had gone down independent of this work).

**File size flag:** None over cap. `agent docs/recipes/` is now ~34 files flat — see Next session.

**Next session:** Chase wants the merged `agent docs/recipes/` folder sorted into topic
subfolders (dwell/overlay, canvas UI, code standards, etc.) — deliberately deferred, not
started. Also worth checking: `agent docs/instructional-layer-htmls/cursor-patterns-review.html`
and its 7 per-file detail pages are now historical record only (folder they describe is gone);
fine to leave as-is, but don't treat them as a current map.

---

## 2026-08-07 — Scorecard Stop hooks for Cursor + Codex; cross-agent hook parity

**Files changed:** `.cursor/hooks.json` (added `stop`, `preCompact`, `beforeSubmitPrompt` — Cursor had only `postToolUse` tally before, so agents could finish with edits and zero bumps); `.codex/hooks.json` (new — same Stop/PreCompact/tally wiring for Codex project hooks); `.gitignore` (track `.codex/hooks.json`); `scripts/scorecard-enforce.js` (also emits `followup_message` for Cursor native stop format); `scripts/scorecard-hook-tally.js` (`beforeSubmitPrompt` turn counting); `agent docs/SESSION_SCORECARD.md` (§ Enforcement table for Cursor / Claude Code / Codex). Also in this repo commit batch: prior-session instructional-layer edits still dirty (`INSTRUCTION_LAYER_AUDIT.md`, `END_OF_SESSION.md`, review HTMLs, `append-session-scorecard.js`, `.claude/settings.json`).

**What worked:** Chase noticed Cursor only auto-tallied tool use — the Claude Code **Stop** hook that blocks finishing without a `--bump-file` never ran in Cursor. Root cause: enforcement lived only in `.claude/settings.json`. Wired the same `scripts/scorecard-enforce.js --stop` / `--precompact` into native `.cursor/hooks.json` (`loop_limit: 3`) and new `.codex/hooks.json` (Codex trusted-project hooks). Documented all three agents in one table so the gap doesn't recur. Separate Macro App work this session (AA download double save dialog + workspace history on Google Drive) logged in `School Scrips/Macro App/docs/sessions/SESSIONS.md`.

**Current state:** Green headlessly — hook scripts smoke-test clean. **Not live-verified:** Cursor needs restart to reload hooks; Codex needs one-time `/hooks` trust after pull; Stop-hook block behavior not exercised in GUI this session.

**File size flag:** None.

**Next session:** After pull on laptop: restart Cursor, trust Codex hooks once, confirm a session with ≥2 file edits and 0 bumps gets blocked at turn end. Consider extending `unbumpedState()` with "time since last bump" if long sessions go quiet after one early bump.

---

## 2026-08-05 — Index-tree Stage A, AGENTS.md 307→218 lines, scorecard hook wired for Claude Code

**Files changed:** `agent docs/INDEX.md` (new, ~25 rows, pure delegation), `AGENTS.md` (307→218,
§ Where rules live deleted, § Dwell & head-mouse deleted at Chase's call, § Windows launchers
widened to cover both launcher surfaces, § End-of-Session moved to `agent docs/END_OF_SESSION.md`,
precedence sentence restored after Codex dropped it), `agent docs/recipes/README.md`→`agent docs/recipes/INDEX.md` and
`cursor-patterns/README.md`→`agent docs/recipes/INDEX.md` (renamed via `git mv`, ~35 inbound refs
updated), `scripts/check-docs.js` (340→418 lines — index coverage + broken-chain checks, ratchet
armed at 99/99), `scripts/scorecard-hook-tally.js` (Claude Code tool names + automatic turn
counting added), `.claude/settings.json` (new — `PostToolUse`/`UserPromptSubmit` hooks, tracked
so it syncs to the laptop like `.cursor/hooks.json` already did), `agent docs/rules/html-delivery.md`
and `multi-repo-git-push.md` (corrected stale `docs/` folder reference; documented the
`.gitignore`-doesn't-untrack lesson from the electron-toolbar collision), `agent docs/index.html` +
`instructional-layer-htmls/` (new — durable-vs-scratch HTML split, front door at `/`),
`Macro App/docs/modal-redesign-queue.md` (+1 finding), `electron-toolbar/docs/LAUNCHER_PANEL.md`
(+launcher pointer). 12 sibling repos synced (doc-pointer rename); electron-toolbar's runtime
state files untracked in two passes (`scroll_config.txt`/`scroll_position.json`/`scroll_state.json`/
`dwell_persisted_settings.json`, then 4 more) after they blocked a push.

**What worked:** Built the index tree's trunk — `agent docs/INDEX.md` delegates to
`APP_LOCATIONS.md`, `agent docs/recipes/INDEX.md`, `agent docs/recipes/INDEX.md`, and app `AGENTS.md` files
rather than listing their contents, so adding a recipe or standard never touches the master index.
Walked AGENTS.md section by section with Chase, cutting or relocating anything that only fires on
a trigger phrase; found and fixed a real bug in the process — the "never a visible console"
launcher rule was scoped `(School Scrips)` and so silently didn't cover electron-toolbar's
Launcher Panel, which Chase uses just as often. Wired the Claude Code scorecard hook that never
existed (Cursor had `.cursor/hooks.json`, Claude Code had nothing — the agent wasn't forgetting to
bump, there was no mechanism), and made turn-counting automatic via `UserPromptSubmit`. Reviewed
Chase's continuation of this work with Codex: verified the orchestrator-rule generalization and
the gitignore fix both survived, caught and restored one real content loss (the app-AGENTS.md
precedence sentence), confirmed a "third time" escalation trigger moved to the capture skill
rather than being lost. Ran end-of-session across Programs root + Macro App + electron-toolbar.

**Current state:** Green — `check-docs.js` exit 0, 0 dead links, 0 broken chain, 99/99 unrouted
(ratchet unchanged this session).

**File size flag:** None — `check-docs.js` itself is at 418 lines (700 is the extract line).

**Next session:** Run the 10-phrase routing drill (listed in the plan) via cold subagents before
trusting the deleted § Where rules live section — it was removed same-day rather than after the
week-long soak the plan called for. Then continue Stage 2 (cursor-patterns merit review, ~100
sections) at `C:\Users\chase\.claude\plans\alright-so-what-i-deep-iverson.md`.

---

## 2026-08-02 — Retired `.mdc`, built `agent docs/recipes/`, AGENTS.md rollout to 19 apps

**Files changed:** `agent docs/recipes/` (new — 25 recipes + README index), `AGENTS.md`, `CLAUDE.md`,
`HOW_TO_INTERACT_WITH_AI.md`, `APP_LOCATIONS.md`, `.gitignore` (allowlist `/agent docs/recipes/`),
`.claude/skills/capture/SKILL.md` (steps 1–5), `scripts/check-docs.js` (+`RECIPE VALUES` check),
`agent docs/rules/` (new — 5 docs), `agent docs/INSTRUCTION_LAYER_AUDIT.md` (+§ 2f-2),
`agent docs/APP_CONFORMANCE_PASS.md` (§ A), `agent docs/AGENT_SETUP_FOR_PEER_REVIEW.md`,
`cursor-patterns/README.md` + `modal-pattern.md` (tombstone), 19 apps' `AGENTS.md` + `CLAUDE.md`,
`electron-toolbar/docs/LAUNCHER_PANEL.md` + `WINDOW_DETECTION_GUIDE.md`,
`Monitor Configuration App/docs/` (4), `spire-overlay/docs/`, `sts2-dwell-targeting/docs/`,
`School Scrips/Matrix app/docs/MATRIX_APP_GUIDE.md`.

**What worked:** Every `.cursor/rules/*.mdc` in the tree is gone except frozen Calendar 2.0.
Three scattered pattern libraries (`electron-toolbar/electron-app/patterns/`, Math App Studio's
9 rules, canvas-kit + Video Player) consolidated into **one** `Programs/agent docs/recipes/` folder with a
single index whose rows are keyed on **"You might say"** — Chase's words, not technical names.
Root went from 10 rules → 0 and 7 loose markdowns → 4. Capture ladder rung 3 rewritten: a recipe
or a keyword row, not a glob rule. Every app now has `AGENTS.md` (content) + a 3-line `CLAUDE.md`
(`@AGENTS.md`), so Cursor / Claude Code / Codex land on the same text.

Recipe audit against live code: deleted 3 obsolete (874 lines) — `overlay-exclusion-zones`
(never implemented) and `hover-to-key-press` / `continuous-key-press` (documented
`modules/arrow_module.py`, removed in commit `e98301b "Interface 2.0"`). Fixed the
`mouseenter`-on-a-click-through-window trap in `hover-to-lock-drag`. All 25 survivors anchored
to verified exemplar paths.

**Found and fixed:** recipes carried hardcoded timings and three were **wrong** —
`DWELL_TIME = 600` (real `0.3`, persisted `250 ms`), `DRAG_RELEASE_TIME = 1.0` (real `0.75`),
`MOVEMENT_THRESHOLD = 10` (real `15`). They hid inside code fences, which the bare-value check
deliberately skips. That exemption was correct for `.mdc` rules and wrong for recipes, which get
**copied**. All tunables now name their constant; `check-docs.js` gained a `RECIPE VALUES` check
that reads `dwell_constants.py` and fails if a number returns.

**Design decision (Chase):** the recipe folder is **not** getting an always-on `AGENTS.md` line.
It costs tokens every session, most sessions aren't building a tool, and the memory load is one
folder name he's already thinking about when he asks. The periodic audit keeps it honest instead.
Captured in the capture skill so it isn't re-proposed.

**Current state:** Green — `check-docs.js`: 0 bare values · 0 recipe values · 0 stale plans.
2 dead links and 3 unindexed rules remain, all pre-existing (Hearthstone README, App Dashboard,
frozen Calendar 2.0).

**File size flag:** None. Largest recipe `toolbar-system.md` ~650 lines (index budget says aim
under 300 — flagged in `agent docs/recipes/README.md`, not enforced).

**Next session:** Chase's electron-toolbar / dwell pass — rewrite the key-press recipe from
`coordinator/arrow_handlers.py` + `arrow-manager.js`, and add a **toolbar-module-lifecycle**
recipe for the `coordinator/` layer (`module_registry.py`, `module_supervisor.py`,
`module_lifecycle.py`), which no recipe covers. Also pending: `DisplayProfileManager-main`,
`Hearthstone Overlay 3.0`, `Quasimorph Tracker` still have full `CLAUDE.md` and no `AGENTS.md`;
8 boilerplate `guidelines/Guidelines.md` awaiting his one-by-one pass; `dwell-and-head-mouse.md`
vs `accessibility-patterns.md` overlap unresolved.

## 2026-08-01 — Capture ladder learning, audit doc, session scorecard HTML log

**Files changed:** `docs/SESSION_SCORECARD.md`, `docs/INSTRUCTION_LAYER_AUDIT.md`, `docs/context-engineering-capture-costs.html` (+ guide boxes), `scripts/append-session-scorecard.js`, `docs/session-scorecards-log.html`, `docs/session-scorecards.jsonl`, `AGENTS.md` (end-of-session scorecard step), `.cursor/rules/html-infographic-delivery.mdc` (write-only scorecard note). Conversation also refined capture ladder mental models (rungs 1–5, 3 vs 5, robot vs AI audit).

**What worked:** Instruction layer audit doc (rung 5, no AGENTS pointer). Session scorecard wired to end-of-session — agents append via script, never read HTML log. First scorecard entry on dry-run wrap. Page 3 capture-costs expanded with good-for / don't-abuse per rung.

**Current state:** Green — scorecard pipeline live; `docs/` still to be renamed `agent-docs` by Chase when ready.

**File size flag:** None over 500 in new scripts/docs.

**Next session:** Rename `docs/` → `agent-docs` and update paths; build scorecard baseline over next weeks; optional Programs meta allowlist for `scripts/` and `docs/`.
