# Session tracking

> **Rung 5 procedure doc** — agents read **this file** for task bumps. Metrics finalize: [SESSION_METRICS.md](./SESSION_METRICS.md).  
> **Trigger:** After each completed deliverable (**bump**).

Chase views: **`http://127.0.0.1:8765/session-tracking-log.html`**

---

## After each completed deliverable — one command

```powershell
node scripts/append-session-scorecard.js --note "Fixed D2L download stall — removed pause without resume"
```

If a doc you opened **should have routed you and didn't** (you still had to grep the tree), add one
`--gap` per doc, as `"<doc path>: <what was missing>"`:

```powershell
node scripts/append-session-scorecard.js --note "Moved grade sync button" --gap "School Scrips/Macro App/AGENTS.md: no row for grade sync"
```

That's the whole bump. Don't write a JSON file, don't list the steps you took, and don't count greps or files.

**`--gap` test:** after reading the doc, did you have to *grep the tree* to find the answer?
**No** → not a gap, even if the doc only pointed you onward or said nothing narrower exists.
**Yes** → gap. **You own the fix:** add the row before the session ends, or say in the note why none is warranted.

`--bump-file <path>` with `{ "chunkNote": "…", "indexGaps": [{ "doc": "…", "note": "…" }] }` still
works. A bump with no note is rejected and logs nothing.

**Granularity:** one bump per **deliverable** (a fix, a feature chunk, a doc update), not per chat exchange.

---

## Recorded automatically — you set none of this

| Field | Meaning |
|-------|---------|
| `billedTokens`, `tokensPerTurn`, `tokenTurns`, `tokensCacheRead`, `tokensOutput` | Real tokens for this task, each reply counted once. **Claude Code only** — Cursor transcripts carry no usage |
| `model` | From the Claude Code transcript, or the hook payload where the host sends one |
| `chatUserMessages` / `chatTranscriptKB` / `chatId` | Chat size so far — **the only cost signal in Cursor** |
| `activeMs` | First to last tool call in the task window (excludes idle) |
| `durationMs` | Wall-clock since previous bump — includes idle; mostly ignore |

**What the cost data showed (2026-09-21, 44 costed tasks):** 98% of billed tokens were cache
re-reads — the conversation re-sent on every reply. Eight tasks over 40 replies used half of all
tokens. Cost tracks **session length**, so the lever is a momentum handoff before the chat gets
long, not fewer searches.

---

## Removed — do not re-add

- **2026-09-08:** `indexFirst`, `unexplainedSearches`, `pathCoverage` measured their own
  instrumentation (0/233, 99.2%, window length). Plain-language write-up:
  `instructional-layer-htmls/measuring-agent-efficiency.html`.
- **2026-09-21:** the step-by-step `navigationPath`, observed search/read counts, and the metrics
  page's grep and file counts. Across 527 bumps, 85% of self-graded steps were "helpful" and 93%
  of tasks said step 1 helped. Agents ran a median of 15 searches but logged 4 steps. A number
  that comes out almost the same for every task can't tell you anything. The one real
  signal in it, docs that failed to route, is now `--gap`. Old rows keep their `navigationPath`
  in the jsonl, and their failed doc steps still show in the page's gap table.

---

## Write-only rule

Bump with `--note`. **Never read** `session-tracking-log.html` (Chase's dashboard).
**Archive:** `agent docs/session-tracking.jsonl`.

The Stop hook blocks finishing when ≥2 files were edited with zero bumps — see
[SESSION_METRICS.md](./SESSION_METRICS.md) § Enforcement.

---

*Updated: 2026-09-21 — bump is one command (`--note`, optional `--gap`); navigationPath retired*
