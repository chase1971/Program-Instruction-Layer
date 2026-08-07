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

## Enforcement (2026-08-07) — hooks block, prose no longer just asks

Prose alone didn't work: a full session on 2026-08-06 had real edits and zero bumps. Two
hooks in `scripts/scorecard-enforce.js` run on **Stop** and **PreCompact** for every agent
that loads the Programs hook configs:

| Agent | Config file | Stop (blocks finish) | PreCompact (reminder) | Auto-tally |
|-------|-------------|----------------------|------------------------|------------|
| **Cursor** | [`.cursor/hooks.json`](../.cursor/hooks.json) | `stop` → `--stop`, `loop_limit: 3` | `preCompact` → `--precompact` | `postToolUse` + `beforeSubmitPrompt` |
| **Claude Code** | [`.claude/settings.json`](../.claude/settings.json) | `Stop` → `--stop` | `PreCompact` → `--precompact` | `PostToolUse` + `UserPromptSubmit` |
| **Codex** | [`.codex/hooks.json`](../.codex/hooks.json) | `Stop` → `--stop` | `PreCompact` → `--precompact` | `PostToolUse` + `UserPromptSubmit` |

Cursor also loads `.claude/settings.json` when **Settings → Rules → Include third-party Plugins, Skills, and other configs** is on — but the native `.cursor/hooks.json` entries above are the primary enforcement path.

**Codex:** project hooks load when the Programs folder is a **trusted** project (already set in your `~/.codex/config.toml`). First run may prompt **Trust** in `/hooks` — accept once per machine.

| Hook | What it does |
|------|----------------|
| **Stop** | **Blocks** the agent's turn from ending when the running tally shows ≥2 edited files, 0 bumps, and ≥3 turns. The block reason is fed back to the agent, telling it to run `--bump-file` before finishing. Capped at **3 consecutive blocks** (`loop_limit` in Cursor; `stopBlockCount` in the running file for Claude/Codex), then force-allows — cannot loop forever. |
| **PreCompact** | Non-blocking reminder injected right before compaction when there's unbumped work. The disk-based tally survives compaction; the agent's memory that it needs to bump does not. |

**Known gap:** the check only fires on "never bumped this session." A session that bumps
once early and then goes quiet for the rest of a long session won't re-trigger — there's no
"time since last bump" check yet. If that pattern shows up, extend `scorecard-enforce.js`'s
`unbumpedState()` rather than adding a second mechanism.

## Hook auto-tally

`.cursor/hooks.json` (Cursor), `.claude/settings.json` (Claude Code), and `.codex/hooks.json`
(Codex) all run `scripts/scorecard-hook-tally.js` on tool use (and on prompt submit where the
agent supports it). It appends to the same running file — this part is fully automatic and
does **not** depend on the agent remembering anything:

| Tool | Count |
|------|--------|
| `Grep`, `Glob`, `WebSearch`, `Shell` | +1 search |
| `Read` | file read (+ docs/rules if path matches; **`.mdc` → `mdcReadsList` + lifetime stats**) |
| `Write`, `StrReplace`, `Delete`, `EditNotebook` | file edited |
| `CallMcpTool` | tool count (`server:toolName`); `browser_snapshot` also increments snapshot total |
| `Task`, `GetMcpTools`, `WebFetch`, `FetchMcpResource` | tool count |

On every tally the hook also sets **`preHookWorkUntracked`**, **`missingEarlyWork`**, and **`countsTrust`** (`low` / `medium` / `high`) via `scripts/scorecard-trust.js`. The live card shows **Missing early work — hook started late** + **Low confidence counts** until the agent bumps tasks. Pass `"summarized": true` in a bump or finalize JSON when Cursor summarized the chat.

HTML groups **Tools**, **Markdowns** (`.mdc` first, then AGENTS/CLAUDE with app label), and **Code** in expandable metric tiles. **Your messages** still needs `addTurns` on finalize — hooks do not count chat turns.

**Hooks do not replace bumps** — they miss task boundaries (`chunkNote`), turns, corrections, and anything run outside Cursor tools (e.g. manual `ilspycmd` in an external terminal).

**Reload Cursor** after changing hooks. Check **Output → Hooks** if counts stay at zero.
**Codex:** run `/hooks` once after pull if hooks show as untrusted.

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
| **`docsRulesOpened`** | Instruction files **read** (.md, .mdc) — not created. HTML shows **filename only**; hover for full path. |
| **`mdcReadsList`** | Subset: `.mdc` files opened via **Read tool**. Lifetime totals in `agent docs/mdc-read-stats.json` + HTML panel. **Does not** count Cursor auto-injecting glob rules when a matching file is open. |
| **`filesRead` / `filesEdited`** | Paths; HTML splits into Tools / Markdowns / Code sections |
| **`toolsUsedCounts`** | MCP and other agent tools (from hook); snapshots also in `browserSnapshots` |

---

*Updated: 2026-08-03 — expandable activity metrics; summarized + no-bump pills; confidence derived at finalize*

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
