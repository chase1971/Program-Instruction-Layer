/**
 * FILE: scripts/session-tracking-store.js
 * PURPOSE: Read/write session-tracking.jsonl — one entry per task bump.
 *          An entry is: what was done (chunkNote), time, cost (tokens or chat size),
 *          model, and any index gaps. Everything but chunkNote and indexGaps is automatic.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const {
  validateIndexGaps,
  normalizeIndexGaps,
  gapsFromLegacyPath,
} = require('./session-index-gaps');
const {
  sliceTimeline,
  activeMsInWindow,
  formatDurationMs,
} = require('./session-tracking-stats');
const { readTranscriptUsage } = require('./session-token-cost');
const { readChat, transcriptKB } = require('./chat-task');

function trackingDataPath(root) {
  return path.join(root, 'agent docs', 'session-tracking.jsonl');
}

function readTrackingEntries(root) {
  const file = trackingDataPath(root);
  if (!fs.existsSync(file)) return [];
  return fs
    .readFileSync(file, 'utf8')
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean)
    .map((l, i) => {
      try {
        return JSON.parse(l);
      } catch (e) {
        throw new Error(`Invalid session-tracking.jsonl line ${i + 1}: ${e.message}`);
      }
    });
}

function appendTrackingEntry(root, entry) {
  fs.appendFileSync(trackingDataPath(root), `${JSON.stringify(entry)}\n`, 'utf8');
}

function writeTrackingEntries(root, entries) {
  const body = entries.map((e) => JSON.stringify(e)).join('\n') + (entries.length ? '\n' : '');
  fs.writeFileSync(trackingDataPath(root), body, 'utf8');
}

function durationSince(prevIso, nextIso) {
  const prev = new Date(prevIso || 0).getTime();
  const next = new Date(nextIso || Date.now()).getTime();
  if (Number.isNaN(prev) || Number.isNaN(next)) return 0;
  return Math.max(0, next - prev);
}

// A bump with no note is refused outright — a blank row is worse than no row.
function assertValidBump(delta) {
  const problems = [];
  if (!String(delta.chunkNote || '').trim()) {
    problems.push('chunkNote is required — one line saying what you finished');
  }
  problems.push(...validateIndexGaps(delta.indexGaps));
  if (problems.length) {
    throw new Error(
      'Bump rejected, nothing was logged. Fix it (agent docs/SESSION_TRACKING.md) '
      + `and rerun:\n  - ${problems.join('\n  - ')}`,
    );
  }
}

// Explicit gaps win; an agent still sending the retired navigationPath keeps only its failed doc steps.
function bumpGaps(delta) {
  if (Array.isArray(delta.indexGaps)) return normalizeIndexGaps(delta.indexGaps);
  return gapsFromLegacyPath(delta.navigationPath);
}

// Messages and transcript size for the chat this bump came from. The only cost signal
// in Cursor, which records no tokens; logged on every host so chats can be compared.
function chatSize(running) {
  const out = {};
  const chat = readChat(running.chatKey);
  if (chat) out.chatUserMessages = chat.prompts;
  const kb = transcriptKB(running.transcriptPath);
  if (Number.isFinite(kb)) out.chatTranscriptKB = kb;
  if (running.chatKey) out.chatId = String(running.chatKey).slice(0, 8);
  return out;
}

function buildTrackingEntry(delta, running, timestamp = new Date().toISOString()) {
  assertValidBump(delta);
  const sessionId = running.sessionStarted || timestamp;
  const prevAt = running.lastTrackingBumpAt || sessionId;
  const durationMs = durationSince(prevAt, timestamp);
  const activeMs = activeMsInWindow(sliceTimeline(running.toolTimeline, prevAt, timestamp));
  const cost = readTranscriptUsage(running.transcriptPath, prevAt, timestamp) || {};
  const model = cost.model || delta.model || running.model || '';
  const indexGaps = bumpGaps(delta);

  return {
    id: timestamp,
    sessionId,
    timestamp,
    chunkNote: String(delta.chunkNote).trim(),
    durationMs,
    durationLabel: formatDurationMs(durationMs),
    activeMs,
    activeLabel: formatDurationMs(activeMs),
    ...cost,
    ...(model ? { model } : {}),
    ...chatSize(running),
    ...(indexGaps.length ? { indexGaps } : {}),
  };
}

function taskLogToTrackingEntries(running) {
  const sessionId = running.sessionStarted;
  const tasks = Array.isArray(running.taskLog) ? running.taskLog : [];
  if (!sessionId || !tasks.length) return [];

  const entries = [];
  let prevAt = sessionId;
  for (const task of tasks) {
    const timestamp = task.time || new Date().toISOString();
    const durationMs = durationSince(prevAt, timestamp);
    const indexGaps = normalizeIndexGaps(task.indexGaps);
    entries.push({
      id: timestamp,
      sessionId,
      timestamp,
      chunkNote: String(task.note || '').trim() || '(no task note)',
      durationMs,
      durationLabel: formatDurationMs(durationMs),
      backfilled: true,
      ...(indexGaps.length ? { indexGaps } : {}),
    });
    prevAt = timestamp;
  }
  return entries;
}

function backfillTrackingFromRunning(root, running) {
  const existing = readTrackingEntries(root);
  const existingIds = new Set(existing.map((e) => e.id));
  const toAdd = taskLogToTrackingEntries(running).filter((e) => !existingIds.has(e.id));
  if (!toAdd.length) return 0;
  writeTrackingEntries(root, [...existing, ...toAdd]);
  return toAdd.length;
}

module.exports = {
  trackingDataPath,
  readTrackingEntries,
  appendTrackingEntry,
  writeTrackingEntries,
  buildTrackingEntry,
  backfillTrackingFromRunning,
};
