/**
 * FILE: scripts/session-context-jumps.js
 * PURPOSE: For a task window, find the tool calls that grew the context the most, so a
 *          costly step shows up as "Read foo.ts, +18k" instead of an average. Claude Code only:
 *          Cursor transcripts have no usage, so there is nothing to measure growth from.
 *
 * How: each reply's context (cache read + cache write + input) minus the previous reply's is
 * what the previous reply's tool calls (and Chase's message) added. The jump is attributed to
 * the tool calls of the previous reply. A drop in context means compaction and is skipped.
 */
'use strict';

const fs = require('fs');

const TOP_N = 5;
// Smaller jumps are noise; the point is the outliers.
const MIN_JUMP_TOKENS = 2000;

function describeTool(block) {
  const input = block.input || {};
  const filePath = input.file_path || input.path;
  if (typeof filePath === 'string' && filePath) {
    return `${block.name} ${filePath.split(/[\\/]/).pop()}`;
  }
  const target = input.pattern || input.command || input.url || input.query;
  if (typeof target !== 'string' || !target) return block.name;
  return `${block.name} ${target.replace(/\s+/g, ' ').slice(0, 50)}`;
}

function contextOf(usage) {
  return (usage.cache_read_input_tokens || 0)
    + (usage.cache_creation_input_tokens || 0)
    + (usage.input_tokens || 0);
}

// Replies in transcript order: { id, t, context, tools[] }. One line per content block, so
// tool_use blocks arrive on lines that repeat the reply's message id.
function readReplies(transcriptPath) {
  let lines;
  try {
    lines = fs.readFileSync(transcriptPath, 'utf8').split('\n');
  } catch {
    return [];
  }
  const replies = [];
  const byId = new Map();
  for (const raw of lines) {
    if (!raw.includes('"assistant"')) continue;
    let entry;
    try {
      entry = JSON.parse(raw);
    } catch {
      continue;
    }
    const message = entry.message;
    if (entry.type !== 'assistant' || !message || entry.isSidechain) continue;
    const id = message.id || entry.uuid;
    let reply = byId.get(id);
    if (!reply) {
      reply = { id, t: new Date(entry.timestamp || 0).getTime(), context: null, tools: [] };
      byId.set(id, reply);
      replies.push(reply);
    }
    if (message.usage && reply.context === null) reply.context = contextOf(message.usage);
    for (const block of message.content || []) {
      if (block.type === 'tool_use') reply.tools.push(describeTool(block));
    }
  }
  return replies.filter((r) => r.context !== null);
}

function readContextJumps(transcriptPath, fromIso, toIso) {
  if (!transcriptPath || !fs.existsSync(transcriptPath)) return null;
  const from = new Date(fromIso || 0).getTime();
  const to = new Date(toIso || Date.now()).getTime();
  if (Number.isNaN(from) || Number.isNaN(to)) return null;

  const replies = readReplies(transcriptPath);
  const jumps = [];
  for (let i = 1; i < replies.length; i += 1) {
    const reply = replies[i];
    if (reply.t <= from || reply.t > to) continue;
    const grew = reply.context - replies[i - 1].context;
    if (grew < MIN_JUMP_TOKENS) continue;
    const tools = replies[i - 1].tools;
    jumps.push({ tokens: grew, from: tools.length ? tools.slice(0, 3).join(' | ') : '(chat)' });
  }
  if (!jumps.length) return null;
  jumps.sort((a, b) => b.tokens - a.tokens);
  return { topJumps: jumps.slice(0, TOP_N) };
}

module.exports = { readContextJumps };
