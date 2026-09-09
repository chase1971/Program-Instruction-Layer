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
| `routed` | → | **The index worked.** It sent you to the right next doc, *or* it correctly told you no narrower owner exists and you stayed scoped |
| `partial` | ~ | Some value, not a direct hit — and it didn't route you either |
| `dead-end` | ✗ | Checked but didn't help |

### `routed` vs `partial` — the one call that matters

`partial` and `dead-end` on a **doc** step feed the **Real index gaps** panel. That panel is a
to-do list, so only put something there when a row really is missing.

**Use this one test.** After reading the doc, did you have to *grep the tree* to find the answer?

- **No** — the doc named the next file, or correctly told you no narrower owner exists → **`routed`**
- **Yes** — you were left hunting → **`partial`**, or **`dead-end`** if the doc was wrong or stale

> **This is the most-violated field in the log.** A 2026-09-08 audit of 342 bumps found **41% of
> flagged gaps were mislabeled** — notes reading *"no narrower recipe was needed"* and *"routed via
> APP_LOCATIONS"* logged as `partial`. Those are the definition of `routed`. The mislabels made
> `recipes/INDEX.md` look like it failed 79% of the time when it was working correctly.
> **Confirming that nothing narrower exists is the index succeeding, not failing.**

**If you log a doc step `partial` or `dead-end`, you own the fix** — add the row, or say in the
`note` why no row is warranted. See [END_OF_SESSION.md](./END_OF_SESSION.md) step 6.

Nested **`steps`** array = Task sub-agent branch. Use `branch` label on the parent step.

Legacy shorthand `{ "step": "…", "result": "✓" }` still parses.

### Honesty rule

Log every lookup that did not help as `dead-end` or `partial` (or `routed` — see above). The
navigation path is a record of where you looked, not a highlight reel.

### Bump granularity

One bump per **deliverable** (a fix, a feature chunk, a doc update), not per chat exchange. Q&A threads where you ask several follow-ups without new code still get one bump when the answer is done.

---

## Hook-verified fields (automatic)

You do not set these. The hook records the tool timeline and the transcript path; the bump slices
both for the task window. They appear on [session tracking](http://127.0.0.1:8765/session-tracking-log.html):

| Field | Meaning |
|-------|---------|
| `billedTokens` | **Real tokens billed for this task** — cache read + cache write + input + output |
| `tokensPerTurn` | Context dragged along per assistant turn. Rises with session length, not task difficulty |
| `tokenTurns` | Assistant turns in the window |
| `activeMs` / `activeLabel` | First-to-last tool event in the window (excludes idle gaps) |
| `observedSearches` / `observedDocReads` | Hook-counted searches and doc reads in the window |
| `durationMs` / `durationLabel` | Wall-clock since previous bump — **includes idle; p90 was 9.6h.** Ignore it |

### Removed 2026-09-08 — do not re-add

An audit of the first 342 bumps found three metrics were measuring their own instrumentation:

- **`indexFirst`** — scored 0/233 tasks. It watched the tool timeline, but `AGENTS.md` and
  `CLAUDE.md` are auto-loaded by the harness and never pass through a Read tool. It was blind to
  the most-used index in the tree.
- **`unexplainedSearches`** — flagged 99.2% of searches. It only recognised a logged step as a
  search when `kind` was `grep|glob|web|search`; agents used **59 different `kind` values**. It
  measured vocabulary drift.
- **`pathCoverage`** — median 0.24, but a bump covers a whole deliverable, so it mostly measured
  how long it had been since the last bump.

**Cost per task replaced all three.** Greps are free; tokens are not.

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
