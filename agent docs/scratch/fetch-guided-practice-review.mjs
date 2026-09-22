/**
 * Fetch guided-practice attempts from Supabase and build review HTML.
 *
 * Run from Programs root:
 *   node "agent docs/scratch/fetch-guided-practice-review.mjs" --student-id 57ccdad0-6017-4f9b-8e7d-10334b97dc42 --student "Michelle (Spare 3)"
 */
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import dotenv from 'dotenv';
import { pathToFileURL } from 'node:url';

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) {
      continue;
    }
    const key = token.slice(2);
    const next = argv[i + 1];
    out[key] = next && !next.startsWith('--') ? argv[++i] : 'true';
  }
  return out;
}

const scratchDir = path.dirname(fileURLToPath(import.meta.url));
const programsRoot = path.resolve(scratchDir, '../..');
const sessionKitRoot = path.join(programsRoot, 'School Scrips', 'student-session-kit');
dotenv.config({ path: path.join(sessionKitRoot, '.env') });

const args = parseArgs(process.argv.slice(2));
const studentId = args['student-id']?.trim();
const studentLabel = args.student?.trim() ?? 'Student';

if (!studentId) {
  console.error('Usage: fetch-guided-practice-review.mjs --student-id <uuid> [--student "Name"]');
  process.exit(1);
}

const url = process.env.VITE_SUPABASE_URL?.trim();
const key = process.env.SUPABASE_SERVICE_ROLE_KEY?.trim();
if (!url || !key) {
  console.error('Missing VITE_SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in student-session-kit/.env');
  process.exit(1);
}

const supabaseModule = pathToFileURL(
  path.join(sessionKitRoot, 'node_modules/@supabase/supabase-js/dist/module/index.js'),
).href;
const { createClient } = await import(supabaseModule);
const client = createClient(url, key, { auth: { persistSession: false } });

const { data, error } = await client
  .from('attempts')
  .select(
    'id,status,score,max_score,started_at,completed_at,problem_id,session_log,attempt_items(slot,outcome,item_kind,attempt_count,selected_option_id)',
  )
  .eq('student_id', studentId)
  .eq('activity_id', 'matrix/guided-practice')
  .order('started_at', { ascending: true });

if (error) {
  console.error(error.message);
  process.exit(1);
}

if (!data?.length) {
  console.error(`No guided-practice attempts for ${studentId}`);
  process.exit(1);
}

const buildScript = path.join(scratchDir, 'build-guided-practice-attempt-page.mjs');
const written = [];

for (const attempt of data) {
  const slug = attempt.id.slice(0, 8);
  const payloadFile = `attempt-${slug}-payload.json`;
  fs.writeFileSync(path.join(scratchDir, payloadFile), JSON.stringify([attempt], null, 2), 'utf8');

  const result = spawnSync(
    process.execPath,
    [buildScript, '--payload', payloadFile, '--student', studentLabel, '--slug', slug],
    { stdio: 'inherit', cwd: scratchDir },
  );

  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }

  written.push(`http://127.0.0.1:8765/scratch/guided-practice-attempt-${slug}.html`);
}

console.log(`Built ${written.length} page(s):`);
for (const link of written) {
  console.log(link);
}
