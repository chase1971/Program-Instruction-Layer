/**
 * FILE: scripts/token-report-data.js
 * PURPOSE: Read real billed-token data out of Claude Code transcripts (and
 *          optionally Cursor's local DB) and reduce it to the few numbers that
 *          actually change behavior.
 *
 * The point of this file: intuition about token cost is usually wrong. Writing
 * code is cheap. READING is expensive, and it compounds — anything pulled into
 * the conversation is re-billed on every later turn of that session.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');

const CLAUDE_PROJECTS = path.join(
  os.homedir(), '.claude', 'projects', 'C--Users-chase-Documents-Programs',
);

// A single turn's billed input is the whole conversation so far. Growth between
// consecutive turns is what that turn permanently ADDED.
function readSessions(dir = CLAUDE_PROJECTS) {
  if (!fs.existsSync(dir)) return [];
  const out = [];
  for (const f of fs.readdirSync(dir).filter((x) => x.endsWith('.jsonl'))) {
    let lines;
    try {
      lines = fs.readFileSync(path.join(dir, f), 'utf8').split('\n');
    } catch {
      continue;
    }
    const turns = [];
    for (const line of lines) {
      const raw = line.trim();
      if (!raw) continue;
      let j;
      try {
        j = JSON.parse(raw);
      } catch {
        continue;
      }
      const us = j.message && j.message.usage;
      if (!us) continue;
      const tools = [];
      if (j.message && Array.isArray(j.message.content)) {
        for (const c of j.message.content) if (c.type === 'tool_use') tools.push(c.name);
      }
      turns.push({
        ctx: (us.cache_read_input_tokens || 0)
          + (us.cache_creation_input_tokens || 0)
          + (us.input_tokens || 0),
        out: us.output_tokens || 0,
        model: (j.message && j.message.model) || null,
        tools,
        ts: j.timestamp || null,
      });
    }
    if (turns.length < 5) continue;
    out.push({
      id: f.slice(0, 8),
      turns,
      turnCount: turns.length,
      billed: turns.reduce((a, t) => a + t.ctx + t.out, 0),
      started: turns[0].ts,
      models: [...new Set(turns.map((t) => t.model).filter(Boolean))],
    });
  }
  return out.sort((a, b) => b.billed - a.billed);
}

// Attribute context growth to the tool that ran on the turn causing it, and
// multiply by turns remaining — that is the real, compounded price of pulling
// something into the conversation.
function toolCosts(sessions, minCalls = 15) {
  const by = {};
  for (const s of sessions) {
    for (let i = 0; i < s.turns.length - 1; i++) {
      const growth = s.turns[i + 1].ctx - s.turns[i].ctx;
      // Negative or huge jumps mean a compaction/reset, not real growth.
      if (growth <= 0 || growth > 400000) continue;
      const remaining = s.turns.length - 1 - i;
      const name = s.turns[i].tools.length ? s.turns[i].tools[0] : '(no tool — plain reply)';
      if (!by[name]) by[name] = { name, calls: 0, added: 0, compounded: 0 };
      by[name].calls += 1;
      by[name].added += growth;
      by[name].compounded += growth * remaining;
    }
  }
  const rows = Object.values(by).filter((r) => r.calls >= minCalls)
    .sort((a, b) => b.compounded - a.compounded);
  const total = rows.reduce((a, r) => a + r.compounded, 0) || 1;
  return rows.map((r) => ({
    ...r,
    avgAdded: Math.round(r.added / r.calls),
    share: r.compounded / total,
  }));
}

// The headline: cost per turn is not constant. It climbs with session length,
// because each turn re-reads everything before it.
const LENGTH_BUCKETS = [
  [0, 50, 'Under 50'],
  [50, 150, '50 – 150'],
  [150, 300, '150 – 300'],
  [300, 600, '300 – 600'],
  [600, Infinity, 'Over 600'],
];

function lengthScaling(sessions) {
  return LENGTH_BUCKETS.map(([lo, hi, label]) => {
    const g = sessions.filter((s) => s.turnCount >= lo && s.turnCount < hi);
    if (!g.length) return null;
    const avgTurns = g.reduce((a, s) => a + s.turnCount, 0) / g.length;
    const avgCost = g.reduce((a, s) => a + s.billed, 0) / g.length;
    return {
      label,
      sessions: g.length,
      avgTurns: Math.round(avgTurns),
      avgCost: Math.round(avgCost),
      costPerTurn: Math.round(avgCost / avgTurns),
    };
  }).filter(Boolean);
}

function totals(sessions) {
  const billed = sessions.reduce((a, s) => a + s.billed, 0);
  const turns = sessions.reduce((a, s) => a + s.turnCount, 0);
  return {
    sessions: sessions.length,
    turns,
    billed,
    perTurn: turns ? Math.round(billed / turns) : 0,
  };
}

// Cursor keeps per-message token counts in its own SQLite store. Reading it
// needs sqlite3, which ships with Python on this machine, so it is opt-in and
// cached — a full scan walks ~400k rows and takes a couple of minutes.
function cursorCachePath(root) {
  return path.join(root, 'agent docs', '.token-report-cursor.json');
}

function readCursorCache(root) {
  const p = cursorCachePath(root);
  if (!fs.existsSync(p)) return null;
  try {
    return JSON.parse(fs.readFileSync(p, 'utf8'));
  } catch {
    return null;
  }
}

function formatTokens(n) {
  if (!Number.isFinite(n) || n <= 0) return '—';
  if (n >= 1e9) return `${(n / 1e9).toFixed(1)}B`;
  if (n >= 1e6) return `${(n / 1e6).toFixed(1)}M`;
  if (n >= 1e3) return `${(n / 1e3).toFixed(0)}k`;
  return String(Math.round(n));
}

module.exports = {
  CLAUDE_PROJECTS,
  readSessions,
  toolCosts,
  lengthScaling,
  totals,
  cursorCachePath,
  readCursorCache,
  formatTokens,
};
