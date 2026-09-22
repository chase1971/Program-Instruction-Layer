/**
 * Combined Cynthia + Maria guided-practice viewer — survey on top,
 * Problem 1 / Problem 2 tabs, student prev/next arrows.
 *
 * Run from Programs root:
 *   node "agent docs/scratch/build-guided-practice-student-viewer.mjs"
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const dir = path.dirname(fileURLToPath(import.meta.url));
const programsRoot = path.resolve(dir, '../..');
const envPath = path.join(programsRoot, 'School Scrips', 'student-session-kit', '.env');

function readEnv(filePath) {
  const text = fs.readFileSync(filePath, 'utf8');
  const out = {};
  for (const line of text.split(/\r?\n/)) {
    const m = line.match(/^([A-Z0-9_]+)=(.*)$/);
    if (m) out[m[1]] = m[2];
  }
  return out;
}

const env = readEnv(envPath);
const baseUrl = env.VITE_SUPABASE_URL?.trim();
const serviceKey = env.SUPABASE_SERVICE_ROLE_KEY?.trim();
if (!baseUrl || !serviceKey) {
  console.error('Missing Supabase env in student-session-kit/.env');
  process.exit(1);
}

const headers = {
  apikey: serviceKey,
  Authorization: `Bearer ${serviceKey}`,
};

const STUDENTS = [
  { id: '3bc881fd-2854-4938-b6cc-2e3570313d40', name: 'Maria Garcia Baptiste' },
  { id: '943b6378-ab8c-43bd-b310-9285921357dd', name: 'Cynthia Jimenez Duran' },
];

const GP_SELECT =
  'id,status,score,max_score,started_at,completed_at,problem_id,session_log,attempt_items(slot,outcome,item_kind,attempt_count,selected_option_id)';
const SV_SELECT = 'id,status,completed_at,attempt_items(slot,selected_option_id)';

const SURVEY_LABELS = [
  'When you got a step wrong, did the help make sense?',
  'Did you use the help buttons (fraction help, row notation help)?',
  'Would you use this again before a test?',
  'Anything else we should know?',
];

const MCQ_LABELS = {
  no: 'No',
  maybe: 'Maybe',
  yes: 'Yes',
  didnt_use: "I didn't use it",
};

async function fetchJson(url) {
  const res = await fetch(url, { headers });
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
  return res.json();
}

function sortByStarted(attempts) {
  return [...attempts].sort((a, b) => {
    const left = a.started_at ?? a.completed_at ?? '';
    const right = b.started_at ?? b.completed_at ?? '';
    const byStarted = left.localeCompare(right);
    if (byStarted !== 0) return byStarted;
    return (a.completed_at ?? '').localeCompare(b.completed_at ?? '');
  });
}

function problemSlotsFromAttempts(guidedAttempts) {
  let problem1 = { dot: 'blank', attempt: null };
  let problem2 = { dot: 'blank', attempt: null };
  let completedCount = 0;

  for (const attempt of sortByStarted(guidedAttempts)) {
    if (attempt.status === 'completed') {
      if (completedCount === 0) problem1 = { dot: 'green', attempt };
      else if (completedCount === 1) problem2 = { dot: 'green', attempt };
      completedCount += 1;
      continue;
    }
    if (attempt.status === 'abandoned' || attempt.status === 'in_progress') {
      if (completedCount === 0 && problem1.dot !== 'green') {
        problem1 = { dot: 'red', attempt };
      } else if (completedCount === 1 && problem2.dot !== 'green') {
        problem2 = { dot: 'red', attempt };
      }
    }
  }
  return { problem1, problem2 };
}

function formatSurveyAnswer(raw) {
  if (raw == null || String(raw).trim() === '') return '—';
  return MCQ_LABELS[raw] ?? raw;
}

function toAttemptData(row) {
  if (!row) return null;
  return {
    attemptId: row.id,
    status: row.status,
    score: row.score,
    maxScore: row.max_score,
    startedAt: row.started_at,
    completedAt: row.completed_at,
    problemId: row.problem_id,
    attemptItems: row.attempt_items ?? [],
    sessionLog: row.session_log ?? { events: [] },
  };
}

function surveyRows(surveyAttempts) {
  const completed = surveyAttempts
    .filter((a) => a.status === 'completed')
    .sort((a, b) => (b.completed_at ?? '').localeCompare(a.completed_at ?? ''));
  if (!completed.length) return null;
  const attempt = completed[0];
  const bySlot = Object.fromEntries((attempt.attempt_items ?? []).map((i) => [i.slot, i.selected_option_id]));
  return {
    completedAt: attempt.completed_at,
    answers: ['1', '2', '3', '4'].map((slot, index) => ({
      label: SURVEY_LABELS[index],
      value: slot === '4' ? (bySlot[slot]?.trim() || '—') : formatSurveyAnswer(bySlot[slot]),
    })),
  };
}

async function loadStudent(student) {
  const gpUrl = `${baseUrl}/rest/v1/attempts?student_id=eq.${student.id}&activity_id=eq.matrix/guided-practice&select=${GP_SELECT}&order=started_at.asc`;
  const svUrl = `${baseUrl}/rest/v1/attempts?student_id=eq.${student.id}&activity_id=eq.matrix/guided-practice-survey&select=${SV_SELECT}&order=completed_at.desc`;
  const [guidedPractice, surveyAttempts] = await Promise.all([fetchJson(gpUrl), fetchJson(svUrl)]);
  const slots = problemSlotsFromAttempts(guidedPractice);
  return {
    id: student.id,
    name: student.name,
    survey: surveyRows(surveyAttempts),
    problem1: {
      dot: slots.problem1.dot,
      data: toAttemptData(slots.problem1.attempt),
    },
    problem2: {
      dot: slots.problem2.dot,
      data: toAttemptData(slots.problem2.attempt),
    },
  };
}

const attemptBuilderSource = fs.readFileSync(
  path.join(dir, 'build-guided-practice-attempt-page.mjs'),
  'utf8',
);
const styleMatch = attemptBuilderSource.match(/<style>([\s\S]*?)<\/style>/);
const scriptMatch = attemptBuilderSource.match(
  /<script>\r?\n\(function \(\) \{\r?\n  'use strict';([\s\S]*?)\r?\n\}\)\(\);\r?\n<\/script>/,
);
if (!styleMatch || !scriptMatch) {
  throw new Error('Could not extract styles/scripts from build-guided-practice-attempt-page.mjs');
}

const baseStyles = styleMatch[1];
let baseRenderScript = scriptMatch[1];
baseRenderScript = baseRenderScript
  .replace(/document\.getElementById\('hero-sub'\)/g, "mount.querySelector('[data-hero-sub]')")
  .replace(/document\.getElementById\('meta-grid'\)/g, "mount.querySelector('[data-meta-grid]')")
  .replace(/document\.getElementById\('ledger-root'\)/g, "mount.querySelector('[data-ledger-root]')")
  .replace(/document\.getElementById\('q-detail-panel'\)/g, "mount.querySelector('[data-q-detail-panel]')")
  .replace(/document\.getElementById\('q-panel-store'\)/g, "mount.querySelector('[data-q-panel-store]')")
  .replace(/document\.getElementById\('struggle-root'\)/g, "mount.querySelector('[data-struggle-root]')")
  .replace(/document\.getElementById\('timeline-root'\)/g, "mount.querySelector('[data-timeline-root]')")
  .replace(/document\.getElementById\('aggregates-root'\)/g, "mount.querySelector('[data-aggregates-root]')")
  .replace(/document\.getElementById\('raw-json'\)/g, "mount.querySelector('[data-raw-json]')")
  .replace(/document\.getElementById\('timeline-toggle'\)/g, "mount.querySelector('[data-timeline-toggle]')")
  .replace(/document\.getElementById\('timeline-body'\)/g, "mount.querySelector('[data-timeline-body]')")
  .replace(/document\.getElementById\('raw-toggle'\)/g, "mount.querySelector('[data-raw-toggle]')")
  .replace(
    /var DATA = JSON\.parse\(document\.getElementById\('attempt-data'\)\.textContent\);/,
    'var DATA = JSON.parse(mount.querySelector("[data-attempt-data]").textContent);',
  )
  .replace(/\/\* ---- Gap panel ----[\s\S]*?\/\* ---- Timeline collapse ---- \*\//, '/* ---- Timeline collapse ---- */')
  .replace(
    /this\.textContent = opening \? 'Hide decoded timeline \(\$\{eventCount\} events\)' : 'Show decoded timeline \(\$\{eventCount\} events\)';/,
    "this.textContent = opening ? 'Hide decoded timeline (' + events.length + ' events)' : 'Show decoded timeline (' + events.length + ' events)';",
  )
  .replace(
    /mount\.querySelector\('\[data-hero-sub\]'\)\.textContent =[\s\S]*?events\.length \+ ' events';/,
    "mount.querySelector('[data-hero-sub]').textContent = 'Problem ' + DATA.problemId + ' · ' + DATA.score + '/' + DATA.maxScore + ' · ' + events.length + ' events';",
  );

const students = [];
for (const student of STUDENTS) {
  const loaded = await loadStudent(student);
  students.push(loaded);
  console.log(
    `${student.name}: P1=${loaded.problem1.dot}${loaded.problem1.data ? ' prob ' + loaded.problem1.data.problemId : ''}, P2=${loaded.problem2.dot}${loaded.problem2.data ? ' prob ' + loaded.problem2.data.problemId : ''}, survey=${loaded.survey ? 'yes' : 'no'}`,
  );
}

const htmlName = 'guided-practice-student-viewer.html';
const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Guided practice — Cynthia &amp; Maria (layout prototype)</title>
<style>
${baseStyles}
  .student-nav {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 12px;
    align-items: center;
    margin: 0 0 24px;
  }
  .student-nav button {
    padding: 18px 24px;
    font: 700 18px system-ui, sans-serif;
    background: #fff;
    border: 2px solid var(--line);
    border-radius: 14px;
    cursor: pointer;
    min-height: 3.5rem;
  }
  .student-nav button:disabled { opacity: 0.35; cursor: default; }
  .student-nav .student-name {
    text-align: center;
    font-size: 28px;
    font-weight: 800;
    margin: 0;
  }
  .student-nav .student-sub {
    text-align: center;
    color: var(--soft);
    font-size: 16px;
    margin: 4px 0 0;
  }
  .survey-card {
    background: #fff;
    border: 2px solid var(--line);
    border-radius: 16px;
    padding: 22px 24px;
    margin: 0 0 24px;
  }
  .survey-card h2 { margin: 0 0 6px; font-size: 24px; border: none; padding: 0; }
  .survey-card .when { color: var(--soft); margin: 0 0 16px; font-size: 15px; }
  .survey-grid { display: grid; gap: 12px; }
  .survey-row {
    border: 2px solid var(--line);
    border-radius: 12px;
    padding: 14px 16px;
    background: #fbfcfe;
  }
  .survey-row .q { font-weight: 700; margin: 0 0 8px; }
  .survey-row .a { margin: 0; white-space: pre-wrap; }
  .problem-tabs {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin: 0 0 20px;
  }
  .problem-tabs button {
    padding: 16px 18px;
    font: 700 17px system-ui, sans-serif;
    background: #fff;
    border: 2px solid var(--line);
    border-radius: 12px;
    cursor: pointer;
    min-height: 3.25rem;
    text-align: left;
  }
  .problem-tabs button.active {
    border-color: #2563eb;
    background: var(--bluebg);
    box-shadow: 0 0 0 3px #bfdbfe;
  }
  .problem-tabs .tab-sub { display: block; font-weight: 400; font-size: 13px; color: var(--soft); margin-top: 4px; }
  .empty-problem {
    background: #fff;
    border: 2px dashed var(--line);
    border-radius: 16px;
    padding: 28px;
    text-align: center;
    color: var(--soft);
    font-size: 18px;
  }
  .dot-green { color: var(--green); font-weight: 700; }
  .dot-red { color: var(--red); font-weight: 700; }
  .dot-blank { color: var(--soft); }
  #problem-mount .banner, #problem-mount .csum, #problem-mount nav.jump, #problem-mount #gap-panel { display: none; }
  #problem-mount h1, #problem-mount .sub { display: none; }
</style>
</head>
<body>

<a class="backlink" href="/pages.html">&larr; All pages</a>

<div class="banner">
  <strong>Layout prototype — live Cynthia &amp; Maria data.</strong>
  Survey on top, Problem 1 / Problem 2 tabs below, arrow between students. Same slot rules as Teacher Console (abandons show red until a finish turns the slot green).
</div>

<h1>Student guided-practice review</h1>
<p class="sub">Pick a student, then a problem tab. Question tiles and struggle cards match the single-attempt review pages.</p>

<div class="student-nav" aria-label="Choose student">
  <button type="button" id="prev-student" aria-label="Previous student">&larr; Previous</button>
  <div>
    <p class="student-name" id="student-name"></p>
    <p class="student-sub" id="student-sub"></p>
  </div>
  <button type="button" id="next-student" style="justify-self:end" aria-label="Next student">Next &rarr;</button>
</div>

<section class="survey-card" id="survey-section">
  <h2>Post-practice survey</h2>
  <p class="when" id="survey-when"></p>
  <div class="survey-grid" id="survey-grid"></div>
</section>

<div class="problem-tabs" role="tablist" aria-label="Problem tabs">
  <button type="button" role="tab" id="tab-problem1" aria-selected="true">Problem 1<span class="tab-sub" id="tab-problem1-sub"></span></button>
  <button type="button" role="tab" id="tab-problem2" aria-selected="false">Problem 2<span class="tab-sub" id="tab-problem2-sub"></span></button>
</div>

<div id="problem-mount"></div>

<script type="application/json" id="students-data">${JSON.stringify(students)}</script>

<script>
(function () {
  'use strict';

  var STUDENTS = JSON.parse(document.getElementById('students-data').textContent);
  var studentIndex = 0;
  var problemTab = 'problem1';

  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function fmtTime(iso) {
    if (!iso) return '—';
    var d = new Date(iso);
    if (isNaN(d)) return iso;
    return d.toLocaleString(undefined, { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' });
  }

  function dotLabel(dot) {
    if (dot === 'green') return 'Completed';
    if (dot === 'red') return 'Abandoned / in progress';
    return 'Not started';
  }

  function dotClass(dot) {
    if (dot === 'green') return 'dot-green';
    if (dot === 'red') return 'dot-red';
    return 'dot-blank';
  }

  function renderSurvey(student) {
    var section = document.getElementById('survey-section');
    var when = document.getElementById('survey-when');
    var grid = document.getElementById('survey-grid');
    if (!student.survey) {
      when.textContent = 'No survey submitted yet.';
      grid.innerHTML = '<div class="empty-problem">Survey not completed</div>';
      return;
    }
    when.textContent = 'Completed ' + fmtTime(student.survey.completedAt);
    grid.innerHTML = student.survey.answers.map(function (row) {
      return '<div class="survey-row"><p class="q">' + esc(row.label) + '</p><p class="a">' + esc(row.value) + '</p></div>';
    }).join('');
  }

  function problemShell(data) {
    if (!data) {
      return '<div class="empty-problem">No attempt in this slot yet.</div>';
    }
    return '<div class="attempt-root">' +
      '<script type="application/json" data-attempt-data>' + JSON.stringify(data).replace(/</g, '\\u003c') + '<\\/script>' +
      '<p data-hero-sub></p>' +
      '<div class="meta-grid" data-meta-grid></div>' +
      '<section class="section-card" id="step-ledger">' +
        '<h2 style="border:none;padding:0;margin:0 0 6px;font-size:26px">All 17 questions</h2>' +
        '<p class="secnote">Four columns — click a question to open the detail panel below it.</p>' +
        '<div class="q-grid" data-ledger-root></div>' +
        '<div data-q-detail-panel class="q-detail-panel" hidden></div>' +
        '<div data-q-panel-store hidden aria-hidden="true"></div>' +
      '</section>' +
      '<section class="section-card" id="struggle-cards">' +
        '<h2 style="border:none;padding:0;margin:0 0 6px;font-size:26px">Struggle cards</h2>' +
        '<p class="secnote">First-try misses only — two columns.</p>' +
        '<div class="struggle-grid" data-struggle-root></div>' +
      '</section>' +
      '<section class="section-card" id="decoded-timeline">' +
        '<h2 style="border:none;padding:0;margin:0 0 6px;font-size:26px">Decoded timeline</h2>' +
        '<button type="button" class="collapsible-toggle" data-timeline-toggle aria-expanded="false">Show decoded timeline</button>' +
        '<div class="collapsible-body" data-timeline-body hidden><ol class="timeline timeline-grid" data-timeline-root></ol></div>' +
      '</section>' +
      '<div class="layout-2col">' +
        '<section class="section-card" id="aggregates">' +
          '<h2 style="border:none;padding:0;margin:0 0 6px;font-size:26px">Aggregates</h2>' +
          '<div data-aggregates-root></div>' +
        '</section>' +
      '</div>' +
      '<button type="button" class="raw-toggle" data-raw-toggle aria-expanded="false">Show raw session_log JSON</button>' +
      '<pre class="raw-json" data-raw-json></pre>' +
    '</div>';
  }

  window.renderGpAttemptInMount = function (mount) {
${baseRenderScript}
  };

  function renderProblem(student) {
    var slot = student[problemTab];
    var mount = document.getElementById('problem-mount');
    mount.innerHTML = problemShell(slot.data);
    if (slot.data) {
      var root = mount.querySelector('.attempt-root');
      window.renderGpAttemptInMount(root);
      var toggle = root.querySelector('[data-timeline-toggle]');
      var events = slot.data.sessionLog && slot.data.sessionLog.events ? slot.data.sessionLog.events.length : 0;
      if (toggle) toggle.textContent = 'Show decoded timeline (' + events + ' events)';
    }
  }

  function updateTabs(student) {
    ['problem1', 'problem2'].forEach(function (key) {
      var slot = student[key];
      var btn = document.getElementById('tab-' + key);
      var sub = document.getElementById('tab-' + key + '-sub');
      var active = problemTab === key;
      btn.classList.toggle('active', active);
      btn.setAttribute('aria-selected', active ? 'true' : 'false');
      var detail = slot.data
        ? 'Problem ' + slot.data.problemId + ' · ' + slot.data.score + '/' + slot.data.maxScore + ' · ' + dotLabel(slot.dot)
        : dotLabel(slot.dot);
      sub.textContent = detail;
      sub.className = 'tab-sub ' + dotClass(slot.dot);
    });
  }

  function renderAll() {
    var student = STUDENTS[studentIndex];
    document.getElementById('student-name').textContent = student.name;
    document.getElementById('student-sub').textContent = (studentIndex + 1) + ' of ' + STUDENTS.length;
    document.getElementById('prev-student').disabled = studentIndex === 0;
    document.getElementById('next-student').disabled = studentIndex === STUDENTS.length - 1;
    renderSurvey(student);
    updateTabs(student);
    renderProblem(student);
  }

  document.getElementById('prev-student').addEventListener('click', function () {
    if (studentIndex > 0) { studentIndex -= 1; renderAll(); }
  });
  document.getElementById('next-student').addEventListener('click', function () {
    if (studentIndex < STUDENTS.length - 1) { studentIndex += 1; renderAll(); }
  });
  document.getElementById('tab-problem1').addEventListener('click', function () {
    problemTab = 'problem1'; renderAll();
  });
  document.getElementById('tab-problem2').addEventListener('click', function () {
    problemTab = 'problem2'; renderAll();
  });

  renderAll();
})();
</script>

</body>
</html>`;

const outPath = path.join(dir, htmlName);
fs.writeFileSync(outPath, html, 'utf8');
console.log('Wrote', outPath, '(' + html.length + ' bytes)');
console.log('http://127.0.0.1:8765/scratch/' + htmlName);
