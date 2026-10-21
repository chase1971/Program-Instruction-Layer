/**
 * FILE: scripts/context-growth-estimate.js
 * PURPOSE: Estimate how much a chat's context has grown from its transcript alone, for hosts
 *          whose transcripts carry no token usage (Cursor, Codex). Feeds the context warning.
 *
 * Why not count messages: across 128 Claude Code sessions (2026-10-21) the number of messages
 * from Chase explained 22% of the variance in context growth. Tool calls explained 87%,
 * and tool calls plus words written explained 89%. One message can start 60 tool calls, and
 * every tool call is another reply that re-reads the whole context.
 *
 * Fit (least squares, growth = context at the largest reply minus context at the first):
 *   growth ~ 25k + 1.1k per tool call + 1.9 per "written token" (characters / 4 of assistant
 *   text and tool-call inputs). The written-token term stands in for tool results, which Cursor
 *   transcripts do not store. Images are not seen by this estimate.
 *
 * Fits Claude Code; applying it to Cursor assumes similar tool-result sizes. Recalibrate against
 * the Cursor usage CSV when there is one. Returns null when the transcript cannot be read.
 */
'use strict';

const fs = require('fs');

const INTERCEPT = 25000;
const PER_TOOL_CALL = 1100;
const PER_WRITTEN_TOKEN = 1.9;
// Claude Code warns at 250k of context, which is about 170k above its ~78k starting point.
// Slightly earlier here because the estimate is looser than a real count.
const HEAVY_GROWTH_TOKENS = 150000;

// Cursor lines: { role, message: { content: [...] } }. Claude Code: { type, message: {...} }.
function countLine(line, tally) {
  let entry;
  try {
    entry = JSON.parse(line);
  } catch {
    return;
  }
  const role = entry.role || entry.type;
  const content = entry.message && entry.message.content;
  if (role !== 'assistant' || !Array.isArray(content)) return;
  for (const block of content) {
    if (block.type === 'text' && typeof block.text === 'string') {
      tally.chars += block.text.length;
    } else if (block.type === 'tool_use') {
      tally.toolCalls += 1;
      tally.chars += JSON.stringify(block.input || {}).length;
    }
  }
}

function estimateContextGrowth(transcriptPath) {
  if (!transcriptPath) return null;
  let text;
  try {
    text = fs.readFileSync(transcriptPath, 'utf8');
  } catch {
    return null;
  }
  const tally = { toolCalls: 0, chars: 0 };
  for (const line of text.split('\n')) {
    if (line.trim()) countLine(line, tally);
  }
  const growth = INTERCEPT
    + tally.toolCalls * PER_TOOL_CALL
    + (tally.chars / 4) * PER_WRITTEN_TOKEN;
  return { growth: Math.round(growth), toolCalls: tally.toolCalls };
}

module.exports = { estimateContextGrowth, HEAVY_GROWTH_TOKENS };
