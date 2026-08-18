/**
 * FILE: scripts/session-tracking-stats.js
 * PURPOSE: Reconcile hook-observed tool timeline against agent navigationPath.
 */
'use strict';

const path = require('path');
const { flattenSteps, normalizeNavigationPath } = require('./scorecard-navigation-path');

const TIMELINE_CAP = 600;
const SEARCH_KINDS = new Set(['grep', 'glob', 'web', 'search']);
const DOC_KINDS = new Set(['doc', 'doc-index']);

function isIndexLike(filePath) {
  const norm = String(filePath || '').replace(/\\/g, '/').toLowerCase();
  if (!norm) return false;
  const base = path.basename(norm);
  return (
    base === 'index.md'
    || base === 'agents.md'
    || base === 'claude.md'
    || base === 'app_locations.md'
  );
}

function pushTimelineEvent(running, event) {
  if (!running.toolTimeline) running.toolTimeline = [];
  running.toolTimeline.push(event);
  if (running.toolTimeline.length > TIMELINE_CAP) {
    running.toolTimeline = running.toolTimeline.slice(-TIMELINE_CAP);
  }
}

function sliceTimeline(timeline, fromIso, toIso) {
  const from = new Date(fromIso || 0).getTime();
  const to = new Date(toIso || Date.now()).getTime();
  return (timeline || []).filter((ev) => {
    const t = new Date(ev.t || 0).getTime();
    if (Number.isNaN(t)) return false;
    return t > from && t <= to;
  });
}

function consumeTimelineUpTo(timeline, toIso) {
  const to = new Date(toIso || Date.now()).getTime();
  const list = timeline || [];
  const remaining = list.filter((ev) => {
    const t = new Date(ev.t || 0).getTime();
    return Number.isNaN(t) || t > to;
  });
  return remaining;
}

function navEventsInWindow(events) {
  return (events || []).filter((ev) => ev.k === 'search' || ev.k === 'doc-read' || ev.k === 'read');
}

function observeWindow(events) {
  const nav = navEventsInWindow(events);
  let observedSearches = 0;
  let observedDocReads = 0;
  let observedReads = 0;
  let searchesBeforeFirstDoc = 0;
  let indexFirst = false;
  let sawDoc = false;
  let firstNavDecided = false;

  for (const ev of nav) {
    if (ev.k === 'search') {
      observedSearches += 1;
      if (!sawDoc) searchesBeforeFirstDoc += 1;
      if (!firstNavDecided) {
        indexFirst = false;
        firstNavDecided = true;
      }
    } else if (ev.k === 'doc-read') {
      observedDocReads += 1;
      if (!firstNavDecided) {
        indexFirst = isIndexLike(ev.p);
        firstNavDecided = true;
      }
      sawDoc = true;
    } else if (ev.k === 'read') {
      observedReads += 1;
    }
  }

  let activeMs = 0;
  if (events.length >= 2) {
    const times = events
      .map((ev) => new Date(ev.t || 0).getTime())
      .filter((t) => !Number.isNaN(t));
    if (times.length >= 2) {
      activeMs = Math.max(0, Math.max(...times) - Math.min(...times));
    }
  }

  const observedNavEvents = observedSearches + observedDocReads + observedReads;

  return {
    observedSearches,
    observedDocReads,
    observedReads,
    observedNavEvents,
    searchesBeforeFirstDoc,
    indexFirst,
    activeMs,
    hasObservedData: nav.length > 0,
  };
}

function countLoggedSearchSteps(navigationPath) {
  const flat = flattenSteps(normalizeNavigationPath(navigationPath));
  return flat.filter((s) => SEARCH_KINDS.has(String(s.kind || '').toLowerCase())).length;
}

function reconcile(observed, navigationPath) {
  const stepCount = flattenSteps(normalizeNavigationPath(navigationPath)).length;
  const loggedSearches = countLoggedSearchSteps(navigationPath);
  const unexplainedSearches = Math.max(
    0,
    (observed.observedSearches || 0) - loggedSearches,
  );
  const pathCoverage = observed.observedNavEvents > 0
    ? Math.min(1, stepCount / observed.observedNavEvents)
    : (stepCount > 0 ? 1 : 0);

  return {
    unexplainedSearches,
    pathCoverage,
    loggedSearches,
  };
}

function hasObservedFields(entry) {
  return entry && (
    entry.hasObservedData === true
    || typeof entry.observedSearches === 'number'
    || typeof entry.observedNavEvents === 'number'
  );
}

function median(values) {
  const nums = (values || []).filter((n) => Number.isFinite(n)).sort((a, b) => a - b);
  if (!nums.length) return null;
  const mid = Math.floor(nums.length / 2);
  return nums.length % 2 ? nums[mid] : (nums[mid - 1] + nums[mid]) / 2;
}

function pct(n, total) {
  if (!total) return null;
  return Math.round((n / total) * 100);
}

function rollup(entries) {
  const observed = (entries || []).filter(hasObservedFields);
  const indexFirstCount = observed.filter((e) => e.indexFirst).length;
  const deadEndSteps = observed.reduce((s, e) => s + (e.deadEndCount || 0), 0);
  const totalSteps = observed.reduce((s, e) => s + (e.stepCount || 0), 0);
  const coverageValues = observed
    .filter((e) => (e.observedNavEvents || 0) > 0)
    .map((e) => e.pathCoverage ?? 0);
  const searchesBeforeDocValues = observed.map((e) => e.searchesBeforeFirstDoc ?? 0);

  return {
    observedTaskCount: observed.length,
    indexFirstRate: pct(indexFirstCount, observed.length),
    indexFirstCount,
    deadEndRate: pct(deadEndSteps, totalSteps),
    deadEndSteps,
    totalSteps,
    medianSearchesBeforeDoc: median(searchesBeforeDocValues),
    medianPathCoverage: median(coverageValues),
  };
}

function collectIndexFailures(entries, limit = 20) {
  const failures = [];
  const sorted = [...(entries || [])].sort(
    (a, b) => new Date(b.timestamp) - new Date(a.timestamp),
  );
  for (const entry of sorted) {
    const flat = flattenSteps(normalizeNavigationPath(entry.navigationPath || []));
    for (const step of flat) {
      if (!DOC_KINDS.has(String(step.kind || '').toLowerCase())) continue;
      if (step.outcome !== 'partial' && step.outcome !== 'dead-end') continue;
      failures.push({
        timestamp: entry.timestamp,
        chunkNote: entry.chunkNote,
        target: step.target,
        outcome: step.outcome,
        note: step.note || '',
      });
      if (failures.length >= limit) return failures;
    }
  }
  return failures;
}

module.exports = {
  TIMELINE_CAP,
  isIndexLike,
  pushTimelineEvent,
  sliceTimeline,
  consumeTimelineUpTo,
  observeWindow,
  reconcile,
  hasObservedFields,
  rollup,
  collectIndexFailures,
};
