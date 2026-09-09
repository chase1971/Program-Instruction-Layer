/**
 * FILE: scripts/token-report.js
 * PURPOSE: Generate agent docs/token-usage-log.html — where the tokens actually
 *          went, from real billed data.
 *
 * Usage:
 *   node scripts/token-report.js              # Claude Code transcripts
 *   node scripts/token-report.js --cursor     # also rescan Cursor's local DB (slow)
 *
 * Chase views: http://127.0.0.1:8765/token-usage-log.html
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const {
  readSessions, toolCosts, lengthScaling, totals,
  cursorCachePath, readCursorCache, formatTokens,
} = require('./token-report-data');

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'agent docs', 'token-usage-log.html');
const CURSOR_SCRIPT = path.join(__dirname, 'cursor-token-scan.py');

const esc = (s) => String(s == null ? '' : s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;');

function refreshCursor() {
  if (!fs.existsSync(CURSOR_SCRIPT)) return null;
  try {
    const raw = execFileSync('python', [CURSOR_SCRIPT], {
      encoding: 'utf8', timeout: 10 * 60 * 1000, maxBuffer: 8 * 1024 * 1024,
    });
    const data = JSON.parse(raw);
    data.scannedAt = new Date().toISOString();
    fs.writeFileSync(cursorCachePath(ROOT), JSON.stringify(data, null, 2), 'utf8');
    return data;
  } catch (e) {
    process.stderr.write(`Cursor scan failed (non-fatal): ${e.message}\n`);
    return null;
  }
}

function bar(share, color) {
  const pct = Math.max(0.4, share * 100);
  return `<div class="bar"><div class="fill" style="width:${pct.toFixed(1)}%;background:${color}"></div></div>`;
}

function toolSection(rows) {
  if (!rows.length) return '<p class="muted">No tool data yet.</p>';
  const colors = ['#f87171', '#fb923c', '#fbbf24', '#a3e635', '#34d399',
    '#38bdf8', '#818cf8', '#a78bfa', '#f472b6', '#94a3b8'];
  return `<table>
    <tr><th>Tool</th><th>Calls</th><th>Avg added</th><th>Real cost once re-billed</th><th>Share</th></tr>
    ${rows.map((r, i) => `<tr>
      <td><b>${esc(r.name)}</b></td>
      <td class="n">${r.calls.toLocaleString()}</td>
      <td class="n">${formatTokens(r.avgAdded)}</td>
      <td class="n">${formatTokens(r.compounded)}</td>
      <td class="barcell">${bar(r.share, colors[i % colors.length])}<span class="pctlab">${(r.share * 100).toFixed(1)}%</span></td>
    </tr>`).join('')}
  </table>`;
}

function scalingSection(rows) {
  if (!rows.length) return '';
  const max = Math.max(...rows.map((r) => r.costPerTurn));
  return `<table>
    <tr><th>Session length</th><th>Sessions</th><th>Avg total cost</th><th>Cost per turn</th><th></th></tr>
    ${rows.map((r) => `<tr>
      <td><b>${esc(r.label)} turns</b></td>
      <td class="n">${r.sessions}</td>
      <td class="n">${formatTokens(r.avgCost)}</td>
      <td class="n">${formatTokens(r.costPerTurn)}</td>
      <td class="barcell">${bar(r.costPerTurn / max, '#fbbf24')}</td>
    </tr>`).join('')}
  </table>`;
}

function sessionSection(sessions) {
  return `<table>
    <tr><th>Session</th><th>Started</th><th>Turns</th><th>Billed</th><th>Per turn</th></tr>
    ${sessions.slice(0, 15).map((s) => `<tr>
      <td class="mono">${esc(s.id)}</td>
      <td class="n">${esc(String(s.started || '').slice(0, 10))}</td>
      <td class="n">${s.turnCount.toLocaleString()}</td>
      <td class="n">${formatTokens(s.billed)}</td>
      <td class="n">${formatTokens(Math.round(s.billed / s.turnCount))}</td>
    </tr>`).join('')}
  </table>`;
}

function cursorSection(cur) {
  if (!cur || !Array.isArray(cur.models) || !cur.models.length) {
    return `<p class="muted">No Cursor data cached yet. Run
      <code>node scripts/token-report.js --cursor</code> to scan Cursor's local database
      (takes a few minutes — it walks every stored message).</p>`;
  }
  const unlabeled = cur.models.find((m) => m.model === '(not recorded)');
  const unlabeledShare = unlabeled && cur.totalIn ? unlabeled.in / cur.totalIn : 0;
  const caveat = unlabeledShare > 0.5 ? `<div class="panel red">
    <h3>Cursor records the tokens, but usually not which model spent them</h3>
    <p><b>${(unlabeledShare * 100).toFixed(0)}%</b> of Cursor's recorded input tokens carry no
       <code>modelName</code> field, so they cannot be attributed to a model. The token totals below
       are trustworthy; the per-model split is only meaningful for the small labelled slice.</p>
    <p><b>What that means for you:</b> Cursor's local data can tell you how much you spent overall,
       but it cannot answer "was Opus worth it" — not even in principle, because the model isn't
       written down for most requests. That comparison needs a deliberate test.</p>
  </div>` : '';

  return `${caveat}<p class="muted">From Cursor's own local database. Input includes the whole
    conversation resent each turn, same as Claude Code. Scanned ${esc(String(cur.scannedAt || '').slice(0, 10))}.</p>
  <table>
    <tr><th>Model</th><th>Requests</th><th>Input</th><th>Output</th><th>Avg input / request</th></tr>
    ${cur.models.map((m) => `<tr>
      <td><b>${esc(m.model)}</b></td>
      <td class="n">${(m.n || 0).toLocaleString()}</td>
      <td class="n">${formatTokens(m.in)}</td>
      <td class="n">${formatTokens(m.out)}</td>
      <td class="n">${formatTokens(Math.round((m.in || 0) / (m.n || 1)))}</td>
    </tr>`).join('')}
  </table>`;
}

function build() {
  const sessions = readSessions();
  const tools = toolCosts(sessions);
  const scaling = lengthScaling(sessions);
  const tot = totals(sessions);
  const cursor = readCursorCache(ROOT);
  const topTool = tools[0];
  const editTool = tools.find((t) => t.name === 'Edit');
  const shortest = scaling[0];
  const longest = scaling[scaling.length - 1];

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Token usage — where they actually went</title>
<style>
  :root{--bg:#0f1419;--panel:#1a2332;--panel-alt:#243044;--text:#e8edf4;--muted:#94a3b8;
        --accent:#38bdf8;--green:#34d399;--amber:#fbbf24;--red:#f87171;--border:#334155;
        --radius:14px;--font:"Segoe UI",system-ui,sans-serif}
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:var(--font);background:var(--bg);color:var(--text);line-height:1.55;font-size:18px}
  .page{max-width:940px;margin:0 auto;padding:2.5rem 1.25rem 4rem}
  header{margin-bottom:1.6rem;padding-bottom:1.4rem;border-bottom:2px solid var(--border)}
  header h1{font-size:clamp(1.6rem,4.6vw,2.2rem);letter-spacing:-.02em;line-height:1.25}
  header p{color:var(--muted);margin-top:.6rem;font-size:1rem}
  h2{font-size:.82rem;letter-spacing:.15em;text-transform:uppercase;font-weight:700;
     margin:2.6rem 0 .4rem;color:var(--accent)}
  h2.amber{color:var(--amber)} h2.red{color:var(--red)} h2.green{color:var(--green)}
  .lede{color:var(--muted);font-size:.96rem;margin-bottom:1rem}
  .lede b{color:var(--text)}
  .panel{background:var(--panel);border:1px solid var(--border);border-radius:var(--radius);
         padding:1.2rem 1.3rem;margin-bottom:.9rem}
  .panel.red{border-left:5px solid var(--red)}
  .panel.green{border-left:5px solid var(--green)}
  .panel.amber{border-left:5px solid var(--amber)}
  .panel h3{font-size:1.06rem;margin-bottom:.45rem}
  .panel p{font-size:.94rem;color:var(--muted)}
  .panel p b{color:var(--text)}
  .tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.8rem;margin-bottom:.9rem}
  .tile{background:var(--panel);border:1px solid var(--border);border-radius:var(--radius);padding:1rem 1.1rem}
  .tile .v{font-size:1.9rem;font-weight:800;letter-spacing:-.02em}
  .tile .k{font-size:.78rem;color:var(--muted);margin-top:.2rem}
  .v.red{color:var(--red)} .v.amber{color:var(--amber)} .v.accent{color:var(--accent)} .v.green{color:var(--green)}
  table{width:100%;border-collapse:collapse;font-size:.92rem;background:var(--panel);
        border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;margin-bottom:.9rem}
  th,td{text-align:left;padding:.62rem .8rem;border-bottom:1px solid var(--border)}
  th{font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);
     font-weight:700;background:var(--panel-alt)}
  tr:last-child td{border-bottom:none}
  td.n{font-family:Consolas,monospace;color:var(--accent);white-space:nowrap}
  td.mono{font-family:Consolas,monospace;color:var(--muted)}
  .barcell{width:34%;min-width:130px}
  .bar{background:var(--panel-alt);border-radius:999px;height:12px;overflow:hidden;display:inline-block;
       width:calc(100% - 52px);vertical-align:middle}
  .fill{height:100%;border-radius:999px}
  .pctlab{font-family:Consolas,monospace;font-size:.78rem;color:var(--muted);margin-left:.5rem}
  code{background:var(--panel-alt);color:var(--accent);padding:.08rem .34rem;border-radius:4px;
       font-size:.85em;font-family:Consolas,monospace}
  .muted{color:var(--muted);font-size:.92rem;margin-bottom:.7rem}
  a.back{display:block;text-align:center;margin-top:2.4rem;padding:1rem;background:var(--panel);
         border:1px solid var(--border);border-radius:var(--radius);color:var(--accent);
         text-decoration:none;font-weight:600;min-height:56px}
  a.back:hover,a.back:focus{background:var(--panel-alt);outline:none}
  footer{margin-top:1.4rem;color:var(--muted);font-size:.8rem;text-align:center}
</style>
</head>
<body>
<div class="page">

<header>
  <h1>Where the tokens actually went</h1>
  <p>Real billed usage from ${tot.sessions} Claude Code sessions. Not estimates — the numbers
     the transcripts recorded at the time.</p>
</header>

<div class="tiles">
  <div class="tile"><div class="v red">${formatTokens(tot.billed)}</div><div class="k">Total billed</div></div>
  <div class="tile"><div class="v amber">${formatTokens(tot.perTurn)}</div><div class="k">Average per turn</div></div>
  <div class="tile"><div class="v accent">${tot.turns.toLocaleString()}</div><div class="k">Assistant turns</div></div>
  <div class="tile"><div class="v green">${tot.sessions}</div><div class="k">Sessions</div></div>
</div>

<h2 class="red">1 — Reading costs far more than writing</h2>
<p class="lede">
  Every tool result stays in the conversation and is <b>re-billed on every later turn</b>.
  So the true price of a tool call is what it added, multiplied by how many turns came after it.
  That is the last column.
</p>
${toolSection(tools)}
${topTool && editTool ? `<div class="panel red">
  <h3>The intuition worth correcting</h3>
  <p>Writing code looks expensive because it takes a long time and fills the screen.
     It isn't. <b>${esc(editTool.name)}</b> accounts for <b>${(editTool.share * 100).toFixed(1)}%</b> of cost,
     while <b>${esc(topTool.name)}</b> accounts for <b>${(topTool.share * 100).toFixed(1)}%</b> —
     about <b>${(topTool.compounded / editTool.compounded).toFixed(1)}× more</b>.</p>
  <p>Time on screen tracks <i>output</i> tokens, which are a small slice of the bill.
     Cost tracks how much got <i>pulled in and carried forward</i>.</p>
</div>` : ''}

<h2 class="amber">2 — Long sessions get expensive faster than you'd think</h2>
<p class="lede">
  Cost per turn is <b>not constant</b>. A turn late in a long session costs several times what an
  early turn costs, because it re-reads everything before it.
</p>
${scalingSection(scaling)}
${shortest && longest ? `<div class="panel amber">
  <h3>What this means in practice</h3>
  <p>A turn in a <b>${esc(longest.label.toLowerCase())}</b>-turn session costs
     <b>${(longest.costPerTurn / shortest.costPerTurn).toFixed(1)}×</b> what a turn in a
     <b>${esc(shortest.label.toLowerCase())}</b>-turn session costs
     (${formatTokens(longest.costPerTurn)} vs ${formatTokens(shortest.costPerTurn)}).</p>
  <p>Models stopped visibly forgetting things in long chats — which removed the symptom that used
     to tell you to start fresh. <b>The cost didn't go away, it just got quiet.</b>
     Starting a new chat at a natural task boundary is the single largest lever here.</p>
</div>` : ''}

<h2>3 — Most expensive sessions</h2>
${sessionSection(sessions)}

<h2 class="green">4 — Cursor</h2>
${cursorSection(cursor)}

<a class="back" href="/pages.html">← All pages</a>
<footer>Generated by <code>scripts/token-report.js</code> ·
  ${esc(new Date().toISOString().slice(0, 16).replace('T', ' '))}</footer>

</div>
</body>
</html>`;
}

function main() {
  if (process.argv.includes('--cursor')) {
    process.stdout.write('Scanning Cursor database (this takes a few minutes)…\n');
    refreshCursor();
  }
  fs.writeFileSync(OUT, build(), 'utf8');
  process.stdout.write('Token report written. View: http://127.0.0.1:8765/token-usage-log.html\n');
}

if (require.main === module) main();

module.exports = { build };
