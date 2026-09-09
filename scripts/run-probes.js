/**
 * FILE: scripts/run-probes.js
 * PURPOSE: Run the fixed retrieval probe set against a fresh agent session per
 *          question, and record correctness + real token cost for each.
 *
 * WHY THIS EXISTS: you cannot measure whether an indexing change helped by
 * watching real work — task difficulty varies ~90x and swamps the signal.
 * Holding the question constant is the only way to attribute a difference to
 * the change you made.
 *
 * Usage:
 *   node scripts/run-probes.js --label "baseline"
 *   node scripts/run-probes.js --label "after-index-rewrite"
 *   node scripts/run-probes.js --label "opus" --model claude-opus-5-thinking-high
 *   node scripts/run-probes.js --label "smoke" --only file-size-cap,python-launcher
 *
 * Each run writes agent docs/probes/runs/<timestamp>-<label>.json.
 * Then: node scripts/probe-report.js
 *
 * Read-only by construction: every probe runs with --mode ask, which cannot edit.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const PROBE_FILE = path.join(ROOT, 'agent docs', 'probes', 'retrieval-probes.json');
const RUNS_DIR = path.join(ROOT, 'agent docs', 'probes', 'runs');

function arg(name, fallback = null) {
  const i = process.argv.indexOf(`--${name}`);
  return i !== -1 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}

function slug(s) {
  return String(s).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'run';
}

// cursor-agent is a .ps1 shim, so it must go through PowerShell rather than
// being spawned directly.
function runProbe(question, model) {
  const args = ['-p', '--output-format', 'json', '--trust', '--mode', 'ask'];
  if (model && model !== 'auto') args.push('--model', model);

  const psCmd = `& cursor-agent ${args.map((a) => `'${a.replace(/'/g, "''")}'`).join(' ')} `
    + `'${question.replace(/'/g, "''")}'`;

  const started = Date.now();
  const r = spawnSync('powershell.exe', ['-NoProfile', '-NonInteractive', '-Command', psCmd], {
    encoding: 'utf8',
    timeout: 5 * 60 * 1000,
    maxBuffer: 16 * 1024 * 1024,
    cwd: ROOT,
  });
  const elapsedMs = Date.now() - started;

  const raw = `${r.stdout || ''}`.trim();
  const start = raw.indexOf('{');
  if (start === -1) {
    return { ok: false, error: (r.stderr || 'no JSON in output').slice(0, 300), elapsedMs };
  }
  let j;
  try {
    j = JSON.parse(raw.slice(start));
  } catch (e) {
    return { ok: false, error: `unparseable JSON: ${e.message}`, elapsedMs };
  }
  const u = j.usage || {};
  return {
    ok: !j.is_error,
    answer: String(j.result || ''),
    elapsedMs,
    apiMs: j.duration_api_ms || null,
    inputTokens: u.inputTokens || 0,
    outputTokens: u.outputTokens || 0,
    cacheReadTokens: u.cacheReadTokens || 0,
    cacheWriteTokens: u.cacheWriteTokens || 0,
  };
}

function grade(answer, mustInclude) {
  const hay = String(answer || '').toLowerCase();
  const missing = (mustInclude || []).filter((k) => !hay.includes(String(k).toLowerCase()));
  return { correct: missing.length === 0, missing };
}

function main() {
  const label = arg('label', 'unlabeled');
  const model = arg('model', 'auto');
  const only = arg('only');
  const spec = JSON.parse(fs.readFileSync(PROBE_FILE, 'utf8'));

  let probes = spec.probes;
  if (only) {
    const want = new Set(only.split(',').map((s) => s.trim()));
    probes = probes.filter((p) => want.has(p.id));
  }
  if (!probes.length) {
    process.stderr.write('No probes selected.\n');
    process.exit(1);
  }

  fs.mkdirSync(RUNS_DIR, { recursive: true });
  process.stdout.write(`Running ${probes.length} probe(s) · label="${label}" · model=${model}\n`);
  process.stdout.write('Each runs in its own fresh session, read-only.\n\n');

  const results = [];
  for (let i = 0; i < probes.length; i++) {
    const p = probes[i];
    process.stdout.write(`[${String(i + 1).padStart(2)}/${probes.length}] ${p.id} … `);
    const r = runProbe(p.question, model);
    const g = r.ok ? grade(r.answer, p.mustInclude) : { correct: false, missing: p.mustInclude };
    const billed = (r.inputTokens || 0) + (r.outputTokens || 0)
      + (r.cacheReadTokens || 0) + (r.cacheWriteTokens || 0);
    results.push({
      id: p.id,
      tier: p.tier,
      correct: g.correct,
      missing: g.missing,
      billedTokens: billed,
      inputTokens: r.inputTokens || 0,
      outputTokens: r.outputTokens || 0,
      elapsedMs: r.elapsedMs,
      answer: (r.answer || '').slice(0, 600),
      error: r.error || null,
    });
    process.stdout.write(
      `${g.correct ? 'PASS' : 'FAIL'}  ${(billed / 1000).toFixed(1)}k tok  `
      + `${(r.elapsedMs / 1000).toFixed(1)}s`
      + `${g.correct ? '' : `  (missing: ${g.missing.join(', ')})`}\n`,
    );
  }

  const byTier = {};
  for (const r of results) {
    if (!byTier[r.tier]) byTier[r.tier] = { n: 0, correct: 0, tokens: 0 };
    byTier[r.tier].n += 1;
    byTier[r.tier].correct += r.correct ? 1 : 0;
    byTier[r.tier].tokens += r.billedTokens;
  }

  const run = {
    label,
    model,
    startedAt: new Date().toISOString(),
    probeVersion: spec.version,
    total: results.length,
    correct: results.filter((r) => r.correct).length,
    billedTokens: results.reduce((a, r) => a + r.billedTokens, 0),
    elapsedMs: results.reduce((a, r) => a + r.elapsedMs, 0),
    byTier,
    results,
  };

  const file = path.join(RUNS_DIR, `${run.startedAt.replace(/[:.]/g, '-')}-${slug(label)}.json`);
  fs.writeFileSync(file, JSON.stringify(run, null, 2), 'utf8');

  process.stdout.write(`\n${run.correct}/${run.total} correct · `
    + `${(run.billedTokens / 1000).toFixed(0)}k tokens · `
    + `${(run.elapsedMs / 1000).toFixed(0)}s\n`);
  for (const [tier, d] of Object.entries(byTier)) {
    process.stdout.write(`  ${tier.padEnd(10)} ${d.correct}/${d.n} correct · ${(d.tokens / 1000).toFixed(0)}k tokens\n`);
  }
  process.stdout.write(`\nSaved: ${path.relative(ROOT, file)}\n`);
  process.stdout.write('Report: node scripts/probe-report.js\n');
}

if (require.main === module) main();

module.exports = { grade, runProbe };
