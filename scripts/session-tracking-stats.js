/**
 * FILE: scripts/session-tracking-stats.js
 * PURPOSE: Summarise the hook-observed tool timeline for a task window, and
 *          roll up the two signals that survived the 2026-09-08 audit:
 *          real token cost, and doc steps that failed to route.
 */
'use strict';

const { flattenSteps, normalizeNavigationPath } = require('./scorecard-navigation-path');

const TIMELINE_CAP = 600;
const DOC_KINDS = new Set(['doc', 'doc-index']);

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

// NOTE (2026-09-08 trim): `indexFirst` and `searchesBeforeFirstDoc` were removed.
// They read the hook's tool timeline to decide whether the agent consulted an
// index first — but AGENTS.md and CLAUDE.md are auto-loaded into context by the
// harness and never pass through a Read tool. The hook therefore could not see
// the most-used index at all, and `indexFirst` scored 0/233 across the whole log
// while `agent docs/INDEX.md` was the single most-visited doc in it. A metric
// that reports 0% for something happening constantly is worse than no metric.
function observeWindow(events) {
  const nav = navEventsInWindow(events);
  let observedSearches = 0;
  let observedDocReads = 0;
  let observedReads = 0;

  for (const ev of nav) {
    if (ev.k === 'search') observedSearches += 1;
    else if (ev.k === 'doc-read') observedDocReads += 1;
    else if (ev.k === 'read') observedReads += 1;
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
    activeMs,
    hasObservedData: nav.length > 0,
  };
}

// NOTE (2026-09-08 trim): `reconcile()` computed `unexplainedSearches` and
// `pathCoverage`. Both were artifacts.
//   - unexplainedSearches counted a logged step as a search only when `kind` was
//     grep/glob/web/search. Agents invented 59 distinct `kind` values across the
//     log, so 4,775 of 4,813 searches (99.2%) scored "unexplained". It measured
//     vocabulary drift, not honesty.
//   - pathCoverage divided logged steps by observed tool events. Because a bump
//     covers a whole deliverable (median 17min, p90 9.6h), it mostly measured how
//     long it had been since the last bump. Median 0.24 was window length, not
//     a summarising agent.
// Real cost per task now comes from session-token-cost.js instead.

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
  const deadEndSteps = observed.reduce((s, e) => s + (e.deadEndCount || 0), 0);
  const totalSteps = observed.reduce((s, e) => s + (e.stepCount || 0), 0);

  const costed = (entries || []).filter((e) => Number.isFinite(e.billedTokens));
  const billedValues = costed.map((e) => e.billedTokens);
  const perTurnValues = costed.map((e) => e.tokensPerTurn).filter(Number.isFinite);

  return {
    observedTaskCount: observed.length,
    deadEndRate: pct(deadEndSteps, totalSteps),
    deadEndSteps,
    totalSteps,
    costedTaskCount: costed.length,
    medianBilledTokens: median(billedValues),
    totalBilledTokens: billedValues.reduce((a, b) => a + b, 0),
    medianTokensPerTurn: median(perTurnValues),
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
  pushTimelineEvent,
  sliceTimeline,
  consumeTimelineUpTo,
  observeWindow,
  hasObservedFields,
  rollup,
  collectIndexFailures,
};
