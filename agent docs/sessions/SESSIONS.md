# Programs workspace — session log

Instruction-layer and cross-app work at `Programs/` root (not inside a single School Scrips app).

## 2026-08-05 — Index-tree Stage A, AGENTS.md 307→218 lines, scorecard hook wired for Claude Code

**Files changed:** `agent docs/INDEX.md` (new, ~25 rows, pure delegation), `AGENTS.md` (307→218,
§ Where rules live deleted, § Dwell & head-mouse deleted at Chase's call, § Windows launchers
widened to cover both launcher surfaces, § End-of-Session moved to `agent docs/END_OF_SESSION.md`,
precedence sentence restored after Codex dropped it), `recipes/README.md`→`recipes/INDEX.md` and
`cursor-patterns/README.md`→`cursor-patterns/INDEX.md` (renamed via `git mv`, ~35 inbound refs
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
`APP_LOCATIONS.md`, `recipes/INDEX.md`, `cursor-patterns/INDEX.md`, and app `AGENTS.md` files
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

## 2026-08-02 — Retired `.mdc`, built `recipes/`, AGENTS.md rollout to 19 apps

**Files changed:** `recipes/` (new — 25 recipes + README index), `AGENTS.md`, `CLAUDE.md`,
`HOW_TO_INTERACT_WITH_AI.md`, `APP_LOCATIONS.md`, `.gitignore` (allowlist `/recipes/`),
`.claude/skills/capture/SKILL.md` (steps 1–5), `scripts/check-docs.js` (+`RECIPE VALUES` check),
`agent docs/rules/` (new — 5 docs), `agent docs/INSTRUCTION_LAYER_AUDIT.md` (+§ 2f-2),
`agent docs/APP_CONFORMANCE_PASS.md` (§ A), `agent docs/AGENT_SETUP_FOR_PEER_REVIEW.md`,
`cursor-patterns/README.md` + `modal-pattern.md` (tombstone), 19 apps' `AGENTS.md` + `CLAUDE.md`,
`electron-toolbar/docs/LAUNCHER_PANEL.md` + `WINDOW_DETECTION_GUIDE.md`,
`Monitor Configuration App/docs/` (4), `spire-overlay/docs/`, `sts2-dwell-targeting/docs/`,
`School Scrips/Matrix app/docs/MATRIX_APP_GUIDE.md`.

**What worked:** Every `.cursor/rules/*.mdc` in the tree is gone except frozen Calendar 2.0.
Three scattered pattern libraries (`electron-toolbar/electron-app/patterns/`, Math App Studio's
9 rules, canvas-kit + Video Player) consolidated into **one** `Programs/recipes/` folder with a
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
under 300 — flagged in `recipes/README.md`, not enforced).

**Next session:** Chase's electron-toolbar / dwell pass — rewrite the key-press recipe from
`coordinator/arrow_handlers.py` + `arrow-manager.js`, and add a **toolbar-module-lifecycle**
recipe for the `coordinator/` layer (`module_registry.py`, `module_supervisor.py`,
`module_lifecycle.py`), which no recipe covers. Also pending: `DisplayProfileManager-main`,
`Hearthstone Overlay 3.0`, `Quasimorph Tracker` still have full `CLAUDE.md` and no `AGENTS.md`;
8 boilerplate `guidelines/Guidelines.md` awaiting his one-by-one pass; `dwell-and-head-mouse.md`
vs `accessibility-patterns.md` overlap unresolved.

## 2026-08-02 — exam2-review-map: full homework harvest + Exam 2 Review

**Files changed:** `agent docs/exam2-review-map.html` (~721 lines), `School Scrips/Macro App/docs/PEARSON_BROWSER_AUTOMATION.md`

**What worked:** Pearson print harvest (Macro App MCP, no snapshots) for homework 3.6–3.10 and Exam 2 Review. Trimmed map to homework 3.3–3.10 only; updated REVIEW to edited 18-question list; added six review-only PROBLEMS (3.3.63, 3.5.25, 3.5.59, 3.7.23, 3.9.36, 3.9.75); right-panel hover tooltips; tooltip wrap fix for long equations.

**Current state:** Green — map complete for current review/homework set.

**File size flag:** None

**Next session:** Serve at `http://127.0.0.1:8765/exam2-review-map.html`; optional fix for parameterized IDs showing homework vs review instance text.

## 2026-08-02 — exam2-review-map: 3.4/3.5 problem text + collapsible sections

**Files changed:** `agent docs/exam2-review-map.html` (~660 lines)

**What worked:** Added 16 + 14 Pearson print-harvested `{ prompt, expr }` entries (3.4, 3.5). Fixed homework accordion — second click on open section collapses it and clears right panel.

**Current state:** Green

**File size flag:** None

**Next session:** Serve via docs server; continue PROBLEMS harvest for 3.6+

## 2026-08-01 — Capture ladder learning, audit doc, session scorecard HTML log

**Files changed:** `docs/SESSION_SCORECARD.md`, `docs/INSTRUCTION_LAYER_AUDIT.md`, `docs/context-engineering-capture-costs.html` (+ guide boxes), `scripts/append-session-scorecard.js`, `docs/session-scorecards-log.html`, `docs/session-scorecards.jsonl`, `AGENTS.md` (end-of-session scorecard step), `.cursor/rules/html-infographic-delivery.mdc` (write-only scorecard note). Conversation also refined capture ladder mental models (rungs 1–5, 3 vs 5, robot vs AI audit).

**What worked:** Instruction layer audit doc (rung 5, no AGENTS pointer). Session scorecard wired to end-of-session — agents append via script, never read HTML log. First scorecard entry on dry-run wrap. Page 3 capture-costs expanded with good-for / don't-abuse per rung.

**Current state:** Green — scorecard pipeline live; `docs/` still to be renamed `agent-docs` by Chase when ready.

**File size flag:** None over 500 in new scripts/docs.

**Next session:** Rename `docs/` → `agent-docs` and update paths; build scorecard baseline over next weeks; optional Programs meta allowlist for `scripts/` and `docs/`.
