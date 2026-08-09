/**
 * FILE: scripts/session-tracking-store.js
 * PURPOSE: Read/write session-tracking.jsonl — one entry per task bump.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const {
  normalizeNavigationPath,
  summarizeNavigationPath,
  formatDurationMs,
} = require('./scorecard-navigation-path');

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
  const file = trackingDataPath(root);
  fs.appendFileSync(file, `${JSON.stringify(entry)}\n`, 'utf8');
}

function writeTrackingEntries(root, entries) {
  const file = trackingDataPath(root);
  const body = entries.map((e) => JSON.stringify(e)).join('\n') + (entries.length ? '\n' : '');
  fs.writeFileSync(file, body, 'utf8');
}

function durationSince(prevIso, nextIso) {
  const prev = new Date(prevIso || 0).getTime();
  const next = new Date(nextIso || Date.now()).getTime();
  if (Number.isNaN(prev) || Number.isNaN(next)) return 0;
  return Math.max(0, next - prev);
}

function buildTrackingEntry(delta, running, timestamp = new Date().toISOString()) {
  const sessionId = running.sessionStarted || timestamp;
  const prevAt = running.lastTrackingBumpAt || sessionId;
  const durationMs = durationSince(prevAt, timestamp);
  const navigationPath = normalizeNavigationPath(delta.navigationPath || []);
  const stats = summarizeNavigationPath(navigationPath);
  const chunkNote = String(delta.chunkNote || '').trim() || '(no task note)';

  return {
    id: timestamp,
    sessionId,
    timestamp,
    chunkNote,
    durationMs,
    durationLabel: formatDurationMs(durationMs),
    missingNavigationPath: navigationPath.length === 0,
    ...stats,
    navigationPath,
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
    const navigationPath = normalizeNavigationPath(task.navigationPath || []);
    const stats = summarizeNavigationPath(navigationPath);
    entries.push({
      id: timestamp,
      sessionId,
      timestamp,
      chunkNote: String(task.note || '').trim() || '(no task note)',
      durationMs,
      durationLabel: formatDurationMs(durationMs),
      missingNavigationPath: navigationPath.length === 0,
      backfilled: true,
      ...stats,
      navigationPath,
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
  taskLogToTrackingEntries,
};
