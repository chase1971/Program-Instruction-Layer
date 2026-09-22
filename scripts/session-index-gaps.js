/**
 * FILE: scripts/session-index-gaps.js
 * PURPOSE: Index gaps — docs that should have routed the agent to the answer but did not,
 *          so it had to grep the tree. The one navigation signal kept from the old
 *          step-by-step navigationPath (trimmed 2026-09-21: 85% of self-graded steps were
 *          "helpful" and 93% of tasks said step 1 helped, so the full path carried no signal).
 *
 *          Bump shape: "indexGaps": [{ "doc": "agent docs/INDEX.md", "note": "no row for X" }]
 *          or the CLI: --gap "agent docs/INDEX.md: no row for X"
 */
'use strict';

const GAP_KEYS = new Set(['doc', 'note']);
const LEGACY_DOC_KINDS = new Set(['doc', 'doc-index']);
const LEGACY_FAIL = new Set(['partial', 'dead-end']);

// "path: why" → { doc, note }. Splits on the first ": " so Windows drive letters survive.
function parseGapArg(raw) {
  const s = String(raw || '').trim();
  const at = s.indexOf(': ');
  if (at === -1) return { doc: s, note: '' };
  return { doc: s.slice(0, at).trim(), note: s.slice(at + 2).trim() };
}

function validateIndexGaps(list) {
  if (list === undefined) return [];
  if (!Array.isArray(list)) return ['indexGaps must be an array of { doc, note }'];
  const problems = [];
  list.forEach((raw, i) => {
    const at = `indexGaps[${i}]`;
    if (typeof raw === 'string') return;
    if (!raw || typeof raw !== 'object') {
      problems.push(`${at} must be an object or a "doc: note" string`);
      return;
    }
    for (const key of Object.keys(raw)) {
      if (!GAP_KEYS.has(key)) problems.push(`${at} has unknown key "${key}" — use doc and note`);
    }
    if (!String(raw.doc || '').trim()) problems.push(`${at} needs a "doc"`);
  });
  return problems;
}

function normalizeIndexGaps(list) {
  if (!Array.isArray(list)) return [];
  return list
    .map((g) => (typeof g === 'string' ? parseGapArg(g) : {
      doc: String(g && g.doc || '').trim(),
      note: String(g && g.note || '').trim(),
    }))
    .filter((g) => g.doc);
}

// Old bumps (and agents still sending navigationPath) — keep only the doc steps that failed.
function gapsFromLegacyPath(steps) {
  const out = [];
  for (const s of steps || []) {
    if (!s || typeof s !== 'object') continue;
    const kind = String(s.kind || '').toLowerCase();
    if (LEGACY_DOC_KINDS.has(kind) && LEGACY_FAIL.has(String(s.outcome || '').toLowerCase())) {
      const doc = String(s.target || s.path || s.label || '').trim();
      if (doc) out.push({ doc, note: String(s.note || '').trim() });
    }
    if (Array.isArray(s.steps)) out.push(...gapsFromLegacyPath(s.steps));
  }
  return out;
}

function entryGaps(entry) {
  if (Array.isArray(entry.indexGaps)) return normalizeIndexGaps(entry.indexGaps);
  return gapsFromLegacyPath(entry.navigationPath);
}

function collectIndexGaps(entries, limit = 25) {
  const out = [];
  const sorted = [...(entries || [])].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  for (const entry of sorted) {
    for (const gap of entryGaps(entry)) {
      out.push({ ...gap, timestamp: entry.timestamp, chunkNote: entry.chunkNote });
      if (out.length >= limit) return out;
    }
  }
  return out;
}

// Which docs fail most often, across the whole log — the to-do list worth acting on.
function gapCountsByDoc(entries) {
  const counts = new Map();
  for (const entry of entries || []) {
    for (const gap of entryGaps(entry)) counts.set(gap.doc, (counts.get(gap.doc) || 0) + 1);
  }
  return [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
}

module.exports = {
  parseGapArg,
  validateIndexGaps,
  normalizeIndexGaps,
  gapsFromLegacyPath,
  entryGaps,
  collectIndexGaps,
  gapCountsByDoc,
};
