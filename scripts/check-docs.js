/**
 * FILE: scripts/check-docs.js
 * PURPOSE: Health check for the instruction layer (AGENTS.md / CLAUDE.md /
 *          .cursor/rules/*.mdc / cursor-patterns/ / per-app docs).
 *
 * Catches the four ways this system decayed historically:
 *   1. DEAD LINK      — a relative link that resolves to nothing
 *   2. ORPHAN         — a doc no other doc links to (functionally deleted)
 *   3. DUPLICATE      — byte-identical copies in two places (two sources of truth)
 *   4. UNINDEXED RULE — an .mdc not named by any CLAUDE.md / AGENTS.md
 *                       (invisible to Claude Code, which does not auto-load .mdc)
 *   5. BARE VALUE     — a rule/entry point restating a timing constant's value
 *                       instead of naming it (AGENTS.md § One content home)
 *
 * Usage:
 *   node scripts/check-docs.js            # report (exit 0 unless dead links)
 *   node scripts/check-docs.js --strict   # exit 1 on any finding
 *   node scripts/check-docs.js --quiet    # only show counts
 *
 * Advisory by default: orphans and duplicates are judgment calls, dead links are not.
 */

'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const strict = process.argv.includes('--strict');
const quiet = process.argv.includes('--quiet');

const IGNORED_DIRS = new Set([
  'node_modules', '.git', 'dist', 'build', 'out', '__pycache__', '.vite',
  'archive', 'Archived markdowns', 'Deprecated apps', 'python-runtime',
  'logs', '.husky', 'dist-installer', 'test-results', 'backups',
  'calendar-vendor', 'assignment-assistant-engine', '.ci-test-venv', 'reports',
  // Ephemeral / tool-generated / vendored — not part of the instruction layer
  'plans', '.pytest_cache', 'DisplayProfileManager-main', 'coverage',
  'playwright-report', 'simulator', 'test-fixtures', 'node_modules_old',
  'animation-library', 'my-calendar', 'sog-world-viewer', 'canvas-vendor',
  'venv', 'site-packages', '.venv', 'Lib', 'python', 'heros-hour-umt-export',
]);

// Generated or vendored filenames that are never instruction-layer docs.
const IGNORED_BASENAMES = new Set([
  'ATTRIBUTIONS.md', 'Attributions.md', 'App.tsx.README.md', 'LICENSE.md',
  'CHANGELOG.md', 'CODE_OF_CONDUCT.md', 'CONTRIBUTING.md',
]);

// Docs that are entry points by definition — never reported as orphans.
const ENTRY_POINTS = new Set([
  'AGENTS.md', 'CLAUDE.md', 'README.md', 'APP_LOCATIONS.md',
  'HOW_TO_INTERACT_WITH_AI.md', 'FROZEN.md', 'SESSIONS.md', 'Guidelines.md',
]);

function walk(dir, out = []) {
  let entries;
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return out; }
  for (const e of entries) {
    if (IGNORED_DIRS.has(e.name)) continue;
    const full = path.join(dir, e.name);
    if (e.isDirectory()) walk(full, out);
    else if (/\.(md|mdc)$/.test(e.name) && !IGNORED_BASENAMES.has(e.name)) out.push(full);
  }
  return out;
}

const files = walk(ROOT);
const rel = (f) => path.relative(ROOT, f).split(path.sep).join('/');

// ---------- gather ----------
const content = new Map();   // relpath -> text
const linkedTo = new Set();  // relpaths that something links to
const byHash = new Map();    // size+firstline -> [relpath]
const deadLinks = [];

for (const f of files) {
  let text;
  try { text = fs.readFileSync(f, 'utf8'); } catch { continue; }
  content.set(rel(f), text);
}

// Markdown links + bare backticked paths that look like docs
const LINK_RE = /\[[^\]]*\]\(([^)#]+?)(?:#[^)]*)?\)/g;
const CODE_PATH_RE = /`([^`\n]*?\.(?:md|mdc))`/g;

// Links inside fenced code blocks are examples, not references.
function stripCodeFences(text) {
  return text.replace(/```[\s\S]*?```/g, '').replace(/^ {4,}\S.*$/gm, '');
}

for (const [r, rawText] of content) {
  const text = stripCodeFences(rawText);
  const dir = path.dirname(path.join(ROOT, r));

  const check = (raw, kind) => {
    let target = decodeURIComponent(raw.trim());
    if (/^(https?:|mailto:|#)/.test(target)) return;
    target = target.replace(/\\/g, '/');
    // Absolute Windows path -> make relative to ROOT if inside
    let abs;
    if (/^[A-Za-z]:\//.test(target)) abs = target;
    else if (target.startsWith('/')) return; // site-absolute, skip
    else abs = path.resolve(dir, target);

    if (fs.existsSync(abs)) {
      const t = path.relative(ROOT, abs).split(path.sep).join('/');
      if (!t.startsWith('..')) linkedTo.add(t);
    } else if (kind === 'link') {
      // Only markdown links are reported dead; backticked paths are often prose
      deadLinks.push({ from: r, target: raw.trim() });
    }
  };

  let m;
  while ((m = LINK_RE.exec(text))) check(m[1], 'link');
  while ((m = CODE_PATH_RE.exec(text))) check(m[1], 'code');
}

// ---------- duplicates ----------
for (const [r, text] of content) {
  const key = `${text.length}:${text.slice(0, 120)}`;
  if (!byHash.has(key)) byHash.set(key, []);
  byHash.get(key).push(r);
}
const duplicates = [...byHash.values()].filter((g) => g.length > 1);

// ---------- orphans ----------
const orphans = [...content.keys()].filter((r) => {
  const base = path.basename(r);
  if (ENTRY_POINTS.has(base)) return false;
  if (linkedTo.has(r)) return false;
  // A rule referenced by bare filename in an index counts as linked
  const named = [...content.values()].some((t) => t.includes(base) );
  return !named;
});

// ---------- unindexed .mdc ----------
const indexes = [...content.entries()]
  .filter(([r]) => /(^|\/)(CLAUDE|AGENTS)\.md$/.test(r))
  .map(([, t]) => t)
  .join('\n');
const unindexedRules = [...content.keys()]
  .filter((r) => r.endsWith('.mdc'))
  .filter((r) => !indexes.includes(path.basename(r)));

// ---------- bare timing values in rules / entry points ----------
// AGENTS.md § "One content home, many pointers": a rule or entry point names the
// constant; it never restates the constant's value. Durations are what drift —
// this check exists because one dwell timing had been copied into six files.
//
// Only `.mdc`, AGENTS.md and CLAUDE.md are scanned. A topic's source-of-truth
// doc under cursor-patterns/ IS allowed to hold values — that is its whole job.
// Visual px specs are deliberately NOT flagged: for a design contract the .mdc
// is the single home, so a border width there is not a duplicate.
const VALUE_FILE_RE = /(\.mdc$)|((^|\/)(AGENTS|CLAUDE)\.md$)/;
const MS_RE = /\b\d{2,6}\s?ms\b/gi;

// Blank fenced code (keeping line numbers) — a value inside an example is fine.
function blankCodeFences(text) {
  let inFence = false;
  return text.split('\n').map((ln) => {
    if (/^\s*```/.test(ln)) { inFence = !inFence; return ''; }
    return inFence ? '' : ln;
  }).join('\n');
}

// Escape hatch: some durations ARE the content (e.g. "wait ~2s after navigation"
// — procedural advice with no constant to name). Mark those lines:
//     ... 2000 ms ...  <!-- value-ok: procedural wait, no constant exists -->
const VALUE_OK_RE = /<!--\s*value-ok/i;

const bareValues = [];
for (const [r, rawText] of content) {
  if (!VALUE_FILE_RE.test(r)) continue;
  if (r.includes('Calendar 2.0')) continue; // frozen — flagging it is noise
  blankCodeFences(rawText).split('\n').forEach((ln, i) => {
    if (VALUE_OK_RE.test(ln)) return;
    const hits = ln.match(MS_RE);
    if (hits) bareValues.push({ file: r, line: i + 1, hits: [...new Set(hits)].join(', ') });
  });
}

// ---------- report ----------
const line = (s) => { if (!quiet) console.log(s); };

line(`\n📚 Instruction-layer health — ${content.size} docs scanned\n`);

if (deadLinks.length) {
  line(`❌ DEAD LINKS (${deadLinks.length}) — these resolve to nothing:`);
  for (const d of deadLinks.slice(0, 40)) line(`   ${d.from}  →  ${d.target}`);
  if (deadLinks.length > 40) line(`   …and ${deadLinks.length - 40} more`);
  line('');
} else line('✅ No dead links\n');

if (duplicates.length) {
  line(`⚠️  DUPLICATES (${duplicates.length}) — same content in two places:`);
  for (const g of duplicates.slice(0, 20)) line(`   ${g.join('\n   = ')}\n`);
} else line('✅ No duplicate docs\n');

if (unindexedRules.length) {
  line(`⚠️  UNINDEXED RULES (${unindexedRules.length}) — invisible to Claude Code:`);
  for (const r of unindexedRules) line(`   ${r}`);
  line('   → add a row to the owning CLAUDE.md rules table\n');
} else line('✅ Every .mdc rule is indexed\n');

if (bareValues.length) {
  line(`⚠️  BARE VALUES (${bareValues.length}) — a rule restating a constant's value:`);
  for (const b of bareValues.slice(0, 25)) line(`   ${b.file}:${b.line}  →  ${b.hits}`);
  if (bareValues.length > 25) line(`   …and ${bareValues.length - 25} more`);
  line('   → name the constant instead; values live in code or the topic doc\n');
} else line('✅ No bare timing values in rules or entry points\n');

if (orphans.length) {
  line(`⚠️  ORPHANS (${orphans.length}) — nothing references these:`);
  for (const o of orphans.slice(0, 30)) line(`   ${o}`);
  if (orphans.length > 30) line(`   …and ${orphans.length - 30} more`);
  line('   → link them from an index, or tombstone them\n');
} else line('✅ No orphaned docs\n');

console.log(
  `Summary: ${deadLinks.length} dead links · ${duplicates.length} duplicate sets · ` +
  `${unindexedRules.length} unindexed rules · ${bareValues.length} bare values · ` +
  `${orphans.length} orphans`
);

const fail = deadLinks.length > 0
  || (strict && (duplicates.length || orphans.length || unindexedRules.length || bareValues.length));
process.exit(fail ? 1 : 0);
