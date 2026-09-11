/**
 * FILE: scripts/scorecard-enforce.js
 * PURPOSE: Force scorecard bumps to actually happen, instead of relying on the agent
 *          remembering an always-on prose instruction (which was the failure Chase hit —
 *          a whole session with real edits and zero bumps).
 *
 * Two modes, one script so the "is there unbumped work" check has one home:
 *   --stop        Stop hook. Blocks the agent from ending its turn when there's clear
 *                 evidence of unbumped work. Capped at MAX_BLOCKS consecutive blocks,
 *                 then force-allows — this can never trap the session.
 *   --context-warning  UserPromptSubmit hook. At a named turn interval, injects a
 *                 reminder that the agent must recommend a fresh task after the current
 *                 deliverable and provide a copy-ready handoff summary.
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

const ROOT = path.join(__dirname, '..');
const RUNNING = path.join(ROOT, 'agent docs', '.session-scorecard-running.json');

const MIN_TURNS = 3;
const MIN_EDITED_FILES = 2;
const MAX_BLOCKS = 3;
// Exact live token totals are not available on every host. Twelve user messages catches
// context-heavy iterative work before compaction without interrupting short tasks.
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

function runStop() {
  const running = readRunning();
  if (!running) {
    return printAndExit();
  }

  const { edited, bumps, turns, looksUnbumped } = unbumpedState(running);
  const blocks = Number(running.stopBlockCount) || 0;
  const shouldBlock = looksUnbumped && turns >= MIN_TURNS && blocks < MAX_BLOCKS;

  if (!shouldBlock) {
    if (blocks > 0) {
      running.stopBlockCount = 0;
      writeRunning(running);
    }
    return printAndExit();
  }

  running.stopBlockCount = blocks + 1;
  writeRunning(running);

  const message =
    `Session tracking: ${edited} file(s) edited this session, ${bumps} bumps logged. `
    + 'Before finishing, run node scripts/append-session-scorecard.js --bump-file <path> '
    + '(see agent docs/SESSION_TRACKING.md) with chunkNote and navigationPath, '
    + 'then finish your reply normally. '
    + `(This auto-allows after ${MAX_BLOCKS} reminders regardless, so it can't loop forever.)`;

  printAndExit({
    decision: 'block',
    reason: message,
    followup_message: message,
  });
}

function runPrecompact() {
  const running = readRunning();
  if (!running) return printAndExit();

  const { edited, bumps } = unbumpedState(running);
  const trackingReminder = edited > 0 && bumps === 0
    ? ` ${edited} file(s) have been edited with 0 session tracking bumps logged; run `
      + 'node scripts/append-session-scorecard.js --bump-file <path> with chunkNote and '
      + 'navigationPath before detail gets summarized away.'
    : '';

  printAndExit({
    hookSpecificOutput: {
      hookEventName: 'PreCompact',
      additionalContext:
        'CONTEXT EFFICIENCY WARNING: Compaction is about to summarize this conversation. '
        + 'Tell Chase plainly in your next response that this task has become context-heavy, '
        + 'finish the current deliverable, and recommend that he say "perform a momentum handoff" '
        + `before starting another major chunk in a fresh Codex task.${trackingReminder}`,
    },
  });
}

function runContextWarning() {
  const running = readRunning();
  if (!running) return printAndExit();

  const turns = Number(running.turns) || 0;
  const lastWarningTurn = Number(running.lastContextWarningTurn) || 0;
  if (
    turns < CONTEXT_WARNING_TURN_INTERVAL
    || turns - lastWarningTurn < CONTEXT_WARNING_TURN_INTERVAL
  ) {
    return printAndExit();
  }

  running.lastContextWarningTurn = turns;
  writeRunning(running);
  printAndExit({
    hookSpecificOutput: {
      hookEventName: 'UserPromptSubmit',
      additionalContext:
        `CONTEXT EFFICIENCY WARNING: This task has reached ${turns} user messages. `
        + 'Tell Chase plainly in your next response that continued unrelated or major work here '
        + 'will drag more context through each turn. Finish the current deliverable, then recommend '
        + 'that he say "perform a momentum handoff" before starting a fresh Codex task. Do not '
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
