/**
 * FILE: scripts/scorecard-enforce.js
 * PURPOSE: Force scorecard bumps to actually happen, instead of relying on the agent
 *          remembering an always-on prose instruction (which was the failure Chase hit —
 *          a whole session with real edits and zero bumps).
 *
 * Three modes, one script so the "is there unbumped work" check has one home:
 *   --stop        Stop hook. When there is clear evidence of unbumped work, writes the
 *                 bump itself (autoBump) instead of blocking the agent.
 *   --context-warning  UserPromptSubmit hook. Counts messages per chat and, once the
 *                 task is heavy (real context size in Claude Code, message count in
 *                 Cursor), injects a reminder to recommend a momentum handoff after
 *                 the current deliverable.
 *   --precompact  PreCompact hook. Non-blocking (Stop is the only hook here allowed to
 *                 block). Injects a reminder before compaction, since the running-tally
 *                 counts already survive compaction (written to disk on every tool call)
 *                 but the agent's memory that it needs to bump does not.
 *
 * Fails open on every path: missing file, unparsable JSON, write error, unknown mode.
 * A bug in this script must never be the reason Chase can't get a response.
 *
 * Manual smoke test:
 *   echo '{}' | node scripts/scorecard-enforce.js --stop
 *   echo '{}' | node scripts/scorecard-enforce.js --context-warning
 *   echo '{}' | node scripts/scorecard-enforce.js --precompact
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const { resolveChat, recordPrompt, updateChat } = require('./chat-task');
const {
  HEAVY_CONTEXT_TOKENS,
  readLatestContextTokens,
  formatTokens,
} = require('./session-token-cost');
const { estimateContextGrowth, HEAVY_GROWTH_TOKENS } = require('./context-growth-estimate');

const ROOT = path.join(__dirname, '..');
const RUNNING = path.join(ROOT, 'agent docs', '.session-scorecard-running.json');

const MIN_TURNS = 3;
const MIN_EDITED_FILES = 2;
// Cursor transcripts carry no token usage, so there the heavy test is the estimate in
// context-growth-estimate.js. Twelve messages is only the fallback when the transcript
// is unreadable. On every host it is also the minimum gap between repeat warnings.
const CONTEXT_WARNING_TURN_INTERVAL = 12;

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
  try {
    fs.writeFileSync(RUNNING, JSON.stringify(data, null, 2), 'utf8');
  } catch {
    // Fail open — a write failure must never be why a turn gets blocked.
  }
}

function unbumpedState(running) {
  const edited = Array.isArray(running.filesEditedList) ? running.filesEditedList.length : 0;
  const bumps = Array.isArray(running.taskLog) ? running.taskLog.length : 0;
  const turns = Number(running.turns) || 0;
  return { edited, bumps, turns, looksUnbumped: edited >= MIN_EDITED_FILES && bumps === 0 };
}

function printAndExit(obj) {
  process.stdout.write(JSON.stringify(obj || {}));
  process.exit(0);
}

// Stop hook: never blocks. When the session shows real edits and no bump, write the bump
// here (flagged autoBump) so the failure this existed for, a whole session of edits with
// zero rows, is covered without forcing the agent to spend extra turns on it.
function runStop() {
  const running = readRunning();
  if (!running) {
    return printAndExit();
  }

  const { edited, turns, looksUnbumped } = unbumpedState(running);
  if (!looksUnbumped || turns < MIN_TURNS) {
    return printAndExit();
  }

  const names = running.filesEditedList.map((f) => String(f).split(/[\\/]/).pop());
  const shown = names.slice(0, 5).join(', ') + (names.length > 5 ? `, +${names.length - 5} more` : '');
  spawnSync(
    process.execPath,
    [path.join(__dirname, 'append-session-scorecard.js'), '--auto', '--note', `Auto: ${edited} files edited (${shown})`],
    { cwd: ROOT, timeout: 8000, stdio: 'ignore' },
  );
  return printAndExit();
}

function runPrecompact() {
  const running = readRunning();
  if (!running) return printAndExit();

  const { edited, bumps } = unbumpedState(running);
  const trackingReminder = edited > 0 && bumps === 0
    ? ` ${edited} file(s) have been edited with 0 session tracking bumps logged; run `
      + 'node scripts/append-session-scorecard.js --note "<what you finished>" before detail '
      + 'gets summarized away.'
    : '';

  printAndExit({
    hookSpecificOutput: {
      hookEventName: 'PreCompact',
      additionalContext:
        'CONTEXT EFFICIENCY WARNING: Compaction is about to summarize this conversation. '
        + 'Tell Chase plainly in your next response that this task has become context-heavy, '
        + 'finish the current deliverable, and recommend that he say "perform a momentum handoff" '
        + `before starting another major chunk in a fresh task.${trackingReminder}`,
    },
  });
}

function readStdinJson() {
  try {
    const raw = fs.readFileSync(0, 'utf8').trim();
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

// Counts are per chat (scripts/chat-task.js), so a fresh task after a handoff starts
// at zero. Where the transcript has real usage (Claude Code) the trigger is the context
// the latest reply re-read; Cursor has none, so there it is messages in this chat.
function runContextWarning() {
  const { chatKey, transcriptPath } = resolveChat(readStdinJson());
  if (!chatKey) return printAndExit();

  const chat = recordPrompt(chatKey);
  const context = readLatestContextTokens(transcriptPath);
  // No usage in the transcript (Cursor, Codex): estimate growth from tool calls and words
  // written. Messages alone are the last resort, when the transcript cannot be read.
  const estimate = context === null ? estimateContextGrowth(transcriptPath) : null;
  const heavy = context !== null
    ? context >= HEAVY_CONTEXT_TOKENS
    : estimate !== null
      ? estimate.growth >= HEAVY_GROWTH_TOKENS
      : chat.prompts >= CONTEXT_WARNING_TURN_INTERVAL;
  const warnedRecently = chat.lastWarnedAtPrompt > 0
    && chat.prompts - chat.lastWarnedAtPrompt < CONTEXT_WARNING_TURN_INTERVAL;
  if (!heavy || warnedRecently) return printAndExit();

  updateChat(chatKey, (row) => ({ ...row, lastWarnedAtPrompt: chat.prompts }));
  const measure = context !== null
    ? `Each reply in this task now re-reads about ${formatTokens(context)} tokens of context `
      + '(a fresh task starts near 60k-90k). '
    : estimate !== null
      ? `This task has made about ${estimate.toolCalls} tool calls and its context has grown by an `
        + `estimated ${formatTokens(estimate.growth)} tokens. `
      : `This task has reached ${chat.prompts} messages from Chase. `;
  printAndExit({
    hookSpecificOutput: {
      hookEventName: 'UserPromptSubmit',
      additionalContext:
        `CONTEXT EFFICIENCY WARNING: ${measure}`
        + 'Tell Chase plainly in your next response that continued unrelated or major work here '
        + 'will drag more context through each turn. Finish the current deliverable, then recommend '
        + 'that he say "perform a momentum handoff" before starting a fresh task. Do not '
        + 'interrupt unfinished work or create or switch tasks automatically.',
    },
  });
}

function main() {
  try {
    if (process.argv.includes('--stop')) {
      return runStop();
    }
    if (process.argv.includes('--precompact')) {
      return runPrecompact();
    }
    if (process.argv.includes('--context-warning')) {
      return runContextWarning();
    }
    printAndExit();
  } catch {
    // Fail open — never block, never crash the hook chain.
    try {
      printAndExit();
    } catch {
      process.exit(0);
    }
  }
}

main();
