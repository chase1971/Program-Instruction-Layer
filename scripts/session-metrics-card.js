/**
 * FILE: scripts/session-metrics-card.js
 * PURPOSE: One session card on session-metrics-log.html — trust pills, activity tiles,
 *          file lists — plus the hover tips and small HTML helpers the page shares.
 */
'use strict';

const path = require('path');
const { NAV_TIP } = require('./scorecard-navigation-path');

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
  partialConfidence: 'Some counts were logged (hook or late bumps) but the chat was summarized — early reads/searches are probably missing.',
  summarized: 'Cursor compressed older messages to save space. Early reads/searches may be missing from the counts.',
  summarizedNoBump: 'Chat was summarized AND the agent never ran --bump-file. Counts are a partial hook tally at best — treat as incomplete.',
  summarizedEarlyMissing: 'Chat was summarized before bumps/hooks captured the start. File lists and search counts understate what actually happened.',
  hookOnlyNoBump: 'Hook auto-tally ran but the agent never logged task bumps — no chunk boundaries, easy to miss work.',
  preHookWorkUntracked: 'Hook tally started on this tool call — any reads/searches before that are not in the counts.',
  missingEarlyWorkLive: 'Live tally is missing work from before the hook started or before the agent bumped a task.',
  notBumped: 'The agent never logged a running tally during this session, so every count here was reconstructed from memory at the end. Treat them as order-of-magnitude. If this pill keeps appearing, the bump rule is not being followed.',
  hookTally: 'Cursor postToolUse hook auto-counted reads, edits, and searches into the running file. Greps/files are more trustworthy; task boundaries still need agent bumps with chunkNote.',
  navigationPath: NAV_TIP,
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

function pathListHtml(paths, labelFn, markdownRed = false) {
  if (!paths.length) return '';
  return `<ul class="path-list">${paths.map((p) => {
    const norm = String(p).toLowerCase();
    const isMdc = norm.endsWith('.mdc');
    const isDoc = markdownRed || fileKind(p) === 'doc';
    const cls = isMdc ? 'path-mdc' : (isDoc ? 'path-doc' : '');
    return `<li><code class="${cls}" title="${esc(p)}">${esc(labelFn(p))}</code></li>`;
  }).join('')}</ul>`;
}

function staticMetric(label, value, warn, tipText) {
  const dt = tipText
    ? `<abbr class="tip" title="${esc(tipText)}">${esc(label)}</abbr>`
    : esc(label);
  return `<div class="metric${warn ? ' metric-warn' : ''}">
    <dt>${dt}</dt>
    <dd>${esc(String(value ?? '—'))}</dd>
  </div>`;
}

function expandableMetric(label, count, paths, tipText, labelFn, opts = {}) {
  const { markdownRed = false, warn = false } = opts;
  const n = paths.length || Number(count) || 0;
  const panel = paths.length
    ? `<div class="metric-panel">${pathListHtml(paths, labelFn, markdownRed)}</div>`
    : `<div class="metric-panel"><p class="muted-inline">None logged</p></div>`;
  return `<details class="metric metric-expandable${warn ? ' metric-warn' : ''}">
    <summary class="metric-summary">
      <dt>${tip(label, tipText)}</dt>
      <dd>${n}</dd>
    </summary>
    ${panel}
  </details>`;
}

function toolsMetricBody(e) {
  const counts = e.toolsUsedCounts && typeof e.toolsUsedCounts === 'object' ? e.toolsUsedCounts : {};
  const entries = Object.entries(counts).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  const snaps = Number(e.browserSnapshots) || 0;
  if (!entries.length && !snaps) return null;

  const paths = entries.map(([key, n]) => `${toolDisplayLabel(key)}${n > 1 ? ` × ${n}` : ''}`);
  if (snaps && !entries.some(([k]) => k.endsWith(':browser_snapshot'))) {
    paths.push(`${snaps} browser snapshot(s)`);
  }
  return { count: toolsChipCount(e), paths };
}

function effectiveConfidence(e) {
  if (e.countsTrust === 'low' || e.countsTrust === 'medium' || e.countsTrust === 'high') {
    return e.countsTrust;
  }
  const summarized = !!e.summarized;
  const bumped = e.bumped === true;
  const hook = !!e.hookTally;
  const taskChunks = Number(e.taskBumpCount) || (Array.isArray(e.taskLog) ? e.taskLog.length : 0);

  if (summarized && !bumped && !hook) return 'low';
  if (summarized && (!bumped || taskChunks < 1)) return 'low';
  if (summarized) return 'medium';
  if (!bumped && hook) return 'medium';
  if (e.bumped === false) return 'low';
  const stated = String(e.confidence || 'high').toLowerCase();
  return stated === 'low' || stated === 'medium' ? stated : 'high';
}

function trustPills(e, inProgress) {
  let html = '';
  const summarized = !!e.summarized;
  const bumped = e.bumped === true || e.agentBumped === true;
  const conf = effectiveConfidence(e);
  const missing = !!e.missingEarlyWork || !!e.preHookWorkUntracked;

  if (inProgress && missing) {
    html += pill('Missing early work — hook started late', 'p3', TIPS.preHookWorkUntracked);
  } else if (inProgress && e.hookTally && !bumped) {
    html += pill('Hook only — no task bumps yet', 'p2', TIPS.hookOnlyNoBump);
  } else if (summarized && !bumped) {
    html += pill('Counts incomplete — summarized, no bumps', 'p3', TIPS.summarizedNoBump);
  } else if (summarized || (missing && !inProgress)) {
    html += pill('Summarized — early work missing', 'p3', TIPS.summarizedEarlyMissing);
  } else if (e.bumped === false) {
    html += pill('Not bumped — counts reconstructed', 'p2', TIPS.notBumped);
  } else if (!bumped && e.hookTally) {
    html += pill('Hook only — no task bumps', 'p2', TIPS.hookOnlyNoBump);
  }

  if (conf === 'low') {
    html += pill('Low confidence counts', 'p2', TIPS.lowConfidence);
  } else if (conf === 'medium') {
    html += pill('Partial counts', 'p2', TIPS.partialConfidence);
  }

  return html;
}

function toolsChipCount(e) {
  const counts = e.toolsUsedCounts && typeof e.toolsUsedCounts === 'object' ? e.toolsUsedCounts : {};
  const uses = Object.values(counts).reduce((sum, n) => sum + n, 0);
  const snaps = Number(e.browserSnapshots) || 0;
  return uses + snaps;
}

function activityBreakdown(e, readSplit, editSplit, docsRulesList, turns, grepWarn, corrWarn, browserSnapshots) {
  const markdownRead = sortMarkdownPaths([...docsRulesList, ...readSplit.doc]);
  const codeRead = dedupePaths(readSplit.code).sort((a, b) => fileLabel(a).localeCompare(fileLabel(b)));
  const markdownEdited = sortMarkdownPaths(editSplit.doc);
  const codeEdited = dedupePaths(editSplit.code).sort((a, b) => fileLabel(a).localeCompare(fileLabel(b)));
  const tools = toolsMetricBody(e);

  const tiles = [
    staticMetric('Your messages', e.turns ?? '—', turns >= 20, TIPS.turns),
    staticMetric('Searches', e.greps ?? '—', grepWarn, TIPS.greps),
    staticMetric('You corrected me', e.corrections ?? '—', corrWarn, TIPS.corrections),
    browserSnapshots
      ? staticMetric('Browser snapshots', browserSnapshots, browserSnapshots >= 3, TIPS.browserSnapshots)
      : '',
    expandableMetric('Markdowns read', markdownRead.length, markdownRead, TIPS.docsRead, agentMarkdownLabel, { markdownRed: true }),
    expandableMetric('Code read', codeRead.length, codeRead, TIPS.codeRead, fileLabel),
    expandableMetric('Markdowns edited', markdownEdited.length, markdownEdited, TIPS.docsEdited, agentMarkdownLabel, { markdownRed: true }),
    expandableMetric('Code edited', codeEdited.length, codeEdited, TIPS.codeEdited, fileLabel),
    tools
      ? expandableMetric('Tools used', tools.count, tools.paths, TIPS.toolsUsed, (p) => p)
      : '',
  ].filter(Boolean);

  return `<div class="metric-grid metric-grid-activity">${tiles.join('')}</div>`;
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

function sessionCard(e, inProgress) {
  const greps = Number(e.greps);
  const corrections = Number(e.corrections);
  const turns = Number(e.turns);
  const grepWarn = greps >= 8;
  const corrWarn = corrections >= 3;

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

  const activityBlock = activityBreakdown(
    e, readSplit, editSplit, docsRulesList, turns, grepWarn, corrWarn, browserSnapshots,
  );

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
        ${trustPills(e, inProgress)}
        ${e.hookTally ? pill('Hook tallied', 'p1', TIPS.hookTally) : ''}
        ${inProgress ? pill('Live tally', 'p1', 'Updated after each completed task — survives summarize.') : ''}
      </div>
      <div class="model">${esc(e.model || '—')}</div>
    </header>
    <p class="summary-human">${esc(summary)}</p>
    ${activityBlock}
    ${e.redFlags ? `<p class="red-flags"><strong>Red flags:</strong> ${esc(e.redFlags)}</p>` : ''}
    ${worthNoting}${captureBlock}
    ${e.nextSession ? `<p class="next"><strong>Next time:</strong> ${esc(e.nextSession)}</p>` : ''}
  </article>`;
}

module.exports = {
  TIPS,
  esc,
  tip,
  dayKey,
  timeShort,
  sessionCard,
};
