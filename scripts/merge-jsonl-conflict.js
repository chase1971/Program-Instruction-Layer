#!/usr/bin/env node
const fs = require('fs');

function mergeJsonlConflict(filePath) {
  const raw = fs.readFileSync(filePath, 'utf8');
  if (!raw.includes('<<<<<<< HEAD')) {
    console.log(`No conflict: ${filePath}`);
    return;
  }
  const start = raw.indexOf('<<<<<<< HEAD');
  const mid = raw.indexOf('=======', start);
  const end = raw.indexOf('>>>>>>> origin/main', mid);
  const ours = raw.slice(0, start).trim().split(/\r?\n/).filter(Boolean);
  const theirs = raw
    .slice(mid + '======='.length, end)
    .trim()
    .split(/\r?\n/)
    .filter(Boolean);
  const byId = new Map();
  for (const line of [...ours, ...theirs]) {
    try {
      const o = JSON.parse(line);
      byId.set(o.id || line, line);
    } catch {
      /* skip malformed */
    }
  }
  const merged = [...byId.values()].sort((a, b) => {
    try {
      return JSON.parse(a).timestamp.localeCompare(JSON.parse(b).timestamp);
    } catch {
      return 0;
    }
  });
  fs.writeFileSync(filePath, `${merged.join('\n')}\n`);
  console.log(`Merged ${merged.length} entries in ${filePath}`);
}

for (const file of process.argv.slice(2)) {
  mergeJsonlConflict(file);
}
