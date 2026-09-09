/**
 * FILE: scripts/build-doc-index.js
 * PURPOSE: Regenerate agent docs/index.html — the front door served at
 *          127.0.0.1:8765 — by scanning the served roots and merging
 *          agent docs/page-manifest.json for grouping and descriptions.
 *
 * Anything not matched by a manifest group lands in "Unsorted", so a new page
 * can never silently go missing. Add it to the manifest to file it properly.
 *
 * Usage: node scripts/build-doc-index.js
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { renderIndexHtml } = require('./doc-index-html');

const ROOT = path.resolve(__dirname, '..');
const MANIFEST = path.join(ROOT, 'agent docs', 'page-manifest.json');
const OUT = path.join(ROOT, 'agent docs', 'index.html');

// Mirrors SERVE_ROOTS in serve-programs-docs.js. School documents wins ties,
// which is why it is scanned first.
const SERVE_ROOTS = [
  path.join(ROOT, 'School Scrips', 'School documents'),
  path.join(ROOT, 'agent docs'),
];

const SKIP_DIRS = new Set(['node_modules', '.git']);

function scanRoot(root) {
  const found = [];
  if (!fs.existsSync(root)) return found;
  const walk = (dir) => {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      if (e.isDirectory()) {
        if (!SKIP_DIRS.has(e.name)) walk(path.join(dir, e.name));
        continue;
      }
      if (!e.name.endsWith('.html')) continue;
      const rel = path.relative(root, path.join(dir, e.name)).split(path.sep).join('/');
      if (rel === 'index.html') continue;
      found.push({ rel, abs: path.join(dir, e.name) });
    }
  };
  walk(root);
  return found;
}

function readTitle(abs) {
  try {
    const head = fs.readFileSync(abs, 'utf8').slice(0, 4000);
    const m = head.match(/<title>([\s\S]*?)<\/title>/i);
    if (!m) return null;
    return m[1].replace(/\s+/g, ' ').replace(/&amp;/g, '&').trim() || null;
  } catch {
    return null;
  }
}

function collectPages() {
  const seen = new Set();
  const pages = [];
  for (const root of SERVE_ROOTS) {
    for (const { rel, abs } of scanRoot(root)) {
      if (seen.has(rel)) continue; // first root wins, same as the server
      seen.add(rel);
      let mtime = null;
      try {
        mtime = fs.statSync(abs).mtime.toISOString().slice(0, 10);
      } catch { /* ignore */ }
      pages.push({ href: rel, title: readTitle(abs) || rel, mtime });
    }
  }
  return pages;
}

function matcher(pattern) {
  if (pattern.startsWith('^')) {
    const re = new RegExp(pattern);
    return (href) => re.test(href);
  }
  return (href) => href === pattern;
}

function groupPages(pages, manifest) {
  const remaining = new Map(pages.map((p) => [p.href, p]));
  const groups = [];

  for (const g of manifest.groups) {
    const tests = (g.match || []).map(matcher);
    const collapse = (g.collapsePatterns || []).map(matcher);
    const items = [];
    const collapsed = [];

    // Preserve manifest order for exact-path entries, so the important page
    // stays at the top of its group rather than sorting alphabetically.
    for (const pattern of g.match || []) {
      const test = matcher(pattern);
      for (const [href, page] of [...remaining]) {
        if (!test(href)) continue;
        remaining.delete(href);
        const isCollapsed = collapse.some((c) => c(href));
        (isCollapsed ? collapsed : items).push(page);
      }
    }
    void tests;

    if (items.length || collapsed.length) {
      groups.push({ ...g, items, collapsed });
    }
  }

  const leftovers = [...remaining.values()].sort((a, b) => a.href.localeCompare(b.href));
  if (leftovers.length) {
    groups.push({
      id: 'unsorted',
      title: 'Unsorted',
      blurb: 'Not yet filed in agent docs/page-manifest.json. Add a match entry to move it into a group.',
      accent: 'amber',
      open: true,
      items: leftovers,
      collapsed: [],
    });
  }
  return groups;
}

function main() {
  const manifest = JSON.parse(fs.readFileSync(MANIFEST, 'utf8'));
  const pages = collectPages();
  const groups = groupPages(pages, manifest);

  for (const g of groups) {
    for (const item of [...g.items, ...g.collapsed]) {
      item.desc = manifest.descriptions[item.href] || null;
    }
  }

  fs.writeFileSync(OUT, renderIndexHtml(groups, pages.length), 'utf8');
  const filed = groups.reduce((a, g) => a + g.items.length + g.collapsed.length, 0);
  const unsorted = (groups.find((g) => g.id === 'unsorted') || { items: [] }).items.length;
  process.stdout.write(`Index rebuilt — ${filed} pages in ${groups.length} groups`
    + `${unsorted ? `, ${unsorted} unsorted` : ''}.\n`);
  process.stdout.write('View: http://127.0.0.1:8765/\n');
}

if (require.main === module) main();

module.exports = { collectPages, groupPages };
