/**
 * FILE: scripts/session-tracking-stats.js
 * PURPOSE: Active time for a task window (from the hook's tool timeline) and the
 *          roll-ups on the tracking page: real token cost and chat size.
 *
 * History: 2026-09-08 removed indexFirst / pathCoverage / unexplainedSearches (they
 * measured artifacts). 2026-09-21 removed observed search/read counts and the
 * self-graded navigationPath — nothing ever read them back to make a decision.
 */
'use strict';

const TIMELINE_CAP = 600;

function pushTimelineEvent(running, event) {
  if (!running.toolTimeline) running.toolTimeline = [];
  running.toolTimeline.push(event);
  if (running.toolTimeline.length > TIMELINE_CAP) {
    running.toolTimeline = running.toolTimeline.slice(-TIMELINE_CAP);
  }
}

function toMs(iso) {
  return new Date(iso || 0).getTime();
}

function sliceTimeline(timeline, fromIso, toIso) {
  const from = toMs(fromIso);
  const to = new Date(toIso || Date.now()).getTime();
  return (timeline || []).filter((ev) => {
    const t = toMs(ev.t);
    return !Number.isNaN(t) && t > from && t <= to;
  });
}

function consumeTimelineUpTo(timeline, toIso) {
  const to = new Date(toIso || Date.now()).getTime();
  return (timeline || []).filter((ev) => {
    const t = toMs(ev.t);
    return Number.isNaN(t) || t > to;
  });
}

// First to last tool call in the window — excludes the idle gap before Chase's prompt.
function activeMsInWindow(events) {
  const times = (events || []).map((ev) => toMs(ev.t)).filter((t) => !Number.isNaN(t));
  if (times.length < 2) return 0;
  return Math.max(0, Math.max(...times) - Math.min(...times));
}

function formatDurationMs(ms) {
  const n = Math.max(0, Number(ms) || 0);
  if (n < 1000) return `${n}ms`;
  const sec = Math.floor(n / 1000);
  if (sec < 60) return `${sec}s`;
  const min = Math.floor(sec / 60);
  const remSec = sec % 60;
  if (min < 60) return remSec ? `${min}m ${remSec}s` : `${min}m`;
  const hr = Math.floor(min / 60);
  const remMin = min % 60;
  return remMin ? `${hr}h ${remMin}m` : `${hr}h`;
}

function median(values) {
  const nums = (values || []).filter((n) => Number.isFinite(n)).sort((a, b) => a - b);
  if (!nums.length) return null;
  const mid = Math.floor(nums.length / 2);
  return nums.length % 2 ? nums[mid] : (nums[mid - 1] + nums[mid]) / 2;
}

function rollup(entries) {
  const costed = (entries || []).filter((e) => Number.isFinite(e.billedTokens));
  const billed = costed.map((e) => e.billedTokens);
  const cacheRead = costed.reduce((s, e) => s + (e.tokensCacheRead || 0), 0);
  const total = billed.reduce((a, b) => a + b, 0);
  return {
    costedTaskCount: costed.length,
    medianBilledTokens: median(billed),
    totalBilledTokens: total,
    medianTokensPerTurn: median(costed.map((e) => e.tokensPerTurn)),
    cacheReadPct: total ? Math.round((cacheRead / total) * 100) : null,
  };
}

module.exports = {
  TIMELINE_CAP,
  pushTimelineEvent,
  sliceTimeline,
  consumeTimelineUpTo,
  activeMsInWindow,
  formatDurationMs,
  median,
  rollup,
};
