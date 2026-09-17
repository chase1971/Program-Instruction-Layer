/**
 * FILE: scripts/session-token-cost.js
 * PURPOSE: Attribute real billed tokens to a task window by reading the
 *          Claude Code transcript the hook captured for this session, and report
 *          how much context the latest reply re-read (the context-warning trigger).
 *
 * Why this exists: the old tracking metrics counted greps as a proxy for
 * effort. Greps are free; tokens are not. Every assistant turn re-reads the
 * whole cached prefix, so cost is (context size x turns), not (searches).
 * This module reports the number that is actually billed.
 *
 * One reply counts once. Claude Code writes a transcript line per content block
 * (thinking, text, each tool call) and every line repeats that reply's usage, so
 * summing lines overcounted ~4x (46 lines for 10 replies on 2026-09-11). Usage is
 * keyed by message id.
 *
 * Cursor transcripts carry no usage at all — both readers return null there.
 */
'use strict';

const fs = require('fs');

// Context re-read per turn at which a task counts as heavy. A fresh task starts
// around 55k-90k; long sessions reached 410k-450k before momentum handoffs existed.
const HEAVY_CONTEXT_TOKENS = 250000;
// The context warning runs on every prompt, so it reads only the transcript tail.
const TAIL_BYTES = 512 * 1024;

function contextTokens(usage) {
  return (usage.cache_read_input_tokens || 0)
    + (usage.cache_creation_input_tokens || 0)
    + (usage.input_tokens || 0);
}

// Claude Code writes one JSON object per line; assistant turns carry `usage`.
function parseUsageLine(raw) {
  if (!raw || !raw.includes('"usage"')) return null;
  let entry;
  try {
    entry = JSON.parse(raw);
  } catch {
    return null;
  }
  const usage = entry.message && entry.message.usage;
  if (!usage) return null;
  return {
    id: entry.message.id || entry.requestId || null,
    timestamp: entry.timestamp,
    usage,
  };
}

function readTranscriptUsage(transcriptPath, fromIso, toIso) {
  if (!transcriptPath || !fs.existsSync(transcriptPath)) return null;

  const from = new Date(fromIso || 0).getTime();
  const to = new Date(toIso || Date.now()).getTime();
  if (Number.isNaN(from) || Number.isNaN(to)) return null;

  let lines;
  try {
    lines = fs.readFileSync(transcriptPath, 'utf8').split('\n');
  } catch {
    return null;
  }

  const seen = new Set();
  let turns = 0;
  let cacheRead = 0;
  let cacheWrite = 0;
  let input = 0;
  let output = 0;

  for (const line of lines) {
    const hit = parseUsageLine(line.trim());
    if (!hit) continue;

    const t = new Date(hit.timestamp || 0).getTime();
    if (Number.isNaN(t) || t <= from || t > to) continue;
    if (hit.id) {
      if (seen.has(hit.id)) continue;
      seen.add(hit.id);
    }

    const { usage } = hit;
    turns += 1;
    cacheRead += usage.cache_read_input_tokens || 0;
    cacheWrite += usage.cache_creation_input_tokens || 0;
    input += usage.input_tokens || 0;
    output += usage.output_tokens || 0;
  }

  if (!turns) return null;

  const billedTokens = cacheRead + cacheWrite + input + output;

  return {
    tokenTurns: turns,
    tokensCacheRead: cacheRead,
    tokensCacheWrite: cacheWrite,
    tokensInput: input,
    tokensOutput: output,
    billedTokens,
    // The headline efficiency number: how much context each turn dragged along.
    // Rises with session length regardless of task difficulty, which is exactly
    // the pressure worth watching.
    tokensPerTurn: Math.round(billedTokens / turns),
  };
}

// Context the most recent reply re-read, or null when the transcript has no usage.
function readLatestContextTokens(transcriptPath) {
  if (!transcriptPath || !fs.existsSync(transcriptPath)) return null;

  let text;
  try {
    const size = fs.statSync(transcriptPath).size;
    const start = Math.max(0, size - TAIL_BYTES);
    const buf = Buffer.alloc(size - start);
    const fd = fs.openSync(transcriptPath, 'r');
    try {
      fs.readSync(fd, buf, 0, buf.length, start);
    } finally {
      fs.closeSync(fd);
    }
    text = buf.toString('utf8');
  } catch {
    return null;
  }

  // The first line of the tail may be cut mid-object; parseUsageLine skips it.
  const lines = text.split('\n');
  for (let i = lines.length - 1; i >= 0; i -= 1) {
    const hit = parseUsageLine(lines[i].trim());
    if (hit) return contextTokens(hit.usage);
  }
  return null;
}

function formatTokens(n) {
  if (!Number.isFinite(n) || n <= 0) return '—';
  if (n >= 1e9) return `${(n / 1e9).toFixed(1)}B`;
  if (n >= 1e6) return `${(n / 1e6).toFixed(1)}M`;
  if (n >= 1e3) return `${(n / 1e3).toFixed(0)}k`;
  return String(n);
}

module.exports = {
  HEAVY_CONTEXT_TOKENS,
  readTranscriptUsage,
  readLatestContextTokens,
  formatTokens,
};
