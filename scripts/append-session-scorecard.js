/**
 * FILE: scripts/append-session-scorecard.js
 * PURPOSE: Task tracking + session metrics — bump writes tracking; finalize writes metrics.
 *          Agents WRITE via this script only — never read the generated HTML logs.
 *          This file only parses the command line; the work lives in:
 *            session-scorecard-ops.js   bump, finalize, regenerate
 *            session-metrics-store.js   metrics jsonl + running tally file
 *            session-metrics-html.js    metrics page (cards: session-metrics-card.js)
 *            session-tracking-store.js  tracking jsonl (page: session-tracking-html.js)
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { backfillTrackingFromRunning } = require('./session-tracking-store');
const { TRACKING_URL, METRICS_URL } = require('./session-metrics-html');
const {
  ROOT,
  readEntries,
  writeEntries,
  normalize,
  readRunning,
} = require('./session-metrics-store');
const {
  regenerate,
  regenerateTracking,
  bumpRunning,
  finalizeRunning,
} = require('./session-scorecard-ops');

function loadJsonArg(flag) {
  const idx = process.argv.indexOf(flag);
  if (idx === -1) return null;
  const p = process.argv[idx + 1];
  if (!p) throw new Error(`${flag} requires a path`);
  return JSON.parse(fs.readFileSync(path.resolve(p), 'utf8'));
}

function loadNewEntry() {
  const stdin = process.argv.includes('--stdin');
  const fileIdx = process.argv.indexOf('--file');
  if (stdin) {
    const raw = fs.readFileSync(0, 'utf8').trim();
    if (!raw) throw new Error('Empty stdin');
    return JSON.parse(raw);
  }
  if (fileIdx !== -1) {
    const p = process.argv[fileIdx + 1];
    if (!p) throw new Error('--file requires a path');
    return JSON.parse(fs.readFileSync(path.resolve(p), 'utf8'));
  }
  return null;
}

function main() {
  if (process.argv.includes('--rebuild')) {
    const n = regenerate();
    console.log(`Rebuilt metrics (${n} sessions) + tracking log`);
    console.log(`Tracking: ${TRACKING_URL}`);
    console.log(`Metrics: ${METRICS_URL}`);
    return;
  }
  if (process.argv.includes('--rebuild-tracking-from-running')) {
    const running = readRunning();
    if (!running) {
      console.log('No running file — nothing to backfill.');
      return;
    }
    const added = backfillTrackingFromRunning(ROOT, running);
    regenerateTracking();
    console.log(`Backfilled ${added} task(s) into session-tracking.jsonl. View: ${TRACKING_URL}`);
    return;
  }
  const bump = loadJsonArg('--bump-file');
  if (bump) {
    bumpRunning(bump);
    console.log(`Task logged. View: ${TRACKING_URL}`);
    return;
  }
  const finalize = loadJsonArg('--finalize-file');
  if (finalize) {
    finalizeRunning(finalize);
    console.log(`Session finalized to metrics jsonl. Tracking: ${TRACKING_URL} · Metrics: ${METRICS_URL}`);
    return;
  }
  const newEntry = loadNewEntry();
  if (!newEntry) {
    console.error(
      'Usage: --file path.json | --bump-file delta.json | --finalize-file meta.json | '
      + '--rebuild | --rebuild-tracking-from-running',
    );
    process.exit(1);
  }
  const entries = readEntries();
  entries.push(normalize(newEntry));
  writeEntries(entries);
  regenerate();
  console.log(`Appended metrics entry. Tracking: ${TRACKING_URL} · Metrics: ${METRICS_URL}`);
}

main();
