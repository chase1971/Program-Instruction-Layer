/**
 * FILE: scripts/session-scorecard-ops.js
 * PURPOSE: What the append-session-scorecard.js commands do — bump a task into the
 *          running tally, finalize a session into metrics, regenerate both HTML logs.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { refreshCountsTrust } = require('./scorecard-trust');
const { consumeTimelineUpTo } = require('./session-tracking-stats');
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
  const running = readRunning();
  fs.writeFileSync(METRICS_HTML, buildHtml(entries, running), 'utf8');
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

function mergeUnique(list, add) {
  const set = new Set(list || []);
  for (const x of add || []) if (x) set.add(x);
  return [...set];
}

function deriveFinalizeConfidence(meta, running, base) {
  const withTrust = refreshCountsTrust({
    ...base,
    agentBumped: !!(running && running.agentBumped),
    bumped: !!(running && running.agentBumped),
    summarized: !!meta.summarized || !!base.summarized,
    taskLog: base.taskLog,
    taskBumpCount: Array.isArray(base.taskLog) ? base.taskLog.length : 0,
  });
  return withTrust.countsTrust;
}

function bumpRunning(delta) {
  let r = readRunning() || emptyRunning();
  if (delta.model) r.model = delta.model;
  if (delta.sessionType) r.sessionType = delta.sessionType;
  if (delta.summaryHuman) r.summaryHuman = delta.summaryHuman;
  if (delta.summarized) r.summarized = true;
  r.turns += Number(delta.addTurns || 0);
  r.greps += Number(delta.addGreps || 0);
  r.corrections += Number(delta.addCorrections || 0);
  r.filesReadList = mergeUnique(r.filesReadList, delta.filesRead);
  r.filesEditedList = mergeUnique(r.filesEditedList, delta.filesEdited);
  r.docsRulesOpened = mergeUnique(r.docsRulesOpened, delta.docsRulesOpened);
  r.mdcReadsList = mergeUnique(r.mdcReadsList, delta.mdcReadsList);
  const bumpTime = new Date().toISOString();
  const shouldTrack =
    delta.chunkNote
    || delta.addGreps
    || delta.addTurns
    || delta.addCorrections
    || (delta.filesRead && delta.filesRead.length)
    || (delta.filesEdited && delta.filesEdited.length)
    || (delta.docsRulesOpened && delta.docsRulesOpened.length)
    || (delta.navigationPath && delta.navigationPath.length);

  if (shouldTrack) {
    const trackingEntry = buildTrackingEntry(delta, r, bumpTime);
    appendTrackingEntry(ROOT, trackingEntry);
    r.lastTrackingBumpAt = bumpTime;
    r.toolTimeline = consumeTimelineUpTo(r.toolTimeline, bumpTime);
  }

  if (delta.chunkNote) {
    if (!r.taskLog) r.taskLog = [];
    r.taskLog.push({
      time: bumpTime,
      note: delta.chunkNote,
      addGreps: delta.addGreps || 0,
      filesRead: delta.filesRead || [],
      filesEdited: delta.filesEdited || [],
      navigationPath: delta.navigationPath || [],
    });
  }
  if (
    delta.chunkNote
    || delta.addGreps
    || delta.addTurns
    || delta.addCorrections
    || (delta.filesRead && delta.filesRead.length)
    || (delta.filesEdited && delta.filesEdited.length)
    || (delta.docsRulesOpened && delta.docsRulesOpened.length)
  ) {
    r.agentBumped = true;
    r.stopBlockCount = 0;
  }
  refreshCountsTrust(r);
  writeRunning(r);
  regenerate();
  return r;
}

function finalizeRunning(meta) {
  const r = readRunning();
  const base = r || emptyRunning();
  if (meta.summarized) base.summarized = true;
  refreshCountsTrust(base);
  const entry = normalize({
    timestamp: meta.timestamp || new Date().toISOString(),
    model: meta.model || base.model,
    sessionType: meta.sessionType || base.sessionType,
    summaryHuman: meta.summaryHuman || base.summaryHuman,
    outcome: meta.outcome || 'Done',
    summarized: !!meta.summarized || !!base.summarized,
    // Derived, never self-reported: a running file only exists if bumps were logged.
    // Separates "the chat was summarized" from "the agent forgot to bump" — different
    // failures, different fixes. Counts reconstructed at the end are guesses.
    bumped: !!(r && r.agentBumped),
    hookTally: !!base.hookTally,
    confidence: deriveFinalizeConfidence(meta, r, base),
    countsTrust: base.countsTrust,
    missingEarlyWork: base.missingEarlyWork,
    preHookWorkUntracked: base.preHookWorkUntracked,
    hookFirstTallyAt: base.hookFirstTallyAt || null,
    turns: base.turns + Number(meta.addTurns || 0),
    greps: base.greps,
    corrections: base.corrections + Number(meta.addCorrections || 0),
    docsRulesOpened: base.docsRulesOpened.length ? base.docsRulesOpened : 'none',
    filesReadList: base.filesReadList,
    filesEditedList: base.filesEditedList,
    mdcReadsList: base.mdcReadsList || [],
    toolsUsedCounts: base.toolsUsedCounts || {},
    browserSnapshots: base.browserSnapshots || 0,
    worthNoting: meta.worthNoting || '',
    captureCandidate: meta.captureCandidate || '',
    nextSession: meta.nextSession || '',
    taskBumpCount: Array.isArray(base.taskLog) ? base.taskLog.length : 0,
    taskLog: base.taskLog || [],
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
