# Session tracking

> **Rung 5 procedure doc** — agents read **this file** for task bumps. Metrics finalize: [SESSION_METRICS.md](./SESSION_METRICS.md).  
> **Trigger:** After each completed task (**bump**).

Chase views: **`http://127.0.0.1:8765/session-tracking-log.html`**

---

## What this is

**One row per completed task** — not one row per chat session. Each bump appends a collapsible entry with:

- What you did (`chunkNote`)
- How long since the previous bump (`durationLabel`)
- Ordered **navigation path** — where you looked, ✓ / ~ / ✗

Greps, files read/edited, and end-of-session totals live on [session metrics](./SESSION_METRICS.md).

---

## After each completed task (bump)

When you finish a chunk of work and report to Chase, run:

```powershell
node scripts/append-session-scorecard.js --bump-file agent docs/.scorecard-bump.json
```

Give Chase: **`http://127.0.0.1:8765/session-tracking-log.html`**

### Bump JSON example — **this task only**

```json
{
  "chunkNote": "Investigated course rename vs folder paths — confirmed safe",
  "addGreps": 3,
  "addTurns": 0,
  "navigationPath": [
    { "target": "agent docs/INDEX.md", "kind": "doc-index", "outcome": "partial", "note": "No row — routed to app AGENTS via row 22" },
    { "target": "School Scrips/Macro App/AGENTS.md", "kind": "doc", "outcome": "helpful" },
    { "target": "renderer/src/hooks/shell/useRenameCoursesModal.ts", "kind": "code", "outcome": "helpful", "note": "Label-only rename" },
    { "target": "modules/d2l/rosters_paths.py", "kind": "code", "outcome": "helpful" }
  ],
  "filesRead": ["School Scrips/Macro App/modules/d2l/rosters_paths.py"],
  "filesEdited": [],
  "docsRulesOpened": ["School Scrips/Macro App/AGENTS.md"]
}
```

### Required fields

| Field | Required | Meaning |
|-------|----------|---------|
| **`chunkNote`** | Yes | One-line description of what you finished |
| **`navigationPath`** | Yes | Ordered lookup steps for **this task** |
| `addGreps`, `filesRead`, `filesEdited` | Optional | Feeds the metrics running file (hooks also tally) |

### navigationPath outcomes

| `outcome` | Marker | Meaning |
|-----------|--------|---------|
| `helpful` | ✓ | Got you closer to the answer |
| `partial` | ~ | Some value, not a direct hit |
| `dead-end` | ✗ | Checked but didn't help |

Nested **`steps`** array = Task sub-agent branch. Use `branch` label on the parent step.

Legacy shorthand `{ "step": "…", "result": "✓" }` still parses.

### Honesty rule

Log every lookup that did not help as `dead-end` or `partial`. The hook records searches independently; the tracking page compares hook counts to your path and shows **"N searches not in path"** when the gap is ≥3. Omitting dead ends makes coverage look better than it was — the page now catches that.

### Bump granularity

One bump per **deliverable** (a fix, a feature chunk, a doc update), not per chat exchange. Q&A threads where you ask several follow-ups without new code still get one bump when the answer is done.

---

## Hook-verified fields (automatic)

Each bump compares the agent's `navigationPath` to the hook's `toolTimeline` for that task window. You do not set these — they appear on [session tracking](http://127.0.0.1:8765/session-tracking-log.html):

| Field | Meaning |
|-------|---------|
| `activeMs` / `activeLabel` | First-to-last tool event in the task window (excludes idle gaps) |
| `durationMs` / `durationLabel` | Wall-clock since previous bump (includes idle — kept for back-compat) |
| `indexFirst` | First nav event was an index-like doc read before any search |
| `searchesBeforeFirstDoc` | Searches that ran before the first doc read |
| `observedSearches` | Hook-counted searches in the window |
| `unexplainedSearches` | Observed searches not logged in the path |
| `pathCoverage` | Logged steps ÷ observed nav events (low = path is a summary, not a record) |

Pre-change entries lack these fields and are excluded from aggregate rates on the summary bar.

---

## Write-only rule

| Do | Don't |
|----|--------|
| `--bump-file` after each deliverable | Read `session-tracking-log.html` |
| Include `navigationPath` every bump | Skip bumps and reconstruct at end |

**Archive:** `agent docs/session-tracking.jsonl` (one line per bump)  
**View:** regenerated `session-tracking-log.html`

---

## Why bump as you go

Summarize erases chat memory — disk entries survive. Each bump is a task boundary Chase can expand to audit doc routing.

Hooks still block finish when ≥2 files edited and zero bumps — see [SESSION_METRICS.md](./SESSION_METRICS.md) § Enforcement.

---

*Updated: 2026-08-14 — hook-verified navigation reconciliation*
