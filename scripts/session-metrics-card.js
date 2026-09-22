/**
 * FILE: scripts/session-metrics-card.js
 * PURPOSE: One session card on session-metrics-log.html — summary, cost, task list,
 *          and the agent's end-of-session notes — plus the small HTML helpers the page shares.
 *
 * 2026-09-21: dropped search counts, file lists, tool counts and count-trust pills.
 * Cost (tokens, or chat size in Cursor) replaced them as the efficiency number.
 */
'use strict';

const { formatTokens } = require('./session-token-cost');

const TIPS = {
  turns: 'How many messages you sent in this session.',
  tokens: 'Tokens billed across the session\'s logged tasks (Claude Code only — Cursor records none). Mostly cache re-reads, so it grows with session length.',
  peakContext: 'The most context one reply re-read. Above ~250k, a fresh task via momentum handoff is cheaper.',
  tasks: 'Task bumps logged this session.',
  corrections: 'Times you pushed back: "no", "wrong", "again". High means the agent drifted or misunderstood.',
  sessionType: 'Category for comparing similar sessions: coding, Q&A, mixed, etc.',
  outcome: 'Done = finished the goal. Partial = some progress. Abandoned = stopped early.',
  notBumped: 'No task bumps were logged during this session, so the task list is missing.',
  summarized: 'The chat was compressed mid-session; early detail may be missing from the notes.',
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

function tip(label, tipText) {
  return `<abbr class="tip" title="${esc(tipText)}">${esc(label)}</abbr>`;
}

function pill(text, cls, tipText) {
  const t = tipText ? ` title="${esc(tipText)}"` : '';
  return `<span class="pill ${cls}"${t}>${esc(text)}</span>`;
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

function metric(label, value, warn, tipText) {
  return `<div class="metric${warn ? ' metric-warn' : ''}">
    <dt>${tip(label, tipText)}</dt>
    <dd>${esc(String(value ?? '—'))}</dd>
  </div>`;
}

function outcomeClass(o) {
  const x = String(o || '').toLowerCase();
  if (x === 'done') return 'p1';
  if (x === 'partial') return 'p2';
  if (x === 'abandoned') return 'p3';
  return 'p0';
}

function outcomeLabel(o) {
  const map = { done: 'Finished', partial: 'Partly done', abandoned: 'Stopped early' };
  return map[String(o || '').toLowerCase()] || o || '—';
}

function costTile(e) {
  if (Number.isFinite(e.billedTokens)) return metric('Tokens', formatTokens(e.billedTokens), false, TIPS.tokens);
  if (Number.isFinite(e.chatUserMessages)) {
    return metric('Chat messages', e.chatUserMessages, e.chatUserMessages >= 30, TIPS.turns);
  }
  return metric('Tokens', '—', false, TIPS.tokens);
}

function taskListHtml(e) {
  const tasks = Array.isArray(e.taskLog) ? e.taskLog : [];
  if (!tasks.length) return '';
  return `<details class="file-details"><summary>${tasks.length} task(s)</summary>
    <ul class="task-list">${tasks.map((t) => `<li>${esc(timeShort(t.time))} — ${esc(t.note || '')}</li>`).join('')}</ul>
  </details>`;
}

function sessionCard(e, inProgress) {
  const turns = Number(e.turns);
  const corrections = Number(e.corrections);
  const taskCount = Number(e.taskBumpCount) || (Array.isArray(e.taskLog) ? e.taskLog.length : 0);
  const peak = Number(e.peakTokensPerTurn);

  const tiles = [
    metric('Your messages', e.turns ?? '—', turns >= 30, TIPS.turns),
    costTile(e),
    Number.isFinite(peak) ? metric('Peak context/turn', formatTokens(peak), peak >= 250000, TIPS.peakContext) : '',
    metric('Tasks logged', taskCount, false, TIPS.tasks),
    metric('You corrected me', e.corrections ?? '—', corrections >= 3, TIPS.corrections),
  ].filter(Boolean);

  const outPill = inProgress
    ? pill('In progress', 'p0', 'Updates after each completed task.')
    : pill(outcomeLabel(e.outcome), outcomeClass(e.outcome), TIPS.outcome);
  const flags = [
    !inProgress && e.bumped === false ? pill('No task bumps', 'p2', TIPS.notBumped) : '',
    e.summarized ? pill('Summarized', 'p2', TIPS.summarized) : '',
  ].join('');

  const worthNoting = e.worthNoting || e.spike
    ? `<div class="note-box"><strong>${tip('Worth noting', TIPS.worthNoting)}:</strong> ${esc(e.worthNoting || e.spike)}</div>`
    : '';
  const capture = e.captureCandidate
    ? `<div class="capture-box"><strong>${tip('Agent suggests capturing', TIPS.captureSuggest)}:</strong> ${esc(e.captureCandidate)}</div>`
    : '';

  return `<article class="${inProgress ? 'session-card in-progress' : 'session-card'}">
    <header class="session-head">
      <div class="pills">
        <span class="time">${esc(timeShort(e.timestamp))}</span>
        ${pill(e.sessionType || 'mixed', 'p0', TIPS.sessionType)}${outPill}${flags}
      </div>
      <div class="model">${esc(e.model || '—')}</div>
    </header>
    <p class="summary-human">${esc(e.summaryHuman || e.goal || '—')}</p>
    <div class="metric-grid">${tiles.join('')}</div>
    ${taskListHtml(e)}
    ${worthNoting}${capture}
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
