/**
 * Cursor postToolUse hook — append tool-use counts to the session scorecard running tally.
 * Stdin: hook JSON (tool_name, tool_input, …). Always exits 0 (fail open).
 *
 * Manual smoke test:
 *   echo {"tool_name":"Read","tool_input":{"path":"foo.ts"}} | node scripts/scorecard-hook-tally.js
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const RUNNING = path.join(ROOT, 'agent docs', '.session-scorecard-running.json');
const MDC_STATS = path.join(ROOT, 'agent docs', 'mdc-read-stats.json');

const DOC_EXT = new Set(['.md', '.mdc', '.html', '.json', '.jsonl', '.txt']);
const SEARCH_TOOLS = new Set(['Grep', 'Glob', 'WebSearch']);
const READ_TOOLS = new Set(['Read']);
const EDIT_TOOLS = new Set(['Write', 'StrReplace', 'Delete', 'EditNotebook']);
const SHELL_TOOLS = new Set(['Shell']);

function mergeUnique(list, add) {
  const set = new Set(list || []);
  for (const x of add || []) {
    if (x) {
      set.add(x);
    }
  }
  return [...set];
}

function emptyRunning() {
  return {
    sessionStarted: new Date().toISOString(),
    model: '',
    sessionType: 'mixed',
    summaryHuman: 'Session in progress…',
    turns: 0,
    greps: 0,
    corrections: 0,
    docsRulesOpened: [],
    mdcReadsList: [],
    filesReadList: [],
    filesEditedList: [],
    taskLog: [],
    hookTally: false,
    agentBumped: false,
  };
}

function readRunning() {
  if (!fs.existsSync(RUNNING)) {
    return null;
  }
  try {
    return JSON.parse(fs.readFileSync(RUNNING, 'utf8'));
  } catch {
    return null;
  }
}

function writeRunning(data) {
  const dir = path.dirname(RUNNING);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(RUNNING, JSON.stringify(data, null, 2), 'utf8');
}

function normalizePath(raw) {
  if (!raw || typeof raw !== 'string') {
    return null;
  }
  return raw.replace(/\\/g, '/');
}

function isDocRulePath(filePath) {
  const normalized = normalizePath(filePath);
  if (!normalized) {
    return false;
  }
  const lower = normalized.toLowerCase();
  const ext = path.extname(lower);
  if (DOC_EXT.has(ext)) {
    return true;
  }
  return (
    lower.includes('/.cursor/rules/')
    || lower.includes('/agent docs/')
    || lower.includes('/docs/')
    || lower.includes('/cursor-patterns/')
  );
}

function isMdcPath(filePath) {
  const normalized = normalizePath(filePath);
  if (!normalized) {
    return false;
  }
  return path.extname(normalized.toLowerCase()) === '.mdc';
}

function mdcLabel(filePath) {
  return path.basename(String(filePath || '').replace(/\\/g, '/'));
}

function bumpLifetimeMdcStats(filePath) {
  if (!isMdcPath(filePath)) {
    return;
  }
  const key = mdcLabel(filePath);
  let stats = {};
  if (fs.existsSync(MDC_STATS)) {
    try {
      stats = JSON.parse(fs.readFileSync(MDC_STATS, 'utf8'));
    } catch {
      stats = {};
    }
  }
  const row = stats[key] || { count: 0, last: null, lastPath: null };
  row.count += 1;
  row.last = new Date().toISOString();
  row.lastPath = normalizePath(filePath);
  stats[key] = row;
  fs.writeFileSync(MDC_STATS, JSON.stringify(stats, null, 2), 'utf8');
}

function pickPath(toolInput) {
  if (!toolInput || typeof toolInput !== 'object') {
    return null;
  }
  return normalizePath(
    toolInput.path
    || toolInput.file_path
    || toolInput.target_path
    || toolInput.target_notebook
  );
}

function recordToolUse(payload) {
  const toolName = String(payload.tool_name || payload.toolName || '').trim();
  if (!toolName) {
    return;
  }

  const toolInput = payload.tool_input || payload.toolInput || payload.arguments || {};
  const running = readRunning() || emptyRunning();
  running.hookTally = true;

  if (SEARCH_TOOLS.has(toolName)) {
    running.greps += 1;
  } else if (SHELL_TOOLS.has(toolName)) {
    running.greps += 1;
  } else if (READ_TOOLS.has(toolName)) {
    const filePath = pickPath(toolInput);
    if (filePath) {
      running.filesReadList = mergeUnique(running.filesReadList, [filePath]);
      if (isDocRulePath(filePath)) {
        running.docsRulesOpened = mergeUnique(running.docsRulesOpened, [filePath]);
      }
      if (isMdcPath(filePath)) {
        running.mdcReadsList = mergeUnique(running.mdcReadsList, [filePath]);
        bumpLifetimeMdcStats(filePath);
      }
    }
  } else if (EDIT_TOOLS.has(toolName)) {
    const filePath = pickPath(toolInput);
    if (filePath) {
      running.filesEditedList = mergeUnique(running.filesEditedList, [filePath]);
      if (isDocRulePath(filePath)) {
        running.docsRulesOpened = mergeUnique(running.docsRulesOpened, [filePath]);
      }
    }
  } else {
    return;
  }

  writeRunning(running);
}

function main() {
  const chunks = [];
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', (chunk) => chunks.push(chunk));
  process.stdin.on('end', () => {
    try {
      const raw = chunks.join('').trim();
      if (!raw) {
        process.exit(0);
        return;
      }
      recordToolUse(JSON.parse(raw));
    } catch {
      // Fail open — never block the agent on tally errors.
    }
    process.exit(0);
  });
}

main();
