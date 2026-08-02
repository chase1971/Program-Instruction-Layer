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

- `AGENTS.md`, `CLAUDE.md`, `APP_LOCATIONS.md`
- `.cursor/rules/*.mdc` (root + per-app)
- `cursor-patterns/*.md` (instruction-relevant)
- `docs/*.md`, `docs/*.html` (instruction/delivery pages)
- Per-app: `CLAUDE.md`, `guidelines/Guidelines.md`, `docs/*_INTEGRATION.md`, app `.cursor/rules/*.mdc`

**Out of scope unless Chase names it**

- `School Scrips/Calendar 2.0/` — **frozen** (`.cursor/rules/45-frozen-apps.mdc`)
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
