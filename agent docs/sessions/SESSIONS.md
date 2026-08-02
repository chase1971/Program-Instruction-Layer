# Programs workspace — session log

Instruction-layer and cross-app work at `Programs/` root (not inside a single School Scrips app).

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
