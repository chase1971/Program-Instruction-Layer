/**
 * FILE: scripts/append-session-scorecard.js
 * PURPOSE: Append one session scorecard entry and regenerate the HTML log.
 *          Agents WRITE via this script only — never read session-scorecards-log.html.
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const DATA = path.join(ROOT, 'docs', 'session-scorecards.jsonl');
const HTML = path.join(ROOT, 'docs', 'session-scorecards-log.html');
const RUNNING = path.join(ROOT, 'docs', '.session-scorecard-running.json');

const DOC_EXT = new Set(['.md', '.mdc', '.html', '.json', '.jsonl', '.txt']);
const CODE_EXT = new Set([
  '.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs', '.py', '.css', '.scss',
  '.vue', '.java', '.go', '.rs', '.sql', '.bat', '.ps1', '.sh',
]);

const TIPS = {
  turns: 'How many messages you sent in this chat. Rough proxy for how long the session ran.',
  greps: 'How many times the agent searched the tree (grep, glob, file hunt). High usually means re-exploring instead of using a doc or rule.',
  corrections: 'Times you pushed back: "no", "wrong", "again", "third time". High means the agent drifted or misunderstood.',
  docsRulesOpened: 'Instruction files the agent opened to learn what to do (.md, .mdc, HTML guides). Count of names listed — not files it created.',
  docsRead: 'Document/instruction files read (.md, .mdc, .html, etc.).',
  codeRead: 'Source code files read (.ts, .js, .py, etc.).',
  docsEdited: 'Document/instruction files changed.',
  codeEdited: 'Source code files changed.',
  sessionType: 'Category for comparing similar sessions: Pearson, coding, Q&A, mixed, etc.',
  outcome: 'Done = finished the goal. Partial = some progress. Abandoned = stopped early.',
  lowConfidence: 'The numbers may be wrong because Cursor summarized away the start of this chat — counts are best-guess.',
  summarized: 'Cursor compressed older messages to save space. Early reads/searches may be missing from the counts.',
  worthNoting: 'Something unusual about this session worth a glance — not necessarily a problem.',
  captureSuggest: 'The agent\'s idea for a future rule or doc. Not a list of what you already asked to build unless you did.',
};

function esc(s) {
  return String(s ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function readEntries() {
  if (!fs.existsSync(DATA)) return [];
  return fs
    .readFileSync(DATA, 'utf8')
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean)
    .map((l, i) => {
      try {
        return JSON.parse(l);
      } catch (e) {
        throw new Error(`Invalid JSONL line ${i + 1}: ${e.message}`);
      }
    });
}

function writeEntries(entries) {
  const body = entries.map((e) => JSON.stringify(e)).join('\n') + (entries.length ? '\n' : '');
  fs.writeFileSync(DATA, body, 'utf8');
}

function fileKind(filePath) {
  const ext = path.extname(String(filePath)).toLowerCase();
  if (DOC_EXT.has(ext)) return 'doc';
  if (CODE_EXT.has(ext)) return 'code';
  return 'other';
}

function splitFiles(list) {
  const doc = [];
  const code = [];
  const other = [];
  for (const f of list) {
    const k = fileKind(f);
    if (k === 'doc') doc.push(f);
    else if (k === 'code') code.push(f);
    else other.push(f);
  }
  return { doc, code, other };
}

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

function tip(label, tipText) {
  return `<abbr class="tip" title="${esc(tipText)}">${esc(label)}</abbr>`;
}

function pill(text, cls, tipText) {
  const t = tipText ? ` title="${esc(tipText)}"` : '';
  return `<span class="pill ${cls}"${t}>${esc(text)}</span>`;
}

function outcomeClass(o) {
  const x = String(o || '').toLowerCase();
  if (x === 'done') return 'p1';
  if (x === 'partial') return 'p2';
  if (x === 'abandoned') return 'p3';
  return 'p0';
}

function sessionTypeLabel(t) {
  const map = {
    pearson: 'Pearson work',
    coding: 'Coding',
    'q&a': 'Q&A learning',
    qa: 'Q&A learning',
    mixed: 'Mixed (talk + edits)',
    'refactor-plan': 'Refactor planning',
    'end-of-session': 'Wrap-up',
  };
  return map[String(t || '').toLowerCase()] || t || 'Mixed';
}

function outcomeLabel(o) {
  const map = { done: 'Finished', partial: 'Partly done', abandoned: 'Stopped early' };
  return map[String(o || '').toLowerCase()] || o || '—';
}

function metricCell(label, value, warn, tipText) {
  const cls = warn ? ' metric-warn' : '';
  const dt = tipText
    ? `<abbr class="tip" title="${esc(tipText)}">${esc(label)}</abbr>`
    : esc(label);
  return `<div class="metric${cls}"><dt>${dt}</dt><dd>${esc(value)}</dd></div>`;
}

function fileListBlock(title, files, tipText) {
  if (!files.length) return '';
  return `<div class="file-group">
    <h4>${tip(title, tipText)} (${files.length})</h4>
    <ul>${files.map((f) => `<li><code>${esc(f)}</code></li>`).join('')}</ul>
  </div>`;
}

function sessionCard(e, inProgress) {
  const greps = Number(e.greps);
  const corrections = Number(e.corrections);
  const turns = Number(e.turns);
  const grepWarn = greps >= 8;
  const corrWarn = corrections >= 3;
  const confLow = String(e.confidence || '').toLowerCase() === 'low';

  const filesRead = Array.isArray(e.filesReadList) ? e.filesReadList : [];
  const filesEdited = Array.isArray(e.filesEditedList) ? e.filesEditedList : [];
  const readSplit = splitFiles(filesRead);
  const editSplit = splitFiles(filesEdited);

  const docsRules = Array.isArray(e.docsRulesOpened)
    ? (e.docsRulesOpened.length ? e.docsRulesOpened.join(', ') : 'none')
    : (e.docsRulesOpened || e.docsRules || 'none');
  const summary = e.summaryHuman || e.goal || '—';

  let worthNoting = '';
  if (e.worthNoting || e.spike) {
    worthNoting = `<div class="note-box">
      <strong>${tip('Worth noting', TIPS.worthNoting)}:</strong> ${esc(e.worthNoting || e.spike)}
    </div>`;
  }
  let captureBlock = '';
  if (e.captureCandidate) {
    captureBlock = `<div class="capture-box">
      <strong>${tip('Agent suggests capturing', TIPS.captureSuggest)}:</strong> ${esc(e.captureCandidate)}
    </div>`;
  }

  const fileDetails =
    filesRead.length || filesEdited.length
      ? `<details class="file-details">
          <summary>File breakdown (hover labels for definitions)</summary>
          <div class="file-grid">
            ${fileListBlock('Docs read', readSplit.doc, TIPS.docsRead)}
            ${fileListBlock('Code read', readSplit.code, TIPS.codeRead)}
            ${fileListBlock('Other read', readSplit.other, 'Other paths opened')}
            ${fileListBlock('Docs edited', editSplit.doc, TIPS.docsEdited)}
            ${fileListBlock('Code edited', editSplit.code, TIPS.codeEdited)}
            ${fileListBlock('Other edited', editSplit.other, 'Other paths changed')}
          </div>
        </details>`
      : '';

  const typePill = pill(sessionTypeLabel(e.sessionType), 'p0', TIPS.sessionType);
  const outPill = inProgress
    ? pill('In progress — tallies update as tasks finish', 'p0', 'Counts logged after each task; safe if chat summarizes later.')
    : pill(outcomeLabel(e.outcome), outcomeClass(e.outcome), TIPS.outcome);

  const cardCls = inProgress ? 'session-card in-progress' : 'session-card';

  return `<article class="${cardCls}">
    <header class="session-head">
      <div class="pills">
        <span class="time">${esc(timeShort(e.timestamp))}</span>
        ${typePill}${outPill}
        ${confLow ? pill('Low confidence counts', 'p2', TIPS.lowConfidence) : ''}
        ${e.summarized && !inProgress ? pill('Chat was summarized', 'p2', TIPS.summarized) : ''}
        ${inProgress ? pill('Live tally', 'p1', 'Updated after each completed task — survives summarize.') : ''}
      </div>
      <div class="model">${esc(e.model || '—')}</div>
    </header>
    <p class="summary-human">${esc(summary)}</p>
    <div class="metric-grid">
      ${metricCell('Your messages', e.turns ?? '—', turns >= 20, TIPS.turns)}
      ${metricCell('Searches', e.greps ?? '—', grepWarn, TIPS.greps)}
      ${metricCell('You corrected me', e.corrections ?? '—', corrWarn, TIPS.corrections)}
      ${metricCell('Docs/rules read', docsRules === 'none' ? 'none' : docsRules, docsRules === 'none', TIPS.docsRulesOpened)}
    </div>
    <div class="metric-grid counts">
      ${metricCell('Doc files read', readSplit.doc.length, false, TIPS.docsRead)}
      ${metricCell('Code files read', readSplit.code.length, false, TIPS.codeRead)}
      ${metricCell('Doc files edited', editSplit.doc.length, false, TIPS.docsEdited)}
      ${metricCell('Code files edited', editSplit.code.length, false, TIPS.codeEdited)}
    </div>
    ${e.redFlags ? `<p class="red-flags"><strong>Red flags:</strong> ${esc(e.redFlags)}</p>` : ''}
    ${worthNoting}${captureBlock}
    ${e.nextSession ? `<p class="next"><strong>Next time:</strong> ${esc(e.nextSession)}</p>` : ''}
    ${fileDetails}
  </article>`;
}

function legendHtml() {
  const items = [
    ['Your messages', TIPS.turns],
    ['Searches', TIPS.greps],
    ['You corrected me', TIPS.corrections],
    ['Docs/rules read', TIPS.docsRulesOpened],
    ['Low confidence counts', TIPS.lowConfidence],
    ['Chat was summarized', TIPS.summarized],
    ['Agent suggests capturing', TIPS.captureSuggest],
  ];
  return `<details class="legend">
    <summary>What do these numbers mean? (hover any label on a card too)</summary>
    <ul>${items.map(([l, t]) => `<li><strong>${esc(l)}:</strong> ${esc(t)}</li>`).join('')}</ul>
  </details>`;
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
      <div class="day-sessions">${sessions.map(sessionCard).join('')}</div>
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
  <title>Session scorecards — running log</title>
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
    .legend, .file-details { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 0.65rem 0.85rem; margin-bottom: 1rem; }
    .legend summary, .file-details summary { cursor: pointer; min-height: 44px; display: flex; align-items: center; font-weight: 600; }
    .legend ul { margin: 0.5rem 0 0; padding-left: 1.2rem; color: var(--muted); font-size: 0.92rem; }
    .legend li { margin: 0.35rem 0; }
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
    .metric-grid.counts { opacity: 0.95; }
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
    .red-flags { color: var(--danger); font-size: 0.9rem; margin: 0.45rem 0 0; }
    .next { color: var(--muted); font-size: 0.9rem; margin: 0.45rem 0 0; }
    .file-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.65rem; margin-top: 0.5rem; }
    @media (max-width: 700px) { .file-grid { grid-template-columns: 1fr; } }
    .file-group h4 { margin: 0 0 0.25rem; font-size: 0.85rem; color: var(--accent); }
    .file-group ul { margin: 0; padding-left: 1rem; font-size: 0.8rem; color: var(--muted); }
    .file-group li { margin: 0.15rem 0; word-break: break-all; }
    .empty { color: var(--muted); padding: 2rem; text-align: center; }
    .footer { margin-top: 2rem; color: var(--muted); font-size: 0.85rem; }
    .footer a { color: var(--accent); }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Session scorecards</h1>
    <p class="subtitle">Hover underlined labels for definitions. Grouped by day — data in <code>session-scorecards.jsonl</code>.</p>
    ${legendHtml()}
    <div class="summary-bar">
      <div><dt>Total sessions</dt><dd>${total}</dd></div>
      <div><dt>Latest</dt><dd style="font-size:1rem">${esc(last)}</dd></div>
    </div>
    ${inProgressSection}
    ${daySections}
    <p class="footer">Generated by <code>scripts/append-session-scorecard.js</code> ·
      <a href="http://127.0.0.1:8765/context-engineering-capture-costs.html">Capture ladder</a></p>
  </div>
</body>
</html>`;
}

function regenerate() {
  const entries = readEntries();
  const running = readRunning();
  fs.writeFileSync(HTML, buildHtml(entries, running), 'utf8');
  return entries.length;
}

function readRunning() {
  if (!fs.existsSync(RUNNING)) return null;
  try {
    return JSON.parse(fs.readFileSync(RUNNING, 'utf8'));
  } catch {
    return null;
  }
}

function writeRunning(data) {
  fs.writeFileSync(RUNNING, JSON.stringify(data, null, 2), 'utf8');
}

function clearRunning() {
  if (fs.existsSync(RUNNING)) fs.unlinkSync(RUNNING);
}

function mergeUnique(list, add) {
  const set = new Set(list || []);
  for (const x of add || []) if (x) set.add(x);
  return [...set];
}

function emptyRunning() {
  return {
    sessionStarted: new Date().toISOString(),
    model: '',
    sessionType: 'mixed',
    summaryHuman: 'Session in progress…',
    turns: 0,
    greps: 0,
    corrections: 0,
    docsRulesOpened: [],
    filesReadList: [],
    filesEditedList: [],
    taskLog: [],
  };
}

function runningToDisplayEntry(r) {
  return {
    timestamp: r.sessionStarted,
    model: r.model || '—',
    sessionType: r.sessionType || 'mixed',
    summaryHuman: r.summaryHuman || 'Session in progress…',
    outcome: 'Partial',
    summarized: false,
    confidence: 'high',
    turns: r.turns,
    greps: r.greps,
    corrections: r.corrections,
    docsRulesOpened: r.docsRulesOpened,
    filesReadList: r.filesReadList,
    filesEditedList: r.filesEditedList,
    worthNoting: r.taskLog?.length
      ? `Tasks logged so far: ${r.taskLog.length} (last: ${r.taskLog[r.taskLog.length - 1].note || '—'})`
      : '',
  };
}

function bumpRunning(delta) {
  let r = readRunning() || emptyRunning();
  if (delta.model) r.model = delta.model;
  if (delta.sessionType) r.sessionType = delta.sessionType;
  if (delta.summaryHuman) r.summaryHuman = delta.summaryHuman;
  r.turns += Number(delta.addTurns || 0);
  r.greps += Number(delta.addGreps || 0);
  r.corrections += Number(delta.addCorrections || 0);
  r.filesReadList = mergeUnique(r.filesReadList, delta.filesRead);
  r.filesEditedList = mergeUnique(r.filesEditedList, delta.filesEdited);
  r.docsRulesOpened = mergeUnique(r.docsRulesOpened, delta.docsRulesOpened);
  if (delta.chunkNote) {
    if (!r.taskLog) r.taskLog = [];
    r.taskLog.push({
      time: new Date().toISOString(),
      note: delta.chunkNote,
      addGreps: delta.addGreps || 0,
      filesRead: delta.filesRead || [],
      filesEdited: delta.filesEdited || [],
    });
  }
  writeRunning(r);
  regenerate();
  return r;
}

function finalizeRunning(meta) {
  const r = readRunning();
  const base = r || emptyRunning();
  const entry = normalize({
    timestamp: meta.timestamp || new Date().toISOString(),
    model: meta.model || base.model,
    sessionType: meta.sessionType || base.sessionType,
    summaryHuman: meta.summaryHuman || base.summaryHuman,
    outcome: meta.outcome || 'Done',
    summarized: !!meta.summarized,
    confidence: meta.confidence || (meta.summarized ? 'low' : 'high'),
    turns: base.turns + Number(meta.addTurns || 0),
    greps: base.greps,
    corrections: base.corrections + Number(meta.addCorrections || 0),
    docsRulesOpened: base.docsRulesOpened.length
      ? base.docsRulesOpened.join(', ')
      : 'none',
    filesReadList: base.filesReadList,
    filesEditedList: base.filesEditedList,
    worthNoting: meta.worthNoting || '',
    captureCandidate: meta.captureCandidate || '',
    nextSession: meta.nextSession || '',
  });
  const entries = readEntries();
  entries.push(entry);
  writeEntries(entries);
  clearRunning();
  regenerate();
  return entry;
}

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

function normalize(entry) {
  if (!entry.timestamp) entry.timestamp = new Date().toISOString();
  if (entry.docsRules && !entry.docsRulesOpened) entry.docsRulesOpened = entry.docsRules;
  if (entry.spike && !entry.worthNoting) entry.worthNoting = entry.spike;
  return entry;
}

function main() {
  if (process.argv.includes('--rebuild')) {
    const n = regenerate();
    console.log(`Rebuilt ${HTML} (${n} sessions)`);
    return;
  }
  const bump = loadJsonArg('--bump-file');
  if (bump) {
    bumpRunning(bump);
    console.log('Running tally updated. View: http://127.0.0.1:8765/session-scorecards-log.html');
    return;
  }
  const finalize = loadJsonArg('--finalize-file');
  if (finalize) {
    finalizeRunning(finalize);
    console.log('Session finalized to jsonl. View: http://127.0.0.1:8765/session-scorecards-log.html');
    return;
  }
  const newEntry = loadNewEntry();
  if (!newEntry) {
    console.error('Usage: --file path.json | --bump-file delta.json | --finalize-file meta.json | --rebuild');
    process.exit(1);
  }
  const entries = readEntries();
  entries.push(normalize(newEntry));
  writeEntries(entries);
  regenerate();
  console.log(`Appended scorecard. View: http://127.0.0.1:8765/session-scorecards-log.html`);
}

main();
