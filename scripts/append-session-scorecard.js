/**
 * FILE: scripts/append-session-scorecard.js
 * PURPOSE: Append one session scorecard entry and regenerate the HTML log.
 *          Agents WRITE via this script only — never read session-scorecards-log.html.
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
// Folder was renamed docs/ -> "agent docs/" on 2026-08-01. Kept as one constant so
// the next rename is a single edit. Note the space — quote it in any shell command.
const DOCS_DIR = 'agent docs';
const DATA = path.join(ROOT, DOCS_DIR, 'session-scorecards.jsonl');
const HTML = path.join(ROOT, DOCS_DIR, 'session-scorecards-log.html');
const RUNNING = path.join(ROOT, DOCS_DIR, '.session-scorecard-running.json');
const MDC_STATS = path.join(ROOT, DOCS_DIR, 'mdc-read-stats.json');

const DOC_EXT = new Set(['.md', '.mdc', '.html', '.json', '.jsonl', '.txt']);
const CODE_EXT = new Set([
  '.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs', '.py', '.css', '.scss',
  '.vue', '.java', '.go', '.rs', '.sql', '.bat', '.ps1', '.sh',
]);

const TIPS = {
  turns: 'How many messages you sent in this chat. Rough proxy for how long the session ran.',
  greps: 'How many times the agent searched the tree (grep, glob, file hunt). High usually means re-exploring instead of using a doc or rule.',
  corrections: 'Times you pushed back: "no", "wrong", "again", "third time". High means the agent drifted or misunderstood.',
  docsRulesOpened: 'Instruction files the agent opened to learn what to do (.md, .mdc, HTML guides). Names only in the card — hover for full path.',
  mdcReadViaTool: 'Times the agent used Read on a .mdc file. Does NOT include Cursor auto-injecting rules when a matching file is open.',
  mdcLifetime: 'Lifetime total across sessions — Read tool on .mdc only. Auto-injected rules are invisible to this log.',
  docsRead: 'Document/instruction files read (.md, .mdc, .html, etc.).',
  codeRead: 'Source code files read (.ts, .js, .py, etc.).',
  docsEdited: 'Document/instruction files changed.',
  codeEdited: 'Source code files changed.',
  toolsUsed: 'Non-read/edit agent tools (MCP browser, Task, WebFetch, etc.). Snapshots counted separately.',
  browserSnapshots: 'Explicit browser_snapshot MCP calls — high count usually means exploratory automation.',
  sessionType: 'Category for comparing similar sessions: Pearson, coding, Q&A, mixed, etc.',
  outcome: 'Done = finished the goal. Partial = some progress. Abandoned = stopped early.',
  lowConfidence: 'The numbers may be wrong because Cursor summarized away the start of this chat — counts are best-guess.',
  summarized: 'Cursor compressed older messages to save space. Early reads/searches may be missing from the counts.',
  notBumped: 'The agent never logged a running tally during this session, so every count here was reconstructed from memory at the end. Treat them as order-of-magnitude. If this pill keeps appearing, the bump rule is not being followed.',
  hookTally: 'Cursor postToolUse hook auto-counted reads, edits, and searches into the running file. Greps/files are more trustworthy; task boundaries still need agent bumps with chunkNote.',
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

/** Display name in HTML lists — basename only; full path in title tooltip. */
function fileLabel(filePath) {
  return path.basename(String(filePath || '').replace(/\\/g, '/')) || String(filePath || '');
}


function dedupePaths(list) {
  const seen = new Set();
  const out = [];
  for (const raw of list || []) {
    const p = String(raw || '').replace(/\\/g, '/');
    if (!p || seen.has(p)) continue;
    seen.add(p);
    out.push(p);
  }
  return out;
}

/** AGENTS.md / CLAUDE.md — show which app or Programs root. */
function agentMarkdownLabel(filePath) {
  const norm = String(filePath || '').replace(/\\/g, '/');
  const base = path.basename(norm).toLowerCase();
  if (base === 'agents.md' || base === 'claude.md') {
    const kind = base === 'agents.md' ? 'AGENTS.md' : 'CLAUDE.md';
    if (norm.includes('School Scrips/Macro App/')) return `${kind} — Macro App`;
    const appMatch = norm.match(/School Scrips\/([^/]+)/);
    if (appMatch) return `${kind} — ${appMatch[1]}`;
    if (norm.includes('/Programs/') || norm.startsWith('AGENTS.md') || norm.endsWith('/AGENTS.md')) {
      return `${kind} — Programs root`;
    }
    return `${kind} — ${path.dirname(norm).split('/').slice(-2).join('/') || 'tree'}`;
  }
  return fileLabel(norm);
}

function markdownSortRank(filePath) {
  const norm = String(filePath || '').replace(/\\/g, '/').toLowerCase();
  if (norm.endsWith('.mdc')) return 0;
  if (norm.endsWith('/agents.md')) return 1;
  if (norm.endsWith('/claude.md')) return 2;
  return 3;
}

function sortMarkdownPaths(list) {
  return dedupePaths(list).sort((a, b) => {
    const ra = markdownSortRank(a);
    const rb = markdownSortRank(b);
    if (ra !== rb) return ra - rb;
    return agentMarkdownLabel(a).localeCompare(agentMarkdownLabel(b));
  });
}

function toolDisplayLabel(key) {
  const s = String(key || '');
  const idx = s.indexOf(':');
  if (idx === -1) return s;
  const server = s.slice(0, idx).replace(/^project-0-Programs-/, '');
  return `${server}:${s.slice(idx + 1)}`;
}

function pathListHtml(paths, labelFn) {
  if (!paths.length) return '';
  return `<ul class="path-list">${paths.map((p) => {
    const isMdc = String(p).toLowerCase().endsWith('.mdc');
    return `<li><code class="${isMdc ? 'path-mdc' : ''}" title="${esc(p)}">${esc(labelFn(p))}</code></li>`;
  }).join('')}</ul>`;
}

function activityChip(label, count) {
  if (!count) return '';
  return `<span class="activity-chip">${esc(label)} (${count})</span>`;
}

function activityCategoryBlock(title, paths, tipText, labelFn) {
  if (!paths.length) return '';
  return `<div class="path-section">
    <h4>${tip(title, tipText)} (${paths.length})</h4>
    ${pathListHtml(paths, labelFn)}
  </div>`;
}

function toolsSectionBody(e) {
  const counts = e.toolsUsedCounts && typeof e.toolsUsedCounts === 'object' ? e.toolsUsedCounts : {};
  const entries = Object.entries(counts).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  const snaps = Number(e.browserSnapshots) || 0;
  if (!entries.length && !snaps) return '';

  let html = `<div class="path-section path-section-tools">
    <h4>${tip('Tools used', TIPS.toolsUsed)}${snaps ? ` · ${esc(String(snaps))} ${tip('snapshots', TIPS.browserSnapshots)}` : ''}</h4>`;
  if (entries.length) {
    html += `<ul class="path-list path-list-tools">${entries.map(([key, n]) => {
      const isSnap = key.endsWith(':browser_snapshot');
      const cls = isSnap ? 'path-snapshot' : '';
      const suffix = n > 1 ? ` × ${n}` : '';
      return `<li><code class="${cls}" title="${esc(key)}">${esc(toolDisplayLabel(key))}${suffix}</code></li>`;
    }).join('')}</ul>`;
  } else if (snaps) {
    html += `<p class="muted-inline">${snaps} browser snapshot(s) — detail not in tool counts (pre-hook session).</p>`;
  }
  html += '</div>';
  return html;
}

function toolsChipCount(e) {
  const counts = e.toolsUsedCounts && typeof e.toolsUsedCounts === 'object' ? e.toolsUsedCounts : {};
  const uses = Object.values(counts).reduce((sum, n) => sum + n, 0);
  const snaps = Number(e.browserSnapshots) || 0;
  return uses + snaps;
}

function activityBreakdown(e, readSplit, editSplit, docsRulesList) {
  const markdownRead = sortMarkdownPaths([...docsRulesList, ...readSplit.doc]);
  const codeRead = dedupePaths(readSplit.code).sort((a, b) => fileLabel(a).localeCompare(fileLabel(b)));
  const markdownEdited = sortMarkdownPaths(editSplit.doc);
  const codeEdited = dedupePaths(editSplit.code);

  const chips = [
    activityChip('Tools', toolsChipCount(e)),
    activityChip('Markdowns read', markdownRead.length) || `<span class="activity-chip">Markdowns read (0)</span>`,
    activityChip('Code read', codeRead.length) || `<span class="activity-chip">Code read (0)</span>`,
    activityChip('Markdowns edited', markdownEdited.length),
    activityChip('Code edited', codeEdited.length),
  ].filter(Boolean);

  const body = [
    toolsSectionBody(e),
    activityCategoryBlock('Markdowns read', markdownRead, TIPS.docsRead, agentMarkdownLabel),
    activityCategoryBlock('Code read', codeRead, TIPS.codeRead, fileLabel),
    activityCategoryBlock('Markdowns edited', markdownEdited, TIPS.docsEdited, agentMarkdownLabel),
    activityCategoryBlock('Code edited', codeEdited, TIPS.codeEdited, fileLabel),
  ].filter(Boolean).join('');

  if (!chips.length && !body) return '';

  return `<details class="activity-details">
    <summary class="activity-summary">
      <span class="activity-summary-label">Activity</span>
      <span class="activity-chips">${chips.join('')}</span>
    </summary>
    <div class="activity-body">${body}</div>
  </details>`;
}


function readMdcLifetimeStats() {
  if (!fs.existsSync(MDC_STATS)) return [];
  try {
    const raw = JSON.parse(fs.readFileSync(MDC_STATS, 'utf8'));
    return Object.entries(raw)
      .map(([name, row]) => ({ name, count: row.count || 0, last: row.last || null }))
      .sort((a, b) => b.count - a.count || a.name.localeCompare(b.name));
  } catch {
    return [];
  }
}

function mdcLifetimeBlock() {
  const rows = readMdcLifetimeStats();
  if (!rows.length) {
    return `<details class="legend">
      <summary>${tip('MDC lifetime (Read tool)', TIPS.mdcLifetime)} — no .mdc reads logged yet</summary>
      <p class="muted-inline">When Cursor <strong>auto-injects</strong> a glob rule because a file is open, that does not appear here — only explicit agent <code>Read</code> on a <code>.mdc</code> file.</p>
    </details>`;
  }
  const top = rows.slice(0, 12);
  const rest = rows.length - top.length;
  return `<details class="legend">
    <summary>${tip('MDC lifetime (Read tool)', TIPS.mdcLifetime)} — ${rows.length} rule file(s) opened via Read</summary>
    <p class="muted-inline">Auto-injected glob rules (file open, no Read) are <strong>not</strong> counted. Low numbers here do not mean a rule is useless.</p>
    <table class="mdc-table">
      <thead><tr><th>Rule file</th><th>Reads</th><th>Last</th></tr></thead>
      <tbody>${top.map((r) => `<tr>
        <td><code>${esc(r.name)}</code></td>
        <td>${r.count}</td>
        <td>${r.last ? esc(timeShort(r.last)) : '—'}</td>
      </tr>`).join('')}</tbody>
    </table>
    ${rest > 0 ? `<p class="muted-inline">+ ${rest} more in <code>agent docs/mdc-read-stats.json</code></p>` : ''}
  </details>`;
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

function normalizeDocsRulesOpened(val) {
  if (Array.isArray(val)) return val;
  if (!val || val === 'none') return [];
  if (typeof val === 'string') {
    return val.split(',').map((s) => s.trim()).filter(Boolean);
  }
  return [];
}

function metricCell(label, value, warn, tipText) {
  const cls = warn ? ' metric-warn' : '';
  const dt = tipText
    ? `<abbr class="tip" title="${esc(tipText)}">${esc(label)}</abbr>`
    : esc(label);
  return `<div class="metric${cls}"><dt>${dt}</dt><dd>${esc(value)}</dd></div>`;
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

  const docsRulesList = normalizeDocsRulesOpened(e.docsRulesOpened || e.docsRules);
  const summary = e.summaryHuman || e.goal || '—';
  const browserSnapshots = Number(e.browserSnapshots) || 0;

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

  const activityBlock = activityBreakdown(e, readSplit, editSplit, docsRulesList);

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
        ${e.bumped === false && !inProgress ? pill('Not bumped — counts reconstructed', 'p2', TIPS.notBumped) : ''}
        ${e.hookTally ? pill('Hook tallied', 'p1', TIPS.hookTally) : ''}
        ${inProgress ? pill('Live tally', 'p1', 'Updated after each completed task — survives summarize.') : ''}
      </div>
      <div class="model">${esc(e.model || '—')}</div>
    </header>
    <p class="summary-human">${esc(summary)}</p>
    <div class="metric-grid metric-grid-core">
      ${metricCell('Your messages', e.turns ?? '—', turns >= 20, TIPS.turns)}
      ${metricCell('Searches', e.greps ?? '—', grepWarn, TIPS.greps)}
      ${metricCell('You corrected me', e.corrections ?? '—', corrWarn, TIPS.corrections)}
      ${browserSnapshots ? metricCell('Browser snapshots', browserSnapshots, browserSnapshots >= 3, TIPS.browserSnapshots) : ''}
    </div>
    ${activityBlock}
    ${e.redFlags ? `<p class="red-flags"><strong>Red flags:</strong> ${esc(e.redFlags)}</p>` : ''}
    ${worthNoting}${captureBlock}
    ${e.nextSession ? `<p class="next"><strong>Next time:</strong> ${esc(e.nextSession)}</p>` : ''}
  </article>`;
}

function legendHtml() {
  const items = [
    ['Your messages', TIPS.turns],
    ['Searches', TIPS.greps],
    ['You corrected me', TIPS.corrections],
    ['Browser snapshots', TIPS.browserSnapshots],
    ['Tools used', TIPS.toolsUsed],
    ['Markdowns read', TIPS.docsRead],
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
    .legend, .file-details, .activity-details { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 0.65rem 0.85rem; margin-bottom: 0.65rem; }
    .legend summary, .file-details summary, .activity-details summary { cursor: pointer; min-height: 44px; display: flex; align-items: center; font-weight: 600; }
    .activity-summary { flex-wrap: wrap; gap: 0.5rem 0.75rem; align-items: center; list-style: none; }
    .activity-summary::-webkit-details-marker { display: none; }
    .activity-summary-label { color: var(--text); flex-shrink: 0; }
    .activity-chips { display: flex; flex-wrap: wrap; gap: 0.35rem 0.5rem; align-items: center; }
    .activity-chip {
      display: inline-block; padding: 0.2em 0.55em; border-radius: 6px;
      font-size: 0.78rem; font-weight: 600; background: #1e3350; color: var(--accent);
      border: 1px solid rgba(94, 184, 255, 0.35);
    }
    .legend ul { margin: 0.5rem 0 0; padding-left: 1.2rem; color: var(--muted); font-size: 0.92rem; }
    .legend li { margin: 0.35rem 0; }
    .muted-inline { color: var(--muted); font-size: 0.9rem; margin: 0.5rem 0 0; }
    .mdc-table { width: 100%; border-collapse: collapse; margin-top: 0.65rem; font-size: 0.9rem; }
    .mdc-table th, .mdc-table td { text-align: left; padding: 0.35rem 0.5rem; border-bottom: 1px solid var(--border); }
    .mdc-table th { color: var(--muted); font-size: 0.78rem; text-transform: uppercase; }
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
    .metric-grid-core { grid-template-columns: repeat(3, 1fr); }
    @media (max-width: 700px) { .metric-grid, .metric-grid-core { grid-template-columns: repeat(2, 1fr); } }
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
    .activity-body { margin-top: 0.35rem; }
    .path-section { margin: 0.5rem 0 0.65rem; padding-top: 0.35rem; border-top: 1px solid rgba(61, 81, 102, 0.45); }
    .path-section:first-child { border-top: none; padding-top: 0; }
    .path-section h4 { margin: 0 0 0.35rem; font-size: 0.85rem; color: var(--accent); font-weight: 600; }
    .path-list { margin: 0; padding: 0; list-style: none; font-size: 0.82rem; color: var(--muted); }
    .path-list li { margin: 0.2rem 0; min-height: 1.35rem; display: flex; align-items: baseline; }
    .path-list code { font-family: Consolas, "Courier New", monospace; font-size: 0.88rem; color: var(--text); word-break: break-all; }
    .path-list code.path-mdc { color: var(--warn); font-weight: 600; }
    .path-list code.path-snapshot { color: var(--accent); }
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
    ${mdcLifetimeBlock()}
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
    mdcReadsList: [],
    filesReadList: [],
    filesEditedList: [],
    toolsUsedCounts: {},
    browserSnapshots: 0,
    taskLog: [],
    hookTally: false,
    agentBumped: false,
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
    mdcReadsList: r.mdcReadsList || [],
    filesReadList: r.filesReadList,
    filesEditedList: r.filesEditedList,
    toolsUsedCounts: r.toolsUsedCounts || {},
    browserSnapshots: r.browserSnapshots || 0,
    worthNoting: [
      r.taskLog?.length
        ? `Tasks logged so far: ${r.taskLog.length} (last: ${r.taskLog[r.taskLog.length - 1].note || '—'})`
        : '',
      r.hookTally ? 'Hook auto-tally active.' : '',
    ]
      .filter(Boolean)
      .join(' '),
    hookTally: !!r.hookTally,
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
  r.mdcReadsList = mergeUnique(r.mdcReadsList, delta.mdcReadsList);
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
  if (
    delta.chunkNote
    || delta.addGreps
    || delta.addTurns
    || delta.addCorrections
    || (delta.filesRead && delta.filesRead.length)
    || (delta.filesEdited && delta.filesEdited.length)
    || (delta.docsRulesOpened && delta.docsRulesOpened.length)
  ) {
    r.agentBumped = true;
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
    // Derived, never self-reported: a running file only exists if bumps were logged.
    // Separates "the chat was summarized" from "the agent forgot to bump" — different
    // failures, different fixes. Counts reconstructed at the end are guesses.
    bumped: !!(r && r.agentBumped),
    hookTally: !!base.hookTally,
    confidence:
      meta.confidence
      || (r && r.agentBumped ? 'high' : base.hookTally ? 'medium' : 'low'),
    turns: base.turns + Number(meta.addTurns || 0),
    greps: base.greps,
    corrections: base.corrections + Number(meta.addCorrections || 0),
    docsRulesOpened: base.docsRulesOpened.length ? base.docsRulesOpened : 'none',
    filesReadList: base.filesReadList,
    filesEditedList: base.filesEditedList,
    mdcReadsList: base.mdcReadsList || [],
    toolsUsedCounts: base.toolsUsedCounts || {},
    browserSnapshots: base.browserSnapshots || 0,
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
