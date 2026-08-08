# Programs workspace — session log

Instruction-layer and cross-app work at `Programs/` root (not inside a single School Scrips app).

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
