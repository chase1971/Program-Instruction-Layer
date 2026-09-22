/**
 * FILE: scripts/session-metrics-html.js
 * PURPOSE: Build session-metrics-log.html — one card per finalized session, plus the
 *          live card for the session still in progress. Cards: session-metrics-card.js.
 */
'use strict';

const {
  TIPS,
  esc,
  tip,
  dayKey,
  timeShort,
  sessionCard,
} = require('./session-metrics-card');

const TRACKING_URL = 'http://127.0.0.1:8765/session-tracking-log.html';
const METRICS_URL = 'http://127.0.0.1:8765/session-metrics-log.html';

function legendHtml() {
  const items = [
    ['Your messages', TIPS.turns],
    ['Tokens', TIPS.tokens],
    ['Peak context/turn', TIPS.peakContext],
    ['You corrected me', TIPS.corrections],
    ['Agent suggests capturing', TIPS.captureSuggest],
  ];
  return `<details class="legend">
    <summary>What do these numbers mean? (hover any label on a card too)</summary>
    <ul>${items.map(([l, t]) => `<li><strong>${esc(l)}:</strong> ${esc(t)}</li>`).join('')}</ul>
  </details>`;
}

function runningToDisplayEntry(r) {
  return {
    timestamp: r.sessionStarted,
    model: r.model || '—',
    sessionType: r.sessionType || 'mixed',
    summaryHuman: r.summaryHuman || 'Session in progress…',
    summarized: !!r.summarized,
    turns: r.turns,
    corrections: r.corrections,
    taskBumpCount: Array.isArray(r.taskLog) ? r.taskLog.length : 0,
    taskLog: r.taskLog || [],
  };
}

function buildHtml(entries, running) {
  const sorted = [...entries].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  const byDay = new Map();
  for (const e of sorted) {
    const k = dayKey(e.timestamp);
    if (!byDay.has(k)) byDay.set(k, []);
    byDay.get(k).push(e);
  }

  let inProgressSection = '';
  if (running) {
    const live = runningToDisplayEntry(running);
    inProgressSection = `<section class="day-block">
      <h2 class="day-title">Current session (live tally)</h2>
      <div class="day-sessions">${sessionCard(live, true)}</div>
    </section>`;
  }

  let daySections = '';
  for (const [day, sessions] of byDay) {
    daySections += `<section class="day-block">
      <h2 class="day-title">${esc(day)}</h2>
      <div class="day-sessions">${sessions.map((e) => sessionCard(e)).join('')}</div>
    </section>`;
  }

  if (!daySections) {
    daySections = `<p class="empty">No sessions logged yet. End a session with <strong>wrap the session</strong>.</p>`;
  }

  const total = sorted.length;
  const last = sorted[0] ? timeShort(sorted[0].timestamp) + ' · ' + dayKey(sorted[0].timestamp) : '—';

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Session metrics — running log</title>
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
    abbr.tip { text-decoration: underline dotted; text-underline-offset: 3px; cursor: help; border: none; }
    .legend, .file-details { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 0.65rem 0.85rem; margin-bottom: 0.65rem; }
    .legend summary, .file-details summary { cursor: pointer; min-height: 44px; display: flex; align-items: center; font-weight: 600; }
    .legend ul { margin: 0.5rem 0 0; padding-left: 1.2rem; color: var(--muted); font-size: 0.92rem; }
    .legend li { margin: 0.35rem 0; }
    .muted-inline { color: var(--muted); font-size: 0.9rem; margin: 0.5rem 0 0; }
    .summary-bar {
      display: flex; flex-wrap: wrap; gap: 1rem; margin-bottom: 1rem;
      padding: 0.85rem 1rem; background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
    }
    .summary-bar dt { font-size: 0.75rem; text-transform: uppercase; color: var(--muted); }
    .summary-bar dd { margin: 0.15rem 0 0; font-size: 1.15rem; font-weight: 700; }
    .day-block { margin: 1.75rem 0; }
    .day-title { font-size: 1.2rem; color: var(--accent); margin: 0 0 0.75rem; padding-bottom: 0.35rem; border-bottom: 2px solid var(--border); }
    .day-sessions { display: flex; flex-direction: column; gap: 0.85rem; }
    .session-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 0.9rem 1rem; border-left: 4px solid var(--accent2); }
    .session-card.in-progress { border-left-color: var(--accent); border-style: dashed; opacity: 0.95; }
    .session-head { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 0.5rem; margin-bottom: 0.5rem; }
    .pills { display: flex; flex-wrap: wrap; align-items: center; gap: 0.25rem; }
    .time { font-weight: 700; margin-right: 0.35rem; }
    .model { color: var(--muted); font-size: 0.9rem; }
    .summary-human { margin: 0.35rem 0 0.75rem; font-size: 1.02rem; line-height: 1.5; }
    .metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem; margin: 0.35rem 0; }
    @media (max-width: 700px) { .metric-grid { grid-template-columns: repeat(2, 1fr); } }
    .metric { background: #151c26; border-radius: 8px; padding: 0.45rem 0.55rem; }
    .metric-warn { border: 1px solid var(--warn); }
    .metric dt { font-size: 0.68rem; text-transform: uppercase; color: var(--muted); margin: 0; letter-spacing: 0.03em; }
    .metric dd { margin: 0.15rem 0 0; font-weight: 700; font-size: 1.05rem; }
    .pill { display: inline-block; padding: 0.2em 0.55em; border-radius: 999px; font-size: 0.72rem; font-weight: 700; cursor: help; }
    .p0 { background: #1e3350; color: var(--accent); }
    .p1 { background: #264032; color: var(--accent2); }
    .p2 { background: #4a3818; color: var(--warn); }
    .p3 { background: #3d2020; color: var(--danger); }
    .note-box, .capture-box { margin-top: 0.55rem; padding: 0.55rem 0.7rem; border-radius: 8px; font-size: 0.92rem; }
    .note-box { background: #2a2a18; border: 1px solid var(--warn); }
    .capture-box { background: #1a2a22; border: 1px solid var(--accent2); }
    .next { color: var(--muted); font-size: 0.9rem; margin: 0.45rem 0 0; }
    .task-list { margin: 0.35rem 0 0; padding-left: 1.2rem; font-size: 0.88rem; color: var(--muted); }
    .task-list li { margin: 0.2rem 0; }
    .empty { color: var(--muted); padding: 2rem; text-align: center; }
    .footer { margin-top: 2rem; color: var(--muted); font-size: 0.85rem; }
    .footer a { color: var(--accent); }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Session metrics</h1>
    <p class="subtitle">One card per finalized session: what got done, what it cost, and the agent's notes. Per-task rows live on <a href="${TRACKING_URL}">session tracking</a>. Data in <code>session-scorecards.jsonl</code>.</p>
    ${legendHtml()}
    <div class="summary-bar">
      <div><dt>Total sessions</dt><dd>${total}</dd></div>
      <div><dt>Latest</dt><dd style="font-size:1rem">${esc(last)}</dd></div>
    </div>
    ${inProgressSection}
    ${daySections}
    <p class="footer">Generated by <code>scripts/append-session-scorecard.js</code> ·
      <a href="${TRACKING_URL}">Session tracking</a> ·
      <a href="http://127.0.0.1:8765/context-engineering-capture-costs.html">Capture ladder</a></p>
  </div>
</body>
</html>`;
}

module.exports = {
  TRACKING_URL,
  METRICS_URL,
  buildHtml,
};
