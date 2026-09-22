/**
 * FILE: scripts/scorecard-hook-tally.js
 * PURPOSE: PostToolUse + UserPromptSubmit hook (Cursor, Claude Code, Codex). Keeps the
 *          running tally the bump reads:
 *            turns            one per prompt from Chase
 *            filesEditedList  evidence of unbumped work for the Stop hook
 *            toolTimeline     timestamps, for active time per task
 *            chatKey / transcriptPath / model
 *          Stdin: hook JSON. Always exits 0 (fail open).
 *
 * 2026-09-21: stopped counting greps, files read, docs opened, .mdc reads and tool
 * usage. Nothing downstream used them to make a decision.
 *
 * Manual smoke test:
 *   echo {"tool_name":"Edit","tool_input":{"file_path":"foo.ts"}} | node scripts/scorecard-hook-tally.js
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { pushTimelineEvent } = require('./session-tracking-stats');
const { resolveChat } = require('./chat-task');
const { emptyRunning } = require('./session-metrics-store');

const ROOT = path.join(__dirname, '..');
const RUNNING = path.join(ROOT, 'agent docs', '.session-scorecard-running.json');

// Cursor sends StrReplace/Delete/EditNotebook; Claude Code sends Edit/NotebookEdit.
const EDIT_TOOLS = new Set([
  'Write', 'StrReplace', 'Delete', 'EditNotebook',
  'Edit', 'NotebookEdit',
]);

function readRunning() {
  if (!fs.existsSync(RUNNING)) return null;
  try {
    return JSON.parse(fs.readFileSync(RUNNING, 'utf8'));
  } catch {
    return null;
  }
}

function writeRunning(data) {
  fs.writeFileSync(RUNNING, JSON.stringify(data, null, 2), 'utf8');
}

function pickPath(toolInput) {
  if (!toolInput || typeof toolInput !== 'object') return null;
  const raw = toolInput.path || toolInput.file_path || toolInput.target_path || toolInput.target_notebook;
  return typeof raw === 'string' ? raw.replace(/\\/g, '/') : null;
}

// Remember which chat and transcript the latest hook came from, so a bump can slice
// that chat's billed tokens (Claude Code only — see scripts/session-token-cost.js)
// and read its size (both hosts — see scripts/chat-task.js). Both fields move
// together so a Cursor chat never inherits a stale Claude Code transcript.
function recordChat(running, payload) {
  const { chatKey, transcriptPath } = resolveChat(payload);
  if (chatKey || transcriptPath) {
    running.chatKey = chatKey;
    running.transcriptPath = transcriptPath;
  }
  if (typeof payload.model === 'string' && payload.model.trim()) running.model = payload.model.trim();
}

function isPromptEvent(payload) {
  const eventName = String(payload.hook_event_name || payload.hookEventName || '').trim();
  return payload.prompt !== undefined
    || eventName === 'UserPromptSubmit'
    || eventName === 'beforeSubmitPrompt';
}

function record(payload) {
  const running = readRunning() || emptyRunning();
  recordChat(running, payload);

  const toolName = String(payload.tool_name || payload.toolName || '').trim();
  if (!toolName) {
    if (isPromptEvent(payload)) running.turns = (running.turns || 0) + 1;
    writeRunning(running);
    return;
  }

  const now = new Date().toISOString();
  pushTimelineEvent(running, { t: now });
  if (EDIT_TOOLS.has(toolName)) {
    const filePath = pickPath(payload.tool_input || payload.toolInput || payload.arguments || {});
    if (filePath && !(running.filesEditedList || []).includes(filePath)) {
      running.filesEditedList = [...(running.filesEditedList || []), filePath];
    }
  }
  writeRunning(running);
}

function main() {
  const chunks = [];
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', (chunk) => chunks.push(chunk));
  process.stdin.on('end', () => {
    try {
      const raw = chunks.join('').trim();
      if (raw) record(JSON.parse(raw));
    } catch {
      // Fail open — never block the agent on tally errors.
    }
    process.exit(0);
  });
}

main();
