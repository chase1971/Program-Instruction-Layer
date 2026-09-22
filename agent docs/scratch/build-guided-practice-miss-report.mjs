/**
 * Guided-practice miss report — misses only, teacher skill labels, class aggregates,
 * post-survey summary, and mini-tutorial help feedback.
 *
 * Run from Programs root:
 *   node "agent docs/scratch/build-guided-practice-miss-report.mjs"
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import {
  aggregateCategoryOrder,
  BADGE_DESCRIPTIONS,
  BADGE_LABELS,
  HELP_TOPIC_LABELS,
  MCQ_LABELS,
  skillForSlot,
  SURVEY_LABELS,
} from './guided-practice-skill-labels.mjs';

const dir = path.dirname(fileURLToPath(import.meta.url));
const programsRoot = path.resolve(dir, '../..');
const rosterPath = path.join(
  'C:',
  'Users',
  'chase',
  'My Drive',
  'Rosters etc',
  'MATH-1324 4202 1',
  'student-portal-codes.json',
);
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

const GP_SELECT =
  'id,status,score,max_score,started_at,completed_at,problem_id,session_log,attempt_items(slot,outcome,item_kind,attempt_count,selected_option_id)';
const SV_SELECT = 'id,status,completed_at,attempt_items(slot,selected_option_id)';

async function fetchJson(url) {
  const res = await fetch(url, { headers });
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
  return res.json();
}

function loadRoster() {
  const raw = JSON.parse(fs.readFileSync(rosterPath, 'utf8'));
  return Object.entries(raw.students)
    .filter(
      ([, row]) =>
        !String(row.username || '').includes('TESTER') && row.firstName !== 'Tester',
    )
    .map(([id, row]) => ({
      id,
      name: `${row.firstName} ${row.lastName}`,
    }))
    .sort((a, b) => a.name.localeCompare(b.name));
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

function surveyFromAttempts(surveyAttempts) {
  const completed = surveyAttempts
    .filter((a) => a.status === 'completed')
    .sort((a, b) => (b.completed_at ?? '').localeCompare(a.completed_at ?? ''));
  if (!completed.length) return null;
  const attempt = completed[0];
  const bySlot = Object.fromEntries(
    (attempt.attempt_items ?? []).map((i) => [i.slot, i.selected_option_id]),
  );
  return {
    completedAt: attempt.completed_at,
    answers: ['1', '2', '3', '4'].map((slot, index) => ({
      label: SURVEY_LABELS[index],
      value: slot === '4' ? (bySlot[slot]?.trim() || '—') : formatSurveyAnswer(bySlot[slot]),
    })),
  };
}

const TRANSFORM_LABELS = {
  'row-scaling': 'Row scaling',
  'row-replacement': 'Row replacement',
  'row-swap': 'Row swap',
};

function readableChoice(category, choice) {
  if (category === 'transform-type') {
    return TRANSFORM_LABELS[choice] ?? choice;
  }
  return choice;
}

function expectedBySlotFromItems(attemptItems) {
  const map = {};
  for (const item of attemptItems ?? []) {
    if (item.expected_option_id) {
      map[item.slot] = item.expected_option_id;
    } else if (item.outcome === 'correct' && item.selected_option_id) {
      map[item.slot] = item.selected_option_id;
    }
  }
  return map;
}

function missesFromEvents(events, attemptItems = []) {
  const expectedBySlot = expectedBySlotFromItems(attemptItems);
  const bySlot = new Map();

  for (const event of events) {
    if (event.kind !== 'answer' || !event.slot) continue;
    if (!bySlot.has(event.slot)) {
      bySlot.set(event.slot, { wrongs: [], firstTry: null, finalCorrect: null });
    }
    const row = bySlot.get(event.slot);
    if (event.attemptIndex === 1) row.firstTry = event;
    if (event.correct === false) row.wrongs.push(event);
    if (event.correct === true) row.finalCorrect = event;
  }

  const misses = [];
  for (const [slot, row] of bySlot.entries()) {
    const firstTryMiss = row.firstTry?.correct === false;
    if (!firstTryMiss && row.wrongs.length === 0) continue;

    const skill = skillForSlot(slot);
    const expectedRaw =
      expectedBySlot[slot] ?? row.finalCorrect?.choice ?? null;
    misses.push({
      slot,
      category: skill.category,
      badgeLabel: skill.badgeLabel,
      description: skill.description,
      tryCount: row.wrongs.length || 1,
      wrongChoices: row.wrongs.map((w) => ({
        choice: readableChoice(skill.category, w.choice),
        attemptIndex: w.attemptIndex,
      })),
      expectedAnswer: expectedRaw
        ? readableChoice(skill.category, expectedRaw)
        : null,
    });
  }

  misses.sort(
    (a, b) =>
      aggregateCategoryOrder().indexOf(a.category) -
      aggregateCategoryOrder().indexOf(b.category),
  );

  return misses;
}

function groupMissesIntoBadges(misses) {
  const byCategory = new Map();
  for (const miss of misses) {
    if (!byCategory.has(miss.category)) {
      byCategory.set(miss.category, {
        category: miss.category,
        badgeLabel: miss.badgeLabel,
        description: miss.description,
        count: 0,
        instances: [],
      });
    }
    const badge = byCategory.get(miss.category);
    badge.count += 1;
    badge.instances.push(miss);
  }
  return aggregateCategoryOrder()
    .filter((cat) => byCategory.has(cat))
    .map((cat) => byCategory.get(cat));
}

function helpFeedbackFromEvents(events) {
  const out = [];
  for (const event of events) {
    if (event.kind !== 'help-feedback' || !event.choice) continue;
    const topic = String(event.meta?.helpTopic ?? 'unknown');
    out.push({
      topic,
      topicLabel: HELP_TOPIC_LABELS[topic] ?? topic,
      choice: event.choice,
    });
  }
  return out;
}

function analyzeAttempt(attempt, problemLabel) {
  const events = attempt.session_log?.events ?? [];
  const misses = missesFromEvents(events, attempt.attempt_items);
  return {
    attemptId: attempt.id,
    problemLabel,
    problemId: attempt.problem_id,
    status: attempt.status,
    score: attempt.score,
    maxScore: attempt.max_score,
    misses,
    badges: groupMissesIntoBadges(misses),
    helpFeedback: helpFeedbackFromEvents(events),
  };
}

async function loadStudent(student) {
  const gpUrl = `${baseUrl}/rest/v1/attempts?student_id=eq.${student.id}&activity_id=eq.matrix/guided-practice&select=${GP_SELECT}&order=started_at.asc`;
  const svUrl = `${baseUrl}/rest/v1/attempts?student_id=eq.${student.id}&activity_id=eq.matrix/guided-practice-survey&select=${SV_SELECT}&order=completed_at.desc`;
  const [guidedPractice, surveyAttempts] = await Promise.all([
    fetchJson(gpUrl),
    fetchJson(svUrl),
  ]);
  const slots = problemSlotsFromAttempts(guidedPractice);

  const problems = [];
  if (slots.problem1.attempt) {
    problems.push(analyzeAttempt(slots.problem1.attempt, 'Problem 1'));
  }
  if (slots.problem2.attempt) {
    problems.push(analyzeAttempt(slots.problem2.attempt, 'Problem 2'));
  }

  const allMisses = problems.flatMap((p) =>
    p.misses.map((m) => ({ ...m, problemLabel: p.problemLabel, problemId: p.problemId })),
  );

  return {
    id: student.id,
    name: student.name,
    survey: surveyFromAttempts(surveyAttempts),
    problems,
    missCount: allMisses.length,
    categoryCounts: countByCategory(allMisses),
    badges: groupMissesIntoBadges(allMisses),
  };
}

function countByCategory(misses) {
  const counts = {};
  for (const miss of misses) {
    counts[miss.category] = (counts[miss.category] ?? 0) + 1;
  }
  return counts;
}

function buildClassAggregates(students) {
  const missByCategory = {};
  const missByStudent = [];
  const surveyAgg = { q1: {}, q2: {}, q3: {}, responses: 0, openFeedback: [] };
  const helpFeedbackAgg = {};

  for (const student of students) {
    if (student.missCount > 0) {
      missByStudent.push({
        name: student.name,
        missCount: student.missCount,
        categories: student.categoryCounts,
      });
    }

    for (const [category, count] of Object.entries(student.categoryCounts)) {
      missByCategory[category] = (missByCategory[category] ?? 0) + count;
    }

    if (student.survey) {
      surveyAgg.responses += 1;
      const mcq = student.survey.answers.slice(0, 3);
      mcq.forEach((row, index) => {
        const key = `q${index + 1}`;
        surveyAgg[key][row.value] = (surveyAgg[key][row.value] ?? 0) + 1;
      });
      const open = student.survey.answers[3]?.value;
      if (open && open !== '—') {
        surveyAgg.openFeedback.push({ name: student.name, text: open });
      }
    }

    for (const problem of student.problems) {
      for (const fb of problem.helpFeedback) {
        const key = fb.topicLabel;
        if (!helpFeedbackAgg[key]) helpFeedbackAgg[key] = {};
        helpFeedbackAgg[key][fb.choice] = (helpFeedbackAgg[key][fb.choice] ?? 0) + 1;
      }
    }
  }

  const rankedMisses = aggregateCategoryOrder()
    .map((category) => ({
      category,
      label: BADGE_LABELS[category],
      description: BADGE_DESCRIPTIONS[category],
      count: missByCategory[category] ?? 0,
    }))
    .filter((row) => row.count > 0)
    .sort((a, b) => b.count - a.count);

  missByStudent.sort((a, b) => b.missCount - a.missCount);

  const instancesByCategory = {};
  for (const student of students) {
    for (const problem of student.problems) {
      for (const miss of problem.misses) {
        if (!instancesByCategory[miss.category]) {
          instancesByCategory[miss.category] = [];
        }
        instancesByCategory[miss.category].push({
          studentName: student.name,
          problemLabel: problem.problemLabel,
          problemId: problem.problemId,
          tryCount: miss.tryCount,
          wrongChoices: miss.wrongChoices,
          expectedAnswer: miss.expectedAnswer,
        });
      }
    }
  }

  return {
    missByCategory: rankedMisses,
    missByStudent,
    instancesByCategory,
    survey: surveyAgg,
    helpFeedback: helpFeedbackAgg,
    studentsWithData: students.filter((s) => s.problems.length > 0).length,
  };
}

const SHARED_CSS = `
  :root {
    --ink: #13243a;
    --soft: #5a6b80;
    --line: #d6dee8;
    --bg: #f6f8fb;
    --card: #ffffff;
    --red: #b42318;
    --redbg: #fef3f2;
    --green: #15803d;
    --greenbg: #f0fdf4;
    --blue: #1d4ed8;
    --bluebg: #eff4ff;
    --amber: #b54708;
    --amberbg: #fffaeb;
  }
  * { box-sizing: border-box; }
  body {
    font: 17px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif;
    color: var(--ink);
    background: var(--bg);
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px 24px 80px;
  }
  a { color: var(--blue); }
  .backlink, .nav-pill {
    display: inline-block;
    padding: 14px 22px;
    background: #fff;
    border: 2px solid var(--line);
    border-radius: 12px;
    font-weight: 600;
    text-decoration: none;
    color: var(--ink);
    margin: 0 8px 8px 0;
    min-height: 3rem;
  }
  .nav-pill.active { border-color: #2563eb; background: var(--bluebg); box-shadow: 0 0 0 3px #bfdbfe; }
  h1 { font-size: 32px; margin: 0 0 8px; }
  .sub { color: var(--soft); font-size: 18px; margin: 0 0 24px; }
  .banner {
    background: var(--amberbg);
    border: 2px solid #fec84b;
    border-radius: 14px;
    padding: 16px 20px;
    margin: 0 0 24px;
    font-size: 16px;
    color: #7a2e0e;
  }
  .card {
    background: var(--card);
    border: 2px solid var(--line);
    border-radius: 16px;
    padding: 20px 22px;
    margin: 0 0 16px;
  }
  .card h2, .card h3 { margin: 0 0 10px; line-height: 1.25; }
  .card h2 { font-size: 24px; }
  .card h3 { font-size: 20px; }
  .pill {
    display: inline-block;
    font: 700 12px/1 system-ui, sans-serif;
    padding: 6px 10px;
    border-radius: 999px;
    margin: 0 6px 6px 0;
  }
  .pill-bad { background: var(--redbg); color: var(--red); border: 1.5px solid #fda29b; }
  .pill-info { background: var(--bluebg); color: var(--blue); border: 1.5px solid #c7d7fe; }
  .pill-ok { background: var(--greenbg); color: var(--green); border: 1.5px solid #a6f4c5; }
  .student-nav {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 12px;
    align-items: center;
    margin: 0 0 20px;
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
  .student-name { text-align: center; font-size: 28px; font-weight: 800; margin: 0; }
  .student-sub { text-align: center; color: var(--soft); margin: 4px 0 0; }
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
  .tab-sub { display: block; font-weight: 400; font-size: 13px; color: var(--soft); margin-top: 4px; }
  .miss-card ul { margin: 8px 0 0; padding-left: 22px; }
  .miss-card li { margin-bottom: 6px; }
  .miss-card code {
    background: #e9eef5;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.92em;
  }
  .empty {
    border: 2px dashed var(--line);
    border-radius: 16px;
    padding: 28px;
    text-align: center;
    color: var(--soft);
  }
  .bar-row { display: grid; grid-template-columns: 1fr 3fr 60px; gap: 12px; align-items: center; margin: 0 0 10px; }
  .bar-track { background: #e9eef5; border-radius: 8px; height: 28px; overflow: hidden; }
  .bar-fill { background: #2563eb; height: 100%; border-radius: 8px; min-width: 4px; }
  table.simple { width: 100%; border-collapse: collapse; font-size: 15px; }
  table.simple th, table.simple td { border: 1.5px solid var(--line); padding: 10px 12px; text-align: left; vertical-align: top; }
  table.simple th { background: #f9fafb; }
  .survey-row { border: 2px solid var(--line); border-radius: 12px; padding: 14px 16px; margin: 0 0 10px; background: #fbfcfe; }
  .survey-row .q { font-weight: 700; margin: 0 0 6px; }
  .survey-row .a { margin: 0; white-space: pre-wrap; }
  .badge-row { display: flex; flex-wrap: wrap; gap: 12px; margin: 0 0 20px; }
  .miss-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 16px 20px;
    min-height: 3.5rem;
    font: 700 17px system-ui, sans-serif;
    background: #fff;
    border: 2px solid var(--line);
    border-radius: 14px;
    cursor: pointer;
    color: var(--ink);
  }
  .miss-badge:hover { border-color: #94a3b8; }
  .miss-badge.active {
    border-color: #2563eb;
    background: var(--bluebg);
    box-shadow: 0 0 0 3px #bfdbfe;
  }
  .miss-badge .count {
    font-size: 15px;
    color: var(--red);
    background: var(--redbg);
    border: 1.5px solid #fda29b;
    border-radius: 999px;
    padding: 4px 10px;
  }
  .badge-detail {
    background: #fff;
    border: 3px solid #2563eb;
    border-radius: 16px;
    padding: 20px 22px;
    margin: 0 0 20px;
  }
  .badge-detail[hidden] { display: none !important; }
  .badge-detail h3 { margin: 0 0 6px; font-size: 22px; }
  .badge-detail .desc { color: var(--soft); margin: 0 0 16px; }
  .instance {
    border: 2px solid var(--line);
    border-radius: 12px;
    padding: 14px 16px;
    margin: 0 0 10px;
    background: #fbfcfe;
  }
  .instance .who { font-weight: 700; margin: 0 0 8px; }
  .compare { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  .compare-box {
    border: 2px solid var(--line);
    border-radius: 10px;
    padding: 12px 14px;
    background: #fff;
  }
  .compare-box.bad { border-color: #fda29b; background: var(--redbg); }
  .compare-box.good { border-color: #a6f4c5; background: var(--greenbg); }
  .compare-box .label {
    font: 700 11px/1 system-ui, sans-serif;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--soft);
    margin: 0 0 6px;
  }
  .compare-box .value {
    margin: 0;
    font-family: ui-monospace, Consolas, monospace;
    font-size: 15px;
    word-break: break-word;
  }
  .student-badge-summary { display: flex; flex-wrap: wrap; gap: 8px; margin: 0; }
  .student-badge-summary span {
    font-size: 14px;
    padding: 6px 10px;
    border-radius: 8px;
    background: #f2f4f7;
    border: 1.5px solid var(--line);
  }
`;

function esc(text) {
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function buildStudentHtml(students) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Guided practice — miss badges by student</title>
<style>${SHARED_CSS}</style>
</head>
<body>
<a class="backlink" href="/pages.html">&larr; All pages</a>
<a class="nav-pill" href="/scratch/guided-practice-miss-aggregate.html">Class aggregate &amp; survey</a>

<div class="banner"><strong>Miss badges.</strong> Seven categories. Click a badge to see what they typed vs the answer.</div>
<h1>Miss badges by student</h1>
<p class="sub">Survey on top, combined badges, then Problem 1 / Problem 2 tabs. Each badge is &times;how many times they missed that skill.</p>

<div class="student-nav">
  <button type="button" id="prev-student">&larr; Previous</button>
  <div><p class="student-name" id="student-name"></p><p class="student-sub" id="student-sub"></p></div>
  <button type="button" id="next-student" style="justify-self:end">Next &rarr;</button>
</div>

<section class="card" id="survey-section">
  <h2>Post-practice survey</h2>
  <div id="survey-body"></div>
</section>

<section class="card">
  <h2>All problems combined</h2>
  <p class="sub" style="margin:0 0 12px">Badge totals across Problem 1 and Problem 2.</p>
  <div class="badge-row" id="student-all-badges"></div>
</section>

<div class="problem-tabs">
  <button type="button" id="tab-p1">Problem 1<span class="tab-sub" id="tab-p1-sub"></span></button>
  <button type="button" id="tab-p2">Problem 2<span class="tab-sub" id="tab-p2-sub"></span></button>
</div>

<div class="badge-row" id="badge-row"></div>
<div class="badge-detail" id="badge-detail" hidden></div>
<div id="miss-empty"></div>

<script type="application/json" id="students-data">${JSON.stringify(students)}</script>
<script>
(function () {
  var STUDENTS = JSON.parse(document.getElementById('students-data').textContent);
  var withData = STUDENTS.filter(function (s) { return s.problems.length > 0; });
  var idx = 0;
  var tab = 0;
  var openBadge = null;
  var openScope = 'problem';

  function fmtTime(iso) {
    if (!iso) return '';
    var d = new Date(iso);
    return isNaN(d) ? iso : d.toLocaleString(undefined, { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' });
  }

  function esc(s) {
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  function renderSurvey(student) {
    var body = document.getElementById('survey-body');
    if (!student.survey) {
      body.innerHTML = '<p class="empty" style="margin:0">No survey yet.</p>';
      return;
    }
    body.innerHTML = '<p style="color:#5a6b80;margin:0 0 12px">Completed ' + fmtTime(student.survey.completedAt) + '</p>' +
      student.survey.answers.map(function (row) {
        return '<div class="survey-row"><p class="q">' + esc(row.label) + '</p><p class="a">' + esc(row.value) + '</p></div>';
      }).join('');
  }

  function instanceHtml(inst, showProblem) {
    var wrongText = inst.wrongChoices.map(function (w) {
      return 'Try ' + w.attemptIndex + ': ' + w.choice;
    }).join('; ');
    var header = showProblem
      ? esc(inst.problemLabel || '') + ' · problem ' + inst.problemId
      : 'Miss';
    return '<div class="instance"><p class="who">' + header + (inst.tryCount > 1 ? ' · ' + inst.tryCount + ' tries' : '') + '</p>' +
      '<div class="compare"><div class="compare-box bad"><p class="label">They wrote</p><p class="value">' + esc(wrongText || '—') + '</p></div>' +
      '<div class="compare-box good"><p class="label">Answer</p><p class="value">' + esc(inst.expectedAnswer || '—') + '</p></div></div></div>';
  }

  function renderBadgeDetail(badge, scope) {
    var panel = document.getElementById('badge-detail');
    if (!badge) { panel.hidden = true; panel.innerHTML = ''; return; }
    panel.hidden = false;
    panel.innerHTML = '<h3>' + esc(badge.badgeLabel) + ' <span class="count">×' + badge.count + '</span></h3>' +
      '<p class="desc">' + esc(badge.description) + '</p>' +
      badge.instances.map(function (inst) { return instanceHtml(inst, scope === 'all'); }).join('');
  }

  function wireBadges(container, badges, scope) {
    container.innerHTML = badges.map(function (badge) {
      var active = openScope === scope && openBadge === badge.category;
      return '<button type="button" class="miss-badge' + (active ? ' active' : '') + '" data-category="' + esc(badge.category) + '" data-scope="' + scope + '">' +
        esc(badge.badgeLabel) + ' <span class="count">×' + badge.count + '</span></button>';
    }).join('');
    container.querySelectorAll('.miss-badge').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var cat = btn.getAttribute('data-category');
        var sc = btn.getAttribute('data-scope');
        var list = sc === 'all' ? withData[idx].badges : ((withData[idx].problems[tab] && withData[idx].problems[tab].badges) || []);
        var badge = list.find(function (b) { return b.category === cat; });
        if (openBadge === cat && openScope === sc) { openBadge = null; renderBadgeDetail(null); }
        else { openBadge = cat; openScope = sc; renderBadgeDetail(badge, sc); }
        render();
      });
    });
  }

  function renderMisses(student) {
    var problem = student.problems[tab];
    var badgeRow = document.getElementById('badge-row');
    var empty = document.getElementById('miss-empty');
    wireBadges(document.getElementById('student-all-badges'), student.badges || [], 'all');
    if (!problem) {
      badgeRow.innerHTML = '';
      empty.innerHTML = '<div class="empty">No attempt in this slot yet.</div>';
      if (openScope === 'problem') renderBadgeDetail(null);
      return;
    }
    if (!problem.badges.length) {
      badgeRow.innerHTML = '';
      empty.innerHTML = '<div class="empty">No misses on ' + esc(problem.problemLabel) + ' — every step correct on first try.</div>';
      if (openScope === 'problem') renderBadgeDetail(null);
      return;
    }
    empty.innerHTML = '';
    wireBadges(badgeRow, problem.badges, 'problem');
    if (openScope === 'problem' && openBadge) {
      renderBadgeDetail(problem.badges.find(function (b) { return b.category === openBadge; }), 'problem');
    } else if (openScope === 'all' && openBadge) {
      renderBadgeDetail(student.badges.find(function (b) { return b.category === openBadge; }), 'all');
    }
  }

  function updateTabs(student) {
    ['Problem 1', 'Problem 2'].forEach(function (label, i) {
      var btn = document.getElementById(i === 0 ? 'tab-p1' : 'tab-p2');
      var sub = document.getElementById(i === 0 ? 'tab-p1-sub' : 'tab-p2-sub');
      var problem = student.problems[i];
      btn.classList.toggle('active', tab === i);
      if (!problem) {
        sub.textContent = 'No attempt';
        return;
      }
      sub.textContent = problem.problemLabel + ' · problem ' + problem.problemId + ' · ' + problem.misses.length + ' badge' + (problem.misses.length === 1 ? '' : 's');
    });
  }

  function render() {
    if (!withData.length) {
      document.getElementById('student-name').textContent = 'No student data yet';
      return;
    }
    var student = withData[idx];
    document.getElementById('student-name').textContent = student.name;
    document.getElementById('student-sub').textContent = (idx + 1) + ' of ' + withData.length + ' with attempts';
    document.getElementById('prev-student').disabled = idx === 0;
    document.getElementById('next-student').disabled = idx >= withData.length - 1;
    renderSurvey(student);
    updateTabs(student);
    renderMisses(student);
  }

  document.getElementById('prev-student').addEventListener('click', function () { if (idx > 0) { idx -= 1; tab = 0; openBadge = null; render(); } });
  document.getElementById('next-student').addEventListener('click', function () { if (idx < withData.length - 1) { idx += 1; tab = 0; openBadge = null; render(); } });
  document.getElementById('tab-p1').addEventListener('click', function () { tab = 0; openBadge = null; openScope = 'problem'; render(); });
  document.getElementById('tab-p2').addEventListener('click', function () { tab = 1; openBadge = null; openScope = 'problem'; render(); });
  render();
})();
</script>
</body>
</html>`;
}

function buildAggregateHtml(aggregates, students) {
  const classBadges = aggregates.missByCategory.map((row) => ({
    category: row.category,
    badgeLabel: row.label,
    description: row.description,
    count: row.count,
  }));

  const studentRows = aggregates.missByStudent
    .map((row) => {
      const badges = Object.entries(row.categories)
        .sort((a, b) => b[1] - a[1])
        .map(([cat, n]) => `<span>${esc(BADGE_LABELS[cat] ?? cat)} ×${n}</span>`)
        .join('');
      return `<tr><td>${esc(row.name)}</td><td>${row.missCount}</td><td><div class="student-badge-summary">${badges || '—'}</div></td></tr>`;
    })
    .join('');

  const surveyMcq = ['q1', 'q2', 'q3'].map((key, i) => {
    const counts = aggregates.survey[key] ?? {};
    const parts = Object.entries(counts)
      .map(([label, n]) => `${label}: ${n}`)
      .join(' · ');
    return `<div class="survey-row"><p class="q">${esc(SURVEY_LABELS[i])}</p><p class="a">${esc(parts || '—')}</p></div>`;
  }).join('');

  const openFeedback = aggregates.survey.openFeedback
    .map(
      (row) =>
        `<div class="survey-row"><p class="q">${esc(row.name)}</p><p class="a">${esc(row.text)}</p></div>`,
    )
    .join('');

  const helpRows = Object.entries(aggregates.helpFeedback)
    .map(([topic, counts]) => {
      const parts = Object.entries(counts)
        .map(([choice, n]) => `${choice}: ${n}`)
        .join(' · ');
      return `<tr><td>${esc(topic)}</td><td>${esc(parts || '—')}</td></tr>`;
    })
    .join('');

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Guided practice — class aggregate</title>
<style>${SHARED_CSS}</style>
</head>
<body>
<a class="backlink" href="/pages.html">&larr; All pages</a>
<a class="nav-pill" href="/scratch/guided-practice-miss-student.html">Per-student misses</a>

<div class="banner"><strong>Class-wide badges.</strong> Click a badge to see every miss instance — who, what they wrote, and the answer.</div>
<h1>Class miss badges</h1>
<p class="sub">${aggregates.studentsWithData} students with guided-practice attempts · ${students.filter((s) => s.survey).length} surveys</p>

<section class="card">
  <h2>Class miss badges (all students, both problems)</h2>
  <p style="color:var(--soft);margin:0 0 16px">Each badge counts one miss on one problem. Click to expand.</p>
  <div class="badge-row" id="class-badge-row"></div>
  <div class="badge-detail" id="class-badge-detail" hidden></div>
</section>

<section class="card">
  <h2>Badges by student</h2>
  <table class="simple">
    <thead><tr><th>Student</th><th>Total badges</th><th>Breakdown</th></tr></thead>
    <tbody>${studentRows || '<tr><td colspan="3">No data</td></tr>'}</tbody>
  </table>
</section>

<section class="card">
  <h2>Post-practice survey (${aggregates.survey.responses} responses)</h2>
  ${surveyMcq}
  ${openFeedback ? '<h3 style="margin:20px 0 10px">Open feedback</h3>' + openFeedback : ''}
</section>

<section class="card">
  <h2>Mini-tutorial help — “Did this help?”</h2>
  <p style="color:var(--soft);margin:0 0 12px">Aggregated Yes / Kinda / No from fraction help and row-notation help prompts.</p>
  <table class="simple">
    <thead><tr><th>Help topic</th><th>Responses</th></tr></thead>
    <tbody>${helpRows || '<tr><td colspan="2">No help feedback yet.</td></tr>'}</tbody>
  </table>
</section>

<script type="application/json" id="aggregate-data">${JSON.stringify({ classBadges, instancesByCategory: aggregates.instancesByCategory })}</script>
<script>
(function () {
  var DATA = JSON.parse(document.getElementById('aggregate-data').textContent);
  var openBadge = null;

  function esc(s) {
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  function instanceHtml(inst) {
    var wrongText = inst.wrongChoices.map(function (w) {
      return 'Try ' + w.attemptIndex + ': ' + w.choice;
    }).join('; ');
    return '<div class="instance"><p class="who">' + esc(inst.studentName) + ' · ' + esc(inst.problemLabel) + ' · problem ' + inst.problemId + '</p>' +
      '<div class="compare"><div class="compare-box bad"><p class="label">They wrote</p><p class="value">' + esc(wrongText || '—') + '</p></div>' +
      '<div class="compare-box good"><p class="label">Answer</p><p class="value">' + esc(inst.expectedAnswer || '—') + '</p></div></div></div>';
  }

  function renderDetail(category) {
    var panel = document.getElementById('class-badge-detail');
    if (!category) { panel.hidden = true; panel.innerHTML = ''; return; }
    var badge = DATA.classBadges.find(function (b) { return b.category === category; });
    var instances = DATA.instancesByCategory[category] || [];
    panel.hidden = false;
    panel.innerHTML = '<h3>' + esc(badge.badgeLabel) + ' <span class="count">×' + badge.count + '</span></h3>' +
      '<p class="desc">' + esc(badge.description) + '</p>' +
      instances.map(instanceHtml).join('');
  }

  function render() {
    var row = document.getElementById('class-badge-row');
    row.innerHTML = DATA.classBadges.map(function (badge) {
      var active = openBadge === badge.category;
      return '<button type="button" class="miss-badge' + (active ? ' active' : '') + '" data-category="' + esc(badge.category) + '">' +
        esc(badge.badgeLabel) + ' <span class="count">×' + badge.count + '</span></button>';
    }).join('');
    row.querySelectorAll('.miss-badge').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var cat = btn.getAttribute('data-category');
        openBadge = openBadge === cat ? null : cat;
        renderDetail(openBadge);
        render();
      });
    });
  }

  render();
})();
</script>

</body>
</html>`;
}

const roster = loadRoster();
console.log(`Loading ${roster.length} roster students…`);

const students = [];
for (const student of roster) {
  const loaded = await loadStudent(student);
  if (loaded.problems.length > 0) {
    students.push(loaded);
    console.log(`  ${student.name}: ${loaded.missCount} misses across ${loaded.problems.length} problem(s)`);
  }
}

students.sort((a, b) => a.name.localeCompare(b.name));
const aggregates = buildClassAggregates(students);

const studentHtml = buildStudentHtml(students);
const aggregateHtml = buildAggregateHtml(aggregates, students);

const studentPath = path.join(dir, 'guided-practice-miss-student.html');
const aggregatePath = path.join(dir, 'guided-practice-miss-aggregate.html');
fs.writeFileSync(studentPath, studentHtml, 'utf8');
fs.writeFileSync(aggregatePath, aggregateHtml, 'utf8');
fs.writeFileSync(path.join(dir, 'guided-practice-miss-data.json'), JSON.stringify({ students, aggregates }, null, 2));

console.log('\nWrote:');
console.log('  http://127.0.0.1:8765/scratch/guided-practice-miss-student.html');
console.log('  http://127.0.0.1:8765/scratch/guided-practice-miss-aggregate.html');
