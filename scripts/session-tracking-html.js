/**
 * FILE: scripts/session-tracking-html.js
 * PURPOSE: Build session-tracking-log.html — one collapsible row per task bump.
 */
'use strict';

const {
  navigationPathStyles,
  renderNavSteps,
  escapeHtml,
} = require('./scorecard-navigation-path');
const { rollup, collectIndexFailures } = require('./session-tracking-stats');

function dayKey(iso) {
  const d = new Date(iso || Date.now());
  if (Number.isNaN(d.getTime())) return 'Unknown date';
  return d.toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

function timeShort(iso) {
  const d = new Date(iso || Date.now());
  if (Number.isNaN(d.getTime())) return '—';
  return d.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
}

function sessionTimeShort(iso) {
  const d = new Date(iso || Date.now());
  if (Number.isNaN(d.getTime())) return '—';
  return d.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
}

function formatPctOrDash(value) {
  if (value == null || Number.isNaN(value)) return '—';
  return `${value}%`;
}

function formatMedianOrDash(value) {
  if (value == null || Number.isNaN(value)) return '—';
  return Number.isInteger(value) ? String(value) : value.toFixed(1);
}

function formatCoverageOrDash(value) {
  if (value == null || Number.isNaN(value)) return '—';
  return `${Math.round(value * 100)}%`;
}

function summaryStats(entries) {
  const today = dayKey(new Date().toISOString());
  const todayEntries = entries.filter((e) => dayKey(e.timestamp) === today);
  const withSteps = entries.filter((e) => (e.stepCount || 0) > 0);
  const avgSteps = withSteps.length
    ? (withSteps.reduce((s, e) => s + (e.stepCount || 0), 0) / withSteps.length).toFixed(1)
    : '—';
  const roll = rollup(entries);

  return {
    total: entries.length,
    today: todayEntries.length,
    avgSteps,
    indexFirstRate: roll.indexFirstRate,
    indexFirstCount: roll.indexFirstCount,
    observedTaskCount: roll.observedTaskCount,
    deadEndRate: roll.deadEndRate,
    deadEndSteps: roll.deadEndSteps,
    totalSteps: roll.totalSteps,
    medianSearchesBeforeDoc: roll.medianSearchesBeforeDoc,
    medianPathCoverage: roll.medianPathCoverage,
  };
}

function taskSummaryLine(entry) {
  const parts = [
    timeShort(entry.timestamp),
    entry.chunkNote,
  ];
  const meta = [];
  if (entry.stepCount) meta.push(`${entry.stepCount} step${entry.stepCount === 1 ? '' : 's'}`);
  if (entry.activeLabel && entry.activeMs > 0) meta.push(entry.activeLabel);
  else if (entry.durationLabel) meta.push(entry.durationLabel);
  if (entry.deadEndCount) meta.push(`${entry.deadEndCount} dead-end`);
  if (entry.missingNavigationPath) meta.push('no path logged');
  if (meta.length) parts.push(meta.join(' · '));
  return parts.filter(Boolean).join(' — ');
}

function coveragePills(entry) {
  let html = '';
  if ((entry.unexplainedSearches || 0) >= 3) {
    html += `<span class="pill p2">${entry.unexplainedSearches} searches not in path</span>`;
  }
  if ((entry.searchesBeforeFirstDoc || 0) >= 3) {
    html += `<span class="pill p2">Hunted before doc — ${entry.searchesBeforeFirstDoc} searches first</span>`;
  }
  if (entry.indexFirst) {
    html += '<span class="pill p1">Index first</span>';
  }
  return html;
}

function taskEntryHtml(entry) {
  const warnPill = entry.missingNavigationPath
    ? '<span class="pill p2">No navigation path</span>'
    : '';
  const backfillPill = entry.backfilled
    ? '<span class="pill p0">Backfilled</span>'
    : '';
  const navTree = entry.navigationPath?.length
    ? `<ul class="nav-tree nav-root">${renderNavSteps(entry.navigationPath)}</ul>`
    : '<p class="muted-inline">No navigation path was logged for this task.</p>';

  const statsLine = entry.stepCount
    ? `${entry.stepCount} steps · first helpful at #${entry.stepsToFirstHelpful || '—'} · `
      + `${entry.helpfulCount || 0} ✓ · ${entry.partialCount || 0} ~ · ${entry.deadEndCount || 0} ✗`
    : '';

  const observedLine = entry.hasObservedData
    ? `Hook saw ${entry.observedSearches || 0} search(es), ${entry.observedDocReads || 0} doc read(s)`
      + `${entry.unexplainedSearches ? ` · ${entry.unexplainedSearches} not in path` : ''}`
      + `${entry.pathCoverage != null ? ` · coverage ${Math.round((entry.pathCoverage || 0) * 100)}%` : ''}`
    : '';

  const idleNote = entry.durationLabel && entry.activeLabel && entry.durationMs !== entry.activeMs
    ? `Wall-clock gap since previous task: ${entry.durationLabel} (includes idle time)`
    : '';

  return `<details class="track-entry">
    <summary class="track-summary">
      <span class="track-title">${escapeHtml(taskSummaryLine(entry))}</span>
      ${warnPill}${backfillPill}${coveragePills(entry)}
    </summary>
    <div class="track-panel">
      <p class="track-meta muted-inline">
        Session ${escapeHtml(sessionTimeShort(entry.sessionId))}
        ${entry.activeLabel && entry.activeMs > 0
    ? ` · ${escapeHtml(entry.activeLabel)} active tool time`
    : (entry.durationLabel ? ` · ${escapeHtml(entry.durationLabel)} since previous task` : '')}
        ${statsLine ? `<br>${escapeHtml(statsLine)}` : ''}
        ${observedLine ? `<br>${escapeHtml(observedLine)}` : ''}
        ${idleNote ? `<br>${escapeHtml(idleNote)}` : ''}
      </p>
      <p class="muted-inline nav-legend">
        <span class="nav-helpful-pill">✓ helpful</span>
        <span class="nav-partial-pill">~ partial</span>
        <span class="nav-dead-pill">✗ dead end</span>
      </p>
      ${navTree}
    </div>
  </details>`;
}

function indexFailuresSection(entries) {
  const failures = collectIndexFailures(entries, 20);
  if (!failures.length) return '';

  const rows = failures.map((f) => {
    const marker = f.outcome === 'dead-end' ? '✗' : '~';
    const cls = f.outcome === 'dead-end' ? 'nav-dead' : 'nav-partial';
    return `<li class="index-fail ${cls}">
      <span class="nav-marker">${marker}</span>
      <code title="${escapeHtml(f.target)}">${escapeHtml(f.target)}</code>
      ${f.note ? `<span class="nav-note">${escapeHtml(f.note)}</span>` : ''}
      <span class="index-fail-task">${escapeHtml(timeShort(f.timestamp))} — ${escapeHtml(f.chunkNote || '')}</span>
    </li>`;
  }).join('');

  return `<section class="index-failures-block">
    <h2 class="day-title">Where the index failed</h2>
    <p class="muted-inline">Partial or dead-end doc steps from recent tasks — a backlog of missing index rows.</p>
    <ul class="index-failures-list">${rows}</ul>
  </section>`;
}

function buildTrackingHtml(entries) {
  const sorted = [...entries].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  const stats = summaryStats(sorted);
  const indexFirstLabel = stats.observedTaskCount
    ? `${formatPctOrDash(stats.indexFirstRate)} (of ${stats.observedTaskCount} tasks)`
    : '—';
  const deadEndLabel = stats.totalSteps
    ? `${formatPctOrDash(stats.deadEndRate)} (${stats.deadEndSteps}/${stats.totalSteps} steps)`
    : '—';
  const coverageLabel = stats.observedTaskCount
    ? formatCoverageOrDash(stats.medianPathCoverage)
    : '—';

  const byDay = new Map();
  for (const e of sorted) {
    const k = dayKey(e.timestamp);
    if (!byDay.has(k)) byDay.set(k, []);
    byDay.get(k).push(e);
  }

  let daySections = '';
  for (const [day, tasks] of byDay) {
    daySections += `<section class="day-block">
      <h2 class="day-title">${escapeHtml(day)} <span class="day-count">${tasks.length} task${tasks.length === 1 ? '' : 's'}</span></h2>
      <div class="day-tasks">${tasks.map((t) => taskEntryHtml(t)).join('')}</div>
    </section>`;
  }

  if (!daySections) {
    daySections = `<p class="empty">No tasks logged yet. After each deliverable, run <code>--bump-file</code> with <code>chunkNote</code> and <code>navigationPath</code>.</p>`;
  }

  const last = sorted[0]
    ? `${timeShort(sorted[0].timestamp)} · ${dayKey(sorted[0].timestamp)}`
    : '—';

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Session tracking — task log</title>
  <style>
    :root {
      --bg: #0f1419; --surface: #1a2332; --surface2: #243044;
      --text: #e8eef4; --muted: #9db0c4; --accent: #5eb8ff; --accent2: #7ee787;
      --warn: #f0b429; --danger: #ff7b72; --border: #3d5166;
    }
    * { box-sizing: border-box; }
    body { margin: 0; font-family: "Segoe UI", system-ui, sans-serif; background: var(--bg); color: var(--text); line-height: 1.55; font-size: 17px; }
    .wrap { max-width: 1100px; margin: 0 auto; padding: 1.25rem 1rem 3rem; }
    h1 { font-size: 1.85rem; margin: 0 0 0.35rem; }
    .subtitle { color: var(--muted); margin-bottom: 1rem; }
    .summary-bar {
      display: flex; flex-wrap: wrap; gap: 1rem; margin-bottom: 1rem;
      padding: 0.85rem 1rem; background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
    }
    .summary-bar dt { font-size: 0.75rem; text-transform: uppercase; color: var(--muted); }
    .summary-bar dd { margin: 0.15rem 0 0; font-size: 1.15rem; font-weight: 700; }
    .day-block, .index-failures-block { margin: 1.75rem 0; }
    .day-title { font-size: 1.2rem; color: var(--accent); margin: 0 0 0.75rem; padding-bottom: 0.35rem; border-bottom: 2px solid var(--border); }
    .day-count { font-size: 0.85rem; color: var(--muted); font-weight: 400; }
    .day-tasks { display: flex; flex-direction: column; gap: 0.55rem; }
    .track-entry { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }
    .track-entry[open] { box-shadow: inset 0 0 0 1px rgba(94, 184, 255, 0.35); }
    .track-summary {
      cursor: pointer; min-height: 48px; padding: 0.65rem 0.85rem;
      display: flex; flex-wrap: wrap; align-items: center; gap: 0.5rem; list-style: none;
    }
    .track-summary::-webkit-details-marker { display: none; }
    .track-title { flex: 1 1 12rem; font-size: 0.95rem; line-height: 1.4; }
    .track-panel { padding: 0 0.85rem 0.75rem; border-top: 1px solid rgba(61, 81, 102, 0.45); }
    .track-meta { margin: 0.5rem 0 0.35rem; font-size: 0.85rem; }
    .pill { display: inline-block; padding: 0.2em 0.55em; border-radius: 999px; font-size: 0.72rem; font-weight: 700; }
    .p0 { background: #1e3350; color: var(--accent); }
    .p1 { background: #264032; color: var(--accent2); }
    .p2 { background: #4a3818; color: var(--warn); }
    .muted-inline { color: var(--muted); font-size: 0.9rem; }
    .empty { color: var(--muted); padding: 2rem; text-align: center; }
    .footer { margin-top: 2rem; color: var(--muted); font-size: 0.85rem; }
    .footer a { color: var(--accent); }
    .index-failures-list { margin: 0.5rem 0 0; padding: 0; list-style: none; }
    .index-fail {
      display: flex; flex-wrap: wrap; align-items: baseline; gap: 0.35rem;
      margin: 0.45rem 0; padding: 0.45rem 0.55rem; background: #151c26; border-radius: 8px; font-size: 0.88rem;
    }
    .index-fail code { font-family: Consolas, "Courier New", monospace; word-break: break-word; }
    .index-fail-task { flex-basis: 100%; color: var(--muted); font-size: 0.82rem; padding-left: 1.45rem; }
    ${navigationPathStyles()}
    .track-entry .nav-path-block { margin-top: 0.35rem; }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Session tracking</h1>
    <p class="subtitle">One row per completed task — hook-verified navigation vs self-reported path. Data in <code>session-tracking.jsonl</code>.</p>
    <div class="summary-bar">
      <div><dt>Total tasks</dt><dd>${stats.total}</dd></div>
      <div><dt>Tasks today</dt><dd>${stats.today}</dd></div>
      <div><dt>Index-first rate</dt><dd style="font-size:1rem">${escapeHtml(indexFirstLabel)}</dd></div>
      <div><dt>Searches before first doc (median)</dt><dd>${escapeHtml(formatMedianOrDash(stats.medianSearchesBeforeDoc))}</dd></div>
      <div><dt>Dead-end rate</dt><dd style="font-size:1rem">${escapeHtml(deadEndLabel)}</dd></div>
      <div><dt>Path coverage (median)</dt><dd>${escapeHtml(coverageLabel)}</dd></div>
      <div><dt>Avg steps</dt><dd>${escapeHtml(String(stats.avgSteps))}</dd></div>
      <div><dt>Latest</dt><dd style="font-size:1rem">${escapeHtml(last)}</dd></div>
    </div>
    ${indexFailuresSection(sorted)}
    ${daySections}
    <p class="footer">Generated by <code>scripts/append-session-scorecard.js</code> ·
      <a href="http://127.0.0.1:8765/session-metrics-log.html">Session metrics</a> ·
      <a href="http://127.0.0.1:8765/index.html">All pages</a></p>
  </div>
</body>
</html>`;
}

module.exports = {
  buildTrackingHtml,
  dayKey,
  timeShort,
};
