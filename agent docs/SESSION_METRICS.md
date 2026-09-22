# Session metrics

> **Rung 5 procedure doc** — end-of-session finalize and the enforcement hooks.  
> Task pathing bumps: [SESSION_TRACKING.md](./SESSION_TRACKING.md).

Chase views: **`http://127.0.0.1:8765/session-metrics-log.html`**

---

## What this is

One **session card** per finalized chat: summary, messages, tokens (or chat size in Cursor), peak
context per reply, the task list, corrections, and the agent's *worth noting* / *capture* notes.
Grep counts, file lists and count-trust pills were removed 2026-09-21. Nothing read them back.

---

## Running tally (automatic)

**Scratch pad:** `agent docs/.session-scorecard-running.json`  
**Archive:** `agent docs/session-scorecards.jsonl`

`scripts/scorecard-hook-tally.js` records, with no agent effort: messages from Chase, files edited
(evidence for the Stop hook), tool-call timestamps (active time), the chat/transcript, and the model.
Bumps add the task list. Session tokens are summed from that session's task rows at finalize.

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
  "worthNoting": "Optional — anything unusual",
  "captureCandidate": "Optional — a rule worth capturing",
  "nextSession": "Concrete next step",
  "addCorrections": 0
}
```

Messages, tasks and tokens come from the running file and task rows — don't estimate them.

---

## Enforcement (2026-08-07)

`scripts/scorecard-enforce.js` runs on **UserPromptSubmit**, **Stop**, and **PreCompact** (`.cursor/hooks.json`, `.claude/settings.json`, `.codex/hooks.json`):

| Hook | Behavior |
|------|----------|
| **UserPromptSubmit** | Counts messages **per chat** (`scripts/chat-task.js`), so a fresh task after a momentum handoff starts at zero. Injects one context-efficiency warning recommending a handoff once the task is heavy — in Claude Code, when the latest reply re-read at least `HEAVY_CONTEXT_TOKENS` (`scripts/session-token-cost.js`); in Cursor, which records no tokens, at `CONTEXT_WARNING_TURN_INTERVAL` messages in the chat. Repeats at most once per that interval. |
| **Stop** | Blocks turn end when ≥2 files edited, 0 bumps, ≥3 turns. Reminds agent to bump with `--note`. Max 3 blocks. |
| **PreCompact** | Always injects the same fresh-task warning before compaction; also reminds the agent to bump any unlogged edited work. |

Procedure detail was in the old SESSION_SCORECARD doc — behavior unchanged.

---

## `bumped` — derived at finalize

| `bumped` | Meaning |
|----------|---------|
| `true` | At least one bump this session — the task list is real |
| `false` | No bumps — the card has no task list |

---

## Rebuild commands

```powershell
node scripts/append-session-scorecard.js --rebuild
node scripts/append-session-scorecard.js --rebuild-tracking-from-running
```

---

*Updated: 2026-09-21 — cards show cost and notes; grep/file counts and trust pills removed*
