/**
 * FILE: scripts/session-token-cost.js
 * PURPOSE: Attribute real billed tokens to a task window by reading the
 *          Claude Code transcript the hook captured for this session.
 *
 * Why this exists: the old tracking metrics counted greps as a proxy for
 * effort. Greps are free; tokens are not. Every assistant turn re-reads the
 * whole cached prefix, so cost is (context size x turns), not (searches).
 * This module reports the number that is actually billed.
 */
'use strict';

const fs = require('fs');

// Claude Code writes one JSON object per line; assistant turns carry `usage`.
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

  let turns = 0;
  let cacheRead = 0;
  let cacheWrite = 0;
  let input = 0;
  let output = 0;

  for (const line of lines) {
    const raw = line.trim();
    if (!raw) continue;
    let entry;
    try {
      entry = JSON.parse(raw);
    } catch {
      continue;
    }
    const usage = entry.message && entry.message.usage;
    if (!usage) continue;

    const t = new Date(entry.timestamp || 0).getTime();
    if (Number.isNaN(t) || t <= from || t > to) continue;

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

function formatTokens(n) {
  if (!Number.isFinite(n) || n <= 0) return '—';
  if (n >= 1e9) return `${(n / 1e9).toFixed(1)}B`;
  if (n >= 1e6) return `${(n / 1e6).toFixed(1)}M`;
  if (n >= 1e3) return `${(n / 1e3).toFixed(0)}k`;
  return String(n);
}

module.exports = {
  readTranscriptUsage,
  formatTokens,
};
