/**
 * FILE: scripts/session-scorecard-ops.js
 * PURPOSE: What the append-session-scorecard.js commands do — bump a task into the
 *          running tally, finalize a session into metrics, regenerate both HTML logs.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { consumeTimelineUpTo } = require('./session-tracking-stats');
const { normalizeIndexGaps } = require('./session-index-gaps');
const {
  readTrackingEntries,
  appendTrackingEntry,
  buildTrackingEntry,
} = require('./session-tracking-store');
const { buildTrackingHtml } = require('./session-tracking-html');
const { buildHtml } = require('./session-metrics-html');
const {
  ROOT,
  readEntries,
  writeEntries,
  normalize,
  readRunning,
  writeRunning,
  clearRunning,
  emptyRunning,
} = require('./session-metrics-store');

const METRICS_HTML = path.join(ROOT, 'agent docs', 'session-metrics-log.html');
const TRACKING_HTML = path.join(ROOT, 'agent docs', 'session-tracking-log.html');

function regenerateMetrics() {
  const entries = readEntries();
  fs.writeFileSync(METRICS_HTML, buildHtml(entries, readRunning()), 'utf8');
  return entries.length;
}

function regenerateTracking() {
  const entries = readTrackingEntries(ROOT);
  fs.writeFileSync(TRACKING_HTML, buildTrackingHtml(entries), 'utf8');
  return entries.length;
}

function regenerate() {
  const n = regenerateMetrics();
  regenerateTracking();
  return n;
}

function bumpRunning(delta) {
  const r = readRunning() || emptyRunning();
  if (delta.sessionType) r.sessionType = delta.sessionType;
  if (delta.summaryHuman) r.summaryHuman = delta.summaryHuman;
  if (delta.summarized) r.summarized = true;
  r.corrections = (r.corrections || 0) + Number(delta.addCorrections || 0);

  const bumpTime = new Date().toISOString();
  // Throws (logging nothing) when chunkNote is missing or indexGaps is malformed.
  const trackingEntry = buildTrackingEntry(delta, r, bumpTime);
  appendTrackingEntry(ROOT, trackingEntry);
  if (trackingEntry.model) r.model = trackingEntry.model;
  r.lastTrackingBumpAt = bumpTime;
  r.toolTimeline = consumeTimelineUpTo(r.toolTimeline, bumpTime);
  if (!r.taskLog) r.taskLog = [];
  r.taskLog.push({
    time: bumpTime,
    note: trackingEntry.chunkNote,
    ...(trackingEntry.indexGaps ? { indexGaps: trackingEntry.indexGaps } : {}),
  });
  r.agentBumped = true;
  r.stopBlockCount = 0;
  writeRunning(r);
  regenerate();
  return r;
}

// Session cost = sum of its task rows. Cursor rows carry chat size instead of tokens.
function sessionCost(sessionId) {
  const rows = readTrackingEntries(ROOT).filter((e) => e.sessionId === sessionId);
  const costed = rows.filter((e) => Number.isFinite(e.billedTokens));
  const out = {};
  if (costed.length) {
    out.billedTokens = costed.reduce((s, e) => s + e.billedTokens, 0);
    out.tokenTurns = costed.reduce((s, e) => s + (e.tokenTurns || 0), 0);
    out.peakTokensPerTurn = Math.max(...costed.map((e) => e.tokensPerTurn || 0));
  }
  const msgs = rows.map((e) => e.chatUserMessages).filter(Number.isFinite);
  if (msgs.length) out.chatUserMessages = Math.max(...msgs);
  return out;
}

function finalizeRunning(meta) {
  const r = readRunning();
  const base = r || emptyRunning();
  const taskLog = Array.isArray(base.taskLog) ? base.taskLog : [];
  const entry = normalize({
    timestamp: meta.timestamp || new Date().toISOString(),
    model: meta.model || base.model || '',
    sessionType: meta.sessionType || base.sessionType,
    summaryHuman: meta.summaryHuman || base.summaryHuman,
    outcome: meta.outcome || 'Done',
    summarized: !!meta.summarized || !!base.summarized,
    // Derived, never self-reported: a running file only exists if bumps were logged.
    bumped: !!(r && r.agentBumped),
    turns: (base.turns || 0) + Number(meta.addTurns || 0),
    corrections: (base.corrections || 0) + Number(meta.addCorrections || 0),
    ...sessionCost(base.sessionStarted),
    worthNoting: meta.worthNoting || '',
    captureCandidate: meta.captureCandidate || '',
    nextSession: meta.nextSession || '',
    taskBumpCount: taskLog.length,
    taskLog: taskLog.map((t) => ({
      time: t.time,
      note: t.note,
      ...(normalizeIndexGaps(t.indexGaps).length ? { indexGaps: t.indexGaps } : {}),
    })),
  });
  const entries = readEntries();
  entries.push(entry);
  writeEntries(entries);
  clearRunning();
  regenerate();
  return entry;
}

module.exports = {
  regenerate,
  regenerateTracking,
  bumpRunning,
  finalizeRunning,
};
