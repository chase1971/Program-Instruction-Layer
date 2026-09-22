/**
 * FILE: scripts/session-metrics-store.js
 * PURPOSE: Read/write session-scorecards.jsonl (one finalized session per line) and the
 *          running tally file that bumps accumulate into until finalize.
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const DATA = path.join(ROOT, 'agent docs', 'session-scorecards.jsonl');
const RUNNING = path.join(ROOT, 'agent docs', '.session-scorecard-running.json');

function readEntries() {
  if (!fs.existsSync(DATA)) return [];
  return fs
    .readFileSync(DATA, 'utf8')
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean)
    .map((l, i) => {
      try {
        return JSON.parse(l);
      } catch (e) {
        throw new Error(`Invalid JSONL line ${i + 1}: ${e.message}`);
      }
    });
}

function writeEntries(entries) {
  const body = entries.map((e) => JSON.stringify(e)).join('\n') + (entries.length ? '\n' : '');
  fs.writeFileSync(DATA, body, 'utf8');
}

function normalize(entry) {
  if (!entry.timestamp) entry.timestamp = new Date().toISOString();
  if (entry.spike && !entry.worthNoting) entry.worthNoting = entry.spike;
  return entry;
}

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

function clearRunning() {
  if (fs.existsSync(RUNNING)) fs.unlinkSync(RUNNING);
}

// Hook-maintained fields: turns (one per prompt), filesEditedList (the Stop hook's
// evidence of unbumped work), toolTimeline (active time), chatKey/transcriptPath.
function emptyRunning() {
  return {
    sessionStarted: new Date().toISOString(),
    model: '',
    sessionType: 'mixed',
    summaryHuman: 'Session in progress…',
    turns: 0,
    corrections: 0,
    filesEditedList: [],
    taskLog: [],
    lastTrackingBumpAt: null,
    toolTimeline: [],
    agentBumped: false,
  };
}

module.exports = {
  ROOT,
  readEntries,
  writeEntries,
  normalize,
  readRunning,
  writeRunning,
  clearRunning,
  emptyRunning,
};
