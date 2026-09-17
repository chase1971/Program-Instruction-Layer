/**
 * FILE: scripts/chat-task.js
 * PURPOSE: Identify which chat a hook fired in, and keep a per-chat message count.
 *
 * Why this exists: the running scorecard file spans everything since the last
 * end-of-session finalize — several chats, across Cursor and Claude Code. The
 * context warning used to count messages there, so a fresh task opened right after
 * a momentum handoff inherited the old task's count (14 on a 1-message task,
 * 2026-09-11). Counts here are keyed by chat, so a new chat starts at zero.
 *
 * Only `scorecard-enforce.js --context-warning` writes the state file, so the two
 * hooks that fire on every prompt never overwrite each other's data.
 */
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const STATE = path.join(ROOT, 'agent docs', '.chat-task-state.json');
const MAX_CHATS = 40;

// Cursor sends conversation_id; its transcript lives at
// ~/.cursor/projects/<workspace>/agent-transcripts/<id>/<id>.jsonl.
function findCursorTranscript(conversationId) {
  const projects = path.join(os.homedir(), '.cursor', 'projects');
  let dirs;
  try {
    dirs = fs.readdirSync(projects);
  } catch {
    return null;
  }
  for (const dir of dirs) {
    const p = path.join(projects, dir, 'agent-transcripts', conversationId, `${conversationId}.jsonl`);
    if (fs.existsSync(p)) return p;
  }
  return null;
}

// Claude Code sends session_id + transcript_path. Cursor sends conversation_id.
function resolveChat(payload) {
  const p = payload || {};
  const conversationId = p.conversation_id || p.conversationId || null;
  const transcriptPath = p.transcript_path || p.transcriptPath
    || (conversationId ? findCursorTranscript(String(conversationId)) : null);
  const chatKey = p.session_id || p.sessionId || conversationId || transcriptPath || null;
  return {
    chatKey: chatKey ? String(chatKey) : null,
    transcriptPath: transcriptPath || null,
  };
}

function readState() {
  try {
    return JSON.parse(fs.readFileSync(STATE, 'utf8')) || {};
  } catch {
    return {};
  }
}

function writeState(state) {
  const newest = Object.keys(state)
    .sort((a, b) => String(state[b].updatedAt).localeCompare(String(state[a].updatedAt)))
    .slice(0, MAX_CHATS);
  const kept = {};
  for (const key of newest) kept[key] = state[key];
  try {
    fs.writeFileSync(STATE, JSON.stringify(kept, null, 2), 'utf8');
  } catch {
    // Fail open — hooks must never block Chase on a state write.
  }
}

function updateChat(chatKey, change) {
  const state = readState();
  const now = new Date().toISOString();
  const row = state[chatKey] || { prompts: 0, lastWarnedAtPrompt: 0, startedAt: now };
  state[chatKey] = { ...change(row), updatedAt: now };
  writeState(state);
  return state[chatKey];
}

// Count one more message from Chase in this chat; returns the chat's row after it.
function recordPrompt(chatKey) {
  return updateChat(chatKey, (row) => ({ ...row, prompts: (row.prompts || 0) + 1 }));
}

function readChat(chatKey) {
  if (!chatKey) return null;
  return readState()[chatKey] || null;
}

function transcriptKB(transcriptPath) {
  if (!transcriptPath) return null;
  try {
    return Math.round(fs.statSync(transcriptPath).size / 1024);
  } catch {
    return null;
  }
}

module.exports = {
  resolveChat,
  recordPrompt,
  updateChat,
  readChat,
  transcriptKB,
};
