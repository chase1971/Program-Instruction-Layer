/**
 * FILE: scripts/session-metrics-store.js
 * PURPOSE: Read/write session-scorecards.jsonl (one finalized session per line) and the
 *          running tally file that bumps accumulate into until finalize.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { emptyTrustFields } = require('./scorecard-trust');

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
  if (entry.docsRules && !entry.docsRulesOpened) entry.docsRulesOpened = entry.docsRules;
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

function emptyRunning() {
  return {
    sessionStarted: new Date().toISOString(),
    model: '',
    sessionType: 'mixed',
    summaryHuman: 'Session in progress…',
    turns: 0,
    greps: 0,
    corrections: 0,
    docsRulesOpened: [],
    mdcReadsList: [],
    filesReadList: [],
    filesEditedList: [],
    toolsUsedCounts: {},
    browserSnapshots: 0,
    taskLog: [],
    lastTrackingBumpAt: null,
    toolTimeline: [],
    hookTally: false,
    agentBumped: false,
    ...emptyTrustFields(),
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
