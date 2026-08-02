# Session scorecard

> **Rung 5 procedure doc** — agents read **this file only**, not the HTML log.  
> **Trigger:** After each completed task (**bump**), or end-of-session (**finalize**).

Chase views: **`http://127.0.0.1:8765/session-scorecards-log.html`**

---

## Why bump as you go (survives summarize)

End-of-session-only scorecards **lose accuracy** when Cursor summarizes the chat — the agent forgets early greps/reads.

**Running tally:** after each deliverable (“here’s the fix”, “done”, “linked”), the agent logs **that chunk only** to disk via a script. Summarize cannot erase what’s already on the scratch pad.

| When | Command | Token cost |
|------|---------|------------|
| **After each completed task** | `--bump-file` | ~50–150 (tiny JSON) |
| **End of session** | `--finalize-file` | ~200–400 (summary sentences only — counts come from running file) |

---

## Write-only rule

| Do | Don’t |
|----|--------|
| `--bump-file` after tasks | Read `session-scorecards-log.html` |
| `--finalize-file` at wrap | Re-count from memory if running file exists |

**Scratch pad:** `agent docs/.session-scorecard-running.json` (auto)  
**Archive:** `agent docs/session-scorecards.jsonl`  
**View:** regenerated HTML

---

## Hook auto-tally (experimental)

`.cursor/hooks.json` runs `scripts/scorecard-hook-tally.js` on every **postToolUse** event. It appends to the same running file:

| Tool | Count |
|------|--------|
| `Grep`, `Glob`, `WebSearch`, `Shell` | +1 search |
| `Read` | file read (+ docs/rules if path matches) |
| `Write`, `StrReplace`, `Delete`, `EditNotebook` | file edited |

Sets `hookTally: true` on the running object. Finalize shows a **Hook tallied** pill; `confidence` is **medium** when hooks ran but the agent never bumped.

**Hooks do not replace bumps** — they miss task boundaries (`chunkNote`), turns, corrections, and anything run outside Cursor tools (e.g. manual `ilspycmd` in an external terminal).

**Reload Cursor** after changing hooks. Check **Output → Hooks** if counts stay at zero.

---

## After each completed task (bump)

When you finish a chunk of work and report to Chase, run:

```powershell
node scripts/append-session-scorecard.js --bump-file agent docs/.scorecard-bump.json
```

**`agent docs/.scorecard-bump.json`** example — only **this task**, not the whole session:

```json
{
  "chunkNote": "Built scorecard HTML layout and hover tooltips",
  "addGreps": 2,
  "addTurns": 0,
  "filesRead": ["agent docs/SESSION_SCORECARD.md"],
  "filesEdited": ["scripts/append-session-scorecard.js", "agent docs/session-scorecards-log.html"],
  "docsRulesOpened": ["agent docs/SESSION_SCORECARD.md"]
}
```

- Count **your** tool uses since the last bump (or since session start).
- `addTurns`: optional — usually only bump at end with `finalize` unless Chase sent several messages in this chunk.
- Delete the temp bump file after running.

HTML shows a dashed **“Current session (live tally)”** card at the top while running file exists.

---

## End of session (finalize)

```powershell
node scripts/append-session-scorecard.js --finalize-file agent docs/.scorecard-final.json
```

```json
{
  "summaryHuman": "Two plain sentences about the whole session.",
  "sessionType": "mixed",
  "outcome": "Done",
  "summarized": true,
  "confidence": "high",
  "worthNoting": "Optional — only if unusual",
  "captureCandidate": "Optional agent suggestion for a future rule",
  "nextSession": "Concrete next step",
  "addTurns": 5,
  "addCorrections": 0
}
```

**Counts** (`greps`, files read/edited, docs opened) come from the **running file** — do not re-guess them here.  
`confidence: high` on counts when bumps were used, even if `summarized: true` for the chat.

Legacy one-shot: `--file full.json` still works (no running tally).

---

## Field guide

| Field | Meaning |
|-------|---------|
| **`summaryHuman`** | 1–2 fluid sentences (finalize only) |
| **`addGreps` / bump** | Searches **this chunk** |
| **`docsRulesOpened`** | Instruction files **read** (.md, .mdc) — not created |
| **`filesRead` / `filesEdited`** | Paths; HTML splits doc vs code |

---

*Updated: 2026-08-02 — hook auto-tally*

---

## `bumped` — derived, never self-reported

`finalize` sets `bumped: true` only if the agent logged at least one **bump**
(`--bump-file`), not merely because the hook created a running file.

| `bumped` | `confidence` | What it means |
|---|---|---|
| `true` | `high` | Counts accumulated on disk as the work happened — trustworthy |
| `false` | `low` | Counts reconstructed from memory at the end — order-of-magnitude only |

This separates **"the chat was summarized"** from **"the agent forgot to bump."**
Those are different failures: the first is a tool limit, the second means the
always-on bump rule is not being followed. A recurring
**"Not bumped — counts reconstructed"** pill in the HTML log is the signal to fix
the rule, not the numbers.

Explicitly passing `confidence` in the finalize JSON still overrides the default.
