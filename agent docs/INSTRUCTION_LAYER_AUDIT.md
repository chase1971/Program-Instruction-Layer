# Instruction layer audit

> **Rung 5 — on demand only.** Not in AGENTS, not always-on.  
> **Where:** `Programs/agent docs/INSTRUCTION_LAYER_AUDIT.md` (whole workspace — rules, docs, pointers — **not one app**; for a single app see `APP_CONFORMANCE_PASS.md`).  
> **Find it:** grep “instruction layer audit” or “duplicate contradictions audit” when Chase asks to run the periodic doc cleanup.  
> **Trigger examples:** “Run the audit doc” / “find the doc that cleans up duplicate or contradictory rules and docs” / “periodic instruction cleanup”

---

## What this is for

Periodic cleanup of **rules, AGENTS pointers, and instruction docs** — things a dumb script cannot judge:

- Same topic documented in two places
- Contradictory guidance (overlay, modals, HTML links, Pearson, etc.)
- Stale course/task docs
- Rules on the wrong rung (always-on bloat, encyclopedia in a glob rule)
- Orphans flagged by the robot — merge, link, or archive

**Not for:** normal feature work, every end-of-session, or code refactors outside the instruction layer.

---

## Open questions — parked by Chase, decide later

> Deliberately deferred during the 2026-08-04 index restructure. These are **not** rot to
> clean up silently — each one needs Chase's judgment. Raise them when he next runs an audit.

| # | Question | Why it's parked | What decides it |
|---|---|---|---|
| 1 | **CourseAgent** — 38 docs, no `AGENTS.md`, 36 unreachable. Currently in `COVERAGE_EXEMPT` in `scripts/check-docs.js` | Chase hasn't looked at what's in there and didn't want to deal with it during the restructure | He reviews the contents, pulls out anything worth keeping, then: give it a keyword table, or move it to `Deprecated apps/`. It is ~25% of the whole coverage gap, so this moves the number more than any other single call |
| ~~2~~ | ~~Three dwell timings disagree~~ — **moot, 2026-08-07** | Chase reviewed `dwell-and-head-mouse.md` and said he doesn't want per-app timing documented in markdown at all — dwell speed is controlled through the toolbar's own settings, and each app legitimately differing is fine. The file was cut to a pointer table (real code paths only); no timing values live in a doc anymore | Resolved by removing the thing the question was about |
| 3 | **Re-split `agent docs/recipes/` into narrower topic subfolders** | `cursor-patterns/` was merged flat into `recipes/` 2026-08-07 (Chase: "get rid of these cursor patterns" — no functional distinction once `.mdc` retired). Chase wants finer buckets so the ~34-file flat folder isn't one big list, but explicitly deferred the split to a future session | His review of what's actually in the merged folder |
| 4 | **Apps with real docs but no `AGENTS.md`** — `makeup-exam-standalone` (15 docs), `Statistics app` (5), `logic-app` (4), `Probability App` (4), `Hearthstone Overlay 3.0` (3) | Each missing file is a hole in the second tier. Adding five is a bigger project than the restructure itself | Whether those apps are still live enough to earn a keyword table |

| ~~5~~ | ~~The session scorecard doesn't fire~~ — **resolved 2026-08-07** | Chase reported a full session (2026-08-06) with real edits and zero bumps — proof the always-on prose instruction alone doesn't reach the agent reliably, prose can't force compliance | Redesigned the mechanism instead of rewording it again: `scripts/scorecard-enforce.js` adds a **Stop hook** that blocks the agent's turn from ending when the running tally shows edited files but zero bumps (capped at 3 consecutive blocks, then force-allows — can't loop forever), plus a non-blocking **PreCompact hook** that reminds the agent to bump right before compaction, since the disk-based tally survives compaction but the agent's memory that it needs to bump does not. Both wired in `.claude/settings.json`. See `SESSION_SCORECARD.md` § Enforcement. **Known gap:** only catches "never bumped all session" — a session that bumps once early then goes quiet for the rest of a long session won't re-trigger. Worth a follow-up if that pattern shows up |

**Note on #2:** `accessibility-patterns.md`'s 500ms figures were fixed separately — every source
agrees those match nothing that ships, so correcting them needed no judgment call.

---

## Cadence

| Run audit when… | Skip when… |
|-----------------|------------|
| Every few months (calendar habit) | `check-docs` clean and nothing feels wrong |
| Chase says “I don’t know if I already made a rule for this” | Right after a small single capture |
| After a burst of “capture that” / “remember” sessions | Frozen apps only — see skip list below |

---

## Phase 0 — Robot first (required)

From Programs root:

```powershell
node scripts/check-docs.js
```

Record the summary line: dead links · duplicate sets · unindexed rules · bare values · orphans.

| Finding | Robot can fix alone? | This audit |
|---------|----------------------|------------|
| Dead links | Often yes — fix paths or remove links | Confirm fix, don’t leave broken |
| Byte-identical duplicates | Yes — delete one copy, keep canonical | Pick which path is canonical |
| Unindexed `.mdc` | Yes — add row to AGENTS/CLAUDE | Verify glob/description make sense |
| Bare values | Yes — replace the number with the constant's name | Confirm the constant is the real owner |
| Orphans | Partially — link or tombstone | **Judgment:** keep, merge, or archive |
| Contradictory / same-topic-two-docs | **No** | **Phase 2** |

Do **not** skip Phase 0. Fix dead links before semantic review.

Optional strict pass (only if Chase asked to block on findings):

```powershell
node scripts/check-docs.js --strict
```

---

## Phase 1 — Scope (what to scan)

**In scope**

- `AGENTS.md`, `CLAUDE.md`, `APP_LOCATIONS.md`, `HOW_TO_INTERACT_WITH_AI.md`
- **`agent docs/recipes/` + `agent docs/recipes/INDEX.md`** — see § 2f-2 (absorbed `cursor-patterns/` 2026-08-07)
- `agent docs/rules/*.md`, `agent docs/*.md`, `agent docs/*.html`
- Per-app: `AGENTS.md`, `CLAUDE.md`, `guidelines/Guidelines.md`, `docs/*_INTEGRATION.md`

> **`.cursor/rules/*.mdc` no longer exist** outside frozen Calendar 2.0 (retired
> 2026-08-02). If you find one, it is either frozen-app history or something a session
> wrongly recreated — flag it.

**Out of scope unless Chase names it**

- `School Scrips/Calendar 2.0/` — **frozen** (`agent docs/rules/frozen-apps.md`)
- `Archived markdowns/` — history only; do not treat as current
- `Deprecated apps/`
- App **source code** (renderer, electron, python modules) — unless the audit finds a doc that wrongly duplicates code comments

**Skip**

- `node_modules`, build output, vendored trees, session logs unless they duplicate instruction content

---

## Phase 2 — AI judgment (what the robot cannot do)

Work topic-by-topic. For each area, grep for related keywords before concluding “nothing duplicate.”

### 2a — Same topic, two homes

Look for pairs like:

- Two HTML delivery writeups
- Two Pearson “start here” docs
- Same rule in AGENTS **and** a long always-on `.mdc` **and** a cursor-patterns doc

**Action:** One canonical home. Merge into the winner; delete or tombstone the loser. Update pointers (AGENTS, rung 3 rules, Task Index rows). **Graduating rungs requires deleting the lower copy** (capture ladder rule).

### 2b — Contradictions

Compare guidance that should agree:

- Modal size, scroll, backdrop dismiss
- HTML: `http://127.0.0.1:8765/…` vs `C:\` paths vs `.bat` openers
- Dwell/head-mouse timing and hover-only UI
- Git/end-of-session vs one-off chat habits

**Action:** Chase decides if unclear. Default: prefer **newer explicit capture** + **exemplar in repo** over stale prose. Mark outdated sections with a one-line tombstone at top: `> Superseded by … — kept for history until archived.`

### 2c — Stale course / task docs

Pearson flows, exam maps, semester-specific HTML — still accurate?

**Action:** Update in place, archive to `Archived markdowns/`, or add “as of YYYY-MM” at top. Do not leave wrong recipes indexed.

### 2d — Wrong rung

| Symptom | Likely fix |
|---------|------------|
| Huge prose in always-on `.mdc` | Demote to glob rule + rung 5 doc |
| Universal habit only in a doc | Thin rung 4 or AGENTS one-liner — not encyclopedia in rung 5 alone |
| AI-behavior note cast as code change | Demote from rung 1; use rung 3 + AGENTS |
| Chat-only habit with no pointer | Add AGENTS one-liner or rung 3 “read X first” |

Count always-on `.mdc` lines (budget ~200 total). Report if over ~250.

### 2e — Orphans from Phase 0

For each orphan listed by `check-docs`:

- **Keep** → link from AGENTS, CLAUDE rules table, or owning `*_INTEGRATION.md`
- **Merge** → fold into canonical doc, delete orphan
- **Archive** → move to `Archived markdowns/` with reason in commit message

### 2f — AGENTS bloat

AGENTS loads every chat (~4k–8k tokens whole file).

**Action:** Trim long procedures to rung 5 docs; leave index rows + pointers. Do not duplicate always-on rule text in AGENTS.

### 2f-2 — The recipe library (`Programs/agent docs/recipes/`)

Added 2026-08-02, when three scattered pattern libraries were consolidated into one
folder. Because everything is now in **one place**, this pass is cheap — do it every
audit, and do it before § 2g.

| Check | How | Action |
|---|---|---|
| **Index row exists** | Every `agent docs/recipes/*.md` appears in a table in `agent docs/recipes/INDEX.md` | A recipe no table names is invisible — add the row or archive the file |
| **"You might say" is in his words** | Read the header line. Is it the *technical* name or what Chase would actually say? | Rewrite in his words. This line is the whole trigger |
| **Duplicate recipes** | Two files covering one interaction (e.g. two drag recipes) | Merge into the one with working exemplars; tombstone the loser |
| **Exemplar paths still exist** | Open each path in the header block | Fix or mark the recipe stale. A recipe pointing at a deleted file is worse than none |
| **Status marks honest** | ✅ / ⚠️ / ❌ against what the code actually does | The 2026-08 import carried two known-bad recipes; do not let more accumulate silently |
| **Bare values crept in** | Grep the folder for timings and pixel sizes | Replace with the **constant's name**. Values live in `dwell-and-head-mouse.md` and `dwell_constants.py` only |
| **Wrong folder** | A file here that explains *one app's history* rather than how to build something | It is an app doc — move it to that app's `docs/` |

**Do not** propose adding an always-on `AGENTS.md` rule to make the recipe folder
"fire automatically." Chase retrieves recipes by asking for them; that is a deliberate
design choice, and this audit is the mechanism that keeps the folder trustworthy.

### 2g — Doc vs **code** (highest yield — do not skip)

Phase 1 lists source code as out of scope. **This subsection is the exception.**
Everything in 2a–2f compares docs to *other docs*, so a doc that is internally
consistent and simply **wrong about the code** passes every one of them. The robot
cannot see this at all. In the 2026-08-01 session, this is where every real bug was.

Pick the 3–5 rules covering the most-touched subsystems and verify each claim:

| Check | How | Real example found |
|---|---|---|
| **Doc contradicts code** | For each value, direction, or behavior a rule asserts, open the code and confirm | `spire-overlay.mdc` said "restore cursor **above** saved position"; `main.js` does `savedPos.y + OFFSET` — positive Y is **down**. Backwards |
| **Doc's example wouldn't work** | Would a fresh agent following this snippet succeed? | `hover-to-lock-drag.md` showed `addEventListener('mouseenter')`; live overlays **poll**, because the window is click-through so DOM events never fire. Following the doc yields a handle that silently never activates |
| **Documented mechanism doesn't exist** | Grep for the implementation the doc describes | `overlay-exclusion-zones.md` — design sketch, no code. Correctly tombstoned; check for others |
| **Named exemplar still valid** | Confirm the file/class named still exists and is still the best one | `patterns/README.md` cites `DragHandler` — verified present. But it named *no* Electron exemplar while `joystick-drag.js` (519 lines) was the real one |
| **Glob actually matches** | List real filenames against the rule's `globs:` | `25-dwell-accessibility.mdc` globbed `*-overlay.html`; a new file named `overlay.html` fell straight through |
| **Parallel implementations** | Grep the concept tree-wide; count homes | Seven independent ghost-drag implementations in `electron-app/src/window-managers/`, none named in the pattern index |

**Action:** fix the doc to match the code — **the code is the truth.** If the
*code* looks wrong, surface it to Chase; never silently "fix" working behavior.
Prefer replacing a restated value with the **constant's name**, so the claim
cannot go stale again.

---

## Phase 3 — Deliverables (report to Chase)

End with a **short table** — no wall of grep output.

| Item | Action taken / proposed | Needs Chase OK? |
|------|-------------------------|-----------------|
| e.g. Duplicate HTML notes | Merged into `html-infographic-delivery.mdc` + AGENTS | Y/N |

Include:

1. Phase 0 summary (before/after if fixes applied)
2. Contradictions found (or “none found”)
3. Merges/archives performed or **proposed** (destructive changes need explicit OK)
4. Always-on line count
5. **Next audit:** suggest date ~3 months out unless Chase says otherwise

---

## Rules for the agent running this audit

1. **Grep before adding** — this audit merges; it does not create parallel docs.
2. **Do not** promote findings to rung 4 unless Chase explicitly asks.
3. **Do not** delete files without listing them in the report; prefer merge + tombstone.
4. **Do not** edit frozen Calendar 2.0 unless Chase unfreezes it.
5. **Do not** run npm test, builds, or GUI launches unless Chase asks.
6. **Do not** commit unless Chase asks (audit can be report-only).

---

## Quick reference — robot vs AI

| Task | Who |
|------|-----|
| Dead links, identical file twins, unindexed `.mdc`, bare timing values | `check-docs.js` |
| Same topic / contradictory meaning / stale / wrong rung | This audit (AI) |
| **Doc contradicts the code it describes** | **This audit (AI) — § 2g, highest yield** |
| Prevent new duplicates at capture time | Capture skill — grep before write |

---

## Related files

| File | Role |
|------|------|
| `scripts/check-docs.js` | Phase 0 robot |
| `.claude/skills/capture/SKILL.md` | Capture-time grep + rung pick |
| `docs/context-engineering-capture-costs.html` | Rung cost + abuse reference (http://127.0.0.1:8765/context-engineering-capture-costs.html) |

This file is **not** indexed in AGENTS (rung 5 only). Chase finds it by description or grep when needed.

---

*Last template update: 2026-08-01 — added § 2g doc-vs-code; check-docs.js now flags bare timing values.*
