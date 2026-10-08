'use strict';

const fs = require('fs');
const path = require('path');

const PROGRAMS_ROOT = path.join(__dirname, '..');
const REGISTRY_PATH = path.join(PROGRAMS_ROOT, 'agent docs', 'sync-pull-registry.json');

function normalizeRepoPath(rel) {
  return rel.replace(/\\/g, '/');
}

/** All git repo roots under Programs (includes `.` for root). */
function listGitReposOnDisk() {
  const repos = new Set();
  if (fs.existsSync(path.join(PROGRAMS_ROOT, '.git'))) {
    repos.add('.');
  }
  (function walk(dir) {
    let ents;
    try {
      ents = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      return;
    }
    for (const e of ents) {
      if (e.name === 'node_modules') continue;
      const p = path.join(dir, e.name);
      if (!e.isDirectory()) continue;
      if (fs.existsSync(path.join(p, '.git'))) {
        repos.add(normalizeRepoPath(path.relative(PROGRAMS_ROOT, p)));
        continue;
      }
      walk(p);
    }
  })(PROGRAMS_ROOT);
  return [...repos].sort((a, b) => a.localeCompare(b));
}

function defaultPullForPath(repoPath) {
  const p = normalizeRepoPath(repoPath);
  if (p === 'School Scrips/Calendar 2.0' || p === 'School Scripts/Calendar 2.0') return false;
  if (p.startsWith('Deprecated apps/')) return false;
  return true;
}

function labelForPath(repoPath) {
  if (repoPath === '.') return 'Programs root — Manim, agent docs, session tracking';
  const base = repoPath.split('/').pop();
  return base;
}

function groupForPath(repoPath) {
  const p = normalizeRepoPath(repoPath);
  if (p === '.') return 'core';
  if (p.startsWith('Deprecated apps/')) return 'deprecated';
  if (p.startsWith('School Scrips/') || p.startsWith('School Scripts/')) return 'school';
  if (['electron-toolbar', 'Video Player', 'Agent Browser'].includes(p)) return 'toolbar';
  return 'other';
}

function loadRegistry() {
  if (!fs.existsSync(REGISTRY_PATH)) {
    return { version: 1, updated: null, repos: [] };
  }
  return JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf8'));
}

function saveRegistry(registry) {
  registry.updated = new Date().toISOString();
  fs.writeFileSync(REGISTRY_PATH, JSON.stringify(registry, null, 2) + '\n', 'utf8');
}

/** Add new disk repos; preserve existing pull flags. */
function refreshRegistryFromDisk() {
  const onDisk = listGitReposOnDisk();
  const registry = loadRegistry();
  const byPath = new Map(registry.repos.map((r) => [normalizeRepoPath(r.path), r]));

  for (const repoPath of onDisk) {
    if (!byPath.has(repoPath)) {
      byPath.set(repoPath, {
        path: repoPath,
        label: labelForPath(repoPath),
        group: groupForPath(repoPath),
        pull: defaultPullForPath(repoPath),
      });
    }
  }

  registry.repos = onDisk.map((p) => {
    const existing = byPath.get(p);
    return {
      path: p,
      label: existing.label || labelForPath(p),
      group: existing.group || groupForPath(p),
      pull: typeof existing.pull === 'boolean' ? existing.pull : defaultPullForPath(p),
    };
  });
  saveRegistry(registry);
  return registry;
}

/** Repos agents may touch on pull / full sync unless Chase names one explicitly. */
function getDefaultPullPaths() {
  const registry = loadRegistry();
  return registry.repos.filter((r) => r.pull).map((r) => normalizeRepoPath(r.path));
}

function resolveRepoPathToAbsolute(repoPath) {
  const p = normalizeRepoPath(repoPath);
  if (p === '.') return PROGRAMS_ROOT;
  return path.join(PROGRAMS_ROOT, p);
}

module.exports = {
  REGISTRY_PATH,
  PROGRAMS_ROOT,
  listGitReposOnDisk,
  loadRegistry,
  saveRegistry,
  refreshRegistryFromDisk,
  getDefaultPullPaths,
  resolveRepoPathToAbsolute,
  normalizeRepoPath,
  defaultPullForPath,
};

if (require.main === module) {
  const cmd = process.argv[2] || 'refresh';
  if (cmd === 'refresh') {
    const r = refreshRegistryFromDisk();
    const pull = r.repos.filter((x) => x.pull).length;
    console.log(`Registry: ${r.repos.length} repos, ${pull} pull, ${r.repos.length - pull} skip`);
    console.log(REGISTRY_PATH);
  } else if (cmd === 'list-pull') {
    getDefaultPullPaths().forEach((p) => console.log(p));
  } else {
    console.error('Usage: node sync-pull-registry-ops.js [refresh|list-pull]');
    process.exit(1);
  }
}
