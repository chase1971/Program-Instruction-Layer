/**
 * FILE: scripts/scorecard-navigation-path.js
 * PURPOSE: Merge and render agent doc-navigation paths on session scorecards.
 *          Agents log ordered steps (and sub-agent branches) in bump JSON as navigationPath.
 */
'use strict';

const path = require('path');

// 'routed' = the doc did its job by sending you onward, or by confirming no narrower owner
// exists. Renders like partial but is NOT an index gap — see collectIndexFailures().
const NAV_OUTCOMES = new Set(['helpful', 'dead-end', 'partial', 'routed']);

const NAV_TIP =
  'Order the agent looked things up — docs, greps, code. ✓ helped, → routed onward, '
  + '~ partial, ✗ dead end. '
  + 'Use this to see whether INDEX.md and app AGENTS.md are creating short routes.';

function normalizeOutcome(raw) {
  const v = String(raw || 'helpful').toLowerCase().trim();
  return NAV_OUTCOMES.has(v) ? v : 'helpful';
}

function normalizeStep(raw, index) {
  if (!raw || typeof raw !== 'object') return null;
  let target = String(raw.target || raw.path || raw.label || '').trim();
  if (!target && raw.step) target = String(raw.step).trim();
  if (!target) return null;

  let outcome = raw.outcome;
  if (!outcome && raw.result) {
    const r = String(raw.result).trim();
    if (r === '✓' || r.toLowerCase() === 'ok') outcome = 'helpful';
    else if (r === '✗' || r.toLowerCase() === 'x') outcome = 'dead-end';
    else if (r === '~') outcome = 'partial';
    else if (r === '→' || r === '->') outcome = 'routed';
  }

  const step = {
    target,
    kind: String(raw.kind || 'other').trim() || 'other',
    outcome: normalizeOutcome(outcome),
    note: String(raw.note || '').trim(),
  };
  if (Number.isFinite(raw.step)) step.step = raw.step;
  else step.step = index + 1;
  if (raw.branch) step.branch = String(raw.branch).trim();
  if (Array.isArray(raw.steps) && raw.steps.length) {
    step.steps = normalizeNavigationPath(raw.steps);
  }
  return step;
}

function normalizeNavigationPath(list) {
  if (!Array.isArray(list)) return [];
  return list.map((item, i) => normalizeStep(item, i)).filter(Boolean);
}

function mergeNavigationPaths(existing, incoming) {
  const base = normalizeNavigationPath(existing);
  const add = normalizeNavigationPath(incoming);
  if (!add.length) return base;
  return [...base, ...add];
}

function outcomeIcon(outcome) {
  if (outcome === 'dead-end') return '✗';
  if (outcome === 'partial') return '~';
  if (outcome === 'routed') return '→';
  return '✓';
}

function outcomeClass(outcome) {
  if (outcome === 'dead-end') return 'nav-dead';
  if (outcome === 'partial') return 'nav-partial';
  if (outcome === 'routed') return 'nav-routed';
  return 'nav-helpful';
}

function navTargetLabel(target, kind) {
  const t = String(target || '');
  if (kind === 'grep' && !t.toLowerCase().startsWith('grep')) return `Grep: ${t}`;
  if (kind === 'glob' && !t.toLowerCase().startsWith('glob')) return `Glob: ${t}`;
  if (kind === 'task' && !t.toLowerCase().startsWith('task')) return `Task: ${t}`;
  if (kind === 'web' && !t.toLowerCase().startsWith('web')) return `Web: ${t}`;
  if (kind === 'doc-index') return t.includes('INDEX') ? t : `INDEX → ${t}`;
  return path.basename(t.replace(/\\/g, '/')) !== t ? t : t;
}

function renderNavSteps(steps, depth = 0) {
  if (!steps.length) return '';
  const items = steps.map((s) => {
    const icon = outcomeIcon(s.outcome);
    const cls = outcomeClass(s.outcome);
    const label = navTargetLabel(s.target, s.kind);
    const branch = s.branch
      ? `<span class="nav-branch" title="Parallel branch">${escapeHtml(s.branch)}</span>`
      : '';
    const note = s.note ? `<span class="nav-note">${escapeHtml(s.note)}</span>` : '';
    const nested = s.steps?.length
      ? `<ul class="nav-tree nav-nested">${renderNavSteps(s.steps, depth + 1)}</ul>`
      : '';
    return `<li class="nav-step ${cls}" style="--nav-depth:${depth}">
      <span class="nav-marker" title="${escapeHtml(s.outcome)}">${icon}</span>
      <span class="nav-step-num">${s.step ?? '·'}</span>
      ${branch}
      <code class="nav-target" title="${escapeHtml(s.target)}">${escapeHtml(label)}</code>
      ${note}
      ${nested}
    </li>`;
  });
  return items.join('');
}

function escapeHtml(s) {
  return String(s ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function navigationPathHtml(steps, tipText = NAV_TIP) {
  const normalized = normalizeNavigationPath(steps);
  if (!normalized.length) return '';

  const helpful = countOutcomes(normalized, 'helpful');
  const dead = countOutcomes(normalized, 'dead-end');
  const partial = countOutcomes(normalized, 'partial');
  const routed = countOutcomes(normalized, 'routed');
  const summary = `${normalized.length} step(s) — ${helpful} helpful, ${routed} routed, `
    + `${partial} partial, ${dead} dead-end`;

  return `<details class="nav-path-block">
    <summary><abbr class="tip" title="${escapeHtml(tipText)}">Doc navigation path</abbr>
      <span class="nav-path-summary">${escapeHtml(summary)}</span>
    </summary>
    <p class="muted-inline nav-legend">
      <span class="nav-helpful-pill">✓ helpful</span>
      <span class="nav-routed-pill">→ routed onward</span>
      <span class="nav-partial-pill">~ partial</span>
      <span class="nav-dead-pill">✗ dead end</span>
      — order the agent looked; nested lists are sub-agent branches.
    </p>
    <ul class="nav-tree nav-root">${renderNavSteps(normalized)}</ul>
  </details>`;
}

function countOutcomes(steps, outcome) {
  let n = 0;
  for (const s of steps || []) {
    if (s.outcome === outcome) n += 1;
    if (s.steps?.length) n += countOutcomes(s.steps, outcome);
  }
  return n;
}

function flattenSteps(steps) {
  const flat = [];
  for (const s of steps || []) {
    flat.push(s);
    if (s.steps?.length) flat.push(...flattenSteps(s.steps));
  }
  return flat;
}

function summarizeNavigationPath(steps) {
  const normalized = normalizeNavigationPath(steps);
  const flat = flattenSteps(normalized);
  let stepsToFirstHelpful = 0;
  for (let i = 0; i < flat.length; i += 1) {
    if (flat[i].outcome === 'helpful' || flat[i].outcome === 'routed') {
      stepsToFirstHelpful = i + 1;
      break;
    }
  }
  return {
    stepCount: flat.length,
    stepsToFirstHelpful: stepsToFirstHelpful || (flat.length ? flat.length : 0),
    helpfulCount: countOutcomes(normalized, 'helpful'),
    partialCount: countOutcomes(normalized, 'partial'),
    routedCount: countOutcomes(normalized, 'routed'),
    deadEndCount: countOutcomes(normalized, 'dead-end'),
  };
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

function navigationPathStyles() {
  return `
    .nav-path-block { background: #151c26; border: 1px solid var(--border); border-radius: 10px; padding: 0.55rem 0.75rem; margin: 0.65rem 0 0.35rem; }
    .nav-path-block summary { cursor: pointer; min-height: 44px; display: flex; align-items: center; flex-wrap: wrap; gap: 0.5rem; font-weight: 600; list-style: none; }
    .nav-path-block summary::-webkit-details-marker { display: none; }
    .nav-path-summary { font-weight: 400; color: var(--muted); font-size: 0.88rem; }
    .nav-legend { margin: 0.35rem 0 0.5rem; font-size: 0.82rem; display: flex; flex-wrap: wrap; gap: 0.65rem; align-items: center; }
    .nav-helpful-pill, .nav-routed-pill, .nav-partial-pill, .nav-dead-pill { font-size: 0.78rem; padding: 0.1rem 0.4rem; border-radius: 6px; }
    .nav-routed-pill { background: #1e3350; color: var(--accent); }
    .nav-helpful-pill { background: #264032; color: var(--accent2); }
    .nav-partial-pill { background: #4a3818; color: var(--warn); }
    .nav-dead-pill { background: #3d2020; color: var(--danger); }
    .nav-tree { margin: 0; padding: 0; list-style: none; }
    .nav-root { padding-left: 0; }
    .nav-nested { margin: 0.25rem 0 0.15rem 1.35rem; padding-left: 0.5rem; border-left: 2px solid rgba(94, 184, 255, 0.25); }
    .nav-step { display: flex; flex-wrap: wrap; align-items: baseline; gap: 0.35rem; margin: 0.35rem 0; font-size: 0.88rem; min-height: 1.4rem; }
    .nav-marker { font-weight: 800; width: 1.1rem; text-align: center; flex-shrink: 0; }
    .nav-step.nav-helpful .nav-marker { color: var(--accent2); }
    .nav-step.nav-partial .nav-marker { color: var(--warn); }
    .nav-step.nav-routed .nav-marker { color: var(--accent); }
    .nav-step.nav-dead .nav-marker { color: var(--danger); }
    .nav-step-num { color: var(--muted); font-size: 0.75rem; min-width: 1.1rem; }
    .nav-branch { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.04em; color: var(--accent); background: #1e3350; padding: 0.1rem 0.35rem; border-radius: 4px; }
    .nav-target { font-family: Consolas, "Courier New", monospace; font-size: 0.84rem; color: var(--text); word-break: break-word; }
    .nav-note { color: var(--muted); font-size: 0.82rem; flex-basis: 100%; padding-left: 2.5rem; }
    .nav-step .nav-tree { flex-basis: 100%; }
  `;
}

module.exports = {
  NAV_TIP,
  normalizeNavigationPath,
  mergeNavigationPaths,
  summarizeNavigationPath,
  flattenSteps,
  formatDurationMs,
  navigationPathHtml,
  navigationPathStyles,
  renderNavSteps,
  escapeHtml,
  outcomeIcon,
  outcomeClass,
  navTargetLabel,
};
