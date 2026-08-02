/**
 * FILE: scripts/archive-stale-plans.js
 * PURPOSE: Move plans nobody has touched in STALE_PLAN_DAYS into docs/archive/plans/.
 *
 * WHY AGE AND NOT STATUS:
 *   A plan's declared status lies. It gets written once, the work happens (or gets
 *   restarted a different way), and the header is never edited again — so a shipped
 *   plan still reads "not yet implemented". Git's last-commit date cannot drift like
 *   that. And because age is measured from last TOUCH, a plan under active edit keeps
 *   resetting its own clock; only abandoned ones age out.
 *
 * WHY ARCHIVE AND NOT DELETE:
 *   "Where did that plan go" needs exactly one answer. Archived plans stay greppable
 *   and stay in git history. Nothing here deletes.
 *
 * Usage:
 *   node scripts/archive-stale-plans.js          # dry run — prints what would move
 *   node scripts/archive-stale-plans.js --yes    # perform the moves (git mv)
 *   node scripts/archive-stale-plans.js --keep <name> [--keep <name>]…
 *                                                # spare specific files this run
 *
 * Reference docs never expire and are not swept — only docs/plans/**.md.
 * Chase's own reminders live in docs/chase-notes/ and are never touched.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { execSync, execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const STALE_PLAN_DAYS = 7;

const argv = process.argv.slice(2);
const apply = argv.includes('--yes');
const keep = new Set(
  argv.reduce((acc, a, i) => (a === '--keep' && argv[i + 1] ? [...acc, argv[i + 1]] : acc), []),
);

const IGNORED_DIRS = new Set([
  'node_modules', '.git', 'dist', 'build', 'out', '__pycache__', '.vite',
  'archive', 'Archived markdowns', 'Deprecated apps', 'python-runtime', 'logs',
  '.husky', 'dist-installer', 'test-results', 'backups', 'venv', '.venv',
  'site-packages', 'coverage', 'chase-notes',
]);

function findPlanDirs(dir, out = []) {
  let entries;
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return out; }
  for (const e of entries) {
    if (!e.isDirectory() || IGNORED_DIRS.has(e.name)) continue;
    const full = path.join(dir, e.name);
    if (e.name === 'plans' && path.basename(path.dirname(full)) === 'docs') out.push(full);
    else findPlanDirs(full, out);
  }
  return out;
}

function lastTouchedUnix(absFile) {
  try {
    const out = execSync(`git log -1 --format=%ct -- "${path.basename(absFile)}"`, {
      cwd: path.dirname(absFile), encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'],
    }).trim();
    if (out) return Number(out);
  } catch { /* untracked or not a repo */ }
  try { return Math.floor(fs.statSync(absFile).mtimeMs / 1000); } catch { return null; }
}

const rel = (f) => path.relative(ROOT, f).split(path.sep).join('/');
const nowUnix = Math.floor(Date.now() / 1000);

const stale = [];
for (const planDir of findPlanDirs(ROOT)) {
  // Frozen apps are never swept — see .cursor/rules/45-frozen-apps.mdc
  if (planDir.includes('Calendar 2.0')) continue;
  for (const name of fs.readdirSync(planDir).filter((f) => f.endsWith('.md'))) {
    if (name === 'README.md' || keep.has(name)) continue;
    const abs = path.join(planDir, name);
    const ts = lastTouchedUnix(abs);
    if (ts === null) continue;
    const days = Math.floor((nowUnix - ts) / 86400);
    if (days >= STALE_PLAN_DAYS) stale.push({ abs, name, days, planDir });
  }
}
stale.sort((a, b) => b.days - a.days);

if (!stale.length) {
  console.log(`✅ No plans untouched ${STALE_PLAN_DAYS}+ days. Nothing to archive.`);
  process.exit(0);
}

console.log(
  `\n${apply ? '📦 Archiving' : '🔍 Would archive'} ${stale.length} plan(s) ` +
  `untouched ${STALE_PLAN_DAYS}+ days:\n`,
);

// Inbound references: moving a plan that something still links to creates a dead link.
// Report them so the pointer gets repaired in the same pass — this is how the archive
// stays traceable instead of just breaking whatever pointed at it.
function inboundRefs(name, appRoot) {
  try {
    const out = execSync(`git grep -l -F "${name}" -- "*.md" "*.mdc"`, {
      cwd: appRoot, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'],
    });
    return out.split('\n').map((s) => s.trim()).filter((s) => s && !s.endsWith(`plans/${name}`));
  } catch { return []; } // git grep exits 1 on no matches
}

let moved = 0;
const needRepair = [];
for (const p of stale) {
  const destDir = path.join(path.dirname(p.planDir), 'archive', 'plans');
  const dest = path.join(destDir, p.name);
  const appRoot = path.dirname(path.dirname(p.planDir)); // …/<app>
  const refs = inboundRefs(p.name, appRoot);
  console.log(`  ${String(p.days).padStart(4)}d  ${rel(p.abs)}\n         → ${rel(dest)}`);
  if (refs.length) {
    console.log(`         ⚠  still referenced by: ${refs.join(', ')}`);
    needRepair.push({ name: p.name, refs });
  }
  if (!apply) continue;

  fs.mkdirSync(destDir, { recursive: true });
  const cwd = path.dirname(p.abs);
  try {
    execFileSync('git', ['mv', p.abs, dest], { cwd, stdio: ['ignore', 'ignore', 'pipe'] });
  } catch {
    fs.renameSync(p.abs, dest); // untracked file — plain move
  }
  moved++;
}

if (apply) {
  console.log(`\n✅ Archived ${moved} plan(s). Nothing deleted — all recoverable from git.`);
  if (needRepair.length) {
    console.log(`\n⚠  ${needRepair.length} archived plan(s) were still referenced. Repoint these to`);
    console.log('   docs/archive/plans/ — otherwise you have just created dead links:');
    for (const r of needRepair) console.log(`   ${r.name}\n      ${r.refs.join('\n      ')}`);
  }
  console.log('\n   Verify with: node scripts/check-docs.js');
} else {
  console.log('\nDry run — nothing moved. Re-run with --yes to archive.');
  console.log('Spare one: --keep <filename>');
}
