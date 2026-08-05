'use strict';
const fs = require('fs');
const vm = require('vm');
const path = require('path');

const root = path.join(__dirname, '..');
const dataPath = path.join(root, 'School Scrips', 'School documents', 'exam2-review-map-data.js');
const statePath = path.join(root, 'School Scrips', 'School documents', 'exam2-review-map-state.json');

const ctx = {};
vm.runInNewContext(
  fs.readFileSync(dataPath, 'utf8') +
    '\n;this.REVIEW = REVIEW; this.PROBLEMS = PROBLEMS;',
  ctx
);

const state = JSON.parse(fs.readFileSync(statePath, 'utf8'));
const native = new Set(ctx.REVIEW.map((r) => r.questionId));
const removed = new Set(state.removed || []);
const added = (state.added || []).filter((id) => !native.has(id) && !removed.has(id));
const active = ctx.REVIEW.filter((r) => !removed.has(r.questionId)).map((r) => r.questionId);
const all = [...active, ...added];

/** Manual tags — expression + Pearson objective, same rules as prior 18-Q analysis. */
const MANUAL = {
  '3.3.63': [],
  '3.3.21': [],
  '3.3.47': ['product'],
  '3.3.68': [],
  '3.4.20': ['product', 'logExp'],
  '3.4.22': ['quotient'],
  '3.4.25': ['quotient', 'logExp'],
  '3.5.25': ['product', 'trig', 'chain', 'logExp'],
  '3.5.29': ['quotient', 'trig'],
  '3.5.43': ['trig'],
  '3.5.59': ['product', 'trig', 'logExp'],
  '3.6.25': [],
  '3.6.29': [],
  '3.6.43': [],
  '3.7.23': ['trig', 'chain'],
  '3.7.28': ['chain'],
  '3.7.29': ['chain'],
  '3.7.31': ['chain'],
  '3.7.44': ['trig', 'chain'],
  '3.7.46': ['trig', 'chain'],
  '3.7.53': ['chain', 'logExp'],
  '3.7.55': ['trig', 'chain'],
  '3.7.63': ['chain'],
  '3.7.70': ['product', 'chain', 'logExp'],
  '3.9.16': ['product', 'logExp'],
  '3.9.17': ['chain', 'logExp'],
  '3.9.36': ['chain', 'logExp'],
  '3.9.39': ['logExp'],
  '3.9.63': ['chain', 'logExp'],
  '3.9.75': ['chain', 'logExp'],
  '3.10.13': ['chain', 'inverse'],
  '3.10.29': ['chain', 'inverse'],
  '3.10.36': ['chain', 'logExp', 'inverse'],
  '3.10.52': ['inverse'],
};

const rows = all.map((id) => ({
  id,
  expr: (ctx.PROBLEMS[id] && ctx.PROBLEMS[id].expr) || '',
  planned: !native.has(id),
  tags: MANUAL[id] || [],
}));

const concepts = ['product', 'quotient', 'trig', 'chain', 'logExp', 'inverse'];
const counts = Object.fromEntries(
  concepts.map((k) => [k, rows.filter((r) => r.tags.includes(k)).length])
);

console.log(
  JSON.stringify(
    {
      total: rows.length,
      official: active.length,
      planned: added.length,
      counts,
      outside: rows.filter((r) => r.tags.length === 0).map((r) => r.id),
      rows,
    },
    null,
    2
  )
);
