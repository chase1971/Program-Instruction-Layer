/**
 * FILE: scripts/session-tracking-html.js
 * PURPOSE: Build session-tracking-log.html — cost roll-up, docs that failed to route,
 *          then one collapsible row per task bump.
 */
'use strict';

const { rollup } = require('./session-tracking-stats');
const { entryGaps, collectIndexGaps, gapCountsByDoc } = require('./session-index-gaps');
const { formatTokens, HEAVY_CONTEXT_TOKENS } = require('./session-token-cost');

function escapeHtml(s) {
  return String(s ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function dayKey(iso) {
  const d = new Date(iso || Date.now());
  if (Number.isNaN(d.getTime())) return 'Unknown date';
  return d.toLocaleDateString('en-US', {
    weekday: 'long', year: 'numeric', month: 'short', day: 'numeric',
  });
}

function timeShort(iso) {
  const d = new Date(iso || Date.now());
  if (Number.isNaN(d.getTime())) return '—';
  return d.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
}

function tokensOrDash(value) {
  return value == null || Number.isNaN(value) ? '—' : formatTokens(value);
}

// Context re-read per turn is the number worth flagging: it grows with session
// length, not task difficulty, so a high value means "this session got expensive".
function costPills(entry) {
  let html = '';
  if (Number.isFinite(entry.billedTokens)) {
    html += `<span class="pill p0">${formatTokens(entry.billedTokens)} tokens</span>`;
  } else if (Number.isFinite(entry.chatUserMessages)) {
    // Cursor records no tokens, so chat length is the only cost signal there.
    html += `<span class="pill p0">Chat: ${entry.chatUserMessages} msgs</span>`;
  }
  if ((entry.tokensPerTurn || 0) >= HEAVY_CONTEXT_TOKENS) {
    html += `<span class="pill p2">Heavy context — ${formatTokens(entry.tokensPerTurn)}/turn</span>`;
  }
  const gaps = entryGaps(entry).length;
  if (gaps) html += `<span class="pill p3">${gaps} index gap${gaps === 1 ? '' : 's'}</span>`;
  return html;
}

function detailLines(entry) {
  const lines = [];
  if (entry.model) lines.push(`Model: ${entry.model}`);
  if (entry.activeMs > 0) lines.push(`${entry.activeLabel} active tool time`);
  if (entry.durationLabel) lines.push(`${entry.durationLabel} since previous task (includes idle)`);
  if (Number.isFinite(entry.billedTokens)) {
    lines.push(`${formatTokens(entry.billedTokens)} tokens over ${entry.tokenTurns} turn(s) · `
      + `${formatTokens(entry.tokensPerTurn)}/turn · ${formatTokens(entry.tokensCacheRead)} cache read · `
      + `${formatTokens(entry.tokensOutput)} output`);
  }
  if (Number.isFinite(entry.chatUserMessages)) {
    lines.push(`Chat so far: ${entry.chatUserMessages} message(s)`
      + `${Number.isFinite(entry.chatTranscriptKB) ? `, ${entry.chatTranscriptKB} KB transcript` : ''}`);
  }
  return lines;
}

function taskEntryHtml(entry) {
  const gaps = entryGaps(entry);
  const gapList = gaps.length
    ? `<ul class="gap-list">${gaps.map((g) => `<li><code>${escapeHtml(g.doc)}</code>`
      + `${g.note ? ` — ${escapeHtml(g.note)}` : ''}</li>`).join('')}</ul>`
    : '';
  return `<details class="track-entry">
    <summary class="track-summary">
      <span class="track-title">${escapeHtml(`${timeShort(entry.timestamp)} — ${entry.chunkNote}`)}</span>
      ${entry.backfilled ? '<span class="pill p0">Backfilled</span>' : ''}${costPills(entry)}
    </summary>
    <div class="track-panel">
      <p class="track-meta muted-inline">${detailLines(entry).map(escapeHtml).join('<br>')}</p>
      ${gapList}
    </div>
  </details>`;
}

function indexGapsSection(entries) {
  const byDoc = gapCountsByDoc(entries).slice(0, 12);
  if (!byDoc.length) return '';
  const recent = collectIndexGaps(entries, 15);
  return `<section class="gaps-block">
    <h2 class="day-title">Docs that failed to route</h2>
    <p class="muted-inline">The agent opened the doc and still had to grep the tree for the answer.
    Most-failing docs first — each is a missing index row or a doc worth fixing.</p>
    <table class="gap-table"><thead><tr><th>Doc</th><th>Times</th></tr></thead><tbody>
      ${byDoc.map(([doc, n]) => `<tr><td><code>${escapeHtml(doc)}</code></td><td>${n}</td></tr>`).join('')}
    </tbody></table>
    <details class="recent-gaps"><summary>Most recent ${recent.length}</summary>
      <ul class="gap-list">${recent.map((g) => `<li><code>${escapeHtml(g.doc)}</code>`
        + `${g.note ? ` — ${escapeHtml(g.note)}` : ''}`
        + `<span class="gap-task">${escapeHtml(timeShort(g.timestamp))} · ${escapeHtml(dayKey(g.timestamp))} — `
        + `${escapeHtml(g.chunkNote || '')}</span></li>`).join('')}</ul>
    </details>
  </section>`;
}

function buildTrackingHtml(entries) {
  const sorted = [...entries].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  const today = dayKey(new Date().toISOString());
  const todayCount = sorted.filter((e) => dayKey(e.timestamp) === today).length;
  const roll = rollup(sorted);
  const costLabel = roll.costedTaskCount
    ? `${tokensOrDash(roll.medianBilledTokens)} (of ${roll.costedTaskCount} costed)`
    : '— (no cost data yet)';

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
      <div class="day-tasks">${tasks.map(taskEntryHtml).join('')}</div>
    </section>`;
  }
  if (!daySections) {
    daySections = '<p class="empty">No tasks logged yet. After each deliverable, run <code>--note "…"</code>.</p>';
  }
  const last = sorted[0] ? `${timeShort(sorted[0].timestamp)} · ${dayKey(sorted[0].timestamp)}` : '—';

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Session tracking — task log</title>
  <style>
    :root {
      --bg: #0f1419; --surface: #1a2332; --text: #e8eef4; --muted: #9db0c4;
      --accent: #5eb8ff; --accent2: #7ee787; --warn: #f0b429; --danger: #ff7b72; --border: #3d5166;
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
    .day-block, .gaps-block { margin: 1.75rem 0; }
    .day-title { font-size: 1.2rem; color: var(--accent); margin: 0 0 0.75rem; padding-bottom: 0.35rem; border-bottom: 2px solid var(--border); }
    .day-count { font-size: 0.85rem; color: var(--muted); font-weight: 400; }
    .day-tasks { display: flex; flex-direction: column; gap: 0.55rem; }
    .track-entry { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }
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
    .p2 { background: #4a3818; color: var(--warn); }
    .p3 { background: #3d2020; color: var(--danger); }
    .muted-inline { color: var(--muted); font-size: 0.9rem; }
    .empty { color: var(--muted); padding: 2rem; text-align: center; }
    .gap-table { border-collapse: collapse; margin: 0.5rem 0; font-size: 0.9rem; }
    .gap-table th, .gap-table td { text-align: left; padding: 0.35rem 0.75rem; border-bottom: 1px solid var(--border); }
    .gap-table th { color: var(--muted); font-size: 0.78rem; text-transform: uppercase; }
    .recent-gaps summary { cursor: pointer; min-height: 44px; display: flex; align-items: center; font-weight: 600; }
    .gap-list { margin: 0.35rem 0 0; padding-left: 1.2rem; font-size: 0.88rem; }
    .gap-list li { margin: 0.35rem 0; }
    .gap-list code { font-family: Consolas, "Courier New", monospace; word-break: break-word; }
    .gap-task { display: block; color: var(--muted); font-size: 0.82rem; }
    .footer { margin-top: 2rem; color: var(--muted); font-size: 0.85rem; }
    .footer a { color: var(--accent); }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Session tracking</h1>
    <p class="subtitle">One row per completed task: what was done, what it cost, and any doc that failed to route. Data in <code>session-tracking.jsonl</code>.</p>
    <div class="summary-bar">
      <div><dt>Total tasks</dt><dd>${sorted.length}</dd></div>
      <div><dt>Tasks today</dt><dd>${todayCount}</dd></div>
      <div><dt>Tokens per task (median)</dt><dd style="font-size:1rem">${escapeHtml(costLabel)}</dd></div>
      <div><dt>Context per turn (median)</dt><dd>${escapeHtml(tokensOrDash(roll.medianTokensPerTurn))}</dd></div>
      <div><dt>Total billed</dt><dd>${escapeHtml(tokensOrDash(roll.totalBilledTokens))}</dd></div>
      <div><dt>Share that is cache re-reads</dt><dd>${roll.cacheReadPct == null ? '—' : `${roll.cacheReadPct}%`}</dd></div>
      <div><dt>Latest</dt><dd style="font-size:1rem">${escapeHtml(last)}</dd></div>
    </div>
    ${indexGapsSection(sorted)}
    ${daySections}
    <p class="footer">Generated by <code>scripts/append-session-scorecard.js</code> ·
      <a href="http://127.0.0.1:8765/session-metrics-log.html">Session metrics</a> ·
      <a href="http://127.0.0.1:8765/pages.html">All pages</a></p>
  </div>
</body>
</html>`;
}

module.exports = {
  buildTrackingHtml,
  dayKey,
  timeShort,
  escapeHtml,
};
