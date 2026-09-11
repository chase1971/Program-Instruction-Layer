/**
 * FILE: scripts/prune-momentum-handoffs.js
 * PURPOSE: Delete dated momentum handoff files older than STALE_HANDOFF_DAYS.
 *
 * Keeps latest.md (always the current handoff) and README.md.
 * Run automatically after each "perform a momentum handoff" — see MOMENTUM_HANDOFF.md.
 *
 * Usage:
 *   node scripts/prune-momentum-handoffs.js          # dry run
 *   node scripts/prune-momentum-handoffs.js --yes    # delete stale files
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const HANDOFF_DIR = path.join(ROOT, 'agent docs', 'momentum-handoffs');
const STALE_HANDOFF_DAYS = 3;
const KEEP_NAMES = new Set(['latest.md', 'README.md']);

const argv = process.argv.slice(2);
const apply = argv.includes('--yes');

function isStale(filePath) {
  const stat = fs.statSync(filePath);
  const ageMs = Date.now() - stat.mtimeMs;
  return ageMs > STALE_HANDOFF_DAYS * 24 * 60 * 60 * 1000;
}

function main() {
  if (!fs.existsSync(HANDOFF_DIR)) {
    console.log('No momentum-handoffs folder yet — nothing to prune.');
    return;
  }

  const entries = fs.readdirSync(HANDOFF_DIR, { withFileTypes: true });
  const toRemove = [];

  for (const entry of entries) {
    if (!entry.isFile() || !entry.name.endsWith('.md')) {
      continue;
    }
    if (KEEP_NAMES.has(entry.name)) {
      continue;
    }
    const fullPath = path.join(HANDOFF_DIR, entry.name);
    if (isStale(fullPath)) {
      toRemove.push(fullPath);
    }
  }

  if (toRemove.length === 0) {
    console.log(`No handoffs older than ${STALE_HANDOFF_DAYS} days.`);
    return;
  }

  for (const filePath of toRemove) {
    const label = path.basename(filePath);
    if (apply) {
      fs.unlinkSync(filePath);
      console.log(`Removed ${label}`);
    } else {
      console.log(`Would remove ${label}`);
    }
  }

  if (!apply) {
    console.log(`\nDry run — pass --yes to delete ${toRemove.length} file(s).`);
  }
}

main();
