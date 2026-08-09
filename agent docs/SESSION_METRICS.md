# Session metrics

> **Rung 5 procedure doc** — grep/file/hook counts and end-of-session finalize.  
> Task pathing bumps: [SESSION_TRACKING.md](./SESSION_TRACKING.md).

Chase views: **`http://127.0.0.1:8765/session-metrics-log.html`**

---

## What this is

One **session card** per finalized chat — greps, files read/edited, docs opened, hook trust pills, corrections. This is the legacy scorecard view; it no longer shows navigation paths (those moved to [session tracking](./SESSION_TRACKING.md)).

---

## Running tally (automatic + bumps)

**Scratch pad:** `agent docs/.session-scorecard-running.json`  
**Archive:** `agent docs/session-scorecards.jsonl`

Hooks in `scripts/scorecard-hook-tally.js` auto-count reads, edits, and searches. **Bumps** add task boundaries and merge chunk-level counts from your bump JSON.

| Tool | Count |
|------|--------|
| `Grep`, `Glob`, `WebSearch`, `Shell` | +1 search |
| `Read` | file read (+ docs/rules if path matches) |
| `Write`, `StrReplace`, `Delete`, `EditNotebook` | file edited |
| `CallMcpTool`, `Task`, `WebFetch`, … | tools used |

---

## End of session (finalize)

On **end of session protocol**, after task bumps are done:

```powershell
node scripts/append-session-scorecard.js --finalize-file agent docs/.scorecard-final.json
```

```json
{
  "summaryHuman": "Two plain sentences about the whole session.",
  "sessionType": "mixed",
  "outcome": "Done",
  "summarized": true,
  "worthNoting": "Optional",
  "nextSession": "Concrete next step",
  "addTurns": 5,
  "addCorrections": 0
}
```

**Counts** come from the running file — do not re-guess greps/files in finalize JSON.

---

## Enforcement (2026-08-07)

`scripts/scorecard-enforce.js` runs on **Stop** and **PreCompact** (`.cursor/hooks.json`, `.claude/settings.json`, `.codex/hooks.json`):

| Hook | Behavior |
|------|----------|
| **Stop** | Blocks turn end when ≥2 files edited, 0 bumps, ≥3 turns. Reminds agent to `--bump-file`. Max 3 blocks. |
| **PreCompact** | Non-blocking reminder before compaction |

Procedure detail was in the old SESSION_SCORECARD doc — behavior unchanged.

---

## `bumped` — derived at finalize

| `bumped` | Meaning |
|----------|---------|
| `true` | At least one `--bump-file` this session — counts trustworthy |
| `false` | Counts reconstructed at end — order-of-magnitude only |

---

## Rebuild commands

```powershell
node scripts/append-session-scorecard.js --rebuild
node scripts/append-session-scorecard.js --rebuild-tracking-from-running
```

---

*Updated: 2026-08-09 — split from session tracking*
