/**
 * FILE: scripts/probe-report.js
 * PURPOSE: Render agent docs/probe-baseline-log.html — every probe run side by
 *          side, so a change to the instruction layer can be read as a delta.
 *
 * Usage: node scripts/probe-report.js
 * Chase views: http://127.0.0.1:8765/probe-baseline-log.html
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const RUNS_DIR = path.join(ROOT, 'agent docs', 'probes', 'runs');
const PROBE_FILE = path.join(ROOT, 'agent docs', 'probes', 'retrieval-probes.json');
const OUT = path.join(ROOT, 'agent docs', 'probe-baseline-log.html');

const esc = (s) => String(s == null ? '' : s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

const tok = (n) => (n >= 1e6 ? `${(n / 1e6).toFixed(1)}M` : n >= 1e3 ? `${(n / 1e3).toFixed(0)}k` : String(Math.round(n || 0)));

function loadRuns() {
  if (!fs.existsSync(RUNS_DIR)) return [];
  return fs.readdirSync(RUNS_DIR).filter((f) => f.endsWith('.json'))
    .map((f) => {
      try {
        return { file: f, ...JSON.parse(fs.readFileSync(path.join(RUNS_DIR, f), 'utf8')) };
      } catch {
        return null;
      }
    })
    .filter(Boolean)
    .sort((a, b) => new Date(b.startedAt) - new Date(a.startedAt));
}

function pctOf(c, n) { return n ? Math.round((c / n) * 100) : 0; }

function deltaCell(cur, prev, invert = false) {
  if (prev == null || !Number.isFinite(prev) || !Number.isFinite(cur)) return '<td class="n">—</td>';
  const d = cur - prev;
  if (d === 0) return '<td class="n muted2">no change</td>';
  // For tokens, lower is better. For correctness, higher is better.
  const good = invert ? d < 0 : d > 0;
  const sign = d > 0 ? '+' : '';
  const val = Math.abs(d) >= 1000 ? `${sign}${tok(d)}` : `${sign}${d}`;
  return `<td class="n ${good ? 'good' : 'bad'}">${val}</td>`;
}

function runsTable(runs) {
  if (runs.length < 1) return '';
  return `<table>
    <tr><th>Run</th><th>Model</th><th>When</th><th>Correct</th><th>Δ</th><th>Tokens</th><th>Δ</th></tr>
    ${runs.map((r, i) => {
    const prev = runs[i + 1];
    return `<tr>
        <td><b>${esc(r.label)}</b></td>
        <td class="mono">${esc(r.model || 'auto')}</td>
        <td class="n">${esc(String(r.startedAt).slice(0, 16).replace('T', ' '))}</td>
        <td class="n">${r.correct}/${r.total} <span class="muted2">(${pctOf(r.correct, r.total)}%)</span></td>
        ${deltaCell(r.correct, prev ? prev.correct : null)}
        <td class="n">${tok(r.billedTokens)}</td>
        ${deltaCell(r.billedTokens, prev ? prev.billedTokens : null, true)}
      </tr>`;
  }).join('')}
  </table>`;
}

function tierTable(run) {
  const tiers = Object.entries(run.byTier || {});
  if (!tiers.length) return '';
  return `<table>
    <tr><th>Tier</th><th>Correct</th><th>Tokens</th><th>Avg per question</th></tr>
    ${tiers.map(([t, d]) => `<tr>
      <td><b>${esc(t)}</b></td>
      <td class="n">${d.correct}/${d.n} <span class="muted2">(${pctOf(d.correct, d.n)}%)</span></td>
      <td class="n">${tok(d.tokens)}</td>
      <td class="n">${tok(Math.round(d.tokens / (d.n || 1)))}</td>
    </tr>`).join('')}
  </table>`;
}

function probeRows(run) {
  return `<table>
    <tr><th>Probe</th><th>Tier</th><th>Result</th><th>Tokens</th><th>Time</th></tr>
    ${(run.results || []).map((r) => `<tr>
      <td class="mono">${esc(r.id)}</td>
      <td class="muted2">${esc(r.tier)}</td>
      <td>${r.correct
    ? '<span class="pill ok">PASS</span>'
    : `<span class="pill no">FAIL</span> <span class="muted2">missing: ${esc((r.missing || []).join(', '))}</span>`}</td>
      <td class="n">${tok(r.billedTokens)}</td>
      <td class="n">${(r.elapsedMs / 1000).toFixed(1)}s</td>
    </tr>`).join('')}
  </table>`;
}

// The cheapest probes answer straight from auto-loaded context and never touch
// the filesystem — their cost is the floor. Anything above that floor is what
// navigation cost, which makes this list the actual index-improvement backlog.
function expensiveSection(run) {
  const rows = (run.results || []).filter((r) => Number.isFinite(r.billedTokens));
  if (rows.length < 4) return '';
  const floor = Math.min(...rows.map((r) => r.billedTokens));
  const over = rows.map((r) => ({ ...r, mult: r.billedTokens / floor }))
    .filter((r) => r.mult >= 1.9)
    .sort((a, b) => b.billedTokens - a.billedTokens)
    .slice(0, 8);
  if (!over.length) return '';
  return `<h2 class="amber">What navigation actually cost — your improvement list</h2>
  <p class="lede">The cheapest question in this run cost <b>${tok(floor)}</b>. That is the floor:
     answered from context already loaded, no searching. Everything below paid more than that,
     and the multiple is what the agent spent hunting. <b>These are the questions worth making
     easier to answer</b> — a clearer index row should pull them toward the floor on the next run.</p>
  <table>
    <tr><th>Probe</th><th>Tokens</th><th>vs floor</th><th>Time</th></tr>
    ${over.map((r) => `<tr>
      <td class="mono">${esc(r.id)}</td>
      <td class="n">${tok(r.billedTokens)}</td>
      <td class="n ${r.mult >= 4 ? 'bad' : ''}">${r.mult.toFixed(1)}×</td>
      <td class="n">${(r.elapsedMs / 1000).toFixed(1)}s</td>
    </tr>`).join('')}
  </table>`;
}

function build() {
  const runs = loadRuns();
  const spec = fs.existsSync(PROBE_FILE) ? JSON.parse(fs.readFileSync(PROBE_FILE, 'utf8')) : { probes: [] };
  const latest = runs[0];

  const body = !latest
    ? `<div class="panel amber"><h3>No runs yet</h3>
       <p>Establish a baseline with:</p>
       <p class="cmd">node scripts/run-probes.js --label "baseline"</p></div>`
    : `
    <div class="tiles">
      <div class="tile"><div class="v ${pctOf(latest.correct, latest.total) >= 80 ? 'green' : 'amber'}">${pctOf(latest.correct, latest.total)}%</div><div class="k">Latest correct — ${esc(latest.label)}</div></div>
      <div class="tile"><div class="v accent">${tok(latest.billedTokens)}</div><div class="k">Tokens for the sweep</div></div>
      <div class="tile"><div class="v amber">${tok(Math.round(latest.billedTokens / (latest.total || 1)))}</div><div class="k">Per question</div></div>
      <div class="tile"><div class="v green">${runs.length}</div><div class="k">Runs recorded</div></div>
    </div>

    <h2>Runs — newest first</h2>
    <p class="lede">Δ compares each run to the one below it. <b>Green is the direction you want:</b>
       more correct, fewer tokens. Only compare runs on the same model.</p>
    ${runsTable(runs)}

    <h2 class="amber">Latest run by tier</h2>
    <p class="lede">
      <b>always-on</b> is answerable from <code>AGENTS.md</code>, which loads automatically every
      session — it tests whether the agent uses what it already has.
      <b>routed</b> requires navigating from an index to an owning doc — <b>this is the tier your
      indexing actually moves.</b> If routed costs far more per question than always-on, the gap is
      the price of navigation.
    </p>
    ${tierTable(latest)}

    ${expensiveSection(latest)}

    <h2>Every probe in the latest run</h2>
    ${probeRows(latest)}`;

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Probe baseline — controlled index test</title>
<style>
  :root{--bg:#0f1419;--panel:#1a2332;--panel-alt:#243044;--text:#e8edf4;--muted:#94a3b8;
        --accent:#38bdf8;--green:#34d399;--amber:#fbbf24;--red:#f87171;--border:#334155;
        --radius:14px;--font:"Segoe UI",system-ui,sans-serif}
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:var(--font);background:var(--bg);color:var(--text);line-height:1.55;font-size:18px}
  .page{max-width:940px;margin:0 auto;padding:2.5rem 1.25rem 4rem}
  header{margin-bottom:1.5rem;padding-bottom:1.3rem;border-bottom:2px solid var(--border)}
  header h1{font-size:clamp(1.6rem,4.6vw,2.2rem);letter-spacing:-.02em;line-height:1.25}
  header p{color:var(--muted);margin-top:.6rem;font-size:1rem}
  h2{font-size:.82rem;letter-spacing:.15em;text-transform:uppercase;font-weight:700;
     margin:2.4rem 0 .4rem;color:var(--accent)}
  h2.amber{color:var(--amber)}
  .lede{color:var(--muted);font-size:.94rem;margin-bottom:.9rem}
  .lede b{color:var(--text)}
  .panel{background:var(--panel);border:1px solid var(--border);border-radius:var(--radius);
         padding:1.2rem 1.3rem;margin-bottom:.9rem}
  .panel.amber{border-left:5px solid var(--amber)}
  .panel.accent{border-left:5px solid var(--accent)}
  .panel h3{font-size:1.05rem;margin-bottom:.45rem}
  .panel p{font-size:.94rem;color:var(--muted);margin-bottom:.4rem}
  .panel p b{color:var(--text)}
  .cmd{font-family:Consolas,monospace;background:#0c1118;border:1px solid var(--border);
       border-radius:8px;padding:.6rem .8rem;color:var(--green);font-size:.86rem;
       overflow-x:auto;white-space:nowrap;margin:.4rem 0}
  .tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.8rem;margin-bottom:.6rem}
  .tile{background:var(--panel);border:1px solid var(--border);border-radius:var(--radius);padding:1rem 1.1rem}
  .tile .v{font-size:1.9rem;font-weight:800;letter-spacing:-.02em}
  .tile .k{font-size:.78rem;color:var(--muted);margin-top:.2rem}
  .v.green{color:var(--green)} .v.amber{color:var(--amber)} .v.accent{color:var(--accent)}
  table{width:100%;border-collapse:collapse;font-size:.92rem;background:var(--panel);
        border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;margin-bottom:.9rem}
  th,td{text-align:left;padding:.6rem .8rem;border-bottom:1px solid var(--border)}
  th{font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);
     font-weight:700;background:var(--panel-alt)}
  tr:last-child td{border-bottom:none}
  td.n{font-family:Consolas,monospace;white-space:nowrap}
  td.mono{font-family:Consolas,monospace;color:var(--accent)}
  .muted2{color:var(--muted);font-size:.85em}
  .good{color:var(--green)} .bad{color:var(--red)}
  .pill{display:inline-block;padding:.14rem .5rem;border-radius:999px;font-size:.72rem;font-weight:700}
  .pill.ok{background:#12332a;color:var(--green)}
  .pill.no{background:#3a1c1c;color:var(--red)}
  code{background:var(--panel-alt);color:var(--accent);padding:.08rem .34rem;border-radius:4px;
       font-size:.85em;font-family:Consolas,monospace}
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
  <h1>Probe baseline</h1>
  <p>${spec.probes.length} fixed questions, each answered in its own fresh read-only session.
     Because the questions never change, any difference between runs is caused by what you changed —
     not by the tasks being different.</p>
</header>

${body}

<h2>How to use this</h2>
<div class="panel accent">
  <h3>1 — Take a baseline before touching anything</h3>
  <p class="cmd">node scripts/run-probes.js --label "baseline"</p>
  <h3>2 — Change exactly one thing</h3>
  <p>Reword <code>INDEX.md</code>, split a doc, shorten <code>AGENTS.md</code>. One change, so the
     delta has one cause.</p>
  <h3>3 — Re-run with a name that says what you changed</h3>
  <p class="cmd">node scripts/run-probes.js --label "index-rewrite"</p>
  <h3>4 — Compare a model, if you want that answer too</h3>
  <p class="cmd">node scripts/run-probes.js --label "opus" --model claude-opus-5-thinking-high</p>
  <p>Same questions, different model — the only fair way to see whether the expensive one earns it.</p>
</div>

<div class="panel amber">
  <h3>Rules that keep this honest</h3>
  <p><b>Never edit an existing question.</b> Comparability is the whole point — a reworded question
     silently invalidates every earlier run. Append new ones instead.</p>
  <p><b>Only compare runs on the same model.</b> A model change and an index change in the same
     delta cannot be told apart.</p>
  <p><b>Grading is keyword matching</b>, so it is approximate — it can mark a good answer wrong if
     it phrased things differently. Open the run JSON and read the answer before believing a
     surprising FAIL.</p>
</div>

<a class="back" href="/pages.html">← All pages</a>
<footer>Generated by <code>scripts/probe-report.js</code> ·
  ${esc(new Date().toISOString().slice(0, 16).replace('T', ' '))}</footer>

</div>
</body>
</html>`;
}

function main() {
  fs.writeFileSync(OUT, build(), 'utf8');
  process.stdout.write('Probe report written. View: http://127.0.0.1:8765/probe-baseline-log.html\n');
}

if (require.main === module) main();

module.exports = { build, loadRuns };
